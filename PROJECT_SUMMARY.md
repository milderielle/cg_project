# Animated Billboard Designer

โปรเจคนี้เป็นระบบสำหรับสร้าง animation แบบ shape morphing ด้วยเส้นโค้ง Bezier

## โจทย์ที่ต้องทำ

1. **Core Concept** - ผสม control points ระหว่างรูปร่าง ใช้ parameter t ตั้งแต่ 0 ถึง 1
2. **Shape Creation** - ผู้ใช้คลิกเพื่อวาด เขียนหลายเส้นโค้ง Bezier ติดต่อกัน ตรวจสอบ control points
3. **Animation Generation** - ผสมรูปร่างให้เป็นภาพเคลื่อนไหว รูป A → B → C → ... → A (วนกลับ)
4. **Visual Quality** - เรียงลำดับจุดถูกต้อง มี easing function หลายตัวให้เลือก ต่อเนื่องไม่มีรอยปะ
5. **Usability** - แสดงจำนวน points ได้ สร้าง แก้ไข ลบรูปร่าง ดูตัวอย่างแบบเรียลไทม์

## สิ่งที่ทำในโปรเจค
- คณิตศาสตร์ Bezier Curves (De Casteljau's algorithm)
- ระบบจัดการรูปร่าง (Curve, Shape, ShapeCollection classes)
- ระบบ Animation (ผสม control points สร้างเฟรม)
- Easing Functions (16 ฟังก์ชัน)
- UI อินเตอร์เฟซสำหรับวาดรูปร่างและเล่น animation
- บันทึก-เรียกใช้ข้อมูล JSON
- 28 test ผ่านทั้งหมด
- เอกสาร: README.md, INSTALL.md, STRUCTURE.md

## โครงสร้างไฟล์

```
CGpj/
├── main.py              - เริ่มต้นที่นี่
├── config.py            - ตั้งค่า
├── bezier.py            - คณิตศาสตร์ Bezier
├── shape.py             - จัดการรูปร่าง
├── animation.py         - สร้าง animation
├── easing.py            - ฟังก์ชันเลื่อน
├── ui.py                - อินเตอร์เฟซ
├── demo.py              - ตัวอย่างการใช้
├── test.py              - ทดสอบ
├── README.md
├── INSTALL.md
├── STRUCTURE.md
└── requirements.txt
```

## วิธีใช้งาน

### ขั้นตอนเริ่มต้น

1. รันโปรแกรม: `python main.py`
2. สร้างรูปร่าง: คลิก "New Shape" → คลิกบน canvas → คลิกขวาจบการวาด → "Finish Shape"
3. เล่น Animation: "Generate Animation" → เลือก easing → "Play"

### อ่านเพิ่มเติม

- ดู INSTALL.md สำหรับการติดตั้ง
- ดู README.md สำหรับอะไรต่างๆ
- รัน `python demo.py` เพื่อดูตัวอย่าง
- รัน `python test.py` เพื่อตรวจสอบ

## เทคนิคสำคัญ

- De Casteljau's Algorithm สำหรับคำนวณเส้นโค้ง Bezier
- Linear Interpolation สำหรับผสม control points
- Easing Functions 16 ตัว (linear, ease-in, ease-out, cubic, sine, exponential, circular)
- ตรวจสอบ control points ให้เท่ากัน
- วนกลับ animation แบบไร้รอยต่อ

## ไม่ต้องติดตั้งอะไร

- ใช้ Python standard library เท่านั้น
- Tkinter สำหรับ GUI (มาพร้อม Python)
- JSON สำหรับบันทึกไฟล์
- Math library สำหรับคำนวณ

---

ไปที่ INSTALL.md เพื่อเริ่มใช้งาน
