# Partitures

Partitures de cançons infantils tradicionals catalanes i populars, amb les notes
acolorides segons la nota musical (DO-RE-MI) perquè els infants les aprenguin de
manera visual.

Cada cançó inclou el **PDF** per imprimir, el **codi font LilyPond** (`.ly`) i el
fitxer d'entrada senzill (`.txt`). La web es publica automàticament a GitHub Pages
a partir de la carpeta `songs/`.

## Estructura

```
.
├── songs/                 # la web publicada a GitHub Pages
│   ├── index.html         # (regenerat automàticament)
│   └── <cançó>/           # una carpeta per cada cançó
│       ├── cançó.txt      # melodia en format senzill (entrada)
│       ├── cançó.ly       # partitura LilyPond (generada)
│       ├── cançó.pdf      # PDF per imprimir (generat)
│       └── cançó.png      # vista prèvia 4:3 (generada)
├── tools/
│   ├── generate.py        # genera les partitures i l'índex web
│   └── publish.sh         # publica la web a GitHub Pages
├── README.md
└── TODO.md                # cançons pendents (ignorat per git)
```

A la web només es publiquen el **PDF** i la **imatge de vista prèvia**: el `.ly` i
el `.txt` es mantenen al repositori però no són descarregables des de la web.

## Requisits

- [LilyPond](https://lilypond.org/) (per compilar els PDFs)
- Python 3

## Afegir una cançó

1. Crea una carpeta a `songs/` amb el nom de la cançó i dins el fitxer
   d'entrada, per exemple `songs/la-castanyera/la-castanyera.txt`:

   ```
   title = La Castanyera
   time = 2/4
   partial = 4          # només si comença amb anacrusa
   magnify = 1.8        # mida del pentagrama
   spacing = 1.5        # separació entre notes
   system-distance = 40 # separació entre sistemes
   lyric-padding = 2.5  # separació lletra-pentagrama

   melodia:
   d'8 d'8 e'8 f'8 |
   g'4 a'4 b'4 c''4 |
   ```

   A la melodia només cal escriure les notes planes (per exemple `e'8`, `g'4`,
   `c''2.`) i els compassos (`|`). El programa hi afegeix automàticament els
   colors i els noms DO-RE-MI.

2. Genera la partitura:

   ```
   python3 tools/generate.py
   ```

   Això crea el `.ly`, el `.pdf` i la imatge de vista prèvia a la carpeta de la
   cançó, i actualitza `songs/index.html`.

## Publicar a GitHub Pages

La web es publica des de la branca `gh-pages` (sense necessitat de GitHub Actions).
Per actualitzar-la, des de la carpeta del projecte:

```
./tools/publish.sh
```

Aquest script genera les partitures, desa els canvis a `main` i publica la web a
la branca `gh-pages`. La primera vegada (o si canvies de configuració), revisa a
GitHub:

1. A **Settings → Pages → Build and deployment**, selecciona *Deploy from a branch*.
2. Selecciona la branca **gh-pages** i la carpeta **/ (root)**.
3. La web queda publicada a `https://<usuari>.github.io/<repositori>/`.
4. Per fer servir un domini propi: afegeix un fitxer `CNAME` amb el domini dins
   de `songs/` (el publicarà `publish.sh`) i crea un registre CNAME al teu
   proveïdor de domini que apunti a `<usuari>.github.io`.
