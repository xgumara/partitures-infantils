#!/usr/bin/env python3
"""Genera partitures (fitxer .ly + PDF) i l'índex web a partir de melodies senzilles.

Ús (des de la carpeta tools/):
  python3 generate.py                          # processa totes les cançons de songs/
  python3 generate.py songs/canço/canço.txt    # processa una cançó concreta
  python3 generate.py -o /tmp/prova songs/canço/canço.txt   # escriu la sortida en un altre directori

Cada cançó viu en una carpeta dins de songs/ (per exemple songs/gegant-del-pi/)
amb el fitxer d'entrada .txt, el .ly generat (notes acolorides + noms DO-RE-MI)
i el .pdf compilat amb lilypond. Aquesta carpeta és la web de GitHub Pages.
Al final es regenera songs/index.html amb totes les cançons.

Format d'un fitxer de cançó (songs/xxx.txt):

  # títol opcional
  title = El Gegant del Pi
  time = 4/4            # mètrica
  partial = 4           # anacrusa (opcional, ometre si no n'hi ha)
  magnify = 1.8         # mida del pentagrama
  spacing = 1.5         # separació entre notes
  system-distance = 40  # separació entre sistemes
  lyric-padding = 2.5   # separació lletra-pentagrama

  melodia:
  e'8 f'8 g'4 e'4 c'4 |
  f'8 e'8 d'8 c'8 d'8 d'8 e'8 c'8 |
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SONGS = BASE / "songs"
WEB = SONGS

COLOR = {"c": "doColor", "d": "reColor", "e": "miColor", "f": "faColor",
         "g": "solColor", "a": "laColor", "b": "siColor"}
NOM = {"c": "DO", "d": "RE", "e": "MI", "f": "FA", "g": "SOL", "a": "LA", "b": "SI"}

NOTE_RE = re.compile(r"^([a-g])([',]*)(\d*)(\.*)(~*)$")

DEFAULTS = {
    "key": "c \\major",
    "time": "4/4",
    "partial": None,
    "magnify": "1.8",
    "spacing": "1.5",
    "system-distance": "40",
    "system-distance-min": "32",
    "lyric-padding": "2.5",
    "lyric-distance": "14",
    "lyric-distance-min": "11",
}


def parse_spec(path):
    spec = dict(DEFAULTS)
    melody = []
    in_melody = False
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.lower().startswith("melodia:"):
            in_melody = True
            continue
        if in_melody:
            melody.extend(line.split())
        elif "=" in line:
            key, _, value = line.partition("=")
            spec[key.strip().lower()] = value.strip()
    spec.setdefault("title", path.stem.replace("-", " ").title())
    return spec, melody


def build_melody(tokens):
    lines = []
    cur = []
    syllables = []

    def flush():
        if cur:
            lines.append("  " + " ".join(cur))
            cur.clear()

    for tok in tokens:
        if tok == "\\bar":
            flush()
            cur.append(tok)
            continue
        m = NOTE_RE.match(tok)
        if m:
            letter = m.group(1)
            syllables.append(letter)
            cur.append("\\tweak color \\%s %s" % (COLOR[letter], tok))
        else:
            cur.append(tok)
        if tok == "|" or len(cur) >= 4:
            flush()
    flush()
    return lines, syllables


def build_noms(syllables):
    lines = []
    for i in range(0, len(syllables), 4):
        chunk = syllables[i:i + 4]
        lines.append("  " + " ".join(
            '\\tweak color \\%s "%s"' % (COLOR[s], NOM[s]) for s in chunk))
    return lines


def render_ly(spec, melody_lines, noms_lines):
    p = spec
    parts = [
        '\\version "2.26.0"',
        "",
        "% Colors de l'arc de Sant Martí",
        "#(define doColor  '(1.00 0.00 0.00))  % vermell",
        "#(define reColor  '(1.00 0.45 0.00))  % taronja",
        "#(define miColor  '(0.98 0.78 0.00))  % groc",
        "#(define faColor  '(0.12 0.60 0.12))  % verd",
        "#(define solColor '(0.00 0.40 0.90))  % blau",
        "#(define laColor  '(0.35 0.20 0.80))  % blau índigo",
        "#(define siColor  '(0.98 0.45 0.70))  % rosa",
        "",
        "% Pinta cada cap de nota segons el seu grau",
        "melodia = {",
        "  \\key %s" % p["key"],
        "  \\time %s" % p["time"],
        "  \\override Stem.thickness = #2.5",
    ]
    if p["partial"]:
        parts.extend(["", "  \\partial %s" % p["partial"]])
    parts += melody_lines
    parts += [
        "}",
        "",
        "noms = \\lyricmode {",
        "  \\override LyricText.font-size = #4",
        "  \\override LyricText.font-series = #'bold",
    ]
    parts += noms_lines
    parts += [
        "}",
        "",
        "\\header {",
        '  title = \\markup { \\fontsize #4 "%s" }' % p["title"],
        "  tagline = ##f",
        "}",
        "",
        "\\paper {",
        '  #(set-paper-size "a4landscape")',
        "  top-margin = 1.5\\cm",
        "  bottom-margin = 1.5\\cm",
        "  left-margin = 1.5\\cm",
        "  right-margin = 1.5\\cm",
        "  ragged-last-bottom = ##t",
        "  markup-system-spacing.basic-distance = 16",
        "  markup-system-spacing.minimum-distance = 12",
        "  system-system-spacing.basic-distance = %s" % p["system-distance"],
        "  system-system-spacing.minimum-distance = %s" % p["system-distance-min"],
        "}",
        "",
        "\\score {",
        "  <<",
        "    \\new Staff \\with {",
        "      \\magnifyStaff #%s" % p["magnify"],
        "      \\override StaffSymbol.line-thickness = #1.2",
        "    } <<",
        '      \\new Voice = "mel" { \\melodia }',
        "    >>",
        '    \\new Lyrics \\lyricsto "mel" \\noms',
        "  >>",
        "  \\layout {",
        "    \\context {",
        "      \\Score",
        "      \\override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/4)",
        "      \\override SpacingSpanner.spacing-increment = #%s" % p["spacing"],
        "    }",
        "    \\context {",
        "      \\Lyrics",
        "      \\override LyricText.padding = #%s" % p["lyric-padding"],
        "      \\override VerticalAxisGroup.nonstaff-relatedstaff-spacing.basic-distance = #%s" % p["lyric-distance"],
        "      \\override VerticalAxisGroup.nonstaff-relatedstaff-spacing.minimum-distance = #%s" % p["lyric-distance-min"],
        "    }",
        "  }",
        "}",
    ]
    return "\n".join(parts) + "\n"


def generate(spec_path, out_dir=None):
    target = Path(out_dir).resolve() if out_dir else spec_path.parent
    target.mkdir(parents=True, exist_ok=True)
    spec, melody = parse_spec(spec_path)
    mel_lines, syllables = build_melody(melody)
    noms_lines = build_noms(syllables)
    ly_path = target / (spec_path.stem + ".ly")
    ly_path.write_text(render_ly(spec, mel_lines, noms_lines))
    print("-> %s" % ly_path.relative_to(BASE))
    try:
        subprocess.run(["lilypond", "--pdf", "-o", str(ly_path.with_suffix("")), str(ly_path)],
                       cwd=str(target), check=True,
                       capture_output=True, text=True)
        print("   PDF generat")
    except subprocess.CalledProcessError as e:
        print("   ERROR: lilypond ha fallat", file=sys.stderr)
        print(e.stdout, file=sys.stderr)
        print(e.stderr, file=sys.stderr)


def generate_index():
    (WEB / ".nojekyll").touch(exist_ok=True)
    songs = []
    for d in sorted(p for p in WEB.iterdir() if p.is_dir()):
        if (d / (d.name + ".pdf")).exists():
            songs.append(d.name)
    cards = []
    for name in songs:
        title = name.replace("-", " ").title()
        base = "%s/%s" % (name, name)
        ly_link = ('<a class="btn" href="%s.ly" download>Codi font (.ly)</a>'
                   % base) if (WEB / name / (name + ".ly")).exists() else ""
        txt_link = ('<a class="btn" href="%s.txt" download>Font senzilla (.txt)</a>'
                    % base) if (WEB / name / (name + ".txt")).exists() else ""
        cards.append(
            '      <article class="score">\n'
            '        <h2>%s</h2>\n'
            '        <div class="links">\n'
            '          <a class="btn primary" href="%s.pdf" download>Baixa el PDF</a>\n'
            '          %s\n'
            '          %s\n'
            '        </div>\n'
            '      </article>' % (title, base, ly_link, txt_link))
    html = """<!DOCTYPE html>
