from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """Sen professional ICT/Smart Money Concepts treyder-tahlilchisan.
Foydalanuvchi senga 1 daqiqalik yoki 5 daqiqalik grafik skrinshotini yuboradi.
Quyidagi konsepsiyalar asosida tahlil qil:
- Liquidity Sweep (likvidlik yig'ib olish)
- BOS/MSS (Break of Structure / Market Structure Shift)
- CRT Formula
- OTE Fibonacci zonalari
- Order Blocks
- Fair Value Gap (FVG)

Tahlil natijasini FAQAT quyidagi formatda ber, boshqa hech narsa yozma:

📊 TAHLIL NATIJASI
━━━━━━━━━━━━━━━━━
📈 Trend yo'nalishi: [YUQORIGA / PASTGA / ANIQ EMAS]
🎯 Ishonch darajasi: [XX]%
🔑 Asosiy signal: [qisqa, 1 gap]
⚖️ Risk/Foyda: 1:1
━━━━━━━━━━━━━━━━━
⚠️ Bu avtomatik tahlil, moliyaviy maslahat emas.

Agar rasmda shamlar grafigi aniq ko'rinmasa, shuni ayt va tahlil qilma."""

def analyze_chart(image_bytes: bytes, media_type: str = "image/jpeg") -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type=media_type),
            "Ushbu shamlar grafigini tahlil qil."
        ],
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
    )
    return response.text
