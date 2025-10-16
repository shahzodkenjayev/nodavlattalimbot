import os
import google.generativeai as genai
from telethon import TelegramClient, events
from dotenv import load_dotenv
# --- O'ZINGIZNING MA'LUMOTLARINGIZNI KIRITING ---

# 1. Telegram ma'lumotlari (avvalgi koddan)
# --- ENV o'qish ---
load_dotenv()

# Telegram ma’lumotlari
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# OpenAI API (eski versiya uchun)
# openai.api_key = os.getenv("OPENAI_API_KEY")

# Kanallar
SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL")
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL")

# --- KODNING ASOSIY QISMI ---

# Gemini modelini sozlash
# Botni TelegramClient orqali ishga tushiramiz
# "bot_session" nomli fayl yaratiladi, u sessiya ma'lumotlarini saqlaydi.
bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

async def translate_with_gemini(text_to_translate):
    prompt = f"""Quyidagi o'zbekcha matnni faqat rus tiliga tarjima qil.
Javobingda faqat tarjima qilingan matn bo'lsin.
Hech qanday qo'shimcha izoh, sarlavha yoki tushuntirish qo'shma. Faqat tarjimaning o'zini qaytar.

O'zbekcha matn:
---
{text_to_translate}
---
"""
    try:
        response = await model.generate_content_async(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini tarjima xatosi: {e}")
        return None

# ChatGPT funksiyasi (hozircha ishlatilmaydi)
# async def translate_with_chatgpt(text_to_translate):
#     prompt = f"""Quyidagi o'zbekcha matnni rus tiliga tarjima qil.
# Faqat tarjima qilingan matnni qaytar. Qo'shimcha izoh yoki sarlavha yozma.
# 
# Matn:
# {text_to_translate}"""
# 
#     try:
#         response = await openai.ChatCompletion.acreate(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.3
#         )
#         return response.choices[0].message['content'].strip()
#     except Exception as e:
#         print(f"ChatGPT tarjimada xatolik: {e}")
#         return None


# Manba kanaldagi yangi xabarlarni kuzatuvchi funksiya
@bot.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handle_new_message(event):
    """
    Manba kanaldagi yangi xabarlarni ushlab oladi, tarjima qiladi va maqsad kanalga yuboradi.
    """
    original_message = event.message
    
    # Rasm yoki video bilan kelgan matnni (caption) yoki oddiy matnni olamiz
    message_text = original_message.text
    
    if not message_text:
        print("Xabarda matn topilmadi. O'tkazib yuborildi.")
        return

    print(f"Original xabar olindi: {message_text[:50]}...")

    # Matnni Gemini orqali tarjima qilish
    translated_text = await translate_with_gemini(message_text)

    if translated_text:
        translated_text = translated_text.replace('@nodavlattalim', '@chastnoeobrazovanie')
    if translated_text:
        print(f"Tarjima qilindi: {translated_text[:50]}...")
        original_message = event.message
        try:
            if original_message.media:
                # Matnni 1024 belgidan uzun bo'lsa, qisqartiramiz
                if len(translated_text) > 1024:
                    print("ℹ️ Matn uzun, qisqartirilmoqda...")
                    # Matnni 1000 belgigacha qisqartiramiz va "..." qo'shamiz
                    short_text = translated_text[:1000] + "..."
                    await bot.send_file(TARGET_CHANNEL, original_message.media, caption=short_text)
                    print("✅ Media qisqartirilgan matn bilan yuborildi.")
                else:
                    # Agar matn sig'sa, caption sifatida yuboramiz
                    await bot.send_file(TARGET_CHANNEL, original_message.media, caption=translated_text)
                    print("✅ Media to'liq matn bilan yuborildi.")
            else:
                # Agar xabarda media bo'lmasa, oddiy matn sifatida yuboramiz
                await bot.send_message(TARGET_CHANNEL, translated_text)
                print("✅ Oddiy matn yuborildi.")
            
            print("Tarjima qilingan xabar muvaffaqiyatli yuborildi.")
        except Exception as e:
            print(f"❌ Xabarni yuborishda xatolik: {e}")
        # Original xabardagi rasm yoki videoni saqlab, tarjima qilingan matn bilan yuborish


# Botni ishga tushirish
async def main():
    print("Bot ishga tushdi va Gemini yordamida tarjimani kutmoqda...")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")
    except Exception as e:
        print(f"Bot xatosi: {e}")
