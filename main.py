import sys
import os
import glob
import json
import pygame
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QScrollArea, QPushButton, QLabel, QDialog, 
    QGraphicsView, QGraphicsScene, QGraphicsLineItem, QGraphicsTextItem, 
    QMessageBox, QListWidget, QListWidgetItem, QLineEdit, QInputDialog, QRadioButton
)
from PyQt5.QtCore import Qt, QUrl, QStandardPaths, QRectF, QSize
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap, QBrush, QImage, QIcon

try:
    from src import config
    from src.widgets import ColorKey, DraggableSticker, CrayonPalette, PlacedStickerItem
except ImportError:
    sys.path.append(os.path.abspath("src"))
    import config
    from widgets import ColorKey, DraggableSticker, CrayonPalette, PlacedStickerItem

# --- (Keep SoundManager, ProfileManager, ProfileDialog as they were) ---
class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        for char, filename in config.SOUND_MAP.items():
            path = os.path.join(config.SOUNDS_DIR, filename)
            if os.path.exists(path):
                try: self.sounds[char] = pygame.mixer.Sound(path)
                except: pass
    def play(self, char):
        if char in self.sounds: self.sounds[char].play()

class ProfileManager:
    def __init__(self):
        self.current_profile_file = None
        self.data = {}
    def load_profile(self, filename):
        self.current_profile_file = os.path.join(config.PROFILE_DIR, filename)
        if os.path.exists(self.current_profile_file):
            try:
                with open(self.current_profile_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except: self.data = {}
        else: self.data = {}
        return self.data
    def save_profile(self, color_map):
        if not self.current_profile_file: return
        try:
            with open(self.current_profile_file, 'w', encoding='utf-8') as f:
                json.dump(color_map, f, ensure_ascii=False, indent=2)
        except: pass

class ProfileDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.selected_profile = None
        self.selected_lang = "en"
        self.setFixedSize(400, 400)
        self.setProperty("class", "dialog")
        
        self.main_layout = QVBoxLayout(self)
        
        # Language Selector (Top)
        lang_layout = QHBoxLayout()
        lang_layout.setAlignment(Qt.AlignCenter)
        lang_layout.setContentsMargins(0, 33, 0, 33) # Breathing room
        
        self.rb_en = QRadioButton("English")
        self.rb_jp = QRadioButton("にほんご")
        self.rb_pt = QRadioButton("Português")
        self.rb_en.setChecked(True)
        for rb, code in [(self.rb_en, "en"), (self.rb_jp, "jp"), (self.rb_pt, "pt")]:
            rb.toggled.connect(lambda _, c=code: self.set_lang(c))
            lang_layout.addWidget(rb)
        self.main_layout.addLayout(lang_layout)

        self.lbl_select = QLabel()
        self.lbl_select.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.lbl_select)
        
        self.list_widget = QListWidget()
        self.main_layout.addWidget(self.list_widget)

        btn_layout = QHBoxLayout()
        self.btn_new = QPushButton(); self.btn_new.setProperty("class", "btn_action"); self.btn_new.clicked.connect(self.create_new)
        self.btn_load = QPushButton(); self.btn_load.setProperty("class", "btn_action"); self.btn_load.clicked.connect(self.load_selected)
        btn_layout.addWidget(self.btn_new); btn_layout.addWidget(self.btn_load)
        self.main_layout.addLayout(btn_layout)
        
        self.refresh_texts(); self.refresh_list()

    def tr(self, key): return config.TEXTS.get(key, {}).get(self.selected_lang, "???")
    def set_lang(self, lang_code):
        self.selected_lang = lang_code
        self.refresh_texts(); self.refresh_list()
    def refresh_texts(self):
        self.setWindowTitle(self.tr("dialog_title"))
        self.lbl_select.setText(self.tr("lbl_select"))
        self.btn_new.setText(self.tr("btn_create"))
        self.btn_load.setText(self.tr("btn_start"))
    def refresh_list(self):
        self.list_widget.clear()
        files = sorted(glob.glob(os.path.join(config.PROFILE_DIR, "*.json")))
        for f in files:
            filename_id = os.path.splitext(os.path.basename(f))[0]
            display_name = config.PROFILE_NAMES.get(filename_id, {}).get(self.selected_lang, filename_id)
            item = QListWidgetItem(display_name)
            item.setData(Qt.UserRole, filename_id)
            self.list_widget.addItem(item)
    def create_new(self):
        name, ok = QInputDialog.getText(self, self.tr("input_title"), self.tr("input_msg"))
        if ok and name:
            with open(os.path.join(config.PROFILE_DIR, f"{name}.json"), 'w') as f: json.dump({}, f)
            self.refresh_list()
    def load_selected(self):
        item = self.list_widget.currentItem()
        if item:
            self.selected_profile = f"{item.data(Qt.UserRole)}.json"
            self.accept()
        else: QMessageBox.warning(self, "Select", self.tr("warn_select"))

