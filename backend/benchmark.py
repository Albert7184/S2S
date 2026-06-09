import time
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import thêm hàm get_offline_recognizer để tải model trước
from stt_engine import listen_from_mic, get_offline_recognizer
from llm_engine import process_text_with_llm
from tts_engine import play_text_to_speech

def run_metrics():
    print("======================================================")
    print("📊 BỘ ĐO LƯỜNG HIỆU NĂNG S2S ĐA NGÔN NGỮ (BENCHMARK) 📊")
    print("======================================================")
    
    # --- Chọn Model ---
    print("Chọn mô hình API để Benchmark:")
    print("1. NVIDIA Nemotron")
    print("2. DeepSeek V4 Flash")
    model_choice = input("Lựa chọn (1 hoặc 2) [Mặc định: 1]: ").strip()
    model_name = "deepseek/deepseek-v4-flash" if model_choice == "2" else "nvidia/nemotron-3-super-120b-a12b:free"
    model_label = "DeepSeek V4" if model_choice == "2" else "Nemotron"

    # --- Chọn Chiều dịch ---
    print("\nChọn chiều dịch để Benchmark:")
    print("1. 🇻🇳 Tiếng Việt -> 🇺🇸 Tiếng Anh")
    print("2. 🇺🇸 Tiếng Anh  -> 🇻🇳 Tiếng Việt")
    dir_choice = input("Lựa chọn (1 hoặc 2) [Mặc định: 1]: ").strip()
    
    direction = "en2vi" if dir_choice == "2" else "vi2en"
    stt_lang = "vi" if direction == "vi2en" else "en"
    tts_lang = "en" if direction == "vi2en" else "vi"
    
    # --- KHỞI ĐỘNG LẠNH (PRE-LOAD) TRƯỚC KHI ĐO ---
    print("\n⏳ Đang tải sẵn các mô hình AI vào RAM để đo cho chuẩn...")
    get_offline_recognizer(stt_lang)
    print("✅ Đã load xong! Sẵn sàng Benchmark.")
    
    print(f"\n🚀 Bắt đầu Benchmark: [{model_label}] | Chiều: {direction.upper()}")
    print("⚠️ LƯU Ý QUAN TRỌNG: Nhấn [ENTER] xong, chờ thấy chữ '🎤 Mời bạn nói...' mới được nói nhé!")
    input("👉 Nhấn [ENTER] để bắt đầu: ")
    
    # 1. Đo lường STT
    t0 = time.time()
    source_text = listen_from_mic(listen_lang=stt_lang) 
    t1 = time.time()
    stt_total_time = t1 - t0

    if not source_text or source_text == "ERROR":
        print("❌ Lỗi STT hoặc không có âm thanh, dừng đo.")
        return

    print(f"✅ STT xong: '{source_text}'")

    # 2. Đo lường LLM 
    print(f"🧠 [{direction}] Bắt đầu dịch qua {model_label} (OpenRouter)...")
    t2 = time.time()
    target_text = process_text_with_llm(
        source_text, 
        model_name=model_name, 
        direction=direction
    )
    t3 = time.time()
    llm_time = t3 - t2

    print(f"✅ LLM xong: '{target_text}'")

    # 3. Đo lường TTS
    print(f"🔊 [{tts_lang.upper()}] Bắt đầu phát âm (Piper)...")
    t4 = time.time()
    if target_text and "Sorry" not in target_text:
        play_text_to_speech(target_text, target_lang=tts_lang)
    t5 = time.time()
    tts_time = t5 - t4

    # 4. In Báo cáo Metrics chi tiết
    total_latency = t5 - t0
    
    print("\n" + "="*60)
    print(f"⏱️ KẾT QUẢ HIỆU NĂNG [{direction.upper()}] - MODEL: {model_label}")
    print("-" * 60)
    
    # Đã sửa chữ Whisper thành Zipformer cho đúng 
    print(f" 🎙️  STT ({stt_lang}): {stt_total_time:.2f} s (Gồm nói + chờ ngắt + Zipformer)")
    print(f" 🧠  LLM ({model_label}): {llm_time:.2f} s")
    print(f" 🔊  TTS (Piper)   : {tts_time:.2f} s")
    print("-" * 60)
    print(f" 🚀  TỔNG THỜI GIAN XỬ LÝ (Latency): {total_latency:.2f} s")
    
    if total_latency < 4.0:
        print(" 🔥  Đánh giá: Cực nhanh! API phản hồi xuất sắc.")
    elif total_latency < 7.0:
        print(" ✅  Đánh giá: Khá mượt, dùng thực tế ổn định.")
    else:
        print(" 🐌  Đánh giá: Hơi chậm, do mạng hoặc có lúc ngừng lấy hơi hơi lâu.")
    print("="*60)

if __name__ == "__main__":
    run_metrics()