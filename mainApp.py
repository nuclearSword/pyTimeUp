
from PyQt6.QtWidgets import QApplication, QWidget,QVBoxLayout, QMainWindow, QDateTimeEdit, QTextEdit,QPushButton,QHBoxLayout, QComboBox, QMessageBox
from PyQt6.QtCore import QDateTime , QThread
from data_window import DataWindow
from myPack import *
import os, time

current_dir =  os.path.dirname(os.path.realpath(__file__))
file = os.path.join(current_dir, 'save.json')

def find_genre(name, items):
    for item in items:
        if isinstance(item, Entry):continue
        if item.name == name:
            return item
    return None

class WorkerThread(QThread):
    def run(self):
        while True:
            print(window.data_window)
            time.sleep(1)


class ForumWidget(QWidget):
    def __init__(self, parent: QWidget | None, main_win) -> None:
        super().__init__(parent)
        self.main_win = main_win
        self.forumLayout = QVBoxLayout()
        titleLayout = QHBoxLayout()
        startLayout = QHBoxLayout()
        endLayout = QHBoxLayout()

        self.title = QComboBox(self)
        self.title.setPlaceholderText("your title...")
        self.title.setEditable(True)
        self.title.addItems([item.name for item in main_win.items])
        self.subTitleBtn= QPushButton("add sub title", self)
        self.subTitleBtn.clicked.connect(self.addSubTitleWidget)
        self.subTitleWidgets = [self.title]

        self.desc = QTextEdit(self)
        self.desc.setPlaceholderText("your descreption...")
      
        self.start = QDateTimeEdit(self)
        self.start.setDisplayFormat("M/dd/yyyy h:mm:ss AP")
        self.startBtn = QPushButton("self.start", self)
        self.startBtn.clicked.connect(self.update_time)
        
        self.end = QDateTimeEdit(self)
        self.end.setDisplayFormat("M/dd/yyyy h:mm:ss AP")
        self.end.setDateTime(QDateTime.currentDateTime())
        self.endBtn = QPushButton("self.end", self)
        self.endBtn.clicked.connect(self.update_time)

        submitBtn = QPushButton("submit", self)
        submitBtn.clicked.connect(self.submit)

        titleLayout.addWidget(self.title)
        titleLayout.addWidget(self.subTitleBtn)
        startLayout.addWidget(self.start)
        startLayout.addWidget(self.startBtn)
        endLayout.addWidget(self.end)
        endLayout.addWidget(self.endBtn)        
        self.forumLayout.addLayout(titleLayout)
        self.forumLayout.addWidget(self.desc)
        self.forumLayout.addLayout(startLayout)
        self.forumLayout.addLayout(endLayout)

        self.forumLayout.addWidget(submitBtn)
        self.setLayout(self.forumLayout)
        self.parent_genre = self.main_win
        self.new_subGenre = True

    def delete_layout(self):
        pass
    
    def addSubTitleWidget(self):
        title = self.subTitleWidgets[-1].currentText()
        if title == "":
            QMessageBox.information(self, "error", "title cant be empty")
            return
        subTitle = QComboBox()
        #check if exists
        if self.new_subGenre:
            result = find_genre(title, self.parent_genre.items)
            if result:
                self.parent_genre = result
                subTitle.addItems([item.name for item in result.items])
            else:
                self.new_subGenre = False

        subTitle.setPlaceholderText("subtitle...")
        subTitle.setEditable(True)
        
        self.forumLayout.insertWidget(len(self.subTitleWidgets),subTitle)
        self.subTitleWidgets.append(subTitle)

    def update_time(self):
        sender = app.sender()
        if sender is self.startBtn:
            self.start.setDateTime(QDateTime.currentDateTime())
            return
        self.end.setDateTime(QDateTime.currentDateTime())
          
    def submit(self):
        start_pos = 0
        parent = find_genre_sequence([x.currentText() for x in self.subTitleWidgets], self.main_win.items)
        if parent:
            for index, item in enumerate(self.subTitleWidgets):
                if item.currentText() != parent.name: continue
                start_pos = index +1
                break 
    
        item = construct_item(self.subTitleWidgets[start_pos:], [self.desc.toPlainText(),self.start.dateTime(),self.end.dateTime()], parent)
        if not parent:
            self.main_win.items.append(item) 
            self.main_win.data_window.add_widget(item)
        else:
            parent.widget.add_widget(parent.items[-1]) 
       
        
        for widget in self.subTitleWidgets[1:]:
            widget.deleteLater()
        self.subTitleWidgets.clear()
        self.subTitleWidgets.append(self.title)

        self.title.clear()
        self.desc.clear()
        self.start.setDateTime(QDateTime.currentDateTime())
        self.end.setDateTime(QDateTime.currentDateTime())
        self.parent_genre = self.main_win
        self.new_subGenre = True

class MyWindows(QMainWindow):
    def __init__(self):
        self.items = read_data(file)
        super(MyWindows, self).__init__()
        
        self.setWindowTitle("My App")
        mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        self.forum_widget = ForumWidget(mainWidget, self)
        dataBtn = QPushButton("data", self)
        dataBtn.clicked.connect(self.showdata)

        self.mainLayout.addWidget(self.forum_widget)
        self.mainLayout.addWidget(dataBtn)

        mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(mainWidget)

        self.data_window = DataWindow(self)
        
        
    def showdata(self):
        if self.data_window.isHidden():
            self.data_window.show()
            return
        self.data_window.hide()

    def remove_item_globally(self, item):
        self.items.remove(item)
        
if __name__ == '__main__':
    app = QApplication([])
    window = MyWindows()
    if window.items:
        entry = get_last_entry(window.items[-1])
        window.forum_widget.start.setDateTime(QDateTime.fromString(entry.end, "yyyy-MM-dd hh:mm:ss AP"))
    else:
        window.forum_widget.start.setDateTime(QDateTime.currentDateTime())

    window.show()
    app.exec()
    save_data(window.items,file)


