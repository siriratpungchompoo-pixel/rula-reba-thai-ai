# RULA / REBA ภาษาไทย พร้อม AI ช่วยประเมิน

เว็บแอปสำหรับการเรียนการสอนด้านการยศาสตร์และ Work Study

## ความสามารถ
- RULA และ REBA ภาษาไทย
- ประเมินก่อน–หลังปรับปรุง
- Upload ภาพหรือถ่ายภาพจากกล้อง
- MediaPipe ช่วยตรวจจับจุดข้อต่อและเสนอค่ามุม
- รูปเกณฑ์และตารางคะแนนอยู่ใกล้ขั้นตอนที่ใช้
- ผู้ประเมินยืนยัน Force/Load, Coupling, Repetition, Static posture และการบิดด้วยตนเอง
- Export รายงาน PDF ภาษาไทย

## เริ่มใช้งานในเครื่อง

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

แนะนำ Python 3.11

## Deploy

อ่าน [DEPLOY_STREAMLIT_TH.md](DEPLOY_STREAMLIT_TH.md)

## ข้อจำกัด

AI เป็นเครื่องมือช่วยคัดกรองจากภาพ 2 มิติ ไม่ใช่ผู้ประเมินแทนมนุษย์
ปัจจัยด้านแรง น้ำหนัก การจับ การค้างท่า ความถี่ และการเคลื่อนไหวนอกระนาบ
ต้องตรวจสอบจากสภาพงานจริง

## Privacy

หาก deploy บน cloud ภาพที่อัปโหลดจะถูกประมวลผลบน server ของแอป
อย่าอัปโหลดข้อมูลลับหรือภาพบุคคลโดยไม่มีสิทธิ์/ความยินยอม
