"""
WhatsApp AI Chatbot Demo - Dental Clinic Edition
A Flask-based demo showing how an AI chatbot handles dental clinic inquiries.
Deploy this as a web demo to show prospects.
"""

from flask import Flask, render_template_string, request, jsonify
import json
from datetime import datetime, timedelta
import re

app = Flask(__name__)

# Demo clinic configuration
CLINIC_CONFIG = {
    "name": "Demo Dental Clinic",
    "hours": "Mon-Fri: 9:00 AM - 6:00 PM, Sat: 9:00 AM - 1:00 PM, Sun: Closed",
    "address": "123 Jalan Example, Petaling Jaya, Selangor",
    "phone": "03-1234 5678",
    "whatsapp": "012-345 6789",
    "services": {
        "Scaling & Polishing": "RM 80 - 150",
        "Tooth Extraction": "RM 80 - 300",
        "Dental Filling": "RM 80 - 250",
        "Root Canal Treatment": "RM 500 - 1500",
        "Teeth Whitening": "RM 800 - 1500",
        "Dental Crown": "RM 800 - 2000",
        "Braces (Metal)": "RM 3500 - 6000",
        "Invisalign": "RM 8000 - 15000",
        "Dental Implant": "RM 5000 - 8000",
    },
    "dentists": [
        "Dr. Sarah Tan (General Dentistry)",
        "Dr. Ahmad Razak (Orthodontics)",
        "Dr. Mei Ling (Cosmetic Dentistry)",
    ],
    "faq": {
        "parking": "Free parking available at basement level. Take ticket at entrance.",
        "insurance": "We accept all major insurance panels including AIA, Prudential, Great Eastern, and Allianz.",
        "emergency": "For dental emergencies, please call our hotline at 012-345 6789. We prioritize emergency cases.",
        "payment": "We accept cash, credit/debit cards, e-wallets (Touch 'n Go, GrabPay), and online banking.",
    }
}

# Available appointment slots (demo)
def get_available_slots():
    slots = []
    today = datetime.now()
    for day_offset in range(1, 8):
        date = today + timedelta(days=day_offset)
        if date.weekday() < 5:  # Mon-Fri
            for hour in [9, 10, 11, 14, 15, 16, 17]:
                slots.append(f"{date.strftime('%A, %d %B')} at {hour}:00")
        elif date.weekday() == 5:  # Saturday
            for hour in [9, 10, 11, 12]:
                slots.append(f"{date.strftime('%A, %d %B')} at {hour}:00")
    return slots[:10]  # Show next 10 available


