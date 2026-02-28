#!/usr/bin/env python3

import webview
import os
import shutil
import json
import re
from pathlib import Path


CATEGORIES = [
    "Kicks", "Snares", "Hi-Hats", "Claps", "Percs",
    "Bass", "Synths", "Leads", "Pads", "Chords",
    "Loops", "Vocals", "FX", "MIDI", "Misc"
]

AUTO_DETECT = {
    "Kicks":   ["kick", "kck", "bd", "bassdrum", "bass_drum"],
    "Snares":  ["snare", "snr", "rimshot", "rim"],
    "Hi-Hats": ["hihat", "hi-hat", "hat", "hh", "cymbal", "ohh", "chh"],
    "Claps":   ["clap", "clp"],
    "Percs":   ["perc", "percussion", "shaker", "tambourine", "conga", "bongo", "tom", "crash", "ride"],
    "Bass":    ["bass", "sub", "808"],
    "Synths":  ["synth", "lead", "arp", "pluck"],
    "Leads":   ["lead", "solo", "melody"],
    "Pads":    ["pad", "atm", "atmosphere", "ambient", "drone"],
    "Chords":  ["chord", "stab", "piano", "keys"],
    "Loops":   ["loop", "break", "groove", "full", "beat"],
    "Vocals":  ["vox", "vocal", "voice", "acapella", "adlib", "hook"],
    "FX":      ["fx", "effect", "riser", "down", "sweep", "impact", "foley", "noise", "verb", "reverb"],
    "MIDI":    [".mid"],
}

AUDIO_EXTS = {".wav", ".mp3", ".aiff", ".aif", ".flac", ".ogg", ".mid", ".midi"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}

THEMES = {
    "Noir": {
        "bg":        "#0a0a0a",
        "surface":   "#111111",
        "surface2":  "#1a1a1a",
        "border":    "#2a2a2a",
        "accent":    "#e8e0d0",
        "accent2":   "#c8b89a",
        "text":      "#e8e0d0",
        "text_dim":  "#666666",
        "danger":    "#c0392b",
        "success":   "#27ae60",
        "font_head": "'Playfair Display', Georgia, serif",
        "font_body": "'IBM Plex Mono', 'Courier New', monospace",
        "radius":    "2px",
    },
    "Vapor": {
        "bg":        "#0d0118",
        "surface":   "#130222",
        "surface2":  "#1d0433",
        "border":    "#3d1060",
        "accent":    "#ff71ce",
        "accent2":   "#01cdfe",
        "text":      "#fffbe6",
        "text_dim":  "#8866aa",
        "danger":    "#ff4488",
        "success":   "#01cdfe",
        "font_head": "'Righteous', 'Impact', sans-serif",
        "font_body": "'Share Tech Mono', monospace",
        "radius":    "0px",
    },
    "Studio": {
        "bg":        "#f0ede8",
        "surface":   "#faf8f5",
        "surface2":  "#e8e4de",
        "border":    "#ccc7c0",
        "accent":    "#1a1a1a",
        "accent2":   "#d4611b",
        "text":      "#1a1a1a",
        "text_dim":  "#888880",
        "danger":    "#c0392b",
        "success":   "#2d6a4f",
        "font_head": "'Bebas Neue', 'Impact', sans-serif",
        "font_body": "'Space Mono', monospace",
        "radius":    "1px",
    },
    "Acid": {
        "bg":        "#0f1900",
        "surface":   "#151f00",
        "surface2":  "#1e2d00",
        "border":    "#3a5000",
        "accent":    "#b8ff00",
        "accent2":   "#78cc00",
        "text":      "#c8f000",
        "text_dim":  "#506600",
        "danger":    "#ff4400",
        "success":   "#b8ff00",
        "font_head": "'Black Ops One', 'Impact', sans-serif",
        "font_body": "'VT323', 'Courier New', monospace",
        "radius":    "0px",
    },
    "Lo-Fi": {
        "bg":        "#2c2416",
        "surface":   "#362d1c",
        "surface2":  "#443820",
        "border":    "#6b5535",
        "accent":    "#f4d090",
        "accent2":   "#e09050",
        "text":      "#f4e8c8",
        "text_dim":  "#8a7050",
        "danger":    "#cc5533",
        "success":   "#88aa44",
        "font_head": "'Abril Fatface', Georgia, serif",
        "font_body": "'Inconsolata', monospace",
        "radius":    "3px",
    },
}

