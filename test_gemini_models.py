import os
import google.generativeai as genai
from dotenv import load_dotenv

# .env faylini o'qish
load_dotenv()

# Gemini API kalitini olish
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY topilmadi!")
    exit()

try:
    # Gemini API'ni sozlash
    genai.configure(api_key=GEMINI_API_KEY)
    print("✅ Gemini API muvaffaqiyatli sozlandi.")
    
    # Mavjud modellarni olish
    print("\n🔍 Mavjud modellar:")
    models = genai.list_models()
    
    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
    
    # Test tarjima
    print("\n🧪 Test tarjima:")
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    test_text = "Salom, bu test xabari"
    response = model.generate_content(f"Quyidagi o'zbekcha matnni rus tiliga tarjima qil: {test_text}")
    
    print(f"Original: {test_text}")
    print(f"Tarjima: {response.text}")
    
    print("\n✅ Test muvaffaqiyatli!")
    
except Exception as e:
    print(f"❌ Xatolik: {e}")
