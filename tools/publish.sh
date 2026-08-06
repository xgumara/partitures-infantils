#!/bin/bash
# Genera les partitures i actualitza la branca gh-pages (la web publicada).
set -e
cd "$(dirname "$0")/.."

python3 tools/generate.py

git add songs
if ! git diff --cached --quiet; then
  git commit -m "Actualitza partitures"
fi

git worktree add .gh-pages-tmp gh-pages
rm -rf .gh-pages-tmp/*
cp -R songs/. .gh-pages-tmp/
git -C .gh-pages-tmp add -A
if ! git -C .gh-pages-tmp diff --cached --quiet; then
  git -C .gh-pages-tmp commit -m "Publica la web"
  git -C .gh-pages-tmp push origin gh-pages
else
  echo "La web no ha canviat: no cal publicar."
fi
git worktree remove .gh-pages-tmp