class SamplePackAPI:
    def __init__(self):
        self.window = None
        self.scanned_files = []
        self.assignments = {}
        self.source_dir = ""
        self.pack_name = ""
        self.output_dir = ""

    def pick_source_folder(self):
        dirs = self.window.create_file_dialog(
            webview.FOLDER_DIALOG,
            allow_multiple=False
        )
        if dirs:
            return dirs[0]
        return None

    def pick_output_folder(self):
        dirs = self.window.create_file_dialog(
            webview.FOLDER_DIALOG,
            allow_multiple=False
        )
        if dirs:
            return dirs[0]
        return None

    def scan_folder(self, folder_path):
        self.source_dir = folder_path
        results = []
        try:
            for root, _, files in os.walk(folder_path):
                for f in files:
                    ext = Path(f).suffix.lower()
                    if ext in AUDIO_EXTS or ext in IMAGE_EXTS:
                        full = os.path.join(root, f)
                        size = os.path.getsize(full)
                        detected = self._detect_category(f, ext)
                        results.append({
                            "path": full,
                            "name": f,
                            "ext": ext,
                            "size": size,
                            "size_str": self._fmt_size(size),
                            "detected": detected,
                            "is_image": ext in IMAGE_EXTS,
                        })
        except Exception as e:
            return {"error": str(e)}

        results.sort(key=lambda x: (x["detected"], x["name"]))
        self.scanned_files = results

        self.assignments = {r["path"]: r["detected"] for r in results}

        return {"files": results, "count": len(results)}

    def _detect_category(self, filename, ext):
        lower = filename.lower()
        if ext in {".mid", ".midi"}:
            return "MIDI"
        if Path(filename).suffix.lower() in IMAGE_EXTS:
            return "Artwork"
        for cat, keywords in AUTO_DETECT.items():
            for kw in keywords:
                if kw in lower:
                    return cat
        return "Misc"

    def _fmt_size(self, size):
        if size < 1024:
            return f"{size} B"
        elif size < 1024**2:
            return f"{size/1024:.1f} KB"
        else:
            return f"{size/1024**2:.1f} MB"

    def set_assignment(self, file_path, category):
        self.assignments[file_path] = category
        return True

    def set_assignments_bulk(self, assignments_dict):
        self.assignments.update(assignments_dict)
        return True

    def get_categories(self):
        return CATEGORIES + ["Artwork"]

    def get_themes(self):
        return list(THEMES.keys())

    def get_theme(self, name):
        return THEMES.get(name, THEMES["Noir"])

    def get_audio_b64(self, file_path):
        import base64
        ext = Path(file_path).suffix.lower()
        MIME = {
            '.wav':  'audio/wav',
            '.mp3':  'audio/mpeg',
            '.mp4':  'audio/mp4',
            '.m4a':  'audio/mp4',
            '.aiff': 'audio/aiff',
            '.aif':  'audio/aiff',
            '.flac': 'audio/flac',
            '.ogg':  'audio/ogg',
            '.opus': 'audio/ogg',
        }
        mime = MIME.get(ext, 'audio/wav')
        try:
            with open(file_path, 'rb') as f:
                data = base64.b64encode(f.read()).decode('ascii')
            return {'ok': True, 'data': data, 'mime': mime}
        except Exception as e:
            return {'ok': False, 'error': str(e)}

    def _sanitize(self, s):
        return re.sub(r'[^\w\s\-]', '', s).strip().replace(' ', '_')

    def build_naming_preview(self, pack_name, prefix, suffix_template, samples):
        results = []
        counters = {}
        for s in samples:
            cat = self.assignments.get(s["path"], "Misc")
            counters[cat] = counters.get(cat, 0) + 1
            n = counters[cat]
            stem = Path(s["name"]).stem
            ext  = Path(s["name"]).suffix

            new_name = suffix_template \
                .replace("{pack}", self._sanitize(pack_name)) \
                .replace("{type}", cat) \
                .replace("{n}", str(n).zfill(2)) \
                .replace("{stem}", stem)
            results.append({"old": s["name"], "new": new_name + ext})
        return results

    def assemble(self, pack_name, output_dir, naming_template, create_readme, readme_text):
        pack_name_safe = self._sanitize(pack_name) if pack_name else "MySamplePack"
        out_root = os.path.join(output_dir, pack_name_safe)

        if os.path.exists(out_root):
            shutil.rmtree(out_root)

        created_dirs = set()
        counters = {}
        errors = []
        copied = 0

        for f in self.scanned_files:
            cat = self.assignments.get(f["path"], "Misc")
            if cat == "Artwork":
                dest_dir = os.path.join(out_root, "Artwork")
            else:
                dest_dir = os.path.join(out_root, cat)

            if dest_dir not in created_dirs:
                os.makedirs(dest_dir, exist_ok=True)
                created_dirs.add(dest_dir)

            counters[cat] = counters.get(cat, 0) + 1
            n = counters[cat]
            stem = Path(f["name"]).stem
            ext  = Path(f["name"]).suffix

            new_name = naming_template \
                .replace("{pack}", pack_name_safe) \
                .replace("{type}", cat) \
                .replace("{n}", str(n).zfill(2)) \
                .replace("{stem}", stem)
            new_name = self._sanitize(new_name) + ext

            dest = os.path.join(dest_dir, new_name)
            try:
                shutil.copy2(f["path"], dest)
                copied += 1
            except Exception as e:
                errors.append(f"{f['name']}: {e}")

        if create_readme and readme_text:
            readme_path = os.path.join(out_root, "README.txt")
            with open(readme_path, "w", encoding="utf-8") as fp:
                fp.write(readme_text)

        total_size = sum(
            os.path.getsize(os.path.join(r, fn))
            for r, _, fs in os.walk(out_root) for fn in fs
        )

        return {
            "success": True,
            "path": out_root,
            "copied": copied,
            "errors": errors,
            "size": self._fmt_size(total_size),
            "dirs": sorted(os.listdir(out_root)),
        }


HTML = r"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sample Pack Assembler</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=IBM+Plex+Mono:wght@400;500&family=Bebas+Neue&family=Space+Mono:wght@400;700&family=Righteous&family=Share+Tech+Mono&family=Black+Ops+One&family=VT323&family=Abril+Fatface&family=Inconsolata:wght@400;700&display=swap" rel="stylesheet">

