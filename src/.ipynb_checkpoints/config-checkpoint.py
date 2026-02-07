import os
import sys

# --- PATHS ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR) 

ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
THEME_DIR = os.path.join(ASSETS_DIR, 'themes')
MODES_DIR = os.path.join(ASSETS_DIR, 'modes')
BGM_DIR = os.path.join(ASSETS_DIR, 'bgm')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')
PROFILE_DIR = os.path.join(ASSETS_DIR, 'profiles')

for d in [ASSETS_DIR, THEME_DIR, MODES_DIR, BGM_DIR, SOUNDS_DIR, PROFILE_DIR]:
    os.makedirs(d, exist_ok=True)

# Dimensions
WINDOW_W, WINDOW_H = 800, 800
PAPER_W, PAPER_H = 500, 250

# Sticker List
STICKERS = ["🦄","🌈","✨","🍄","🐞","🌸","⭐","🎵","❤️","🚀","🐱","🐶","🍦","🎈","🎂", "👻", "🎃", "🚗", "✈️", "🦕"]

# --- TRANSLATION DICTIONARY ---
TEXTS = {
    # Start Dialog
    "dialog_title": {
        "en": "Who is playing?",
        "jp": "だれがあそぶ？",
        "pt": "Quem vai brincar?"
    },
    "lbl_select": {
        "en": "Select your profile:",
        "jp": "プロファイルをえらんでね:",
        "pt": "Selecione seu perfil:"
    },
    "btn_create": {
        "en": "Create New",
        "jp": "あたらしくつくる",
        "pt": "Criar Novo"
    },
    "btn_start": {
        "en": "Start!",
        "jp": "スタート！",
        "pt": "Começar!"
    },
    "input_title": {
        "en": "New Profile",
        "jp": "あたらしいプロファイル",
        "pt": "Novo Perfil"
    },
    "input_msg": {
        "en": "Enter Name:",
        "jp": "なまえをいれてね:",
        "pt": "Digite o Nome:"
    },
    "warn_select": {
        "en": "Please select a profile!",
        "jp": "プロファイルをえらんでください！",
        "pt": "Por favor selecione um perfil!"
    },

    # Main Window Top Bar
    "btn_color": {
        "en": "🎨 Color Set",
        "jp": "🎨 いろあそび",
        "pt": "🎨 Cores"
    },
    "btn_write": {
        "en": "✏️ Write Mode",
        "jp": "✏️ かいてみよう",
        "pt": "✏️ Escrever"
    },
    "btn_bgm": {
        "en": "🎵 BGM",
        "jp": "🎵 おんがく",
        "pt": "🎵 Música"
    },
    "btn_mode":{
        "en": "🎨 Mode",
        "jp": "🎨 きせかえ",
        "pt": "🎨 Modo"},

    # Main Window Tools
    "lbl_theme": {
        "en": "Themes",
        "jp": "はいけい",
        "pt": "Temas"
    },
    "btn_preview": {
        "en": "👁️ Preview",
        "jp": "👁️ みてみる",
        "pt": "👁️ Ver"
    },
    "lbl_sticker": {
        "en": "Stickers",
        "jp": "シール",
        "pt": "Adesivos"
    },

    # Modals & Messages
    "modal_color": {
        "en": "Color: ",
        "jp": "いろ: ",
        "pt": "Cor: "
    },
    "modal_music": {
        "en": "Select Music",
        "jp": "おんがくをえらぶ",
        "pt": "Escolher Música"
    },
    "btn_stop": {
        "en": "Stop Music",
        "jp": "とめる",
        "pt": "Parar Música"
    },
    "btn_ok": {
        "en": "OK",
        "jp": "OK",
        "pt": "OK"
    },
    "btn_back": {
        "en": "Back",
        "jp": "もどる",
        "pt": "Voltar"
    },
    "btn_save_copy": {
        "en": "Download",
        "jp": "ダウンロード",
        "pt": "Baixar"
    },
    "msg_saved_title": {
        "en": "Saved & Copied!",
        "jp": "ほぞんしました！",
        "pt": "Salvo e Copiado!"
    },
    "msg_saved_body": {
        "en": "Download complete! Image has been copied to the dashboard so you can paste it whenever you want! :)\n\nSaved to: ",
        "jp": "ダウンロードかんりょう！ クリップボードにコピーしたよ。すきなところにはりつけてね！ :)\n\nほぞんさき: ",
        "pt": "Download completo! A imagem foi copiada para a área de transferência para você colar onde quiser! :)\n\nSalvo em: "
    }
}

