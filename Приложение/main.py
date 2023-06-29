import sys
from PyQt5.QtWidgets import QApplication
from window_authorization import authorization
#from main_window import Form
app = QApplication(sys.argv)
window = authorization() 
window.show()
sys.exit(app.exec_())






  



