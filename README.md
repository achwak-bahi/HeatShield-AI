\# HeatShield AI



AI-powered heat risk prediction platform with machine learning, FastAPI backend, and React frontend.



\## Current features



\- User registration and login with JWT

\- Heat risk prediction

\- Prediction history per user

\- Dashboard with latest risk, average score, prediction distribution, and top risky locations

\- Methodology documentation page



\## Project structure



\- `src/` — data collection, model training, and prediction logic

\- `backend/` — FastAPI REST API and database models

\- `frontend/` — React application

\- `models/` — trained ML model files (not committed)

\- `data/` — training and reference datasets



\## Backend setup



```powershell

python -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt

uvicorn backend.main:app --reload

```



The API runs on `http://127.0.0.1:8000`.



\## Frontend setup



```powershell

cd frontend

npm install

npm run dev

```



The frontend runs on `http://localhost:3000`.



\## Model files



The trained model files are not uploaded to GitHub. Run the training pipeline before starting predictions.



\## Next improvements



\- Interactive map visualization

\- Personalized safety recommendations

\- Better dashboards and visual design

\- Deployment to the cloud

