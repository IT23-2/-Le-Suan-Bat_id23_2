import sys
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
import math


class StringSimulation(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Затухающие колебания струны")
        self.setGeometry(100, 100, 800, 600)

        # Параметры колебаний
        self.amplitude = 100
        self.damping = 0.05
        self.time = 0

        # Создание элементов управления
        self.initUI()

        # Таймер для обновления анимации
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_simulation)

    def initUI(self):
        # Спинбокс для длины струны
        self.length_spinbox = QtWidgets.QSpinBox(self)
        self.length_spinbox.setRange(100, 800)
        self.length_spinbox.setValue(400)
        self.length_spinbox.setPrefix("Длина струны: ")

        # Слайдер для амплитуды
        self.amplitude_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.amplitude_slider.setRange(1, 200)
        self.amplitude_slider.setValue(self.amplitude)

        # Слайдер для коэффициента затухания
        self.damping_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.damping_slider.setRange(0, 100)
        self.damping_slider.setValue(int(self.damping * 100))

        # Кнопка запуска анимации
        self.start_button = QtWidgets.QPushButton("Запустить", self)
        self.start_button.clicked.connect(self.start_animation)

        # Кнопка сброса параметров
        self.reset_button = QtWidgets.QPushButton("Сбросить", self)
        self.reset_button.clicked.connect(self.reset_parameters)

        # Расположение элементов управления
        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(self.length_spinbox)
        layout.addWidget(QtWidgets.QLabel("Амплитуда начального колебания:"))
        layout.addWidget(self.amplitude_slider)

        layout.addWidget(QtWidgets.QLabel("Коэффициент затухания:"))
        layout.addWidget(self.damping_slider)

        layout.addWidget(self.start_button)
        layout.addWidget(self.reset_button)

        self.setLayout(layout)

    def start_animation(self):
        # Обновление параметров из элементов управления
        self.amplitude = self.amplitude_slider.value()
        self.damping = self.damping_slider.value() / 100.0

        # Сброс времени и запуск таймера
        self.time = 0
        self.timer.start(16)

    def reset_parameters(self):
        # Сброс параметров к начальным значениям
        self.amplitude_slider.setValue(100)
        self.damping_slider.setValue(5)

    def update_simulation(self):
        if not (self.amplitude > 0 and self.damping >= 0):
            return

        self.time += 0.1
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        painter.fillRect(self.rect(), QtGui.QColor(255, 255, 255))

        length = self.length_spinbox.value()

        omega_0 = math.pi / length

        gamma = self.damping

        current_amplitude = self.amplitude * np.exp(-gamma * self.time)

        width = self.width()

        for x in range(width):
            t_x = (x / width) * length

            if gamma < omega_0:
                y = (self.height() // 2) + current_amplitude * np.cos(
                    omega_0 * t_x * math.sqrt(1 - (gamma ** 2 / (omega_0 ** 2))) * self.time)
            else:
                y = (self.height() // 2) + current_amplitude * np.exp(-gamma * t_x) * np.cos(omega_0 * t_x * self.time)

            painter.drawPoint(x, int(y))

            # Завершение при полном затухании
            if current_amplitude < 1e-3:
                self.timer.stop()
                break


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = StringSimulation()
    window.show()
    sys.exit(app.exec_())
