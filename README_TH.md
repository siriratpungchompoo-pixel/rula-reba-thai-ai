# RULA / REBA Student Web App V5 — ภาษาไทย + AI ช่วยประเมิน

เว็บแอปสำหรับห้องปฏิบัติการการยศาสตร์/Work Study โดยออกแบบให้ **AI เป็นผู้ช่วยวัดมุม** แต่ยังคงให้ผู้เรียนเป็นผู้ตัดสินตัวแปรที่ต้องอาศัยการสังเกตจริง เช่น แรง/น้ำหนัก การจับชิ้นงาน การทำซ้ำ การค้างท่า และการบิดออกนอกระนาบ

## จุดสำคัญของ V5

- หน้าจอหลักเป็นภาษาไทย
- เลือกประเมิน **RULA หรือ REBA**
- ใช้ภาพจากการ Upload หรือถ่ายภาพจากกล้อง
- ใช้ **MediaPipe Pose** ตรวจจับจุดข้อต่อและเสนอค่ามุมซ้าย/ขวา
- แสดงภาพโครงกระดูกที่ AI ตรวจจับ
- ผู้ใช้เลือกด้านซ้าย/ขวา หรือใช้ด้านที่ AI แนะนำจากความชัดของจุดข้อต่อ
- ภาพอ้างอิงของแต่ละส่วนร่างกายแสดง **อยู่ตรงขั้นตอนที่กำลังให้คะแนน**
- ตาราง A / B / C อยู่ตรงขั้นตอนที่นำคะแนนไป lookup พร้อมแสดงค่าที่ระบบใช้
- เปรียบเทียบ **ก่อนปรับปรุง / หลังปรับปรุง**
- ดาวน์โหลดผลเป็น JSON
- ดาวน์โหลด **รายงาน PDF ภาษาไทย**
- ไม่คำนวณ “% improvement” จากคะแนน RULA/REBA เพราะคะแนนเป็น ordinal risk score

## การติดตั้งบน Windows

แนะนำ Python 3.11

```bat
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

จากนั้นเปิด URL ที่ Streamlit แสดง เช่น `http://localhost:8501`

## macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Deploy ให้ทุกคนใช้ผ่าน Streamlit Community Cloud

1. สร้าง GitHub repository ของโครงการนี้
2. Upload ไฟล์ทั้งหมดในโฟลเดอร์ V5 ไปยัง repository
3. เข้า Streamlit Community Cloud และสร้างแอปใหม่
4. เลือก repository และกำหนด Main file เป็น `app.py`
5. ใช้ Python 3.11
6. Deploy

เวอร์ชันนี้ใช้ `st.camera_input` สำหรับถ่ายภาพ จึง **ไม่ต้องใช้ Metered.ca API key หรือ TURN server**

ไฟล์ `packages.txt` จะให้ Streamlit Cloud ติดตั้งฟอนต์ที่รองรับภาษาไทยเพื่อสร้าง PDF

## วิธีใช้ใน Lab

1. กรอกชื่อ/รหัสนักศึกษา งานหรือสถานีที่ประเมิน
2. เลือก RULA หรือ REBA
3. เปิดแท็บ “ก่อนปรับปรุง”
4. Upload หรือถ่ายภาพ โดยควรถ่ายให้เห็นร่างกายชัดและกล้องตั้งฉากกับระนาบที่ต้องการประเมิน
5. กด “ให้ AI ตรวจจับข้อต่อและวัดมุม”
6. ตรวจค่ามุมซ้าย/ขวา แล้วกดนำค่ามุม AI ไปใช้
7. ตรวจภาพอ้างอิงที่อยู่ตรงหัวข้อและยืนยันตัวปรับคะแนนด้วยตนเอง
8. ทำแบบเดียวกันในแท็บ “หลังปรับปรุง”
9. เปิดแท็บ “สรุปก่อน–หลัง” และดาวน์โหลด PDF

## สิ่งที่ AI ไม่ควรตัดสินจากภาพนิ่งเพียงอย่างเดียว

- แรง/น้ำหนักจริงที่ผู้ปฏิบัติงานรับ
- คุณภาพการจับชิ้นงาน (Coupling)
- ความถี่การทำซ้ำ
- ระยะเวลาการค้างท่า
- แรงกระแทกหรือแรงที่เพิ่มขึ้นทันที
- Twist / side bending บางกรณี โดยเฉพาะเมื่อเกิด out-of-plane motion

ดังนั้นผล AI ในแอปถูกใช้เป็น **ค่าช่วยวัด** ไม่ใช่การประเมินอัตโนมัติ 100%

## ข้อจำกัดของการวัดจากภาพ 2 มิติ

มุมจาก AI อาจคลาดเคลื่อนจาก perspective, การบังของข้อต่อ, เสื้อผ้า, มุมกล้อง และการหมุนออกนอกระนาบ ควรใช้ Side view และ/หรือ Front view ที่เหมาะกับตัวแปรที่ประเมิน และตรวจสภาพงานจริงร่วมด้วย

## References

- McAtamney, L. & Corlett, E.N. (1993). *RULA: a survey method for the investigation of work-related upper limb disorders*. Applied Ergonomics, 24(2), 91–99.
- Hignett, S. & McAtamney, L. (2000). *Rapid Entire Body Assessment (REBA)*. Applied Ergonomics, 31, 201–205.
- Cornell University Ergonomics Web: RULA / REBA educational worksheets and guidance.
- MediaPipe Pose: body landmark estimation.
- แนวคิดสถาปัตยกรรม AI + Streamlit ได้รับแรงบันดาลใจจากโครงการสาธารณะ `RashidiA/Ergonomic-Risk-Evaluation-REBA` แต่ซอร์สโค้ดใน V5 นี้เขียนขึ้นใหม่เพื่อรองรับ RULA + REBA + ภาษาไทย + Before/After สำหรับงานสอน

## สิทธิ์การใช้งาน

ซอร์สโค้ด: MIT License

ภาพอ้างอิงที่มาจากโปสเตอร์/แบบประเมินซึ่งผู้ใช้จัดเตรียมให้ **ไม่รวมอยู่ใน MIT License** โปรดอ่าน `RIGHTS_NOTICE.txt` ก่อนเผยแพร่แอปต่อสาธารณะ
