# Telegram Tarjima Botlari

Bu loyiha Telegram kanallar orasida avtomatik tarjima qiluvchi botlar to'plamidir. O'zbek tilidan Rus tiliga tarjima qiladi.

## 🚀 Xususiyatlar

- **Real-time tarjima**: Yangi xabarlarni avtomatik tarjima qiladi
- **Tarixiy xabarlar**: Eski xabarlarni o'qib tarjima qiladi
- **Ko'p AI platformalar**: Gemini AI, ChatGPT, Google Translate
- **Media qo'llab-quvvatlash**: Rasm, video va boshqa fayllar bilan ishlaydi
- **Xavfsizlik**: API kalitlari `.env` fayl orqali saqlanadi

## 📁 Fayllar

### 1. `history_translator.py`
- **Maqsad**: Eski xabarlarni Gemini AI orqali tarjima qiladi
- **Ishlash usuli**: Foydalanuvchi akkaunti orqali
- **Xususiyat**: Oxirgi 5 ta xabarni o'qib tarjima qiladi

### 2. `gemini_translator_bot.py`
- **Maqsad**: Yangi xabarlarni real vaqtda Gemini AI orqali tarjima qiladi
- **Ishlash usuli**: Bot sifatida
- **Xususiyat**: Yangi xabarlarni avtomatik ushlab oladi

### 3. `chatgpt_history.py`
- **Maqsad**: Eski xabarlarni ChatGPT orqali tarjima qiladi
- **Ishlash usuli**: Foydalanuvchi akkaunti orqali
- **Xususiyat**: Oxirgi 4 ta xabarni o'qib tarjima qiladi

### 4. `translator_bot.py`
- **Maqsad**: Yangi xabarlarni Google Translate orqali tarjima qiladi
- **Ishlash usuli**: Bot sifatida
- **Xususiyat**: Eng oddiy va tez tarjima usuli

## 🛠️ O'rnatish

### 1. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 2. API kalitlarini olish

#### Telegram API:
1. [my.telegram.org](https://my.telegram.org) ga kiring
2. API ID va API Hash oling

#### Bot Token:
1. [@BotFather](https://t.me/BotFather) ga yozing
2. Yangi bot yarating va token oling

#### Gemini AI:
1. [Google AI Studio](https://makersuite.google.com/app/apikey) ga kiring
2. API kalit yarating

#### OpenAI:
1. [OpenAI Platform](https://platform.openai.com/api-keys) ga kiring
2. API kalit yarating

### 3. Konfiguratsiya

`.env` fayl yarating va quyidagi ma'lumotlarni kiriting:

```env
# Telegram API ma'lumotlari
API_ID=your_api_id_here
API_HASH=your_api_hash_here
BOT_TOKEN=your_bot_token_here

# AI API kalitlari
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Kanallar
SOURCE_CHANNEL=your_source_channel_here
TARGET_CHANNEL=your_target_channel_here
```

## 🚀 Ishlatish

### Tarixiy xabarlarni tarjima qilish (Gemini AI):
```bash
python history_translator.py
```

### Real-time bot (Gemini AI):
```bash
python gemini_translator_bot.py
```

### Tarixiy xabarlarni tarjima qilish (ChatGPT):
```bash
python chatgpt_history.py
```

### Real-time bot (Google Translate):
```bash
python translator_bot.py
```

## ⚙️ Sozlamalar

### Kanal nomlarini o'zgartirish:
Kodlarda `@nodavlattalim` ni `@chastnoeobrazovanie` ga o'zgartirish:
```python
translated_text = translated_text.replace('@nodavlattalim', '@chastnoeobrazovanie')
```

### Xabar limitini o'zgartirish:
```python
message_limit = 5  # Kerakli sonni kiriting
```

### Pauza vaqti:
```python
await asyncio.sleep(5)  # Soniyalarda
```

## 🔧 Xatoliklar bilan ishlash

### Umumiy xatoliklar:
1. **API kalit xatosi**: `.env` faylda to'g'ri kalitlar borligini tekshiring
2. **Kanal xatosi**: Kanal nomlarini to'g'ri kiriting
3. **Import xatosi**: Barcha kutubxonalar o'rnatilganligini tekshiring

### Media fayllar bilan ishlash:
- Matn 1024 belgidan uzun bo'lsa, media va matn alohida yuboriladi
- Media fayllar avtomatik qo'llab-quvvatlanadi

## 📝 Eslatmalar

- Bot ishlashi uchun kanalga admin huquqlari berilishi kerak
- Foydalanuvchi akkaunti orqali ishlaydigan skriptlar uchun telefon raqam tasdiqlash kerak
- API limitlariga e'tibor bering
- Pauza vaqtlarini o'zgartirib, rate limitlardan qoching

## 🤝 Yordam

Agar muammo yuz bersa:
1. Xatolik xabarlarini diqqat bilan o'qing
2. API kalitlarini tekshiring
3. Kanal nomlarini to'g'ri kiriting
4. Kutubxonalar to'liq o'rnatilganligini tekshiring

## 📄 Litsenziya

Bu loyiha ochiq manba kodidir. O'zingizning ehtiyojlaringiz uchun ishlatishingiz mumkin.
