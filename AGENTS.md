# Partitures — notes de treball

Repositori: `git@github.com:xgumara/partitures-infantils.git` (branca principal: `main`)
Web publicada: `https://xgumara.github.io/partitures-infantils/`

## Estructura
- `songs/<cançó>/` — una carpeta per cançó amb `.txt` (entrada), `.ly` (LilyPond) i `.pdf`. És el contingut de la web.
- `tools/generate.py` — genera `.ly`, `.pdf` i `index.html` a partir dels `.txt`.
- `tools/publish.sh` — genera tot i publica la web.

## Comandes
- Generar partitures: `python3 tools/generate.py`
- Publicar la web: `./tools/publish.sh` (commit a main + push de la branca `gh-pages`)

## Afegir una cançó
1. Crear `songs/<cançó>/<cançó>.txt` amb: `title`, `time`, opcionals `partial`, `magnify`, `spacing`, `system-distance`, `lyric-padding`, i el bloc `melodia:` amb notes planes (ex. `e'8 f'8 g'4 c'4 |`) i barres `|`.
2. `python3 tools/generate.py`
3. `./tools/publish.sh`

## Desplegament
- GitHub Pages es publica des de la branca `gh-pages` (arrel `/`), sense GitHub Actions.
- `TODO.md` està a `.gitignore` (no es puja).
