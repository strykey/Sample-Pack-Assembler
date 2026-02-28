<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://capsule-render.vercel.app/api?type=waving&color=c8b89a&height=120&section=header&text=Sample%20Pack%20Assembler&fontSize=42&fontColor=0a0a0a&fontAlignY=65&animation=fadeIn&desc=by%20Strykey&descAlignY=85&descSize=16&descColor=0a0a0a"/>
  <source media="(prefers-color-scheme: light)" srcset="https://capsule-render.vercel.app/api?type=waving&color=1a1a1a&height=120&section=header&text=Sample%20Pack%20Assembler&fontSize=42&fontColor=e8e0d0&fontAlignY=65&animation=fadeIn&desc=by%20Strykey&descAlignY=85&descSize=16&descColor=c8b89a"/>
  <img alt="Sample Pack Assembler" src="https://capsule-render.vercel.app/api?type=waving&color=c8b89a&height=120&section=header&text=Sample%20Pack%20Assembler&fontSize=42&fontColor=0a0a0a&fontAlignY=65&animation=fadeIn&desc=by%20Strykey&descAlignY=85&descSize=16&descColor=0a0a0a"/>
</picture>

<br/>

[![Python](https://img.shields.io/badge/Python-3.7+-3572A5?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge&logo=linux&logoColor=white)](https://github.com/strykey/sample-pack-assembler)
[![License](https://img.shields.io/badge/License-Restrictive%20Custom-c0392b?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](./LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-27ae60?style=for-the-badge&logo=semanticrelease&logoColor=white)](https://github.com/strykey/sample-pack-assembler/releases)
[![pywebview](https://img.shields.io/badge/pywebview-4.x-e8e0d0?style=for-the-badge&logo=python&logoColor=black)](https://pywebview.flowrl.com)

<br/>

> *A desktop tool for producers who take their sample packs seriously.*

</div>

---

## What it is

Sample Pack Assembler is a desktop application built for music producers who need to organize, categorize, rename and export their sample collections into clean, structured packs. You drop in a messy folder of kicks, snares, synths and loops, and it comes out the other side sorted, renamed and ready to distribute or sell.

The interface runs in a native desktop window with five distinct visual themes ranging from a dark cinematic noir to a terminal green acid aesthetic. Everything is done locally, nothing leaves your machine.

---

## Screenshots

<div align="center">
<table>
<tr>
<td align="center"><b>Noir</b></td>
<td align="center"><b>Vapor</b></td>
<td align="center"><b>Acid</b></td>
</tr>
<tr>
<td><img src="https://placehold.co/320x200/0a0a0a/e8e0d0?text=Noir+Theme" alt="Noir Theme"/></td>
<td><img src="https://placehold.co/320x200/0d0118/ff71ce?text=Vapor+Theme" alt="Vapor Theme"/></td>
<td><img src="https://placehold.co/320x200/0f1900/b8ff00?text=Acid+Theme" alt="Acid Theme"/></td>
</tr>
</table>
</div>

---

## Features

**Auto-detection** — the app scans every file in your source folder and automatically assigns it to a category based on its filename. Anything with "kick", "bd" or "kck" in the name goes to Kicks. "808", "sub" or "bass" lands in Bass. "loop", "break" or "groove" becomes Loops. There are 57 keyword rules across 14 categories and it handles the overwhelming majority of sample pack naming conventions out of the box.

**Manual override** — every file has a dropdown you can click to reassign it to a different category. You can also select a batch of files and bulk-assign them all at once with two clicks. Nothing is locked in until you build the pack.

**Audio preview on hover** — move your cursor over any card and the sample plays immediately, no click required. It loads from a base64 cache so playback is instant after the first load. Moving away stops it.

**Five themes** — Noir, Vapor, Studio, Lo-Fi and Acid. Each one changes the fonts, colors and border radius of the entire interface. The Vapor theme uses Righteous and Share Tech Mono. The Acid theme renders in Black Ops One and VT323 from Google Fonts. They are genuinely different aesthetics, not just color swaps.

**Naming templates** — before you export you set a naming template using four variables: `{pack}` for the pack name, `{type}` for the category, `{n}` for the padded sequential number, and `{stem}` for the original filename. A live preview shows how the first eight files will be renamed before you commit to anything.

**README generation** — optionally include a `README.txt` in the root of your assembled pack. You write whatever you want in the text area: licensing terms, BPM, key, your artist name.

**One-click assembly** — pick an output folder, hit the button, and the app builds the entire directory structure, copies every file into its category subfolder with the new name applied, and reports back with the total file count, pack size and a list of every folder created.

---

## Installation

```bash
git clone https://github.com/strykey/sample-pack-assembler.git
cd sample-pack-assembler
pip install -r requirements.txt
python main.py
```

**Dependencies**

```
pywebview>=4.0
```

That is the entire dependency list. The UI is self-contained HTML and JavaScript embedded in the Python file. No build step, no frontend toolchain, no webpack. You install one package and run one file.

---

## How it works

When you click Scan, the app walks your source folder recursively and collects every file with a recognized audio or image extension. Audio formats include `.wav`, `.mp3`, `.aiff`, `.aif`, `.flac`, `.ogg` and `.mid`. Image files (artwork) are detected separately and automatically assigned to an Artwork folder.

Each file is run through a keyword matching function against a dictionary of 14 categories. The detection is case-insensitive and matches anywhere in the filename, so `Tight_Snare_01.wav`, `snr_tight.wav` and `MY_SNARE.wav` all land in Snares.

The organize view gives you a grid of cards filtered by category and searchable in real time. The assemble view handles naming templates, README options and the final export.

During assembly, the app rebuilds the output folder from scratch each time, copies every file to its destination with the new name applied, and writes the README if enabled. The original source files are never touched.

---

## Supported formats

| Type | Extensions |
|---|---|
| Audio | `.wav` `.mp3` `.aiff` `.aif` `.flac` `.ogg` |
| MIDI | `.mid` `.midi` |
| Artwork | `.png` `.jpg` `.jpeg` `.webp` |

---

## Categories

`Kicks` `Snares` `Hi-Hats` `Claps` `Percs` `Bass` `Synths` `Leads` `Pads` `Chords` `Loops` `Vocals` `FX` `MIDI` `Misc` `Artwork`

---

## Naming template variables

| Variable | Value |
|---|---|
| `{pack}` | The pack name you entered in the sidebar |
| `{type}` | The category assigned to the file |
| `{n}` | Two-digit sequential number per category (01, 02…) |
| `{stem}` | Original filename without extension |

**Examples**

`{type}_{n}_{stem}` → `Kicks_01_HardKick.wav`

`{pack}_{type}_{n}` → `MyPack_Kicks_01.wav`

`{stem}` → `HardKick.wav` (preserves original name)

---

## Themes

| Theme | Vibe | Primary Font |
|---|---|---|
| Noir | Dark cinema, cream and black | Playfair Display |
| Vapor | Purple and pink, vaporwave | Righteous |
| Studio | Light, cream paper and orange | Bebas Neue |
| Acid | Terminal green on black | Black Ops One |
| Lo-Fi | Warm brown, candlelight | Abril Fatface |

---

## Project structure

```
sample-pack-assembler/
├── main.py            # Application entry point, Python backend + embedded HTML/JS
├── requirements.txt   # Single dependency: pywebview
├── README.md          # This file
├── LICENSE            # Restrictive custom license
└── CHANGELOG.md       # Version history
```

---

## Author

**Strykey** — made with ♥

---

<div align="center">

[![Made by Strykey](https://img.shields.io/badge/made%20by-Strykey-c8b89a?style=for-the-badge)](https://github.com/strykey)
[![Stars](https://img.shields.io/github/stars/strykey/sample-pack-assembler?style=for-the-badge&color=e8e0d0)](https://github.com/strykey/sample-pack-assembler/stargazers)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://capsule-render.vercel.app/api?type=waving&color=c8b89a&height=80&section=footer"/>
  <img alt="footer" src="https://capsule-render.vercel.app/api?type=waving&color=c8b89a&height=80&section=footer"/>
</picture>

</div>