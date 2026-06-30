# AI Sales Agent
AI Sales Agent is a full-stack application that helps businesses answer customer queries, recommend products, generate quotes, calculate discounts, and create orders using Google's Gemini model.

## Features
- AI-powered sales assistant
- Product recommendations
- Quote generation
- Discount calculation
- Order checkout
- Customer purchase history
- Business policy support
- Sales analytics dashboard
- Chainlit chat interface
- FastAPI REST API

## Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Strands Agents
- Google Gemini
- Python Dotenv

### Frontend
- HTML
- CSS
- JavaScript

### AI
- Gemini 2.5 Flash
- Strands Agent Tools

## Project Structure
```
LLM-SALES-AGENT/

backend/
api/
database/
models/
schemas/
services/

frontend/

chainlit_app/

.env
README.md
```

## Installation

Clone the repository
```bash
git clone <repository-url>
cd LLM-SALES-AGENT
```

Create a virtual environment
```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r backend/requirements.txt
```

Create a `.env` file

```env
DATABASE_URL=your_database_url
GOOGLE_API_KEY=your_google_api_key
```

Start the FastAPI backend
```bash
cd backend
uvicorn main:app --reload
```

Run Chainlit
```bash
cd chainlit_app
chainlit run app.py
```

Open the frontend HTML files in your browser.

## API Endpoints

- Business
- Products
- Customers
- Policies
- Orders
- Quotes
- Discounts
- Checkout
- Analytics
- AI Chat

## Author
Made by **Ayush Sandal**