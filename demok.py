import streamlit as st
import re
import random

# --- Helper function to get translation based on session state ---
def get_translation_data():
    """Returns the current translation dictionary (t) and the full language map."""
    
    # ------------------ Translation Dictionary ------------------
    # Define the dictionary entirely first
    translations = {
        "en": {
            "page_title": "Phishing & URL Checker",
            "email_checker": "Email Checker",
            "url_checker": "URL Checker",
            "email_title": "AI Gmail Phishing Detector",
            "email_desc": "Paste the content of a suspicious email below to analyze it for phishing indicators, including sender verification and phone number requests. Include the 'From:' field if possible for better accuracy.",
            "email_input": "Email Content",
            "email_placeholder": "Paste the full content of the email, including sender details (e.g., From: example@gmail.com)...",
            "analyze_button": "Analyze for Phishing",
            "no_content_warning": "Please paste some email content to analyze.",
            "analysis_results": "Analysis Results",
            "phishing_score": "Phishing Score",
            "detected_sender": "Detected Sender",
            "indicators": "Detected Phishing Indicators:",
            "no_indicators": "No obvious phishing indicators detected. This email appears safe.",
            "safe_sender": "Sender appears to be a legitimate address with no suspicious verification requests detected.",
            "footer": "Prototype built with Streamlit. For educational/demo purposes only. Always verify suspicious emails manually.",
            "url_title": "URL Phishing Checker",
            "url_desc": "Paste a URL below to check for phishing risks. This is a simple prototype.",
            "url_input": "Enter URL",
            "url_placeholder": "e.g., https://login.bankofamerica.com.xyz",
            "check_button": "Check URL",
            "url_warning": "Please enter a URL to check.",
            "keyword_detected": "🚩 Suspicious Keyword Detected in URL: This URL contains a sensitive keyword like 'login' or 'bank'.",
            "tld_detected": "🚩 Suspicious Top-Level Domain Detected:",
            "heuristics_warning": "⚠ This URL is flagged by our basic heuristics. Please proceed with caution.",
            "url_safe": "✅ The URL appears to be safe to visit!",
            "url_suspicious": "🚨 This URL is highly suspicious – possible phishing detected!",
            "sender_not_found": "Not Found",
            "sender_placeholder": "Not Found",
            "welcome_title": "Welcome to Phishing & URL Checker", 
            "select_lang": "Please select your preferred language to continue:", 
            "confirm_lang": "Continue to App", 
            "nav_title": "Navigation", 
            "theme_title": "Theme", # New translation key
            "light_mode": "Light Mode 💡", # New translation key
            "dark_mode": "Dark Mode 🌙", # New translation key
        },
        "hi": {  # Hindi
            "page_title": "फ़िशिंग और यूआरएल चेकर",
            "email_checker": "ईमेल चेकर",
            "url_checker": "यूआरएल चेकर",
            "email_title": "एआई जीमेल फ़िशिंग डिटेक्टर",
            "email_desc": "संदिग्ध ईमेल की सामग्री नीचे पेस्ट करें ताकि फ़िशिंग संकेतकों का विश्लेषण किया जा सके। बेहतर सटीकता के लिए 'From:' फ़ील्ड शामिल करें।",
            "email_input": "ईमेल सामग्री",
            "email_placeholder": "ईमेल की पूरी सामग्री पेस्ट करें, प्रेषक का विवरण शामिल करें (उदा: From: example@gmail.com)...",
            "analyze_button": "फ़िशिंग के लिए विश्लेषण करें",
            "no_content_warning": "कृपया विश्लेषण के लिए कुछ ईमेल सामग्री पेस्ट करें।",
            "analysis_results": "विश्लेषण परिणाम",
            "phishing_score": "फ़िशिंग स्कोर",
            "detected_sender": "पता लगाया गया प्रेषक",
            "indicators": "पता लगाए गए फ़िशिंग संकेतक:",
            "no_indicators": "कोई स्पष्ट फ़िशिंग संकेतक नहीं मिले। यह ईमेल सुरक्षित प्रतीत होता है।",
            "safe_sender": "प्रेषक एक वैध पता प्रतीत होता है।",
            "footer": "स्ट्रीमलिट के साथ निर्मित प्रोटोटाइप। केवल शैक्षिक/डेमो उद्देश्यों के लिए।",
            "url_title": "यूआरएल फ़िशिंग चेकर",
            "url_desc": "फ़िशिंग जोखिम की जाँच के लिए नीचे एक यूआरएल पेस्ट करें। यह एक साधारण प्रोटोटाइप है।",
            "url_input": "यूआरएल दर्ज करें",
            "url_placeholder": "उदा: https://login.bankofamerica.com.xyz",
            "check_button": "यूआरएल जांचें",
            "url_warning": "कृपया जांचने के लिए एक यूआरएल दर्ज करें।",
            "keyword_detected": "🚩 संदिग्ध कीवर्ड पाया गया: इस यूआरएल में 'login' या 'bank' जैसे संवेदनशील शब्द हैं।",
            "tld_detected": "🚩 संदिग्ध शीर्ष-स्तरीय डोमेन पाया गया:",
            "heuristics_warning": "⚠ इस यूआरएल को हमारे सरल नियमों द्वारा चिह्नित किया गया है। सावधानी से आगे बढ़ें।",
            "url_safe": "✅ यह यूआरएल सुरक्षित प्रतीत होता है!",
            "url_suspicious": "🚨 यह यूआरएल संदिग्ध है - संभवतः फ़िशिंग!",
            "sender_not_found": "नहीं मिला",
            "sender_placeholder": "नहीं मिला",
            "welcome_title": "फ़िशिंग और यूआरएल चेकर में आपका स्वागत है", 
            "select_lang": "जारी रखने के लिए कृपया अपनी पसंदीदा भाषा चुनें:", 
            "confirm_lang": "ऐप पर जारी रखें", 
            "nav_title": "नेविगेशन",
            "theme_title": "थीम", # New translation key
            "light_mode": "लाइट मोड 💡", # New translation key
            "dark_mode": "डार्क मोड 🌙", # New translation key
        },

        "te": {
            "page_title": "ఫిషింగ్ & URL చెకర్",
            "email_checker": "ఇమెయిల్ చెకర్",
            "url_checker": "URL చెకర్",
            "email_title": "AI Gmail ఫిషింగ్ డిటెక్టర్",
            "email_desc": "ఫిషింగ్ సూచికలను విశ్లేషించడానికి అనుమానాస్పద ఇమెయిల్ కంటెంట్‌ను క్రింద పేస్ట్ చేయండి. మరింత ఖచ్చితత్వం కోసం 'From:' ఫీల్డ్‌ను చేర్చండి.",
            "email_input": "ఇమెయిల్ కంటెంట్",
            "email_placeholder": "ఇమెయిల్ యొక్క పూర్తి కంటెంట్‌ను పేస్ట్ చేయండి, పంపినవారి వివరాలను చేర్చండి (ఉదా: From: example@gmail.com)...",
            "analyze_button": "ఫిషింగ్ కోసం విశ్లేషించండి",
            "no_content_warning": "విశ్లేషించడానికి కొంత ఇమెయిల్ కంటెంట్‌ను పేస్ట్ చేయండి.",
            "analysis_results": "విశ్లేషణ ఫలితాలు",
            "phishing_score": "ఫిషింగ్ స్కోర్",
            "detected_sender": "గుర్తించిన పంపినవాడు",
            "indicators": "గుర్తించిన ఫిషింగ్ సూచికలు:",
            "no_indicators": "ఏ ఫిషింగ్ సూచికలు కనుగొనబడలేదు. ఈ ఇమెయిల్ సురక్షితంగా ఉంది.",
            "safe_sender": "పంపినవారు సరైన చిరునామా నుండి ఉన్నట్లు కనిపిస్తుంది, అనుమానాస్పద ధృవీకరణ అభ్యర్థనలు లేవు.",
            "footer": "స్ట్రీంలిట్‌తో నిర్మించిన ప్రోటోటైప్. ఇది విద్యా/డెమో ప్రయోజనాల కోసం మాత్రమే. అనుమానాస్పద ఇమెయిల్స్‌ను ఎల్లప్పుడూ చేతితో ధృవీకరించండి.",
            "url_title": "URL ఫిషింగ్ చెకర్",
            "url_desc": "ఫిషింగ్ ప్రమాదాలను తనిఖీ చేయడానికి క్రింద URL పేస్ట్ చేయండి. ఇది ఒక సరళమైన ప్రోటోటైప్.",
            "url_input": "URL నమోదు చేయండి",
            "url_placeholder": "ఉదా: https://login.bankofamerica.com.xyz",
            "check_button": "URL తనిఖీ చేయండి",
            "url_warning": "దయచేసి తనిఖీ చేయడానికి ఒక URL నమోదు చేయండి.",
            "keyword_detected": "🚩 అనుమానాస్పద కీవర్డ్ గుర్తించబడింది: ఈ URLలో 'login' లేదా 'bank' వంటి సున్నితమైన పదం ఉంది.",
            "tld_detected": "🚩 అనుమానాస్పద టాప్-లెవల్ డొమైన్ గుర్తించబడింది:",
            "heuristics_warning": "⚠ ఈ URL మా ప్రాథమిక హ్యూరిస్టిక్స్ ద్వారా ఫ్లాగ్ చేయబడింది. జాగ్రత్తగా కొనసాగండి.",
            "url_safe": "✅ ఈ URL సురక్షితంగా ఉంది!",
            "url_suspicious": "🚨 ఈ URL అనుమానాస్పదంగా ఉంది – ఫిషింగ్ కావచ్చు!",
            "sender_not_found": "కనుగొనబడలేదు",
            "sender_placeholder": "కనుగొనబడలేదు",
            "welcome_title": "ఫిషింగ్ & URL చెకర్‌కి స్వాగతం",
            "select_lang": "దయచేసి కొనసాగడానికి మీకు ఇష్టమైన భాషను ఎంచుకోండి:",
            "confirm_lang": "యాప్ కొనసాగించండి",
            "nav_title": "నావిగేషన్",
            "theme_title": "థీమ్", # New translation key
            "light_mode": "లైట్ మోడ్ 💡", # New translation key
            "dark_mode": "డార్క్ మోడ్ 🌙", # New translation key
        }, 
        "bn": {
            "page_title": "ফিশিং ও ইউআরএল চেকার",
            "email_checker": "ইমেইল চেকার",
            "url_checker": "ইউআরএল চেকার",
            "email_title": "এআই জিমেইল ফিশিং ডিটেক্টর",
            "email_desc": "ফিশিং সূচক বিশ্লেষণ করার জন্য নিচে সন্দেহজনক ইমেইলের বিষয়বস্তু পেস্ট করুন। আরও সঠিকতার জন্য 'From:' ফিল্ডটি অন্তর্ভুক্ত করুন।",
            "email_input": "ইমেইল বিষয়বস্তু",
            "email_placeholder": "ইমেইলের সম্পূর্ণ বিষয়বস্তু পেস্ট করুন, প্রেরকের বিবরণ অন্তর্ভুক্ত করুন (যেমন: From: example@gmail.com)...",
            "analyze_button": "ফিশিং বিশ্লেষণ করুন",
            "no_content_warning": "দয়া করে বিশ্লেষণের জন্য কিছু ইমেইল বিষয়বস্তু পেস্ট করুন।",
            "analysis_results": "বিশ্লেষণের ফলাফল",
            "phishing_score": "ফিশিং স্কোর",
            "detected_sender": "সনাক্তকৃত প্রেরক",
            "indicators": "সনাক্তকৃত ফিশিং সূচক:",
            "no_indicators": "কোনও স্পষ্ট ফিশিং সূচক পাওয়া যায়নি। এই ইমেইলটি নিরাপদ বলে মনে হচ্ছে।",
            "safe_sender": "প্রেরক একটি বৈধ ঠিকানা থেকে এসেছে বলে মনে হচ্ছে, কোনও সন্দেহজনক যাচাইকরণের অনুরোধ নেই।",
            "footer": "স্ট্রিমলিট দিয়ে তৈরি প্রোটোটাইপ। শুধুমাত্র শিক্ষা/ডেমো উদ্দেশ্যে। সর্বদা সন্দেহজনক ইমেইল ম্যানুয়ালি যাচাই করুন।",
            "url_title": "ইউআরএল ফিশিং চেকার",
            "url_desc": "ফিশিং ঝুঁকি পরীক্ষা করার জন্য নিচে একটি ইউআরএল পেস্ট করুন। এটি একটি সাধারণ প্রোটোটাইপ।",
            "url_input": "ইউআরএল লিখুন",
            "url_placeholder": "যেমন: https://login.bankofamerica.com.xyz",
            "check_button": "ইউআরএল পরীক্ষা করুন",
            "url_warning": "দয়া করে পরীক্ষা করার জন্য একটি ইউআরএল লিখুন।",
            "keyword_detected": "🚩 সন্দেহজনক কীওয়ার্ড সনাক্ত করা হয়েছে: এই ইউআরএলে 'login' বা 'bank' এর মতো সংবেদনশীল শব্দ রয়েছে।",
            "tld_detected": "🚩 সন্দেহজনক টপ-লেভেল ডোমেইন সনাক্ত করা হয়েছে:",
            "heuristics_warning": "⚠ এই ইউআরএল আমাদের মৌলিক হিউরিস্টিক্স দ্বারা ফ্ল্যাগ করা হয়েছে। সতর্কতার সাথে এগিয়ে যান।",
            "url_safe": "✅ ইউআরএলটি নিরাপদ বলে মনে হচ্ছে!",
            "url_suspicious": "🚨 এই ইউআরএলটি খুব সন্দেহজনক – সম্ভবত ফিশিং!",
            "sender_not_found": "পাওয়া যায়নি",
            "sender_placeholder": "পাওয়া যায়নি",
            "welcome_title": "ফিশিং ও ইউআরএল চেকারে স্বাগতম",
            "select_lang": "চালিয়ে যেতে আপনার পছন্দের ভাষা নির্বাচন করুন:",
            "confirm_lang": "অ্যাপে চালিয়ে যান",
            "nav_title": "ন্যাভিগেশন",
            "theme_title": "থিম", # New translation key
            "light_mode": "লাইট মোড 💡", # New translation key
            "dark_mode": "ডার্ক মোড 🌙", # New translation key
        }, 
        "ur": {
            "page_title": "فشنگ اور یو آر ایل چیکر",
            "email_checker": "ای میل چیکر",
            "url_checker": "یو آر ایل چیکر",
            "email_title": "اے آئی جی میل فشنگ ڈیٹیکٹر",
            "email_desc": "فشنگ کے اشارے تجزیہ کرنے کے لیے نیچے مشتبہ ای میل کا مواد پیسٹ کریں۔ بہتر درستگی کے لیے 'From:' فیلڈ شامل کریں۔",
            "email_input": "ای میل مواد",
            "email_placeholder": "ای میل کا مکمل مواد پیسٹ کریں، بھیجنے والے کی تفصیلات شامل کریں (مثال: From: example@gmail.com)...",
            "analyze_button": "فشنگ کے لیے تجزیہ کریں",
            "no_content_warning": "تجزیہ کرنے کے لیے کچھ ای میل مواد پیسٹ کریں۔",
            "analysis_results": "تجزیاتی نتائج",
            "phishing_score": "فشنگ سکور",
            "detected_sender": "پہچاننے والا بھیجنے والا",
            "indicators": "پہچانے گئے فشنگ اشارے:",
            "no_indicators": "کوئی واضح فشنگ اشارے نہیں ملے۔ یہ ای میل محفوظ لگتی ہے۔",
            "safe_sender": "بھیجنے والا ایک جائز پتہ لگتا ہے، کوئی مشتبہ تصدیقی درخواست نہیں۔",
            "footer": "اسٹریملٹ کے ساتھ بنایا گیا پروٹوٹائپ۔ صرف تعلیمی/ڈیمو مقاصد کے لیے۔ مشتبہ ای میلز ہمیشہ دستی طور پر تصدیق کریں۔",
            "url_title": "یو آر ایل فشنگ چیکر",
            "url_desc": "فشنگ کے خطرات چیک کرنے کے لیے نیچے ایک یو آر ایل پیسٹ کریں۔ یہ ایک سادہ پروٹوٹائپ ہے۔",
            "url_input": "یو آر ایل درج کریں",
            "url_placeholder": "مثال: https://login.bankofamerica.com.xyz",
            "check_button": "یو آر ایل چیک کریں",
            "url_warning": "براہ کرم چیک کرنے کے لیے ایک یو آر ایل درج کریں۔",
            "keyword_detected": "🚩 مشتبہ کلیدی لفظ پایا گیا: اس یو آر ایل میں 'login' یا 'bank' جیسے حساس الفاظ ہیں۔",
            "tld_detected": "🚩 مشتبہ ٹاپ-لیول ڈومین پایا گیا:",
            "heuristics_warning": "⚠ یہ یو آر ایل ہماری بنیادی ہورسٹکس کے تحت فلیگ کیا گیا ہے۔ احتیاط سے آگے بڑھیں۔",
            "url_safe": "✅ یہ یو آر ایل محفوظ لگتا ہے!",
            "url_suspicious": "🚨 یہ یو آر ایل انتہائی مشتبہ ہے – ممکنہ فشنگ!",
            "sender_not_found": "نہیں ملا",
            "sender_placeholder": "نہیں ملا",
            "welcome_title": "فشنگ اور یو آر ایل چیکر میں خوش آمدید",
            "select_lang": "جاری رکھنے کے لیے اپنی پسندیدہ زبان منتخب کریں:",
            "confirm_lang": "ایپ پر جاری رکھیں",
            "nav_title": "نیویگیشن",
            "theme_title": "تھیم", # New translation key
            "light_mode": "لائٹ موڈ 💡", # New translation key
            "dark_mode": "ڈارک موڈ 🌙", # New translation key
        }, 
    }

    lang_map = {
        "English (अंग्रेज़ी)": "en", 
        "Hindi (हिन्दी)": "hi", 
        "Telugu (తెలుగు)": "te", 
        "Bengali (বাংলা)": "bn", 
        "Urdu (اردو)": "ur"

    }

    # Initialize state if not present
    if 'lang_code' not in st.session_state:
        st.session_state.lang_code = None 
    if 'theme' not in st.session_state: # Initialize theme
        st.session_state.theme = 'dark' # Default theme
        
    # Get translation dictionary (t)
    lang_code = st.session_state.lang_code if st.session_state.lang_code else 'en'
    t = translations.get(lang_code, translations["en"])
    
    return t, lang_map, translations

