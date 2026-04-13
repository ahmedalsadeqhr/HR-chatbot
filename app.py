import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="مساعد HR - 51Talk Egypt",
    page_icon="💬",
    layout="centered",
)

# ── Handbook text ────────────────────────────────────────────────────────────
HANDBOOK = """
51Talk Egypt — Employee Handbook (Bilingual Edition 2026)
HR Contact: hr.egy@51talk.com

1. WELCOME & INTRODUCTION
This handbook is your comprehensive reference for company policies, benefits, and employment
standards at 51Talk Egypt. It forms an integral part of your employment relationship and supplements
your individual contract. We are committed to providing a safe, respectful, and inclusive workplace.

2. COMPANY IDENTITY & CORE VALUES
Vision:  To be recognized as a highly respectable online education platform for centuries.
Mission: To enable every student to speak up, stand out, and succeed in life.
Values:
  - Customer Focus: Fulfilling duties and responding swiftly to customer needs.
  - Game Changer: Proactively adapting, driving initiatives, and learning through change.
  - Passion: Taking responsibility, striving for higher goals, facing difficulties head-on.
  - Team Work: Fostering mutual trust, open communication, and cross-cultural integration.

3. WORK SCHEDULE & ATTENDANCE
Official Working Week: Six days (Saturday–Thursday)
  - Sunday–Thursday: 12:00 PM – 9:00 PM
  - Saturday: 12:00 PM – 4:00 PM
Break Times (Sun–Thu): 2:45–3:00 PM and 5:00–6:00 PM
Break Time (Sat): 1:45–2:00 PM
Attendance is recorded via fingerprint system. Missing daily records without approved leave = unauthorized absence.

4. LEAVE POLICIES
Leave Type         | Days                        | Pay  | Key Conditions
Annual Leave       | 15 days (<1yr) / 21 (≥1yr) | Full | Must be used within same year
Casual Leave       | 7 days/year (max 2/request) | Full | Counts toward annual leave balance
Sick Leave         | As needed                   | 75%  | Stamped medical certificate required
Maternity Leave    | 120 days                    | Full | After 1 year of service; birth certificate required
Paternity Leave    | 1 day/occurrence (max 3×/yr)| Full | Proof required
Marriage Leave     | 3 days                      | Full | Extra days from annual balance or unpaid
Bereavement Leave  | 3 days                      | Full | Parents, spouse, children only; proof required
Unpaid Leave       | As approved                 | 0%   | Manager + HR approval required

5. ATTENDANCE VIOLATIONS & PENALTIES
Late arrival — 1st time:          100 EGP deduction
Late arrival — 2nd time:          200 EGP deduction
Late arrival — 3rd time:          500 EGP deduction
Late arrival — 4th time+:         500 EGP + Warning letter
Missing punch (3 occurrences):    Half-day salary deduction
Missing punch (6 occurrences):    Warning letter
Early departure (no approval):    Half-day salary deduction
Unapproved absence:               Two-day salary deduction + Warning letter

6. WORKPLACE CONDUCT STANDARDS
All employees are expected to:
  - Communicate respectfully — no insults or demeaning language
  - Protect confidential company and student information
  - Disclose any conflicts of interest
  - Follow health, safety, and security procedures
  - Report misconduct through available channels

Strictly Prohibited:
  - Harassment or discrimination (race, religion, gender, age, disability)
  - Smoking indoors or in vehicles (designated outdoor areas only)
  - Possession or consumption of drugs or alcohol during work hours
  - Fraud, falsification of documents, theft, or embezzlement
  - Physical violence, threats, or intimidation
  - Unauthorized sharing of confidential data or credentials

7. PROFESSIONAL DRESS CODE
Standard: Business casual — clean, neat, and professional.
Acceptable: Collared shirts, blouses, polo shirts; slacks, modest dresses/skirts; closed-toe shoes.
Not Acceptable: Short skirts or shorts; off-shoulder/crop tops; clothing with offensive slogans or ripped items.
Note: Clothing should cover from neck to knees. Cultural and religious dress is respected and accommodated.

8. PROBATION & EMPLOYMENT STRUCTURE
Probationary Period: 3 months with monthly KPI evaluations.
  - A low rating in any month = probation unsuccessful.
  - Termination during probation carries no severance compensation.

Resignation:
  - 30-day notice period required.
  - Submit resignation email to Team Leader, CC hr.egy@51talk.com.
  - Early departure without department head approval results in withheld salary.

Off-Boarding Process:
  1. Submit resignation email.
  2. Obtain Chinese Manager approval (if required).
  3. HR confirms internal clearance and vendor off-boarding.
  4. Complete exit meeting on final day.
  5. Return all company assets to Admin/IT.
  6. Vendor & labor office finalization within 2–5 working days.
  7. Final salary processed in next cycle after clearance.

9. COMPENSATION & BENEFITS
Payment Schedule:
  - Basic salary: paid on the 30th of each month.
  - Commission: paid on the 20th of each month.
  - Attendance variables calculated: 21st of previous month to 20th of current month.

Insurance:
  - Social Insurance: shared contribution between company and employee.
  - Medical Insurance: company-provided; effective same month if hired by the 20th,
    following month if hired after the 20th.

KPI System: Performance targets tied to both salary and commission. Errors corrected in next cycle.

10. COMMUNICATION & ESCALATION
Escalation Matrix:
  1. Direct Manager — day-to-day concerns, performance issues, early-stage conflicts.
  2. Director / 2nd Manager — repeated or severe issues.
  3. HR (hr.egy@51talk.com) — workplace conduct, grievances, harassment, discrimination, policy clarification.

Confidentiality: The company makes reasonable efforts to protect reporter confidentiality.
Non-Retaliation: Retaliation against anyone who reports a concern is strictly prohibited.
"""