<html lang="ca">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Partitures</title>
  <style>
    :root { --bg:#f7f7f5; --ink:#222; --accent:#d2483e; --muted:#666; }
    * { box-sizing:border-box; }
    body { margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
           background:var(--bg); color:var(--ink); }
    header { padding:3rem 1.5rem 1rem; text-align:center; }
    header h1 { margin:0; font-size:2.2rem; }
    header p { color:var(--muted); }
    main { max-width:860px; margin:0 auto; padding:1.5rem; display:grid;
           grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:1rem; }
    .score { background:#fff; border:1px solid #e3e1dc; border-radius:10px; padding:1.25rem; }
    .score h2 { margin:0 0 1rem; font-size:1.1rem; }
    .links { display:flex; gap:.5rem; flex-wrap:wrap; }
    .btn { text-decoration:none; padding:.55rem .9rem; border-radius:8px;
           font-size:.9rem; border:1px solid #d8d5cf; color:var(--ink); }
    .btn:hover { border-color:#b3afa7; }
    .btn.primary { background:var(--accent); border-color:var(--accent); color:#fff; }
    .btn.primary:hover { opacity:.9; }
    footer { text-align:center; color:var(--muted); padding:2rem 1rem; font-size:.85rem; }
  </style>
</head>
<body>
  <header>
    <h1>Partitures</h1>
    <p>Cançons infantils amb notes acolorides per a aprendre a tocar-les</p>
  </header>
  <main>
%s
  </main>
  <footer>Fet amb LilyPond</footer>
</body>
</html>
""" % ("\n".join(cards))
    (WEB / "index.html").write_text(html)
    print("index.html actualitzat")


def main():
    parser = argparse.ArgumentParser(description="Genera partitures i l'índex web.")
    parser.add_argument("specs", nargs="*", help="fitxers de cançó (per defecte: tots els de songs/)")
    parser.add_argument("-o", "--out", default=None, help="directori de sortida")
    args = parser.parse_args()

    out_dir = Path(args.out).resolve() if args.out else None
    if args.specs:
        specs = [Path(s) for s in args.specs]
    else:
        specs = sorted(SONGS.glob("*/*.txt"))
    if not specs:
        print("No hi ha cap cançó a %s ni has indicat cap fitxer." % SONGS)
        sys.exit(1)

    for s in specs:
        generate(s, out_dir)
    if args.out is None:
        generate_index()


if __name__ == "__main__":
    main()