# --- Analysis Logic (Simplified) ---
def analyze_email(content, t_dict):
    sender_email = t_dict["sender_placeholder"]
    from_match = re.search(r'From:\s*<?([^>]+@[^>\s]+)>?', content, re.IGNORECASE)
    if from_match:
        sender_email = from_match.group(1).strip().lower()

    phishing_indicators = []
    score = 0
    if sender_email != t_dict["sender_placeholder"] and not sender_email.endswith('@gmail.com'):
        phishing_indicators.append({'type': 'Suspicious Sender', 'message': 'Non-Gmail sender.', 'severity': 'high'})
        score += 40
    if re.search(r'(urgent|act now)', content, re.IGNORECASE):
        phishing_indicators.append({'type': 'Urgency/Threat', 'message': 'Uses urgent language.', 'severity': 'medium'})
        score += 20
        
    final_score = min(100, score + random.randint(0, 5))
    return sender_email, phishing_indicators, final_score

# --- App UI Functions ---

def email_checker(t):
    st.title(f"{t['email_title']}")
    st.markdown(t["email_desc"])
    
    email_content = st.text_area(t["email_input"], placeholder=t["email_placeholder"], height=200)

    if st.button(t["analyze_button"], type="primary"):
        if not email_content.strip():
            st.warning(t["no_content_warning"])
            return

        sender_email, indicators, score = analyze_email(email_content, t)

        st.subheader(t["analysis_results"])
        col1, col3 = st.columns([1, 1])
        with col1:
            st.metric(t["phishing_score"], f"{score}/100")
        with col3:
            st.metric(t["detected_sender"], sender_email)

        st.markdown("---")
        
        if not indicators:
            st.success(t["no_indicators"])
            
    st.markdown("---")
    st.markdown(t["footer"])
    