class PaperView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setAcceptDrops(True)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFocusPolicy(Qt.NoFocus) 
        # Note: NoFocus here prevents click-focus, but ScrollAreas are the real danger
        
    def dragEnterEvent(self, e): e.accept() if e.mimeData().hasText() else e.ignore()
    def dragMoveEvent(self, e): e.accept()
    def dropEvent(self, e):
        if e.mimeData().hasText():
            item = PlacedStickerItem(e.mimeData().text())
            item.setZValue(4)
            item.setPos(self.mapToScene(e.pos()))
            self.scene().addItem(item)
            e.accept()
            # FIX: Ensure focus returns to Main Window after drop
            if self.parent(): self.parent().setFocus()

class MainWindow(QMainWindow):
    def __init__(self, profile_manager, lang="en"):
        super().__init__()
        self.pm = profile_manager; self.sm = SoundManager(); self.lang = lang
        self.setWindowTitle(f"Synesthetic Keyboard ({lang})")
        self.setMinimumSize(1200, 800)
        self.setProperty("class", "mainwindow")
        
        self.mode = "setting"
        self.color_map = self.pm.data
        self.text_buffer = []; self.cursor_index = 0
        self.cursor_item = None
        
        self.theme_modes = config.THEME_ORDER
        self.current_css_idx = 0 
        
        self.init_ui()
        self.apply_theme()
        self.set_mode("setting")
        self.setFocus()

    def tr(self, key): return config.TEXTS.get(key, {}).get(self.lang, "???")

    def init_ui(self):
        widget = QWidget(); self.setCentralWidget(widget)
        self.main_layout = QVBoxLayout(widget)
        
        # --- Top Bar ---
        top = QHBoxLayout()
        self.btn_color = QPushButton(self.tr("btn_color")); self.btn_color.clicked.connect(lambda: self.set_mode("setting"))
        self.btn_write = QPushButton(self.tr("btn_write")); self.btn_write.clicked.connect(lambda: self.set_mode("writing"))
        self.btn_bgm = QPushButton(self.tr("btn_bgm")); self.btn_bgm.clicked.connect(self.open_bgm)
        self.btn_mode = QPushButton(self.tr("btn_mode")); self.btn_mode.clicked.connect(self.cycle_theme)
        
        for b in [self.btn_color, self.btn_write, self.btn_bgm, self.btn_mode]:
            b.setFixedSize(160, 45); b.setProperty("class", "topbar"); b.setFocusPolicy(Qt.NoFocus); top.addWidget(b)
        self.main_layout.addLayout(top)

        # --- Workspace ---
        self.ws = QWidget(); ws_layout = QHBoxLayout(self.ws)
        
        # Themes (Left)
        left = QVBoxLayout()
        self.btn_prev = QPushButton(self.tr("btn_preview")); self.btn_prev.setProperty("class", "btn_action")
        self.btn_prev.setFixedSize(140, 50); self.btn_prev.clicked.connect(self.open_preview); self.btn_prev.setFocusPolicy(Qt.NoFocus)
        left.addWidget(self.btn_prev); left.addWidget(QLabel(self.tr("lbl_theme")))
        
        scroll = QScrollArea() 
        scroll.setFixedWidth(140); scroll.setWidgetResizable(True); scroll.setProperty("class", "dock")
        scroll.setFocusPolicy(Qt.NoFocus) # <--- CRITICAL FIX: Prevent scroll area from stealing arrow keys
        
        cont = QWidget(); cont.setAttribute(Qt.WA_StyledBackground, True); v = QVBoxLayout(cont); v.setAlignment(Qt.AlignHCenter); v.setSpacing(15)
        for f in sorted(glob.glob(os.path.join(config.THEME_DIR, "*.png"))):
            n = os.path.splitext(os.path.basename(f))[0]
            btn = QPushButton(); btn.setFixedSize(110, 80); btn.setProperty("class", "thumb")
            btn.setIcon(QIcon(QPixmap(f))); btn.setIconSize(QSize(110, 80)); btn.setStyleSheet("border: none; background: transparent; outline: none;")
            btn.clicked.connect(lambda _, x=n: self.change_theme(x)); v.addWidget(btn)
        v.addStretch(); scroll.setWidget(cont); left.addWidget(scroll); ws_layout.addLayout(left)

        # Paper (Center)
        self.scene = QGraphicsScene(0, 0, config.PAPER_W, config.PAPER_H)
        self.view = PaperView(self.scene, self) # Pass self as parent
        self.view.setFixedSize(config.PAPER_W+4, config.PAPER_H+4)
        ws_layout.addWidget(self.view)

        # Stickers (Right)
        right = QVBoxLayout(); right.addWidget(QLabel(self.tr("lbl_sticker")))
        
        s_scroll = QScrollArea() 
        s_scroll.setFixedWidth(160); s_scroll.setWidgetResizable(True); s_scroll.setProperty("class", "dock")
        s_scroll.setFocusPolicy(Qt.NoFocus) # <--- CRITICAL FIX
        
        s_cont = QWidget(); s_cont.setAttribute(Qt.WA_StyledBackground, True); g = QGridLayout(s_cont)
        r, c = 0, 0
        for s in config.STICKERS:
            g.addWidget(DraggableSticker(s), r, c); c+=1; (c>1) and (setattr(sys.modules[__name__], 'c', 0) or setattr(sys.modules[__name__], 'r', r+1)); (c>1) and (setattr(sys.modules[__name__], 'c', 0) or setattr(sys.modules[__name__], 'r', r+1)); 
            if c>1: c=0; r+=1
        s_scroll.setWidget(s_cont); right.addWidget(s_scroll); ws_layout.addLayout(right)
        self.main_layout.addWidget(self.ws)

        # --- Keyboard ---
        self.kb_container_widget = QWidget()
        self.kb_con = QHBoxLayout(self.kb_container_widget)
        
        # Tabs
        tabs = QVBoxLayout()
        self.tabs = ["hira", "hira_plus", "kata", "kata_plus", "eng_upper", "eng_lower", "num"]
        self.tab_labels = ["あ","あ+","ア","ア+","A","a", "1"] 
        self.tab_btns = {}
        for i, t in enumerate(self.tabs):
            l = self.tab_labels[i]
            b = QPushButton(l); b.setFixedSize(50, 40); b.setProperty("class", "tab"); b.setFocusPolicy(Qt.NoFocus)
            b.clicked.connect(lambda _, x=t: self.load_kb(x)); tabs.addWidget(b); self.tab_btns[t] = b
        tabs.addStretch(); self.kb_con.addLayout(tabs)
        
        # Grid
        ks = QScrollArea()
        ks.setWidgetResizable(True); kw = QWidget(); self.kb_grid = QGridLayout(kw)
        ks.setFocusPolicy(Qt.NoFocus) # <--- CRITICAL FIX
        self.kb_grid.setAlignment(Qt.AlignCenter); ks.setWidget(kw); self.kb_con.addWidget(ks)
        
        # Punctuation (Right Column)
        spec = QVBoxLayout()
        spec.setAlignment(Qt.AlignCenter) # Center vertically relative to keyboard
        spec.setContentsMargins(10, 0, 10, 0) # "Diminishing Area": Add padding left/right
        spec.setSpacing(15) # Add space between buttons
        
        for k in config.SPECIAL_KEYS:
            if k in ["Space", "Back", "Enter"]: continue 
            b = QPushButton(k); b.setFixedSize(60, 45); b.setProperty("class", "special"); b.setFocusPolicy(Qt.NoFocus)
            b.clicked.connect(lambda _, x=k: self.type(x))
            spec.addWidget(b)
        
        self.kb_con.addLayout(spec)
        
        self.main_layout.addWidget(self.kb_container_widget)
        self.load_kb("hira")

    def cycle_theme(self):
        self.current_css_idx = (self.current_css_idx + 1) % len(self.theme_modes)
        self.apply_theme()
        
    def apply_theme(self):
        mode_key = self.theme_modes[self.current_css_idx]
        qss_path = os.path.join(config.MODES_DIR, f"{mode_key}.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r", encoding="utf-8") as f:
                QApplication.instance().setStyleSheet(f.read())
        theme_label = config.THEME_NAMES.get(mode_key, {}).get(self.lang, mode_key)
        self.btn_mode.setText(f"{self.tr('btn_mode')} ({theme_label})")
        self.set_mode(self.mode)

    def set_mode(self, m):
        self.mode = m
        self.btn_color.setProperty("active", m=="setting"); self.btn_write.setProperty("active", m=="writing")
        for b in [self.btn_color, self.btn_write, self.btn_bgm, self.btn_mode]:
            b.style().unpolish(b); b.style().polish(b)

        if m == "setting":
            self.ws.hide(); self.kb_container_widget.show()
        else: 
            self.ws.show(); self.kb_container_widget.show(); self.render()
            
        self.setFocus() # Force focus back to window

    def keyPressEvent(self, event):
        if self.mode == "writing":
            if event.key() == Qt.Key_Left: self.move_cursor(-1)
            elif event.key() == Qt.Key_Right: self.move_cursor(1)
            elif event.key() == Qt.Key_Up: self.move_cursor(-15)
            elif event.key() == Qt.Key_Down: self.move_cursor(15)
            elif event.key() == Qt.Key_Backspace: self.backspace()
            elif event.key() == Qt.Key_Space: self.type(" ")
            elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter: self.type("\n")

    def load_kb(self, layout):
        for i in reversed(range(self.kb_grid.count())): self.kb_grid.itemAt(i).widget().setParent(None)
        for k,b in self.tab_btns.items(): 
            b.setProperty("active", k==layout); b.style().unpolish(b); b.style().polish(b)
        chars = config.LAYOUTS_ENG[layout] if "eng" in layout or "num" in layout else []
        if chars:
            r, c = 0, 0
            for char in chars:
                k = ColorKey(char); k.clicked.connect(lambda _,x=char: self.handle(x))
                if char in self.color_map: k.set_synesthesia_color(self.color_map[char])
                self.kb_grid.addWidget(k, r, c); c+=1; (c>=10) and (setattr(sys.modules[__name__], 'c', 0) or setattr(sys.modules[__name__], 'r', r+1)); (c>=10) and (setattr(sys.modules[__name__], 'c', 0) or setattr(sys.modules[__name__], 'r', r+1)); 
                if c>=10: c=0; r+=1
        else:
            cols = config.LAYOUTS_JP[layout]
            for ci, col_d in enumerate(cols):
                for ri, char in enumerate(col_d):
                    if char:
                        k = ColorKey(char); k.clicked.connect(lambda _,x=char: self.handle(x))
                        if char in self.color_map: k.set_synesthesia_color(self.color_map[char])
                        self.kb_grid.addWidget(k, ri, len(cols)-1-ci)

    def handle(self, c):
        if self.mode == "setting": self.modal_color(c)
        else: self.type(c)

    def type(self, c):
        self.sm.play(c)
        self.text_buffer.insert(self.cursor_index, {'char': c, 'color': self.color_map.get(c, "#000")})
        self.cursor_index += 1; self.render()

    def backspace(self):
        if self.cursor_index > 0: self.text_buffer.pop(self.cursor_index-1); self.cursor_index-=1; self.render()

    def move_cursor(self, delta):
        self.cursor_index += delta
        self.cursor_index = max(0, min(self.cursor_index, len(self.text_buffer)))
        self.render()

    def render(self):
        for i in self.scene.items(): 
            if isinstance(i, (QGraphicsTextItem, QGraphicsLineItem)) and not isinstance(i, PlacedStickerItem): self.scene.removeItem(i)
        
        self.cursor_item = None 
        x, y = 20, 20; font = QFont("Hiragino Sans", 24)
        for i, d in enumerate(self.text_buffer):
            if i==self.cursor_index and self.mode=="writing": 
                self.cursor_item = self.scene.addLine(x, y, x, y+30, QColor("red"))
                self.cursor_item.setZValue(3)
            c = d['char']
            if c == '\n': x=20; y+=40; continue
            s = self.scene.addText(c, font); s.setDefaultTextColor(QColor(200,200,200)); s.setPos(x+2, y+2); s.setZValue(1)
            t = self.scene.addText(c, font); t.setDefaultTextColor(QColor(d['color'])); t.setPos(x, y); t.setZValue(2)
            x += t.boundingRect().width()
            if x > config.PAPER_W-40: x=20; y+=40
            
        if self.cursor_index == len(self.text_buffer) and self.mode=="writing": 
            self.cursor_item = self.scene.addLine(x, y, x, y+30, QColor("red"))
            self.cursor_item.setZValue(3)

    def modal_color(self, char):
        d = QDialog(self); d.setWindowTitle(f"{self.tr('modal_color')}{char}"); d.setFixedSize(400, 500)
        l = QVBoxLayout(d); p = QLabel(char); p.setAlignment(Qt.AlignCenter); p.setFont(QFont("Hiragino Sans", 90))
        p.setStyleSheet(f"color: {self.color_map.get(char, '#000')}"); l.addWidget(p)
        def cb(h): p.setStyleSheet(f"color: {h}"); self.color_map[char]=h; self.pm.save_profile(self.color_map)
        l.addWidget(CrayonPalette(config.CRAYON_COLORS, cb)); b=QPushButton(self.tr("btn_ok")); b.setProperty("class", "btn_action"); b.clicked.connect(d.accept); l.addWidget(b); d.exec_()
        for i in range(self.kb_grid.count()):
            w = self.kb_grid.itemAt(i).widget()
            if isinstance(w, ColorKey) and w.char == char: w.set_synesthesia_color(self.color_map[char])

    def open_bgm(self):
        d = QDialog(self); d.setWindowTitle(self.tr("modal_music")); d.setFixedSize(300, 400); l=QVBoxLayout(d)
        lst = QListWidget(); files = sorted(glob.glob(os.path.join(config.BGM_DIR, "*")))
        for f in files: 
            n = os.path.basename(f); disp = config.BGM_NAMES.get(n, {}).get(self.lang, n)
            it = QListWidgetItem(disp); it.setData(Qt.UserRole, n); lst.addItem(it)
        lst.itemClicked.connect(lambda i: pygame.mixer.music.load(os.path.join(config.BGM_DIR, i.data(Qt.UserRole))) or pygame.mixer.music.play(-1))
        l.addWidget(lst); b=QPushButton(self.tr("btn_stop")); b.setProperty("class", "btn_action"); b.clicked.connect(pygame.mixer.music.stop); l.addWidget(b); d.exec_()

    def change_theme(self, n):
        p = os.path.join(config.THEME_DIR, f"{n}.png")
        if os.path.exists(p): self.scene.setBackgroundBrush(QBrush(QPixmap(p).scaled(config.PAPER_W, config.PAPER_H)))

    def open_preview(self):
        d = QDialog(self); d.setWindowTitle(self.tr("btn_preview")); d.setFixedSize(800, 500); d.setStyleSheet("background: #333"); l=QVBoxLayout(d)
        w, h = int(config.PAPER_W), int(config.PAPER_H)
        
        if self.cursor_item: self.cursor_item.setVisible(False)
        img = QImage(w, h, QImage.Format_ARGB32); img.fill(Qt.transparent)
        p = QPainter(img); self.scene.render(p, QRectF(0,0,w,h), QRectF(0,0,w,h)); p.end()
        if self.cursor_item: self.cursor_item.setVisible(True)
        
        lbl = QLabel(); lbl.setPixmap(QPixmap.fromImage(img)); lbl.setAlignment(Qt.AlignCenter); l.addWidget(lbl)
        
        hl = QHBoxLayout(); bb=QPushButton(self.tr("btn_back")); bb.setProperty("class", "btn_action"); bb.clicked.connect(d.reject); hl.addWidget(bb)
        bs=QPushButton(self.tr("btn_save_copy")); bs.setStyleSheet("background: green; color: white"); bs.setProperty("class", "btn_action")
        def save():
            path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.DownloadLocation), f"Letter_{self.cursor_index}.png")
            if self.cursor_item: self.cursor_item.setVisible(False)
            sw, sh = w*2, h*2
            hi = QImage(sw, sh, QImage.Format_ARGB32); hi.fill(Qt.transparent)
            hp = QPainter(hi); self.scene.render(hp, QRectF(0,0,sw,sh), QRectF(0,0,w,h)); hp.end()
            hi.save(path); QApplication.clipboard().setImage(hi)
            if self.cursor_item: self.cursor_item.setVisible(True)
            QMessageBox.information(d, self.tr("msg_saved_title"), self.tr("msg_saved_body")+path); d.accept()
        bs.clicked.connect(save); hl.addWidget(bs); l.addLayout(hl); d.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    default_qss = os.path.join(config.MODES_DIR, "clean.qss")
    if os.path.exists(default_qss):
        with open(default_qss, "r", encoding="utf-8") as f: app.setStyleSheet(f.read())

    pd = ProfileDialog()
    if pd.exec_() == QDialog.Accepted:
        pm = ProfileManager(); pm.load_profile(pd.selected_profile)
        w = MainWindow(pm, lang=pd.selected_lang); w.show(); sys.exit(app.exec_())