<style>
  :root {
    --bg: #0a0a0a;
    --surface: #111111;
    --surface2: #1a1a1a;
    --border: #2a2a2a;
    --accent: #e8e0d0;
    --accent2: #c8b89a;
    --text: #e8e0d0;
    --text-dim: #666666;
    --danger: #c0392b;
    --success: #27ae60;
    --font-head: 'Playfair Display', Georgia, serif;
    --font-body: 'IBM Plex Mono', 'Courier New', monospace;
    --radius: 2px;
    --transition: 0.18s ease;
  }

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  html, body {
    height: 100%;
    background: var(--bg);
    color: var(--text);
    font-family: var(--font-body);
    font-size: 13px;
    line-height: 1.5;
    overflow: hidden;
    user-select: none;
  }

  /* ─── LAYOUT ─── */
  #app {
    display: grid;
    grid-template-columns: 220px 1fr;
    grid-template-rows: 48px 1fr;
    height: 100vh;
  }

  /* ─── TOPBAR ─── */
  #topbar {
    grid-column: 1 / -1;
    display: flex;
    align-items: center;
    padding: 0 20px;
    border-bottom: 1px solid var(--border);
    background: var(--surface);
    gap: 24px;
  }
  #topbar .logo {
    font-family: var(--font-head);
    font-size: 17px;
    letter-spacing: 0.04em;
    color: var(--accent);
    white-space: nowrap;
    text-transform: uppercase;
  }
  #topbar .logo span { color: var(--accent2); font-style: italic; }
  #topbar .spacer { flex: 1; }

  .theme-pills {
    display: flex;
    gap: 6px;
  }
  .theme-pill {
    padding: 3px 10px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    cursor: pointer;
    font-family: var(--font-body);
    font-size: 11px;
    background: transparent;
    color: var(--text-dim);
    transition: all var(--transition);
  }
  .theme-pill:hover { border-color: var(--accent); color: var(--accent); }
  .theme-pill.active { background: var(--accent); color: var(--bg); border-color: var(--accent); }

  /* ─── SIDEBAR ─── */
  #sidebar {
    border-right: 1px solid var(--border);
    background: var(--surface);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  .sidebar-section {
    padding: 16px 14px 12px;
    border-bottom: 1px solid var(--border);
  }
  .sidebar-section label {
    display: block;
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-bottom: 8px;
  }
  .sidebar-input {
    width: 100%;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    color: var(--text);
    font-family: var(--font-body);
    font-size: 12px;
    padding: 6px 9px;
    outline: none;
    transition: border-color var(--transition);
  }
  .sidebar-input:focus { border-color: var(--accent); }

  .sidebar-btn {
    width: 100%;
    padding: 7px 0;
    background: transparent;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    color: var(--text-dim);
    font-family: var(--font-body);
    font-size: 11px;
    letter-spacing: 0.06em;
    cursor: pointer;
    transition: all var(--transition);
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    display: block;
    margin-top: 6px;
  }
  .sidebar-btn:hover { border-color: var(--accent); color: var(--accent); }
  .sidebar-btn.primary {
    border-color: var(--accent);
    color: var(--accent);
    font-weight: 700;
  }
  .sidebar-btn.primary:hover { background: var(--accent); color: var(--bg); }
  .sidebar-btn.success-btn {
    border-color: var(--success);
    color: var(--success);
  }
  .sidebar-btn.success-btn:hover { background: var(--success); color: var(--bg); }

  .stats-row {
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: var(--text-dim);
    padding: 4px 0;
  }
  .stats-row span:last-child { color: var(--accent); }

  /* Category filter */
  .cat-filter-list {
    flex: 1;
    overflow-y: auto;
    padding: 8px 6px;
    scrollbar-width: thin;
    scrollbar-color: var(--border) transparent;
  }
  .cat-filter-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 5px 8px;
    border-radius: var(--radius);
    cursor: pointer;
    transition: background var(--transition);
    font-size: 12px;
    color: var(--text-dim);
  }
  .cat-filter-item:hover { background: var(--surface2); color: var(--text); }
  .cat-filter-item.active { background: var(--surface2); color: var(--accent); }
  .cat-filter-item .badge {
    font-size: 10px;
    background: var(--surface2);
    padding: 1px 6px;
    border-radius: 20px;
    color: var(--text-dim);
  }
  .cat-filter-item.active .badge { background: var(--accent); color: var(--bg); }

  /* ─── MAIN CONTENT ─── */
  #main {
    display: flex;
    flex-direction: column;
    overflow: hidden;
    background: var(--bg);
  }

  /* Tabs */
  #tabs {
    display: flex;
    border-bottom: 1px solid var(--border);
    padding: 0 16px;
    background: var(--surface);
    gap: 0;
  }
  .tab {
    padding: 13px 18px;
    font-family: var(--font-body);
    font-size: 11px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    cursor: pointer;
    color: var(--text-dim);
    border-bottom: 2px solid transparent;
    transition: all var(--transition);
  }
  .tab:hover { color: var(--text); }
  .tab.active { color: var(--accent); border-bottom-color: var(--accent); }

  /* Toolbar */
  #toolbar {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 16px;
    border-bottom: 1px solid var(--border);
    flex-shrink: 0;
  }
  #search-box {
    flex: 1;
    max-width: 280px;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    color: var(--text);
    font-family: var(--font-body);
    font-size: 12px;
    padding: 5px 10px;
    outline: none;
  }
  #search-box:focus { border-color: var(--accent); }
  #search-box::placeholder { color: var(--text-dim); }

  .toolbar-btn {
    padding: 5px 12px;
    background: transparent;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    color: var(--text-dim);
    font-family: var(--font-body);
    font-size: 11px;
    cursor: pointer;
    transition: all var(--transition);
    white-space: nowrap;
  }
  .toolbar-btn:hover { border-color: var(--accent); color: var(--accent); }

  .bulk-assign {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-left: auto;
  }
  .bulk-assign select {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    color: var(--text);
    font-family: var(--font-body);
    font-size: 11px;
    padding: 4px 8px;
    outline: none;
  }

  /* File grid */
  #file-grid-wrap {
    flex: 1;
    overflow-y: auto;
    padding: 12px 14px;
    scrollbar-width: thin;
    scrollbar-color: var(--border) transparent;
  }
  #file-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
    gap: 8px;
  }

  .file-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 10px 10px 8px;
    cursor: pointer;
    transition: border-color var(--transition), transform var(--transition);
    position: relative;
  }
  .file-card:hover { border-color: var(--accent2); transform: translateY(-1px); }
  .file-card.selected { border-color: var(--accent); background: var(--surface2); }

  .file-card.previewing {
    border-color: var(--accent2);
    box-shadow: 0 0 0 1px var(--accent2), inset 0 0 12px rgba(0,0,0,0.2);
  }
  .file-card.previewing .fname { color: var(--accent2); }
  .file-card.previewing::before {
    content: '▶';
    position: absolute;
    bottom: 8px; right: 10px;
    font-size: 9px;
    color: var(--accent2);
    opacity: 0.8;
  }

  .file-card .cb {
    position: absolute;
    top: 8px; right: 8px;
    width: 14px; height: 14px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    background: var(--surface2);
    cursor: pointer;
    transition: all var(--transition);
    display: flex; align-items: center; justify-content: center;
  }
  .file-card.selected .cb {
    background: var(--accent);
    border-color: var(--accent);
  }
  .file-card.selected .cb::after {
    content: '';
    width: 7px; height: 5px;
    border-left: 1.5px solid var(--bg);
    border-bottom: 1.5px solid var(--bg);
    transform: rotate(-45deg) translateY(-1px);
  }

  .file-card .ext-badge {
    display: inline-block;
    font-size: 9px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 2px 6px;
    border-radius: var(--radius);
    margin-bottom: 6px;
    background: var(--surface2);
    color: var(--text-dim);
    border: 1px solid var(--border);
  }
  .file-card .ext-badge.wav { border-color: var(--accent2); color: var(--accent2); }
  .file-card .ext-badge.mid { border-color: #a880ff; color: #a880ff; }
  .file-card .ext-badge.img { border-color: #80c8ff; color: #80c8ff; }

  .file-card .fname {
    font-size: 11px;
    color: var(--text);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    margin-bottom: 8px;
  }

  .file-card .cat-select {
    width: 100%;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    color: var(--text);
    font-family: var(--font-body);
    font-size: 10px;
    padding: 3px 5px;
    outline: none;
    cursor: pointer;
  }
  .file-card .cat-select:hover, .file-card .cat-select:focus {
    border-color: var(--accent);
  }

  .file-card .fsize {
    font-size: 10px;
    color: var(--text-dim);
    margin-top: 4px;
  }

  /* ─── EMPTY STATE ─── */
  #empty-state {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: var(--text-dim);
    gap: 16px;
  }
  #empty-state .big-text {
    font-family: var(--font-head);
    font-size: 28px;
    color: var(--border);
    letter-spacing: 0.04em;
  }
  #empty-state p { font-size: 12px; text-align: center; max-width: 300px; }

  /* ─── ASSEMBLE TAB ─── */
  #assemble-panel {
    padding: 24px;
    overflow-y: auto;
    flex: 1;
  }
  .form-row {
    margin-bottom: 18px;
  }
  .form-row label {
    display: block;
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-bottom: 6px;
  }
  .form-row input, .form-row textarea, .form-row select {
    width: 100%;
    max-width: 480px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    color: var(--text);
    font-family: var(--font-body);
    font-size: 12px;
    padding: 8px 10px;
    outline: none;
    transition: border-color var(--transition);
  }
  .form-row input:focus, .form-row textarea:focus { border-color: var(--accent); }
  .form-row textarea { height: 100px; resize: vertical; }

  .naming-templates {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 8px;
  }
  .naming-template-btn {
    padding: 4px 10px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    background: transparent;
    color: var(--text-dim);
    font-family: var(--font-body);
    font-size: 11px;
    cursor: pointer;
    transition: all var(--transition);
  }
  .naming-template-btn:hover { border-color: var(--accent2); color: var(--accent2); }
  .naming-template-btn.active { border-color: var(--accent); color: var(--accent); background: var(--surface2); }

  .assemble-section-title {
    font-family: var(--font-head);
    font-size: 18px;
    color: var(--accent);
    margin-bottom: 20px;
    letter-spacing: 0.02em;
  }

  .big-assemble-btn {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 12px 32px;
    background: var(--accent);
    color: var(--bg);
    border: none;
    border-radius: var(--radius);
    font-family: var(--font-head);
    font-size: 16px;
    cursor: pointer;
    transition: all var(--transition);
    letter-spacing: 0.04em;
    margin-top: 8px;
  }
  .big-assemble-btn:hover { opacity: 0.88; transform: translateY(-1px); }
  .big-assemble-btn:disabled { opacity: 0.3; cursor: not-allowed; transform: none; }

  /* ─── RESULT PANEL ─── */
  #result-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.85);
    display: none;
    align-items: center;
    justify-content: center;
    z-index: 100;
  }
  #result-overlay.show { display: flex; }
  .result-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 32px 36px;
    max-width: 480px;
    width: 90%;
  }
  .result-box h2 {
    font-family: var(--font-head);
    font-size: 22px;
    color: var(--accent);
    margin-bottom: 16px;
  }
  .result-box .result-row {
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    border-bottom: 1px solid var(--border);
    font-size: 12px;
  }
  .result-box .result-row:last-of-type { border-bottom: none; }
  .result-box .result-row span:first-child { color: var(--text-dim); }
  .result-box .result-row span:last-child { color: var(--accent); }
  .result-box .result-dirs {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin: 14px 0;
  }
  .result-box .dir-tag {
    padding: 3px 10px;
    border: 1px solid var(--accent2);
    border-radius: var(--radius);
    font-size: 11px;
    color: var(--accent2);
  }
  .result-close {
    margin-top: 20px;
    padding: 9px 24px;
    background: transparent;
    border: 1px solid var(--accent);
    border-radius: var(--radius);
    color: var(--accent);
    font-family: var(--font-body);
    font-size: 12px;
    cursor: pointer;
    transition: all var(--transition);
  }
  .result-close:hover { background: var(--accent); color: var(--bg); }

  /* Scrollbar */
  ::-webkit-scrollbar { width: 5px; height: 5px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
  ::-webkit-scrollbar-thumb:hover { background: var(--text-dim); }

  /* Divider label */
  .divider-label {
    font-size: 10px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-dim);
    padding: 8px 14px 4px;
    border-top: 1px solid var(--border);
  }

  /* Spinner */
  @keyframes spin { to { transform: rotate(360deg); } }
  .spinner {
    width: 14px; height: 14px;
    border: 2px solid var(--border);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
    display: inline-block;
  }

  /* Toggle */
  .toggle-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
  }
  .toggle {
    width: 34px; height: 18px;
    background: var(--border);
    border-radius: 9px;
    position: relative;
    cursor: pointer;
    transition: background var(--transition);
    flex-shrink: 0;
  }
  .toggle.on { background: var(--accent); }
  .toggle::after {
    content: '';
    position: absolute;
    width: 12px; height: 12px;
    background: var(--bg);
    border-radius: 50%;
    top: 3px; left: 3px;
    transition: transform var(--transition);
  }
  .toggle.on::after { transform: translateX(16px); }

  .checkbox-label {
    font-size: 12px;
    color: var(--text-dim);
    cursor: pointer;
  }

  #strykey-credit {
    padding: 10px 14px;
    font-family: var(--font-body);
    font-size: 10px;
    color: var(--border);
    letter-spacing: 0.08em;
    transition: color 0.3s ease;
    cursor: default;
    border-top: 1px solid var(--border);
    margin-top: auto;
  }
  #strykey-credit:hover {
    color: var(--accent2);
  }

  #toast {
    position: fixed;
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%) translateY(12px);
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    color: var(--text);
    font-family: var(--font-body);
    font-size: 12px;
    padding: 9px 20px;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.2s ease, transform 0.2s ease;
    z-index: 999;
    white-space: nowrap;
  }
  #toast.show {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
  #toast.error { border-color: var(--danger); color: var(--danger); }
  #toast.success { border-color: var(--success); color: var(--success); }
