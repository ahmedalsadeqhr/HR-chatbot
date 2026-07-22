import streamlit as st

_BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;500;600;700;800&family=Tajawal:wght@400;500;700;800&display=swap');

:root {
    --navy:          #08122A;
    --navy-mid:      #0F1C3A;
    --navy-panel:    #111f3f;
    --navy-card:     #152040;
    --amber:         #FFC800;
    --amber-light:   #FFD94A;
    --amber-dark:    #D4A800;
    --amber-glow:    rgba(255, 200, 0, 0.22);
    --amber-soft:    rgba(255, 200, 0, 0.08);
    --amber-border:  rgba(255, 200, 0, 0.28);
    --cream:         #F5EDD6;
    --cream-muted:   rgba(245, 237, 214, 0.42);
    --glass:         rgba(255, 255, 255, 0.03);
    --glass-warm:    rgba(255, 200, 0, 0.04);
    --border:        rgba(255, 255, 255, 0.06);
    --shadow-card:   0 8px 32px rgba(0,0,0,0.45), 0 1px 0 rgba(255,200,0,0.08);
    --shadow-hover:  0 12px 40px rgba(0,0,0,0.55), 0 0 0 1px rgba(255,200,0,0.18);
    --yellow:        #FFC800;
    --yellow-dark:   #D4A800;
    --yellow-glow:   rgba(255, 200, 0, 0.22);
    --yellow-soft:   rgba(255, 200, 0, 0.08);
    --border-yellow: rgba(255, 200, 0, 0.28);
    --text:          #F5EDD6;
    --text-muted:    rgba(245, 237, 214, 0.42);
}

html, body, [class*="css"], .stApp {
    font-family: 'Nunito', 'Tajawal', sans-serif !important;
    direction: rtl;
    color: var(--cream) !important;
}
[data-testid="stIconMaterial"] {
    font-family: 'Material Symbols Rounded' !important;
    direction: ltr !important;
    unicode-bidi: isolate !important;
    letter-spacing: normal !important;
}

.stApp {
    background-color: var(--navy) !important;
    background-image:
        radial-gradient(ellipse 70% 55% at 50% -8%, rgba(255,200,0,0.16) 0%, transparent 62%),
        radial-gradient(ellipse 35% 40% at 85% 95%,  rgba(255,140,0,0.07) 0%, transparent 50%),
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E");
    background-size: 100% 100%, 100% 100%, 300px 300px;
    background-attachment: fixed;
}

[data-testid="stAppViewContainer"] { background: transparent !important; }
[data-testid="stMainBlockContainer"] { padding-top: 1rem !important; max-width: 800px; }
[data-testid="stBottomBlockContainer"] { background: transparent !important; }

