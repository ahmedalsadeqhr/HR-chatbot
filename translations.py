UI: dict[str, dict] = {
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
        "api_invalid_key":  "⚠️ مفتاح API غير صالح. تواصل مع فريق الدعم التقني.",
        "api_rate_limit":   "⚠️ تم تجاوز حد الطلبات. انتظر لحظة وحاول مجدداً.",
        "api_connection":   "⚠️ خطأ في الاتصال. تحقق من اتصالك بالإنترنت.",
        "api_generic":      "⚠️ حدث خطأ غير متوقع. حاول مجدداً.",
        "calc_out_of_range": "⚠️ إجمالي الراتب والعمولة كبير جداً أو صغير جداً لحسابه. تواصل مع hr.egy@51talk.com لمساعدتك.",
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
        "api_invalid_key":  "⚠️ Invalid API key. Please contact technical support.",
        "api_rate_limit":   "⚠️ Rate limit exceeded. Please wait a moment and try again.",
        "api_connection":   "⚠️ Connection error. Please check your internet connection.",
        "api_generic":      "⚠️ An unexpected error occurred. Please try again.",
        "calc_out_of_range": "⚠️ The total salary and commission is too high or too low to calculate. Please contact hr.egy@51talk.com for help.",
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
