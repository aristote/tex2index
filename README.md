TeX2Index (Tex to Index) is a small script aiming at help people creating Indexes from scratch for Tex Files.
It uses Natural Language Processing in order to help detecting keyworks (called tokens) or simply dump all separate words from the source TeX file.

Because TeX files can be a bit complex, you can help tex2index to find the document's body by adding a ```%T2I-BEGIN```where you want TeX2index to start parsing your file. Otherwise it will try and look for the \begin tag.

```bash
▗▄▄▄▖     ▗▄ ▄▖ ▄▄▖  ▄▄▄         ▗▖
▝▀█▀▘      █▄█ ▐▀▀█▖ ▀█▀         ▐▌
  █   ▟█▙  ▐█▌    ▐▌  █  ▐▙██▖ ▟█▟▌ ▟█▙ ▝█ █▘
  █  ▐▙▄▟▌  █    ▗▛   █  ▐▛ ▐▌▐▛ ▜▌▐▙▄▟▌ ▐█▌
  █  ▐▛▀▀▘ ▐█▌  ▗▛    █  ▐▌ ▐▌▐▌ ▐▌▐▛▀▀▘ ▗█▖
  █  ▝█▄▄▌ █ █ ▗█▄▄▖ ▄█▄ ▐▌ ▐▌▝█▄█▌▝█▄▄▌ ▟▀▙
  ▀   ▝▀▀ ▝▀ ▀▘▝▀▀▀▘ ▀▀▀ ▝▘ ▝▘ ▝▀▝▘ ▝▀▀ ▝▀ ▀▘

usage: tex2index.py [-h] [--finalise] [--verbose] [--notext] [--nlp]
                    [--footnotes] [--purge]
                    input db

TeX index Generation script.

positional arguments:
  input        TeX filename to parse.
  db           database name to use (will be created if it does not exist)

optional arguments:
  -h, --help   show this help message and exit
  --finalise   Generate the final TeX file
  --verbose    Display verbose informations
  --notext     Do not index individual words
  --nlp        Use Natural Language Processing (slow)
  --footnotes  Indexes footnotes
  --purge      Purge the index table.
```
