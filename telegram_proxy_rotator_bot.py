#!/usr/bin/env python3
# coding: utf-8
"""
Telegram bot that controls proxy rotation.
Commands:
  /start - help
  /start_rotation - start proxy rotation
  /stop_rotation  - stop rotation
  /status         - show current status
  /set_interval X - change rotation interval (seconds)

ENV:
  TELEGRAM_BOT_TOKEN - Bot token (overrides constant if present)
"""

import os
import asyncio
import aiohttp
import random
import logging
from typing import List, Optional
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ---------------- Configuration ----------------
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TEST_URL = "https://httpbin.org/ip"
DEFAULT_INTERVAL = 0.5
PROXIES: List[str] = [
    # "http://user:pass@proxy1.example.com:3128",
    # "http://user:pass@proxy2.example.com:3128",
]
MAX_CONCURRENT = 10
# ------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("rotator_bot")


class ProxyRotator:
    def __init__(self, proxies: List[str], interval: float = DEFAULT_INTERVAL):
        self.proxies = proxies
        self.interval = interval
        self.stop_event: asyncio.Event = asyncio.Event()
        self._task: Optional[asyncio.Task] = None
        self._running: bool = False
        self._last_proxy: Optional[str] = None
        self._iteration: int = 0

    async def _fetch(self, session: aiohttp.ClientSession, proxy: Optional[str]) -> Optional[str]:
        try:
            kwargs = {}
            if proxy:
                kwargs["proxy"] = proxy
            async with session.get(TEST_URL, timeout=10, **kwargs) as resp:
                text = await resp.text()
                logger.info("OK via %s [%s]", proxy or "direct", resp.status)
                return text.strip()
        except Exception as e:
            logger.warning("Proxy failed %s: %s", proxy or "direct", str(e))
            return None

    async def _rotate(self) -> None:
        conn = aiohttp.TCPConnector(limit_per_host=MAX_CONCURRENT)
        async with aiohttp.ClientSession(connector=conn) as session:
            while not self.stop_event.is_set():
                self._iteration += 1
                proxy = random.choice(self.proxies) if self.proxies else None
                self._last_proxy = proxy
                await self._fetch(session, proxy)
                try:
                    await asyncio.wait_for(self.stop_event.wait(), timeout=self.interval)
                except asyncio.TimeoutError:
                    continue

    async def start(self) -> bool:
        if self._running:
            return False
        if not self.proxies:
            logger.warning("Proxy list is empty; rotating with direct connection checks only.")
        self.stop_event.clear()
        self._task = asyncio.create_task(self._rotate())
        self._running = True
        logger.info("Rotation started")
        return True

    async def stop(self) -> bool:
        if not self._running:
            return False
        self.stop_event.set()
        if self._task:
            await self._task
        self._running = False
        logger.info("Rotation stopped")
        return True

    def status(self) -> str:
        if self._running:
            return (
                f"✅ Rotation active | Interval: {self.interval}s | "
                f"Iteration: {self._iteration} | Last proxy: {self._last_proxy}"
            )
        else:
            return "🛑 Rotation stopped."

    def set_interval(self, value: float) -> float:
        self.interval = value
        return self.interval


rotator = ProxyRotator(PROXIES, DEFAULT_INTERVAL)

# ---------------- Telegram Handlers ----------------
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Привет! Я бот для управления ротацией прокси.\n"
        "Команды:\n"
        "/start_rotation — запустить ротацию\n"
        "/stop_rotation — остановить\n"
        "/status — статус\n"
        "/set_interval <сек> — изменить интервал"
    )

async def start_rotation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        started = await rotator.start()
        if started:
            await update.message.reply_text("🚀 Ротация прокси запущена!")
        else:
            await update.message.reply_text("⚠️ Уже запущено.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка запуска: {e}")

async def stop_rotation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        stopped = await rotator.stop()
        if stopped:
            await update.message.reply_text("🛑 Ротация остановлена.")
        else:
            await update.message.reply_text("ℹ️ Ротация уже остановлена.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка остановки: {e}")

async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(rotator.status())

async def set_interval_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Укажите интервал в секундах: /set_interval 1.5")
        return
    try:
        value = float(context.args[0])
        if value <= 0:
            raise ValueError("interval must be positive")
        rotator.set_interval(value)
        await update.message.reply_text(f"⏱ Интервал установлен: {value}s")
    except Exception as e:
        await update.message.reply_text(f"Неверное значение: {e}")


def main() -> None:
    token = TELEGRAM_BOT_TOKEN
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("start_rotation", start_rotation))
    application.add_handler(CommandHandler("stop_rotation", stop_rotation))
    application.add_handler(CommandHandler("status", status_cmd))
    application.add_handler(CommandHandler("set_interval", set_interval_cmd))

    logger.info("Bot is starting...")
    application.run_polling()


if __name__ == "__main__":
    main()
