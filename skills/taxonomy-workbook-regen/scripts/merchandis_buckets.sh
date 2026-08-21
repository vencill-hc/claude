#!/bin/zsh
# Bucket the merchandis* title population from the GDU titles corpus by shape,
# to test whether commercial merchandising is separable from buyer/procurement.
gzcat ~/Documents/git/workpod/assets/titles.ndjson.gz \
| grep -i merchandis \
| jq -r '[.job_title, .n] | @tsv' \
| awk -F'\t' '
  {
    t = tolower($1); n = $2; total += n
    if (t ~ /chief merchandis|cmo.*merchandis/)                        { b["1 chief merchandising"] += n }
    else if (t ~ /(vp|vice president|svp|evp)[^a-z]*(of )?merchandis/) { b["2 vp merchandising"] += n }
    else if (t ~ /head of merchandis/)                                 { b["3 head of merchandising"] += n }
    else if (t ~ /merchandis[a-z]* director|director[^a-z]*(of )?merchandis/) { b["4 merchandising director"] += n }
    else if (t ~ /visual merchandis/)                                  { b["5 visual merchandising"] += n }
    else if (t ~ /merchandise plan|merchandising plan/)                { b["6 merchandise planning"] += n }
    else if (t ~ /merchandis[a-z]* manager|manager[^a-z]*(of )?merchandis/) { b["7 merchandising manager"] += n }
    else if (t ~ /buy/)                                                { b["8 explicit buyer + merchandis"] += n }
    else                                                               { b["9 other (merchandiser etc.)"] += n }
  }
  END {
    printf "TOTAL\t%d\n", total
    for (k in b) printf "%s\t%d\t%.2f%%\n", k, b[k], 100*b[k]/total
  }' | sort
