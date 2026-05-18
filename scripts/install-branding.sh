#!/bin/bash

echo "Installing Firefighter Linux branding..."

# os-release
sudo cp ~/FirefighterLinux/branding/os-release/firefighter-os-release /etc/os-release

# GRUB
sudo cp ~/FirefighterLinux/branding/grub/grub.conf /etc/default/grub
sudo update-grub

# Plymouth
sudo cp -r ~/FirefighterLinux/branding/plymouth/firefighterlinux /usr/share/plymouth/themes/

sudo update-alternatives --install \
/usr/share/plymouth/themes/default.plymouth default.plymouth \
/usr/share/plymouth/themes/firefighterlinux/firefighterlinux.plymouth 100

sudo update-alternatives --set default.plymouth \
/usr/share/plymouth/themes/firefighterlinux/firefighterlinux.plymouth

sudo update-initramfs -u

# Wallpaper
sudo mkdir -p /usr/share/backgrounds/firefighterlinux

sudo cp ~/FirefighterLinux/branding/wallpapers/* \
/usr/share/backgrounds/firefighterlinux/

# LightDM
sudo cp ~/FirefighterLinux/branding/lightdm/lightdm-gtk-greeter.conf \
/etc/lightdm/

echo "Firefighter Linux branding installed."
