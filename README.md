# LUEATTOK-AI (Digital Morphology Analyzer)

โปรเจกต์นี้คือแอปพลิเคชันสำหรับวิเคราะห์และแยกประเภทเซลล์เม็ดเลือดขาว (White Blood Cells) และตรวจจับความผิดปกติจากภาพ Blood Smear โดยใช้ Deep Learning (TensorFlow/Keras) พร้อม Web UI สาธิตด้วย Gradio

## โครงสร้างโปรเจกต์

```
LUEATTOK-AI/
├── app.py                 # UI (Gradio)
├── requirements.txt      # รายการ dependencies
├── data/                 # ตัวอย่างภาพและ dataset
├── demos/                # วิดีโอตัวอย่าง
├── models/               # วางไฟล์น้ำหนักโมเดลที่ฝึกเสร็จแล้วที่นี่
└── src/                  # โค้ด backend (predict.py, preprocess.py)
```

## ข้อกำหนด (Prerequisites)
- Python 3.10 หรือ 3.11
- Git (ถ้าต้องการ clone และ push ขึ้น GitHub)
- (optional) GPU + CUDA/cuDNN เมื่อต้องการรัน TensorFlow บน GPU

## การติดตั้ง (Reproducible setup)

1. Clone โปรเจกต์ และเข้าโฟลเดอร์

```bash
git clone <repo-url>
cd LueatTok-AI
```

2. สร้างและเปิดใช้งาน virtual environment

Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Windows (cmd):

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. อัปเดต pip และติดตั้ง dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. วางไฟล์โมเดล

วางไฟล์น้ำหนักโมเดลที่ฝึกเสร็จแล้ว (เช่น `model.h5`) ในโฟลเดอร์ `models/` หากยังไม่มี ให้ตรวจสอบเอกสารฝึกสอนหรือสคริปต์ training

## รันแอป (Run)

1. เปิด virtual environment (ถ้ายังไม่เปิด)

2. รัน

```bash
python app.py
```

เมื่อรันสำเร็จ Gradio จะแจ้ง URL (เช่น http://127.0.0.1:7860) เพื่อเปิดใช้งานในเบราว์เซอร์

หากต้องการระบุพอร์ต (ขึ้นอยู่กับ `app.py`):

```bash
python app.py --server_port 7861
```

## ตัวอย่างการเรียกใช้แบบโปรแกรมมาติค

เรียกใช้ฟังก์ชันใน `src/predict.py` โดยตรง (ปรับชื่อฟังก์ชันตามโค้ดจริง):

```python
from src import predict

img_path = 'data/examples/example1.jpg'
result = predict.predict_image(img_path)
print(result)
```

ดูรายละเอียดและชื่อฟังก์ชันจริงได้ที่ [src/predict.py](src/predict.py)

## ตรวจสอบและแก้ปัญหาเบื้องต้น
- ติดตั้งไม่ผ่าน: ตรวจสอบเวอร์ชัน Python และสร้าง venv ใหม่
- TensorFlow ไม่พบ GPU: ตรวจสอบไดรเวอร์ CUDA/cuDNN และเวอร์ชันที่รองรับ
- พอร์ต Gradio ถูกใช้งาน: ปิด process ที่ใช้พอร์ตหรือเปลี่ยนพอร์ต
