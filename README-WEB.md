# SalesInsight web migration — fixed flow

## User flow
1. Create account
2. Choose subscription
3. Upload CSV/XLSX
4. Claude profiles the schema/sample and recommends semantic field mapping
5. Python/pandas deterministically cleans and calculates the real analytics
6. Dashboard, product, customer, forecast and performance pages use the same processed dataset

The LLM is **not** used to invent KPI values or chart data. This is deliberate: numerical analytics must come from the uploaded dataset. Claude is used for schema interpretation and evidence-based dataset insights.

## Configure Claude
Create a `.env` file in the project root (next to `frontend` and `backend`) using `.env.example`:

```env
ANTHROPIC_API_KEY=your_real_key
ANTHROPIC_MODEL=claude-sonnet-4-5
```

Never put the API key in React/frontend code.

## Run backend
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\activate
python -m pip install -r backend\requirements.txt
python -m uvicorn backend.app.main:app --reload --port 8000
```

## Run frontend in a second terminal
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.
