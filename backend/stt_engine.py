import os
import numpy as np
import sherpa_onnx
import speech_recognition as sr

# --- Cấu hình đường dẫn ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_ROOT = os.path.join(BASE_DIR, "models")

# Cache model trong RAM để hỗ trợ đa ngôn ngữ (chuyển đổi nhanh, không đơ máy)
_cached_recognizers = {}

def get_offline_recognizer(lang="vi"):
    """Khởi tạo và trả về model recognizer tương ứng với ngôn ngữ"""
    if lang not in _cached_recognizers:
        print(f"⏳ Đang khởi tạo Offline Recognizer cho tiếng '{lang}'...")
        try:
            if lang == "vi":
                model_dir = os.path.join(MODELS_ROOT, "sherpa-onnx-zipformer-vi-int8-2025-04-20")
                paths = {
                    "encoder": os.path.join(model_dir, "encoder-epoch-12-avg-8.int8.onnx"),
                    "decoder": os.path.join(model_dir, "decoder-epoch-12-avg-8.onnx"),
                    "joiner": os.path.join(model_dir, "joiner-epoch-12-avg-8.int8.onnx"),
                    "tokens": os.path.join(model_dir, "tokens.txt")
                }
            else: 
                model_dir = os.path.join(MODELS_ROOT, "sherpa-onnx-zipformer-en-2023-06-26")
                paths = {
                    "encoder": os.path.join(model_dir, "encoder-epoch-99-avg-1.int8.onnx"),
                    "decoder": os.path.join(model_dir, "decoder-epoch-99-avg-1.onnx"),
                    "joiner": os.path.join(model_dir, "joiner-epoch-99-avg-1.int8.onnx"),
                    "tokens": os.path.join(model_dir, "tokens.txt")
                }
            
            _cached_recognizers[lang] = sherpa_onnx.OfflineRecognizer.from_transducer(
                encoder=paths["encoder"],
                decoder=paths["decoder"],
                joiner=paths["joiner"],
                tokens=paths["tokens"],
                num_threads=4,
            )
            print(f"✅ Đã sẵn sàng model Offline cho: '{lang}'!")
        except Exception as e:
            print(f"❌ Lỗi khởi tạo model ({lang}): {e}")
            return None
            
    return _cached_recognizers[lang]

def listen_from_mic(listen_lang="vi"):
    """Nghe từ mic và chuyển đổi sang text bằng Zipformer"""
    # Lấy đúng model theo ngôn ngữ được truyền vào
    recognizer = get_offline_recognizer(listen_lang)
    if not recognizer: 
        return "ERROR"

    vad = sr.Recognizer()
    vad.dynamic_energy_threshold = True
    vad.pause_threshold = 1.2
    
    with sr.Microphone(sample_rate=16000) as source:
        print(f"🎤 [STT] Đang nghe {listen_lang.upper()}... (Nói xong nghỉ chút là máy dịch liền)")
        print("🎙️ [VAD] Đang đo mức âm thanh nền (đợi 1.5s)...")
        vad.adjust_for_ambient_noise(source, duration=0.2)
        print("🎤 Mời bạn nói...")
        
        try:
            audio = vad.listen(source, timeout=10, phrase_time_limit=25)
            print("⏳ [STT] Đang giải mã...")
            
            # Xử lý âm thanh
            raw = audio.get_raw_data(convert_rate=16000, convert_width=2)
            waveform = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
            
            # Giải mã bằng Zipformer Offline
            stream = recognizer.create_stream()
            stream.accept_waveform(16000, waveform)
            recognizer.decode_stream(stream)
            
            result = stream.result.text.strip()
            print(f"✅ Nhận diện: {result}")
            return result
            
        except Exception as e:
            print(f"❌ Lỗi STT: {e}")
            return "ERROR"