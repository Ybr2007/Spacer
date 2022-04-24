from Gui import *
from PyQt5.QtWidgets import QApplication,QMessageBox
import qdarkstyle
import sys,os

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    
    try:
        mainWin = MainWindow()

        fadeInAnim = QPropertyAnimation(mainWin,b'windowOpacity')
        fadeInAnim.setDuration(1000)
        fadeInAnim.setStartValue(0)
        fadeInAnim.setEndValue(1)
        fadeInAnim.start()

        mainWin.show()
    except BaseException as e:
        QMessageBox.critical(None,'错误',str(e))

    os._exit(app.exec_())
    