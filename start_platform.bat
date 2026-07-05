@echo off
echo Starting AI Business Platform...

:: Start Backend
start cmd /k "cd ai-business-platform && venv\Scripts\activate && uvicorn backend.main:app --reload --port 8000"

:: Wait 3 seconds
timeout /t 3

:: Start Frontend
start cmd /k "cd ai-business-platform\frontend\dashboard && npm start"

echo Both servers starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
pause