SYSTEM_PROMPT = f"""أنت مساعد الموارد البشرية الذكي لشركة 51Talk Egypt، اسمك "مساعد HR".

مهمتك الوحيدة هي مساعدة موظفي الشركة في الإجابة على أسئلتهم المتعلقة بسياسات الشركة وإجراءات الموارد البشرية.

**قواعد مهمة جداً:**
1. أجب دائماً باللغة العربية بأسلوب واضح ومهني وودود.
2. استند في إجاباتك فقط إلى المعلومات الموجودة في دليل الموظف أدناه.
3. إذا كان السؤال يتعلق ببيانات شخصية (رصيد الإجازات، الراتب، الحضور الفردي)، وضح بلطف أنك لا تملك صلاحية الوصول إلى البيانات الشخصية ووجّه الموظف للتواصل مع HR على hr.egy@51talk.com.
4. إذا لم تجد إجابة في الدليل، قل ذلك بصراحة واقترح التواصل مع HR.
5. لا تخترع معلومات غير موجودة في الدليل.
6. قدم إجاباتك بشكل منظم وسهل القراءة (نقاط، جداول، أرقام حسب الحاجة).

**دليل الموظف الرسمي:**
{HANDBOOK}
"""

# ── Styling ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');

/* ── Design tokens ── */
:root {
    --bg-deep:       #070B14;
    --bg-mid:        #0D1525;
    --bg-panel:      #111827;
    --blue:          #0056D6;
    --blue-glow:     rgba(0, 86, 214, 0.35);
    --blue-bright:   #1E7FFF;
    --cyan:          #38BDF8;
    --glass:         rgba(255, 255, 255, 0.04);
    --glass-hover:   rgba(255, 255, 255, 0.08);
    --border:        rgba(255, 255, 255, 0.07);
    --border-blue:   rgba(0, 86, 214, 0.4);
    --text:          #E8EDF5;
    --text-muted:    rgba(232, 237, 245, 0.45);
}

/* ── Global ── */
html, body, [class*="css"], .stApp {
    font-family: 'Tajawal', sans-serif !important;
    direction: rtl;
}

