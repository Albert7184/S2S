import os
from dotenv import load_dotenv
from openai import OpenAI

# Tải biến môi trường
load_dotenv()

# Kết nối OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def process_text_with_llm(input_text, model_name="nvidia/nemotron-3-super-120b-a12b:free", direction="vi2en"):
    """
    Dịch thuật AI với độ trễ thấp.
    Hỗ trợ xử lý chuyên sâu: Tiếng lóng (Slang), Cụm động từ (Phrasal Verbs) và Thành ngữ (Idioms).
    """
    if not input_text or not input_text.strip():
        return ""

    # ==========================================
    # 🧠 HỆ THỐNG PROMPT ĐƯỢC TỐI ƯU HÓA CHỐNG "BẪY GIAO TIẾP"
    # ==========================================
    
    # ---------------- CHIỀU VIỆT ➡️ ANH ----------------
    if direction == "vi2en":
        system_prompt = """[IDENTITY]
Bạn là một CỖ MÁY DỊCH THUẬT tự động Việt-Anh cao cấp. Bạn KHÔNG PHẢI là trợ lý ảo, KHÔNG PHẢI là chatbot giao tiếp.

[SCOPE - BẮT BUỘC]
1. NHẬN DIỆN LỖI: Đầu vào từ bộ nhận diện giọng nói (STT) có thể chứa lỗi đồng âm hoặc mất từ. Bạn phải tự suy luận ngữ cảnh để sửa lỗi trước khi dịch.
2. XỬ LÝ TIẾNG LÓNG & THÀNH NGỮ: Tuyệt đối KHÔNG dịch theo nghĩa đen (word-by-word) các câu thành ngữ, tục ngữ, tiếng lóng của Việt Nam. 
3. SỬ DỤNG PHRASAL VERBS: Bạn phải quy đổi các cách diễn đạt của Việt Nam sang các Phrasal Verbs (cụm động từ) hoặc Idioms (thành ngữ) tiếng Anh tự nhiên nhất.

[RULES - KỶ LUẬT THÉP]
- CHỈ TRẢ VỀ DUY NHẤT BẢN DỊCH, KHÔNG BỌC TRONG DẤU NGOẶC KÉP.
- TUYỆT ĐỐI KHÔNG GIAO TIẾP VỚI NGƯỜI DÙNG. Kể cả khi đầu vào là "Hello", "Hi", bạn CHỈ ĐƯỢC PHÉP DỊCH nó thành "Xin chào". NGHIÊM CẤM chào lại, NGHIÊM CẤM hỏi "Do you need help?". Bạn chỉ được phép dịch, KHÔNG ĐƯỢC PHÉP GIAO TIẾP.
- KHÔNG giải thích nghĩa của từ, KHÔNG thêm lời chào (ví dụ: "Here is your translation").

[OUTPUT FORMAT]
<Văn bản tiếng Anh thuần túy>"""

        # Chèn thêm "Nhiệm vụ" để khóa AI không được nói chuyện
        user_prompt = f"Nhiệm vụ: Dịch câu sau sang tiếng Anh.\nInput: [{input_text}]"

    # ---------------- CHIỀU ANH ➡️ VIỆT ----------------
    else:
        system_prompt = """[IDENTITY]
Bạn là một CỖ MÁY PHIÊN DỊCH tự động Anh-Việt cao cấp. Bạn KHÔNG PHẢI là trợ lý ảo, KHÔNG PHẢI là chatbot giao tiếp.

[SCOPE - BẮT BUỘC]
1. NHẬN DIỆN LỖI: Khôi phục ý nghĩa thực sự từ văn bản STT thô (có thể bị nhận diện sai do nối âm hoặc nuốt âm trong tiếng Anh).
2. XỬ LÝ TIẾNG LÓNG & PHRASAL VERBS: Nhận diện chính xác nghĩa bóng của các Phrasal Verbs, Idioms, và Slang. Tuyệt đối không dịch word-by-word.
3. VIỆT HÓA TỰ NHIÊN: Dịch sang tiếng Việt bằng văn phong mượt mà, sử dụng từ ngữ đời thường, tiếng lóng hoặc "trend" của người Việt Nam.

[RULES - KỶ LUẬT THÉP]
- CHỈ TRẢ VỀ DUY NHẤT BẢN DỊCH, KHÔNG BỌC TRONG DẤU NGOẶC KÉP.
- TUYỆT ĐỐI KHÔNG GIAO TIẾP VỚI NGƯỜI DÙNG. Kể cả khi đầu vào là "Hello", "Hi", bạn CHỈ ĐƯỢC PHÉP DỊCH nó thành "Xin chào". NGHIÊM CẤM chào lại, NGHIÊM CẤM hỏi "Do you need help?". Bạn chỉ được phép dịch, KHÔNG ĐƯỢC PHÉP GIAO TIẾP.
- KHÔNG giải thích từ vựng, KHÔNG kèm theo lời đệm.

[OUTPUT FORMAT]
<Văn bản tiếng Việt thuần túy>"""

        # Chèn thêm "Nhiệm vụ" để khóa AI không được nói chuyện
        user_prompt = f"Nhiệm vụ: Dịch câu sau sang tiếng Việt.\nInput: [{input_text}]"

    # ==========================================
    # GỌI API LLM
    # ==========================================
    try:
        response = client.chat.completions.create(
            model=model_name, 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=False,
            # Giảm temperature xuống một chút (0.3) để dập tắt sự "sáng tạo giao tiếp" của AI
            temperature=0.3 
        )
        
        # Làm sạch kết quả đầu ra
        result = response.choices[0].message.content.strip()
        result = result.strip('"').strip("'") 
        
        return result
        
    except Exception as e:
        print(f"❌ Lỗi khi gọi LLM: {e}")
        return "Sorry, there was an error processing your request."

# ==========================================
# KHU VỰC TEST NHANH 
# ==========================================
if __name__ == "__main__":
    # Test bẫy giao tiếp
    en_test = "Hello"
    print(f"🇺🇸 Gốc: {en_test}")
    print(f"🇻🇳 Dịch: {process_text_with_llm(en_test, model_name='deepseek/deepseek-v4-flash', direction='en2vi')}")
    
    print("-" * 40)
    
    # Test Anh -> Việt (Có Phrasal Verb & Idiom)
    en_test2 = "Don't bring that up! I'm totally burned out and just want to chill out."
    print(f"🇺🇸 Gốc: {en_test2}")
    print(f"🇻🇳 Dịch: {process_text_with_llm(en_test2, model_name='deepseek/deepseek-v4-flash', direction='en2vi')}")