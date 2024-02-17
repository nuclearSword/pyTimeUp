import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QScrollArea, QWidget, QVBoxLayout, QLabel

class ScrollableWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Scrollable Widget")

        # Create a QScrollArea widget and set it as the central widget
        self.scrollArea = QScrollArea()
        self.setCentralWidget(self.scrollArea)

        # Create a widget to hold your data
        self.dataWidget = QWidget()
        self.dataLayout = QVBoxLayout(self.dataWidget)  # Assign layout to dataWidget
        self.dataWidget.setLayout(self.dataLayout)

        # Set dataWidget as the widget inside the QScrollArea
        self.scrollArea.setWidget(self.dataWidget)

        # Populate the data window with labels
        self.populate_data_win()

    def populate_data_win(self):
        # Populate the data window with labels
        for i in range(10):
            label = QLabel(f"Label {i}")
            self.dataLayout.addWidget(label)

        # Set the widget inside the QScrollArea to be resizable
        self.scrollArea.setWidgetResizable(True)

        # Set a minimum size for the widget inside the QScrollArea
        self.dataWidget.setMinimumSize(200, 500)  # Adjust the size as needed

def main():
    app = QApplication(sys.argv)
    window = ScrollableWidget()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
