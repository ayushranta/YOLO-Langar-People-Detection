# ---------------- Auto Install Required Libraries ---------------- #
import sys, subprocess, importlib

required = ["ultralytics", "opencv-python", "PyQt5", "numpy", "matplotlib"]
for pkg in required:
    try:
        importlib.import_module(pkg if pkg != "opencv-python" else "cv2")
    except ImportError:
        print(f"📦 Installing missing package: {pkg} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

# ---------------- Imports ---------------- #
import sys, csv, time
import cv2
import numpy as np
from ultralytics import YOLO
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QFrame, QGridLayout, QPushButton, QFileDialog, QComboBox
)
from PyQt5.QtGui import QImage, QPixmap, QFont, QColor, QPalette
from PyQt5.QtCore import QTimer, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# ---------------- Food Requirement Logic ---------------- #    
def calculate_food_requirements(people_count: int):
    plate_count = people_count
    rice_kg = people_count * 0.25
    dal_liters = people_count * 0.2
    roti_count = people_count * 2
    sabji_kg = people_count * 0.15

    return {
        "Plates": plate_count,
        "Rice (kg)": round(rice_kg, 2),
        "Dal (liters)": round(dal_liters, 2),
        "Rotis": roti_count,
        "Sabji (kg)": round(sabji_kg, 2)
    }


