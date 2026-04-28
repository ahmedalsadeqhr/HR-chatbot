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

# ── UI translations ───────────────────────────────────────────────────────────
UI = {
    "ar": {
        "dir":              "rtl",
        "page_icon":        "🐣",
        "header_title":     "مساعد HR",
        "header_sub":       "مرحباً! أنا توكي، مساعدك في الموارد البشرية 🌟",
        "brand_sub":        "مساعد الموارد البشرية",
        "switch_lang":      "🇬🇧 English",
        "section_policies": "سياسات الشركة",
        "section_italent":  "iTalent",
        "hr_label":         "📧 تواصل مع فريق HR",
        "clear_chat":       "🗑️ مسح المحادثة",
        "upload_title":     "🧾 إرفاق كشف راتب",
        "upload_hint":      "ارفع صورة كشف راتبك واسأل عنه مباشرةً",
        "image_caption":    "✅ الصورة مرفقة — اكتب سؤالك وأرسل",
        "attached_badge":   "📎 صورة مرفقة",
        "spinner":          "جاري التفكير...",
        "placeholder":      "اكتب سؤالك هنا...",
        "placeholder_img":  "اسأل عن كشف راتبك...",
        "api_error":        "⚠️ مفتاح API غير موجود.",
        "suggestions": [
            "كم يوم إجازة سنوية لديّ؟",
            "ما هو نظام الحضور والانصراف؟",
            "ما هي عقوبة التأخير؟",
            "ما هي إجراءات الاستقالة؟",
            "ما هو موعد صرف الراتب؟",
            "ما هي سياسة الإجازة المرضية؟",
            "ما هو كود اللبس الرسمي؟",
            "كيف أتواصل مع HR؟",
        ],
        "italent_suggestions": [
            "كيف أسجل الحضور والانصراف في iTalent؟",
            "كيف أطلب إجازة في iTalent؟",
            "كيف أتابع طلبات الإجازة؟",
            "كيف أفتح iTalent؟",
            "كيف أطلب مأمورية في iTalent؟",
        ],
        "welcome": (
            "مرحباً! 👋 أنا **توكي**، مساعد HR الخاص بشركة **51Talk Egypt**.\n\n"
            "يمكنني مساعدتك في:\n"
            "- 📅 سياسات الإجازات (السنوية، المرضية، الأمومة...)\n"
            "- ⏰ جداول العمل والحضور والغيابات\n"
            "- 💰 الرواتب والمزايا والتعويضات\n"
            "- 🧮 **حساب صافي الراتب والضريبة** — اكتب مثلاً: *«احسب صافي راتب 15000 جنيه»*\n"
            "- 📋 قواعد السلوك المهني ومعايير العمل\n"
            "- 📝 إجراءات الاستقالة والتوظيف\n"
            "- 📱 نظام **iTalent** — الحضور وطلبات الإجازة والمأموريات\n"
            "- 🧾 كشوف الرواتب — أرفق صورة وأنا أشرحها لك!\n\n"
            "كيف يمكنني مساعدتك اليوم؟"
        ),
        "commission_q": (
            "حسناً! قبل ما أكمل الحساب، هل لديك **عمولة** هذا الشهر؟ 💰\n\n"
            "- إذا **نعم** — أخبرني بمبلغها وسأضيفها للراتب قبل الحساب.\n"
            "- إذا **لا** — اكتب «لا» أو «0» وسأحسب على الراتب الأساسي مباشرةً.\n\n"
            "الراتب الأساسي المُسجَّل: **{gross:,.0f} ج.م**"
        ),
        "calc_with_comm":    "الراتب الأساسي {base:,.2f} ج.م + العمولة {comm:,.2f} ج.م = الإجمالي {total:,.2f} ج.م",
        "calc_no_comm":      "الراتب الأساسي {base:,.2f} ج.م (بدون عمولة)",
        "system_lang_instr": "أجب دائماً باللغة العربية.",
        "vision_system": (
            "أنت مساعد HR متخصص في قراءة كشوف الرواتب لشركة 51Talk Egypt. "
            "اقرأ الصورة المرفقة بعناية وأجب على سؤال الموظف باللغة العربية "
            "بشكل واضح ودقيق. إذا رأيت أرقاماً أو بنوداً، اشرحها بالتفصيل. "
            "إذا كان السؤال لا علاقة له بكشف الراتب أو شؤون الموارد البشرية، "
            "رفض الإجابة بأدب وأخبر المستخدم أن اختصاصك محدود في الموارد البشرية فقط."
        ),
        "vision_default_q": "اشرح لي محتوى كشف الراتب هذا.",
        "out_of_scope": (
            "عذراً، أنا متخصص فقط في شؤون الموارد البشرية لشركة 51Talk Egypt. "
            "لا أستطيع الإجابة على أسئلة خارج نطاق عملي.\n\n"
            "يمكنني مساعدتك في: الإجازات، الرواتب، الحضور، سياسات الشركة، نظام iTalent، وكشوف الرواتب. "
            "هل لديك سؤال في هذه المجالات؟ 😊"
        ),
    },
    "en": {
        "dir":              "ltr",
        "page_icon":        "🐣",
        "header_title":     "HR Assistant",
        "header_sub":       "Hi! I'm Toki, your HR assistant 🌟",
        "brand_sub":        "Human Resources Assistant",
        "switch_lang":      "🇸🇦 العربية",
        "section_policies": "Company Policies",
        "section_italent":  "iTalent",
        "hr_label":         "📧 Contact HR Team",
        "clear_chat":       "🗑️ Clear Chat",
        "upload_title":     "🧾 Attach Payslip",
        "upload_hint":      "Upload a photo of your payslip and ask about it",
        "image_caption":    "✅ Image attached — type your question and send",
        "attached_badge":   "📎 Image attached",
        "spinner":          "Thinking...",
        "placeholder":      "Type your question here...",
        "placeholder_img":  "Ask about your payslip...",
        "api_error":        "⚠️ API key not found.",
        "suggestions": [
            "How many annual leave days do I have?",
            "What is the attendance system?",
            "What is the penalty for being late?",
            "What is the resignation process?",
            "When is salary paid?",
            "What is the sick leave policy?",
            "What is the dress code?",
            "How do I contact HR?",
        ],
        "italent_suggestions": [
            "How do I clock in/out on iTalent?",
            "How do I request leave on iTalent?",
            "How do I track my leave requests?",
            "How do I access iTalent?",
            "How do I request a business trip on iTalent?",
        ],
        "welcome": (
            "Hello! 👋 I'm **Toki**, the HR assistant for **51Talk Egypt**.\n\n"
            "I can help you with:\n"
            "- 📅 Leave policies (annual, sick, maternity...)\n"
            "- ⏰ Work schedules, attendance & absences\n"
            "- 💰 Salaries, benefits & compensation\n"
            "- 🧮 **Net salary & tax calculator** — just type e.g. *\"calculate net salary 15000 EGP\"*\n"
            "- 📋 Professional conduct & workplace standards\n"
            "- 📝 Resignation & onboarding procedures\n"
            "- 📱 **iTalent** system — attendance, leave & business trips\n"
            "- 🧾 Payslips — attach an image and I'll explain it!\n\n"
            "How can I help you today?"
        ),
        "commission_q": (
            "Got it! Before I calculate, do you have a **commission** this month? 💰\n\n"
            "- If **yes** — tell me the amount and I'll add it to your salary before calculating.\n"
            "- If **no** — just type \"no\" or \"0\" and I'll calculate on your base salary.\n\n"
            "Recorded base salary: **{gross:,.0f} EGP**"
        ),
        "calc_with_comm":    "Base {base:,.2f} EGP + Commission {comm:,.2f} EGP = Total {total:,.2f} EGP",
        "calc_no_comm":      "Base salary {base:,.2f} EGP (no commission)",
        "system_lang_instr": "Always respond in English.",
        "vision_system": (
            "You are an HR assistant for 51Talk Egypt specializing in reading payslips. "
            "Read the attached image carefully and answer the employee's question in English "
            "clearly and accurately. If you see numbers or line items, explain them in detail. "
            "If the question is unrelated to the payslip or HR matters, politely decline and "
            "remind the user that your scope is limited to HR topics only."
        ),
        "vision_default_q": "Please explain the contents of this payslip.",
        "out_of_scope": (
            "Sorry, I'm only able to help with HR-related topics for 51Talk Egypt. "
            "That question is outside my scope.\n\n"
            "I can assist with: leave policies, salaries, attendance, company policies, "
            "the iTalent system, and payslip explanations. Do you have a question in those areas? 😊"
        ),
    },
}

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

