import asyncio
import edge_tts
import pygame
import os
import time

def play_text_to_speech(text, target_lang="en"):
    """
    Phát âm thanh ra loa sử dụng Microsoft Edge TTS (Đã sửa lỗi đồng bộ cho Streamlit Cloud).
    Giữ nguyên logic kiểm tra chuỗi và tên hàm cũ của ní.
    """
    # 1. Giữ nguyên logic check text rỗng của ní
    if not text or not text.strip():
        return
        
    # 2. Giữ nguyên logic tự động trỏ đúng giọng bản xứ theo ngôn ngữ (vi/en)
    if target_lang == "vi":
        voice = "vi-VN-NamMinhNeural"
    else:
        voice = "en-US-ChristopherNeural"

    # In log ra terminal giống như phong cách file cũ của ní
    print(f"🔊 [{target_lang.upper()}] Đang phát: '{text}'")
    
    output_file = "temp_tts_output.mp3"

    # Hàm bất đồng bộ kết nối server Microsoft để lấy audio
    async def _generate_audio():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)

    try:
        # Chạy luồng tải audio
        asyncio.run(_generate_audio())

        # Khởi tạo pygame mixer để phát âm thanh ra loa
        pygame.mixer.init()
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()

        # Giữ luồng chạy cho đến khi phát xong hết câu
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Giải phóng file để hệ điều hành không giữ khóa
        pygame.mixer.quit()
        time.sleep(0.1) 
        
        # Xóa file tạm thời
        if os.path.exists(output_file):
            os.remove(output_file)

    except Exception as e:
        print(f"❌ Lỗi phát TTS: {e}")

# ==========================================
# KHU VỰC TEST NHANH (GIỮ NGUYÊN KHUNG CỦA NÍ)
# ==========================================
if __name__ == "__main__":
    play_text_to_speech("Hello, this is a speed test for the English voice.", target_lang="en")
    play_text_to_speech("Xin chào, tôi là giọng nói tiếng Việt được tối ưu hóa siêu tốc.", target_lang="vi")
    print("🎉 Hoàn tất quá trình test TTS song ngữ!")