/* ── Dark background + dot lattice ── */
.stApp {
    background-color: var(--bg-deep) !important;
    background-image:
        radial-gradient(ellipse 80% 40% at 50% 0%, rgba(0,86,214,0.18) 0%, transparent 70%),
        radial-gradient(circle, rgba(56,189,248,0.06) 1px, transparent 1px);
    background-size: 100% 100%, 28px 28px;
    background-attachment: fixed;
}

[data-testid="stAppViewContainer"] {
    background: transparent !important;
}

[data-testid="block-container"] {
    padding-top: 1.5rem !important;
    max-width: 820px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-panel) !important;
    border-left: 1px solid var(--border) !important;
    direction: rtl;
}
[data-testid="stSidebar"] > div { padding-top: 1.5rem; }

/* ── Sidebar buttons (suggestion chips) ── */
[data-testid="stSidebar"] .stButton > button {
    background: var(--glass) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 10px !important;
    font-family: 'Tajawal', sans-serif !important;
    font-size: 0.82rem !important;
    text-align: right !important;
    direction: rtl !important;
    transition: all 0.2s ease !important;
    padding: 0.45rem 0.8rem !important;
    position: relative;
    overflow: hidden;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--glass-hover) !important;
    border-color: var(--border-blue) !important;
    color: var(--cyan) !important;
    box-shadow: 0 0 12px var(--blue-glow) !important;
    transform: translateX(-2px) !important;
}

/* Clear button */
[data-testid="stSidebar"] .stButton:last-child > button {
    background: rgba(239,68,68,0.08) !important;
    border-color: rgba(239,68,68,0.25) !important;
    color: rgba(239,68,68,0.7) !important;
    margin-top: 0.5rem;
}
[data-testid="stSidebar"] .stButton:last-child > button:hover {
    background: rgba(239,68,68,0.15) !important;
    color: #ef4444 !important;
    box-shadow: none !important;
    transform: none !important;
}

/* ── Sidebar labels / markdown ── */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--text) !important;
    direction: rtl;
    text-align: right;
}
[data-testid="stSidebar"] hr { border-color: var(--border) !important; }

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    direction: rtl;
    text-align: right;
    background: var(--glass) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 1rem 1.1rem !important;
    margin-bottom: 0.75rem !important;
    backdrop-filter: blur(8px);
    animation: fadeInUp 0.35s ease both;
    color: var(--text) !important;
}

/* Assistant messages — slight blue accent on right border */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    border-right: 2px solid var(--border-blue) !important;
}

/* User messages — blue tint */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: rgba(0, 86, 214, 0.08) !important;
    border-color: var(--border-blue) !important;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span {
    direction: rtl !important;
    text-align: right !important;
    color: var(--text) !important;
    font-family: 'Tajawal', sans-serif !important;
    font-size: 0.97rem !important;
    line-height: 1.75 !important;
}
[data-testid="stChatMessage"] strong { color: var(--cyan) !important; }
[data-testid="stChatMessage"] ul,
[data-testid="stChatMessage"] ol { padding-right: 1.2rem; padding-left: 0; }