# ── Egyptian Salary Calculation Knowledge (2026) ──────────────────────────────
SALARY_KNOWLEDGE = """
12. SALARY CALCULATION & TAX DEDUCTIONS (Egypt 2026)

HOW YOUR NET SALARY IS CALCULATED — STEP BY STEP:

STEP 1 — Social & Health Insurance (Employee Share)
  Rate:           11% (Social Insurance only)
  Applied to:     Your "insurable wage" (basic salary + fixed allowances)
  Monthly cap:    EGP 16,700 maximum insurable wage (2026 figure)
  Monthly floor:  EGP 2,700 minimum insurable wage (2026 figure)
  Max deduction:  EGP 16,700 × 11% = EGP 1,837/month
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

QUICK EXAMPLES (2026 figures):
  Gross EGP 5,000/month  → approx. net EGP 4,448/month
  Gross EGP 10,000/month → approx. net EGP 8,303/month
  Gross EGP 15,000/month → approx. net EGP 11,860/month
  Gross EGP 20,000/month → approx. net EGP 15,708/month
  Gross EGP 30,000/month → approx. net EGP 23,457/month
  Gross EGP 50,000/month → approx. net EGP 38,618/month

KEY NOTES:
  - Tax is calculated on annual income then divided by 12 for monthly payslip.
  - The SI cap means all employees earning above EGP 16,700/month pay the
    same fixed SI deduction of EGP 1,837/month.
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
_SI_RATE       = 0.11    # 11% social insurance (employee share)
_SI_CAP        = 16_700
_SI_FLOOR      = 2_700
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


def build_system_prompt(lang: str) -> str:
    lang_instr = UI[lang]["system_lang_instr"]
    out_of_scope_reply = UI[lang]["out_of_scope"]
    return f"""You are Toki, the smart HR assistant for 51Talk Egypt.
