import sys
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGraphicsTextItem, QGridLayout
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPixmap, QColor
try:
    import config
except ImportError:
    from src import config

class CrayonPalette(QWidget):
    def __init__(self, colors, callback, parent=None):
        super().__init__(parent)
        self.callback = callback
        layout = QGridLayout(self)
        layout.setSpacing(8)
        row, col = 0, 0
        for hex_code in colors:
            btn = QPushButton()
            btn.setFixedSize(35, 35)
            # Tooltip
            color_name = config.JAPANESE_COLORS.get(hex_code, "Unknown")
            btn.setToolTip(color_name)
            # Inline Style (Restored)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {hex_code};
                    border: 2px solid #ddd;
                    border-radius: 17px;
                }}
                QPushButton:hover {{
                    border: 2px solid #333;
                }}
            """)
            btn.clicked.connect(lambda _, c=hex_code: self.callback(c))
            layout.addWidget(btn, row, col)
            col += 1
            if col > 5:
                col = 0; row += 1

class PlacedStickerItem(QGraphicsTextItem):
    def __init__(self, text):
        super().__init__(text)
        self.setDefaultTextColor(QColor("black"))
        font = self.font(); font.setPointSize(45); self.setFont(font)
        self.setFlag(QGraphicsTextItem.ItemIsMovable)
        self.setFlag(QGraphicsTextItem.ItemIsSelectable)
        self.setToolTip("Double-click to remove!")
    def mouseDoubleClickEvent(self, event): self.scene().removeItem(self)

class DraggableSticker(QLabel):
    def __init__(self, char, parent=None):
        super().__init__(parent)
        self.setText(char)
        self.setAlignment(Qt.AlignCenter)
        # Inline Style (Restored)
        self.setStyleSheet("font-size: 35px; border: 2px solid #ddd; border-radius: 10px; background: white;")
        self.setFixedSize(55, 55)
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData(); mime.setText(self.text()); drag.setMimeData(mime)
            pixmap = QPixmap(self.size()); self.render(pixmap); drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos())
            drag.exec_(Qt.CopyAction | Qt.MoveAction)

class ColorKey(QPushButton):
    def __init__(self, char, parent=None):
        super().__init__(char, parent)
        self.char = char
        self.setFixedSize(45, 45)
        self.current_color = "#000000"
        self.update_style()
    def set_synesthesia_color(self, hex_color):
        self.current_color = hex_color
        self.update_style()
    def update_style(self):
        # Inline Style (Restored)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: white; border: 1px solid #bbb; border-radius: 8px;
                font-size: 20px; color: {self.current_color}; font-weight: bold;
            }}
            QPushButton:pressed {{ background-color: #eee; }}
        """)