import re

_TAX_BRACKETS: list[tuple[float, float]] = [
    (40_000,       0.00),
    (55_000,       0.10),
    (70_000,       0.15),
    (200_000,      0.20),
    (400_000,      0.225),
    (1_200_000,    0.25),
    (float("inf"), 0.275),
]
_SI_RATE       = 0.11
_SI_CAP        = 16_700.0
_SI_FLOOR      = 2_700.0
_MARTYRS_RATE  = 0.0005
_ANNUAL_EXEMPT = 20_000.0

_MIN_VALID_SALARY = 500.0
_MAX_VALID_SALARY = 5_000_000.0

CALC_TRIGGER_WORDS: list[str] = [
    "احسب", "حساب", "كم صافي", "صافي راتب", "صافي مرتب",
    "كم يتبقى", "خصومات", "ضريبة", "تأمين", "نت", "net",
    "calculate", "salary calc", "كم راتب", "راتبي", "مرتبي",
]

_NO_COMMISSION_WORDS: list[str] = [
    "لا", "لأ", "لا يوجد", "لا توجد", "مفيش", "ما فيش", "بدون",
    "بدون عمولة", "no", "none", "zero", "0", "nothing",
]


def calculate_net_salary(gross: float) -> dict:
    if not (_MIN_VALID_SALARY <= gross <= _MAX_VALID_SALARY):
        raise ValueError(f"Gross salary must be between {_MIN_VALID_SALARY:,.0f} and {_MAX_VALID_SALARY:,.0f}")

    insurable = max(_SI_FLOOR, min(gross, _SI_CAP))
    monthly_si = round(insurable * _SI_RATE, 2)
    monthly_martyrs = round(gross * _MARTYRS_RATE, 2)

    annual_gross = gross * 12
    annual_si = monthly_si * 12
    annual_before_exempt = annual_gross - annual_si
    annual_taxable = max(0.0, annual_before_exempt - _ANNUAL_EXEMPT)

    annual_tax = 0.0
    prev = 0.0
    breakdown: list[dict] = []
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
            breakdown.append({
                "شريحة (سنوي)": label,
                "نسبة": f"{rate * 100:.1f}%",
                "دخل في الشريحة": f"{chunk:,.2f}",
                "ضريبة": f"{tax:,.2f}",
            })
        annual_tax += tax
        remaining -= chunk
        prev = limit if limit != float("inf") else prev

    monthly_tax = round(annual_tax / 12, 2)
    net = round(gross - monthly_si - monthly_tax - monthly_martyrs, 2)
    effective = round(annual_tax / annual_gross * 100, 2) if annual_gross else 0.0

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
            if _MIN_VALID_SALARY <= val <= _MAX_VALID_SALARY:
                return val
    return None


def is_salary_calc_request(text: str) -> bool:
    if not text or not text.strip():
        return False
    lower = text.lower()
    has_trigger = any(w in lower for w in CALC_TRIGGER_WORDS)
    has_number = bool(re.search(r'\d{4,}', text.replace(",", "").replace("،", "")))
    return has_trigger and has_number


def is_no_commission(text: str) -> bool:
    t = text.strip().lower()
    return any(t == w or t.startswith(w + " ") for w in _NO_COMMISSION_WORDS)
