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
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl;
}

/* Header */
.main-header {
    background: linear-gradient(135deg, #0056D6 0%, #003DA6 100%);
    color: white;
    padding: 1.5rem 2rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    text-align: center;
    direction: rtl;
}
.main-header h1 { color: white; font-size: 1.8rem; margin: 0; font-weight: 700; }
.main-header p  { color: rgba(255,255,255,0.85); margin: 0.3rem 0 0; font-size: 0.95rem; }

/* Chat messages RTL */
[data-testid="stChatMessage"] {
    direction: rtl;
    text-align: right;
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    direction: rtl;
    text-align: right;
}

/* Chat input RTL */
[data-testid="stChatInput"] textarea {
    direction: rtl;
    text-align: right;
    font-family: 'Cairo', sans-serif !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    direction: rtl;
    text-align: right;
}

/* Suggested questions */
.suggestion-btn {
    background: #f0f4ff;
    border: 1px solid #0056D6;
    border-radius: 20px;
    padding: 0.4rem 0.9rem;
    color: #0056D6;
    font-size: 0.85rem;
    cursor: pointer;
    margin: 0.2rem;
    direction: rtl;
}

/* HR contact footer */
.hr-contact {
    background: #f8f9fa;
    border-right: 4px solid #0056D6;
    padding: 0.8rem 1rem;
    border-radius: 8px;
    direction: rtl;
    font-size: 0.85rem;
    color: #555;
}
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>💬 مساعد HR</h1>
    <p>51Talk Egypt — اسأل عن أي شيء يتعلق بسياسات الشركة والموارد البشرية</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📋 أسئلة مقترحة")
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

    st.divider()
    st.markdown("""
    <div class="hr-contact">
        <strong>📧 تواصل مع HR</strong><br>
        hr.egy@51talk.com
    </div>
    """, unsafe_allow_html=True)

    st.divider()
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
