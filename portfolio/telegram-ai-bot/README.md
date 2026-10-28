# Telegram AI Assistant Bot

An AI chat bot for Telegram built with Python, aiogram 3 and the Claude API.
It can be turned into a customer-support bot, FAQ bot or personal assistant by
changing a single setting (`SYSTEM_PROMPT`).

## Features

- Remembers the conversation for each user
- `/start`, `/help`, `/reset` commands
- Custom persona via `SYSTEM_PROMPT` (support agent, tutor, sales assistant…)
- Handles long answers (splits them to fit Telegram's message limit)
- Graceful error handling (rate limits, API errors)

## Quick start

1. Create a bot with [@BotFather](https://t.me/BotFather) and copy the token.
2. Get an API key at [console.anthropic.com](https://console.anthropic.com).
3. Install and run:

```bash
cd portfolio/telegram-ai-bot
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then put your tokens into .env
python bot.py
```

## Example: support bot for a business

```env
SYSTEM_PROMPT=You are the support assistant of Mario's Pizza. Menu: Margherita $10, Pepperoni $12. Delivery 30-45 min, free over $25. If you don't know the answer, ask the customer to call +1-555-0100.
```

## Tech stack

Python 3.11+ · aiogram 3 · Anthropic Claude API · python-dotenv