def url_checker(t):
    st.title(f" {t['url_title']}")
    st.markdown(t["url_desc"])
    
    url_input = st.text_input(t["url_input"], placeholder=t["url_placeholder"])
    if st.button(t["check_button"], type="primary"):
        if not url_input.strip():
            st.warning(t["url_warning"])
            return

        is_phishy = False
        url_lower = url_input.lower()
        suspicious_keywords = ['login', 'bank', 'paypal']

        if any(keyword in url_lower for keyword in suspicious_keywords):
            is_phishy = True
            st.error(t["keyword_detected"])
            
        if not is_phishy:
            st.success(t["url_safe"])
        else:
            st.error(t["url_suspicious"])
    
    st.markdown("---")
    st.markdown(t["footer"])

# --- Theme CSS Injection ---
def set_custom_theme():
    """Injects custom CSS based on the theme selected in session_state."""
    if st.session_state.theme == 'light':
        # Custom Light Theme (Overrides Streamlit's default dark mode if it was selected)
        # Using a simple light theme by setting the main background and text colors
        css = """
        <style>
            .stApp {
                background-color: white; 
                color: black;
            }
            /* Adjust sidebar for light mode if needed */
            .stSidebar {
                background-color: #f0f2f6; 
            }
            /* Adjust headers for better contrast */
            h1, h2, h3, h4 {
                color: #262730;
            }
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    elif st.session_state.theme == 'dark':
        # Custom Dark Theme (Uses Streamlit's default dark mode colors as a base, 
        # but you can override specific elements if needed)
        # In the absence of a direct Streamlit theme toggle, 
        # using a general dark mode style is the only way to ensure consistency.
        css = """
        <style>
            .stApp {
                background-color: #0E1117;
                color: white;
            }
            .stSidebar {
                background-color: #1A1D23;
            }
            h1, h2, h3, h4 {
                color: #FAFAFA;
            }
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
        
