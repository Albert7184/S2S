def get_custom_css():
    """
    Chứa toàn bộ CSS tùy chỉnh cho giao diện Glassmorphism và Nature Background.
    Tách ra file riêng để app.py gọn gàng hơn.
    """
    return """
    <style>
        /* ========================================================= */
        /* HÌNH NỀN THIÊN NHIÊN FULL MÀN HÌNH                        */
        /* ========================================================= */
        .stApp {
            background-image: linear-gradient(rgba(2, 44, 34, 0.7), rgba(2, 44, 34, 0.8)), 
                              url("https://images.unsplash.com/photo-1511497584788-876760111969?q=80&w=2560&auto=format&fit=crop");
            background-size: cover; 
            background-position: center; 
            background-attachment: fixed;
            font-family: 'Inter', system-ui, sans-serif; 
            color: #f8fafc; 
        }
        
        /* ========================================================= */
        /* SIDEBAR ĐỒNG BỘ: Xuyên thấu với thiên nhiên               */
        /* ========================================================= */
        [data-testid="stSidebar"] {
            background-color: transparent !important; 
            backdrop-filter: blur(15px) saturate(120%) !important; 
            -webkit-backdrop-filter: blur(15px) saturate(120%) !important; 
            border-right: none !important; 
            box-shadow: 10px 0 30px rgba(0, 0, 0, 0.3); 
        }
        
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div,
        [data-testid="stSidebar"] label { 
            color: #f8fafc !important; 
            text-shadow: 0 1px 3px rgba(0,0,0,0.5); 
        }
        
        [data-testid="stSidebar"] button { 
            color: #f8fafc !important; 
        }
        
        [data-testid="stSidebar"] .stSelectbox label p {
            color: #ffffff !important; 
            font-weight: 800 !important; 
            background: linear-gradient(135deg, #059669, #10b981);
            padding: 6px 14px; 
            border-radius: 12px; 
            display: inline-block; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
            border: 1px solid rgba(255,255,255,0.3);
        }
        
        [data-testid="stSidebar"] .stSlider label p { 
            font-weight: 800 !important; 
            font-size: 15px !important; 
        }
        
        [data-testid="stSidebar"] [data-testid="stAlert"] {
            background: rgba(255, 255, 255, 0.15) !important; 
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            backdrop-filter: blur(10px); 
            border-radius: 18px; 
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        }
        
        [data-testid="stSidebar"] [data-testid="stAlert"] div[role="alert"] { 
            color: #f8fafc !important; 
        }
        
        /* ========================================================= */
        /* HEADER BANNER & ANIMATED TITLE                            */
        /* ========================================================= */
        .header-banner { 
            width: 100%; 
            height: 220px; 
            border-radius: 40px; 
            overflow: hidden; 
            margin-bottom: -75px; 
            position: relative; 
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.5); 
            border: 2px solid rgba(255, 255, 255, 0.3); 
        }
        
        .header-banner img { 
            width: 100%; 
            height: 100%; 
            object-fit: cover; 
            opacity: 0.95; 
            transition: transform 0.5s; 
        }
        
        .header-banner:hover img { 
            transform: scale(1.05); 
        }
        
        .header-banner::after { 
            content: ''; 
            position: absolute; 
            bottom: 0; 
            left: 0; 
            right: 0; 
            height: 100%; 
            background: linear-gradient(to top, rgba(2, 44, 34, 1) 5%, transparent 100%); 
        }
        
        .sidebar-img { 
            width: 100%; 
            border-radius: 20px; 
            margin-bottom: 25px; 
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); 
            border: 2px solid rgba(255, 255, 255, 0.4); 
        }
        
        .title-container { 
            text-align: center; 
            position: relative; 
            z-index: 10; 
            padding-bottom: 10px; 
        }
        
        .title-main { 
            font-size: 72px; 
            font-weight: 900; 
            background: linear-gradient(90deg, #34d399, #10b981, #6ee7b7, #10b981, #34d399); 
            background-size: 200% auto; 
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent; 
            letter-spacing: -2.5px; 
            text-shadow: 0px 5px 30px rgba(0, 0, 0, 0.6); 
            margin-bottom: 0; 
            animation: shine 5s linear infinite; 
        }
        
        @keyframes shine { 
            to { background-position: 200% center; } 
        }
        
        .title-sub { 
            font-size: 19px; 
            color: #a7f3d0; 
            font-weight: 800; 
            letter-spacing: 6px; 
            text-transform: uppercase; 
            text-shadow: 0 2px 4px rgba(0,0,0,0.5); 
        }

        /* ========================================================= */
        /* GIAO DIỆN NÚT ĐIỀU KHIỂN & ĐẢO NGÔN NGỮ                     */
        /* ========================================================= */
        .lang-switcher-container { 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            gap: 15px; 
            margin: 30px 0; 
            position: relative; 
            z-index: 10; 
        }
        
        .lang-box { 
            background: rgba(255,255,255,0.95); 
            padding: 14px 30px; 
            border-radius: 40px; 
            font-weight: 800; 
            font-size: 19px; 
            color: #022c22; 
            box-shadow: 0 15px 35px rgba(0,0,0,0.3); 
            border: 2px solid rgba(255,255,255,1); 
            display: flex; 
            align-items: center; 
            gap: 12px; 
            transition: all 0.3s; 
        }
        
        .lang-box:hover { 
            transform: translateY(-3px); 
            box-shadow: 0 20px 40px rgba(0,0,0,0.4); 
        }

        /* NÚT BẤM (START / STOP / SWAP / TRANSCRIBE) */
        [data-testid="baseButton-primary"] { 
            background: linear-gradient(135deg, #10b981, #059669) !important; 
            border: 1px solid rgba(255,255,255,0.4) !important; 
            color: white !important; 
            font-size: 22px !important; 
            font-weight: 900 !important; 
            border-radius: 50px !important; 
            padding: 25px 40px !important; 
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), inset 0 2px 5px rgba(255,255,255,0.4) !important; 
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important; 
        }
        
        [data-testid="baseButton-primary"]:hover { 
            transform: scale(1.03) translateY(-5px); 
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5), inset 0 2px 5px rgba(255,255,255,0.5) !important; 
        }
        
        [data-testid="baseButton-secondary"] { 
            background: linear-gradient(135deg, #f43f5e, #be123c) !important; 
            border: 1px solid rgba(255,255,255,0.4) !important; 
            color: white !important; 
            font-size: 22px !important; 
            font-weight: 900 !important; 
            border-radius: 50px !important; 
            padding: 25px 40px !important; 
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), inset 0 2px 5px rgba(255,255,255,0.4) !important; 
            animation: pulse-red 1.5s infinite; 
        }
        
        @keyframes pulse-red { 
            0% { box-shadow: 0 0 0 0 rgba(244, 63, 94, 0.7), inset 0 2px 5px rgba(255,255,255,0.4); } 
            70% { box-shadow: 0 0 0 25px rgba(244, 63, 94, 0), inset 0 2px 5px rgba(255,255,255,0.4); } 
            100% { box-shadow: 0 0 0 0 rgba(244, 63, 94, 0), inset 0 2px 5px rgba(255,255,255,0.4); } 
        }

        /* ========================================================= */
        /* HACK GIAO DIỆN FORM THÀNH BẢNG KÍNH (UNIFIED BOARD)       */
        /* ========================================================= */
        div[data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.88) !important; 
            backdrop-filter: blur(35px) saturate(180%) !important; 
            -webkit-backdrop-filter: blur(35px) !important;
            border-radius: 50px !important; 
            padding: 45px 55px !important; 
            margin: 15px auto 45px auto !important;
            box-shadow: 0 40px 80px rgba(0, 0, 0, 0.4), 0 15px 35px rgba(0, 0, 0, 0.3), inset 0 2px 10px rgba(255, 255, 255, 1) !important;
            border: 2px solid rgba(255, 255, 255, 0.8) !important; 
            max-width: 1050px !important;
            transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s !important;
        }
        
        div[data-testid="stForm"]:hover {
            transform: translateY(-8px) !important;
            box-shadow: 0 50px 100px rgba(0, 0, 0, 0.5), 0 20px 45px rgba(0, 0, 0, 0.4), inset 0 2px 10px rgba(255, 255, 255, 1) !important;
        }

        /* ========================================================= */
        /* KHẮC PHỤC LỖI TEXT AREA ĐEN - ÉP NÓ TRONG SUỐT HOÀN TOÀN  */
        /* ========================================================= */
        div[data-baseweb="textarea"], 
        div[data-baseweb="base-input"],
        div[data-testid="stTextArea"] > div > div {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }

        .stTextArea textarea {
            background-color: rgba(255, 255, 255, 0.2) !important; 
            color: #022c22 !important; 
            -webkit-text-fill-color: #022c22 !important;
            font-size: 23px !important; 
            font-weight: 600 !important; 
            border: 1px solid rgba(0,0,0,0.1) !important; 
            border-radius: 10px !important; 
            box-shadow: none !important;
            padding: 10px !important; 
            line-height: 1.6 !important; 
            resize: none !important;
            text-shadow: 0 1px 3px rgba(255, 255, 255, 0.5) !important; 
        }

        .stTextArea textarea:focus { 
            border: 1px solid rgba(16, 185, 129, 0.5) !important; 
            box-shadow: none !important; 
            background-color: rgba(255, 255, 255, 0.3) !important; 
        }

        .stTextArea textarea::placeholder { 
            color: rgba(2, 44, 34, 0.4) !important; 
            -webkit-text-fill-color: rgba(2, 44, 34, 0.4) !important; 
            font-weight: 500 !important; 
        }
        
        /* NÚT DỊCH NHỎ GỌN TRONG BẢNG (Giống Google Translate) */
        [data-testid="stFormSubmitButton"] { 
            display: flex; 
            justify-content: flex-end; 
            margin-top: -40px; 
            margin-bottom: 0px; 
            position: relative; 
            z-index: 20;
        }
        
        [data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, #10b981, #059669) !important; 
            color: white !important; 
            font-weight: 800 !important;
            font-size: 15px !important; 
            border-radius: 20px !important; 
            padding: 5px 25px !important; 
            border: 1px solid rgba(255,255,255,0.4) !important;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4) !important;
        }
        
        [data-testid="stFormSubmitButton"] button:hover { 
            transform: scale(1.05); 
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.6) !important; 
        }

        /* LABELS & TEXT */
        .source-label { 
            font-size: 15px; 
            font-weight: 800; 
            color: #059669; 
            text-transform: uppercase; 
            letter-spacing: 2px; 
            margin-bottom: 12px; 
            display: flex; 
            align-items: center; 
            gap: 10px;
        }
        
        .target-label { 
            font-size: 15px; 
            font-weight: 800; 
            color: #0284c7; 
            text-transform: uppercase; 
            letter-spacing: 2px; 
            margin-bottom: 20px; 
            display: flex; 
            align-items: center; 
            gap: 10px;
        }
        
        .target-text {
            font-size: 23px !important; 
            font-weight: 600 !important; 
            color: #022c22 !important; 
            -webkit-text-fill-color: #022c22 !important;
            line-height: 1.6; 
            font-style: normal !important; 
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important; 
            min-height: 100px;
        }

        /* ĐƯỜNG KẺ SÁNG & SÓNG ÂM */
        .glowing-divider { 
            height: 4px; 
            border-radius: 5px; 
            background: linear-gradient(90deg, transparent, #10b981, #0ea5e9, #10b981, transparent); 
            background-size: 200% 100%; 
            animation: glow-move 3s linear infinite; 
            margin: 30px 0; 
            opacity: 0.6; 
        }
        
        @keyframes glow-move { 
            0% {background-position: 100% 0;} 
            100% {background-position: -100% 0;} 
        }
        
        .wave-container { 
            display: inline-flex; 
            align-items: center; 
            gap: 8px; 
            margin-left: 15px; 
            vertical-align: middle; 
        }
        
        .bar { 
            width: 12px; 
            background: linear-gradient(to top, #10b981, #14b8a6); 
            border-radius: 12px; 
            animation: wave-bounce 1s ease-in-out infinite; 
        }
        
        .bar:nth-child(1) { height: 20px; animation-delay: 0.0s; } 
        .bar:nth-child(2) { height: 40px; animation-delay: 0.1s; } 
        .bar:nth-child(3) { height: 60px; animation-delay: 0.2s; } 
        .bar:nth-child(4) { height: 75px; animation-delay: 0.3s; } 
        .bar:nth-child(5) { height: 60px; animation-delay: 0.4s; } 
        .bar:nth-child(6) { height: 40px; animation-delay: 0.5s; } 
        .bar:nth-child(7) { height: 20px; animation-delay: 0.6s; }
        
        @keyframes wave-bounce { 
            0%, 100% { transform: scaleY(0.3); opacity: 0.5; } 
            50% { transform: scaleY(1); opacity: 1; box-shadow: 0 0 20px rgba(20, 184, 166, 0.9); } 
        }

        /* HISTORY & UPLOAD */
        .history-box { 
            background: rgba(255, 255, 255, 0.92); 
            border-left: 8px solid #10b981; 
            padding: 22px 35px; 
            border-radius: 22px; 
            margin-bottom: 25px; 
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3); 
            border: 1px solid rgba(255,255,255,0.8); 
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s; 
        }
        
        .history-box:hover { 
            transform: scale(1.02) translateY(-2px); 
            box-shadow: 0 18px 40px rgba(0, 0, 0, 0.4); 
        }
        
        .history-src { 
            color: #047857; 
            font-size: 17px; 
            margin-bottom: 12px; 
            font-weight: 600; 
        }
        
        .history-tgt { 
            color: #022c22; 
            font-size: 21px; 
            font-weight: 800; 
        }
        
        h3 { 
            color: #f8fafc !important; 
            text-shadow: 0 2px 5px rgba(0,0,0,0.5); 
        }
        
        [data-testid="stFileUploadDropzone"] { 
            background-color: rgba(255,255,255,0.15) !important; 
            border: 2px dashed rgba(255,255,255,0.5) !important; 
            border-radius: 20px; 
        }
    </style>
    """