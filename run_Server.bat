@echo off
:: 1. Navigate to your project folder
cd /d "D:\FastAPI"

:: 2. Activate the virtual environment
call venv\Scripts\activate

:: 3. Run the server
uvicorn app.main:app --reload

:: 4. Keep the window open so you can see logs (optional)
cmd /k