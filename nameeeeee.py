import streamlit as st
import re
import random

# Page configuration
st.set_page_config(
    page_title="Phishing & URL Checker",
    page_icon="🔍",
    layout="wide"
)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Email Checker", "URL Checker"])

# --- Email Checker Logic ---
def email_checker():
    st.title("AI Gmail Phishing Detector")
    st.markdown(
        "Paste the content of a suspicious email below to analyze it for phishing indicators, "
        "including sender verification and phone number requests. Include the 'From:' field if possible for better accuracy."
    )

    # Input section
    email_content = st.text_area(
        "Email Content",
        placeholder="Paste the full content of the email, including sender details (e.g., From: example@gmail.com)...",
        height=200,
        help="Include headers like 'From:' for sender analysis."
    )

    # Analyze button
    if st.button("Analyze for Phishing", type="primary"):
        if not email_content.strip():
            st.warning("Please paste some email content to analyze.")
        else:
            # Try to extract sender email from 'From:' header first
            sender_email = None
            from_match = re.search(r'From:\s*<?([^>]+@[^>\s]+)>?', email_content, re.IGNORECASE)
            if from_match:
                sender_email = from_match.group(1).strip().lower()
            else:
                # Fallback: Search for a standalone email address anywhere in the text
                email_match = re.search(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', email_content, re.IGNORECASE)
                if email_match:
                    sender_email = email_match.group(0).strip().lower()

            # Initialize phishing indicators
            phishing_indicators = []

            # Check sender domain - warn if not @gmail.com or suspicious variation
            if sender_email:
                is_gmail = sender_email.endswith('@gmail.com')
                suspicious_variations = ['@gmai1.com', '@gmial.com', '@goog1e.com', '@gmail.co', '@gmaill.com', '@gmailllllll.com']
                is_suspicious_variation = any(variation in sender_email for variation in suspicious_variations)
                
                if not is_gmail or is_suspicious_variation:
                    phishing_indicators.append({
                        'type': 'suspicious_sender',
                        'message': f'Sender email "{sender_email}" does not appear to be a legitimate Gmail address. Legitimate Gmail emails should come from @gmail.com domains.',
                        'severity': 'high',
                        'icon': '📧'
                    })
                else:
                    # Simulate basic verification check (mock; real would use Gmail API)
                    mentions_verification = re.search(r'phone|sms|verification code|2fa|two-factor|number verification', email_content, re.IGNORECASE)
                    if mentions_verification:
                        phishing_indicators.append({
                            'type': 'verification_request',
                            'message': 'Email mentions phone/SMS verification, which legitimate Gmail security notifications rarely request via email. This could be a phishing attempt to steal your verification codes.',
                            'severity': 'high',
                            'icon': '📱'
                        })
            else:
                phishing_indicators.append({
                    'type': 'no_sender_detected',
                    'message': 'Could not detect sender email address in the provided content. Please include the "From" field for better analysis.',
                    'severity': 'medium',
                    'icon': '📧'
                })

            # Existing checks (urgency, suspicious links, personal info, grammar)
            if re.search(r'(urgent|immediate|act now|limited time|account suspended)', email_content, re.IGNORECASE):
                phishing_indicators.append({
                    'type': 'urgency',
                    'message': 'Uses urgent language to pressure quick action',
                    'severity': 'medium'
                })

            if re.search(r'(http|https):\/\/(?!.google\.com|.*gmail\.com).', email_content, re.IGNORECASE):
                phishing_indicators.append({
                    'type': 'suspicious_link',
                    'message': 'Contains links to non-Google domains',
                    'severity': 'high'
                })

            if re.search(r'(password|credit card|social security|bank account)', email_content, re.IGNORECASE):
                phishing_indicators.append({
                    'type': 'personal_info_request',
                    'message': 'Requests sensitive personal information',
                    'severity': 'high'
                })

            # Enhanced check for number/phone verification requests
            if re.search(r'phone number|sms code|verification code|confirm your number|2-step verification', email_content, re.IGNORECASE):
                phishing_indicators.append({
                    'type': 'phone_verification_phish',
                    'message': 'Requests phone number or verification codes, a common phishing tactic to bypass Gmail\'s security.',
                    'severity': 'high',
                    'icon': '📱'
                })

            # Check for poor grammar/spelling (simple pattern match)
            grammar_errors = re.findall(r'\b(?:your|you\'re)\b.\b(?:account|password)\b.\b(?:is|are)\b.*\b(?:compromised|expired|suspended)\b', email_content, re.IGNORECASE)
            if len(grammar_errors) > 2:
                phishing_indicators.append({
                    'type': 'poor_grammar',
                    'message': 'Contains grammatical errors common in phishing emails',
                    'severity': 'low'
                })

            # Calculate overall phishing score (0-100)
            score = min(100, sum(
                40 if ind['severity'] == 'high' else
                20 if ind['severity'] == 'medium' else
                10 for ind in phishing_indicators
            ))

            # Determine status
            if score >= 70:
                status = "Highly Suspicious"
                status_color = "🔴"
            elif score >= 30:
                status = "Moderately Suspicious"
                status_color = "🟠"
            else:
                status = "Likely Safe"
                status_color = "🟢"

            # Display results
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader("Analysis Results")
            with col2:
                st.markdown(f"{status_color} {status}")

            st.markdown(f"Phishing Score: {score}/100")
            if sender_email:
                st.markdown(f"Detected Sender: {sender_email}")

            # Display indicators
            if phishing_indicators:
                st.subheader("Detected Phishing Indicators:")
                for ind in phishing_indicators:
                    severity_color = {
                        'high': 'error',
                        'medium': 'warning',
                        'low': 'info'
                    }.get(ind['severity'], 'info')
                    icon = ind.get('icon', '⚠')
                    st.markdown(f"{icon} {ind['type'].replace('_', ' ').title()}** ({ind['severity'].title()} Severity)")
                    st.markdown(f"{ind['message']}")
                    st.markdown("---")
            else:
                st.success("No obvious phishing indicators detected. This email appears safe.")
                if sender_email and sender_email.endswith('@gmail.com'):
                    st.info("Sender appears to be a legitimate Gmail address with no suspicious verification requests detected.")
    
    st.markdown("---")
    st.markdown("Prototype built with Streamlit. For educational/demo purposes only. Always verify suspicious emails manually.")
    
# --- URL Checker Logic ---
def url_checker():
    st.title("URL Phishing Checker")
    st.markdown("Paste a URL below to check for phishing risks. This is a simple prototype.")
    
    # URL input and check button
    url_input = st.text_input("Enter URL", placeholder="e.g., https://login.bankofamerica.com.xyz")
    if st.button("Check URL", type="primary"):
        if not url_input.strip():
            st.warning("Please enter a URL to check.")
            return

        # Simple phishing detection logic
        suspicious_keywords = ['login', 'bank', 'paypal', 'update', 'verify']
        suspicious_domains = ['.xyz', '.top', '.club', '.tk']
        
        is_phishy = False
        url_lower = url_input.lower()
        
        # Check for suspicious keywords
        if any(keyword in url_lower for keyword in suspicious_keywords):
            is_phishy = True
            st.error("🚩 Suspicious Keyword Detected in URL: This URL contains a sensitive keyword like 'login' or 'bank'.")
            
        # Check for suspicious domains
        if any(domain in url_lower for domain in suspicious_domains):
            is_phishy = True
            st.error(f"🚩 Suspicious Top-Level Domain Detected: The domain '{url_lower.split('/')[-1]}' is on our watchlist.")
            
        # Random element for prototype variability
        if not is_phishy and random.random() < 0.3:
            is_phishy = True
            st.warning("⚠ This URL is flagged by our basic heuristics. Please proceed with caution.")

        if not is_phishy:
            st.success("✅ The URL appears to be safe to visit!")
        else:
            st.error("🚨 This URL is highly suspicious – possible phishing detected!")
    
    st.markdown("---")
    st.markdown("Prototype built with Streamlit. For educational/demo purposes only.")


# Display the selected page
if page == "Email Checker":
    email_checker()
else:
    url_checker()