.star-field { position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden; }
.stars-sm, .stars-md, .stars-lg {
    position: absolute; inset: 0;
    background: transparent;
    animation: twinkle-sm 6s ease-in-out infinite alternate;
}
.stars-sm {
    box-shadow:
        12px  80px 1px rgba(255,255,220,0.55), 88px  30px 1px rgba(255,255,220,0.40),
        155px 140px 1px rgba(255,255,220,0.50),220px  55px 1px rgba(255,255,220,0.45),
        310px 200px 1px rgba(255,255,220,0.35),400px  90px 1px rgba(255,255,220,0.55),
        480px 170px 1px rgba(255,255,220,0.40),560px  40px 1px rgba(255,255,220,0.50),
        640px 220px 1px rgba(255,255,220,0.45),720px 110px 1px rgba(255,255,220,0.35),
        780px 290px 1px rgba(255,255,220,0.55),830px  65px 1px rgba(255,255,220,0.40),
         45px 320px 1px rgba(255,255,220,0.35),130px 380px 1px rgba(255,255,220,0.50),
        200px 440px 1px rgba(255,255,220,0.40),290px 510px 1px rgba(255,255,220,0.45),
        370px 460px 1px rgba(255,255,220,0.35),460px 390px 1px rgba(255,255,220,0.55),
        540px 480px 1px rgba(255,255,220,0.40),620px 350px 1px rgba(255,255,220,0.50);
    animation-duration: 7s;
}
.stars-md {
    box-shadow:
         70px 130px 2px rgba(255,245,180,0.60), 190px  70px 2px rgba(255,245,180,0.50),
        265px 255px 2px rgba(255,245,180,0.55), 355px 145px 2px rgba(255,245,180,0.45),
        445px 310px 2px rgba(255,245,180,0.60), 515px 200px 2px rgba(255,245,180,0.50),
        600px 280px 2px rgba(255,245,180,0.55), 680px 150px 2px rgba(255,245,180,0.45),
        750px  80px 2px rgba(255,245,180,0.60), 110px 420px 2px rgba(255,245,180,0.50),
        250px 490px 2px rgba(255,245,180,0.55), 420px 550px 2px rgba(255,245,180,0.45),
        580px 530px 2px rgba(255,245,180,0.60), 700px 490px 2px rgba(255,245,180,0.50);
    animation-duration: 9s;
    animation-delay: 1.5s;
}
.stars-lg {
    box-shadow:
        160px  50px 3px rgba(255,230,100,0.55), 330px 180px 3px rgba(255,230,100,0.45),
        500px  95px 3px rgba(255,230,100,0.55), 675px 240px 3px rgba(255,230,100,0.45),
        820px 130px 3px rgba(255,230,100,0.55), 100px 360px 3px rgba(255,230,100,0.45),
        340px 450px 3px rgba(255,230,100,0.55), 610px 410px 3px rgba(255,230,100,0.45);
    animation-duration: 11s;
    animation-delay: 3s;
}
@keyframes twinkle-sm {
    0%   { opacity: 0.6; }
    33%  { opacity: 1.0; }
    66%  { opacity: 0.5; }
    100% { opacity: 0.9; }
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(13,25,50,0.80) 0%, rgba(10,20,40,0.86) 100%) !important;
    backdrop-filter: blur(28px) saturate(160%);
    -webkit-backdrop-filter: blur(28px) saturate(160%);
    border-left: 1px solid rgba(255,200,0,0.22) !important;
    box-shadow: inset -1px 0 0 rgba(255,200,0,0.06);
}
[data-testid="stSidebar"] > div { padding-top: 1.2rem; }

[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    color: var(--cream) !important;
    border-radius: 10px !important;
    font-family: 'Nunito', 'Tajawal', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    text-align: right !important;
    direction: rtl !important;
    transition: background-color 0.2s cubic-bezier(0.22,1,0.36,1),
                border-color 0.2s cubic-bezier(0.22,1,0.36,1),
                color 0.2s cubic-bezier(0.22,1,0.36,1),
                transform 0.15s cubic-bezier(0.22,1,0.36,1),
                box-shadow 0.2s cubic-bezier(0.22,1,0.36,1) !important;
    padding: 0.42rem 0.75rem !important;
    width: 100% !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,200,0,0.08) !important;
    border-color: rgba(255,200,0,0.30) !important;
    color: var(--amber-light) !important;
    transform: translateX(-3px) !important;
    box-shadow: 4px 0 12px rgba(255,200,0,0.10) inset !important;
}
[data-testid="stSidebar"] .stButton > button:active {
    transform: translateX(-1px) scale(0.97) !important;
    transition-duration: 0.08s !important;
}
[data-testid="stSidebar"] .stButton > button:focus-visible {
    outline: 2px solid var(--amber) !important;
    outline-offset: 2px !important;
}
[data-testid="stSidebar"] .stButton:last-child > button {
    background: rgba(220,53,53,0.07) !important;
    border-color: rgba(220,53,53,0.22) !important;
    color: rgba(255,120,120,0.75) !important;
}
[data-testid="stSidebar"] .stButton:last-child > button:hover {
    background: rgba(220,53,53,0.14) !important;
    color: #ff8080 !important;
    transform: none !important;
    box-shadow: none !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: var(--cream) !important; direction: rtl; text-align: right; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.06) !important; }

