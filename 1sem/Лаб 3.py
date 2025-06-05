from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QSpinBox, QLabel, QDialog, QMainWindow
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtCore import Qt, QTimer, QRect
import random
import json

class CloudSimulation:
    def __init__(this, x_position, y_position, is_stopped, refresh_callback):
        this.x_position = x_position
        this.y_position = y_position
        this.width = 150
        this.height = 60
        this.drop_count = 130
        this.fall_speed = 4
        this.cloud_shape = 2
        this.drops = []
        this.is_stopped = is_stopped
        this.refresh_callback = refresh_callback
        this.is_dragging = False
        this.initialize_drops()

        this.timer = QTimer()
        this.timer.timeout.connect(this.update_drops)
        if not is_stopped:
            this.timer.start(10)

    def render_cloud(this, painter):
        painter.setPen(QPen(Qt.blue, 2))
        
        if this.cloud_shape == 1:
            painter.drawRect(this.x_position, this.y_position, this.width, this.height)
        elif this.cloud_shape == 2:
            painter.drawEllipse(this.x_position, this.y_position, this.width, this.height)
        elif this.cloud_shape == 3:
            pixmap = QPixmap("Vinni Pukh.png")
            painter.drawPixmap(QRect(this.x_position, this.y_position, this.width, this.height), pixmap)

        for drop in this.drops:
            painter.drawLine(drop[0], drop[1], drop[5] + drop[0], drop[1] + drop[2])

    def initialize_drops(this):
        this.drops = [
            [random.randint(this.x_position, this.x_position + this.width),
             random.randint(this.y_position + this.height, this.y_position + this.height),
             random.randint(0, 40),
             random.randint(0, 5),
             random.randint(this.fall_speed, 3 * this.fall_speed),
             random.randint(-2, 2)
            ]
            for _ in range(this.drop_count)
        ]

    def update_settings(this):
        cloud_dimensions = (this.width, this.height)
        rain_parameters = (this.drop_count, this.fall_speed)

        settings_dialog = CloudSettingsDialog(cloud_dimensions, rain_parameters, this.cloud_shape)

        if settings_dialog.exec_() == QDialog.Accepted:
            new_values = settings_dialog.get_values()
            (this.width, this.height,
             this.drop_count, this.fall_speed,
             this.cloud_shape) = new_values

            this.initialize_drops()
            this.refresh_callback()

    def update_drops(this):
        for drop in this.drops:
            drop[0] += drop[5]
            drop[1] += drop[4]
            if drop[1] + drop[2] > 800:
                drop[1] = random.randint(this.height + this.y_position + 20, this.height + this.y_position + 100)
                drop[0] = random.randint(this.x_position + 30, this.width + this.x_position - 30)

        this.refresh_callback()

class CloudSettingsDialog(QDialog):
    def __init__(this, cloud_size, rain_parameters, cloud_shape):
        super().__init__()

        layout = QVBoxLayout()
        
        this.width_spinbox = QSpinBox(this)
        this.width_spinbox.setRange(0, 800)
        this.width_spinbox.setValue(cloud_size[0])
        
        layout.addWidget(QLabel('Ширина:', this))
        layout.addWidget(this.width_spinbox)

        this.height_spinbox = QSpinBox(this)
        this.height_spinbox.setRange(0, 800)
        this.height_spinbox.setValue(cloud_size[1])
        
        layout.addWidget(QLabel('Высота:', this))
        layout.addWidget(this.height_spinbox)

        this.density_spinbox = QSpinBox(this)
        this.density_spinbox.setRange(50, 300)
        this.density_spinbox.setValue(rain_parameters[0])
        
        layout.addWidget(QLabel('Плотность капель:', this))
        layout.addWidget(this.density_spinbox)

        this.speed_spinbox = QSpinBox(this)
        this.speed_spinbox.setRange(3, 9)
        this.speed_spinbox.setValue(rain_parameters[1])
        
        layout.addWidget(QLabel('Скорость капель:', this))
        layout.addWidget(this.speed_spinbox)

        this.shape_spinbox = QSpinBox(this)
        this.shape_spinbox.setRange(1, 3)
        this.shape_spinbox.setValue(cloud_shape)
        
        layout.addWidget(QLabel('Форма облака:\n1 - Прямоугольник\n2 - Овал\n3 - Винни-Пух', this))
        
        layout.addWidget(this.shape_spinbox)

        apply_button = QPushButton("Применить", this)
        
        apply_button.clicked.connect(this.accept)  
        layout.addWidget(apply_button)

        this.setLayout(layout)
        this.setWindowTitle('Настройки облаков')
        this.show()

    def get_values(this):
       return (
           this.width_spinbox.value(),
           this.height_spinbox.value(),
           this.density_spinbox.value(),
           this.speed_spinbox.value(),
           this.shape_spinbox.value()
       )

