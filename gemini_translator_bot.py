import os
import asyncio
import google.generativeai as genai
from telethon import TelegramClient, events
from dotenv import load_dotenv

# --- Sozlamalar ---
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SOURCE_CHANNEL = int(os.getenv("SOURCE_CHANNEL"))  # ID raqam bo'lishi kerak
TARGET_CHANNEL = int(os.getenv("TARGET_CHANNEL"))  # ID raqam bo'lishi kerak

# --- Gemini modelini sozlash ---
try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Sizning akkauntingiz uchun mavjud bo'lgan eng yaxshi modelni tanlaymiz
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest') 
    print("✅ Gemini modeli muvaffaqiyatli sozlandi ('gemini-1.5-flash-latest').")
except Exception as e:
    print(f"❌ Gemini sozlashda xatolik: {e}")
    exit()

# --- Telegram Client sozlash (BOT SIFATIDA EMAS, FOYDALANUVCHI SIFATIDA) ---
# 'user_session' fayli avtomatik yaratiladi
client = TelegramClient('user_session', API_ID, API_HASH)

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
        print(f"❌ Gemini tarjima xatosi: {e}")
        return None

# Manba kanaldagi yangi xabarlarni kuzatuvchi funksiya
@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handle_new_message(event):
    print("🔔 Event handler ishga tushdi!")
    original_message = event.message
    message_text = original_message.text
    
    print(f"📨 Xabar ID: {original_message.id}")
    print(f"📨 Xabar matni: {message_text}")
    
    if not message_text:
        print("ℹ️ Xabarda matn topilmadi. O'tkazib yuborildi.")
        return

    print(f"📥 Yangi xabar olindi: {message_text[:50]}...")
    
    translated_text = await translate_with_gemini(message_text)

    if translated_text:
        translated_text = translated_text.replace('@nodavlattalim', '@chastnoeobrazovanie')
        print(f"🔄 Tarjima qilindi: {translated_text[:50]}...")
        try:
            if original_message.media:
                caption = translated_text[:1024] # Telegram caption limiti
                await client.send_file(TARGET_CHANNEL, original_message.media, caption=caption)
                print("📤 Media bilan tarjima yuborildi.")
            else:
                await client.send_message(TARGET_CHANNEL, translated_text)
                print("📤 Matnli tarjima yuborildi.")
        except Exception as e:
            print(f"❌ Xabarni yuborishda xatolik: {e}")
    else:
        print("❌ Tarjima qilishda xatolik yuz berdi.")

async def main():
    print("🤖 Tarjimon ishga tushdi. Shaxsiy akkaunt orqali yangi xabarlar kutilmoqda...")
    await client.start()
    print(f"✅ Tizimga kirildi. '{SOURCE_CHANNEL}' kanalidagi yangi xabarlar kuzatilmoqda.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (TypeError, ValueError):
        print("\nXATOLIK: .env faylida SOURCE_CHANNEL yoki TARGET_CHANNEL uchun to'g'ri ID raqam kiriting (masalan, -100123456789).")
    except Exception as e:
        print(f"\n❌ Botda kutilmagan xatolik: {e}")