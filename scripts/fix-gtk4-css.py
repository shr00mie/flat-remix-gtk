#!/usr/bin/env python3
"""Make Flat-Remix GTK4 CSS compatible with modern GTK4 / libadwaita.

Fixes applied (from Ubuntu 24.04→26.04 breakage):
- shade(@color, n) → mix(white|black, @color, …)
- @sidebar_bg → @sidebar_bg_color
- normalize "mix (" → "mix("
- missing semicolon after flowbox padding
- drop -gtk-icon-effect: dim (GTK3-only)
- sync accent_* colors from libadwaita/gtk.css into gtk-4.0/gtk.css
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def fix_css(text: str) -> str:
    def repl_shade(m: re.Match[str]) -> str:
        color, factor = m.group(1).strip(), float(m.group(2))
        if factor >= 1.0:
            return f"mix(white, {color}, {round(factor - 1.0, 4)})"
        return f"mix(black, {color}, {round(1.0 - factor, 4)})"

    text = re.sub(
        r"shade\s*\(\s*(@[\w]+)\s*,\s*([0-9]*\.?[0-9]+)\s*\)",
        repl_shade,
        text,
    )
    text = (
        text.replace("@sidebar_bg;", "@sidebar_bg_color;")
        .replace("@sidebar_bg}", "@sidebar_bg_color}")
        .replace("@sidebar_bg ", "@sidebar_bg_color ")
    )
    text = re.sub(r"mix\s+\(", "mix(", text)
    text = re.sub(r"(flowbox\s*\{\s*padding:\s*18px)\s*\}", r"\1;\n}", text)
    text = re.sub(
        r"\s*-gtk-icon-effect:\s*dim;\s*/\*\s*GTK 3 only\s*\*/\s*/\*\s*GTK 4 TODO:[^*]*\*/\s*",
        "\n  ",
        text,
        flags=re.S,
    )
    text = re.sub(r"^\s*-gtk-icon-effect:\s*dim;\s*$", "", text, flags=re.M)
    return text


def sync_accent_from_libadwaita(gtk4_text: str, libadwaita_text: str) -> str:
    accents = {}
    for name in ("accent_bg_color", "accent_fg_color", "accent_color"):
        m = re.search(rf"@define-color {name} ([^;]+);", libadwaita_text)
        if m:
            accents[name] = m.group(1).strip()
    if not accents:
        return gtk4_text
    for name, value in accents.items():
        gtk4_text, n = re.subn(
            rf"@define-color {name} [^;]+;",
            f"@define-color {name} {value};",
            gtk4_text,
            count=1,
        )
        if n == 0 and name == "accent_bg_color":
            gtk4_text = f"@define-color {name} {value};\n" + gtk4_text
    return gtk4_text


def process_theme(theme_dir: Path) -> bool:
    gtk4 = theme_dir / "gtk-4.0" / "gtk.css"
    if not gtk4.exists():
        return False
    text = gtk4.read_text(encoding="utf-8")
    la = theme_dir / "libadwaita" / "gtk.css"
    if la.exists():
        text = sync_accent_from_libadwaita(text, la.read_text(encoding="utf-8"))
    text = fix_css(text)
    gtk4.write_text(text, encoding="utf-8")
    dark = theme_dir / "gtk-4.0" / "gtk-dark.css"
    if dark.exists() and not dark.is_symlink():
        dark.write_text(text, encoding="utf-8")
    return True


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        paths = [Path(a) for a in argv[1:]]
    else:
        root = Path(__file__).resolve().parents[1] / "themes"
        paths = sorted(p for p in root.iterdir() if p.is_dir())

    count = 0
    for path in paths:
        theme = path
        if process_theme(theme):
            count += 1
            print(f"fixed {theme.name}")
    print(f"fixed {count} themes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
