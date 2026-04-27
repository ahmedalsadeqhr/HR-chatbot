import base64
import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="مساعد HR - 51Talk Egypt",
    page_icon="🐣",
    layout="centered",
)

# Load Toki mascot as base64 for inline HTML embedding
def _load_toki() -> str:
    path = os.path.join(os.path.dirname(__file__), "toki.png")
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""

TOKI_B64 = _load_toki()

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

11. ITALENT SYSTEM — HOW TO USE
iTalent is the company's HR self-service platform for managing attendance, leave, business trips, and personal HR requests.

ACCESS:
  - Web browser: open iTalent from your browser (ask HR or IT for the link if you don't have it).
  - Mobile app: download the iTalent app on your phone for on-the-go access.
  Both channels give you the same features.

CLOCKING IN & OUT:
  - Clock-in and clock-out are done via the iTalent mobile app only.
  - Open the app at the start of your shift → tap Clock In.
  - At the end of your shift → tap Clock Out.
  - Do this every working day. Missing a punch 3 times results in a half-day salary deduction; 6 times results in a warning letter.

HOW TO REQUEST LEAVE:
  Step 1: Open iTalent (web or mobile app).
  Step 2: Go to Employee Self-Service → My Attendance → Leave Application.
           (Or click "Leave Application" directly from the left sidebar on the home screen.)
  Step 3: Click "Leave Project" and select the leave type:
            - Annual Leave
            - Sick Leave
            - Unpaid Leave
            - Maternity Leave
            - Paternity Leave
            - Bereavement Leave
            - Miscarriage Leave
  Step 4: Choose the start and end dates of your leave.
  Step 5: Write a reason in the Reason field (recommended).
  Step 6: Attach supporting documents if required (e.g., medical certificate for sick leave, birth certificate for paternity/maternity leave).
  Step 7: Click Submit.
  Step 8: Your request is sent automatically to your manager for approval.
  Step 9: Track the status under My Approval → Applied tab.

TRACKING YOUR REQUESTS (MY APPROVAL):
  - Pending:   request submitted and awaiting manager decision.
  - Processed: manager has approved or rejected the request.
  - Applied:   full list of all requests you have submitted.

BUSINESS TRIPS:
  - For local business trips: Employee Self-Service → My Attendance → Business Trip (Local).
  - For international business trips: Employee Self-Service → My Attendance → My Business Trips.
  - Fill in the trip details and submit for approval.

PERSONNEL APPLICATION:
  - For any formal HR request (e.g., contract-related): go to Self-Service Application → Personnel Application.

COMMON FUNCTIONS:
  - The "Common Functions" section in Employee Self-Service gives quick access to frequently used actions.

MY PROFILE:
  - View and verify your personal HR information under Employee Self-Service → My Profile.
"""

# ── Egyptian Salary Calculation Knowledge (2025) ──────────────────────────────
SALARY_KNOWLEDGE = """
12. SALARY CALCULATION & TAX DEDUCTIONS (Egypt 2025)

HOW YOUR NET SALARY IS CALCULATED — STEP BY STEP:

STEP 1 — Social & Health Insurance (Employee Share)
  Rate:           12% total (11% Social Insurance + 1% Health Insurance)
  Applied to:     Your "insurable wage" (basic salary + fixed allowances)
  Monthly cap:    EGP 14,500 maximum insurable wage (2025 figure)
  Monthly floor:  EGP 2,300 minimum insurable wage (2025 figure)
  Max deduction:  EGP 14,500 × 12% = EGP 1,740/month
  This deduction is tax-deductible (reduces your taxable income).

STEP 2 — Martyrs Fund
  Rate: 0.05% of gross monthly salary (very small deduction).

STEP 3 — Annual Taxable Income
  Formula: (Gross Monthly × 12) − (Monthly SI deduction × 12)

STEP 4 — Personal Exemption
  EGP 20,000 per year is deducted from annual taxable income (tax-free).

STEP 5 — Apply Progressive Tax Brackets (Annual)
  Bracket                          Rate    Max Tax in Bracket
  EGP 0       – EGP 40,000         0%      EGP 0
  EGP 40,001  – EGP 55,000        10%      EGP 1,500
  EGP 55,001  – EGP 70,000        15%      EGP 2,250
  EGP 70,001  – EGP 200,000       20%      EGP 26,000
  EGP 200,001 – EGP 400,000       22.5%    EGP 45,000
  EGP 400,001 – EGP 1,200,000     25%      EGP 200,000
  Above EGP 1,200,000             27.5%    unlimited

STEP 6 — Monthly Tax
  Annual Tax ÷ 12 = Monthly Tax deducted from payslip.

STEP 7 — Net Monthly Salary
  Net = Gross − Monthly SI − Monthly Tax − Martyrs Fund

QUICK EXAMPLES:
  Gross EGP 5,000/month  → approx. net EGP 4,367/month
  Gross EGP 10,000/month → approx. net EGP 8,513/month
  Gross EGP 15,000/month → approx. net EGP 12,441/month
  Gross EGP 20,000/month → approx. net EGP 16,300/month
  Gross EGP 30,000/month → approx. net EGP 23,547/month
  Gross EGP 50,000/month → approx. net EGP 37,262/month

KEY NOTES:
  - Tax is calculated on annual income then divided by 12 for monthly payslip.
  - The SI cap means all employees earning above EGP 14,500/month pay the
    same fixed SI deduction of EGP 1,740/month.
  - The personal exemption (EGP 20,000/year ≈ EGP 1,667/month) benefits
    lower-income employees most.
  - Salary increases can move you into a higher tax bracket only on the
    portion above the bracket threshold, not your entire income.
  - Company's share of social insurance (18.75%) is paid separately by the
    employer and does NOT appear as a deduction on your payslip.
  - For personalized tax advice, contact HR at hr.egy@51talk.com.
"""

# ── Salary Calculator ─────────────────────────────────────────────────────────
import re

_TAX_BRACKETS = [
    (40_000,       0.00),
    (55_000,       0.10),
    (70_000,       0.15),
    (200_000,      0.20),
    (400_000,      0.225),
    (1_200_000,    0.25),
    (float("inf"), 0.275),
]
_SI_RATE       = 0.12    # 11% pension + 1% health
_SI_CAP        = 14_500
_SI_FLOOR      = 2_300
_MARTYRS_RATE  = 0.0005
_ANNUAL_EXEMPT = 20_000


def calculate_net_salary(gross: float) -> dict:
    insurable = max(_SI_FLOOR, min(gross, _SI_CAP))
    monthly_si = round(insurable * _SI_RATE, 2)
    monthly_martyrs = round(gross * _MARTYRS_RATE, 2)

    annual_gross = gross * 12
    annual_si = monthly_si * 12
    annual_before_exempt = annual_gross - annual_si
    annual_taxable = max(0.0, annual_before_exempt - _ANNUAL_EXEMPT)

    annual_tax = 0.0
    prev = 0
    breakdown = []
    remaining = annual_taxable
    for limit, rate in _TAX_BRACKETS:
        if remaining <= 0:
            break
        band = (limit - prev) if limit != float("inf") else remaining
        chunk = min(remaining, band)
        tax = round(chunk * rate, 2)
        if chunk > 0:
            label = (f"{prev:,.0f} – {limit:,.0f}" if limit != float("inf")
                     else f"فوق {prev:,.0f}")
            breakdown.append({"شريحة (سنوي)": label,
                               "نسبة": f"{rate*100:.1f}%",
                               "دخل في الشريحة": f"{chunk:,.2f}",
                               "ضريبة": f"{tax:,.2f}"})
        annual_tax += tax
        remaining -= chunk
        prev = limit if limit != float("inf") else prev

    monthly_tax = round(annual_tax / 12, 2)
    net = round(gross - monthly_si - monthly_tax - monthly_martyrs, 2)
    effective = round(annual_tax / annual_gross * 100, 2) if annual_gross else 0

    return {
        "gross": gross,
        "insurable_wage": insurable,
        "monthly_si": monthly_si,
        "monthly_martyrs": monthly_martyrs,
        "annual_gross": annual_gross,
        "annual_si": annual_si,
        "annual_taxable_before_exempt": round(annual_before_exempt, 2),
        "personal_exemption": _ANNUAL_EXEMPT,
        "annual_taxable": round(annual_taxable, 2),
        "annual_tax": round(annual_tax, 2),
        "monthly_tax": monthly_tax,
        "net": net,
        "effective_rate": effective,
        "breakdown": breakdown,
    }


def salary_calc_context(gross: float) -> str:
    r = calculate_net_salary(gross)
    rows = "\n".join(
        f"  {b['شريحة (سنوي)']:35s} | {b['نسبة']:6s} | دخل {b['دخل في الشريحة']:>12s} | ضريبة {b['ضريبة']:>12s}"
        for b in r["breakdown"]
    )
    return f"""
[نتيجة حساب الراتب الصافي — أرقام دقيقة محسوبة آلياً]

الراتب الإجمالي (Gross):           {r['gross']:>12,.2f} ج.م / شهر
الوعاء التأميني:                   {r['insurable_wage']:>12,.2f} ج.م / شهر
خصم تأمينات اجتماعية وصحية (12%): {r['monthly_si']:>12,.2f} ج.م / شهر
خصم صندوق الشهداء (0.05%):         {r['monthly_martyrs']:>12,.2f} ج.م / شهر

الدخل السنوي الإجمالي:             {r['annual_gross']:>12,.2f} ج.م
خصم التأمينات السنوية:             {r['annual_si']:>12,.2f} ج.م
الإعفاء الشخصي السنوي:            {r['personal_exemption']:>12,.2f} ج.م
صافي الدخل الخاضع للضريبة سنوياً: {r['annual_taxable']:>12,.2f} ج.م

تفصيل الشرائح الضريبية:
{rows}

إجمالي الضريبة السنوية:            {r['annual_tax']:>12,.2f} ج.م
الضريبة الشهرية:                   {r['monthly_tax']:>12,.2f} ج.م

═══════════════════════════════════════════
الراتب الصافي الشهري:              {r['net']:>12,.2f} ج.م
المعدل الضريبي الفعلي:             {r['effective_rate']:>11.2f}%
═══════════════════════════════════════════
"""


def extract_salary_amount(text: str) -> float | None:
    text_clean = text.replace(",", "").replace("،", "")
    patterns = [
        r'(\d+(?:\.\d+)?)\s*(?:ج\.م|جنيه|egp|le)',
        r'(?:راتب|gross|salary|مرتب|دخل)[\s:]*(\d+(?:\.\d+)?)',
        r'(\d{4,}(?:\.\d+)?)',
    ]
    for pat in patterns:
        m = re.search(pat, text_clean, re.IGNORECASE)
        if m:
            val = float(m.group(1))
            if 500 <= val <= 5_000_000:
                return val
    return None


CALC_TRIGGER_WORDS = [
    "احسب", "حساب", "كم صافي", "صافي راتب", "صافي مرتب",
    "كم يتبقى", "خصومات", "ضريبة", "تأمين", "نت", "net",
    "calculate", "salary calc", "كم راتب", "راتبي", "مرتبي",
]


def is_salary_calc_request(text: str) -> bool:
    lower = text.lower()
    has_trigger = any(w in lower for w in CALC_TRIGGER_WORDS)
    has_number = bool(re.search(r'\d{4,}', text.replace(",", "").replace("،", "")))
    return has_trigger and has_number


SYSTEM_PROMPT = f"""أنت مساعد الموارد البشرية الذكي لشركة 51Talk Egypt، اسمك "توكي".

مهمتك مساعدة موظفي الشركة في أسئلة سياسات الشركة، إجراءات HR، وحساب الرواتب والضرائب.

**قواعد مهمة جداً:**
1. أجب دائماً باللغة العربية بأسلوب واضح ومهني وودود.
2. استند في إجاباتك فقط إلى المعلومات الموجودة في دليل الموظف أدناه.
3. إذا وجدت [نتيجة حساب الراتب الصافي] في الرسالة، استخدم هذه الأرقام مباشرةً وقدّمها بشكل منسق وواضح بالعربية.
4. إذا كان السؤال يتعلق ببيانات شخصية (رصيد الإجازات، الحضور الفردي)، وجّه الموظف لـ hr.egy@51talk.com.
5. إذا لم تجد إجابة في الدليل، قل ذلك بصراحة واقترح التواصل مع HR.
6. لا تخترع معلومات غير موجودة في الدليل.
7. قدم إجاباتك بشكل منظم (نقاط، جداول، أرقام حسب الحاجة).

**دليل الموظف الرسمي:**
{HANDBOOK}

{SALARY_KNOWLEDGE}
"""

# ── Styling ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');

/* ── 51Talk Brand Design Tokens ── */
:root {
    --navy:          #162040;
    --navy-mid:      #1D2B50;
    --navy-panel:    #1A2645;
    --yellow:        #FFC800;
    --yellow-dark:   #E6B400;
    --yellow-glow:   rgba(255, 200, 0, 0.30);
    --yellow-soft:   rgba(255, 200, 0, 0.12);
    --glass:         rgba(255, 255, 255, 0.04);
    --glass-hover:   rgba(255, 255, 255, 0.08);
    --border:        rgba(255, 255, 255, 0.08);
    --border-yellow: rgba(255, 200, 0, 0.35);
    --text:          #F0F4FF;
    --text-muted:    rgba(240, 244, 255, 0.45);
}

/* ── Global ── */
html, body, [class*="css"], .stApp {
    font-family: 'Tajawal', sans-serif !important;
    direction: rtl;
}

/* ── Navy background + star lattice ── */
.stApp {
    background-color: var(--navy) !important;
    background-image:
        radial-gradient(ellipse 80% 45% at 50% 0%, rgba(255,200,0,0.10) 0%, transparent 65%),
        radial-gradient(circle, rgba(255,255,255,0.07) 1px, transparent 1px);
    background-size: 100% 100%, 32px 32px;
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
    background: var(--navy-panel) !important;
    border-left: 1px solid var(--border-yellow) !important;
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
    background: var(--yellow-soft) !important;
    border-color: var(--border-yellow) !important;
    color: var(--yellow) !important;
    box-shadow: 0 0 12px var(--yellow-glow) !important;
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

/* Assistant messages — yellow right accent */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    border-right: 3px solid var(--yellow) !important;
}

/* User messages — subtle yellow tint */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: rgba(255, 200, 0, 0.06) !important;
    border-color: var(--border-yellow) !important;
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
[data-testid="stChatMessage"] strong { color: var(--yellow) !important; }
[data-testid="stChatMessage"] ul,
[data-testid="stChatMessage"] ol { padding-right: 1.2rem; padding-left: 0; }

/* Avatar icons */
[data-testid="chatAvatarIcon-assistant"],
[data-testid="chatAvatarIcon-user"] {
    background: var(--navy-mid) !important;
    border: 2px solid var(--yellow) !important;
    border-radius: 10px !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: var(--navy-panel) !important;
    border: 1px solid var(--border-yellow) !important;
    border-radius: 14px !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--yellow) !important;
    box-shadow: 0 0 0 3px var(--yellow-glow) !important;
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

/* Send button */
[data-testid="stChatInput"] button {
    background: var(--yellow) !important;
    color: var(--navy) !important;
    border-radius: 10px !important;
}
[data-testid="stChatInput"] button:hover {
    background: var(--yellow-dark) !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] p { color: var(--text-muted) !important; direction: rtl; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--navy); }
::-webkit-scrollbar-thumb { background: rgba(255,200,0,0.35); border-radius: 99px; }

/* ── Animations ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes toki-float {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-6px); }
}

@keyframes shimmer-gold {
    0%   { background-position: 0% center; }
    100% { background-position: 200% center; }
}

/* ── Chat header ── */
.chat-header {
    text-align: center;
    padding: 2rem 0 1.5rem;
    direction: rtl;
}
.chat-header .toki-wrap {
    display: inline-block;
    margin-bottom: 0.6rem;
    animation: toki-float 3s ease-in-out infinite;
    filter: drop-shadow(0 8px 24px rgba(255,200,0,0.45));
}
.chat-header .toki-wrap img {
    width: 90px;
    height: 90px;
    object-fit: contain;
}
.chat-header .brand-badge {
    display: inline-block;
    background: linear-gradient(135deg, var(--yellow), #FFE066);
    color: var(--navy);
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    margin-bottom: 0.6rem;
}
.chat-header h1 {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(90deg, var(--yellow), #FFF5B0, var(--yellow));
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer-gold 4s linear infinite;
    margin: 0 0 0.3rem;
}
.chat-header p {
    color: var(--text-muted);
    font-size: 0.9rem;
    margin: 0;
}
.chat-header .divider {
    width: 60px; height: 2px;
    background: linear-gradient(90deg, transparent, var(--yellow), transparent);
    margin: 1rem auto 0;
    border-radius: 99px;
}

/* Sidebar brand strip */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.6rem 0.4rem 1rem;
    direction: rtl;
}
.sidebar-brand img {
    width: 40px;
    height: 40px;
    object-fit: contain;
    filter: drop-shadow(0 2px 8px rgba(255,200,0,0.4));
}
.sidebar-brand .sb-text {
    color: var(--yellow);
    font-weight: 800;
    font-size: 1rem;
    line-height: 1.1;
}
.sidebar-brand .sb-sub {
    color: var(--text-muted);
    font-size: 0.72rem;
}

/* HR contact card */
.hr-card {
    background: linear-gradient(135deg, rgba(255,200,0,0.10), rgba(255,200,0,0.05));
    border: 1px solid var(--border-yellow);
    border-radius: 12px;
    padding: 0.9rem 1rem;
    direction: rtl;
    text-align: right;
    margin-top: 0.5rem;
}
.hr-card .label { color: var(--text-muted); font-size: 0.75rem; margin-bottom: 0.2rem; }
.hr-card .email { color: var(--yellow); font-size: 0.85rem; font-weight: 700; }

/* Sidebar section title */
.sidebar-title {
    color: var(--yellow) !important;
    font-size: 0.70rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    direction: rtl;
    text-align: right;
    border-bottom: 1px solid rgba(255,200,0,0.2);
    padding-bottom: 0.25rem;
}

/* ── Payslip upload zone ── */
.upload-zone {
    background: linear-gradient(135deg, rgba(255,200,0,0.06), rgba(255,200,0,0.03));
    border: 1.5px dashed rgba(255,200,0,0.35);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
    direction: rtl;
    text-align: right;
    transition: border-color 0.2s;
}
.upload-zone:hover { border-color: rgba(255,200,0,0.65); }
.upload-zone .uz-title {
    color: var(--yellow);
    font-weight: 700;
    font-size: 0.9rem;
    margin-bottom: 0.2rem;
}
.upload-zone .uz-hint {
    color: var(--text-muted);
    font-size: 0.78rem;
}

/* Attached badge */
.attached-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(255,200,0,0.1);
    border: 1px solid rgba(255,200,0,0.3);
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    color: var(--yellow);
    font-size: 0.8rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    direction: rtl;
}

/* Style the Streamlit file uploader */
[data-testid="stFileUploader"] {
    background: transparent !important;
    direction: rtl;
}
[data-testid="stFileUploader"] section {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
[data-testid="stFileUploader"] label {
    color: var(--text-muted) !important;
    font-family: 'Tajawal', sans-serif !important;
    font-size: 0.85rem !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1.5px dashed rgba(255,200,0,0.3) !important;
    border-radius: 10px !important;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: rgba(255,200,0,0.6) !important;
    background: rgba(255,200,0,0.04) !important;
}
[data-testid="stFileUploaderDropzone"] span {
    color: var(--text-muted) !important;
    font-family: 'Tajawal', sans-serif !important;
}
[data-testid="stFileUploaderDropzone"] button {
    background: var(--yellow) !important;
    color: var(--navy) !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    font-family: 'Tajawal', sans-serif !important;
}

/* Payslip thumbnail in chat */
[data-testid="stChatMessage"] img {
    border-radius: 10px;
    max-width: 280px;
    border: 1px solid var(--border-yellow);
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
_toki_src = f"data:image/png;base64,{TOKI_B64}" if TOKI_B64 else "https://placehold.co/90x90/FFC800/162040?text=HR"
st.markdown(f"""
<div class="chat-header">
    <div class="toki-wrap">
        <img src="{_toki_src}" alt="Toki">
    </div>
    <div><span class="brand-badge">51Talk Egypt</span></div>
    <h1>مساعد HR</h1>
    <p>مرحباً! أنا توكي، مساعدك في الموارد البشرية 🌟</p>
    <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-brand">
        <img src="{_toki_src}" alt="Toki">
        <div>
            <div class="sb-text">51Talk Egypt</div>
            <div class="sb-sub">Human Resources Assistant</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<p class="sidebar-title">سياسات الشركة</p>', unsafe_allow_html=True)
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

    st.markdown('<p class="sidebar-title" style="margin-top:1rem">iTalent</p>', unsafe_allow_html=True)
    italent_suggestions = [
        "كيف أسجل الحضور والانصراف في iTalent؟",
        "كيف أطلب إجازة في iTalent؟",
        "كيف أتابع طلبات الإجازة؟",
        "كيف أفتح iTalent؟",
        "كيف أطلب مأمورية في iTalent؟",
    ]
    for s in italent_suggestions:
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
        st.session_state.pending_salary_gross = None
        st.rerun()

# ── Chat state ────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "attached_image" not in st.session_state:
    st.session_state.attached_image = None
if "pending_salary_gross" not in st.session_state:
    st.session_state.pending_salary_gross = None  # gross stored while awaiting commission

# Welcome message on first load
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("""
مرحباً! 👋 أنا **توكي**، مساعد HR الخاص بشركة **51Talk Egypt**.

يمكنني مساعدتك في:
- 📅 سياسات الإجازات (السنوية، المرضية، الأمومة...)
- ⏰ جداول العمل والحضور والغيابات
- 💰 الرواتب والمزايا والتعويضات
- 🧮 **حساب صافي الراتب والضريبة** — فقط اكتب مثلاً: *"احسب صافي راتب 15000 جنيه"*
- 📋 قواعد السلوك المهني ومعايير العمل
- 📝 إجراءات الاستقالة والتوظيف
- 📱 نظام **iTalent** — الحضور وطلبات الإجازة والمأموريات
- 🧾 كشوف الرواتب — أرفق صورة وأنا أشرحها لك!

كيف يمكنني مساعدتك اليوم؟
        """)

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("image_b64"):
            img_bytes = base64.b64decode(msg["image_b64"])
            st.image(img_bytes, width=260)
        st.markdown(msg["content"])

# ── Groq API functions ────────────────────────────────────────────────────────
def _client() -> Groq:
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        st.error("⚠️ مفتاح API غير موجود.")
        st.stop()
    return Groq(api_key=api_key)


def get_text_response(messages: list[dict]) -> str:
    """HR handbook Q&A — text only."""
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in messages
    ]
    response = _client().chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history,
        temperature=0.2,
        max_tokens=1500,
    )
    return response.choices[0].message.content