Your ONLY job is to help employees with HR-related topics for 51Talk Egypt.

══════════════════════════════════════════
SCOPE ENFORCEMENT — READ THIS FIRST
══════════════════════════════════════════
You are STRICTLY limited to these topics:
  • Company policies (leave, attendance, conduct, dress code, resignation)
  • Salary, tax, and compensation questions
  • iTalent system usage
  • Payslip explanations (when an image is attached)
  • HR contact and escalation procedures

If the user's message is about ANYTHING outside this list — including but not limited to:
  food, recipes, cooking, sports, news, science, history, coding, general knowledge,
  entertainment, travel, relationships, health advice, or any non-HR topic —
you MUST respond with EXACTLY this message and nothing else:

"{out_of_scope_reply}"

Do NOT attempt to answer, do NOT explain why, do NOT apologize at length.
Just return that exact message.
══════════════════════════════════════════

Critical rules:
1. {lang_instr} Use a clear, professional, and friendly tone.
2. Base your answers only on the Employee Handbook and Salary Knowledge below.
3. If the message contains [Net Salary Calculation Result], use those exact numbers and present them clearly.
4. For personal data questions (individual leave balance, personal attendance), direct the employee to hr.egy@51talk.com.
5. If the answer is not in the handbook, say so honestly and suggest contacting HR.
6. Never invent information not in the handbook.
7. Present answers in an organized format (bullet points, tables, numbered steps as needed).

Employee Handbook:
{HANDBOOK}

