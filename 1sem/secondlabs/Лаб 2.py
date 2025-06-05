import sys
import random
from PyQt5 import QtWidgets, QtGui, QtCore


class RainDrop(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 800)  # Устанавливаем фиксированный размер окна 800x800 пикселей
        self.drops_fixed = []  # Список для хранения фиксированных капель дождя
        self.drops_random = []  # Список для хранения случайных капель дождя

    def paintEvent(self, event):
        # Метод для отрисовки капель дождя и фона
        painter = QtGui.QPainter(self)

        # Устанавливаем цвет фона в белый и рисуем его
        painter.setBrush(QtGui.QColor(255, 255, 255))  # Белый цвет для фона
        painter.drawRect(0, 0, self.width(), self.height())  # Рисуем прямоугольник, заполняющий все окно

        # Устанавливаем цвет капель дождя в синий
        painter.setBrush(QtGui.QColor(0, 0, 255))  # Синий цвет для капель

        # Рисуем фиксированные капли дождя
        for drop in self.drops_fixed:
            painter.drawRect(drop[0], drop[1], drop[2], drop[3])  # Рисуем каждую фиксированную каплю

        # Рисуем случайные капли дождя
        for drop in self.drops_random:
            painter.drawRect(drop[0], drop[1], drop[2], drop[3])  # Рисуем каждую случайную каплю

    def updateDrops(self, bias=random.randint(-1, 1), speed=random.randint(20, 50)):
        # Метод для обновления состояния капель дождя

        # Добавляем новые фиксированные капли с повышенной вероятностью (например, 95%)
        if random.random() < 0.95:
            x = random.randint(0, self.width())  # Генерируем случайную позицию по оси X
            self.drops_fixed.append([x, 0, 2, random.randint(15, 25)])
            # Добавляем новую фиксированную каплю (x, y, ширина фиксированная на 2 пикселя, высота случайная от 15 до 25)

        # Перемещаем фиксированные капли вниз на 20 пикселей
        for drop in self.drops_fixed:
            drop[1] += 20  # Увеличиваем координату Y каждой фиксированной капли

        # Добавляем новые случайные капли с повышенной вероятностью (например, от 0 до 1)
        if random.random() < random.uniform(0.5, 1):
            x = random.randint(0, self.width())  # Генерируем случайную позицию по оси X
            self.drops_random.append([x, 0, random.randint(2, 4), random.randint(30, 40)])
            # Добавляем новую случайную каплю (x, y, ширина (случайно от 2 до 4), высота (случайно от 30 до 40))

        # Перемещаем случайные капли вниз с учетом смещения (bias)
        for drop in self.drops_random:
            drop[1] += speed  # Увеличиваем координату Y каждой случайной капли на скорость
            drop[0] += bias  # Смещаем каплю по оси X влево или вправо

        # Удаляем капли, которые вышли за пределы окна
        self.drops_fixed = [drop for drop in self.drops_fixed if drop[1] < self.height()]
        self.drops_random = [drop for drop in self.drops_random if drop[1] < self.height()]

        self.update()  # Обновляем виджет для перерисовки


class RainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.rain = RainDrop()  # Создаем экземпляр класса RainDrop (капли дождя)
        self.setCentralWidget(self.rain)  # Устанавливаем RainDrop как центральный виджет окна
        self.setWindowTitle("Дождь")  # Устанавливаем заголовок окна

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.rain.updateDrops)
        timer.start(19)  # Запускаем таймер для обновления состояния каждые 30 миллисекунд


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RainApp()
    window.show()
    sys.exit(app.exec_())