def get_vision_response(question: str, image_b64: str, mime: str) -> str:
    """Payslip reading — vision model."""
    system = (
        "أنت مساعد HR متخصص في قراءة كشوف الرواتب. "
        "اقرأ الصورة المرفقة بعناية وأجب على سؤال الموظف باللغة العربية "
        "بشكل واضح ودقيق. إذا رأيت أرقاماً أو بنوداً، اشرحها بالتفصيل."
    )
    response = _client().chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": [
                    {"type": "image_url",
                     "image_url": {"url": f"data:{mime};base64,{image_b64}"}},
                    {"type": "text", "text": question or "اشرح لي محتوى كشف الراتب هذا."},
                ],
            },
        ],
        temperature=0.2,
        max_tokens=1500,
    )
    return response.choices[0].message.content


_NO_COMMISSION_WORDS = [
    "لا", "لأ", "لا يوجد", "لا توجد", "مفيش", "ما فيش", "بدون",
    "بدون عمولة", "no", "none", "zero", "0", "nothing",
]

_COMMISSION_QUESTION = (
    "حسناً! قبل ما أكمل الحساب، هل لديك **عمولة** هذا الشهر؟ 💰\n\n"
    "- إذا **نعم** — أخبرني بمبلغها وسأضيفها للراتب قبل الحساب.\n"
    "- إذا **لا** — اكتب «لا» أو «0» وسأحسب على الراتب الأساسي مباشرةً.\n\n"
    "الراتب الأساسي المُسجَّل: **{gross:,.0f} ج.م**"
)


