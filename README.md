# 🎹 SynesthesiaKeyboard

![App Screenshot](assets/screenshot.png)

An interactive, visually rich musical keyboard application built in Python. 

SynesthesiaKeyboard combines real-time audio playback, music theory generation, and highly customizable visual themes to make exploring and composing music intuitive and engaging.

## ✨ Features

* **🎵 Interactive Playback:** Low-latency audio handling for smooth, responsive keyboard playing.
* **🎼 Music Theory & Generation:** Leverages programmatic music generation to create, analyze, and export tracks and MIDI files.
* **🎨 Optimized Visual Themes:** Beautiful, customizable UI driven by QSS. Theme backgrounds are heavily optimized (reduced from 8MB to ~300KB) for lightning-fast loading without sacrificing quality.
* **💾 User Profiles:** Save custom configurations, progress, and preferences locally using a lightweight JSON structure.
* **🚀 Version Controlled:** Fully managed via Git for stable updates and feature branching.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **UI Framework:** PyQt5 (with QSS for styling)
* **Audio Engine:** `pygame`
* **Music Logic:** `music21`
* **Asset Processing:** `Pillow` (PIL) for on-the-fly image quantization and optimization

## 📂 Project Structure

\`\`\`text
SynesthesiaKeyboard/
├── main.py                 # Application entry point
├── requirements.txt        # Dependency list
├── src/                    # Core logic and widget classes
│   ├── config.py
│   └── widgets.py
└── assets/                 # Static files
    ├── themes/             # Optimized PNG backgrounds
    ├── modes/              # QSS stylesheet files
    ├── profiles/           # User JSON data (Git-ignored by default)
    └── sounds/             # WAV audio files
\`\`\`

## 🚀 Getting Started

### Prerequisites
Make sure you have [Python 3](https://www.python.org/downloads/) and `git` installed on your machine.

### Installation
1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/YOUR_USERNAME/SynesthesiaKeyboard.git
   cd SynesthesiaKeyboard
   \`\`\`

2. Install the required dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. Run the application:
   \`\`\`bash
   python main.py
   \`\`\`

## 📝 License
This project is for educational and personal use.