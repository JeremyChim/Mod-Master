import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import config
from UI import untitled
from UI import untitled2
from UI import untitled3


class MainWin(QMainWindow, untitled.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.file_win = None
        self.pushButton.clicked.connect(self.open_file_win)

    def open_file_win(self):
        self.file_win = FileWin(config.npc_file_path)
        self.file_win.show()


class FileWin(QWidget, untitled2.Ui_Form):
    def __init__(self, file_path):
        super().__init__()
        self.setupUi(self)
        self.file_path = file_path
        self.txt_path = None
        self.edited_win = None
        self.model = None
        self.init()

    def init(self):
        self.model = QFileSystemModel(self)
        self.model.setRootPath(self.file_path)
        self.model.setNameFilterDisables(False)
        self.listView.setModel(self.model)
        self.listView.setRootIndex(self.model.index(self.file_path))
        self.pushButton.clicked.connect(self.open_edited_win)
        self.listView.doubleClicked.connect(self.double_click)

    def open_edited_win(self):
        indexes = self.listView.selectedIndexes()
        if indexes:
            index = indexes[0]
            file_name = self.model.fileName(index)
            print(os.path.abspath(file_name))
            self.txt_path = os.path.abspath(file_name)
        if self.txt_path:
            self.edited_win = EditedWin(self.txt_path)
            self.edited_win.show()

    def double_click(self):
        indexes = self.listView.selectedIndexes()
        if indexes:
            index = indexes[0]
            file_name = self.model.fileName(index)
            print(file_name)
            self.txt_path = f'npc/heroes/{file_name}'
        if self.txt_path:
            self.edited_win = EditedWin(self.txt_path)
            self.edited_win.show()


class EditedWin(QWidget, untitled3.Ui_Form):
    def __init__(self, txt_path):
        super().__init__()
        self.setupUi(self)
        self.txt_path = txt_path
        self.init()
        self.show_txt()

    def init(self):
        self.pushButton.clicked.connect(self.show_txt)

    def show_txt(self):
        try:
            with open(self.txt_path, 'r', encoding='utf-8') as f:
                lines: list[str] = f.readlines()
            model = QStringListModel(lines)
            self.listView.setModel(model)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication([])
    win = MainWin()
    win.show()
    app.exec_()
