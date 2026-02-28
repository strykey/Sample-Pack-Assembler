<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0a0a0a,60:1a1208,100:c8b89a&height=200&section=header&text=Sample%20Pack%20Assembler&fontSize=46&fontColor=f5f0e8&fontAlignY=55&animation=fadeIn" width="100%"/>

<br/>

[![Python](https://img.shields.io/badge/Python-3.7+-3572A5?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Win%20%7C%20Mac%20%7C%20Linux-555555?style=for-the-badge&logo=linux&logoColor=white)](https://github.com/strykey/sample-pack-assembler)
[![License](https://img.shields.io/badge/License-Restrictive-c0392b?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](./LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-27ae60?style=for-the-badge&logo=semanticrelease&logoColor=white)](https://github.com/strykey/sample-pack-assembler/releases)
[![pywebview](https://img.shields.io/badge/pywebview-4.x-c8b89a?style=for-the-badge&logo=python&logoColor=111111)](https://pywebview.flowrl.com)

<br/>

*A desktop tool for producers who take their sample packs seriously.*

<br/>

[Get Started](#installation) &nbsp;·&nbsp; [Features](#features) &nbsp;·&nbsp; [Themes](#themes) &nbsp;·&nbsp; [Naming Templates](#naming-template-variables) &nbsp;·&nbsp; [License](#license)

</div>

---

## What it is

Sample Pack Assembler is a desktop application built for music producers who need to organize, categorize, rename and export their sample collections into clean, structured packs. You drop in a messy folder of kicks, snares, synths and loops, and it comes out the other side sorted, renamed and ready to distribute or sell.

The interface runs in a native desktop window with five distinct visual themes. There is no account, no subscription, no internet connection required. Everything is processed on your machine and stays there.

---

## Table of Contents

[What it is](#what-it-is) &nbsp;&nbsp; [Features](#features) &nbsp;&nbsp; [Screenshots](#screenshots) &nbsp;&nbsp; [Installation](#installation) &nbsp;&nbsp; [How it works](#how-it-works) &nbsp;&nbsp; [Supported formats](#supported-formats) &nbsp;&nbsp; [Categories](#categories) &nbsp;&nbsp; [Naming templates](#naming-template-variables) &nbsp;&nbsp; [Themes](#themes) &nbsp;&nbsp; [Project structure](#project-structure)

---

## Features

**Auto-detection** is the first thing that runs when you scan a folder. The app checks every filename against 57 keyword rules spread across 14 categories. If a file has "kick", "bd" or "kck" anywhere in its name, it lands in Kicks. If it has "808", "sub" or "bass", it goes to Bass. It covers most naming conventions producers actually use, so the grid usually looks right without touching anything.

**Manual override** is always available. Every card has a dropdown you can change on the spot, and if you have a batch of files to move together you can select them and reassign them all in two clicks.

**Audio preview on hover** works by moving your cursor over a card. The sample plays immediately, no click required. It caches the file after the first load so playback stays instant. Moving away stops it.

**Five themes** change more than just colors. Each one has its own font pairing loaded from Google Fonts and its own border radius. Vapor uses Righteous and Share Tech Mono. Acid renders in Black Ops One and VT323. They are genuinely different aesthetics to work in, not palette swaps.

**Naming templates** let you define exactly how output files are named using four variables before you export. A live preview shows you the first eight files renamed in real time before you commit to anything.

**Assembly** takes everything you have organized and builds a clean output folder from scratch. Category subfolders, renamed files, an optional README you write yourself. One click, everything in order.

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
<td><img src="https://i.ibb.co/5x9bzpk4/Noir.png" alt="Noir"/></td>
<td><img src="https://i.ibb.co/qFLkHg5n/Vapor.png" alt="Vapor"/></td>
<td><img src="https://i.ibb.co/Gv1YkS1Z/Acid.png" alt="Acid"/></td>
</tr>
<tr>
<td align="center"><b>Studio</b></td>
<td align="center"><b>Lo-Fi</b></td>
<td align="center"></td>
</tr>
<tr>
<td><img src="https://i.ibb.co/Lz18r4GH/STUDIO.png" alt="Studio"/></td>
<td><img src="https://i.ibb.co/wZ62Nmm4/LOFI.png" alt="Lo-Fi"/></td>
<td></td>
</tr>
</table>

*Replace placeholders with real screenshots once the app is running.*

</div>

---

## Installation

```bash
git clone https://github.com/strykey/sample-pack-assembler.git
cd sample-pack-assembler
pip install -r requirements.txt
python main.py
```

**Requirements**

```
pywebview >= 4.0
```

One package. One file to run. No build step, no frontend toolchain, no webpack. If you have Python 3.7 or higher, you are two commands away from having it open on your screen.

---

## How it works

When you click Scan, the app walks your source folder recursively and collects every audio and image file it finds. Each file goes through a keyword matching function against a dictionary of 14 categories. The matching is case-insensitive and checks anywhere in the filename, so `Tight_Snare_01.wav`, `snr_tight.wav` and `MY_SNARE.wav` all land in Snares without you doing anything.

The organize view gives you a card grid, filterable by category on the left and searchable in real time at the top. You can reassign any file with a dropdown, or select a group and use the bulk assign button.

The assemble view is where you set the naming template, write the README text if you want one, and trigger the export. The app builds the output directory from scratch on each run, copies every file to its category subfolder with the new name applied, and reports back with the file count, total size and the list of folders it created. Your source folder is never touched.

---

## Supported formats

<div align="center">

| Type | Extensions |
|:---|:---|
| Audio | `.wav` `.mp3` `.aiff` `.aif` `.flac` `.ogg` |
| MIDI | `.mid` `.midi` |
| Artwork | `.png` `.jpg` `.jpeg` `.webp` |

</div>

---

## Categories

<div align="center">

`Kicks` &nbsp; `Snares` &nbsp; `Hi-Hats` &nbsp; `Claps` &nbsp; `Percs` &nbsp; `Bass` &nbsp; `Synths` &nbsp; `Leads` &nbsp; `Pads` &nbsp; `Chords` &nbsp; `Loops` &nbsp; `Vocals` &nbsp; `FX` &nbsp; `MIDI` &nbsp; `Misc` &nbsp; `Artwork`

</div>

---

## Naming template variables

<div align="center">

| Variable | Value |
|:---:|:---|
| `{pack}` | The pack name you entered in the sidebar |
| `{type}` | The category assigned to the file |
| `{n}` | Two-digit sequential number per category (01, 02…) |
| `{stem}` | Original filename without extension |

</div>

**Examples**

```
{type}_{n}_{stem}   ->   Kicks_01_HardKick.wav
{pack}_{type}_{n}   ->   MyPack_Kicks_01.wav
{stem}              ->   HardKick.wav   (keeps original name)
```

---

## Themes

<div align="center">

| Theme | Vibe | Primary Font |
|:---|:---|:---|
| **Noir** | Dark cinema, cream on black | Playfair Display |
| **Vapor** | Purple and pink, vaporwave | Righteous |
| **Studio** | Light, cream paper with orange accents | Bebas Neue |
| **Acid** | Terminal green on black | Black Ops One |
| **Lo-Fi** | Warm brown, candlelight | Abril Fatface |

</div>

---

## Project structure

```
sample-pack-assembler/
├── main.py            # Entry point — Python backend + embedded HTML/JS UI
├── requirements.txt   # Single dependency: pywebview
├── README.md          # This file
├── LICENSE            # Custom restrictive license
└── CHANGELOG.md       # Version history
```

---

## License

This project is under a custom restrictive license. Personal use is permitted. Commercial use, redistribution and public forks all require explicit written permission. Read the full terms in [LICENSE](./LICENSE).

---

<div align="center">

<br/>

made with love by **Strykey**

<br/>

[![GitHub stars](https://img.shields.io/github/stars/strykey/sample-pack-assembler?style=for-the-badge&color=c8b89a&labelColor=1a1a1a)](https://github.com/strykey/sample-pack-assembler/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/strykey/sample-pack-assembler?style=for-the-badge&color=c8b89a&labelColor=1a1a1a)](https://github.com/strykey/sample-pack-assembler/network)

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:c8b89a,40:1a1208,100:0a0a0a&height=120&section=footer" width="100%"/>

</div>
