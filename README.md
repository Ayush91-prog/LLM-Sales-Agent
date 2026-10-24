# 🛒 Multi-Tenant AI Sales Agent & Marketplace Concierge

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-4285F4.svg?logo=google&logoColor=white)](https://ai.google.dev/)
[![Chainlit](https://img.shields.io/badge/Chainlit-2.11-FF4B4B.svg)](https://chainlit.io/)
[![Neon PostgreSQL](https://img.shields.io/badge/Database-Neon%20PostgreSQL-00E599.svg?logo=postgresql&logoColor=white)](https://neon.tech/)
[![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7.svg?logo=render&logoColor=white)](https://render.com/)

An autonomous, full-stack, multi-tenant AI Sales Marketplace designed to replicate an Amazon-grade conversational concierge. Unlike generic chatbots that merely answer FAQs, this agent dynamically resolves customer shopping intent across independent merchants, negotiates discounts strictly within merchant-defined policy thresholds, and completes end-to-end checkouts with zero human intervention.

---

## 🌐 Live Production Links

| Service | Component | Live URL |
| :--- | :--- | :--- |
| **Marketplace Portal** | Customer Onboarding, Landing & Merchant Dashboard | [Live Portal](https://ai-sales-marketplace-portal.onrender.com/) |
| **AI Storefront** | Chainlit Real-Time Shopping Assistant | [Live AI Concierge](https://llm-sales-agent.onrender.com/) |
| **Backend API** | FastAPI REST Services & Interactive Swagger Docs | [Swagger Documentation](https://ai-sales-agent-backend-uuhq.onrender.com/docs) |

---

## 🏗️ System Architecture

```mermaid
graph TD
    subgraph Client ["Client Layer"]
        A[Customer / Merchant] -->|HTTP / CDN| B[Frontend Portal<br/>Landing & Auth]
        B -->|Auto-Handoff with Session| C[Chainlit AI Storefront<br/>custom.js Bridge]
    end

    subgraph AppLayer ["Application & Intelligence Layer"]
        C -->|WebSockets / REST| D[FastAPI Backend Server]
        D -->|Intent & Multi-Tool Calls| E[Google Gemini 2.5 Flash]
        E -->|Policy Rules & Catalog Resolution| D
    end

    subgraph DataLayer ["Persistence & Cloud Infrastructure"]
        D -->|ACID Transactions| F[(Neon Serverless PostgreSQL)]
        D -->|Live Analytics| G[Merchant Admin Dashboard]
    end
```

### Key Architectural Highlights:
1. **Multi-Tenant Intent Resolution**: Customers converse naturally (e.g. *"I need 1kg Toor Dal"*). The AI searches across all merchant catalogs, isolates the matching seller, and enforces seller-specific pricing.
2. **Margin-Aware Policy Negotiation**: Business owners configure maximum discount limits (e.g., 5%) and shipping policies. The LLM acts as an autonomous sales negotiator, calculating and granting discounts without ever breaching merchant margins.
3. **Session & Address Binding**: When a customer signs up or logs in, their profile and full delivery address are bridged seamlessly into Chainlit via a custom client-side event listener (`custom.js`) and `CopilotFunction`, eliminating redundant checkout questions.
4. **Real-Time Merchant Fulfillment**: Completed orders instantly update the merchant's cloud PostgreSQL database and reflect on their management dashboard with live revenue metrics.

---

## 💻 Tech Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy, Uvicorn, Pydantic, HTTPX
- **AI & Reasoning**: Google Gemini 2.5 Flash, Strands Agents, Custom Function Tool-Calling
- **Conversational UI**: Chainlit 2.11, WebSockets, Client-Side Event Hooks
- **Frontend**: Vanilla HTML5, Modern CSS (Glassmorphism & Responsive Cards), Vanilla JavaScript
- **Database**: Neon Serverless PostgreSQL (Production) / SQLite (Testing)
- **Deployment**: Render Cloud (Web Services + Static CDN Site)

---

## 📁 Repository Structure

```
LLM-SALES-AGENT/
├── backend/
│   ├── api/                 # REST Route Handlers (Auth, Catalog, Orders, Policies, AI)
│   ├── database/            # Connection Pooling & DB Sessions
│   ├── models/              # SQLAlchemy Relational Models (Business, Customer, Order, etc.)
│   ├── schemas/             # Pydantic Schemas for Validation
│   ├── services/            # Business Logic & Auth Service
│   ├── tests/               # Pytest Automated Test Suite
│   ├── main.py              # FastAPI Application Entrypoint & Auto-Migrations
│   └── requirements.txt     # Backend Dependencies
├── chainlit_app/
│   ├── .chainlit/           # Chainlit Server Configuration (config.toml)
│   ├── public/              # Public Assets & custom.js Parameter Bridge
│   ├── app.py               # AI Chatbot Controller & Session Lifecycle Hooks
│   └── requirements.txt     # Chainlit Dependencies
├── Frontend/
│   ├── js/                  # Client Auth, Config & Dashboard Logic
│   ├── styles/              # Modern CSS Design Tokens
│   ├── index.html           # Marketplace Landing Page
│   ├── customer_login.html  # Customer Registration & Login Portal
│   ├── admin_login.html     # Merchant Sign-in & Registration
│   ├── catalog.html         # Merchant Product Management
│   ├── orders.html          # Live Merchant Order Fulfillment & Tracking
│   ├── policies.html        # Merchant Discount & Shipping Policy Rules
│   └── analytics.html       # Real-Time Revenue & Order Analytics
├── .env.example             # Environment Variable Template
├── README.md                # Project Documentation
└── requirements.txt         # Root Dependencies
```

---

## 🚀 Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Ayush91-prog/LLM-Sales-Agent.git
cd LLM-SALES-AGENT
```

### 2. Configure Environment Variables
Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql://username:password@your-neon-host/neondb?sslmode=require
GOOGLE_API_KEY=your_gemini_api_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
CHAINLIT_AUTH_SECRET=your_chainlit_secret_key_here
BACKEND_URL=http://127.0.0.1:8000/ai/chat
```

### 3. Run FastAPI Backend
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r backend/requirements.txt

# Start backend server
cd backend
uvicorn main:app --reload --port 8000
```
Backend Swagger API will be live at: `http://127.0.0.1:8000/docs`

### 4. Run Chainlit AI Storefront (in a separate terminal)
```bash
cd chainlit_app
chainlit run app.py --port 8001
```

### 5. Launch Frontend
Open `Frontend/index.html` in your browser (or use VS Code Live Server).

---

## 🧪 Running Automated Tests

Run the backend test suite with SQLite isolation:
```bash
cd backend
pytest -v
```

---

## 👨‍💻 Author

**Ayush Sandal**
* GitHub: [@Ayush91-prog](https://github.com/Ayush91-prog)
* Project: [LLM-Sales-Agent](https://github.com/Ayush91-prog/LLM-Sales-Agent)

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).