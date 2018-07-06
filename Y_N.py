from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QMovie, QPixmap
from PyQt5.QtCore import Qt, QTimer, QSize, QRect, QPoint, QThread, pyqtSignal

import datetime, os, random, requests, bs4, sys


class GifImg(QLabel):
    signal = pyqtSignal()

    def __init__(self, file_name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mov = QMovie(file_name)
        self.mov.start()
        self.setMovie(self.mov)

    def mousePressEvent(self, event):
        self.signal.emit()

class SlowTask(QThread):
    signalAnimation1 = pyqtSignal()
    signalAnimation2 = pyqtSignal()
    signalMessageY = pyqtSignal()
    signalMessageN = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(SlowTask, self).__init__(*args, **kwargs)

    def run(self):
        s=requests.get('https://sinoptik.com.ru/погода-москва')
        b=bs4.BeautifulSoup(s.text, "html.parser")
        p3=b.select('.temperature .p3')
        pogoda1=p3[0].getText()
        inp_1 = int(pogoda1[1:3])
        x = []
        y = []
        for _ in range(10000):
            inp_2 = str(datetime.datetime.today())
            x.append(int(inp_2[-6:]))
            y.append(int(inp_2[-6:])/random.randint(1,inp_1))   
        x2 = sum(x) / len(x)
        y2 = sum(y) / len(y)
        r = (x2 + y2) % 2

        if r > 1:                         
            self.signalAnimation1.emit()
            self.signalMessageY.emit()
        else:
            self.signalAnimation2.emit()
            self.signalMessageN.emit()


class Main(QWidget):
    def __init__(self):
        super().__init__()
        button_gif = os.getcwd() + os.sep + 'img/'+ "x2.gif"
        label_gif = GifImg(button_gif)
        label_gif.setAlignment(Qt.AlignHCenter| Qt.AlignVCenter)

        label_gif.signal.connect(self.click)
        layout = QVBoxLayout()
        layout.addWidget(label_gif)

        self.button2 = QPushButton('Try again?', self)
        self.button2.clicked.connect(self.click)
        self.button2.move(288, 305)
        self.button2.setMaximumHeight(30)
        self.button2.setMaximumWidth(40)
        self.button2.setStyleSheet("""
        QPushButton:hover { color: #2e354f; text-align: center; border: 1px solid #2e354f; background: #f24964; min-width: 80px; }
        QPushButton:!hover { color: #f24964; text-align: center; border: 1px solid #2e354f; background: #2e354f; min-width: 80px;}
        QPushButton:pressed {color: #f24964; text-align: center;  border: 1px solid #f24964; background: #2e354f; min-width: 80px;}""")

        self.button6 = QPushButton(self)
        self.button6.clicked.connect(self.quit_e)
        self.button6.move(370, 300)
        self.button6.setMaximumHeight(30)
        self.button6.setMaximumWidth(30)
        self.button6.setStyleSheet("""
        QPushButton:!hover { border-image: url(img/cl1.png) 10 10 10 10; border-top: 10px transparent; border-bottom: 10px transparent;
            border-right: 10px transparent; border-left: 10px transparent;}
        QPushButton:hover { border-image: url(img/cl_h1.png) 10 10 10 10; border-top: 10px transparent; border-bottom: 10px transparent;
            border-right: 10px transparent; border-left: 10px transparent;}
        QPushButton:pressed { border-image: url(img/cl_p1.png) 10 10 10 10; border-top: 10px transparent; border-bottom: 10px transparent;
            border-right: 10px transparent; border-left: 10px transparent;} """)

        self.label_title = QLabel(self)
        self.label_title.setGeometry(QRect(0, 300, 120, 30))
        self.label_title.setStyleSheet("font: 10pt \"Segoe UI\";color: rgb(180,180,180);")
        self.label_title.setAlignment(Qt.AlignHCenter| Qt.AlignVCenter) 
        self.label_title.setText("Are you sure? :)")

        self.labelf = QLabel(self)
        self.labelf.setGeometry(QRect(0, 0, 400, 300))
        self.labelf.setLayout(layout)

        self.label = QLabel(self)
        self.label.setGeometry(QRect(0, 0, 400, 300))
        self.label.setAlignment(Qt.AlignHCenter| Qt.AlignVCenter)
        self.label.hide()

        self.setWindowTitle('Are you sure? :)')
        logo = os.getcwd() + os.sep + 'img/' + 'logo.ico'
        self.setWindowIcon(QIcon(logo))
        self.setFixedSize(400, 330)
        self.setStyleSheet("background: #2e354f; font: 10pt \"Segoe UI\";")
        self.setWindowFlags(Qt.FramelessWindowHint)
    
    def center(self):
            qr = self.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def quit_e(self):
        app.quit()

    def click(self):
        self.animation_load()
        self.label_title.setText("I think... ")
        QTimer.singleShot(2000, self.main)
    
    def main(self):
        self.task = SlowTask(self)
        self.task.signalAnimation1.connect(self.animation_1)
        self.task.signalMessageY.connect(self.message_yes)
        self.task.signalAnimation2.connect(self.animation_2)
        self.task.signalMessageN.connect(self.message_no)
        self.task.start()
    
    def animation_load(self):
        self.label.show()
        load_p = os.getcwd() + os.sep + 'img/'+ '39920.gif'
        movie = QMovie(load_p)
        self.label.setMovie(movie)
        
        movie.start()

    def animation_1(self):
        my = os.getcwd() + os.sep + 'img/'+ 'y' + str(random.randint(1,6)) + '.gif'
        movie_y = QMovie(my)
        self.label.setMovie(movie_y)
        self.label.setScaledContents(False)
        movie_y.start()

    def message_yes(self):
        self.label_title.setText("Yes")

    def animation_2(self):
        mn = os.getcwd() + os.sep + 'img/'+ 'n' + str(random.randint(1,6)) + '.gif'
        movie_n = QMovie(mn)
        self.label.setMovie(movie_n)
        self.label.setScaledContents(False)
        movie_n.start()

    def message_no(self):
        self.label_title.setText("No")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())