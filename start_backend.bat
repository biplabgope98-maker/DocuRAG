@echo off
title DOCURAG Backend
echo Starting DOCURAG FastAPI Backend...
echo.

uvicorn backend.fastapi_app:app --host 127.0.0.1 --port 8000 --reload

pause