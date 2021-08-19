import sys
import PyQt5.QtWidgets as pyqt

from node_editor_wnd import NodeEditorWnd


if __name__ == '__main__':
    app = pyqt.QApplication(sys.argv)

    wnd = NodeEditorWnd()

    sys.exit(app.exec_())