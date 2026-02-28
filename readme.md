<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0,1a1a1a,c8b89a&height=200&section=header&text=Sample%20Pack%20Assembler&fontSize=48&fontColor=ffffff&fontAlignY=55&animation=fadeIn&desc=by%20Strykey&descAlignY=75&descSize=18&descColor=c8b89a&stroke=c8b89a&strokeWidth=1" width="100%"/>

<br/>

[![Python](https://img.shields.io/badge/Python-3.7+-3572A5?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Win%20%7C%20Mac%20%7C%20Linux-555555?style=for-the-badge&logo=linux&logoColor=white)](https://github.com/strykey/sample-pack-assembler)
[![License](https://img.shields.io/badge/License-Restrictive-c0392b?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](./LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-27ae60?style=for-the-badge&logo=semanticrelease&logoColor=white)](https://github.com/strykey/sample-pack-assembler/releases)
[![pywebview](https://img.shields.io/badge/pywebview-4.x-c8b89a?style=for-the-badge&logo=python&logoColor=black)](https://pywebview.flowrl.com)

<br/>

**A desktop tool for producers who take their sample packs seriously.**

<br/>

[Get Started](#installation) · [Features](#features) · [Themes](#themes) · [Naming Templates](#naming-template-variables) · [License](#license)

<br/>

</div>

---

## Table of Contents

[What it is](#what-it-is) &nbsp;&nbsp; [Features](#features) &nbsp;&nbsp; [Screenshots](#screenshots) &nbsp;&nbsp; [Installation](#installation) &nbsp;&nbsp; [How it works](#how-it-works) &nbsp;&nbsp; [Supported formats](#supported-formats) &nbsp;&nbsp; [Categories](#categories) &nbsp;&nbsp; [Naming templates](#naming-template-variables) &nbsp;&nbsp; [Themes](#themes) &nbsp;&nbsp; [Project structure](#project-structure)

---

## What it is

Sample Pack Assembler is a desktop application built for music producers who need to organize, categorize, rename and export their sample collections into clean, structured packs. You drop in a messy folder of kicks, snares, synths and loops, and it comes out the other side sorted, renamed and ready to distribute or sell.

The interface runs in a native desktop window with five distinct visual themes. Everything is processed locally. Nothing leaves your machine.

---

## Features

<div align="center">

| | Feature | Description |
|:---:|:---|:---|
| 🔍 | **Auto-detection** | 57 keyword rules across 14 categories. Handles most naming conventions out of the box |
| ✏️ | **Manual override** | Per-file dropdown and bulk assignment for full control |
| 🔊 | **Audio preview** | Hover over any card to play the sample instantly, no click required |
| 🎨 | **Five themes** | Noir, Vapor, Studio, Acid, Lo-Fi — genuine aesthetics, not just color swaps |
| 📝 | **Naming templates** | Four variables, live preview before you export |
| 📦 | **One-click assembly** | Clean folder structure, renamed files, optional README, all in one click |

</div>

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
<td><img src="https://placehold.co/300x190/0a0a0a/e8e0d0?text=Noir" alt="Noir"/></td>
<td><img src="https://placehold.co/300x190/0d0118/ff71ce?text=Vapor" alt="Vapor"/></td>
<td><img src="https://placehold.co/300x190/0f1900/b8ff00?text=Acid" alt="Acid"/></td>
</tr>
<tr>
<td align="center"><b>Studio</b></td>
<td align="center"><b>Lo-Fi</b></td>
<td align="center"></td>
</tr>
<tr>
<td><img src="https://placehold.co/300x190/f0ede8/1a1a1a?text=Studio" alt="Studio"/></td>
<td><img src="https://placehold.co/300x190/2c2416/f4d090?text=Lo-Fi" alt="Lo-Fi"/></td>
<td></td>
</tr>
</table>

> Replace placeholders with real screenshots once the app is running.

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

One package. One file to run. No build step, no frontend toolchain, no webpack.

---

## How it works

When you click Scan, the app walks your source folder recursively and collects every audio and image file it finds. Each file is run through a keyword matching function against 57 rules across 14 categories. Detection is case-insensitive and matches anywhere in the filename, so `Tight_Snare_01.wav`, `snr_tight.wav` and `MY_SNARE.wav` all land in Snares without any manual input.

The organize view gives you a card grid, filterable by category and searchable in real time. You can reassign any file with a click, or select a batch and bulk-assign them all at once.

The assemble view handles naming templates, README content and the final export. On assembly, the app builds the output folder from scratch, copies every file to its destination with the new name applied, and writes the README if enabled. Your source files are never modified.

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
{type}_{n}_{stem}   →   Kicks_01_HardKick.wav
{pack}_{type}_{n}   →   MyPack_Kicks_01.wav
{stem}              →   HardKick.wav   (keeps original name)
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

This project is distributed under a custom restrictive license. Personal use is permitted. Commercial use, redistribution, and public forks require explicit written permission from the author. Read the full terms in [LICENSE](./LICENSE).

---

<div align="center">

<br/>

made with ♥ by **Strykey**

<br/>

[![GitHub stars](https://img.shields.io/github/stars/strykey/sample-pack-assembler?style=for-the-badge&color=c8b89a&labelColor=1a1a1a)](https://github.com/strykey/sample-pack-assembler/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/strykey/sample-pack-assembler?style=for-the-badge&color=c8b89a&labelColor=1a1a1a)](https://github.com/strykey/sample-pack-assembler/network)

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0,c8b89a,1a1a1a&height=100&section=footer" width="100%"/>

</div>
