import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QDesktopWidget

class Launcher(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Игровой Лаунчер')
        self.resize(400, 300)  # Увеличиваем размер окна
        self.center()  # Размещаем окно в центре экрана

        layout = QVBoxLayout()

        self.button = QPushButton('Запустить игру', self)
        self.button.clicked.connect(self.launch_game)

        layout.addWidget(self.button)
        self.setLayout(layout)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def launch_game(self):
        # Путь к файлу с вашей игрой на Pygame
        game_file = 'tennis_game.py'

        try:
            # Запуск игры с помощью subprocess
            subprocess.Popen(['python', game_file])
        except Exception as e:
            print(f"Ошибка при запуске игры: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = Launcher()
    launcher.show()
    sys.exit(app.exec_())