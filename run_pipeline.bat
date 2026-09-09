@echo off
echo ==================================================
echo Starting Weather Pipeline at %date% %time%
echo ==================================================

cd C:\Users\jenng\data_engineering_projects\project_21_api_pipeline
call venv\Scripts\activate
python scripts/api_weather_pipeline.py

echo ==================================================
echo Pipeline completed at %date% %time%
echo ==================================================
pause