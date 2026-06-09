import os
import pyaudio
from piper.voice import PiperVoice

# --- Cấu hình đường dẫn ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_FOLDER = os.path.join(BASE_DIR, "models", "tts_piper")

# --- Bộ nhớ đệm (Cache) ---
_cached_voices = {}
_pyaudio_instance = None 

def get_pyaudio():
    """Khởi tạo PyAudio 1 lần duy nhất để tối ưu tốc độ 0.3s khởi động."""
    global _pyaudio_instance
    if _pyaudio_instance is None:
        _pyaudio_instance = pyaudio.PyAudio()
    return _pyaudio_instance

def get_voice(lang="en"):
    """Tải và lưu trữ model Piper theo ngôn ngữ."""
    global _cached_voices
    if lang not in _cached_voices:
        # Tự động trỏ đúng model bản xứ chất lượng cao
        model_name = "vi_VN-vais1000-medium.onnx" if lang == "vi" else "en_US-amy-medium.onnx"
        model_path = os.path.join(MODEL_FOLDER, model_name)
        
        print(f"⏳ Đang tải model TTS Piper ('{lang}')...")
        if not os.path.exists(model_path):
            print(f"❌ KHÔNG TÌM THẤY FILE: {model_path}")
            return None
        
        try:
            # Gộp thẳng config_path vào lúc load cho gọn code
            _cached_voices[lang] = PiperVoice.load(model_path, config_path=f"{model_path}.json")
            print(f"✅ Đã sẵn sàng giọng đọc: '{lang}'!")
        except Exception as e:
            print(f"❌ Lỗi tải PiperVoice ({lang}): {e}")
            return None
            
    return _cached_voices[lang]

def play_text_to_speech(text, target_lang="en"):
    """Phát âm thanh ra loa."""
    if not text or not text.strip():
        return
        
    voice = get_voice(target_lang)
    if not voice:
        return

    print(f"🔊 [{target_lang.upper()}] Đang phát: '{text}'")
    
    p = get_pyaudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=voice.config.sample_rate,
        output=True,
        frames_per_buffer=1024
    )

    try:
        # Dùng lại đúng hàm synthesize() hợp với phiên bản Piper của ní
        for audio_chunk in voice.synthesize(text):
            stream.write(audio_chunk.audio_int16_bytes)
    except Exception as e:
        print(f"❌ Lỗi phát TTS: {e}")
    finally:
        stream.stop_stream()
        stream.close()

# ==========================================
# KHU VỰC TEST NHANH 
# ==========================================
if __name__ == "__main__":
    play_text_to_speech("Hello, this is a speed test for the English voice.", target_lang="en")
    play_text_to_speech("Xin chào, tôi là giọng nói tiếng Việt được tối ưu hóa siêu tốc.", target_lang="vi")
    print("🎉 Hoàn tất quá trình test TTS song ngữ!")