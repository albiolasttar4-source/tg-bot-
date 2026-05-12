import telebot
import requests
import os
import time

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

    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        r.raise_for_status()
        ans = r.json()["choices"][0]["message"]["content"]
        bot.reply_to(m, ans)
    except Exception as e:
        bot.reply_to(m, f"Error: {str(e)}")

print("Bot running...")
while True:
    try:
        bot.infinity_polling(timeout=60)
    except Exception as e:
        print(f"Polling error: {e}")
        time.sleep(5)
