# ⚡ ELECTRO SPARK — Deployment Guide
### Venture Code: VEN-ELEC-5613 | SRIT Coimbatore

---

## 🗂️ Project Structure
```
ELECTRO_SPARK_DEPLOY/
├── backend/
│   ├── app.py              ← Flask API (Production v4.0)
│   ├── nlp_engine.py       ← NLP query matching
│   ├── translator.py       ← 10+ language translation
│   ├── legal_db.json       ← 60+ legal Q&A database
│   ├── requirements.txt    ← Python packages
│   ├── Procfile            ← Gunicorn start command
│   └── render.yaml         ← Render.com config
└── frontend/
    └── index.html          ← Complete single-file app
```

---

## 🚀 OPTION 1: Run Locally (Development)

```bash
# 1. Install dependencies
cd backend
pip install -r requirements.txt

# 2. Start backend
python app.py
# → API running at http://localhost:5000

# 3. Open frontend
# Just double-click frontend/index.html in browser
# OR serve it:
cd frontend && python -m http.server 8080
# → Open http://localhost:8080
```

---

## ☁️ OPTION 2: Deploy to Render.com (FREE — Recommended)

### Step 1 — Deploy Backend API
1. Go to **https://render.com** → Sign up free
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repo OR upload the `backend/` folder
4. Settings:
   - **Name:** `electro-spark-api`
   - **Region:** Singapore (closest to India)
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
   - **Plan:** Free
5. Click **"Create Web Service"**
6. Copy your API URL: `https://electro-spark-api.onrender.com`

### Step 2 — Update Frontend
Open `frontend/index.html` and change line:
```javascript
const API_BASE = "http://localhost:5000";
```
to:
```javascript
const API_BASE = "https://electro-spark-api.onrender.com";
```

### Step 3 — Deploy Frontend
**Option A — Netlify (easiest):**
1. Go to **https://netlify.com**
2. Drag and drop the `frontend/` folder
3. Your app is live instantly!
   URL: `https://electro-spark.netlify.app`

**Option B — GitHub Pages:**
1. Push `frontend/index.html` to GitHub repo
2. Settings → Pages → Source: main branch
3. URL: `https://yourusername.github.io/electro-spark`

---

## ☁️ OPTION 3: Deploy to Railway.app

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
cd backend
railway login
railway init
railway up

# Get your URL from Railway dashboard
```

---

## ☁️ OPTION 4: Deploy to Heroku

```bash
# Install Heroku CLI, then:
cd backend
heroku create electro-spark-api
git init && git add . && git commit -m "deploy"
git push heroku main

# Get URL: https://electro-spark-api.herokuapp.com
```

---

## 🔧 API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat` | Send legal query, get response |
| GET | `/plans` | Get subscription plans |
| POST | `/subscribe` | Change user plan |
| POST | `/register` | Register user profile |
| GET | `/profile/<sid>` | Get user profile + usage |
| GET | `/history/<sid>` | Get chat history |
| DELETE | `/history/<sid>` | Clear chat history |
| GET | `/languages` | Supported languages |
| GET | `/categories` | Legal categories |
| GET | `/emergency` | Emergency contacts |
| GET | `/persona` | Customer persona data |
| GET | `/financials` | Financial projections |
| GET | `/stats` | Usage statistics |
| GET | `/health` | Health check |

### Chat API Example
```bash
curl -X POST https://your-api-url.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are my land rights?",
    "language": "en",
    "session_id": "user-123"
  }'
```

---

## 📱 Subscription Plans

| Plan | Queries/Day | Price | Target |
|------|-------------|-------|--------|
| Free | 20/day | ₹0 | Individual users |
| Premium | Unlimited | ₹99/month | Power users |
| NGO | Unlimited | ₹999/month | Organizations |

---

## 📊 Financial Projections (PPT Slide 18)

| Year | Revenue | Expenses | Profit |
|------|---------|----------|--------|
| Year 1 | ₹5,00,000 | ₹12,00,000 | -₹7,00,000 |
| Year 2 | ₹15,00,000 | ₹18,00,000 | -₹3,00,000 |
| Year 3 | ₹35,00,000 | ₹25,00,000 | +₹10,00,000 |

---

## 🌍 Languages Supported

Tamil · Hindi · Telugu · Kannada · Malayalam · Marathi · Bengali · Gujarati · Punjabi · Urdu · English

---

## 🚨 Emergency Contacts (Built-in)

| Service | Number |
|---------|--------|
| Police | 100 |
| Women Helpline | 181 |
| Child Helpline | 1098 |
| Free Legal Aid (DLSA) | 1516 |
| Cyber Crime | 1930 |
| Consumer Helpline | 1915 |
| Labour Helpline | 1800-11-4444 |
| Senior Citizen | 14567 |
| Ambulance | 108 |

---

## ⚠️ Disclaimer

Electro Spark provides general legal information only — not professional legal advice. For complex matters consult a licensed advocate or contact DLSA at **1516** for free legal aid.

---

*⚡ Electro Spark v4.0 | VEN-ELEC-5613 | Niralthiruvizha 3.0 | SRIT Coimbatore*