</style>
</head>
<body>
<div id="app">

  <!-- TOPBAR -->
  <div id="topbar">
    <div class="logo">Sample Pack <span>Assembler</span></div>
    <div class="spacer"></div>
    <div class="theme-pills" id="theme-pills"></div>
  </div>

  <!-- SIDEBAR -->
  <div id="sidebar">
    <div class="sidebar-section">
      <label>Pack Name</label>
      <input class="sidebar-input" id="pack-name-input" type="text" placeholder="My Pack Vol.1" />
    </div>

    <div class="sidebar-section">
      <label>Source Folder</label>
      <button class="sidebar-btn" id="btn-source">Pick folder...</button>
      <div id="source-path" style="font-size:10px;color:var(--text-dim);margin-top:5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;"></div>
    </div>

    <div class="sidebar-section">
      <label>Output Folder</label>
      <button class="sidebar-btn" id="btn-output">Pick folder...</button>
      <div id="output-path" style="font-size:10px;color:var(--text-dim);margin-top:5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;"></div>
    </div>

    <div class="sidebar-section">
      <div class="stats-row"><span>Files scanned</span><span id="stat-total">0</span></div>
      <div class="stats-row"><span>Selected</span><span id="stat-selected">0</span></div>
      <div class="stats-row"><span>Categories used</span><span id="stat-cats">0</span></div>
    </div>

    <div class="divider-label">Filter by Category</div>
    <div class="cat-filter-list" id="cat-filter-list">
      <div class="cat-filter-item active" data-cat="All">
        <span>All</span>
        <span class="badge" id="badge-all">0</span>
      </div>
    </div>

    <div id="strykey-credit">made with &hearts; by Strykey</div>
  </div>

  <!-- MAIN -->
  <div id="main">

    <div id="tabs">
      <div class="tab active" data-tab="organize">Organize</div>
      <div class="tab" data-tab="assemble">Assemble</div>
    </div>

    <!-- ORGANIZE TAB -->
    <div id="tab-organize" style="display:flex;flex-direction:column;flex:1;overflow:hidden;">
      <div id="toolbar">
        <input id="search-box" type="text" placeholder="Search files..." />
        <button class="toolbar-btn" id="btn-scan">Scan</button>
        <button class="toolbar-btn" id="btn-select-all">Select All</button>
        <button class="toolbar-btn" id="btn-clear-sel">Clear</button>
        <div class="bulk-assign">
          <span style="font-size:11px;color:var(--text-dim);">Bulk assign:</span>
          <select id="bulk-cat-select">
            <option value="">— category —</option>
          </select>
          <button class="toolbar-btn" id="btn-bulk-apply">Apply</button>
        </div>
      </div>

      <div id="file-grid-wrap">
        <div id="empty-state">
          <div class="big-text">No samples loaded</div>
          <p>Pick a source folder and click Scan to load your samples.</p>
        </div>
        <div id="file-grid" style="display:none;"></div>
      </div>
    </div>

    <!-- ASSEMBLE TAB -->
    <div id="tab-assemble" style="display:none;flex:1;overflow:hidden;">
      <div id="assemble-panel">
        <div class="assemble-section-title">Build the Pack</div>

        <div class="form-row">
          <label>Naming Template</label>
          <input type="text" id="naming-template" value="{type}_{n}_{stem}" />
          <div class="naming-templates">
            <button class="naming-template-btn active" data-tpl="{type}_{n}_{stem}">{type}_{n}_{stem}</button>
            <button class="naming-template-btn" data-tpl="{pack}_{type}_{n}">{pack}_{type}_{n}</button>
            <button class="naming-template-btn" data-tpl="{n}_{stem}">{n}_{stem}</button>
            <button class="naming-template-btn" data-tpl="{stem}">{stem} (original)</button>
          </div>
          <div style="margin-top:8px;font-size:11px;color:var(--text-dim);">
            Variables: <code style="color:var(--accent2)">{pack}</code> pack name &nbsp;
            <code style="color:var(--accent2)">{type}</code> category &nbsp;
            <code style="color:var(--accent2)">{n}</code> number &nbsp;
            <code style="color:var(--accent2)">{stem}</code> original filename
          </div>
        </div>

        <div class="form-row">
          <div class="toggle-row">
            <div class="toggle on" id="toggle-readme"></div>
            <span class="checkbox-label">Include README.txt</span>
          </div>
          <textarea id="readme-text" placeholder="Pack description, license info, BPM, key, artist name...">Pack created with Sample Pack Assembler.