[data-testid="stChatMessage"] {
    direction: rtl;
    text-align: right;
    background: rgba(255,255,255,0.028) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 18px !important;
    padding: 1.1rem 1.25rem !important;
    margin-bottom: 0.9rem !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.35) !important;
    animation: msgIn 0.32s cubic-bezier(0.34,1.56,0.64,1) both;
    position: relative;
    overflow: hidden;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background: linear-gradient(135deg,
        rgba(255,248,220,0.055) 0%,
        rgba(255,200,0,0.028) 100%) !important;
    border-color: rgba(255,200,0,0.18) !important;
    border-right: 3px solid var(--amber) !important;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"])::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,200,0,0.35), transparent);
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: rgba(255,200,0,0.055) !important;
    border-color: rgba(255,200,0,0.22) !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.30), 0 0 0 1px rgba(255,200,0,0.08) !important;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span:not([data-testid="stIconMaterial"]) {
    direction: rtl !important;
    text-align: right !important;
    color: var(--cream) !important;
    font-family: 'Nunito', 'Tajawal', sans-serif !important;
    font-size: 0.96rem !important;
    line-height: 1.8 !important;
}
[data-testid="stChatMessage"] [data-testid="stIconMaterial"] {
    font-family: 'Material Symbols Rounded' !important;
    direction: ltr !important;
    unicode-bidi: isolate !important;
    letter-spacing: normal !important;
}
[data-testid="stChatMessage"] strong { color: var(--amber-light) !important; }
[data-testid="stChatMessage"] ul,
[data-testid="stChatMessage"] ol { padding-right: 1.2rem; padding-left: 0; }
[data-testid="stChatMessage"] code {
    background: rgba(255,200,0,0.12) !important;
    color: var(--amber-light) !important;
    border-radius: 5px !important;
    padding: 0.1em 0.35em !important;
    font-size: 0.88em !important;
}

[data-testid="stChatMessageAvatarAssistant"],
[data-testid="stChatMessageAvatarUser"] {
    background: var(--navy-mid) !important;
    border: 2px solid var(--amber) !important;
    border-radius: 12px !important;
    box-shadow: 0 0 12px rgba(255,200,0,0.25) !important;
}
[data-testid="stChatMessageAvatarAssistant"] [data-testid="stIconMaterial"],
[data-testid="stChatMessageAvatarUser"] [data-testid="stIconMaterial"] {
    color: var(--amber-light) !important;
    font-size: 1.1rem !important;
}

[data-testid="stChatInput"] {
    background: rgba(15,28,58,0.85) !important;
    border: 1.5px solid rgba(255,200,0,0.25) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(12px);
    transition: border-color 0.22s cubic-bezier(0.22,1,0.36,1),
                box-shadow 0.22s cubic-bezier(0.22,1,0.36,1) !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--amber) !important;
    box-shadow: 0 0 0 3px rgba(255,200,0,0.14), 0 4px 24px rgba(255,200,0,0.10) !important;
}
[data-testid="stChatInput"] textarea {
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Nunito', 'Tajawal', sans-serif !important;
    font-size: 0.95rem !important;
    color: var(--cream) !important;
    background: transparent !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: var(--cream-muted) !important; }
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, var(--amber), var(--amber-dark)) !important;
    color: var(--navy) !important;
    border-radius: 10px !important;
    font-weight: 800 !important;
    transition: transform 0.15s cubic-bezier(0.22,1,0.36,1),
                box-shadow 0.15s cubic-bezier(0.22,1,0.36,1) !important;
}
[data-testid="stChatInput"] button:hover {
    transform: scale(1.06) !important;
    box-shadow: 0 4px 14px rgba(255,200,0,0.35) !important;
}
[data-testid="stChatInput"] button:active {
    transform: scale(0.96) !important;
    transition-duration: 0.08s !important;
}
[data-testid="stChatInput"] button:focus-visible,
[data-testid="stChatInput"] textarea:focus-visible {
    outline: 2px solid var(--amber-light) !important;
    outline-offset: 2px !important;
}

