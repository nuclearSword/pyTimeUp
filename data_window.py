from PyQt6.QtWidgets import  QWidget,QVBoxLayout, QMainWindow, QDateTimeEdit,QLineEdit,QTextEdit,QPushButton,QHBoxLayout,QLabel, QMessageBox,QGroupBox,QScrollArea
from PyQt6.QtCore import QDateTime 
from myPack import Entry


class EditWindow(QMainWindow):
    def __init__(self, entry):
        super().__init__()
        self.entry = entry
        editWidget = QWidget()  # Create a QWidget as the central widget
        editLayout = QVBoxLayout()  # Create a QVBoxLayout for the central widget
        
        self.title = QLineEdit(editWidget)
        self.title.setText(entry.name)

        self.desc = QTextEdit(editWidget)
        self.desc.setText(entry.desc)

        self.start = QDateTimeEdit(editWidget)
        self.start.setDisplayFormat("M/dd/yyyy h:mm:ss AP")
        self.start.setDateTime(QDateTime.fromString(entry.start, "yyyy-MM-dd hh:mm:ss AP"))

        self.end = QDateTimeEdit(editWidget)
        self.end.setDisplayFormat("M/dd/yyyy h:mm:ss AP")
        self.end.setDateTime(QDateTime.fromString(entry.end, "yyyy-MM-dd hh:mm:ss AP"))


        confirmBtn = QPushButton("confirm changes", editWidget)
        confirmBtn.clicked.connect(self.confirm)

        editLayout.addWidget(self.title)
        editLayout.addWidget(self.desc)
        editLayout.addWidget(self.start)
        editLayout.addWidget(self.end)
        editLayout.addWidget(confirmBtn)

        editWidget.setLayout(editLayout)  
        self.setCentralWidget(editWidget)  

    def confirm(self):
        self.entry.name = self.title.text()
        self.entry.desc = self.desc.toPlainText()
        start = self.start.dateTime()
        self.entry.start = start.toString("yyyy-MM-dd hh:mm:ss AP")
        end = self.end.dateTime()
        self.entry.end = end.toString("yyyy-MM-dd hh:mm:ss AP")
        self.entry.duration  = start.secsTo(end)
        QMessageBox.information(self, "Information", "edited!")
        self.entry.widget.deleteLater()
        self.entry.widget = None 
        if self.entry.parent:
            self.entry.parent.widget.add_widget(self.entry)
     
class MoreWindow(QMainWindow):
    def __init__(self, event):
        super().__init__()
        
        moreWidget = QWidget()  # Create a QWidget as the central widget
        moreLayout = QVBoxLayout()  # Create a QVBoxLayout for the central widget
        
        duration = QLabel(str(event.duration))  # Create QLabel for duration
        desc = QLabel(event.desc)  # Create QLabel for description
        
        moreLayout.addWidget(duration)  # Add duration label to the layout
        moreLayout.addWidget(desc)  # Add description label to the layout
        
        moreWidget.setLayout(moreLayout)  # Set the layout for the central widget
        self.setCentralWidget(moreWidget)  #

class GroupWidget(QGroupBox):
    def __init__(self, genre, parent:QWidget|None, main_win) -> None:
        super().__init__(genre.name,parent)
        self.main_win = main_win
        self.genre = genre
        self.parent_widget = parent
        self.setLayout(QVBoxLayout())

        self.setCheckable(True)
        self.setChecked(True)
        self.parent_widget.layout().addWidget(self)

    def add_widget(self, item):
        if isinstance(item,Entry):
            entry_widget = EntryWidget(item.parent.widget,item, self.main_win)
            item.widget = entry_widget
            return
        group_widget = GroupWidget(item,item.parent.widget, self.main_win)
        item.widget = group_widget
        for sub_item in item.items:
            group_widget.add_widget(sub_item)

    def del_widget(self):
        self.deleteLater()
        self.genre.widget = None
        if self.genre.parent is None:
            self.main_win.items.remove(self.genre)
            return
        self.genre.parent.items.remove(self.genre)
        if not self.genre.parent.items:
            self.genre.parent.widget.del_widget()
        
class EntryWidget(QWidget):
    def __init__(self, parent:QWidget|None, entry, main_win) -> None:
        super().__init__(parent)
        self.main_win = main_win
        self.entry = entry
        entryLayout = QHBoxLayout()
        title = QLabel(entry.name, self)
        start = QLabel(entry.start, self)
        end = QLabel(entry.end, self)
        
        editBtn = QPushButton("edit", self)
        editBtn.clicked.connect(self.show_edit_win)
        delBtn = QPushButton("del", self)
        delBtn.clicked.connect(self.del_entry)
        moreBtn = QPushButton("more..", self)
        moreBtn.clicked.connect(self.show_more_window)

        entryLayout.addWidget(title)
        entryLayout.addWidget(start)
        entryLayout.addWidget(end)
        entryLayout.addWidget(editBtn)
        entryLayout.addWidget(delBtn)
        entryLayout.addWidget(moreBtn)
        self.setLayout(entryLayout)
        parent.layout().addWidget(self)
        self.more_window = None
        self.edit_window = None
    
    def show_more_window(self):
        self.more_window = MoreWindow(self.entry)
        self.more_window.show()

    def del_entry(self):
        self.deleteLater()
        self.entry.widget = None
        if self.entry.parent is None:
            self.main_win.items.remove(self.entry)
            return
        
        self.entry.parent.items.remove(self.entry)
        if not self.entry.parent.items:
            self.entry.parent.widget.del_widget()

    def show_edit_win(self):
        self.edit_win = EditWindow(self.entry)
        self.edit_win.show()

class DataWindow(QMainWindow):
    def __init__(self, main_win):
        self.main_win = main_win
        super().__init__()
        self.setWindowTitle("My data")
        self.scrollArea = QScrollArea()
        self.setCentralWidget(self.scrollArea) 

        self.dataWidget = QWidget()
        self.dataLayout = QVBoxLayout()
        self.dataWidget.setLayout(self.dataLayout)
        self.scrollArea.setWidget(self.dataWidget)
        self.populate_data_win(self.main_win.items)

    def add_widget(self, item):
        if isinstance(item,Entry):
            entry_widget = EntryWidget(self.dataWidget,item, self.main_win)
            item.widget = entry_widget
            return
        group_widget = GroupWidget(item,self.dataWidget, self.main_win)
        item.widget = group_widget
        for sub_item in item.items:
            group_widget.add_widget(sub_item)

    def populate_data_win(self, items):
        for item in items:
            self.add_widget(item)
        self.scrollArea.setWidgetResizable(True)
        
        
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                layout.removeWidget(widget)
                widget.deleteLater()
                continue

            sublayout = item.layout()
            if sublayout:
                self.clear_layout(sublayout)   
            sublayout.deleteLater() 

    def update_display(self):   
        self.clear_layout(self.dataLayout)
        self.populate_data_window() 
