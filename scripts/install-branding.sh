#!/bin/bash

echo "Installing Firefighter Linux branding..."

REPO_DIR="$HOME/FirefighterLinux"

# os-release
sudo cp "$REPO_DIR/branding/os-release/firefighter-os-release" /etc/os-release

# GRUB
sudo cp "$REPO_DIR/branding/grub/grub.conf" /etc/default/grub

if mount | grep -q "overlay"; then
    echo "Live/overlay system detected. Skipping update-grub and update-initramfs."
else
    sudo update-grub
fi

# Plymouth
sudo cp -r "$REPO_DIR/branding/plymouth/firefighterlinux" /usr/share/plymouth/themes/

sudo update-alternatives --install \
/usr/share/plymouth/themes/default.plymouth default.plymouth \
/usr/share/plymouth/themes/firefighterlinux/firefighterlinux.plymouth 100

sudo update-alternatives --set default.plymouth \
/usr/share/plymouth/themes/firefighterlinux/firefighterlinux.plymouth

if mount | grep -q "overlay"; then
    echo "Live/overlay system detected. Skipping update-initramfs."
else
    sudo update-initramfs -u
fi

# Wallpaper
sudo mkdir -p /usr/share/backgrounds/firefighterlinux
sudo cp "$REPO_DIR"/branding/wallpapers/* /usr/share/backgrounds/firefighterlinux/

# LightDM
sudo cp "$REPO_DIR/branding/lightdm/lightdm-gtk-greeter.conf" /etc/lightdm/

echo "Firefighter Linux branding installed."
