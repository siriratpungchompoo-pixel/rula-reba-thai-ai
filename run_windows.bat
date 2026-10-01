@echo off
chcp 65001 >nul
if not exist venv (
  echo กำลังสร้าง virtual environment...
  py -3.11 -m venv venv
)
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
