# ระบบประมวลผลข้อมูล IoT

## แนวทางการประมวลผลข้อมูล

ระบบทำงานโดยการประมวลผลข้อมูลเซนเซอร์แบบเรียลไทม์ด้วยวิธีการดังนี้:

1. **การทำความสะอาดข้อมูล**
   - จัดการค่าที่หายไปด้วยการประมาณค่าในช่วง
   - ลบข้อมูลที่มีเวลาซ้ำกัน
   - ตรวจสอบช่วงค่าที่ถูกต้องสำหรับ:
     - อุณหภูมิ (0-50°C)
     - ความชื้น (0-100%)
     - คุณภาพอากาศ (0-500)

2. **การตรวจจับความผิดปกติ**
   - ใช้วิธี IQR (Interquartile Range) ในการตรวจจับค่าผิดปกติ
   - วิธีการคำนวณ IQR:
     1. คำนวณ Q1 (ควอไทล์ที่ 1) คือค่าที่อยู่ที่ตำแหน่ง 25%
     2. คำนวณ Q3 (ควอไทล์ที่ 3) คือค่าที่อยู่ที่ตำแหน่ง 75%
     3. คำนวณ IQR = Q3 - Q1
     4. กำหนดขอบเขตบน = Q3 + (1.5 × IQR)
     5. กำหนดขอบเขตล่าง = Q1 - (1.5 × IQR)
     6. ค่าที่อยู่นอกขอบเขตจะถูกระบุว่าเป็นค่าผิดปกติ
   

## วิธีการเริ่มต้นใช้งาน

### สิ่งที่ต้องติดตั้ง
- Docker และ Docker Compose
- Git

### ขั้นตอนการรันโปรเจค

1. Clone โปรเจค:
```bash
git clone <repository-url>
cd scgp-iot-testing
```

2. รันระบบทั้งหมดด้วย Docker Compose:
```bash
cd deployment
docker-compose up --build
```

การรันจะเริ่ม:
- Backend API (FastAPI) ที่ http://localhost:8000
- Frontend (Vue.js) ที่ http://localhost:3000
- ระบบจำลองเซนเซอร์

### เอกสาร API

สามารถดูเอกสาร API แบบ OpenAPI ได้ที่:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## โครงสร้างโปรเจค

```
/scgp-iot-testing
├── backend/          # แอพพลิเคชัน FastAPI
├── frontend/         # ส่วนติดต่อผู้ใช้ Vue.js
└── deployment/       # การตั้งค่า Docker และการ Deploy
    └── scripts/     # สคริปต์จำลองเซนเซอร์
```

## การทำงานของระบบ

1. ระบบจะรับข้อมูลจากเซนเซอร์ผ่าน API
2. ทำการประมวลผลและทำความสะอาดข้อมูลอัตโนมัติ
3. ตรวจจับความผิดปกติและแสดงผลบนหน้าเว็บ
4. เก็บข้อมูลลงฐานข้อมูล SQLite
5. แสดงผลกราฟและสถิติต่างๆ บนหน้าเว็บ