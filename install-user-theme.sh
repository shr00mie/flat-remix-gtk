#!/usr/bin/env bash
# Install a Flat-Remix GTK theme for the current user (XDG + libadwaita).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
THEME_NAME="${1:-Flat-Remix-GTK-Red-Darkest}"
THEME_SRC="$ROOT/themes/$THEME_NAME"
TARGET="${TARGET:-$HOME/.local/share/themes}"
GTK4_CONFIG="${GTK4_CONFIG:-$HOME/.config/gtk-4.0}"

if [ ! -d "$THEME_SRC" ]; then
  echo "install-user-theme: theme not found: $THEME_SRC" >&2
  echo "Available:" >&2
  ls "$ROOT/themes" | sed 's/^/  /' >&2
  exit 1
fi

# Ensure GTK4 CSS fixes are applied (idempotent).
if [ -x "$ROOT/scripts/fix-gtk4-css.py" ]; then
  python3 "$ROOT/scripts/fix-gtk4-css.py" "$THEME_SRC"
fi

mkdir -p "$TARGET"
rm -rf "$TARGET/$THEME_NAME"
cp -a "$THEME_SRC" "$TARGET/$THEME_NAME"

# Libadwaita apps read ~/.config/gtk-4.0 (theme install.sh convention).
if [ -d "$THEME_SRC/libadwaita" ]; then
  mkdir -p "$GTK4_CONFIG"
  cp -a "$THEME_SRC/libadwaita/." "$GTK4_CONFIG/"
  # Keep a small settings.ini preferring dark when installing darkest/dark themes.
  if [[ "$THEME_NAME" == *Dark* ]]; then
    cat > "$GTK4_CONFIG/settings.ini" <<'EOF'
[Settings]
gtk-application-prefer-dark-theme=1
EOF
  fi
  echo "install-user-theme: refreshed $GTK4_CONFIG from libadwaita/"
fi

echo "install-user-theme: installed $THEME_NAME -> $TARGET/$THEME_NAME"
echo "install-user-theme: apply with:"
echo "  gsettings set org.gnome.desktop.interface gtk-theme '$THEME_NAME'"
echo "  gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'"