def _is_no_commission(text: str) -> bool:
    t = text.strip().lower()
    return any(t == w or t.startswith(w + " ") for w in _NO_COMMISSION_WORDS)


def handle_input(user_input: str) -> None:
    image_data = st.session_state.attached_image
    image_b64 = base64.b64encode(image_data[0]).decode() if image_data else None
    pending_gross = st.session_state.pending_salary_gross

    # ── Step 2: user is replying to the commission question ──────────────────
    if not image_data and pending_gross is not None:
        commission = extract_salary_amount(user_input)
        no_comm = _is_no_commission(user_input)

        if commission is not None or no_comm:
            comm_amount = commission or 0.0
            total = pending_gross + comm_amount
            st.session_state.pending_salary_gross = None

            if comm_amount > 0:
                calc_note = (
                    f"الراتب الأساسي {pending_gross:,.2f} ج.م + العمولة {comm_amount:,.2f} ج.م"
                    f" = الإجمالي {total:,.2f} ج.م"
                )
            else:
                calc_note = f"الراتب الأساسي {pending_gross:,.2f} ج.م (بدون عمولة)"

            effective_input = (
                user_input
                + f"\n\n[{calc_note}]\n\n"
                + salary_calc_context(total)
            )

            _record_and_show_user(user_input, image_data)
            _call_and_show_assistant(effective_input)
            return

        # Can't parse the reply — fall through to normal LLM response
        _record_and_show_user(user_input, image_data)
        messages_for_api = st.session_state.messages[:]
        _call_and_show_assistant(user_input, messages_for_api)
        return

    # ── Step 1: user provides a gross salary — ask about commission ──────────
    if not image_data and is_salary_calc_request(user_input):
        gross = extract_salary_amount(user_input)
        if gross:
            st.session_state.pending_salary_gross = gross
            _record_and_show_user(user_input, image_data)
            reply = _COMMISSION_QUESTION.format(gross=gross)
            with st.chat_message("assistant"):
                st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            return

    # ── Default: normal LLM Q&A ───────────────────────────────────────────────
    _record_and_show_user(user_input, image_data)
    messages_for_api = st.session_state.messages[:]

    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير..."):
            if image_data:
                reply = get_vision_response(user_input, image_b64, image_data[1])
            else:
                reply = get_text_response(messages_for_api)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.attached_image = None