class RainfallSimulation(QMainWindow):
    def __init__(this):
       super().__init__()

       this.setGeometry(650, 100, 800, 800)
       this.setStyleSheet("background-color: white;")

       this.clouds = []
       this.is_paused = False
       this.delete_mode = False

       this.setup_ui()

       try:
           with open('file.json', 'r') as file:
               file_j = json.load(file)

           for i in range(len(file_j['x_position'])):
               clouds_instance = CloudSimulation(
                   file_j['x_position'][i],
                   file_j['y_position'][i],
                   False,
                   lambda: None) 
               clouds_instance.width = file_j['width'][i]
               clouds_instance.height = file_j['height'][i]
               clouds_instance.drop_count = file_j['drop_count'][i]
               clouds_instance.fall_speed = file_j['fall_speed'][i]
               clouds_instance.cloud_shape = file_j['cloud_shape'][i]

               this.clouds.append(clouds_instance)

           this.update()

       except FileNotFoundError:
           print("JSON file not found. Starting with an empty simulation.")

    def setup_ui(that):
        add_cloud_btn = QPushButton("Добавить облако", that)
        add_cloud_btn.setStyleSheet("background-color: lightgreen;")
        add_cloud_btn.resize(120, 50)
        add_cloud_btn.move(10, 10)
        add_cloud_btn.clicked.connect(that.create_cloud)

        pause_btn = QPushButton("Пауза", that)
        pause_btn.setStyleSheet("background-color: lightyellow;")
        pause_btn.resize(120, 50)
        pause_btn.move(10, 70)
        pause_btn.clicked.connect(that.toggle_pause)

        delete_cloud_btn = QPushButton("Удалить облако", that)
        delete_cloud_btn.setStyleSheet("background-color: lightcoral;")
        delete_cloud_btn.resize(120, 50)
        delete_cloud_btn.move(10, 130)
        delete_cloud_btn.clicked.connect(that.enable_deletion)

        that.show()

    def create_cloud(that):
      new_cloud_instance = CloudSimulation(random.randint(1 ,600), 
                                            random.randint(20 ,100), 
                                            that.is_paused,
                                            that.refresh) 

      that.clouds.append(new_cloud_instance) 
      that.refresh()

    def mousePressEvent(that ,event):
      for cloud in reversed(that.clouds):
          cloud_rect_area = QRect(cloud.x_position,
                                   cloud.y_position,
                                   cloud.x_position+cloud.width,
                                   cloud.y_position+cloud.height)

          if cloud_rect_area.contains(event.pos()):
              if event.button() == Qt.LeftButton:
                  if that.delete_mode:
                      that.clouds.remove(cloud) 
                      that.delete_mode = False 
                      that.refresh() 
                  else:
                      cloud.update_settings()  
              elif event.button() == Qt.RightButton:
                  cloud.is_dragging=True  
                  break 

    def mouseReleaseEvent(that, event):
        if event.button() == Qt.RightButton and any(cloud.is_dragging for cloud in that.clouds):
            for cloud in that.clouds:
                if cloud.is_dragging:
                    cloud.is_dragging=False
                    cloud.x_position, cloud.y_position = event.pos().x(), event.pos().y()
                    break 

    def toggle_pause(that):
      that.is_paused=not that.is_paused  
      for cloud in that.clouds:  
          if that.is_paused:  
              cloud.timer.stop()  
          else:  
              cloud.timer.start(20)  

    def enable_deletion(that):
      that.delete_mode=True  

    def paintEvent(that ,event): 
      painter=QPainter(that) 
      for cloud in that.clouds: 
          cloud.render_cloud(painter) 
      that.update() 

    def refresh(that): 
      that.update() 

if __name__ == '__main__':
   app=QApplication([])  
   main_window=RainfallSimulation() 
   app.exec_()