/* Avatar icons */
[data-testid="chatAvatarIcon-assistant"],
[data-testid="chatAvatarIcon-user"] {
    background: var(--blue) !important;
    border-radius: 10px !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: var(--bg-panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 3px var(--blue-glow) !important;
}
[data-testid="stChatInput"] textarea {
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Tajawal', sans-serif !important;
    font-size: 0.95rem !important;
    color: var(--text) !important;
    background: transparent !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: var(--text-muted) !important; }

/* ── Spinner ── */
[data-testid="stSpinner"] p { color: var(--text-muted) !important; direction: rtl; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: rgba(0,86,214,0.35); border-radius: 99px; }

/* ── Animations ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes pulse-glow {
    0%, 100% { text-shadow: 0 0 20px rgba(56,189,248,0.4); }
    50%       { text-shadow: 0 0 35px rgba(56,189,248,0.7), 0 0 60px rgba(0,86,214,0.3); }
}

/* ── Custom HTML components ── */
.chat-header {
    text-align: center;
    padding: 2rem 0 1.5rem;
    direction: rtl;
}
.chat-header .logo-ring {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 64px; height: 64px;
    background: linear-gradient(135deg, #0056D6, #38BDF8);
    border-radius: 18px;
    font-size: 2rem;
    margin-bottom: 1rem;
    box-shadow: 0 0 0 8px rgba(0,86,214,0.12), 0 0 40px rgba(0,86,214,0.3);
}
.chat-header h1 {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #38BDF8, #ffffff, #38BDF8);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: pulse-glow 3s ease-in-out infinite, shimmer 4s linear infinite;
    margin: 0 0 0.3rem;
}
@keyframes shimmer {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}
.chat-header p {
    color: var(--text-muted);
    font-size: 0.9rem;
    margin: 0;
    letter-spacing: 0.01em;
}
.chat-header .divider {
    width: 60px; height: 2px;
    background: linear-gradient(90deg, transparent, var(--blue), transparent);
    margin: 1rem auto 0;
    border-radius: 99px;
}

/* HR contact card */
.hr-card {
    background: linear-gradient(135deg, rgba(0,86,214,0.12), rgba(56,189,248,0.06));
    border: 1px solid var(--border-blue);
    border-radius: 12px;
    padding: 0.9rem 1rem;
    direction: rtl;
    text-align: right;
    margin-top: 0.5rem;
}
.hr-card .label { color: var(--text-muted); font-size: 0.75rem; margin-bottom: 0.2rem; }
.hr-card .email { color: var(--cyan); font-size: 0.85rem; font-weight: 700; }

/* Sidebar section title */
.sidebar-title {
    color: var(--text-muted) !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    direction: rtl;
    text-align: right;
}
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="chat-header">
    <div class="logo-ring">💬</div>
    <h1>مساعد HR</h1>
    <p>51Talk Egypt &nbsp;·&nbsp; اسأل عن أي شيء في سياسات الشركة</p>
    <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="sidebar-title">أسئلة سريعة</p>', unsafe_allow_html=True)
    suggestions = [
        "كم يوم إجازة سنوية لديّ؟",
        "ما هو نظام الحضور والانصراف؟",
        "ما هي عقوبة التأخير؟",
        "ما هي إجراءات الاستقالة؟",
        "ما هو موعد صرف الراتب؟",
        "ما هي سياسة الإجازة المرضية؟",
        "ما هو كود اللبس الرسمي؟",
        "كيف أتواصل مع HR؟",
    ]
    for s in suggestions:
        if st.button(s, use_container_width=True, key=s):
            st.session_state["pending_input"] = s

    st.markdown("""
    <div class="hr-card">
        <div class="label">📧 تواصل مع فريق HR</div>
        <div class="email">hr.egy@51talk.com</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ مسح المحادثة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ── Chat state ────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome message on first load
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("""
مرحباً! 👋 أنا مساعد HR الخاص بشركة **51Talk Egypt**.

يمكنني مساعدتك في الإجابة على أسئلتك المتعلقة بـ:
- 📅 سياسات الإجازات (السنوية، المرضية، الأمومة...)
- ⏰ جداول العمل والحضور
- 💰 الرواتب والمزايا
- 📋 قواعد السلوك المهني
- 📝 إجراءات الاستقالة والتعيين
- وأي شيء آخر في دليل الموظف!

كيف يمكنني مساعدتك اليوم؟
        """)

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Groq response ─────────────────────────────────────────────────────────────
def get_groq_response(messages: list[dict]) -> str:
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        return "⚠️ خطأ في الإعداد: مفتاح API غير موجود. يرجى التواصل مع المسؤول."
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        temperature=0.2,
        max_tokens=1500,
    )
    return response.choices[0].message.content


def handle_input(user_input: str) -> None:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير..."):
            reply = get_groq_response(st.session_state.messages)
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})


# Handle sidebar suggestion buttons
if "pending_input" in st.session_state:
    pending = st.session_state.pop("pending_input")
    handle_input(pending)

# Handle chat input box
if prompt := st.chat_input("اكتب سؤالك هنا..."):
    handle_input(prompt)
