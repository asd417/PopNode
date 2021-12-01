import sys
from PyQt5 import QtWidgets, QtCore, QtGui #pyqt stuff

from node_editor_wnd import NodeEditorWnd

# credit to
# https://www.youtube.com/playlist?list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz
# for extensive tutorial on node-editor in qtpy

if __name__ == '__main__':
    
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons
    
    app = QtWidgets.QApplication(sys.argv)
    wnd = NodeEditorWnd()
    sys.exit(app.exec_())
    


