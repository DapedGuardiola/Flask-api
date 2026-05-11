# Flask API - NextWatch

## Setup
1. Create virtual environment: `python -m venv venv`
2. Activate: `.\venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env`
5. Run: `python app.py`

## Endpoints
- POST `/saw/rank` — ranking film dengan SAW
- POST `/cbf/recommend` — rekomendasi dengan CBF