All samples are royalty-free.

For licensing and credits, see the individual folder READMEs.
</textarea>
        </div>

        <div class="form-row" id="preview-section" style="display:none;">
          <label>Naming Preview</label>
          <div id="preview-list" style="background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:10px;max-height:180px;overflow-y:auto;"></div>
        </div>

        <button class="big-assemble-btn" id="btn-assemble" disabled>
          <span id="assemble-btn-text">Assemble Pack</span>
        </button>

      </div>
    </div>

  </div>
</div>

<!-- RESULT OVERLAY -->
<div id="result-overlay">
  <div class="result-box">
    <h2>Pack Assembled</h2>
    <div id="result-rows"></div>
    <div id="result-dirs" class="result-dirs"></div>
    <div id="result-errors" style="display:none;margin-top:10px;font-size:11px;color:var(--danger);"></div>
    <button class="result-close" id="result-close-btn">Close</button>
  </div>
</div>

<script>
let api = null;

let _toastTimer = null;
function toast(msg, type) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.className = 'show' + (type ? ' ' + type : '');
  clearTimeout(_toastTimer);
  _toastTimer = setTimeout(() => { el.className = ''; }, 2800);
}

let allFiles = [];
let selectedPaths = new Set();
let currentCatFilter = 'All';
let currentSearch = '';
let outputDir = '';
let includeReadme = true;

