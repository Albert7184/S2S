import os
import numpy as np
import sherpa_onnx
import speech_recognition as sr
import streamlit as st

# --- Cấu hình đường dẫn ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_ROOT = os.path.join(BASE_DIR, "models")

# Loại bỏ biến _cached_recognizers = {} cũ để tránh xung đột con trỏ bộ nhớ C++ trên Cloud

@st.cache_resource
def get_offline_recognizer(lang="vi"):
    """
    Khởi tạo và trả về model recognizer tương ứng với ngôn ngữ.
    Sử dụng hoàn toàn cơ chế cache hệ thống của Streamlit để khóa chặt RAM,
    giúp xử lý triệt để lỗi 'invalid unordered_map<K, T> key' trên Streamlit Cloud.
    """
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
        
        # Tạo trực tiếp đối tượng và để Streamlit tự cache dựa trên tham số 'lang'
        recognizer = sherpa_onnx.OfflineRecognizer.from_transducer(
            encoder=paths["encoder"],
            decoder=paths["decoder"],
            joiner=paths["joiner"],
            tokens=paths["tokens"],
            num_threads=4,
        )
        print(f"✅ Đã sẵn sàng model Offline cho: '{lang}'!")
        return recognizer
        
    except Exception as e:
        print(f"❌ Lỗi khởi tạo model ({lang}): {e}")
        return None

def listen_from_mic(listen_lang="vi"):
    """Nghe từ mic và chuyển đổi sang text bằng Zipformer (Giữ nguyên 100% logic của ní)"""
    # Lấy đúng model theo ngôn ngữ được truyền vào từ hàm cache hệ thống
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
            
            # Xử lý âm thanh (Giữ nguyên thuật toán của ní)
            raw = audio.get_raw_data(convert_rate=16000, convert_width=2)
            waveform = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
            
            # Giải mã bằng Zipformer Offline (Giữ nguyên luồng xử lý stream của ní)
            stream = recognizer.create_stream()
            stream.accept_waveform(16000, waveform)
            recognizer.decode_stream(stream)
            
            result = stream.result.text.strip()
            print(f"✅ Nhận diện: {result}")
            return result
            
        except Exception as e:
            print(f"❌ Lỗi STT: {e}")
            return "ERROR"