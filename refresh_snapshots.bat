@echo off

cd /d "C:\Users\Samarveer\Desktop\MarketMind AI\backend"

call "..\venv\Scripts\activate.bat"

python daily_ingestion.py

pause