[data-testid="stSpinner"] p { color: var(--cream-muted) !important; direction: rtl; font-family: 'Nunito','Tajawal',sans-serif !important; }

[data-testid="stAlertContainer"] {
    background: rgba(220,53,53,0.10) !important;
    border: 1px solid rgba(220,120,120,0.35) !important;
    border-radius: 14px !important;
    direction: rtl !important;
    text-align: right !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.30) !important;
}
[data-testid="stAlertContainer"] p {
    color: rgba(255,190,190,0.92) !important;
    font-family: 'Nunito', 'Tajawal', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
}
[data-testid="stAlertContainer"] [data-testid="stIconMaterial"] { color: rgb(255,140,140) !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,200,0,0.28); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,200,0,0.50); }

@keyframes msgIn {
    from { opacity: 0; transform: translateY(10px) scale(0.97); }
    to   { opacity: 1; transform: translateY(0)    scale(1);    }
}
@keyframes toki-float {
    0%, 100% { transform: translateY(0)   rotate(-1deg); }
    50%       { transform: translateY(-8px) rotate(1deg); }
}
@keyframes shimmer-gold {
    0%   { background-position: 0%   center; }
    100% { background-position: 200% center; }
}
@keyframes halo-pulse {
    0%, 100% { box-shadow: 0 0 0 0   rgba(255,200,0,0.0), 0 0 40px 10px rgba(255,200,0,0.18); }
    50%       { box-shadow: 0 0 0 12px rgba(255,200,0,0.0), 0 0 60px 20px rgba(255,200,0,0.28); }
}
@keyframes badge-pop {
    0%   { transform: scale(0.7); opacity: 0; }
    70%  { transform: scale(1.05); }
    100% { transform: scale(1);   opacity: 1; }
}

.chat-header {
    text-align: center;
    padding: 2.2rem 1.5rem 1.8rem;
    direction: rtl;
    background: linear-gradient(160deg,
        rgba(255,200,0,0.07) 0%,
        rgba(255,200,0,0.02) 50%,
        rgba(15,28,58,0.20) 100%);
    border: 1px solid rgba(255,200,0,0.16);
    border-radius: 24px;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,200,0,0.14);
}
.chat-header::before {
    content: '';
    position: absolute;
    top: -60%; left: -30%;
    width: 160%; height: 140%;
    background: radial-gradient(ellipse at 50% 0%, rgba(255,200,0,0.10) 0%, transparent 65%);
    pointer-events: none;
}
.chat-header .toki-wrap {
    display: inline-block;
    margin-bottom: 0.5rem;
    animation: toki-float 3.5s ease-in-out infinite;
    filter: drop-shadow(0 6px 20px rgba(255,200,0,0.55));
    position: relative;
    z-index: 1;
}
.chat-header .toki-wrap::after {
    content: '';
    position: absolute;
    bottom: -4px; left: 50%; transform: translateX(-50%);
    width: 70px; height: 20px;
    background: radial-gradient(ellipse, rgba(255,200,0,0.30) 0%, transparent 70%);
    border-radius: 50%;
    animation: halo-pulse 3.5s ease-in-out infinite;
}
.chat-header .toki-wrap img { width: 96px; height: 96px; object-fit: contain; }
.chat-header .brand-badge {
    display: inline-block;
    background: linear-gradient(135deg, var(--amber) 0%, #FFE55C 100%);
    color: var(--navy);
    font-family: 'Fredoka One', 'Nunito', sans-serif !important;
    font-size: 0.68rem;
    font-weight: 400;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 0.22rem 0.8rem;
    border-radius: 20px;
    margin-bottom: 0.55rem;
    box-shadow: 0 2px 10px rgba(255,200,0,0.40);
    animation: badge-pop 0.5s cubic-bezier(0.34,1.56,0.64,1) 0.3s both;
}
.chat-header h1 {
    font-family: 'Fredoka One', 'Nunito', sans-serif !important;
    font-size: 2.2rem;
    font-weight: 400;
    background: linear-gradient(90deg, #FFD94A, #FFF8C0, #FFD94A);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer-gold 4.5s linear infinite;
    margin: 0 0 0.3rem;
    letter-spacing: -0.015em;
}
.chat-header p {
    color: var(--cream-muted);
    font-family: 'Nunito', 'Tajawal', sans-serif !important;
    font-size: 0.88rem;
    margin: 0;
    letter-spacing: 0.01em;
}
.chat-header .divider {
    width: 56px; height: 2px;
    background: linear-gradient(90deg, transparent, var(--amber), transparent);
    margin: 1rem auto 0;
    border-radius: 99px;
    opacity: 0.7;
}

.sidebar-brand {
    display: flex; align-items: center; gap: 0.65rem;
    padding: 0.5rem 0.4rem 0.9rem;
    direction: rtl;
    border-bottom: 1px solid rgba(255,200,0,0.10);
    margin-bottom: 0.4rem;
}
.sidebar-brand img {
    width: 38px; height: 38px; object-fit: contain;
    filter: drop-shadow(0 2px 8px rgba(255,200,0,0.45));
}
.sidebar-brand .sb-text {
    font-family: 'Fredoka One', sans-serif !important;
    color: var(--amber-light);
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.1;
    letter-spacing: 0.01em;
}
.sidebar-brand .sb-sub { color: var(--cream-muted); font-size: 0.70rem; font-weight: 500; }

.sidebar-title {
    color: var(--amber) !important;
    font-family: 'Nunito', 'Tajawal', sans-serif !important;
    font-size: 0.68rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase;
    margin-bottom: 0.45rem;
    direction: rtl; text-align: right;
    position: relative;
    padding-bottom: 0.3rem;
}
.sidebar-title::after {
    content: '';
    position: absolute;
    bottom: 0; right: 0; left: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,200,0,0.25), transparent);
}

