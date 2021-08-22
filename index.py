import sys
from PyQt5.QtWidgets import QApplication

from node_editor_wnd import NodeEditorWnd

# credit to
# https://www.youtube.com/playlist?list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz
# for extensive tutorial on node-editor in qtpy

if __name__ == '__main__':
    app = QApplication(sys.argv)

    wnd = NodeEditorWnd()

    sys.exit(app.exec_())