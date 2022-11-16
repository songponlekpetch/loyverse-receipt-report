# loyverse-receipt-report
For query receipt report

# Use docker
### Installation
1. ดาวน์โหลดโปรแกรม Docker Desktop https://www.docker.com/products/docker-desktop/
2. เปิดโปรเเกรม Docker Desktop
3. ไปยัง folder ของ source code
4. สร้างไฟล์ ```.env``` ใน folder project เเล้วใส่ค่า paramter ตามตัวอย่างในไฟล์ .env.example
5. สร้าง folder ชื่อ ```credentials``` เเล้ววางไฟล์ ```service_account.json``` สำหรับคุยกับ google sheet ข้างใน folder
   
### Run command
1. ไปที่ folder ของ source code เเละ run command ```docker-compose up```

   
# Use Python localy
### Installation
1. ดาวน์โหลดโปรแกรม Python เเละติดตั้ง https://www.python.org/downloads/
2. ไปยัง folder ของ source code
3. Run command ```pip install -r requirements.txt``` เพื่อติดตั้ง packages
4. สร้างไฟล์ ```.env``` ใน folder project เเล้วใส่ค่า paramter ตามตัวอย่างในไฟล์ .env.example
5. สร้าง folder ชื่อ ```credentials``` เเล้ววางไฟล์ ```service_account.json``` สำหรับคุยกับ google sheet ข้างใน folder

### Run command
1. ไปที่ folder ของ source code เเละ run command ```python main.py```