const AUDIO_PLAYABLE = new Set(['wav','mp3','mp4','m4a','aiff','aif','flac','ogg','opus']);
const audioCache = new Map();
const preloadQueue = new Set();

let activeAudio  = null;
let activeCard   = null;
let loadToken    = 0;

function stopAll() {
  loadToken++;
  if (activeAudio) { activeAudio.pause(); activeAudio.src = ''; activeAudio = null; }
  if (activeCard)  { activeCard.classList.remove('previewing'); activeCard = null; }
}

async function startPreview(card) {
  if (card === activeCard) return;
  stopAll();

  const path = decodeURIComponent(card.dataset.path);
  const ext  = path.split('.').pop().toLowerCase();
  if (!AUDIO_PLAYABLE.has(ext)) return;

  const myToken = ++loadToken;
  activeCard = card;
  card.classList.add('previewing');

  if (!audioCache.has(path) && !preloadQueue.has(path)) {
    preloadQueue.add(path);
    try {
      const res = await api.get_audio_b64(path);
      if (res && res.ok) audioCache.set(path, 'data:' + res.mime + ';base64,' + res.data);
    } catch(e) {}
    preloadQueue.delete(path);
  } else if (preloadQueue.has(path)) {

    let waited = 0;
    while (preloadQueue.has(path) && waited < 5000) {
      await new Promise(r => setTimeout(r, 30));
      waited += 30;
    }
  }

  if (myToken !== loadToken) return;
  const src = audioCache.get(path);
  if (!src) return;

  const audio = new Audio(src);
  audio.volume = 0.8;
  activeAudio = audio;
  try { await audio.play(); } catch(e) {}
}

function initAudioPreview() {
  const grid = document.getElementById('file-grid-wrap');
  grid.addEventListener('mouseover', (e) => {
    const card = e.target.closest('.file-card');
    if (card) startPreview(card); else stopAll();
  });
  grid.addEventListener('mouseleave', stopAll, true);
}

async function initThemes() {
  const themes = await api.get_themes();
  const pills = document.getElementById('theme-pills');
  themes.forEach((t, i) => {
    const el = document.createElement('button');
    el.className = 'theme-pill' + (i === 0 ? ' active' : '');
    el.textContent = t;
    el.onclick = () => applyTheme(t, el);
    pills.appendChild(el);
  });
}

async function applyTheme(name, clickedEl) {
  const theme = await api.get_theme(name);
  const root = document.documentElement;
  root.style.setProperty('--bg', theme.bg);
  root.style.setProperty('--surface', theme.surface);
  root.style.setProperty('--surface2', theme.surface2);
  root.style.setProperty('--border', theme.border);
  root.style.setProperty('--accent', theme.accent);
  root.style.setProperty('--accent2', theme.accent2);
  root.style.setProperty('--text', theme.text);
  root.style.setProperty('--text-dim', theme.text_dim);
  root.style.setProperty('--danger', theme.danger);
  root.style.setProperty('--success', theme.success);
  root.style.setProperty('--font-head', theme.font_head);
  root.style.setProperty('--font-body', theme.font_body);
  root.style.setProperty('--radius', theme.radius);

  document.querySelectorAll('.theme-pill').forEach(p => p.classList.remove('active'));
  if (clickedEl) clickedEl.classList.add('active');
}

