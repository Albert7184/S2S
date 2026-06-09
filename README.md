# 🌐 S2S - Hệ Thống Dịch Thuật Giọng Nói

> Dịch tiếng Việt ↔ tiếng Anh với STT offline, dịch bằng LLM qua OpenRouter và TTS offline.

---

## 📋 Mục Lục

- [Giới Thiệu](#giới-thiệu)
- [Tính Năng Nổi Bật](#tính-năng-nổi-bật)
- [Cây Thư Mục](#cây-thư-mục)
- [Kiến Trúc Hệ Thống](#kiến-trúc-hệ-thống)
- [Chi Tiết Các Module](#chi-tiết-các-module)
- [Mô Tả Model](#mô-tả-model)
- [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
- [Cài Đặt](#cài-đặt)
- [Chạy Ứng Dụng](#chạy-ứng-dụng)
- [Hướng Dẫn Sử Dụng](#hướng-dẫn-sử-dụng)
- [Giới Hạn Hiện Tại](#giới-hạn-hiện-tại)
- [Khắc Phục Sự Cố](#khắc-phục-sự-cố)
- [Ghi Chú](#ghi-chú)

---

## 🎯 Giới Thiệu

S2S (Speech-to-Speech) là một hệ thống dịch giọng nói tiếng Việt ↔ tiếng Anh thiết kế để chạy trên máy cá nhân.

Hệ thống kết hợp:

- **STT offline**: nhận diện giọng nói bằng Sherpa-ONNX Zipformer.
- **LLM dịch thuật**: gọi OpenRouter API để dịch văn bản.
- **TTS offline**: phát âm thanh bằng Piper.

> Ứng dụng không hoàn toàn offline vì bước dịch LLM vẫn cần mạng.

> Dự án hoạt động theo từng phiên: ghi âm mic → nhận diện STT → dịch LLM → phát TTS.

---

## ✨ Tính Năng Nổi Bật

- Dịch giọng nói **Việt ↔ Anh** qua mic.
- **STT offline** cho tiếng Việt và tiếng Anh.
- **TTS offline** với giọng Anh và giọng Việt.
- **Web UI Streamlit** giao diện đẹp, dễ dùng.
- **CLI đơn giản** cho thao tác nhanh.
- Chọn **model LLM** giữa `Nemotron` và `DeepSeek V4 Flash`.
- Chế độ **Coach Mode**: Gia sư ngữ pháp, gợi ý từ vựng, sửa câu.
- Tải lên file audio (`.wav`, `.mp3`) để **transcribe** bằng Whisper.
- Lưu lịch sử phiên dịch và hiển thị trực quan.

---

## 📁 Cây Thư Mục

```
S2S/
│
├── README.md
├── requirements.txt
├── .env  (tùy chọn)
├── .venv/  (môi trường ảo)
├── venv/   (môi trường ảo)
│
├── backend/
│   ├── benchmark.py
│   ├── coach_engine.py
│   ├── file_transcriber.py
│   ├── llm_engine.py
│   ├── pipeline.py
│   ├── stt_engine.py
│   └── tts_engine.py
│
├── frontend/
│   ├── app.py
│   ├── styles.py
│   
│
└── models/
    ├── sherpa-onnx-zipformer-en-2023-06-26/
    ├── sherpa-onnx-zipformer-vi-int8-2025-04-20/
    └── tts_piper/
```

---

## 🔧 Kiến Trúc Hệ Thống

```
🎤 STT offline (Sherpa-ONNX)
    ↓
📝 Text đầu vào
    ↓
🧠 Dịch thuật LLM OpenRouter
    ↓
🔊 TTS offline (Piper)
```

---

## 🧩 Chi Tiết Các Module

### backend/stt_engine.py

- Nhận diện giọng nói từ micro bằng Sherpa-ONNX.
- Hỗ trợ hai ngôn ngữ: `vi`, `en`.
- Trả về văn bản thô cho bước dịch tiếp theo.

### backend/llm_engine.py

- Gọi OpenRouter API qua `openai`.
- Prompt được tối ưu để dịch chính xác và hạn chế phản hồi không liên quan.
- Hỗ trợ dịch hai chiều: `vi2en` và `en2vi`.
- Cho phép chọn model giữa `Nemotron` và `DeepSeek V4 Flash`.

### backend/tts_engine.py

- Phát âm thanh bằng Piper.
- Hỗ trợ giọng:
  - tiếng Anh: `en_US-amy-medium`
  - tiếng Việt: `vi_VN-vais1000-medium`
- Dùng `pyaudio` để phát trực tiếp.
- Cache model để cải thiện tốc độ lần đầu.

### backend/coach_engine.py

- Chế độ Gia sư giúp dịch kèm phân tích ngữ pháp và từ vựng.
- Trả về kết quả theo định dạng Markdown dễ đọc.

### backend/file_transcriber.py

- Dùng Whisper để trích xuất văn bản từ file audio.
- Hỗ trợ `.wav`, `.mp3` và nhiều định dạng khác.
- Mặc định sử dụng model Whisper `base`.

### backend/pipeline.py

- Giao diện CLI chính của hệ thống.
- Quản lý chọn model, đổi chiều dịch, ghi âm, dịch và phát TTS.
- Hỗ trợ lệnh: `ENTER`, `S`, `Q`.

### frontend/app.py

- Web UI bằng Streamlit.
- Hiển thị đầu vào/đầu ra, nút thu âm, chuyển đổi ngôn ngữ.
- Bật `Coach Mode` để nhận xét ngữ pháp.
- Upload audio file để transcribe.
- Lưu lịch sử phiên dịch.

---

## 🤖 Mô Tả Model

### STT: Sherpa-ONNX Zipformer

- `models/sherpa-onnx-zipformer-en-2023-06-26/`
- `models/sherpa-onnx-zipformer-vi-int8-2025-04-20/`

Yêu cầu:
- `encoder-*.onnx`
- `decoder-*.onnx`
- `joiner-*.onnx`
- `tokens.txt`
- `bpe.model` (tiếng Việt)

### TTS: Piper

- `models/tts_piper/en_US-amy-medium.onnx`
- `models/tts_piper/en_US-amy-medium.onnx.json`
- `models/tts_piper/vi_VN-vais1000-medium.onnx`
- `models/tts_piper/vi_VN-vais1000-medium.onnx.json`

### Transcribe file audio: Whisper

- Dùng `openai-whisper` để chuyển file âm thanh thành văn bản.
- Phục vụ cho tính năng upload audio trong giao diện web.

---

## 💻 Yêu Cầu Hệ Thống

### Phần mềm

- Python 3.11+.
- Windows / macOS / Linux.
- Internet cho bước gọi OpenRouter API.
- File `.env` chứa `OPENROUTER_API_KEY`.

### Phần cứng

- Microphone và loa/tai nghe hoạt động.
- CPU 4 lõi trở lên.
- RAM tối thiểu 4 GB, khuyến nghị 8 GB.

### Thư viện chính

- `streamlit`
- `sherpa-onnx`
- `numpy`
- `SpeechRecognition`
- `openai`
- `python-dotenv`
- `piper-tts`
- `pyaudio`
- `soundfile`
- `openai-whisper` (nếu dùng tính năng upload audio)

---

## 📦 Cài Đặt

### 1. Tạo môi trường ảo

```powershell
cd d:\S2S
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Cài dependencies

```powershell
pip install -r requirements.txt
```

Nếu dùng upload audio:

```powershell
pip install openai-whisper
```

### 3. Thiết lập API key

Tạo file `.env` ở thư mục gốc:

```env
OPENROUTER_API_KEY=your_api_key_here
```

### 4. Kiểm tra model

Đảm bảo các thư mục và file model sau tồn tại:

- `models/sherpa-onnx-zipformer-en-2023-06-26/`
- `models/sherpa-onnx-zipformer-vi-int8-2025-04-20/`
- `models/tts_piper/en_US-amy-medium.onnx`
- `models/tts_piper/vi_VN-vais1000-medium.onnx`

---

## 🚀 Chạy Ứng Dụng

### Chạy CLI

```powershell
python backend\pipeline.py
```

### Chạy Web UI

```powershell
streamlit run frontend\app.py
```

Mở trình duyệt tới `http://localhost:8501`.

---

## 🧭 Hướng Dẫn Sử Dụng

### Web UI

- Chọn model LLM trong sidebar.
- Chuyển chiều dịch bằng nút `SWAP`.
- Nhập văn bản hoặc nhấn `TOUCH TO SPEAK` để dùng micro.
- Bật `Coach Mode` nếu cần phân tích ngữ pháp và gợi ý từ vựng.
- Upload file audio `.wav` / `.mp3` để trích xuất văn bản.

### CLI Mode

- Nhấn `ENTER` để bắt đầu ghi âm.
- Nhập `S` để đổi chiều dịch.
- Nhập `Q` hoặc `exit` để thoát.
- Quy trình: ghi âm mic → STT → dịch LLM → phát TTS.

---

## ⚠️ Giới Hạn Hiện Tại

- Bước dịch vẫn cần kết nối OpenRouter.
- Không phải dịch real-time.
- Kết quả phụ thuộc chất lượng micro và môi trường ồn.
- Whisper dùng model `base`; nếu cần chính xác hơn, có thể nâng cấp sang `small` hoặc `medium`.
- Một số cụm từ lóng vùng miền có thể dịch chưa chuẩn tuyệt đối.

---

## 🛠️ Khắc Phục Sự Cố

- Nếu TTS không phát:
  - Kiểm tra `pyaudio` đã cài.
  - Kiểm tra loa/tai nghe đang hoạt động.
  - Kiểm tra file model Piper có tồn tại.

- Nếu STT không nghe rõ:
  - Kiểm tra mic và quyền truy cập micro.
  - Giảm tiếng ồn xung quanh.

- Nếu LLM lỗi API:
  - Kiểm tra `OPENROUTER_API_KEY` trong `.env`.
  - Kiểm tra kết nối Internet.

- Nếu upload audio không chạy:
  - Cài `openai-whisper`.
  - Đảm bảo file hợp lệ `.wav` hoặc `.mp3`.

---

## 📌 Ghi Chú

- STT: offline với Sherpa-ONNX.
- Dịch: online qua OpenRouter LLM.
- TTS: offline với Piper.
- Dự án phù hợp để thử nghiệm dịch thoại song ngữ và học ngôn ngữ.

---

## ❤️ Cảm Ơn

Cảm ơn bạn đã sử dụng S2S. Chúc bạn có trải nghiệm dịch thoại song ngữ mượt mà!
