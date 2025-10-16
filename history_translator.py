import os
import asyncio
import google.generativeai as genai
from telethon import TelegramClient
from dotenv import load_dotenv

# --- O'ZINGIZNING MA'LUMOTLARINGIZNI KIRITING ---
# BU YERDA FAQAT API_ID VA API_HASH KERAK BO'LADI
load_dotenv()
# 1. Telegram ma'lumotlari
# --- KODNING ASOSIY QISMI ---
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL")
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL")
# Gemini modelini sozlash
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    print("Gemini modeli muvaffaqiyatli sozlandi.")
except Exception as e:
    print(f"Gemini sozlashda xatolik: {e}")
    exit()

# Gemini orqali tarjima qiladigan funksiya
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

# Asosiy funksiya
async def main():
    # DIQQAT: Skript endi BOT SIFATIDA EMAS, SIZNING AKKAUNTINGIZ ORQALI ishlaydi.
    # Bu manba kanal tarixini o'qish uchun zarur.
    # 'user_session' nomli yangi sessiya fayli yaratiladi.
    async with TelegramClient('user_session', API_ID, API_HASH) as client:
        print("Foydalanuvchi akkaunti orqali tizimga kirilmoqda...")
        # await client.start() chaqirish shart emas, `async with` buni o'zi bajaradi

        print("Tizimga kirildi. Eski xabarlarni o'qish boshlandi.")

        message_limit = 5
        print(f"Manba kanaldan oxirgi {message_limit} ta xabar olinmoqda...")
        
        # Xabarlarni o'qib olamiz
        messages = await client.get_messages(SOURCE_CHANNEL, limit=message_limit)
        messages.reverse() # Eskidan yangiga qarab saralash

        print(f"Jami {len(messages)} ta xabar topildi. Tarjima boshlanmoqda...")
        
        i = 0
        for message in messages:
            i += 1
            if not message.text:
                print(f"({i}/{len(messages)}) Xabarda matn yo'q. O'tkazib yuborildi.")
                continue

            print(f"--- ({i}/{len(messages)}) Quyidagi xabar tarjima qilinmoqda: {message.text[:30]}...")
            translated_text = await translate_with_gemini(message.text)

# Tarjima qilingan matn mavjudligini tekshirish
            if translated_text:
                # 1. KANAL NOMINI ALMASHTIRISH:
                # Har bir tarjimada eski nomni yangisiga o'zgartiramiz
                translated_text = translated_text.replace('@nodavlattalim', '@chastnoeobrazovanie')
                
                # 2. XABARNI YUBORISH (UZUN MATNNI TEKSHIRISH BILAN):
                try:
                    # Original xabarda media (rasm/video) borligini tekshiramiz
                    if message.media:
                        # Matnni 1024 belgidan uzun bo'lsa, qisqartiramiz
                        if len(translated_text) > 1024:
                            print("ℹ️ Matn uzun, qisqartirilmoqda...")
                            # Matnni 1000 belgigacha qisqartiramiz va "..." qo'shamiz
                            short_text = translated_text[:1000] + "..."
                            await client.send_file(TARGET_CHANNEL, message.media, caption=short_text)
                            print("✅ Media qisqartirilgan matn bilan yuborildi.")
                        else:
                            # Agar matn sig'sa, media bilan birga (caption sifatida) yuboramiz
                            await client.send_file(TARGET_CHANNEL, message.media, caption=translated_text)
                            print("✅ Media to'liq matn bilan yuborildi.")
                    else:
                        # Agar xabarda media bo'lmasa, shunchaki matnni yuboramiz
                        await client.send_message(TARGET_CHANNEL, translated_text)
                        print("✅ Oddiy matn yuborildi.")
                    
                    print("✅ Tarjima muvaffaqiyatli yuborildi.")
                except Exception as e:
                    print(f"❌ Xabarni yuborishda xatolik: {e}")
            else:
                # Agar tarjimaning o'zi muvaffaqiyatsiz bo'lsa
                print("❌ Tarjima qilishda xatolik yuz berdi.")

            # 3. PAUZANI UZAYTIRISH:
            # Daqiqalik limitga tushmaslik uchun pauzani 5 soniya qilamiz
            print("5 soniya pauza...")
            await asyncio.sleep(5)

        # Sikl tugagach chiqadigan xabar
        print("\n🎉 Barcha eski xabarlar tarjima qilib bo'lindi!")

if __name__ == '__main__':
    asyncio.run(main())
