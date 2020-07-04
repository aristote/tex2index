#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import argparse
import sqlite3
from progress.bar import ShadyBar
from pylatexenc.latex2text import LatexNodes2Text

#python -m spacy download fr_core_news_sm

print("""
▗▄▄▄▖     ▗▄ ▄▖ ▄▄▖  ▄▄▄         ▗▖
▝▀█▀▘      █▄█ ▐▀▀█▖ ▀█▀         ▐▌
  █   ▟█▙  ▐█▌    ▐▌  █  ▐▙██▖ ▟█▟▌ ▟█▙ ▝█ █▘
  █  ▐▙▄▟▌  █    ▗▛   █  ▐▛ ▐▌▐▛ ▜▌▐▙▄▟▌ ▐█▌
  █  ▐▛▀▀▘ ▐█▌  ▗▛    █  ▐▌ ▐▌▐▌ ▐▌▐▛▀▀▘ ▗█▖
  █  ▝█▄▄▌ █ █ ▗█▄▄▖ ▄█▄ ▐▌ ▐▌▝█▄█▌▝█▄▄▌ ▟▀▙
  ▀   ▝▀▀ ▝▀ ▀▘▝▀▀▀▘ ▀▀▀ ▝▘ ▝▘ ▝▀▝▘ ▝▀▀ ▝▀ ▀▘
""")

#### Menu building ###############################################################################
parser = argparse.ArgumentParser(description='Génération d\'index TeX.')
parser.add_argument("input", help="Nom du fichier TeX à parcourir.")
parser.add_argument("db", help="Nom de la base d'index à créer ou utiliser")
parser.add_argument("--finalise", action="store_true", help="Générer le fichier TeX final")
parser.add_argument("--verbose", action="store_true", help="Afficher des informations supplémentaires")
parser.add_argument("--notext", action="store_true", help="N'indexe pas les mots individuels")
parser.add_argument("--nlp", action="store_true", help="Lance le traitement automatique du langage naturel (lent)")
parser.add_argument("--footnotes", action="store_true", help="Indexe les notes de bas de page")
parser.add_argument("--purge", action="store_true", help="Purge la table d'index.")
args = parser.parse_args()
##################################################################################################
# -- display debug information is --verbose
def verbose(text):
    if args.verbose:
        print('➜ ',text)

# -- populating variables from command line parameters
inputfile= args.input
outputdb = args.db 
verbose("Ouverture du fichier")
num_lines = sum(1 for line in open(inputfile))

verbose("File line count:" + str(num_lines))
verbose("Connecting to the database")

conn = sqlite3.connect(outputdb)
db = conn.cursor()

def findTeXstart():
    open_file.seek(0,0)
    verbose("Scanning for %T2I-BEGIN")
    file_to_string = open_file.read()
    try:
        start = re.search(r'\%T2I\-BEGIN', file_to_string, re.M).start()
    except:
        start=0
        pass
    if start > 0:
        verbose("%T2I-BEGIN Found at offset: " + str(start))
    else:
        open_file.seek(0,0)
        verbose("%T2I-BEGIN not found, scanning for \\begin{}")
        file_to_string = open_file.read()
        try:
            start = re.search(r'\\begin\{.*?\}', file_to_string, re.M).start()
        except:
            start=0
            pass
        if start > 0:
            verbose("Found at offset: " + str(start))
        else:
            verbose("Not Found: starting from line 0")
    return int(start)

#### Opening the file and searching for \begin
open_file = open(inputfile, 'r')
start = findTeXstart()
open_file.seek(0,0)
#### Finalise ####################################################################################
# --- The BIG loop where we put everything together for the final Tex File
#\lieux{Ay : village de Champagne} 
if args.finalise:
    finalfile = args.input + ".final.tex"
    header = open_file.read()[:start]
    open_file.seek(0,0)
    final = open_file.read()[start:]
    query = '''SELECT token, type, information FROM texindex WHERE active = 1'''
    num_row = db.execute(query)
    num_row = len(num_row.fetchall())
    bar = ShadyBar('Processing', max=num_row)
    for row in db.execute(query):
        row_re = re.escape(row[0]) + "(?![^{]*})"
        row_sub = row[0] + "\\\\" + "index" +"{" + row[0] + " : " + row[2] + "}"
        final = re.sub(row_re, row_sub, final, re.M)
        bar.next()
    bar.finish()
    print("Done")
    final_file = open(finalfile, "w")
    final_file.write(header)
    final_file.write(final)
    final_file.close() 
    exit(1)

#### Reading the file before parsing it ##########################################################
file_to_string = open_file.read()[start:]
# if we use the --nofoot, we also remove footnotes before parsing the TeX file
if not args.footnotes:
    verbose("Removing footnotes.")
    footnotes_re = re.compile(r'\\footnote\{.*?\}|\\endnote\{.*?\}|\\autocites\{.*?\}|\\autocite\{.*?\}')
    file_to_string = footnotes_re.sub(r'', file_to_string)
else:
    verbose("Leaving footnotes.")
verbose("Cleaning text from TeX Marking")
string_to_text = LatexNodes2Text().latex_to_text(file_to_string)
words = re.findall(r'(\b[A-Za-z][a-z]{0,50}\b)', string_to_text)

    
# -- database connection and table cleaning

#### purge #######################################################################################
if args.purge:
    verbose("Purging texindex table")
    db.execute('''DROP TABLE IF EXISTS texindex''')
    conn.commit()
verbose("Checking tables")
db.execute('''CREATE TABLE IF NOT EXISTS texindex (token NOT NULL, active DEFAULT 1,len INTEGER NOT NULL, type TEXT, information TEXT, PRIMARY KEY (token))''')
conn.commit()
#### nlp #########################################################################################
# -- if --nlp then we import spacy and process again the text with Natural Language Processing
# Results will be sent to the nlp table

if args.nlp:
    verbose("Entering NLP processing (this might take a while)")
    verbose("    loading nlp set")
    import spacy
    from spacy import displacy
    nlp = spacy.load('fr_core_news_lg')
    verbose("    done loading, processing for nlp")
    query = "INSERT OR IGNORE INTO texindex VALUES(?, ?, ?, ?, ? );"
    verbose("    Populating nlp table with nlp data")
    for X in nlp(string_to_text).ents:
        db.execute(query, (X.text, 1, len(X.text), X.label_, ""))
    conn.commit()
#### texindex ###################################################################################
# -- Populating texindex table with individual words
if not args.notext:
    verbose("Populating texindex table with individual words")
    for word in words:
        #print(word + ", ", end=""),
        query = "INSERT OR IGNORE INTO texindex VALUES(?, ?, ?, ?, ? );"
        db.execute(query, (word, 1, len(word), "", ""))
verbose("Commiting database")
conn.commit()
conn.close()
# -- cleanup and exiting --------------------------------- THE END -----------------------------
print("Done, exiting")