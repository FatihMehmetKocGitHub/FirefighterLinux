#!/bin/bash

MARKER="$HOME/.config/firefighter-welcome-disabled"
TEXT="$HOME/firefighter-welcome/welcome.txt"

[ -f "$MARKER" ] && exit 0

while true; do
    yad --text-info \
    --title="Firefighter Linux v1.0 - Hoş Geldiniz" \
    --width=760 \
    --height=620 \
    --center \
    --wrap \
    --fontname="Sans 11" \
    --filename="$TEXT" \
    --button="GitHub:2" \
    --button="Web Sitesi:3" \
    --button="KlavunOS:4" \
    --button="LinkedIn:5" \
    --button="Instagram:6" \
    --button="X:7" \
    --button="NSosyal:8" \
    --button="Bir daha gösterme:9" \
    --button="Kapat:0"

    case $? in
        2) xdg-open "https://github.com/FatihMehmetKocGitHub" ;;
        3) xdg-open "https://firefighterlinux.org" ;;
        4) xdg-open "https://boraklavun.blog/klavunos/" ;;
        5) xdg-open "https://tr.linkedin.com/in/fatihmehmetkoc" ;;
        6) xdg-open "https://www.instagram.com/fatihmehmet_koc/" ;;
        7) xdg-open "https://x.com/koc_fatihmehmet" ;;
        8) xdg-open "https://nsosyal.com/fatihmehmetkoc" ;;
        9) touch "$MARKER"; exit 0 ;;
        0) exit 0 ;;
        *) exit 0 ;;
    esac
done
