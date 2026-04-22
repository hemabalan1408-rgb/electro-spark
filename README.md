<<<<<<< HEAD
# ⚡ ELECTRO SPARK — AI Legal Assistant v2.0
### Complete Product | Venture Code: VEN-ELEC-5613

---

## 📁 Project Structure

```
ELECTRO_SPARK/
├── backend/
│   ├── app.py              ← Flask API server (all routes)
│   ├── nlp_engine.py       ← NLP query matching engine
│   ├── translator.py       ← Regional language translation
│   ├── legal_db.json       ← 60+ legal Q&A in 9 categories
│   └── requirements.txt    ← Python dependencies
├── frontend/
│   └── index.html          ← Complete multi-page app
├── docs/
└── README.md
```

---

## 🚀 Quick Start

### Step 1 — Install Python dependencies
```bash
cd backend
pip install flask flask-cors deep-translator
```

### Step 2 — Start backend server
```bash
python app.py
```
✅ API running at: **http://localhost:5000**

### Step 3 — Open frontend
Just open `frontend/index.html` in your browser — no server needed!

---

## ✅ Features

### Frontend
- 🎨 Premium dark UI with 3 pages (Chat, About, Emergency)
- 💬 WhatsApp-style chat interface
- 🌐 6 language switcher (EN/Tamil/Hindi/Telugu/Kannada/Malayalam)
- 📱 Responsive sidebar navigation
- ⚡ Offline mode — works without backend
- 🚨 Emergency contacts page with copy-on-click
- 🔍 9 legal topic categories with quick cards

### Backend
- 🔌 REST API with 6 endpoints
- 🌍 10+ regional language translation
- 🧠 NLP keyword + similarity scoring
- 📝 Session-based chat history
- 🛡️ CORS enabled for frontend connection

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat` | Send message, get legal response |
| GET | `/languages` | List supported languages |
| GET | `/categories` | List legal categories |
| GET | `/emergency` | Get emergency contacts |
| GET | `/history/<session_id>` | Get chat history |
| GET | `/health` | Server health check |

### Chat API Example
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are my land rights?", "language": "en"}'
```

---

## 📚 Legal Categories Covered (60+ Q&A)

| # | Category | Topics |
|---|----------|--------|
| 1 | 🏡 Land Rights | Patta, encroachment, transfer, inheritance |
| 2 | 👷 Labour Rights | Minimum wage, PF, gratuity, maternity |
| 3 | 🛡️ Women's Rights | PWDVA, dowry, POSH, divorce, maintenance |
| 4 | 🛒 Consumer Rights | Complaints, refunds, medical, banking |
| 5 | 🏛️ Govt Schemes | PM Awas, ration card, pension, scholarships |
| 6 | 🚔 Criminal Law | FIR, arrest rights, bail, cyber crime |
| 7 | 👨‍👩‍👧 Family Law | Marriage, custody, will, adoption |
| 8 | 📋 RTI | Right to Information filing |
| 9 | 💻 Cyber Law | Online fraud, hacking, privacy |

---

## 🌍 Languages Supported

Tamil • Hindi • Telugu • Kannada • Malayalam • Marathi • Bengali • Gujarati • Punjabi • Urdu • English

---

## 🚨 Emergency Contacts (Built-in)

| Service | Number |
|---------|--------|
| Police | 100 |
| Women Helpline | 181 |
| Child Helpline | 1098 |
| Free Legal Aid | 1516 |
| Cyber Crime | 1930 |
| Consumer Helpline | 1915 |
| Labour Helpline | 1800-11-4444 |
| Senior Citizen | 14567 |

---

## 📊 Financial Projections

| Year | Revenue | Expenses | Profit |
|------|---------|----------|--------|
| Year 1 | ₹5L | ₹12L | -₹7L |
| Year 2 | ₹15L | ₹18L | -₹3L |
| Year 3 | ₹35L | ₹25L | +₹10L |

---

## ⚠️ Disclaimer

Electro Spark provides general legal information only — not professional legal advice. For complex matters, consult a licensed advocate or call DLSA: **1516** for free legal aid.

---

*Built for Wadhwani Ignite Bootcamp — Niralthiruvizha 3.0, Coimbatore*
=======
# electro-spark
AI Legal Assistant - VEN-ELEC-5613
>>>>>>> 346f00b68be1aca85ad37cbd43e11e1c97903a51
