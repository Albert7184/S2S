import time
import os
import sys

# Đảm bảo Python tìm thấy các file trong backend
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from stt_engine import listen_from_mic
from llm_engine import process_text_with_llm
from tts_engine import play_text_to_speech

def main_pipeline():
    print("======================================================")
    print("🚀 HỆ THỐNG SPEECH-TO-SPEECH (S2S) ĐA NGÔN NGỮ 🚀")
    print("      (Đồng bộ: STT-Whisper | LLM-OpenRouter | TTS-Piper)")
    print("======================================================")
    
    # --- Chọn Model ngay từ đầu ---
    print("Chọn mô hình API sử dụng:")
    print("1. NVIDIA Nemotron")
    print("2. DeepSeek V4 Flash")
    model_choice = input("Lựa chọn (1 hoặc 2) [Mặc định: 1]: ").strip()
    model_name = "deepseek/deepseek-v4-flash" if model_choice == "2" else "nvidia/nemotron-3-super-120b-a12b:free"
    model_label = "DeepSeek V4" if model_choice == "2" else "Nemotron"
    
    print(f"\n=> Đã kích hoạt Model: {model_label} ✅")
    
    # Mặc định chiều dịch ban đầu
    direction = "vi2en" 
    
    while True:
        try:
            # Xác định icon và ngôn ngữ
            src_icon = "🇻🇳" if direction == "vi2en" else "🇺🇸"
            tgt_icon = "🇺🇸" if direction == "vi2en" else "🇻🇳"
            stt_lang = "vi" if direction == "vi2en" else "en"
            tts_lang = "en" if direction == "vi2en" else "vi"

            print(f"\n[ CHẾ ĐỘ HIỆN TẠI: {src_icon} ➡️ {tgt_icon} | 🧠 {model_label} ]")
            print("-" * 60)
            print("👉 [ENTER]: Bắt đầu nói")
            print("👉 [S]    : Đảo chiều dịch (Swap)")
            print("👉 [Q]    : Thoát hệ thống")
            
            cmd = input("Lựa chọn của ní: ").lower().strip()
            
            if cmd in ['q', 'exit', 'quit']:
                print("🛑 Tạm biệt ní, hẹn gặp lại!")
                break
            
            if cmd == 's':
                direction = "en2vi" if direction == "vi2en" else "vi2en"
                print(f"🔄 Đã đảo chiều sang: {'Anh -> Việt' if direction == 'en2vi' else 'Việt -> Anh'}")
                continue

            # 1. Bật Mic nghe
            print(f"🎙️ {src_icon} Đang nghe... (Nói xong im lặng để máy xử lý)")
            source_text = listen_from_mic(listen_lang=stt_lang)
            
            if not source_text or source_text == "ERROR":
                print("⚠️ Không nghe rõ, ní nói lại tí đi.")
                continue
                
            print(f"✅ [{stt_lang.upper()}] Nhận diện: '{source_text}'")
            
            # 2. Gửi cho LLM dịch
            print(f"🧠 [LLM] Đang dịch sang {tgt_icon}...")
            target_text = process_text_with_llm(
                source_text, 
                model_name=model_name, 
                direction=direction
            )
            print(f"✅ [{tts_lang.upper()}] Bản dịch: {target_text}")

            # 3. Phát âm thanh (TTS)
            if target_text and "Sorry" not in target_text:
                print(f"🔊 {tgt_icon} Đang phát giọng đọc...")
                play_text_to_speech(target_text, target_lang=tts_lang)
            else:
                print("⚠️ [TTS] Có lỗi gì đó, không thể phát âm.")

        except KeyboardInterrupt:
            print("\n🛑 Đã thoát đột ngột.")
            break
        except Exception as e:
            print(f"❌ Lỗi phát sinh: {e}")

if __name__ == "__main__":
    main_pipeline()