def toggle_theme():
    """Switches the theme between light and dark."""
    if st.session_state.theme == 'dark':
        st.session_state.theme = 'light'
    else:
        st.session_state.theme = 'dark'


# --- Main Application Flow ---

t, lang_map, translations_all = get_translation_data()

# Inject the custom theme CSS BEFORE any other Streamlit component
set_custom_theme()

# Page configuration
st.set_page_config(
    page_title=t["page_title"],
    page_icon="🔍",
    layout="wide"
)

# 1. LANDING PAGE: FORCE LANGUAGE SELECTION
if st.session_state.lang_code is None:
    # Center the content using columns
    col_l, col_c, col_r = st.columns([1, 2, 1])

    with col_c:
        # Use the initial English translation for the welcome screen to ensure consistency
        st.title(translations_all["en"]["welcome_title"])
        st.markdown("---")
        
        st.subheader(" Please select your language / कृपया अपनी भाषा चुनें:")
        
        # Selectbox for the initial choice
        selected_lang_name = st.selectbox(
            "Select Language", 
            list(lang_map.keys()),
            key='initial_language_select',
            label_visibility="collapsed"
        )
        
        # Callback to set the state and rerun the script
        def set_language():
            st.session_state.lang_code = lang_map[st.session_state.initial_language_select]
            
        # Get the confirmation text based on the selected language's code for a translated button
        confirm_code = lang_map.get(st.session_state.get('initial_language_select'), 'en')
        confirm_text = translations_all.get(confirm_code, translations_all['en'])['confirm_lang']
        
        st.markdown("\n\n") 
        if st.button(confirm_text, on_click=set_language, type="primary"):
            pass

