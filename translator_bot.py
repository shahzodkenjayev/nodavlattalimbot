import os
from telethon import TelegramClient, events
from googletrans import Translator

# 1. O'ZINGIZNING MA'LUMOTLARINGIZNI KIRITING
API_ID = 21167390  # my.telegram.org dan olingan api_id
API_HASH = '4e78786ac13f6cf7337d78b1396a4e68'  # my.telegram.org dan olingan api_hash
BOT_TOKEN = '8178185778:AAEs43_cIPSYACGkhA-oATyXTGdI4ImYyZ8'  # @BotFather dan olingan token

# Kanallar manzili
SOURCE_CHANNEL = 'nodavlattalim'  # Kuzatiladigan kanal (bez @)
TARGET_CHANNEL = '@nodavlattalim_ru'  # Post joylanadigan kanal

# Tarjimon ob'ektini yaratish
translator = Translator()

# Botni TelegramClient orqali ishga tushiramiz, bu unga boshqa kanallarni ham o'qish imkonini beradi.
# "bot_session" nomli fayl yaratiladi, u sessiya ma'lumotlarini saqlaydi.
bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handle_new_message(event):
    """
    Manba kanaldagi yangi xabarlarni ushlab oladi va tarjima qilib, maqsad kanalga yuboradi.
    """
    message_text = event.message.text
    print(f"Original xabar olindi: {message_text[:30]}...")

    if not message_text:
        # Agar xabarda matn bo'lmasa (masalan, faqat rasm), hech narsa qilmaymiz
        print("Xabarda matn yo'q.")
        return

    try:
        # Matnni o'zbek tilidan ('uz') rus tiliga ('ru') tarjima qilish
        translated = translator.translate(message_text, src='uz', dest='ru')
        translated_text = translated.text

        print(f"Tarjima qilindi: {translated_text[:30]}...")

        # Tarjima qilingan xabarni maqsad kanalga yuborish
        await bot.send_message(TARGET_CHANNEL, translated_text)
        print("Xabar muvaffaqiyatli yuborildi.")

    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

async def main():
    print("Bot ishga tushdi va yangi xabarlarni kutmoqda...")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    bot.loop.run_until_complete(main())
