#!/usr/bin/env bash
set -e

echo "[FFL] Creating Firefighter Linux LXC containers..."

lxc launch ubuntu:24.04 ffl-db || true
lxc launch ubuntu:24.04 ffl-api || true
lxc launch ubuntu:24.04 ffl-web || true
lxc launch ubuntu:24.04 ffl-repo || true

echo "[FFL] Container status:"
lxc list