else:
    # 2. MAIN APP: LANGUAGE AND THEME IS SET
    
    # --- Sidebar Theme Switcher ---
    st.sidebar.title(t["nav_title"])

    # Theme Switcher Logic
    st.sidebar.subheader(t["theme_title"])
    
    # The current label for the button will be the opposite of the current theme
    if st.session_state.theme == 'dark':
        button_label = t["light_mode"]
    else:
        button_label = t["dark_mode"]
        
    st.sidebar.button(
        button_label, 
        on_click=toggle_theme, 
        key='theme_toggle_button'
    )
    
    st.sidebar.markdown("---")

    # --- Sidebar Navigation (Permanent Language Switcher) ---
    
    # Function to update language from the sidebar
    def update_language_from_sidebar():
        st.session_state.lang_code = lang_map[st.session_state.sidebar_language_select]

    # Find current language index for the selectbox default value
    current_lang_name = next(name for name, code in lang_map.items() if code == st.session_state.lang_code)
    current_lang_index = list(lang_map.keys()).index(current_lang_name)
    
    # Language Switcher
    st.sidebar.selectbox(
        " Language / ভাষা",
        list(lang_map.keys()),
        index=current_lang_index,
        key='sidebar_language_select',
        on_change=update_language_from_sidebar
    )
    
    st.sidebar.markdown("---")
    
    # Navigation Radio Buttons
    page = st.sidebar.radio("Go to", [t["email_checker"], t["url_checker"]])

    # --- Content Area ---
    if page == t["email_checker"]:
        email_checker(t)
    else:
        url_checker(t)
