import os
from dotenv import load_dotenv
from openai import OpenAI

# Tải biến môi trường
load_dotenv()

def get_coach_client(model_name):
    """
    Hàm động kiểm tra và lấy đúng API Key tương ứng với từng Model từ Secrets cho Coach Mode.
    Giúp hệ thống tự chuyển mạch Key khi user chọn model trên UI mà không làm sập app.
    """
    # Nếu chọn DeepSeek Flash
    if "deepseek" in model_name:
        api_key = os.getenv("OPENROUTER_API_KEY_DEEPSEEK")
    # Nếu chọn Nemotron
    elif "nemotron" in model_name:
        api_key = os.getenv("OPENROUTER_API_KEY_NEMOTRON")
    # Phương án dự phòng (Fallback) nếu chạy local bằng file .env cũ
    else:
        api_key = os.getenv("OPENROUTER_API_KEY")

    # Khởi tạo OpenAI client với Key tương ứng
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )
    return client

def process_with_coach(input_text, model_name="nvidia/nemotron-3-super-120b-a12b:free", direction="vi2en"):
    """
    Chế độ Gia Sư: Trả về Bản dịch + Gợi ý từ vựng/Sửa lỗi ngữ pháp.
    """
    if not input_text or not input_text.strip():
        return ""

    if direction == "vi2en":
        system_prompt = """
[IDENTITY]
Bạn là một Thầy giáo dạy tiếng Anh chuẩn bản xứ. Nhiệm vụ của bạn là dịch câu tiếng Việt sang tiếng Anh, đồng thời hướng dẫn học viên cách dùng từ hay hơn.

[RULES]
- Bạn phải biết tất cả các câu thành ngữ tục ngữ của Việt Nam để gợi ý cho học viên cách nói hay hơn và dịch đươc nghĩa của nó sang tiếng Anh.
- Giải thích bằng tiếng việt và cho ví dụ bằng tiếng anh để học viên dễ hiểu hơn.
- Nếu không chắc chắn, hãy chọn cách dịch tự nhiên nhất.
- Dùng cố định định đại từ nhân xưng "tớ" và "cậu" cho tiếng việt để tạo cảm giác thân thiện, gần gũi như đang nói chuyện với bạn bè. SỬ DỤNG "I" and "you". CHO TIẾNG ANH.
- TUYỆT ĐỐI KHÔNG ĐƯỢC GIAO TIẾP BẤT KỲ ĐIỀU GÌ, CHỈ CẦN DỊCH VÀ HƯỚNG DẪN CÁCH NÓI HAY HƠN CHO HỌC VIÊN.

[OUTPUT FORMAT - BẮT BUỘC TRẢ VỀ ĐÚNG FORMAT NÀY DƯỚI DẠNG MARKDOWN]
**🎯 Bản dịch chuẩn:** [Câu dịch tiếng Anh tự nhiên nhất]

**💡 Gợi ý nâng cao (Vocabulary/Idioms):**
- [Từ vựng/Cụm từ 1]: [Giải nghĩa ngắn gọn]
- [Từ vựng/Cụm từ 2]: [Giải nghĩa ngắn gọn]
- Những chỗ nào giải thích thì BẮT BUỘC đặt trong dấu ngoặc kép "" để học viên dễ nhận biết. KHÔNG ĐƯỢC SỬ DỤNG DẤU NÀO NGOÀI DẤU NGOẶC KÉP "" ĐỂ GIẢI THÍCH, VÍ DỤ: "Cụm từ "hit the books" 

"""
        user_prompt = f"Học viên nói: [{input_text}]"

    else:
        system_prompt = """
[IDENTITY]
- Bạn là một Thầy giáo tiếng Anh chấm điểm cho học viên. Học viên sẽ nói 1 câu tiếng Anh (do STT nhận diện). Nhiệm vụ của bạn là dịch nó sang tiếng Việt TUYỆT ĐỐI KHÔNG ĐƯỢC GIAO TIẾP BẤT KỲ ĐIỀU GÌ, và sửa lỗi ngữ pháp/cách dùng từ cho học viên (nếu có).
- Bạn phải biết tất cả các câu thành ngữ tục ngữ của tiếng anh để gợi ý cho học viên cách nói hay hơn và dịch đươc nghĩa của nó sang tiếng Việt.

[RULES]
- Bạn phải biết tất cả các câu thành ngữ tục ngữ của tiếng Anh để gợi ý cho học viên cách nói hay hơn và dịch đươc nghĩa của nó sang tiếng Việt.
- Giải thích bằng tiếng anh và cho ví dụ bằng tiếng việt để học viên dễ hiểu hơn.
- Nếu không chắc chắn, hãy chọn cách dịch tự nhiên nhất.
- Dùng cố định định đại từ nhân xưng "Tớ" và "Cậu" cho tiếng việt để tạo cảm giác thân thiện, gần gũi như đang nói chuyện với bạn bè. SỬ DỤNG "I" and "You". CHO TIẾNG ANH.
- TUYỆT ĐỐI KHÔNG ĐƯỢC GIAO TIẾP BẤT KỲ ĐIỀU GÌ, CHỈ CẦN DỊCH VÀ HƯỚNG DẪN CÁCH NÓI HAY HƠN CHO HỌC VIÊN.

[OUTPUT FORMAT - BẮT BUỘC TRẢ VỀ ĐÚNG FORMAT NÀY DƯỚI DẠNG MARKDOWN]

**🎯 Dịch nghĩa:** [Câu dịch tiếng Việt tự nhiên]

**🛠️ Phân tích & Sửa lỗi:**
- Lỗi phát âm/ngữ pháp: [Chỉ ra lỗi và sửa lại cho đúng]
- Cách nói hay hơn (Native way): [Gợi ý cách người bản xứ hay dùng]
- Những chỗ nào giải thích thì BẮT BUỘC đặt trong dấu ngoặc kép "" để học viên dễ nhận biết. KHÔNG ĐƯỢC SỬ DỤNG DẤU NÀO NGOÀI DẤU NGOẶC KÉP "" ĐỂ GIẢI THÍCH, VÍ DỤ: "Cụm từ "hit the books" 
"""
        user_prompt = f"Học viên nói tiếng Anh: [{input_text}]"

    try:
        # Gọi hàm lấy client động dựa vào model_name thay vì biến toàn cục cũ
        client = get_coach_client(model_name)
        
        response = client.chat.completions.create(
            model=model_name, 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=False,
            temperature=0.4 
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Lỗi Coach Engine: {e}")
        return "Lỗi kết nối Gia sư. Vui lòng thử lại!"