# Map filename (without extension) -> Display Name
PROFILE_NAMES = {
    "unicorn": {
        "en": "Unicorn",
        "jp": "ユニコーン",
        "pt": "Unicórnio"
    },
    "rainbow": {
        "en": "Rainbow",
        "jp": "にじ",
        "pt": "Arco-íris"
    },
    "nature": {
        "en": "Nature",
        "jp": "しぜん",
        "pt": "Natureza"
    }
}

# Map filename (WITH extension) -> Display Name
BGM_NAMES = {
    "01_earth_root.wav": {
        "en": "Earth",
        "jp": "だいち",
        "pt": "Terra"
    },
    "02_flow_state.wav": {
        "en": "Flowing",
        "jp": "ながれ",
        "pt": "Fluindo"
    },
    "03_solar_clarity.mp3": {
        "en": "Clarity",
        "jp": "ひかり",
        "pt": "Claridade"
    },
    "04_cloud_dream.mp3": {
        "en": "Dream",
        "jp": "ゆめ",
        "pt": "Sonho"
    }
    # Add your real BGM filenames here!
}

# These keys match the filenames: clean.qss, dark.qss...
THEME_NAMES = {
    "clean":  {"en": "Clean",  "jp": "シンプル", "pt": "Limpo"},
    "dark":   {"en": "Dark",   "jp": "ダーク",   "pt": "Escuro"},
    "sepia":  {"en": "Sepia",  "jp": "セピア",   "pt": "Sépia"},
    "ice":    {"en": "Ice",    "jp": "アイス",   "pt": "Gelo"},
    "pastel": {"en": "Pastel", "jp": "パステル", "pt": "Pastel"}
}

# The order to cycle through
THEME_ORDER = ["clean", "dark", "sepia", "ice", "pastel"]

# --- JAPANESE TRADITIONAL COLORS ---
JAPANESE_COLORS = {
    "#f5b1aa": "珊瑚色 さんごいろ",
    "#e198b4": "桃花色 ももはないろ",
    "#e95295": "躑躅色 つつじいろ",
    "#d7003a": "紅 くれない",
    "#b7282e": "茜色 あかねいろ",
    "#b94047": "臙脂 えんじ",

    "#eb6101": "朱色 しゅいろ",
    "#f08300": "蜜柑色 みかんいろ",
    "#f8b500": "山吹色 やまぶきいろ",
    "#ffd900": "蒲公英色 たんぽぽいろ",
    "#ffec47": "菜の花色 なのはないろ",
    "#fddea5": "蜂蜜色 はちみついろ",

    "#a8bf93": "山葵色 わさびいろ",
    "#68be8d": "若竹色 わかたけいろ",
    "#c3d825": "若草色 わかくさいろ",
    "#007b43": "常磐色 ときわいろ",
    "#69821b": "苔色 こけいろ",
    "#928c36": "鶯色 うぐいすいろ",

    "#bce2e8": "水色 みずいろ",
    "#a0d8ef": "空色 そらいろ",
    "#4c6cb3": "群青色 ぐんじょういろ",
    "#1e50a2": "瑠璃色 るりいろ",
    "#165e83": "藍色 あいいろ",
    "#223a70": "紺色 こんいろ",

    "#bbbcde": "藤色 ふじいろ",
    "#cc7eb1": "菖蒲色 あやめいろ",
    "#5654a2": "桔梗色 ききょういろ",
    "#674196": "菖蒲色 しょうぶいろ",
    "#55295b": "桑の実色 くわのみいろ",
    "#949495": "鼠色 ねずみいろ",

    "#a19361": "油色 あぶらいろ",
    "#c39143": "黄土色 おうどいろ",
    "#bc763c": "土色 つちいろ",
    "#96514d": "小豆色 あずきいろ",
    "#762f07": "栗色 くりいろ",
    "#2b2b2b": "黒 くろ",
    # "#0d0015": "漆黒 しっこく"
}

CRAYON_COLORS = list(JAPANESE_COLORS.keys())

