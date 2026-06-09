import asyncio
import edge_tts
import os
import time
import streamlit as st

def play_text_to_speech(text, target_lang="en"):
    """
    Phát âm thanh sử dụng Microsoft Edge TTS.
    Đã tối ưu hóa: Thay thế Pygame bằng st.audio để phát trực tiếp trên trình duyệt Web,
    khắc phục hoàn toàn lỗi mất Card âm thanh (ALSA error) trên Streamlit Cloud.
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
        # Chạy luồng tải audio từ server Microsoft về máy chủ tạm thời
        asyncio.run(_generate_audio())

        # 3. Thay thế Pygame bằng st.audio để đẩy file âm thanh về trình duyệt người dùng
        if os.path.exists(output_file):
            with open(output_file, "rb") as audio_file:
                audio_bytes = audio_file.read()
            
            # Phát âm thanh tự động (autoplay) trực tiếp trên trình duyệt của người dùng
            st.audio(audio_bytes, format="audio/mp3", autoplay=True)
            
            # Xóa file tạm thời để tránh rác máy chủ
            os.remove(output_file)

    except Exception as e:
        print(f"❌ Lỗi phát TTS: {e}")

# ==========================================
# KHU VỰC TEST NHANH (GIỮ NGUYÊN KHUNG CỦA NÍ)
# ==========================================
if __name__ == "__main__":
    # Khi chạy file này độc lập ở máy local, nó vẫn sẽ in log test bình thường
    play_text_to_speech("Hello, this is a speed test for the English voice.", target_lang="en")
    play_text_to_speech("Xin chào, tôi là giọng nói tiếng Việt được tối ưu hóa siêu tốc.", target_lang="vi")
    print("🎉 Hoàn tất quá trình test TTS song ngữ!")