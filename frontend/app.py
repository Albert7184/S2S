import streamlit as st
import time
import sys
import os
import urllib.request
import zipfile

# ================= PATH =================
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, '..', 'backend')
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

# ================= TỰ ĐỘNG TẢI MODEL NẾU CHƯA CÓ =================
@st.cache_resource
def download_model_if_missing():
    # Khai báo thư mục đích chứa model (bạn đang dùng model tiếng Việt)
    model_dir = os.path.join(current_dir, "../models/sherpa-onnx-zipformer-vi-int8-2025-04-20")
    
    # Nếu chưa có thư mục này -> Cần tải về
    if not os.path.exists(model_dir):
        # Bật thông báo trên giao diện Streamlit
        with st.spinner("📦 Đang tải Mô hình Nhận diện giọng nói từ Cloud (Chỉ tải 1 lần duy nhất, khoảng 1-2 phút)..."):
            
            # Link Hugging Face bạn đã cung cấp
            url = "https://huggingface.co/datasets/RVAlbert/s2s-models-voxta/resolve/main/model_s2s.zip"
            zip_path = os.path.join(current_dir, "temp_model.zip")
            
            try:
                # 1. Tải file về
                urllib.request.urlretrieve(url, zip_path)
                
                # 2. Giải nén vào thư mục models/
                models_base_dir = os.path.join(current_dir, "../models")
                if not os.path.exists(models_base_dir):
                    os.makedirs(models_base_dir)
                    
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(models_base_dir)
                
                # 3. Dọn dẹp file zip
                if os.path.exists(zip_path):
                    os.remove(zip_path)
                    
            except Exception as e:
                st.error(f"❌ Lỗi khi tự động tải model: {e}")

# Kích hoạt hàm kiểm tra ngay khi khởi động
download_model_if_missing()


# Import logic modules
from stt_engine import listen_from_mic
from llm_engine import process_text_with_llm
from tts_engine import play_text_to_speech
from coach_engine import process_with_coach
from file_transcriber import transcribe_audio_file

# Import CSS custom
from styles import get_custom_css