.hr-card {
    background: linear-gradient(135deg,
        rgba(255,200,0,0.09) 0%,
        rgba(255,200,0,0.04) 100%);
    border: 1px solid rgba(255,200,0,0.22);
    border-radius: 14px;
    padding: 0.85rem 1rem;
    direction: rtl; text-align: right;
    margin-top: 0.6rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.25);
}
.hr-card .label { color: var(--cream-muted); font-size: 0.73rem; margin-bottom: 0.18rem; font-weight: 500; }
.hr-card .email { color: var(--amber-light); font-size: 0.84rem; font-weight: 700; letter-spacing: 0.01em; }

.upload-zone {
    background: linear-gradient(135deg, rgba(255,200,0,0.055), rgba(255,200,0,0.025));
    border: 1.5px dashed rgba(255,200,0,0.30);
    border-radius: 16px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
    direction: rtl; text-align: right;
    transition: border-color 0.2s, background 0.2s;
    cursor: pointer;
}
.upload-zone:hover {
    border-color: rgba(255,200,0,0.60);
    background: linear-gradient(135deg, rgba(255,200,0,0.09), rgba(255,200,0,0.04));
}
.upload-zone .uz-title { color: var(--amber-light); font-weight: 700; font-size: 0.9rem; margin-bottom: 0.2rem; }
.upload-zone .uz-hint  { color: var(--cream-muted); font-size: 0.78rem; }

.attached-badge {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: rgba(255,200,0,0.10);
    border: 1px solid rgba(255,200,0,0.28);
    border-radius: 20px;
    padding: 0.22rem 0.72rem;
    color: var(--amber-light);
    font-size: 0.80rem; font-weight: 700;
    margin-bottom: 0.5rem; direction: rtl;
}