# ---------------- GUI Application ---------------- #
class LangarHallApp(QWidget):
    def __init__(self):
        super().__init__()

        # YOLO + Camera
        self.model = YOLO("yolov8n.pt")  # lightweight model
        self.cap = cv2.VideoCapture(0)

        # Tracking
        self.last_update_time = 0
        self.person_count = 0
        
        self.history = []

        # Config
        self.update_interval = 5  # seconds
        self.hall_capacity = 5
        self.dark_mode = False

        # GUI Setup
        self.setWindowTitle("Langar Hall Management Dashboard")
        self.setGeometry(50, 50, 1400, 800)

        main_layout = QHBoxLayout()

        # Left Panel (Video + Camera Selector)
        left_panel = QVBoxLayout()
        video_title = QLabel("🎥 Live Hall Feed")
        video_title.setFont(QFont("Arial", 16, QFont.Bold))
        video_title.setAlignment(Qt.AlignCenter)

        self.video_label = QLabel()
        self.video_label.setFixedSize(640, 480)
        self.video_label.setFrameStyle(QFrame.Box | QFrame.Raised)

        self.camera_selector = QComboBox()
        self.camera_selector.addItems(["Camera 0", "Camera 1", "Camera 2"])
        self.camera_selector.currentIndexChanged.connect(self.switch_camera)

        left_panel.addWidget(video_title)
        left_panel.addWidget(self.video_label, alignment=Qt.AlignCenter)
        left_panel.addWidget(self.camera_selector)
        main_layout.addLayout(left_panel)

        # Right Panel (Dashboard)
        right_panel = QVBoxLayout()

        heading = QLabel("🍽 Langar Hall Dashboard")
        heading.setFont(QFont("Arial", 20, QFont.Bold))
        heading.setAlignment(Qt.AlignCenter)
        right_panel.addWidget(heading)

        # People stats
        self.people_count_label = QLabel("Current People: 0")
        self.people_count_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.people_count_label.setAlignment(Qt.AlignCenter)
        right_panel.addWidget(self.people_count_label)

        
        self.capacity_label = QLabel(f"Hall Capacity: {self.hall_capacity}")
        self.capacity_label.setFont(QFont("Arial", 14))
        self.capacity_label.setAlignment(Qt.AlignCenter)
        right_panel.addWidget(self.capacity_label)

        # Food stats
        stats_frame = QFrame()
        stats_frame.setFrameShape(QFrame.StyledPanel)
        grid = QGridLayout()

        self.food_labels = {}
        for i, item in enumerate(["Plates", "Rice (kg)", "Dal (liters)", "Rotis", "Sabji (kg)"]):
            lbl = QLabel(f"{item}: 0")
            lbl.setFont(QFont("Arial", 14))
            grid.addWidget(lbl, i, 0)
            self.food_labels[item] = lbl

        stats_frame.setLayout(grid)
        right_panel.addWidget(stats_frame)

        # Chart (Matplotlib)
        self.figure = Figure(figsize=(4, 3))
        self.canvas = FigureCanvas(self.figure)
        right_panel.addWidget(self.canvas)

        # Buttons
        btn_layout = QHBoxLayout()
        reset_btn = QPushButton("🔄 Reset Count")
        reset_btn.clicked.connect(self.reset_count)
        theme_btn = QPushButton("🌗 Toggle Theme")
        theme_btn.clicked.connect(self.toggle_theme)
        save_btn = QPushButton("💾 Export Food Report")
        save_btn.clicked.connect(self.save_report)
        btn_layout.addWidget(reset_btn)
        btn_layout.addWidget(theme_btn)
        btn_layout.addWidget(save_btn)

        right_panel.addLayout(btn_layout)

        main_layout.addLayout(right_panel)
        self.setLayout(main_layout)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(50)  # ~20 fps

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return


        # Run YOLO continuously (bounding boxes always visible)
        results = self.model(frame, verbose=False)[0]
        count = 0
        for box in results.boxes:
            cls_id = int(box.cls[0])
            if self.model.names[cls_id] == "person":
                count += 1
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        current_time = time.time()
        if current_time - self.last_update_time >= self.update_interval:
            self.history.append(count)
            if len(self.history) > 3:
                self.history.pop(0)
            self.person_count = int(np.mean(self.history))
           
            self.last_update_time = current_time

            # Update Dashboard
            self.people_count_label.setText(f"Current People: {self.person_count}")
           

            food_reqs = calculate_food_requirements(self.person_count)
            for item, lbl in self.food_labels.items():
                lbl.setText(f"{item}: {food_reqs[item]}")

            # Capacity alert
            if self.person_count > self.hall_capacity:
                self.capacity_label.setText(f"⚠ Capacity Exceeded! ({self.person_count}/{self.hall_capacity})")
                self.capacity_label.setStyleSheet("color: red; font-weight: bold;")
            else:
                self.capacity_label.setText(f"Hall Capacity: {self.hall_capacity}")
                self.capacity_label.setStyleSheet("color: black;")

            # Update chart
            self.plot_chart(food_reqs)

        # Convert frame to Qt image
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qt_img = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        pix = QPixmap.fromImage(qt_img).scaled(
            self.video_label.width(), self.video_label.height(), Qt.KeepAspectRatio
        )
        self.video_label.setPixmap(pix)

    def plot_chart(self, food_reqs):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        items = list(food_reqs.keys())
        values = list(food_reqs.values())
        ax.bar(items, values, color="skyblue")
        ax.set_title("Food Requirements")
        self.canvas.draw()

    def reset_count(self):
        self.person_count = 0
        
        self.history = []
        self.people_count_label.setText("Current People: 0")
        
        for item, lbl in self.food_labels.items():
            lbl.setText(f"{item}: 0")
        print("✅ Counts reset")

    def toggle_theme(self):
        if self.dark_mode:
            app.setStyle("Fusion")
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(240, 240, 240))
            palette.setColor(QPalette.WindowText, Qt.black)
            app.setPalette(palette)
            self.dark_mode = False
        else:
            app.setStyle("Fusion")
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            app.setPalette(palette)
            self.dark_mode = True

    def switch_camera(self, index):
        self.cap.release()
        self.cap = cv2.VideoCapture(index)
        print(f"📷 Switched to camera {index}")

    def save_report(self):
        food_reqs = calculate_food_requirements(self.person_count)
        path, _ = QFileDialog.getSaveFileName(self, "Save Report", "food_report.csv", "CSV Files (*.csv)")
        if path:
            with open(path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Item", "Quantity"])
                for item, qty in food_reqs.items():
                    writer.writerow([item, qty])
            print(f"✅ Report saved at {path}")

    def closeEvent(self, event):
        self.cap.release()


# ---------------- Main ---------------- #
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LangarHallApp()
    window.show()
    sys.exit(app.exec_())
