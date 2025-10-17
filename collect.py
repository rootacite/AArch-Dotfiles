#!/usr/bin/env python3
import os
import shutil
import subprocess
from pathlib import Path

def main():
    home = Path.home()
    dst = Path.cwd()

    print("Dumping GNOME settings...")
    try:
        with open(dst / "gnome-settings.ini", "w") as f:
            subprocess.run(
                ["dconf", "dump", "/org/gnome/"],
                check=True,
                stdout=f,
                stderr=subprocess.PIPE,
                text=True
            )
    except subprocess.CalledProcessError as e:
        print(f"⚠ Failed to dump GNOME settings: {e.stderr.strip()}")
        return

    include_paths = [
        ".config/ags",
        ".config/autostart",
        ".config/cava",
        ".config/gtk-3.0",
        ".config/gtk-4.0",
        ".config/gnome-shell",
        ".config/gnome-terminal",
        ".config/gnome-session",
        ".local/share/gnome-shell",
        ".themes",
        ".icons",
        ".fonts",
        "Fonts",
        ".local/share/icons",
        ".local/share/themes",
        ".config/hypr",
        ".config/waybar",
        ".config/wofi",
        ".config/swaylock",
        ".config/swaync",
        ".config/mako",
        ".config/hyprpaper",
        ".config/hypridle",
        ".config/starship.toml",
        ".config/zsh",
        ".zshrc",
        "startup.sh",
        ".bashrc",
        ".profile",
        ".bash_profile",
        ".local/share/backgrounds",
        ".gitignore",
        ".gitattributes",
        ".gitmodules",
        ".gitkeep",
        ".config/kitty",
        ".config/alacritty",
        ".config/wezterm",
        ".config/rofi",
        ".config/nvim",
        ".config/vim",
    ]

    print(f"\nExporting selected dotfiles from {home} to {dst} ...\n")

    for rel_path in include_paths:
        src_path = home / rel_path
        dst_path = dst / rel_path

        if src_path.exists():
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                if src_path.is_dir():
                    if dst_path.exists():
                        shutil.rmtree(dst_path)
                    shutil.copytree(src_path, dst_path, symlinks=True)
                else:
                    shutil.copy2(src_path, dst_path)
                print(f"✓ Copied: {rel_path}")
            except Exception as e:
                print(f"⚠ Error copying {rel_path}: {e}")
        else:
            print(f"⚠ Skipped (not found): {rel_path}")

if __name__ == "__main__":
    main()