[data-testid="stFileUploader"] { background: transparent !important; direction: rtl; }
[data-testid="stFileUploader"] section { background: transparent !important; border: none !important; padding: 0 !important; }
[data-testid="stFileUploader"] label { color: var(--cream-muted) !important; font-family: 'Nunito','Tajawal',sans-serif !important; font-size: 0.85rem !important; }
[data-testid="stFileUploaderDropzone"] { background: rgba(255,255,255,0.02) !important; border: 1.5px dashed rgba(255,200,0,0.28) !important; border-radius: 12px !important; }
[data-testid="stFileUploaderDropzone"]:hover { border-color: rgba(255,200,0,0.58) !important; background: rgba(255,200,0,0.04) !important; }
[data-testid="stFileUploaderDropzone"] span { color: var(--cream-muted) !important; font-family: 'Nunito','Tajawal',sans-serif !important; }
[data-testid="stFileUploaderDropzone"] button {
    background: linear-gradient(135deg, var(--amber), var(--amber-dark)) !important;
    color: var(--navy) !important;
    font-weight: 800 !important;
    border-radius: 9px !important;
    font-family: 'Nunito','Tajawal',sans-serif !important;
    box-shadow: 0 3px 10px rgba(255,200,0,0.30) !important;
    transition: transform 0.15s cubic-bezier(0.22,1,0.36,1) !important;
}
[data-testid="stFileUploaderDropzone"] button:active { transform: scale(0.96) !important; }
[data-testid="stFileUploaderDropzone"] button:focus-visible {
    outline: 2px solid var(--amber-light) !important;
    outline-offset: 2px !important;
}

[data-testid="stChatMessage"] img {
    border-radius: 12px;
    max-width: 280px;
    border: 1px solid rgba(255,200,0,0.28);
    margin-bottom: 0.5rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.4);
}

@media (prefers-reduced-motion: reduce) {
    .star-field, .stars-sm, .stars-md, .stars-lg,
    .chat-header .toki-wrap, .chat-header .toki-wrap::after,
    .chat-header h1, .chat-header .brand-badge { animation: none !important; }
    [data-testid="stChatMessage"] { animation: msgFade 0.18s ease both !important; }
    [data-testid="stSidebar"] .stButton > button:hover,
    [data-testid="stChatInput"] button:hover { transform: none !important; }
    * { scroll-behavior: auto !important; }
}
@keyframes msgFade { from { opacity: 0; } to { opacity: 1; } }

@media (prefers-reduced-transparency: reduce) {
    [data-testid="stSidebar"] {
        background: #0A1428 !important;
        backdrop-filter: none !important;
        -webkit-backdrop-filter: none !important;
    }
    [data-testid="stChatInput"] { background: #0F1C3A !important; backdrop-filter: none !important; }
    [data-testid="stChatMessage"] { background: rgba(21,32,64,0.95) !important; }
}

@media (prefers-contrast: more) {
    [data-testid="stChatMessage"] { border-width: 1.5px !important; }
    [data-testid="stSidebar"] .stButton > button { border-color: rgba(255,255,255,0.35) !important; }
    [data-testid="stChatInput"] { border-width: 2px !important; }
}
</style>
"""

_LTR_OVERRIDE_CSS = """
<style>
html, body, [class*="css"], .stApp { direction: ltr !important; }
[data-testid="stSidebar"] { direction: ltr !important; border-left: none !important; border-right: 1px solid var(--border-yellow) !important; }
[data-testid="stChatMessage"] { direction: ltr !important; text-align: left !important; }
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span:not([data-testid="stIconMaterial"]) { direction: ltr !important; text-align: left !important; }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) { border-right: none !important; border-left: 3px solid var(--yellow) !important; }
[data-testid="stChatInput"] textarea { direction: ltr !important; text-align: left !important; }
[data-testid="stSidebar"] p, [data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { direction: ltr !important; text-align: left !important; }
[data-testid="stSidebar"] .stButton > button { direction: ltr !important; text-align: left !important; }
[data-testid="stSidebar"] .stButton > button:hover { transform: translateX(3px) !important; }
[data-testid="stSidebar"] .stButton > button:active { transform: translateX(1px) scale(0.97) !important; }
.chat-header, .sidebar-title, .hr-card, .upload-zone, .attached-badge { direction: ltr !important; text-align: left !important; }
.sidebar-brand { direction: ltr !important; }
</style>
"""


def render_styles(lang: str) -> None:
    st.markdown(_BASE_CSS, unsafe_allow_html=True)
    if lang == "en":
        st.markdown(_LTR_OVERRIDE_CSS, unsafe_allow_html=True)
