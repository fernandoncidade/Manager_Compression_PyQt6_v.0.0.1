from PyQt6.QtWidgets import QListWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QDragMoveEvent


class DragDropListWidget(QListWidget):
    def __init__(self, parent=None, accept_folders_only=False):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.accept_folders_only = accept_folders_only

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()

            urls = event.mimeData().urls()
            for url in urls:
                file_path = url.toLocalFile()

                if self.accept_folders_only and not self._is_directory(file_path):
                    continue

                exists = False
                for i in range(self.count()):
                    if self.item(i).text() == file_path:
                        exists = True
                        break

                if not exists:
                    self.addItem(file_path)

        else:
            event.ignore()

    def _is_directory(self, path):
        import os
        return os.path.isdir(path)