{SALARY_KNOWLEDGE}
"""

# ── Styling ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;500;600;700;800&family=Tajawal:wght@400;500;700;800&display=swap');

/* ══════════════════════════════════════════════════
   51Talk × Toki — "Warm Starfield" Design System
   ══════════════════════════════════════════════════ */
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

    /* Legacy aliases so LTR override block stays consistent */
    --yellow:        #FFC800;
    --yellow-dark:   #D4A800;
    --yellow-glow:   rgba(255, 200, 0, 0.22);
    --yellow-soft:   rgba(255, 200, 0, 0.08);
    --border-yellow: rgba(255, 200, 0, 0.28);
    --text:          #F5EDD6;
    --text-muted:    rgba(245, 237, 214, 0.42);
}

/* ════════════════ GLOBAL ════════════════ */
html, body, [class*="css"], .stApp {
    font-family: 'Nunito', 'Tajawal', sans-serif !important;
    direction: rtl;
    color: var(--cream) !important;
}

/* ════════════════ BACKGROUND — deep navy + amber bloom + noise grain ════════ */
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
[data-testid="block-container"] { padding-top: 1rem !important; max-width: 800px; }
[data-testid="stMain"] { background: transparent !important; }

/* ════════════════ STAR FIELD ════════════════ */
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

/* ════════════════ SIDEBAR ════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1932 0%, #0A1428 100%) !important;
    border-left: 1px solid rgba(255,200,0,0.22) !important;
    box-shadow: inset -1px 0 0 rgba(255,200,0,0.06);
}
[data-testid="stSidebar"] > div { padding-top: 1.2rem; }

/* Sidebar suggestion buttons */
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
    transition: all 0.18s ease !important;
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
    transform: translateX(-1px) scale(0.98) !important;
}

/* Clear / destructive button */
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

/* ════════════════ CHAT MESSAGES ════════════════ */
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
/* Warm paper tint for assistant */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: linear-gradient(135deg,
        rgba(255,248,220,0.055) 0%,
        rgba(255,200,0,0.028) 100%) !important;
    border-color: rgba(255,200,0,0.18) !important;
    border-right: 3px solid var(--amber) !important;
}
/* Subtle top gleam on assistant bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"])::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,200,0,0.35), transparent);
}
/* User messages — slightly elevated navy card */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: rgba(255,200,0,0.055) !important;
    border-color: rgba(255,200,0,0.22) !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.30), 0 0 0 1px rgba(255,200,0,0.08) !important;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span {
    direction: rtl !important;
    text-align: right !important;
    color: var(--cream) !important;
    font-family: 'Nunito', 'Tajawal', sans-serif !important;
    font-size: 0.96rem !important;
    line-height: 1.8 !important;
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

/* Avatars */
[data-testid="chatAvatarIcon-assistant"],
[data-testid="chatAvatarIcon-user"] {
    background: var(--navy-mid) !important;
    border: 2px solid var(--amber) !important;
    border-radius: 12px !important;
    box-shadow: 0 0 12px rgba(255,200,0,0.25) !important;
}

/* ════════════════ CHAT INPUT ════════════════ */
[data-testid="stChatInput"] {
    background: rgba(15,28,58,0.85) !important;
    border: 1.5px solid rgba(255,200,0,0.25) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(12px);
    transition: border-color 0.22s, box-shadow 0.22s !important;
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
    transition: transform 0.12s, box-shadow 0.12s !important;
}
[data-testid="stChatInput"] button:hover {
    transform: scale(1.06) !important;
    box-shadow: 0 4px 14px rgba(255,200,0,0.35) !important;
}
[data-testid="stChatInput"] button:active { transform: scale(0.96) !important; }

/* ════════════════ SPINNER ════════════════ */
[data-testid="stSpinner"] p { color: var(--cream-muted) !important; direction: rtl; font-family: 'Nunito','Tajawal',sans-serif !important; }

/* ════════════════ SCROLLBAR ════════════════ */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,200,0,0.28); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,200,0,0.50); }

/* ════════════════ ANIMATIONS ════════════════ */
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

/* ════════════════ HEADER CARD ════════════════ */
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
    letter-spacing: 0.01em;
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

/* ════════════════ SIDEBAR BRAND STRIP ════════════════ */
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

/* ════════════════ SIDEBAR SECTION TITLES ════════════════ */
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

/* ════════════════ HR CONTACT CARD ════════════════ */
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

/* ════════════════ UPLOAD ZONE ════════════════ */
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

/* Attached badge */
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

/* ════════════════ FILE UPLOADER ════════════════ */
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
}

/* ════════════════ PAYSLIP THUMBNAIL ════════════════ */
[data-testid="stChatMessage"] img {
    border-radius: 12px;
    max-width: 280px;
    border: 1px solid rgba(255,200,0,0.28);
    margin-bottom: 0.5rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.4);
}
</style>
""", unsafe_allow_html=True)

# ── Language state (must be before any UI rendering) ─────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
lang = st.session_state.lang
T = UI[lang]

# Direction override for English (base CSS is RTL)
if lang == "en":
    st.markdown("""
    <style>
    html, body, [class*="css"], .stApp {
        direction: ltr !important;
    }
    [data-testid="stSidebar"] { direction: ltr !important; border-left: none !important; border-right: 1px solid var(--border-yellow) !important; }
    [data-testid="stChatMessage"] { direction: ltr !important; text-align: left !important; }
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span { direction: ltr !important; text-align: left !important; }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) { border-right: none !important; border-left: 3px solid var(--yellow) !important; }
    [data-testid="stChatInput"] textarea { direction: ltr !important; text-align: left !important; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { text-align: left !important; }
    .chat-header, .sidebar-title, .hr-card, .upload-zone, .attached-badge { direction: ltr !important; text-align: left !important; }
    .sidebar-brand { direction: ltr !important; }
    </style>
    """, unsafe_allow_html=True)

