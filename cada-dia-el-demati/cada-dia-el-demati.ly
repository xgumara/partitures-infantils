\version "2.26.0"

% Colors de l'arc de Sant Martí
#(define doColor  '(1.00 0.00 0.00))  % vermell
#(define reColor  '(1.00 0.45 0.00))  % taronja
#(define miColor  '(0.98 0.78 0.00))  % groc
#(define faColor  '(0.12 0.60 0.12))  % verd
#(define solColor '(0.00 0.40 0.90))  % blau
#(define laColor  '(0.35 0.20 0.80))  % blau índigo
#(define siColor  '(0.98 0.45 0.70))  % rosa

% Pinta cada cap de nota segons el seu grau
melodia = {
  \key c \major
  \time 2/4
  \override Stem.thickness = #2.5

  \partial 4
  \tweak color \doColor c'8 \tweak color \doColor c'8 \tweak color \solColor g'8 \tweak color \solColor g'8
  \tweak color \laColor a'8 \tweak color \laColor a'8 |
  \tweak color \solColor g'4 \tweak color \faColor f'8 \tweak color \faColor f'8 |
  \tweak color \miColor e'8 \tweak color \miColor e'8 \tweak color \reColor d'8 \tweak color \reColor d'8
  |
  \tweak color \doColor c'4 \tweak color \solColor g'8 \tweak color \solColor g'8 |
  \tweak color \faColor f'8 \tweak color \faColor f'8 \tweak color \miColor e'8 \tweak color \miColor e'8
  |
  \tweak color \miColor e'8 \tweak color \reColor d'8 \tweak color \solColor g'8 \tweak color \solColor g'8
  |
  \tweak color \faColor f'8 \tweak color \faColor f'8 \tweak color \miColor e'8 \tweak color \miColor e'8
  |
  \tweak color \miColor e'8 \tweak color \reColor d'8 \tweak color \doColor c'8 \tweak color \doColor c'8
  |
  \tweak color \solColor g'8 \tweak color \solColor g'8 \tweak color \laColor a'8 \tweak color \laColor a'8
  |
  \tweak color \solColor g'4 \tweak color \faColor f'8 \tweak color \faColor f'8 |
  \tweak color \miColor e'8 \tweak color \miColor e'8 \tweak color \reColor d'8 \tweak color \reColor d'8
  |
  \tweak color \doColor c'4
  \bar "|."
}

noms = \lyricmode {
  \override LyricText.font-size = #4
  \override LyricText.font-series = #'bold
  \tweak color \doColor "DO" \tweak color \doColor "DO" \tweak color \solColor "SOL" \tweak color \solColor "SOL"
  \tweak color \laColor "LA" \tweak color \laColor "LA" \tweak color \solColor "SOL" \tweak color \faColor "FA"
  \tweak color \faColor "FA" \tweak color \miColor "MI" \tweak color \miColor "MI" \tweak color \reColor "RE"
  \tweak color \reColor "RE" \tweak color \doColor "DO" \tweak color \solColor "SOL" \tweak color \solColor "SOL"
  \tweak color \faColor "FA" \tweak color \faColor "FA" \tweak color \miColor "MI" \tweak color \miColor "MI"
  \tweak color \miColor "MI" \tweak color \reColor "RE" \tweak color \solColor "SOL" \tweak color \solColor "SOL"
  \tweak color \faColor "FA" \tweak color \faColor "FA" \tweak color \miColor "MI" \tweak color \miColor "MI"
  \tweak color \miColor "MI" \tweak color \reColor "RE" \tweak color \doColor "DO" \tweak color \doColor "DO"
  \tweak color \solColor "SOL" \tweak color \solColor "SOL" \tweak color \laColor "LA" \tweak color \laColor "LA"
  \tweak color \solColor "SOL" \tweak color \faColor "FA" \tweak color \faColor "FA" \tweak color \miColor "MI"
  \tweak color \miColor "MI" \tweak color \reColor "RE" \tweak color \reColor "RE" \tweak color \doColor "DO"
}

\header {
  title = \markup { \fontsize #4 "Cada Dia Al Dematí" }
  tagline = ##f
}

\paper {
  #(set-paper-size "a4landscape")
  top-margin = 1.5\cm
  bottom-margin = 1.5\cm
  left-margin = 1.5\cm
  right-margin = 1.5\cm
  ragged-last-bottom = ##t
  markup-system-spacing.basic-distance = 16
  markup-system-spacing.minimum-distance = 12
  system-system-spacing.basic-distance = 40
  system-system-spacing.minimum-distance = 32
}

\score {
  <<
    \new Staff \with {
      \magnifyStaff #1.8
      \override StaffSymbol.line-thickness = #1.2
    } <<
      \new Voice = "mel" { \melodia }
    >>
    \new Lyrics \lyricsto "mel" \noms
  >>
  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/4)
      \override SpacingSpanner.spacing-increment = #1.5
    }
    \context {
      \Lyrics
      \override LyricText.padding = #2.5
      \override VerticalAxisGroup.nonstaff-relatedstaff-spacing.basic-distance = #14
      \override VerticalAxisGroup.nonstaff-relatedstaff-spacing.minimum-distance = #11
    }
  }
}
