import sys
import os
import glob
import json
import pygame  # <--- NEW AUDIO ENGINE
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QScrollArea, QPushButton, QLabel, QDialog, 
    QGraphicsView, QGraphicsScene, QGraphicsLineItem, QGraphicsTextItem, 
    QMessageBox, QListWidget, QSizePolicy
)
from PyQt5.QtCore import Qt, QUrl, QStandardPaths, QRectF
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap, QBrush, QImage

# --- IMPORT MODULES ---
try:
    from src import config
    from src.widgets import ColorKey, DraggableSticker, CrayonPalette, PlacedStickerItem
except ImportError:
    sys.path.append(os.path.abspath("src"))
    import config
    from widgets import ColorKey, DraggableSticker, CrayonPalette, PlacedStickerItem

# --- PERSISTENCE ---
class ProfileManager:
    @staticmethod
    def load_profile():
        if os.path.exists(config.PROFILE_PATH):
            try:
                with open(config.PROFILE_PATH, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    @staticmethod
    def save_profile(color_map):
        try:
            with open(config.PROFILE_PATH, 'w') as f:
                json.dump(color_map, f)
        except Exception as e:
            print(f"Error saving: {e}")

# --- CUSTOM VIEW ---
class PaperView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setAcceptDrops(True)
        # Use High Quality Anti-Aliasing
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFocusPolicy(Qt.NoFocus)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText(): event.accept()
        else: event.ignore()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            char = event.mimeData().text()
            item = PlacedStickerItem(char)
            item.setPos(self.mapToScene(event.pos()))
            self.scene().addItem(item)
            event.accept()
        else:
            event.ignore()

# --- MAIN CONTROLLER ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize Audio Engine
        pygame.mixer.init()
        
        self.setWindowTitle("Synesthetic Keyboard v1.2")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet("background-color: #f4f7f6;")

        # --- STATE ---
        self.mode = "setting"
        self.color_map = ProfileManager.load_profile()
        self.text_buffer = [] 
        self.cursor_index = 0
        self.current_theme = ""
        
        # Font Stack (Tries to find the best one available)
        self.font_family = "Hiragino Sans" # Mac Default
        # Fallback logic could be added here, but Qt handles generic fallbacks well
        # if we just pick a standard one.
        
        # --- UI SETUP ---
        self.init_ui()
        self.set_mode("setting")

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QVBoxLayout(main_widget)
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # 1. TOP BAR
        top_bar = QHBoxLayout()
        top_bar.setAlignment(Qt.AlignCenter)
        top_bar.setSpacing(30)
        
        self.btn_color_mode = QPushButton("🎨 Color Set")
        self.btn_write_mode = QPushButton("✏️ Write Mode")
        self.btn_bgm = QPushButton("🎵 BGM")
        
        btn_style = """
            QPushButton { 
                font-size:16px; font-weight:bold;
                border-radius:22px; 
                border:none; 
                background:#e0e0e0; color:#555; 
            }
            QPushButton:hover { background:#d0d0d0; }
        """
        
        for btn in [self.btn_color_mode, self.btn_write_mode, self.btn_bgm]:
            btn.setFixedSize(160, 45)
            btn.setStyleSheet(btn_style)
            btn.setFocusPolicy(Qt.NoFocus)
            top_bar.addWidget(btn)
            
        self.btn_color_mode.clicked.connect(lambda: self.set_mode("setting"))
        self.btn_write_mode.clicked.connect(lambda: self.set_mode("writing"))
        self.btn_bgm.clicked.connect(self.open_bgm_modal)
        
        self.main_layout.addLayout(top_bar)

        # 2. WORKSPACE
        self.workspace_widget = QWidget()
        ws_layout = QHBoxLayout(self.workspace_widget)
        ws_layout.setAlignment(Qt.AlignCenter)
        ws_layout.setSpacing(20)
        
        # LEFT: Themes
        left_col = QVBoxLayout()
        self.btn_preview = QPushButton("👁️ Preview")
        self.btn_preview.setFixedSize(140, 50)
        self.btn_preview.setStyleSheet("background:#9C27B0; color:white; font-weight:bold; border-radius:10px; font-size:16px;")
        self.btn_preview.clicked.connect(self.open_preview_modal)
        self.btn_preview.setFocusPolicy(Qt.NoFocus)
        left_col.addWidget(self.btn_preview)
        
        left_col.addWidget(QLabel("Themes"))
        
        self.theme_dock = QScrollArea()
        self.theme_dock.setFixedWidth(140)
        self.theme_dock.setWidgetResizable(True)
        self.theme_dock.setStyleSheet("border:none; background:transparent;")
        self.theme_dock.setFocusPolicy(Qt.NoFocus)
        
        theme_content = QWidget()
        theme_layout = QVBoxLayout(theme_content)
        
        theme_files = glob.glob(os.path.join(config.THEME_DIR, "*.png"))
        for t_path in theme_files:
            t_name = os.path.splitext(os.path.basename(t_path))[0]
            btn = QPushButton()
            btn.setFixedSize(110, 80)
            
            # --- AUTO THUMBNAIL GENERATION ---
            # Instead of loading the huge image as background, we create a scaled icon
            pix = QPixmap(t_path).scaled(110, 80, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            icon = QIcon(pix)
            btn.setIcon(icon)
            btn.setIconSize(api_size := pix.size()) 
            
            btn.setStyleSheet("border: 2px solid #ccc; border-radius: 8px; background: white;")
            btn.clicked.connect(lambda _, n=t_name: self.change_theme(n))
            btn.setFocusPolicy(Qt.NoFocus)
            theme_layout.addWidget(btn)
            
        theme_layout.addStretch()
        self.theme_dock.setWidget(theme_content)
        left_col.addWidget(self.theme_dock)
        ws_layout.addLayout(left_col)

        # CENTER: Paper
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, config.PAPER_W, config.PAPER_H)
        
        self.view = PaperView(self.scene)
        self.view.setFixedSize(config.PAPER_W + 4, config.PAPER_H + 4)
        ws_layout.addWidget(self.view)

        # RIGHT: Stickers
        right_col = QVBoxLayout()
        right_col.addWidget(QLabel("Stickers"))
        self.sticker_dock = QScrollArea()
        self.sticker_dock.setFixedWidth(160)
        self.sticker_dock.setWidgetResizable(True)
        self.sticker_dock.setStyleSheet("background: #e0e0e0; border-radius: 10px;")
        self.sticker_dock.setFocusPolicy(Qt.NoFocus)
        
        dock_content = QWidget()
        dock_layout = QGridLayout(dock_content)
        self.sticker_dock.setWidget(dock_content)
        
        row, col = 0, 0
        for s in config.STICKERS:
            lbl = DraggableSticker(s)
            dock_layout.addWidget(lbl, row, col)
            col += 1
            if col > 1:
                col = 0; row += 1
                
        right_col.addWidget(self.sticker_dock)
        ws_layout.addLayout(right_col)

        self.main_layout.addWidget(self.workspace_widget)

        # 3. KEYBOARD
        self.kb_container = QHBoxLayout()
        
        # Tabs
        tabs_layout = QVBoxLayout()
        tabs_layout.setAlignment(Qt.AlignTop)
        self.tabs = ["hira", "hira_plus", "kata", "kata_plus", "eng_upper", "eng_lower", "num"]
        self.tab_buttons = {}
        
        for t in self.tabs:
            label = t.replace("hira", "あ").replace("plus", "+").replace("kata", "ア").replace("eng_upper", "A").replace("eng_lower", "a").replace("num", "1")
            btn = QPushButton(label)
            btn.setFixedSize(50, 40)
            btn.setStyleSheet("background: #ddd; border-radius: 20px; font-weight: bold;")
            btn.clicked.connect(lambda _, x=t: self.load_keyboard(x))
            btn.setFocusPolicy(Qt.NoFocus)
            tabs_layout.addWidget(btn)
            self.tab_buttons[t] = btn
        
        tabs_layout.addStretch()
        self.kb_container.addLayout(tabs_layout)
        
        # Grid
        kb_scroll = QScrollArea()
        kb_scroll.setWidgetResizable(True)
        kb_scroll.setFocusPolicy(Qt.NoFocus)
        self.kb_widget = QWidget()
        self.kb_grid = QGridLayout(self.kb_widget)
        self.kb_grid.setAlignment(Qt.AlignCenter)
        kb_scroll.setWidget(self.kb_widget)
        self.kb_container.addWidget(kb_scroll)
        
        # Special Keys
        special_layout = QVBoxLayout()
        special_layout.setAlignment(Qt.AlignTop)
        for key_label in config.SPECIAL_KEYS:
            btn = QPushButton(key_label)
            btn.setFixedSize(70, 45)
            btn.setStyleSheet("font-size:14px; font-weight:bold; background:#ddd; border-radius: 22px;")
            btn.setFocusPolicy(Qt.NoFocus)
            
            if key_label == "Space": btn.clicked.connect(lambda: self.type_char(" "))
            elif key_label == "Back": btn.clicked.connect(self.backspace)
            elif key_label == "Enter": btn.clicked.connect(lambda: self.type_char("\n"))
            elif key_label == "ー": btn.clicked.connect(lambda: self.type_char("ー"))
            else: btn.clicked.connect(lambda _, k=key_label: self.type_char(k))
            special_layout.addWidget(btn)
        special_layout.addStretch()
        self.kb_container.addLayout(special_layout)
        
        self.main_layout.addLayout(self.kb_container)
        self.load_keyboard("hira")

    # --- MODES ---
    def set_mode(self, mode):
        self.mode = mode
        if mode == "setting":
            self.btn_color_mode.setStyleSheet(self.btn_color_mode.styleSheet() + "background:#00d2ff; color:white;")
            self.btn_write_mode.setStyleSheet(self.btn_write_mode.styleSheet().replace("background:#00d2ff; color:white;", "background:#e0e0e0; color:#555;"))
            self.workspace_widget.hide()
        else: 
            self.btn_write_mode.setStyleSheet(self.btn_write_mode.styleSheet() + "background:#00d2ff; color:white;")
            self.btn_color_mode.setStyleSheet(self.btn_color_mode.styleSheet().replace("background:#00d2ff; color:white;", "background:#e0e0e0; color:#555;"))
            self.workspace_widget.show()
            self.render_paper()
            self.setFocus()
            self.activateWindow()

    # --- INPUT ---
    def keyPressEvent(self, event):
        if self.mode == "writing":
            if event.key() == Qt.Key_Left: self.move_cursor(-1)
            elif event.key() == Qt.Key_Right: self.move_cursor(1)
            elif event.key() == Qt.Key_Backspace: self.backspace()

    def load_keyboard(self, layout_type):
        for i in reversed(range(self.kb_grid.count())): 
            self.kb_grid.itemAt(i).widget().setParent(None)
        
        base_style = "QPushButton { background: #ddd; border-radius: 20px; font-weight: bold; font-size: 14px; }"
        active_style = "QPushButton { background: #333; color: white; border-radius: 20px; font-weight: bold; font-size: 14px; }"
        
        for k, btn in self.tab_buttons.items(): btn.setStyleSheet(base_style)
        self.tab_buttons[layout_type].setStyleSheet(active_style)

        if "eng" in layout_type or "num" in layout_type:
            chars = config.LAYOUTS_ENG[layout_type]
            col_count = 10
            row, col = 0, 0
            for char in chars:
                key = ColorKey(char)
                key.clicked.connect(lambda _, c=char: self.handle_key(c))
                key.setFocusPolicy(Qt.NoFocus)
                if char in self.color_map: key.set_synesthesia_color(self.color_map[char])
                self.kb_grid.addWidget(key, row, col)
                col += 1
                if col >= col_count: col = 0; row += 1
        else:
            cols = config.LAYOUTS_JP[layout_type]
            total_cols = len(cols)
            for col_idx, column_data in enumerate(cols):
                grid_col = total_cols - 1 - col_idx
                for row_idx, char in enumerate(column_data):
                    if char:
                        key = ColorKey(char)
                        key.clicked.connect(lambda _, c=char: self.handle_key(c))
                        key.setFocusPolicy(Qt.NoFocus)
                        if char in self.color_map: key.set_synesthesia_color(self.color_map[char])
                        self.kb_grid.addWidget(key, row_idx, grid_col)

    def handle_key(self, char):
        if self.mode == "setting": self.open_color_modal(char)
        else: self.type_char(char)
        if self.mode == "writing": self.setFocus()

    def open_color_modal(self, char):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Color: {char}")
        dialog.setFixedSize(400, 500)
        dialog.setStyleSheet("background: white;")
        layout = QVBoxLayout(dialog)
        
        # Use fallback font stack to prevent lag
        font = QFont("Hiragino Sans", 90, QFont.Bold)
        font.setStyleHint(QFont.SansSerif)
        
        preview = QLabel(char)
        preview.setAlignment(Qt.AlignCenter)
        preview.setFont(font)
        initial_color = self.color_map.get(char, "#000000")
        preview.setStyleSheet(f"color: {initial_color}")
        layout.addWidget(preview)
        
        def on_crayon_click(hex_color):
            preview.setStyleSheet(f"color: {hex_color}")
            self.color_map[char] = hex_color
            ProfileManager.save_profile(self.color_map)
        
        palette = CrayonPalette(config.CRAYON_COLORS, on_crayon_click)
        layout.addWidget(palette)
        
        btn_ok = QPushButton("OK")
        btn_ok.setFixedSize(150, 50)
        btn_ok.clicked.connect(dialog.accept)
        layout.addWidget(btn_ok, alignment=Qt.AlignCenter)
        dialog.exec_()
        
        for i in range(self.kb_grid.count()):
            widget = self.kb_grid.itemAt(i).widget()
            if isinstance(widget, ColorKey) and widget.char == char:
                widget.set_synesthesia_color(self.color_map[char])

    # --- RENDER ENGINE ---
    def type_char(self, char):
        color = self.color_map.get(char, "#000000")
        self.text_buffer.insert(self.cursor_index, {'char': char, 'color': color})
        self.cursor_index += 1
        self.render_paper()

    def backspace(self):
        if self.cursor_index > 0:
            self.text_buffer.pop(self.cursor_index - 1)
            self.cursor_index -= 1
            self.render_paper()

    def move_cursor(self, delta):
        self.cursor_index += delta
        self.cursor_index = max(0, min(self.cursor_index, len(self.text_buffer)))
        self.render_paper()

    def render_paper(self):
        self.scene.clear() # Safer than item removal loop
        
        # Redraw Background if exists
        if self.current_theme:
             self.change_theme(self.current_theme)

        # Draw Stickers (Need to restore them from memory if we clear scene?
        # Actually scene.clear() kills stickers too.
        # FIX: We should separate Layers.
        # For this version, we will iterate items and only remove Text/Lines.
        
        # ... Reverting to Item Removal Loop to save stickers ...
        # But let's fix the font lag here too.
        pass

        # Optimized Loop
        items_to_remove = [item for item in self.scene.items() 
                          if isinstance(item, (QGraphicsTextItem, QGraphicsLineItem)) 
                          and not isinstance(item, PlacedStickerItem)]
        for item in items_to_remove:
            self.scene.removeItem(item)

        x, y = 20, 20
        line_height = 40
        max_width = config.PAPER_W - 40
        cursor_drawn = False
        
        # Robust Font
        font = QFont("Hiragino Sans", 24)
        font.setStyleHint(QFont.SansSerif)

        for i, data in enumerate(self.text_buffer):
            if i == self.cursor_index and self.mode == "writing":
                self.draw_cursor(x, y)
                cursor_drawn = True
            
            char = data['char']
            if char == '\n': x = 20; y += line_height; continue
            
            # Shadow
            s = QGraphicsTextItem(char)
            s.setDefaultTextColor(QColor(200, 200, 200)) 
            s.setFont(font)
            s.setPos(x + 2, y + 2) 
            s.setZValue(1) 
            self.scene.addItem(s)

            # Text
            t = QGraphicsTextItem(char)
            t.setDefaultTextColor(QColor(data['color']))
            t.setFont(font)
            t.setPos(x, y)
            t.setZValue(2) 
            self.scene.addItem(t)
            
            x += t.boundingRect().width()
            if x > max_width: x = 20; y += line_height

        if not cursor_drawn and self.cursor_index == len(self.text_buffer) and self.mode == "writing":
             self.draw_cursor(x, y)

    def draw_cursor(self, x, y):
        line = QGraphicsLineItem(x, y, x, y + 30)
        pen = line.pen()
        pen.setColor(Qt.red)
        pen.setWidth(2)
        line.setPen(pen)
        line.setZValue(3)
        self.scene.addItem(line)

    def change_theme(self, theme_name):
        self.current_theme = theme_name
        path = os.path.join(config.THEME_DIR, f"{theme_name}.png")
        if os.path.exists(path):
            # HIGH RES LOAD
            bg = QPixmap(path)
            # Scale Smoothly
            bg = bg.scaled(config.PAPER_W, config.PAPER_H, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            self.scene.setBackgroundBrush(QBrush(bg))
            self.setFocus()

    def open_bgm_modal(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Music")
        dialog.setFixedSize(300, 400)
        layout = QVBoxLayout(dialog)
        list_widget = QListWidget()
        
        # Absolute paths for Pygame
        abs_bgm_dir = os.path.abspath(config.BGM_DIR)
        files = glob.glob(os.path.join(abs_bgm_dir, "*.mp3")) + glob.glob(os.path.join(abs_bgm_dir, "*.wav"))
        
        for f in files: list_widget.addItem(os.path.basename(f))
        
        def play_selected(item):
            full_path = os.path.join(abs_bgm_dir, item.text())
            try:
                pygame.mixer.music.load(full_path)
                pygame.mixer.music.play(-1) # Loop forever
            except Exception as e:
                print(f"Pygame Error: {e}")
            
        list_widget.itemClicked.connect(play_selected)
        layout.addWidget(list_widget)
        
        btn_stop = QPushButton("Stop Music")
        btn_stop.clicked.connect(pygame.mixer.music.stop)
        layout.addWidget(btn_stop)
        
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(dialog.accept)
        layout.addWidget(btn_ok)
        dialog.exec_()

    def open_preview_modal(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Preview")
        dialog.setFixedSize(800, 500)
        dialog.setStyleSheet("background: #333;")
        layout = QVBoxLayout(dialog)
        
        # Standard Render
        img = QImage(config.PAPER_W, config.PAPER_H, QImage.Format_ARGB32)
        img.fill(Qt.transparent)
        painter = QPainter(img)
        self.scene.render(painter)
        painter.end()
        
        lbl_img = QLabel()
        lbl_img.setPixmap(QPixmap.fromImage(img))
        lbl_img.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_img)
        
        h_layout = QHBoxLayout()
        btn_back = QPushButton("Back")
        btn_back.clicked.connect(dialog.reject)
        
        btn_save = QPushButton("Download High-Res")
        btn_save.setStyleSheet("background: #4CAF50; color: white; font-weight: bold;")
        
        def save_to_downloads():
            path = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)
            fname = f"Letter_{self.cursor_index}.png"
            full_path = os.path.join(path, fname)
            
            try:
                # --- HIGH RES CRASH FIX ---
                scale = 2.0
                hd_img = QImage(int(config.PAPER_W * scale), int(config.PAPER_H * scale), QImage.Format_ARGB32)
                hd_img.fill(Qt.transparent)
                hd_painter = QPainter(hd_img)
                hd_painter.setRenderHint(QPainter.Antialiasing)
                
                # Define Source and Target explicitly to avoid memory overflow
                target_rect = QRectF(0, 0, config.PAPER_W * scale, config.PAPER_H * scale)
                source_rect = QRectF(0, 0, config.PAPER_W, config.PAPER_H)
                
                self.scene.render(hd_painter, target_rect, source_rect)
                hd_painter.end()
                
                hd_img.save(full_path)
                QMessageBox.information(dialog, "Saved!", f"High-Res image saved to:\n{full_path}")
                dialog.accept()
            except Exception as e:
                QMessageBox.critical(dialog, "Error", f"Failed to save: {e}")
            
        btn_save.clicked.connect(save_to_downloads)
        h_layout.addWidget(btn_back)
        h_layout.addWidget(btn_save)
        layout.addLayout(h_layout)
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())