def generate_bot_response(user_message):
    msg = user_message.lower().strip()
    
    # Greeting
    if any(w in msg for w in ['hi', 'hello', 'hey', 'halo', 'hai']):
        return f"""👋 Hello! Welcome to {CLINIC_CONFIG['name']}.

I'm your AI dental assistant. How can I help you today?

1️⃣ Book an appointment
2️⃣ View our services & pricing
3️⃣ Check clinic hours & location
4️⃣ Talk to our team

Just type a number or ask me anything! 😊"""

    # Appointment booking
    if any(w in msg for w in ['book', 'appointment', 'schedule', 'slot', 'available', '1']):
        slots = get_available_slots()
        slot_text = "\n".join([f"  • {s}" for s in slots[:6]])
        return f"""📅 Great! Let's book your appointment.

Here are our next available slots:
{slot_text}

Which slot works best for you? Just tell me your preferred date and time, and I'll reserve it.

I'll also need:
• Your full name
• Contact number
• Type of treatment needed"""

    # Services & pricing
    if any(w in msg for w in ['service', 'price', 'pricing', 'cost', 'how much', 'treatment', '2', 'berapa']):
        services_text = "\n".join([f"  • {k}: {v}" for k, v in CLINIC_CONFIG['services'].items()])
        return f"""💰 Here are our services and pricing:

{services_text}

*Prices may vary based on complexity. A consultation is recommended for an accurate quote.*

Would you like to book a consultation? 😊"""

    # Hours & location
    if any(w in msg for w in ['hour', 'open', 'close', 'time', 'location', 'address', 'where', '3', 'waktu', 'buka']):
        return f"""🏥 {CLINIC_CONFIG['name']}

📍 Address: {CLINIC_CONFIG['address']}
🕐 Hours: {CLINIC_CONFIG['hours']}
📞 Phone: {CLINIC_CONFIG['phone']}
💬 WhatsApp: {CLINIC_CONFIG['whatsapp']}

📍 Google Maps: [Click here for directions]

Would you like to book an appointment? 😊"""

    # Dentist info
    if any(w in msg for w in ['doctor', 'dentist', 'dr', 'doktor']):
        dentist_text = "\n".join([f"  • {d}" for d in CLINIC_CONFIG['dentists']])
        return f"""👨‍⚕️ Our Dental Team:

{dentist_text}

All our dentists are registered with the Malaysian Dental Council.

Would you like to book with a specific dentist? 😊"""

    # Insurance
    if any(w in msg for w in ['insurance', 'panel', 'claim', 'insurans']):
        return f"""🏦 Insurance & Payment:

{CLINIC_CONFIG['faq']['insurance']}

{CLINIC_CONFIG['faq']['payment']}

Need help with an insurance claim? Our front desk team can assist you."""

    # Parking
    if any(w in msg for w in ['parking', 'park', 'car']):
        return f"🚗 {CLINIC_CONFIG['faq']['parking']}"

    # Emergency
    if any(w in msg for w in ['emergency', 'urgent', 'pain', 'sakit', 'kecemasan']):
        return f"""🚨 {CLINIC_CONFIG['faq']['emergency']}

Common dental emergencies we handle:
• Severe toothache
• Broken/chipped tooth
• Knocked-out tooth
• Swelling or abscess
• Bleeding gums

Please call us immediately and we'll prioritize your case."""

    # Thank you
    if any(w in msg for w in ['thank', 'thanks', 'terima kasih', 'tq']):
        return """😊 You're welcome! 

Is there anything else I can help you with? Feel free to ask anytime.

Have a great day! 🦷✨"""

    # Human handoff
    if any(w in msg for w in ['human', 'staff', 'person', 'real', 'speak', '4']):
        return f"""👤 Sure! Let me connect you with our team.

You can reach us directly:
📞 Call: {CLINIC_CONFIG['phone']}
💬 WhatsApp: {CLINIC_CONFIG['whatsapp']}

Our staff will respond within 5 minutes during business hours.

Is there anything else I can help with in the meantime?"""

    # Default / catch-all
    return f"""I understand you're asking about "{user_message}". Let me help!

Here's what I can assist you with:

1️⃣ Book an appointment
2️⃣ View services & pricing
3️⃣ Check hours & location
4️⃣ Talk to our team

Just type a number or ask your question in any way — I'll do my best to help! 😊"""


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp AI Chatbot Demo — Phyto Link Venture</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0b141a; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { width: 100%; max-width: 420px; height: 90vh; max-height: 700px; display: flex; flex-direction: column; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.3); }
        .header { background: #1f2c33; padding: 12px 16px; display: flex; align-items: center; gap: 12px; }
        .header .avatar { width: 40px; height: 40px; border-radius: 50%; background: #00a884; display: flex; align-items: center; justify-content: center; font-size: 20px; }
        .header .info h3 { color: #e9edef; font-size: 16px; }
        .header .info p { color: #8696a0; font-size: 12px; }
        .chat { flex: 1; overflow-y: auto; padding: 16px; background: #0b141a url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90" opacity="0.02">🦷</text></svg>') repeat; }
        .message { max-width: 85%; margin-bottom: 8px; padding: 8px 12px; border-radius: 8px; font-size: 14px; line-height: 1.5; white-space: pre-wrap; word-wrap: break-word; }
        .bot { background: #1f2c33; color: #e9edef; border-top-left-radius: 0; margin-right: auto; }
        .user { background: #005c4b; color: #e9edef; border-top-right-radius: 0; margin-left: auto; }
        .time { font-size: 11px; color: #8696a0; text-align: right; margin-top: 4px; }
        .input-area { background: #1f2c33; padding: 10px 16px; display: flex; gap: 8px; }
        .input-area input { flex: 1; background: #2a3942; border: none; border-radius: 8px; padding: 10px 16px; color: #e9edef; font-size: 14px; outline: none; }
        .input-area button { background: #00a884; border: none; border-radius: 50%; width: 40px; height: 40px; cursor: pointer; font-size: 18px; display: flex; align-items: center; justify-content: center; }
        .badge { background: #00a884; color: white; text-align: center; padding: 6px; font-size: 11px; }
        .badge a { color: white; }
        .typing { color: #8696a0; font-style: italic; font-size: 13px; padding: 8px 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="avatar">🦷</div>
            <div class="info">
                <h3>Demo Dental Clinic</h3>
                <p>AI Assistant • Always Online</p>
            </div>
        </div>
        <div class="chat" id="chat">
            <div class="message bot">👋 Hello! Welcome to Demo Dental Clinic.

I'm your AI dental assistant. How can I help you today?

1️⃣ Book an appointment
2️⃣ View our services & pricing
3️⃣ Check clinic hours & location
4️⃣ Talk to our team

Just type a number or ask me anything! 😊
                <div class="time">Now</div>
            </div>
        </div>
        <div class="input-area">
            <input type="text" id="userInput" placeholder="Type a message..." onkeypress="if(event.key==='Enter')sendMessage()">
            <button onclick="sendMessage()">➤</button>
        </div>
        <div class="badge">⚡ Powered by <b>Phyto Link Venture</b> — AI WhatsApp Automation</div>
    </div>
    <script>
        function sendMessage() {
            const input = document.getElementById('userInput');
            const msg = input.value.trim();
            if (!msg) return;
            
            const chat = document.getElementById('chat');
            const now = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            
            // User message
            chat.innerHTML += `<div class="message user">${msg}<div class="time">${now}</div></div>`;
            input.value = '';
            
            // Typing indicator
            chat.innerHTML += `<div class="typing" id="typing">typing...</div>`;
            chat.scrollTop = chat.scrollHeight;
            
            // Bot response (simulate delay)
            setTimeout(async () => {
                document.getElementById('typing')?.remove();
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: msg})
                });
                const data = await res.json();
                chat.innerHTML += `<div class="message bot">${data.reply}<div class="time">${now}</div></div>`;
                chat.scrollTop = chat.scrollHeight;
            }, 800 + Math.random() * 700);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    reply = generate_bot_response(user_message)
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=False)
