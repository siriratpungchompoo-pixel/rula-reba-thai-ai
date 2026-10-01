# การนำ RULA / REBA Web App ขึ้น GitHub และ Streamlit Community Cloud

แพ็กเกจนี้เตรียมไว้สำหรับ deploy เป็นเว็บไซต์สาธารณะแล้ว

## ค่าที่แนะนำ

- Repository: `rula-reba-thai-ai`
- Branch: `main`
- Main file path: `app.py`
- Python: **3.11**
- Visibility: Public หากต้องการให้ทุกคนใช้งานได้
- Secrets: **ไม่ต้องใช้** สำหรับเวอร์ชันนี้

## ขั้นตอน GitHub

1. สร้าง repository ใหม่ใน GitHub ชื่อ `rula-reba-thai-ai`
2. อัปโหลดไฟล์ **ทุกไฟล์ในโฟลเดอร์นี้** ไปที่ root ของ repository
3. ตรวจว่าที่ root มีไฟล์ต่อไปนี้:
   - `app.py`
   - `requirements.txt`
   - `packages.txt`
   - `scoring.py`
   - `pose_ai.py`
   - `pdf_report.py`
   - โฟลเดอร์ `assets`
   - โฟลเดอร์ `.streamlit`
4. Commit ไปที่ branch `main`

## ขั้นตอน Streamlit Community Cloud

1. เข้า Streamlit Community Cloud และเชื่อมบัญชี GitHub
2. เลือก **Create app / Deploy an app**
3. เลือก repository `rula-reba-thai-ai`
4. Branch = `main`
5. Main file path = `app.py`
6. เปิด **Advanced settings**
7. เลือก Python **3.11**
8. Secrets เว้นว่าง
9. กด Deploy

ระบบจะติดตั้ง:
- Python packages จาก `requirements.txt`
- Linux packages จาก `packages.txt`

## หลัง Deploy

ทดสอบอย่างน้อย 6 จุด:
1. เปิดหน้าเว็บได้และภาษาไทยแสดงถูกต้อง
2. เลือก RULA และ REBA ได้
3. Upload ภาพได้
4. AI ตรวจ landmark และแสดงภาพ skeleton ได้
5. คะแนน Before/After คำนวณได้
6. ดาวน์โหลด PDF ภาษาไทยได้

## ข้อควรระวังด้านข้อมูล

แอป Streamlit ประมวลผลภาพบน server ของแอป ไม่ใช่เฉพาะในเครื่องผู้ใช้
จึงไม่ควรอัปโหลดภาพที่มีข้อมูลส่วนบุคคล ข้อมูลลับของโรงงาน หรือบุคคลที่ไม่ได้ให้ความยินยอม

## สิทธิ์ของภาพประกอบ

โค้ดของแอปมี LICENSE แยกต่างหาก แต่ภาพอ้างอิง RULA/REBA ที่ตัดจากเอกสารต้นฉบับ
ควรตรวจสอบสิทธิ์ก่อนเผยแพร่เป็นสาธารณะในวงกว้าง
หากต้องการใช้งานสาธารณะระยะยาว ควรวาดภาพประกอบใหม่ที่เป็นทรัพย์สินของโครงการ