async function renderFiles() {
  const cats = await api.get_categories();
  const grid = document.getElementById('file-grid');
  const empty = document.getElementById('empty-state');

  const filtered = allFiles.filter(f => {
    const catMatch = currentCatFilter === 'All' || f.detected === currentCatFilter;
    const searchMatch = !currentSearch || f.name.toLowerCase().includes(currentSearch.toLowerCase());
    return catMatch && searchMatch;
  });

  if (filtered.length === 0) {
    grid.style.display = 'none';
    empty.style.display = 'flex';
    empty.querySelector('.big-text').textContent = allFiles.length === 0 ? 'No samples loaded' : 'No results';
    return;
  }

  grid.style.display = 'grid';
  empty.style.display = 'none';

  grid.innerHTML = filtered.map(f => {
    const extClass = ['.wav','.aiff','.aif'].includes(f.ext) ? 'wav' :
                     ['.mid','.midi'].includes(f.ext) ? 'mid' :
                     f.is_image ? 'img' : '';
    const extLabel = f.ext.replace('.','').toUpperCase();
    const isSel = selectedPaths.has(f.path);

    const optionsHTML = cats.map(c =>
      `<option value="${c}" ${f.detected===c?'selected':''}>${c}</option>`
    ).join('');

    return `<div class="file-card${isSel?' selected':''}" data-path="${encodeURIComponent(f.path)}">
      <div class="cb"></div>
      <span class="ext-badge ${extClass}">${extLabel}</span>
      <div class="fname" title="${f.name}">${f.name}</div>
      <select class="cat-select" data-path="${encodeURIComponent(f.path)}">${optionsHTML}</select>
      <div class="fsize">${f.size_str}</div>
    </div>`;
  }).join('');

  grid.onclick = (e) => {
    const card = e.target.closest('.file-card');
    if (!card) return;
    if (e.target.tagName === 'SELECT') return;
    const path = decodeURIComponent(card.dataset.path);
    if (selectedPaths.has(path)) {
      selectedPaths.delete(path);
      card.classList.remove('selected');
    } else {
      selectedPaths.add(path);
      card.classList.add('selected');
    }
    updateStats();
  };

  grid.onchange = async (e) => {
    if (e.target.tagName !== 'SELECT') return;
    const path = decodeURIComponent(e.target.dataset.path);
    const cat = e.target.value;
    await api.set_assignment(path, cat);

    const f = allFiles.find(f2 => f2.path === path);
    if (f) f.detected = cat;
    buildCatFilter();
    updateStats();
  };
}