# --- SOUND MAPPING ---
SOUND_MAP = {
    # --- JAPANESE (GOJUON) ---
    'あ': 'あ.wav', 'ア': 'あ.wav', 'ぁ': 'あ.wav', 'ァ': 'あ.wav',
    'い': 'い.wav', 'イ': 'い.wav', 'ぃ': 'い.wav', 'ィ': 'い.wav',
    'う': 'う.wav', 'ウ': 'う.wav', 'ぅ': 'う.wav', 'ゥ': 'う.wav',
    'え': 'え.wav', 'エ': 'え.wav', 'ぇ': 'え.wav', 'ェ': 'え.wav',
    'お': 'お.wav', 'オ': 'お.wav', 'ぉ': 'お.wav', 'ォ': 'お.wav',

    'か': 'か.wav', 'カ': 'か.wav',
    'き': 'き.wav', 'キ': 'き.wav',
    'く': 'く.wav', 'ク': 'く.wav',
    'け': 'け.wav', 'ケ': 'け.wav',
    'こ': 'こ.wav', 'コ': 'こ.wav',

    'さ': 'さ.wav', 'サ': 'さ.wav',
    'し': 'し.wav', 'シ': 'し.wav',
    'す': 'す.wav', 'ス': 'す.wav',
    'せ': 'せ.wav', 'セ': 'せ.wav',
    'そ': 'そ.wav', 'ソ': 'そ.wav',

    'た': 'た.wav', 'タ': 'た.wav',
    'ち': 'ち.wav', 'チ': 'ち.wav',
    'つ': 'つ.wav', 'ツ': 'つ.wav', 'っ': 'つ.wav', 'ッ': 'つ.wav',
    'て': 'て.wav', 'テ': 'て.wav',
    'と': 'と.wav', 'ト': 'と.wav',

    'な': 'な.wav', 'ナ': 'な.wav',
    'に': 'に.wav', 'ニ': 'に.wav',
    'ぬ': 'ぬ.wav', 'ヌ': 'ぬ.wav',
    'ね': 'ね.wav', 'ネ': 'ね.wav',
    'の': 'の.wav', 'ノ': 'の.wav',

    'は': 'は.wav', 'ハ': 'は.wav',
    'ひ': 'ひ.wav', 'ヒ': 'ひ.wav',
    'ふ': 'ふ.wav', 'フ': 'ふ.wav',
    'へ': 'へ.wav', 'ヘ': 'へ.wav',
    'ほ': 'ほ.wav', 'ホ': 'ほ.wav',

    'ま': 'ま.wav', 'マ': 'ま.wav',
    'み': 'み.wav', 'ミ': 'み.wav',
    'む': 'む.wav', 'ム': 'む.wav',
    'め': 'め.wav', 'メ': 'め.wav',
    'も': 'も.wav', 'モ': 'も.wav',

    'や': 'や.wav', 'ヤ': 'や.wav', 'ゃ': 'や.wav', 'ャ': 'や.wav',
    'ゆ': 'ゆ.wav', 'ユ': 'ゆ.wav', 'ゅ': 'ゆ.wav', 'ュ': 'ゆ.wav',
    'よ': 'よ.wav', 'ヨ': 'よ.wav', 'ょ': 'よ.wav', 'ョ': 'よ.wav',

    'ら': 'ら.wav', 'ラ': 'ら.wav',
    'り': 'り.wav', 'リ': 'り.wav',
    'る': 'る.wav', 'ル': 'る.wav',
    'れ': 'れ.wav', 'レ': 'れ.wav',
    'ろ': 'ろ.wav', 'ロ': 'ろ.wav',

    'わ': 'わ.wav', 'ワ': 'わ.wav',
    'を': 'を.wav', 'ヲ': 'を.wav',
    'ん': 'ん.wav', 'ン': 'ん.wav',

    # --- JAPANESE (DAKUON / HANDAKUON) ---
    'が': 'が.wav', 'ガ': 'が.wav',
    'ぎ': 'ぎ.wav', 'ギ': 'ぎ.wav',
    'ぐ': 'ぐ.wav', 'グ': 'ぐ.wav',
    'げ': 'げ.wav', 'ゲ': 'げ.wav',
    'ご': 'ご.wav', 'ゴ': 'ご.wav',

    'ざ': 'ざ.wav', 'ザ': 'ざ.wav',
    'じ': 'じ.wav', 'ジ': 'じ.wav',
    'ず': 'ず.wav', 'ズ': 'ず.wav',
    'ぜ': 'ぜ.wav', 'ゼ': 'ぜ.wav',
    'ぞ': 'ぞ.wav', 'ゾ': 'ぞ.wav',

    'だ': 'だ.wav', 'ダ': 'だ.wav',
    'ぢ': 'ぢ.wav', 'ヂ': 'ぢ.wav',
    'づ': 'づ.wav', 'ヅ': 'づ.wav',
    'で': 'で.wav', 'デ': 'で.wav',
    'ど': 'ど.wav', 'ド': 'ど.wav',

    'ば': 'ば.wav', 'バ': 'ば.wav',
    'び': 'び.wav', 'ビ': 'び.wav',
    'ぶ': 'ぶ.wav', 'ブ': 'ぶ.wav',
    'べ': 'べ.wav', 'ベ': 'べ.wav',
    'ぼ': 'ぼ.wav', 'ボ': 'ぼ.wav',

    'ぱ': 'ぱ.wav', 'パ': 'ぱ.wav',
    'ぴ': 'ぴ.wav', 'ピ': 'ぴ.wav',
    'ぷ': 'ぷ.wav', 'プ': 'ぷ.wav',
    'ぺ': 'ぺ.wav', 'ペ': 'ぺ.wav',
    'ぽ': 'ぽ.wav', 'ポ': 'ぽ.wav',

    # --- ENGLISH (A-Z) ---
    'A': 'a.wav', 'a': 'a.wav',
    'B': 'b.wav', 'b': 'b.wav',
    'C': 'c.wav', 'c': 'c.wav',
    'D': 'd.wav', 'd': 'd.wav',
    'E': 'e.wav', 'e': 'e.wav',
    'F': 'f.wav', 'f': 'f.wav',
    'G': 'g.wav', 'g': 'g.wav',
    'H': 'h.wav', 'h': 'h.wav',
    'I': 'i.wav', 'i': 'i.wav',
    'J': 'j.wav', 'j': 'j.wav',
    'K': 'k.wav', 'k': 'k.wav',
    'L': 'l.wav', 'l': 'l.wav',
    'M': 'm.wav', 'm': 'm.wav',
    'N': 'n.wav', 'n': 'n.wav',
    'O': 'o.wav', 'o': 'o.wav',
    'P': 'p.wav', 'p': 'p.wav',
    'Q': 'q.wav', 'q': 'q.wav',
    'R': 'r.wav', 'r': 'r.wav',
    'S': 's.wav', 's': 's.wav',
    'T': 't.wav', 't': 't.wav',
    'U': 'u.wav', 'u': 'u.wav',
    'V': 'v.wav', 'v': 'v.wav',
    'W': 'w.wav', 'w': 'w.wav',
    'X': 'x.wav', 'x': 'x.wav',
    'Y': 'y.wav', 'y': 'y.wav',
    'Z': 'z.wav', 'z': 'z.wav',

    # --- NUMBERS (0-9) ---
    '0': '0.wav',
    '1': '1.wav',
    '2': '2.wav',
    '3': '3.wav',
    '4': '4.wav',
    '5': '5.wav',
    '6': '6.wav',
    '7': '7.wav',
    '8': '8.wav',
    '9': '9.wav',
}

