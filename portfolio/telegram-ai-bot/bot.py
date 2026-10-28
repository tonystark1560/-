"""Telegram AI assistant bot powered by Claude.

Features:
- remembers the conversation per user (in memory)
- /start, /help, /reset commands
- configurable system prompt (e.g. "support agent for a pizza shop")
- splits long answers to fit Telegram's 4096-char limit
"""

import asyncio
import logging
import os
from collections import defaultdict

import anthropic
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-5-5")
SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "You are a friendly, concise assistant in a Telegram chat. "
    "Answer in the user's language. Keep answers short unless asked for detail.",
)
MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "20"))
TELEGRAM_LIMIT = 4096

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("bot")

claude = anthropic.AsyncAnthropic()  # reads ANTHROPIC_API_KEY from the environment
dp = Dispatcher()

# user_id -> list of {"role": ..., "content": str}
history: dict[int, list[dict]] = defaultdict(list)


async def ask_claude(user_id: int, text: str) -> str:
    messages = history[user_id]
    messages.append({"role": "user", "content": text})

    response = await claude.beta.messages.create(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        messages=messages,
        output_config={"effort": "low"},  # chat replies don't need deep reasoning
        # If the model declines, the API retries on a fallback model automatically.
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    )

    if response.stop_reason == "refusal":
        messages.pop()  # don't keep the declined question in history
        return "Sorry, I can't help with that request."

    answer = "".join(b.text for b in response.content if b.type == "text").strip()
    messages.append({"role": "assistant", "content": answer})

    # Keep the history bounded; it must start with a user message.
    if len(messages) > MAX_HISTORY_MESSAGES:
        del messages[: len(messages) - MAX_HISTORY_MESSAGES]
        while messages and messages[0]["role"] != "user":
            messages.pop(0)

    return answer or "…"


def split_for_telegram(text: str) -> list[str]:
    return [text[i : i + TELEGRAM_LIMIT] for i in range(0, len(text), TELEGRAM_LIMIT)]


@dp.message(CommandStart())
async def on_start(message: Message) -> None:
    await message.answer(
        "Hi! I'm an AI assistant. Just send me a message.\n"
        "/reset — start a new conversation\n/help — help"
    )


@dp.message(Command("help"))
async def on_help(message: Message) -> None:
    await message.answer(
        "Send any question and I'll answer. I remember our conversation "
        "until you type /reset."
    )


@dp.message(Command("reset"))
async def on_reset(message: Message) -> None:
    history.pop(message.from_user.id, None)
    await message.answer("Conversation cleared.")


@dp.message(F.text)
async def on_text(message: Message) -> None:
    await message.bot.send_chat_action(message.chat.id, "typing")
    try:
        answer = await ask_claude(message.from_user.id, message.text)
    except anthropic.RateLimitError:
        history[message.from_user.id].pop()
        answer = "Too many requests right now, please try again in a minute."
    except anthropic.APIError:
        log.exception("Claude API error")
        history[message.from_user.id].pop()
        answer = "Something went wrong, please try again."

    for chunk in split_for_telegram(answer):
        await message.answer(chunk)


async def main() -> None:
    bot = Bot(TELEGRAM_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