# ── Star field (decorative, fixed background) ────────────────────────────────
st.markdown("""
<div class="star-field" aria-hidden="true">
  <div class="stars-sm"></div>
  <div class="stars-md"></div>
  <div class="stars-lg"></div>
</div>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
_toki_src = f"data:image/png;base64,{TOKI_B64}" if TOKI_B64 else "https://placehold.co/90x90/FFC800/162040?text=HR"
st.markdown(f"""
<div class="chat-header">
    <div class="toki-wrap">
        <img src="{_toki_src}" alt="Toki">
    </div>
    <div><span class="brand-badge">51Talk Egypt</span></div>
    <h1>{T["header_title"]}</h1>
    <p>{T["header_sub"]}</p>
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
            <div class="sb-sub">{T["brand_sub"]}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Language toggle
    if st.button(T["switch_lang"], use_container_width=True, key="lang_toggle"):
        st.session_state.lang = "en" if lang == "ar" else "ar"
        st.session_state.messages = []
        st.session_state.pending_salary_gross = None
        st.rerun()

    st.markdown(f'<p class="sidebar-title" style="margin-top:0.8rem">{T["section_policies"]}</p>', unsafe_allow_html=True)
    for s in T["suggestions"]:
        if st.button(s, use_container_width=True, key=s):
            st.session_state["pending_input"] = s

    st.markdown(f'<p class="sidebar-title" style="margin-top:1rem">{T["section_italent"]}</p>', unsafe_allow_html=True)
    for s in T["italent_suggestions"]:
        if st.button(s, use_container_width=True, key=s):
            st.session_state["pending_input"] = s

    st.markdown(f"""
    <div class="hr-card">
        <div class="label">{T["hr_label"]}</div>
        <div class="email">hr.egy@51talk.com</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(T["clear_chat"], use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_salary_gross = None
        st.rerun()

# ── Chat state ────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "attached_image" not in st.session_state:
    st.session_state.attached_image = None
if "pending_salary_gross" not in st.session_state:
    st.session_state.pending_salary_gross = None

# Welcome message on first load
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(T["welcome"])

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
        st.error(T["api_error"])
        st.stop()
    return Groq(api_key=api_key)


def get_text_response(messages: list[dict]) -> str:
    history = [{"role": m["role"], "content": m["content"]} for m in messages]
    response = _client().chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": build_system_prompt(lang)}] + history,
        temperature=0.2,
        max_tokens=1500,
    )
    return response.choices[0].message.content


def get_vision_response(question: str, image_b64: str, mime: str) -> str:
    response = _client().chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "system", "content": T["vision_system"]},
            {
                "role": "user",
                "content": [
                    {"type": "image_url",
                     "image_url": {"url": f"data:{mime};base64,{image_b64}"}},
                    {"type": "text", "text": question or T["vision_default_q"]},
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
                calc_note = T["calc_with_comm"].format(base=pending_gross, comm=comm_amount, total=total)
            else:
                calc_note = T["calc_no_comm"].format(base=pending_gross)

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
            reply = T["commission_q"].format(gross=gross)
            with st.chat_message("assistant"):
                st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            return

    # ── Default: normal LLM Q&A ───────────────────────────────────────────────
    _record_and_show_user(user_input, image_data)
    messages_for_api = st.session_state.messages[:]

    with st.chat_message("assistant"):
        with st.spinner(T["spinner"]):
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
        with st.spinner(T["spinner"]):
            reply = get_text_response(messages_for_api)
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.attached_image = None


# ── Payslip upload zone ───────────────────────────────────────────────────────
st.markdown(f"""
<div class="upload-zone">
    <div class="uz-title">{T["upload_title"]}</div>
    <div class="uz-hint">{T["upload_hint"]}</div>
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
    st.image(img_bytes, caption=T["image_caption"], width=260)
elif st.session_state.attached_image:
    st.markdown(f'<span class="attached-badge">{T["attached_badge"]}</span>', unsafe_allow_html=True)

# ── Input handling ────────────────────────────────────────────────────────────
if "pending_input" in st.session_state:
    pending = st.session_state.pop("pending_input")
    handle_input(pending)

placeholder = T["placeholder_img"] if st.session_state.attached_image else T["placeholder"]
if prompt := st.chat_input(placeholder):
    handle_input(prompt)
