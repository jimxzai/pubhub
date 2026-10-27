#!/bin/bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36"
for spec in 1:17 2:17 3:11 4:16 5:16 6:13 7:13 8:14; do
  c=${spec%:*}; n=${spec#*:}
  for v in $(seq 1 $n); do
    f=$c-$v.html
    [ -s $f ] && grep -q vheading2 $f && continue
    for try in 1 2 3 4; do
      code=$(curl -s -m 40 -A "$UA" -o $f -w "%{http_code}" https://biblehub.com/commentaries/songs/$c-$v.htm)
      if [ "$code" = 200 ] && grep -q vheading2 $f; then break; fi
      sleep $((try*10))
    done
    echo "$c:$v $code $(wc -c <$f)"
    sleep 2.5
  done
done
echo DONE
