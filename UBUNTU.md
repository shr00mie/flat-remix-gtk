# Flat Remix GTK on Ubuntu (GNOME 50 / GTK 4.22 / libadwaita 1.9)

This fork keeps classic **Flat-Remix-GTK-*-*** color variants and applies GTK4
CSS fixes required on modern Ubuntu (invalid `shade()`, `@sidebar_bg`, and
gtk-4.0 accent colors that incorrectly stayed blue).

## Dependencies

```bash
sudo apt update
sudo apt install -y python3
```

## Apply GTK4 CSS fixes (all themes)

```bash
python3 scripts/fix-gtk4-css.py
```

## Quick install (Red Darkest, recommended)

```bash
git clone https://github.com/shr00mie/flat-remix-gtk.git
cd flat-remix-gtk
./install-user-theme.sh Flat-Remix-GTK-Red-Darkest
gsettings set org.gnome.desktop.interface gtk-theme 'Flat-Remix-GTK-Red-Darkest'
gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'
gsettings set org.gnome.desktop.interface accent-color 'red'
```

This installs to `~/.local/share/themes/` and refreshes
`~/.config/gtk-4.0/` from the theme’s `libadwaita/` directory (required for
Nautilus / libadwaita apps).

## Pair with shell + icons

- Shell: [flat-remix-gnome](https://github.com/shr00mie/flat-remix-gnome)
- Icons: [flat-remix](https://github.com/shr00mie/flat-remix)

## Fixes included in this fork

- `shade()` → `mix()` for GTK4
- `@sidebar_bg` → `@sidebar_bg_color`
- Sync `accent_*` from `libadwaita/gtk.css` into `gtk-4.0/gtk.css`
- Drop GTK3-only `-gtk-icon-effect: dim`
- User install helper for XDG + libadwaita config