async function init() {
  await initThemes();
  const firstPill = document.querySelector('.theme-pill');
  if (firstPill) await applyTheme(firstPill.textContent, firstPill);

  await populateBulkSelect();
  buildCatFilter();
  initAudioPreview();

  document.querySelectorAll('.tab').forEach(tab => {
    tab.onclick = () => {
      stopAll();
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const id = tab.dataset.tab;
      document.querySelectorAll('[id^="tab-"]').forEach(p => p.style.display = 'none');
      document.getElementById('tab-' + id).style.display = 'flex';
      if (id === 'assemble') refreshPreview();
    };
  });


  document.getElementById('pack-name-input').oninput = () => { refreshPreview(); };

  document.getElementById('btn-source').onclick = async () => {
    const dir = await api.pick_source_folder();
    if (!dir) return;
    document.getElementById('source-path').textContent = dir;
    document.getElementById('btn-source').textContent = dir.split(/[\\/]/).pop() || dir;
  };

  document.getElementById('btn-output').onclick = async () => {
    const dir = await api.pick_output_folder();
    if (!dir) return;
    outputDir = dir;
    document.getElementById('output-path').textContent = dir;
    document.getElementById('btn-output').textContent = dir.split(/[\\/]/).pop() || dir;
    checkAssembleReady();
  };

  document.getElementById('btn-scan').onclick = async () => {
    const src = document.getElementById('source-path').textContent.trim();
    if (!src) { toast('Pick a source folder first.', 'error'); return; }
    document.getElementById('btn-scan').innerHTML = '<span class="spinner"></span>';
    const result = await api.scan_folder(src);
    document.getElementById('btn-scan').textContent = 'Scan';
    if (result.error) { toast(result.error, 'error'); return; }
    allFiles = result.files;
    selectedPaths = new Set();
    renderFiles();
    buildCatFilter();
    updateStats();
    checkAssembleReady();
  };

  document.getElementById('btn-select-all').onclick = () => {
    const visible = allFiles.filter(f => {
      const catMatch = currentCatFilter === 'All' || f.detected === currentCatFilter;
      const searchMatch = !currentSearch || f.name.toLowerCase().includes(currentSearch.toLowerCase());
      return catMatch && searchMatch;
    });
    visible.forEach(f => selectedPaths.add(f.path));
    renderFiles();
    updateStats();
  };

  document.getElementById('btn-clear-sel').onclick = () => {
    selectedPaths.clear();
    renderFiles();
    updateStats();
  };

  async function populateBulkSelect() {
    const cats = await api.get_categories();
    const sel = document.getElementById('bulk-cat-select');
    sel.innerHTML = '<option value="">— category —</option>' +
      cats.map(c => `<option value="${c}">${c}</option>`).join('');
  }

  document.getElementById('btn-bulk-apply').onclick = async () => {
    const cat = document.getElementById('bulk-cat-select').value;
    if (!cat) return;
    if (selectedPaths.size === 0) { toast('Select files first.', 'error'); return; }
    const dict = {};
    selectedPaths.forEach(p => { dict[p] = cat; });
    await api.set_assignments_bulk(dict);
    allFiles.forEach(f => { if (selectedPaths.has(f.path)) f.detected = cat; });
    buildCatFilter();
    renderFiles();
    updateStats();
  };

  document.getElementById('search-box').oninput = (e) => {
    currentSearch = e.target.value;
    renderFiles();
  };

  function buildCatFilter() {
    const counts = { All: allFiles.length };
    allFiles.forEach(f => {
      counts[f.detected] = (counts[f.detected] || 0) + 1;
    });

    const list = document.getElementById('cat-filter-list');
    const cats = ['All', ...Object.keys(counts).filter(c => c !== 'All').sort()];

    list.innerHTML = cats.map(cat => `
      <div class="cat-filter-item${currentCatFilter===cat?' active':''}" data-cat="${cat}">
        <span>${cat}</span>
        <span class="badge">${counts[cat]||0}</span>
      </div>
    `).join('');

    list.onclick = (e) => {
      const item = e.target.closest('.cat-filter-item');
      if (!item) return;
      currentCatFilter = item.dataset.cat;
      list.querySelectorAll('.cat-filter-item').forEach(i => i.classList.remove('active'));
      item.classList.add('active');
      renderFiles();
    };
  }

  function updateStats() {
    document.getElementById('stat-total').textContent = allFiles.length;
    document.getElementById('stat-selected').textContent = selectedPaths.size;
    const cats = new Set(allFiles.map(f => f.detected));
    document.getElementById('stat-cats').textContent = cats.size;
  }

  function checkAssembleReady() {
    const hasFiles = allFiles.length > 0;
    const hasOutput = outputDir !== '';
    document.getElementById('btn-assemble').disabled = !(hasFiles && hasOutput);
  }

  document.querySelectorAll('.naming-template-btn').forEach(btn => {
    btn.onclick = () => {
      document.querySelectorAll('.naming-template-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById('naming-template').value = btn.dataset.tpl;
      refreshPreview();
    };
  });

  document.getElementById('naming-template').oninput = refreshPreview;

  async function refreshPreview() {
    if (allFiles.length === 0) return;
    const packName = document.getElementById('pack-name-input').value || 'Pack';
    const tpl = document.getElementById('naming-template').value;
    const sample = allFiles.slice(0, 8).map(f => ({ path: f.path, name: f.name, ext: f.ext }));
    const previews = await api.build_naming_preview(packName, '', tpl, sample);

    const sec = document.getElementById('preview-section');
    const lst = document.getElementById('preview-list');
    sec.style.display = 'block';
    lst.innerHTML = previews.map(p =>
      `<div style="display:flex;gap:12px;padding:4px 0;border-bottom:1px solid var(--border);font-size:11px;">
        <span style="color:var(--text-dim);flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${p.old}</span>
        <span style="color:var(--accent2);">→</span>
        <span style="color:var(--accent);flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${p.new}</span>
      </div>`
    ).join('');
  }

  document.getElementById('toggle-readme').onclick = function() {
    includeReadme = !includeReadme;
    this.classList.toggle('on', includeReadme);
    document.getElementById('readme-text').style.opacity = includeReadme ? '1' : '0.3';
  };

  document.getElementById('btn-assemble').onclick = async () => {
    const packName = document.getElementById('pack-name-input').value.trim() || 'MySamplePack';
    const tpl = document.getElementById('naming-template').value;
    const readmeText = includeReadme ? document.getElementById('readme-text').value : '';

    const btn = document.getElementById('btn-assemble');
    btn.disabled = true;
    document.getElementById('assemble-btn-text').innerHTML = '<span class="spinner"></span> Building...';

    const result = await api.assemble(packName, outputDir, tpl, includeReadme, readmeText);

    btn.disabled = false;
    document.getElementById('assemble-btn-text').textContent = 'Assemble Pack';

    if (!result.success) { toast('Assembly failed.', 'error'); return; }

    document.getElementById('result-rows').innerHTML = `
      <div class="result-row"><span>Files copied</span><span>${result.copied}</span></div>
      <div class="result-row"><span>Total size</span><span>${result.size}</span></div>
      <div class="result-row"><span>Output path</span><span style="font-size:10px;max-width:220px;text-align:right;overflow:hidden;text-overflow:ellipsis;">${result.path}</span></div>
    `;
    document.getElementById('result-dirs').innerHTML =
      result.dirs.map(d => `<span class="dir-tag">${d}</span>`).join('');

    if (result.errors && result.errors.length > 0) {
      const errDiv = document.getElementById('result-errors');
      errDiv.style.display = 'block';
      errDiv.textContent = 'Errors: ' + result.errors.slice(0,3).join(', ');
    }

    document.getElementById('result-overlay').classList.add('show');
  };

  document.getElementById('result-close-btn').onclick = () => {
    document.getElementById('result-overlay').classList.remove('show');
  };
}

window.addEventListener('pywebviewready', () => {
  api = window.pywebview.api;
  init();
});
</script>
<div id="toast"></div>
</body>
</html>
"""

def main():
    api_instance = SamplePackAPI()

    window = webview.create_window(
        title="Sample Pack Assembler",
        html=HTML,
        js_api=api_instance,
        width=1100,
        height=700,
        min_size=(800, 550),
        background_color="#0a0a0a",
        frameless=False,
        easy_drag=False,
    )
    api_instance.window = window
    webview.start(debug=False)

if __name__ == "__main__":
    main()