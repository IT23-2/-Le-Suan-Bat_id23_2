import math
import tkinter as tk

# Настройки
width, height = 600, 600
center = (width// 2 ,height // 2)
root = tk.Tk()
root.title('Работа №1. Знакомство с tkinter')
speed = 0.05 # Скорость
radius = 200
point_distance = 20 # Расстояние от окружности до точки

class circle_and_point:
    def __init__(self, main):
        self.main = main
        self.canvas = tk.Canvas(main, width = width, height = height, bg = 'white')
        self.canvas.pack()

        self.angle = 0  # Начальный угол
        self.point_radius = 5  # Радиус точки

        self.animate()

    def draw_circle(self):
        x0 = center[0] - radius
        y0 = center[1] - radius
        x1 = center[0] + radius
        y1 = center[1] + radius
        self.canvas.create_oval(x0, y0, x1, y1, outline='black')

    def draw_point(self):
        x = center[0] + (radius + point_distance) * math.cos(self.angle)
        y = center[1] + (radius + point_distance) * math.sin(self.angle)

        self.canvas.delete('point')

        self.canvas.create_oval(x - self.point_radius, y - self.point_radius,
                                x + self.point_radius, y + self.point_radius,
                                fill='red', tags='point')

    def animate(self):
        self.draw_circle()
        self.draw_point()

        self.angle += speed

        # Запланируем следующий вызов функции
        self.main.after(30, self.animate)

app = circle_and_point(root)
root.mainloop()