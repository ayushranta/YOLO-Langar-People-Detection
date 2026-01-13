# 🧠 YOLOv8 People Detection & Food Estimation System

### *Real-Time AI Project for Langar Halls*

This project uses **YOLOv8** and **Python** to automatically detect and count people in a Langar hall (community kitchen). Based on the crowd count, the system estimates the required quantity of food (rice, dal, roti, sabji) in real time.

---

## 📌 Features

* ✔ Real-time **people detection** using YOLOv8
* ✔ Live video processing using **OpenCV**
* ✔ **Food estimation algorithm** based on crowd count
* ✔ Modern GUI using **PyQt5**
* ✔ Real-time charts and analytics using **Matplotlib**
* ✔ Supports USB cameras & CCTV feeds
* ✔ Export food reports as CSV

---

## 🛠 Tech Stack

| Component        | Technology           |
| ---------------- | -------------------- |
| Object Detection | YOLOv8 (Ultralytics) |
| Programming      | Python               |
| Video Processing | OpenCV               |
| GUI              | PyQt5                |
| Charts           | Matplotlib           |
| Model File       | `yolov8n.pt`         |

---

## 📂 Project Structure

```
YOLO_Langar_Project/
│
├── Ai.py                # Main application
├── yolov8n.pt           # YOLOv8 model
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
├── .gitignore           # Files to ignore in GitHub
```

---

## 🚀 How It Works

1. A camera captures live video feed
2. YOLOv8 model detects people in the frame
3. Crowd count is calculated
4. Food estimate is generated based on formulas
5. GUI displays:

   * Live camera feed
   * Real-time person count
   * Food (kg/L) needed
   * Bar charts

---

## 🧮 Food Estimation Formula

For example:

```
Rice  = people_count × 0.25 kg  
Dal   = people_count × 0.20 L  
Roti  = people_count × 2  
Sabji = people_count × 0.15 kg
```

(Modify as needed.)

---

## ▶️ How to Run the Project

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Run the main file

```bash
python Ai.py
```

### 3️⃣ Select a camera and start detection

---

## 📦 requirements.txt (copy this)

```
ultralytics
opencv-python
numpy
matplotlib
PyQt5
```

---

## 📄 .gitignore (copy this)

```
__pycache__/
*.mp4
*.avi
*.png
*.jpg
runs/
*.log
*.tmp
*.zip
```

---

## 📸 Screenshot 

<img width="964" height="1114" alt="image" src="https://github.com/user-attachments/assets/aac1cd5a-001b-46e2-bf30-051c2c67a748" />
```

---

## 👨‍💻 Authors

* Ayush Ranta

---

## 📚 References

* YOLOv8 Docs – Ultralytics
* OpenCV
* Crowd Counting Research Papers
* Langar Hall Food Estimation Studies

---

## ⭐ If you like this project, don't forget to star the repo!
