import os
import asyncio
import openai
from telethon import TelegramClient
from openai import AsyncOpenAI
from dotenv import load_dotenv
# --- FOYDALANUVCHI MA'LUMOTLARI ---
load_dotenv()

# Ma'lumotlarni olish
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL")
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL")

# OpenAI sozlamasi
openai.api_key = OPENAI_API_KEY

# --- FUNKSIYA: ChatGPT orqali tarjima ---
async def translate_with_chatgpt(text_to_translate):
    prompt = f"""Quyidagi o‘zbekcha matnni faqat rus tiliga tarjima qil.
Faqat tarjima qilingan matnni qaytar.

O‘zbekcha matn:
{text_to_translate}
"""
    try:
        response = await openai.chat.completions.acreate(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ ChatGPT tarjima xatosi: {e}")
        return None

# --- ASOSIY FUNKSIYA ---
async def main():
    async with TelegramClient('user_session', API_ID, API_HASH) as client:
        print("✅ Telegram foydalanuvchi sifatida tizimga kirdingiz.")
        message_limit = 4

        print(f"📥 So‘nggi {message_limit} ta xabar olinmoqda...")
        messages = await client.get_messages(SOURCE_CHANNEL, limit=message_limit)
        messages.reverse()  # Eskidan yangiga

        for idx, message in enumerate(messages, 1):
            if not message.text:
                print(f"({idx}) Xabarda matn yo‘q. O‘tkazildi.")
                continue

            print(f"({idx}) Tarjimaga tayyor: {message.text[:50]}...")
            translated_text = await translate_with_chatgpt(message.text)

            if translated_text:
                translated_text = translated_text.replace('@nodavlattalim', '@chastnoeobrazovanie')

                try:
                    if message.media:
                        if len(translated_text) > 1024:
                            print("📦 Media va uzun matn alohida yuboriladi.")
                            await client.send_file(TARGET_CHANNEL, message.media)
                            await client.send_message(TARGET_CHANNEL, translated_text)
                        else:
                            await client.send_file(TARGET_CHANNEL, message.media, caption=translated_text)
                    else:
                        await client.send_message(TARGET_CHANNEL, translated_text)

                    print("✅ Xabar yuborildi.")
                except Exception as e:
                    print(f"❌ Yuborishda xatolik: {e}")
            else:
                print("❌ Tarjima olish muvaffaqiyatsiz bo‘ldi.")

            await asyncio.sleep(5)

        print("\n🎉 Barcha xabarlar tarjima qilindi!")

# --- DASTURNI ISHGA TUSHURISH ---
if __name__ == '__main__':
    asyncio.run(main())