def _record_and_show_user(user_input: str, image_data) -> None:
    image_b64 = base64.b64encode(image_data[0]).decode() if image_data else None
    msg_record = {"role": "user", "content": user_input}
    if image_b64:
        msg_record["image_b64"] = image_b64
    st.session_state.messages.append(msg_record)
    with st.chat_message("user"):
        if image_data:
            st.image(image_data[0], width=260)
        st.markdown(user_input)


def _call_and_show_assistant(effective_input: str, messages_for_api: list | None = None) -> None:
    if messages_for_api is None:
        messages_for_api = st.session_state.messages[:-1] + [
            {"role": "user", "content": effective_input}
        ]
    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير..."):
            reply = get_text_response(messages_for_api)
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.attached_image = None


# ── Payslip upload zone ───────────────────────────────────────────────────────
st.markdown("""
<div class="upload-zone">
    <div class="uz-title">🧾 إرفاق كشف راتب</div>
    <div class="uz-hint">ارفع صورة كشف راتبك واسأل عنه مباشرةً</div>
</div>
""", unsafe_allow_html=True)

uploaded = st.file_uploader(
    label="",
    type=["png", "jpg", "jpeg", "webp"],
    label_visibility="collapsed",
    key="payslip_upload",
)

if uploaded:
    img_bytes = uploaded.read()
    mime = uploaded.type or "image/jpeg"
    st.session_state.attached_image = (img_bytes, mime)
    st.image(img_bytes, caption="✅ الصورة مرفقة — اكتب سؤالك وأرسل", width=260)
elif st.session_state.attached_image:
    st.markdown('<span class="attached-badge">📎 صورة مرفقة</span>', unsafe_allow_html=True)

# ── Input handling ────────────────────────────────────────────────────────────
if "pending_input" in st.session_state:
    pending = st.session_state.pop("pending_input")
    handle_input(pending)

placeholder = "اسأل عن كشف راتبك..." if st.session_state.attached_image else "اكتب سؤالك هنا..."
if prompt := st.chat_input(placeholder):
    handle_input(prompt)
