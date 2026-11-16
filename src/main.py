import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class SpeechifyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Speechify Desktop")
        self.resize(1000, 700)
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 20, 25, 20)
        main_layout.setSpacing(15)

        title = QLabel("Speechify Desktop")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title)

        self.text_area = QPlainTextEdit()
        self.text_area.setPlaceholderText("Enter or paste text to read aloud...")
        main_layout.addWidget(self.text_area, stretch=1)

        controls_group = QGroupBox("Reading Controls")
        controls_layout = QVBoxLayout(controls_group)
        controls_layout.setSpacing(10)

        voice_layout = QHBoxLayout()
        voice_label = QLabel("Voice:")
        self.voice_combo = QComboBox()
        self.voice_combo.addItems(["Default (placeholder)", "Kokoro (planned)", "Piper (planned)"])
        voice_layout.addWidget(voice_label)
        voice_layout.addWidget(self.voice_combo, stretch=1)
        controls_layout.addLayout(voice_layout)

        speed_layout = QHBoxLayout()
        speed_label = QLabel("Speed:")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(50, 200)
        self.speed_slider.setValue(100)
        self.speed_slider.setTickInterval(10)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_value_label = QLabel("1.0x")
        self.speed_value_label.setMinimumWidth(40)
        self.speed_slider.valueChanged.connect(self.on_speed_changed)
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_slider, stretch=1)
        speed_layout.addWidget(self.speed_value_label)
        controls_layout.addLayout(speed_layout)

        buttons_layout = QHBoxLayout()
        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")
        self.stop_button = QPushButton("Stop")
        self.clear_button = QPushButton("Clear Text")

        self.play_button.clicked.connect(self.on_play)
        self.pause_button.clicked.connect(self.on_pause)
        self.stop_button.clicked.connect(self.on_stop)
        self.clear_button.clicked.connect(self.on_clear)

        buttons_layout.addWidget(self.play_button)
        buttons_layout.addWidget(self.pause_button)
        buttons_layout.addWidget(self.stop_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.clear_button)
        controls_layout.addLayout(buttons_layout)

        main_layout.addWidget(controls_group)

        self.status_label = QLabel("Status: Ready")
        main_layout.addWidget(self.status_label)

    def on_speed_changed(self, value):
        self.speed_value_label.setText(f"{value / 100:.1f}x")

    def on_play(self):
        if not self.text_area.toPlainText().strip():
            self.status_label.setText("Status: No text to read")
            return
        voice = self.voice_combo.currentText()
        speed = self.speed_value_label.text()
        self.status_label.setText(f"Status: Play requested ({voice}, {speed})")

    def on_pause(self):
        self.status_label.setText("Status: Pause requested")

    def on_stop(self):
        self.status_label.setText("Status: Stop requested")

    def on_clear(self):
        self.text_area.clear()
        self.status_label.setText("Status: Text cleared")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpeechifyWindow()
    window.show()
    sys.exit(app.exec())
