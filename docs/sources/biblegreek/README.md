# Biblegreek — source corpus

`morphgnt/` holds the 27 files of MorphGNT SBLGNT (lemmatized, parsed Greek NT),
fetched 2026-11-01 with `curl` from
`https://raw.githubusercontent.com/morphgnt/sblgnt/master/<NN>-<Bk>-morphgnt.txt`.
Nothing typed from memory. Columns: ref, POS, parse, text(with punct), word, normalized, lemma.

All Greek counts and the John 1:1-5 parse in `books/bible/Biblegreek/` are computed
by `scripts/gen-biblegreek-data.py` from these files. Totals (this edition):
137,554 word tokens, 5,461 lemmas. (Other editions/counters give slightly different totals.)