# ================= CONFIG =================
st.set_page_config(page_title="Voxta AI Translator", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ================= STATE =================
if "is_running" not in st.session_state: st.session_state.is_running = False
if "history" not in st.session_state: st.session_state.history = []
if "direction" not in st.session_state: st.session_state.direction = "vi2en"
if "current_source" not in st.session_state: st.session_state.current_source = ""
if "current_target" not in st.session_state: st.session_state.current_target = ""
if "needs_translation" not in st.session_state: st.session_state.needs_translation = False

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("""<img src="https://images.unsplash.com/photo-1473448912268-2022ce9509d8?q=80&w=600&auto=format&fit=crop" class="sidebar-img">""", unsafe_allow_html=True)
    st.markdown("### 🌿 SYSTEM CONFIGURATION")
    st.markdown("---")
    
    model_mapping = {
        "⚡ DeepSeek V4 Flash (High Speed)": "deepseek/deepseek-v4-flash",
        "🧠 NVIDIA Nemotron (Thinking)": "nvidia/nemotron-3-super-120b-a12b:free",
    }
    m = st.selectbox("LLM AI Model", list(model_mapping.keys()))
    st.session_state.model = model_mapping[m]
    
    st.markdown("---")
    st.slider("Silence Threshold (s)", 0.5, 3.0, 1.2, help="Time threshold for silence detection")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🎓 ADVANCED FEATURES")
    st.markdown("---")
    is_coach_mode = st.toggle("👨‍🏫 Enable Coach Mode", value=False)
    st.info("💡 **Tip:** Bật Coach Mode để biến công cụ dịch thành Gia sư AI chỉnh sửa ngữ pháp và nâng cấp từ vựng chuẩn bản xứ!")

# ================= HEADER & LANG SWITCHER =================
st.markdown("""
<div class='header-banner'><img src="https://images.unsplash.com/photo-1448375240586-882707db888b?q=80&w=2000&auto=format&fit=crop"></div>
<div class='title-container'><div class='title-main'>VOXTA AI</div><div class='title-sub'>Nature Voice Translation</div></div>
""", unsafe_allow_html=True)

flag_vn, flag_us = "https://flagcdn.com/w80/vn.png", "https://flagcdn.com/w80/us.png"
if st.session_state.direction == "vi2en":
    src_lang, tgt_lang, src_flag, tgt_flag, stt_lang, tts_lang = "Vietnamese", "English", flag_vn, flag_us, "vi", "en"
else:
    src_lang, tgt_lang, src_flag, tgt_flag, stt_lang, tts_lang = "English", "Vietnamese", flag_us, flag_vn, "en", "vi"

sw1, sw2, sw3, sw4, sw5 = st.columns([2, 1.5, 1, 1.5, 2])
with sw2: st.markdown(f"<div class='lang-box' style='float:right;'><img src='{src_flag}' width='28' style='border-radius:4px;'> {src_lang}</div>", unsafe_allow_html=True)
with sw3:
    if st.button("🔄 SWAP", use_container_width=True):
        st.session_state.direction = "en2vi" if st.session_state.direction == "vi2en" else "vi2en"
        st.session_state.current_source = ""
        st.session_state.current_target = ""
        st.rerun()
with sw4: st.markdown(f"<div class='lang-box'><img src='{tgt_flag}' width='28' style='border-radius:4px;'> {tgt_lang}</div>", unsafe_allow_html=True)

# ================= GIAO DIỆN BẢNG DỊCH (UNIFIED BOARD) =================
with st.form(key="unified_board_form", clear_on_submit=False):
    # Ô Nguồn (Người dùng gõ tay hoặc Mic tự điền vào)
    st.markdown(f"<div class='source-label'><img src='{src_flag}' width='22' style='border-radius:3px;'> {src_lang.upper()}</div>", unsafe_allow_html=True)
    manual_text = st.text_area("Source", value=st.session_state.current_source, height=120, label_visibility="collapsed", placeholder="Nhập văn bản vào đây để dịch...")
    
    # Nút Dịch nằm gọn bên góc phải
    submit_btn = st.form_submit_button("✨ Dịch Text")
    
    st.markdown("<div class='glowing-divider'></div>", unsafe_allow_html=True)
    
    # Ô Đích
    st.markdown(f"<div class='target-label'><img src='{tgt_flag}' width='22' style='border-radius:3px;'> {tgt_lang.upper()}</div>", unsafe_allow_html=True)
    target_display = st.empty()

# Nút Thu Âm (Đứng tách biệt phía dưới để không vướng luồng form)
btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
with btn_col2:
    if not st.session_state.is_running:
        if st.button("🎙️ TOUCH TO SPEAK", type="primary", use_container_width=True):
            st.session_state.is_running = True
            st.rerun()
    else:
        if st.button("🛑 LISTENING... CLICK TO STOP", type="secondary", use_container_width=True):
            st.session_state.is_running = False
            st.rerun()

# ================= CORE LOGIC =================
# 1. BẮT SỰ KIỆN MIC
if st.session_state.is_running:
    target_display.markdown("<div class='target-text'>Listening... <div class='wave-container'><div class='bar'></div><div class='bar'></div><div class='bar'></div><div class='bar'></div><div class='bar'></div><div class='bar'></div><div class='bar'></div></div></div>", unsafe_allow_html=True)
    
    spoken_text = listen_from_mic(listen_lang=stt_lang)
    st.session_state.is_running = False
    
    if spoken_text and spoken_text != "ERROR":
        st.session_state.current_source = spoken_text
        st.session_state.needs_translation = True
        st.rerun() # Refresh lại để text_area hiện chữ vừa nói ngay lập tức

# 2. BẮT SỰ KIỆN GÕ PHÍM
elif submit_btn and manual_text.strip():
    st.session_state.current_source = manual_text.strip()
    st.session_state.needs_translation = True

# 3. TIẾN HÀNH DỊCH & PHÁT ÂM
if st.session_state.needs_translation:
    st.session_state.needs_translation = False
    text_to_process = st.session_state.current_source
    
    if is_coach_mode:
        target_display.markdown("<div class='target-text'>Analyzing grammar & vocabulary...</div>", unsafe_allow_html=True)
        translated = process_with_coach(text_to_process, model_name=st.session_state.model, direction=st.session_state.direction)
        
        display_text = translated.replace("**", "").replace("\n", "<br>")
        target_display.markdown(f"<div class='target-text' style='font-size: 20px; line-height: 1.5; font-weight: 500;'>{display_text}</div>", unsafe_allow_html=True)
        
        first_line = translated.split('\n')[0].replace("**", "").replace("🎯 Bản dịch chuẩn:", "").replace("🎯 Dịch nghĩa:", "").strip()
        play_text_to_speech(first_line, target_lang=tts_lang)
        
        st.session_state.current_target = translated
        st.session_state.history.append({"src": text_to_process, "tgt": translated, "src_lang": src_lang, "tgt_lang": tgt_lang})
    else:
        target_display.markdown("<div class='target-text'>Translating...</div>", unsafe_allow_html=True)
        translated = process_text_with_llm(text_to_process, model_name=st.session_state.model, direction=st.session_state.direction)
        
        typed = ""
        for ch in translated:
            typed += ch
            target_display.markdown(f"<div class='target-text'>{typed}▌</div>", unsafe_allow_html=True)
            time.sleep(0.005)
            
        target_display.markdown(f"<div class='target-text'>{translated}</div>", unsafe_allow_html=True)
        play_text_to_speech(translated, target_lang=tts_lang)
        
        st.session_state.current_target = translated
        st.session_state.history.append({"src": text_to_process, "tgt": translated, "src_lang": src_lang, "tgt_lang": tgt_lang})

# 4. TRẠNG THÁI NGHỈ (Giữ kết quả hiển thị trên màn hình)
elif not st.session_state.is_running:
    display_tgt = st.session_state.current_target
    if display_tgt:
        if is_coach_mode:
            display_tgt = display_tgt.replace("**", "").replace("\n", "<br>")
            target_display.markdown(f"<div class='target-text' style='font-size: 20px; line-height: 1.5; font-weight: 500;'>{display_tgt}</div>", unsafe_allow_html=True)
        else:
            target_display.markdown(f"<div class='target-text'>{display_tgt}</div>", unsafe_allow_html=True)
    else:
        target_display.markdown("<div class='target-text' style='opacity: 0.3;'>Bản dịch sẽ xuất hiện ở đây...</div>", unsafe_allow_html=True)

# ================= HISTORY BELOW =================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("### 📝 Conversation History")
st.markdown("---")

if not st.session_state.history:
    st.caption("No conversation history yet.")
else:
    for item in reversed(st.session_state.history):
        s_flag = flag_vn if "Vietnamese" in item['src_lang'] else flag_us
        t_flag = flag_us if "English" in item['tgt_lang'] else flag_vn
        
        history_tgt = item['tgt'].replace("**", "").replace("\n", "<br>")
        st.markdown(f"""
        <div class='history-box'>
            <div class='history-src'><img src='{s_flag}' width='22' style='border-radius:3px; vertical-align:middle; margin-right:10px;'> {item['src']}</div>
            <div class='history-tgt' style='font-size: 18px; font-weight: 600;'><img src='{t_flag}' width='26' style='border-radius:3px; vertical-align:middle; margin-right:10px;'> {history_tgt}</div>
        </div>
        """, unsafe_allow_html=True)

# ================= AUDIO FILE PROCESSING =================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("### 📁 Upload & Transcribe Audio")
st.markdown("---")
with st.container():
    st.info("💡 **Tip**: Hỗ trợ định dạng cả **.wav** và **.mp3**. Hệ thống sử dụng Whisper AI để dịch và tự động điền dấu câu chuẩn xác.")
    uploaded_file = st.file_uploader("Browse / Drag and drop an audio file here", type=['wav', 'mp3'])
    if uploaded_file is not None:
        if st.button("🚀 Xử lý âm thanh (Transcribe to Text)", type="primary", use_container_width=True):
            with st.spinner("Đang trích xuất dữ liệu âm thanh offline bằng Whisper..."):
                file_extension = os.path.splitext(uploaded_file.name)[1]
                temp_path = os.path.abspath("temp_uploaded_audio" + file_extension)
                with open(temp_path, "wb") as f: f.write(uploaded_file.getbuffer())
                
                transcribed_text = transcribe_audio_file(temp_path, lang=stt_lang)
                if "Lỗi" in transcribed_text: st.error(transcribed_text)
                else:
                    st.success("✅ Trích xuất văn bản hoàn tất!")
                    st.markdown(f"<div style='background:rgba(255,255,255,0.92); padding:25px; border-radius:22px; color:#022c22; box-shadow:0 12px 30px rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.8); margin-bottom: 20px;'><b style='color:#10b981; font-size: 18px; text-transform: uppercase;'>Extracted Text:</b><br><br><span style='font-size: 24px; line-height: 1.6; font-weight: 500;'>{transcribed_text}</span></div>", unsafe_allow_html=True)
                    st.download_button(label="💾 Tải File Text (.TXT)", data=transcribed_text, file_name="Transcription_S2S.txt", mime="text/plain", use_container_width=True)
                
                if os.path.exists(temp_path):
                    try: os.remove(temp_path)
                    except: pass