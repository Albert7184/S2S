import os
import whisper

def transcribe_audio_file(audio_path, lang="vi"):
    """
    Sử dụng mô hình Whisper của OpenAI để chuyển âm thanh thành văn bản.
    Hỗ trợ đa định dạng (mp3, wav, m4a,...) và tự động xử lý tần số mượt mà.
    """
    try:
        # Tải mô hình Whisper 
        # (Ní có thể đổi "base" thành "small" hoặc "medium" nếu muốn chữ ra chính xác hơn nữa)
        model = whisper.load_model("base")
        
        # Định chuẩn mã ngôn ngữ cho Whisper
        whisper_lang = "vi" if lang == "vi" else "en"
        
        # Tiến hành giải mã file âm thanh
        result = model.transcribe(audio_path, language=whisper_lang)
        
        # Trả về văn bản sạch, đã gọt bỏ khoảng trắng thừa
        return result["text"].strip()
        
    except Exception as e:
        return f"Lỗi khi xử lý bằng mô hình Whisper: {str(e)}"