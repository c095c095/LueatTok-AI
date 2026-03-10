# LUEATTOK-AI (Digital Morphology Analyzer)

โปรเจกต์นี้คือแอปพลิเคชันสำหรับวิเคราะห์และแยกประเภทเซลล์เม็ดเลือดขาว (White Blood Cells) รวมถึงตรวจจับความผิดปกติจากภาพ Blood Smear โดยใช้ Deep Learning (TensorFlow/Keras) และแสดงผลผ่าน Web UI ด้วย Gradio

## 📂 โครงสร้างของโปรเจกต์ (Project Structure)

```text
LUEATTOK-AI/
│
├── data/                  # โฟลเดอร์สำหรับเก็บชุดข้อมูล (Dataset) ที่ใช้ในการ Train/Test โมเดล
│
├── demos/                 # โฟลเดอร์เก็บคลิปวิดีโอ Demo ของทั้ง 3 Scenarios (เช่น easy.mp4, medium.mp4, hard.mp4)
│
├── models/                # โฟลเดอร์สำหรับเก็บไฟล์น้ำหนักโมเดล (เช่น .h5, .keras) ที่ผ่านการเทรนมาแล้ว วิธีการสร้างซ้ำ
│
├── src/                   # โฟลเดอร์หลักสำหรับเก็บ Source Code การทำงานเบื้องหลัง
│   ├── __init__.py        # ไฟล์ที่ทำให้ Python รู้จักโฟลเดอร์ src ในฐานะ Module (สามารถใช้คำสั่ง import ได้)
│   ├── predict.py         # ไฟล์สำหรับโหลดโมเดล และจัดการ Logic ในการทำนายผล (Inference)
│   └── preprocess.py      # ไฟล์ฟังก์ชันสำหรับเตรียมข้อมูลภาพก่อนเข้าโมเดล (เช่น Resize, Normalize, Crop)
│
├── app.py                 # ไฟล์หลักของโปรเจกต์สำหรับสร้าง User Interface (UI) ด้วย Gradio
└── requirements.txt       # ไฟล์ระบุรายการ Libraries และเวอร์ชันที่จำเป็นสำหรับรันโปรเจกต์นี้

```

### ⚙️ คำอธิบายเพิ่มเติม

* **`app.py`**: จะเป็นเพียงส่วนหน้าบ้าน (Frontend) ที่รับรูปภาพจากผู้ใช้ และแสดงผลลัพธ์
* **`src/predict.py`**: จะเป็นส่วนหลังบ้าน (Backend) ที่รับรูปจาก `app.py` มาโยนเข้าโมเดลใน `models/` และคืนค่าผลลัพธ์กลับไป
* **การติดตั้ง (Installation)**: รันคำสั่ง `pip install -r requirements.txt` เพื่อติดตั้งสภาพแวดล้อมให้พร้อมทำงาน
* **การรันโปรแกรม (Usage)**: รันคำสั่ง `python app.py` เพื่อเปิดใช้งานแอปพลิเคชันผ่าน Web Browser
