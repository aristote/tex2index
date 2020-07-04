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

Génération d'index TeX.

positional arguments:
  input        Nom du fichier TeX à parcourir.
  db           Nom de la base d'index à créer ou utiliser

optional arguments:
  -h, --help   show this help message and exit
  --finalise   Générer le fichier TeX final
  --verbose    Afficher des informations supplémentaires
  --notext     N'indexe pas les mots individuels
  --nlp        Lance le traitement automatique du langage naturel (lent)
  --footnotes  Indexe les notes de bas de page
  --purge      Purge la table d'index.
```