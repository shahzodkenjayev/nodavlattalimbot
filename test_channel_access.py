import os
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SOURCE_CHANNEL = int(os.getenv("SOURCE_CHANNEL"))
TARGET_CHANNEL = int(os.getenv("TARGET_CHANNEL"))

async def test_channel_access():
    async with TelegramClient('user_session', API_ID, API_HASH) as client:
        print("🔍 Kanal huquqlarini tekshirilmoqda...")
        
        try:
            # Manba kanal ma'lumotlarini olish
            source_entity = await client.get_entity(SOURCE_CHANNEL)
            print(f"✅ Manba kanal: {source_entity.title} (@{source_entity.username})")
            print(f"   ID: {source_entity.id}")
            print(f"   Turi: {type(source_entity).__name__}")
            
            # Oxirgi 3 ta xabarni olish
            messages = await client.get_messages(SOURCE_CHANNEL, limit=3)
            print(f"📥 Oxirgi {len(messages)} ta xabar topildi:")
            
            for i, msg in enumerate(messages, 1):
                if msg.text:
                    print(f"   {i}. {msg.text[:50]}...")
                else:
                    print(f"   {i}. [Media xabar]")
            
        except Exception as e:
            print(f"❌ Manba kanal xatosi: {e}")
        
        try:
            # Maqsad kanal ma'lumotlarini olish
            target_entity = await client.get_entity(TARGET_CHANNEL)
            print(f"✅ Maqsad kanal: {target_entity.title} (@{target_entity.username})")
            print(f"   ID: {target_entity.id}")
            print(f"   Turi: {type(target_entity).__name__}")
            
            # Test xabar yuborish
            test_message = "🤖 Test xabar - bot ishlayotganini tekshirish"
            await client.send_message(TARGET_CHANNEL, test_message)
            print("✅ Test xabar muvaffaqiyatli yuborildi!")
            
        except Exception as e:
            print(f"❌ Maqsad kanal xatosi: {e}")

if __name__ == '__main__':
    asyncio.run(test_channel_access())