# Layouts
LAYOUTS_JP = {
    'hira': [['あ','い','う','え','お'], ['か','き','く','け','こ'], ['さ','し','す','せ','そ'],['た','ち','つ','て','と'], ['な','に','ぬ','ね','の'], ['は','ひ','ふ','へ','ほ'],['ま','み','む','め','も'], ['や','','ゆ','','よ'], ['ら','り','る','れ','ろ'],['わ','','を','','ん']],
    'hira_plus': [['が','ぎ','ぐ','げ','ご'], ['ざ','じ','ず','ぜ','ぞ'], ['だ','ぢ','づ','で','ど'],['ば','び','ぶ','べ','ぼ'], ['ぱ','ぴ','ぷ','ぺ','ぽ'], ['ぁ','ぃ','ぅ','ぇ','ぉ'], ['ゃ','','ゅ','','ょ'], ['っ','','','','']],
    'kata': [['ア','イ','ウ','エ','オ'], ['カ','キ','ク','ケ','コ'], ['サ','シ','ス','セ','ソ'],['タ','チ','ツ','テ','ト'], ['ナ','ニ','ヌ','ネ','ノ'], ['ハ','ヒ','フ','ヘ','ホ'],['マ','ミ','ム','メ','モ'], ['ヤ','','ユ','','ヨ'], ['ラ','リ','ル','レ','ロ'],['ワ','','ヲ','','ン']],
    'kata_plus': [['ガ','ギ','グ','ゲ','ゴ'], ['ザ','ジ','ズ','ゼ','ゾ'], ['ダ','ヂ','ヅ','デ','ド'],['バ','ビ','ブ','ベ','ボ'], ['パ','ピ','プ','ペ','ポ'], ['ァ','ィ','ゥ','ェ','ォ'], ['ャ','','ュ','','ョ'], ['ッ','','','','']]
}

LAYOUTS_ENG = {
    'eng_upper': list("ABCDEFGHIJ KLMNOPQRST UVWXYZ".replace(" ", "")),
    'eng_lower': list("abcdefghij klmnopqrst uvwxyz".replace(" ", "")),
    'num': list("1234567890")
}

SPECIAL_KEYS = ["Space", "Back", "Enter", "。", "、", "！", "？", "ー"]
