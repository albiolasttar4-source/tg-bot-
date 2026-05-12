import telebot
import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda m: True)
def reply(m):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a helpful Tagalog AI."},
            {"role": "user", "content": m.text}
        ]
    }

    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=data
    )

    ans = r.json()["choices"][0]["message"]["content"]
    bot.reply_to(m, ans)

print("Bot running...")
bot.infinity_polling()
