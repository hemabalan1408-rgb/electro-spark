"""
Electro Spark Legal Assistant — Production Backend v4.0
Venture Code: VEN-ELEC-5613 | Niralthiruvizha 3.0
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from nlp_engine import get_legal_response, get_categories, get_emergency_dict
from translator import translate_to_english, translate_from_english, get_supported_languages, detect_language
import datetime, uuid, os, json

app = Flask(__name__)
CORS(app, origins="*")

# ── PLANS (Free = 20 queries/day) ──────────────────
PLANS = {
    "free":    {"queries_per_day": 20,  "price_inr": 0,   "price_label": "Free",
                "features": ["20 queries/day", "6 languages", "Text input", "Basic legal Q&A", "Emergency contacts"]},
    "premium": {"queries_per_day": -1,  "price_inr": 99,  "price_label": "₹99/month",
                "features": ["Unlimited queries", "10+ languages", "Voice input", "Document help", "Priority support", "Chat history"]},
    "ngo":     {"queries_per_day": -1,  "price_inr": 999, "price_label": "₹999/month",
                "features": ["Everything in Premium", "Multi-user access", "Analytics dashboard", "REST API access", "Custom knowledge base", "Dedicated support", "White-label option"]}
}

# In-memory stores (use Redis/DB in production)
chat_sessions = {}   # sid -> list of messages
user_plans    = {}   # sid -> "free"|"premium"|"ngo"
daily_usage   = {}   # sid -> {"date": str, "count": int}
user_profiles = {}   # sid -> {name, email, plan, joined}

def log(msg):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def get_usage(sid):
    today = datetime.date.today().isoformat()
    u = daily_usage.get(sid, {"date": today, "count": 0})
    if u["date"] != today:
        u = {"date": today, "count": 0}
    return u

def check_quota(sid):
    plan  = user_plans.get(sid, "free")
    limit = PLANS[plan]["queries_per_day"]
    if limit == -1:
        return True, -1
    u = get_usage(sid)
    if u["count"] >= limit:
        return False, 0
    u["count"] += 1
    daily_usage[sid] = u
    return True, max(0, limit - u["count"])

# ── ROUTES ─────────────────────────────────────────

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "name": "Electro Spark Legal Assistant API",
        "version": "4.0.0",
        "venture": "VEN-ELEC-5613",
        "program": "Niralthiruvizha 3.0 — Wadhwani Ignite",
        "institute": "Sri Ramakrishna Institute of Technology, Coimbatore",
        "status": "running",
        "docs": "/docs",
        "endpoints": [
            "POST /chat", "GET /languages", "GET /categories",
            "GET /emergency", "GET /plans", "POST /subscribe",
            "POST /register", "GET /profile/<sid>",
            "GET /history/<sid>", "DELETE /history/<sid>",
            "GET /persona", "GET /financials",
            "GET /stats", "GET /health"
        ]
    })

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or not data.get("message", "").strip():
        return jsonify({"error": "No message provided"}), 400

    user_msg  = data["message"].strip()
    sel_lang  = data.get("language", "auto")
    sid       = data.get("session_id") or str(uuid.uuid4())
    is_voice  = data.get("is_voice", False)

    # Quota
    allowed, remaining = check_quota(sid)
    if not allowed:
        plan = user_plans.get(sid, "free")
        return jsonify({
            "response": ("⚠️ You've reached your 20 free queries for today. "
                         "Upgrade to Premium (₹99/month) for unlimited queries. "
                         "Or call free legal aid: 1516"),
            "quota_exceeded": True,
            "current_plan": plan,
            "queries_remaining": 0,
            "status": "quota_exceeded"
        }), 429

    try:
        # Language detection
        detected = detect_language(user_msg) if sel_lang == "auto" else sel_lang

        # Translate → English for NLP
        en_text, src_lang = translate_to_english(user_msg)

        # NLP
        en_response = get_legal_response(en_text, detected)

        # Translate back
        final = translate_from_english(en_response, detected) if detected != "en" else en_response

        # Save history
        ts = datetime.datetime.now().isoformat()
        if sid not in chat_sessions:
            chat_sessions[sid] = []
        chat_sessions[sid].append({"role": "user",  "message": user_msg,   "is_voice": is_voice, "ts": ts})
        chat_sessions[sid].append({"role": "bot",   "message": final,      "ts": ts})

        plan = user_plans.get(sid, "free")
        log(f"[{sid[:8]}] [{plan.upper()}] {'🎤' if is_voice else '💬'} {user_msg[:55]}")

        return jsonify({
            "response": final,
            "detected_language": detected,
            "english_query": en_text,
            "session_id": sid,
            "plan": plan,
            "queries_remaining": remaining,
            "status": "success"
        })

    except Exception as e:
        log(f"ERROR: {e}")
        return jsonify({
            "response": "Sorry, an error occurred. For immediate help call: 1516 (Free Legal Aid)",
            "status": "error"
        }), 500

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    sid  = data.get("session_id") or str(uuid.uuid4())
    user_profiles[sid] = {
        "name":   data.get("name", "Guest"),
        "email":  data.get("email", ""),
        "plan":   user_plans.get(sid, "free"),
        "joined": datetime.datetime.now().isoformat()
    }
    return jsonify({"session_id": sid, "profile": user_profiles[sid], "status": "registered"})

@app.route("/profile/<sid>", methods=["GET"])
def profile(sid):
    p = user_profiles.get(sid, {})
    u = get_usage(sid)
    plan  = user_plans.get(sid, "free")
    limit = PLANS[plan]["queries_per_day"]
    return jsonify({
        "profile": p,
        "plan": plan,
        "plan_details": PLANS[plan],
        "usage_today": u.get("count", 0),
        "limit_today": limit
    })

@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json() or {}
    sid  = data.get("session_id", "")
    plan = data.get("plan", "free")
    if plan not in PLANS:
        return jsonify({"error": "Invalid plan. Choose: free, premium, ngo"}), 400
    user_plans[sid] = plan
    if sid in user_profiles:
        user_profiles[sid]["plan"] = plan
    log(f"[{sid[:8]}] SUBSCRIBED → {plan.upper()}")
    return jsonify({
        "session_id": sid,
        "plan": plan,
        "features": PLANS[plan]["features"],
        "price": PLANS[plan]["price_label"],
        "status": "subscribed"
    })

@app.route("/history/<sid>", methods=["GET"])
def history(sid):
    h = chat_sessions.get(sid, [])
    return jsonify({"session_id": sid, "messages": h, "count": len(h)})

@app.route("/history/<sid>", methods=["DELETE"])
def clear_history(sid):
    chat_sessions.pop(sid, None)
    return jsonify({"session_id": sid, "status": "cleared"})

@app.route("/languages", methods=["GET"])
def languages():
    return jsonify(get_supported_languages())

@app.route("/categories", methods=["GET"])
def categories():
    return jsonify(get_categories())

@app.route("/emergency", methods=["GET"])
def emergency():
    return jsonify(get_emergency_dict())

@app.route("/plans", methods=["GET"])
def plans():
    return jsonify(PLANS)

@app.route("/persona", methods=["GET"])
def persona():
    return jsonify({
        "primary": {
            "name": "Arun Kumar", "age": 28, "location": "Small Town, Tamil Nadu",
            "education": "College Graduate", "gender": "Male",
            "occupation": "Private Company Employee",
            "interests": ["Gaming", "Entertainment"],
            "primary_info_source": "Social Media",
            "shopping_preference": "Hybrid",
            "tech_comfort": "Medium",
            "favourite_social_media": "YouTube",
            "favourite_offline_spots": "Malls",
            "segment": "Low-income rural individuals aged 25-55 seeking basic legal assistance in regional languages",
            "jtbd": {
                "functional": "Understand legal rights, file complaints, access government schemes, resolve disputes without expensive lawyers",
                "emotional": "Feel confident about legal rights, reduce fear, feel empowered and not helpless",
                "social": "Gain respect in community, help family with legal issues, stand up against injustice"
            },
            "current_alternatives": ["Village elders", "Paid lawyers", "Government offices", "NGOs", "Local politicians"],
            "gaps": ["Wrong advice from elders", "Lawyers expensive/far", "Multiple office visits", "NGOs limited reach", "Info only in English"]
        },
        "secondary": {
            "segment": "NGOs and Legal Aid Organizations providing free legal services to underprivileged communities",
            "type": "B2B",
            "plan": "NGO Plan — ₹999/month"
        }
    })

@app.route("/financials", methods=["GET"])
def financials():
    return jsonify({
        "currency": "INR",
        "business_model": "Subscription",
        "projections": [
            {"year": 1, "revenues": 500000,  "expenses": 1200000, "profit": -700000,  "phase": "Setup"},
            {"year": 2, "revenues": 1500000, "expenses": 1800000, "profit": -300000,  "phase": "Growth"},
            {"year": 3, "revenues": 3500000, "expenses": 2500000, "profit": 1000000,  "phase": "Profitable"}
        ],
        "plans": PLANS,
        "market": {
            "tam": "USD 1.7 billion (2023)",
            "cagr": "27.4% (2023-2030)",
            "sources": ["Inc42 Legal Tech Report 2023", "Fortune Business Insights 2024"]
        }
    })

@app.route("/stats", methods=["GET"])
def stats():
    total_msgs = sum(len(v) for v in chat_sessions.values())
    return jsonify({
        "active_sessions": len(chat_sessions),
        "total_messages": total_msgs,
        "registered_users": len(user_profiles),
        "plan_distribution": {
            "free":    sum(1 for p in user_plans.values() if p == "free"),
            "premium": sum(1 for p in user_plans.values() if p == "premium"),
            "ngo":     sum(1 for p in user_plans.values() if p == "ngo")
        },
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "Electro Spark API v4.0",
        "venture": "VEN-ELEC-5613",
        "uptime": "running",
        "timestamp": datetime.datetime.now().isoformat()
    })

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    DEBUG = os.environ.get("FLASK_ENV", "production") == "development"
    print("=" * 58)
    print("⚡  ELECTRO SPARK LEGAL ASSISTANT  v4.0")
    print("    Venture Code : VEN-ELEC-5613")
    print("    Program      : Niralthiruvizha 3.0")
    print("    Institute    : SRIT, Coimbatore")
    print("=" * 58)
    print(f"📡  API running at  http://0.0.0.0:{PORT}")
    print(f"🔧  Debug mode      {'ON' if DEBUG else 'OFF'}")
    print("📚  Key endpoints:")
    print("    POST /chat  |  GET /plans  |  GET /health")
    print("=" * 58)
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
