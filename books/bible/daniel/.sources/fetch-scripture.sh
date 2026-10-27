#!/bin/bash
# Fetch Daniel 1-12 from the sources the Ezra build used.
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15"
cd "$(dirname "$0")"
for n in $(seq 1 12); do
  nn=$(printf %02d $n)
  curl -s -m 30 -A "$UA" "https://bible.fhl.net/json/qb.php?chineses=%E4%BD%86&chap=$n&version=unv&gb=0" -o cuv/fhl-unv-$nn.json
  curl -s -m 30 -A "$UA" "https://cnbible.com/daniel/$n.htm" -o cnbible/$n.htm
  curl -s -m 30 -A "$UA" "https://biblehub.com/nasb/daniel/$n.htm" -o nasb/biblehub-$nn.htm
  curl -s -m 30 "https://www.sefaria.org/api/texts/Daniel.$n?context=0&commentary=0&lang=he&vhe=Miqra_according_to_the_Masorah" -o hebrew/sefaria-$n.json
  for try in 1 2 3 4; do
    curl -s -m 30 -A "$UA" "https://www.ai-eden.com/api/bible/daniel/$n?t=CUV,NASB" -o cuv/aieden-$nn.json
    grep -q '"success":true' cuv/aieden-$nn.json && break
    sleep 20
  done
  echo "ch $n done"; sleep 6
done
