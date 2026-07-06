"""
Formation Complete - Jour 2 - Fichiers, Pandas et SQL
Exercice apres chaque concept, ligne par ligne, dataset Beobank.
"""
import json, os
OUT = r"C:\Users\axiat\Desktop\orsys\Beobank\Formation_Complete"
os.makedirs(OUT, exist_ok=True)

def md(src):
    lines = src.strip().split('\n')
    s = [l + '\n' for l in lines[:-1]] + [lines[-1]]
    return {"cell_type": "markdown", "metadata": {}, "source": s}

def code(src):
    lines = src.strip().split('\n')
    s = [l + '\n' for l in lines[:-1]] + [lines[-1]]
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": s}

def nb(cells):
    return {"cells": cells,
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                         "language_info": {"name": "python", "version": "3.10.0"}},
            "nbformat": 4, "nbformat_minor": 5}

cells = [

# ════════════════════════════════════════════════════════
# PAGE DE GARDE
# ════════════════════════════════════════════════════════
md("""# Jour 2 · Fichiers, Pandas et SQL avec les données Beobank
### Formation Python 3 jours · 19 novembre 2026

---

## Objectifs du Jour 2

Hier vous avez appris les bases de Python. Aujourd'hui vous allez découvrir
**Pandas**, la bibliothèque qui remplace 90 % de votre code SAS.

## Comparaison SAS ↔ Pandas

| SAS | Pandas |
|-----|--------|
| `data work.CTR; set "CTR.csv"` | `ctr = pd.read_csv("CTR.csv")` |
| `proc print data=CTR(obs=5);` | `ctr.head(5)` |
| `proc means data=CTR;` | `ctr.describe()` |
| `proc freq data=CTR; tables COD_ECV_CTR;` | `ctr["COD_ECV_CTR"].value_counts()` |
| `proc sort data=CTR by SLD_CTR;` | `ctr.sort_values("SLD_CTR")` |
| `proc sql; select ... where COD_ECV_CTR='1';` | `ctr[ctr["COD_ECV_CTR"]=="1"]` |
| `data CTR2; set CTR; SEGMENT=...` | `ctr["SEGMENT"] = ...` |
| `proc sql; left join ...` | `pd.merge(..., how="left")` |

## Plan du Jour 2

1. Gestion de fichiers avec `pathlib`
2. Lire/écrire CSV, JSON, TXT
3. Charger les 5 tables Beobank avec Pandas
4. Explorer un DataFrame (head, info, describe...)
5. Sélectionner des colonnes et des lignes
6. Filtrer et trier
7. Colonnes calculées et transformations
8. Groupby et agrégations
9. Jointures (merge)
10. Export et connexion SQL (SQLite / Vertica)"""),

# ════════════════════════════════════════════════════════
# SECTION 1 · PATHLIB
# ════════════════════════════════════════════════════════
md("""---
# 1 · Gestion des chemins avec pathlib

`pathlib.Path` est la façon moderne de gérer les chemins de fichiers en Python.
Il remplace les anciennes concaténations de chaînes comme `"dossier" + "\\" + "fichier"`.

## Avantage : portable Windows/Mac/Linux

```python
# Ancienne méthode (fragile, Windows uniquement)
chemin = "C:\\Users\\axiat\\data\\CTR.csv"

# Méthode moderne avec pathlib (portable)
from pathlib import Path
chemin = Path("../Orsys") / "CTR.csv"
```"""),

code("""# ── Découvrir pathlib ────────────────────────────────────────
from pathlib import Path    # import du module standard

# Créer un objet Path
# Path("..") = dossier parent
# / est l'opérateur de concaténation de chemin (pas le slash de division !)
DATA = Path("../Orsys")    # chemin vers le dossier des données Beobank

# Vérifier l'existence
print(f"Le dossier existe : {DATA.exists()}")
print(f"C'est un dossier : {DATA.is_dir()}")
print()

# Lister les fichiers CSV dans le dossier
print("Fichiers CSV dans ../Orsys :")
for fichier in sorted(DATA.glob("*.csv")):    # glob() filtre par motif
    taille_ko = fichier.stat().st_size // 1024 + 1   # taille en Ko
    print(f"  {fichier.name:<25} {taille_ko:>5} Ko")
print()

# Propriétés d'un chemin
chemin_ctr = DATA / "CTR.csv"
print(f"Chemin complet : {chemin_ctr}")
print(f"Nom du fichier : {chemin_ctr.name}")
print(f"Extension      : {chemin_ctr.suffix}")
print(f"Dossier parent : {chemin_ctr.parent}")
print(f"Sans extension : {chemin_ctr.stem}")"""),

code("""# ── Créer des dossiers et gérer les sorties ──────────────────
from pathlib import Path

# Dossier de sortie pour nos rapports
SORTIE = Path("../Sorties_Beobank")

# mkdir(parents=True, exist_ok=True) :
# - parents=True : crée aussi les dossiers intermédiaires si nécessaire
# - exist_ok=True : ne lève pas d'erreur si le dossier existe déjà
SORTIE.mkdir(parents=True, exist_ok=True)
print(f"Dossier de sortie créé : {SORTIE.resolve()}")    # resolve() = chemin absolu

# Construire un chemin de fichier de rapport
import datetime
aujourd_hui = datetime.date.today().strftime("%Y%m%d")   # ex: "20261118"
chemin_rapport = SORTIE / f"rapport_mensuel_{aujourd_hui}.csv"
print(f"Rapport sera écrit dans : {chemin_rapport}")

# Lire un fichier entier (pour les fichiers texte petits)
# chemin.read_text(encoding="utf-8") retourne le contenu comme une chaîne
chemin_test = Path("../Orsys/CTR.csv")
if chemin_test.exists():
    contenu = chemin_test.read_text(encoding="utf-8")
    lignes   = contenu.split("\\n")     # split sur les sauts de ligne
    print(f"\\nCTR.csv : {len(lignes)} lignes")
    print(f"Première ligne (en-tête) : {lignes[0]}")
    print(f"Deuxième ligne (1ère donnée) : {lignes[1]}")"""),

# ── EXERCICE 1 ──────────────────────────────────────────────
md("""---
### 🟡 Exercice 1 · Pathlib Beobank

**À faire :**
1. Créer une variable `DATA = Path("../Orsys")`
2. Vérifier que les 5 fichiers existent (CTR, TIE, TIE_ADR, TIE_X_CTR, TXN_X_CTR)
3. Pour chaque fichier : afficher son nom, sa taille en Ko, et le nombre de lignes
4. Calculer et afficher le nombre total de lignes dans tous les fichiers combinés"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────
from pathlib import Path

DATA = Path("../Orsys")
FICHIERS = ["CTR.csv", "TIE.csv", "TIE_ADR.csv", "TIE_X_CTR.csv", "TXN_X_CTR.csv"]

total_lignes = 0

print(f"{'Fichier':<20}  {'Existe':>6}  {'Ko':>5}  {'Lignes':>8}")
print("-" * 46)

for nom in FICHIERS:
    chemin = DATA / nom
    # vérifier existence, taille, compter les lignes
    ...

print("-" * 46)
print(f"Total lignes : {total_lignes}")"""),

md("""**✅ Correction exercice 1 :**"""),

code("""# ✅ CORRECTION exercice 1 ──────────────────────────────────
from pathlib import Path

DATA     = Path("../Orsys")
FICHIERS = ["CTR.csv", "TIE.csv", "TIE_ADR.csv", "TIE_X_CTR.csv", "TXN_X_CTR.csv"]

total_lignes = 0

print(f"{'Fichier':<22}  {'Existe':>6}  {'Ko':>5}  {'Lignes':>8}")
print("-" * 50)

for nom in FICHIERS:
    chemin  = DATA / nom
    existe  = chemin.exists()
    taille  = chemin.stat().st_size // 1024 + 1 if existe else 0

    if existe:
        # compter les lignes : lire et splitter sur le saut de ligne
        # len() - 1 pour ne pas compter la ligne d'en-tête
        contenu  = chemin.read_text(encoding="utf-8")
        nb_lignes = len([l for l in contenu.split("\\n") if l.strip()]) - 1  # -1 pour l'en-tête
    else:
        nb_lignes = 0

    total_lignes += nb_lignes
    flag = "✓" if existe else "✗"
    print(f"{nom:<22}  {flag:>6}  {taille:>5}  {nb_lignes:>8}")

print("-" * 50)
print(f"{'TOTAL':<22}  {'':>6}  {'':>5}  {total_lignes:>8} enregistrements")"""),

# ════════════════════════════════════════════════════════
# SECTION 2 · LIRE/ÉCRIRE CSV JSON TXT
# ════════════════════════════════════════════════════════
md("""---
# 2 · Lire et écrire des fichiers (CSV, JSON, TXT)

Avant Pandas, Python a ses propres outils de lecture/écriture.
Ces modules sont utiles pour les petits fichiers et les fichiers non-tabulaires."""),

code("""# ── Lire un CSV avec le module csv ───────────────────────────
import csv
from pathlib import Path

DATA = Path("../Orsys")

print("=== Lecture de TIE.csv avec le module csv ===")
print()

with open(DATA / "TIE.csv", "r", encoding="utf-8") as f:
    # DictReader : chaque ligne est un dictionnaire {colonne: valeur}
    lecteur = csv.DictReader(f, delimiter=";")

    # Afficher l'en-tête
    colonnes = lecteur.fieldnames
    print(f"Colonnes ({len(colonnes)}) : {colonnes}")
    print()

    # Lire les 5 premières lignes
    print(f"{'IDT_PI':<10}  {'NUM_TIE':<12}  {'TYP':>3}  {'SEX':>3}  {'LNG':>3}")
    print("-" * 40)
    for i, ligne in enumerate(lecteur):
        if i >= 5:     # limiter à 5 lignes pour la démo
            break
        print(f"{ligne['IDT_PI']:<10}  {ligne['NUM_TIE']:<12}  "
              f"{ligne['COD_TYP_TIE']:>3}  "
              f"{ligne.get('COD_SEX','?') or '?':>3}  "
              f"{ligne['COD_LNG_CTR']:>3}")"""),

code("""# ── Écrire un CSV ────────────────────────────────────────────
import csv
from pathlib import Path

SORTIE = Path("../Sorties_Beobank")
SORTIE.mkdir(exist_ok=True)

# Données à exporter : résumé des statuts
resume_statuts = [
    {"Code": "1", "Libelle": "Ouvert",         "Categorie": "Actif",   "Nb": 87},
    {"Code": "2", "Libelle": "En attente",      "Categorie": "Actif",   "Nb": 12},
    {"Code": "3", "Libelle": "Suspendu",        "Categorie": "Actif",   "Nb": 8},
    {"Code": "4", "Libelle": "Cloture",         "Categorie": "Inactif", "Nb": 45},
    {"Code": "5", "Libelle": "En resiliation",  "Categorie": "Inactif", "Nb": 23},
    {"Code": "6", "Libelle": "Resilie",         "Categorie": "Inactif", "Nb": 25},
]

chemin_sortie = SORTIE / "resume_statuts.csv"

with open(chemin_sortie, "w", encoding="utf-8", newline="") as f:
    # DictWriter : écrire des dictionnaires ligne par ligne
    # fieldnames définit l'ordre des colonnes
    ecrivain = csv.DictWriter(f, fieldnames=["Code","Libelle","Categorie","Nb"], delimiter=";")
    ecrivain.writeheader()         # écrire la ligne d'en-tête
    ecrivain.writerows(resume_statuts)   # écrire toutes les lignes

print(f"Fichier écrit : {chemin_sortie}")
print(f"Taille : {chemin_sortie.stat().st_size} octets")

# Vérifier en relisant
print()
print("Contenu :")
print(chemin_sortie.read_text(encoding="utf-8"))"""),

code("""# ── JSON : lire et écrire ────────────────────────────────────
import json
from pathlib import Path

SORTIE = Path("../Sorties_Beobank")

# Écrire un fichier JSON (métadonnées de la formation)
metadata = {
    "formation":  "Python pour Beobank",
    "jour":       2,
    "date":       "2026-11-19",
    "tables": {
        "CTR":       {"lignes": 200,  "cle": "IDT_AC"},
        "TIE":       {"lignes": 100,  "cle": "IDT_PI"},
        "TIE_ADR":   {"lignes": 100,  "cle": "IDT_PI"},
        "TIE_X_CTR": {"lignes": 200,  "cle": ["IDT_PI","IDT_AC"]},
        "TXN_X_CTR": {"lignes": 1260, "cle": ["IDT_AC","NUM_ORD_MVT_CPB"]},
    },
    "statuts_actifs": ["1","2","3"],
}

chemin_json = SORTIE / "metadata_beobank.json"

# json.dump() : écrire un objet Python en JSON
# indent=2 : indentation pour la lisibilité
# ensure_ascii=False : garder les accents
with open(chemin_json, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print(f"JSON écrit : {chemin_json}")
print()

# Relire le JSON
with open(chemin_json, "r", encoding="utf-8") as f:
    data_lue = json.load(f)      # json.load() : lire un fichier JSON

print(f"Formation : {data_lue['formation']}")
print(f"Jour : {data_lue['jour']}")
print(f"Tables :")
for table, info in data_lue["tables"].items():
    print(f"  {table:<12} : {info['lignes']:>5} lignes")"""),

# ── EXERCICE 2 ──────────────────────────────────────────────
md("""---
### 🟡 Exercice 2 · Lire TXN_X_CTR.csv et écrire un résumé JSON

**À faire :**
1. Lire `TXN_X_CTR.csv` avec `csv.DictReader`
2. Compter les transactions par `COD_LNG_RIU` (langue)
3. Lister les 3 premières colonnes et leurs valeurs uniques
4. Écrire un résumé JSON dans `../Sorties_Beobank/resume_txn.json`"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────
import csv, json
from pathlib import Path

DATA   = Path("../Orsys")
SORTIE = Path("../Sorties_Beobank")
SORTIE.mkdir(exist_ok=True)

comptage_lng = {}
nb_lignes    = 0

with open(DATA / "TXN_X_CTR.csv", "r", encoding="utf-8") as f:
    for ligne in csv.DictReader(f, delimiter=";"):
        nb_lignes += 1
        lng = ligne.get("COD_LNG_RIU", "?") or "N/A"
        comptage_lng[lng] = comptage_lng.get(lng, 0) + 1

resume = {
    "fichier"        : "TXN_X_CTR.csv",
    "nb_transactions": nb_lignes,
    "par_langue"     : comptage_lng,
}

with open(SORTIE / "resume_txn.json", "w", encoding="utf-8") as f:
    json.dump(resume, f, indent=2, ensure_ascii=False)

print(f"Transactions : {nb_lignes}")
print(f"Par langue   : {comptage_lng}")
print(f"JSON écrit   : {SORTIE / 'resume_txn.json'}")"""),

# ════════════════════════════════════════════════════════
# SECTION 3 · CHARGER LES 5 TABLES PANDAS
# ════════════════════════════════════════════════════════
md("""---
# 3 · Charger les 5 tables Beobank avec Pandas

## Pourquoi Pandas ?

Pandas est la bibliothèque de référence pour la manipulation de données tabulaires en Python.
Un **DataFrame** Pandas est l'équivalent d'un dataset SAS : des lignes et des colonnes.

## Installation et import

```python
pip install pandas    # une seule fois sur votre machine
import pandas as pd   # convention universelle : alias "pd"
```

## Paramètres Beobank

Tous nos fichiers CSV ont les mêmes paramètres :
- Séparateur : `;` (pas la virgule par défaut)
- Valeur manquante SAS : `.` (point) → `na_values="."`
- Encodage : `utf-8`"""),

code("""# ── Charger les 5 tables en une fois ─────────────────────────
import pandas as pd              # la convention universelle est "pd"
from pathlib import Path

# Chemin vers les données
DATA = Path("../Orsys")

# Paramètres communs à tous les fichiers Beobank
# On les regroupe dans un dictionnaire pour éviter de les répéter
PARAMS = dict(
    sep       = ";",          # séparateur : point-virgule (pas la virgule par défaut)
    na_values = ".",          # "." signifie "valeur manquante" en SAS → None/NaN en Pandas
    encoding  = "utf-8",      # encodage des caractères
)

# Charger chaque table
# pd.read_csv() lit un CSV et retourne un DataFrame
# **PARAMS décompresse le dictionnaire comme des paramètres nommés
ctr     = pd.read_csv(DATA / "CTR.csv",       **PARAMS)   # 200 contrats
tie     = pd.read_csv(DATA / "TIE.csv",       **PARAMS)   # 100 clients
tie_adr = pd.read_csv(DATA / "TIE_ADR.csv",   **PARAMS)   # 100 adresses
txc     = pd.read_csv(DATA / "TIE_X_CTR.csv", **PARAMS)   # 200 liens client-contrat
txn     = pd.read_csv(DATA / "TXN_X_CTR.csv", **PARAMS)   # 1260 transactions

# Vérifier le chargement
print(f"{'Table':<12}  {'Lignes':>7}  {'Colonnes':>9}")
print("-" * 33)
for nom, df in [("CTR",ctr), ("TIE",tie), ("TIE_ADR",tie_adr),
                ("TIE_X_CTR",txc), ("TXN_X_CTR",txn)]:
    print(f"{nom:<12}  {df.shape[0]:>7}  {df.shape[1]:>9}")
    # shape : tuple (nb_lignes, nb_colonnes)
print()
print("✓ Toutes les tables chargées avec succès")"""),

# ════════════════════════════════════════════════════════
# SECTION 4 · EXPLORER UN DATAFRAME
# ════════════════════════════════════════════════════════
md("""---
# 4 · Explorer un DataFrame

Pandas fournit de nombreuses fonctions pour explorer rapidement vos données.
Elles remplacent `PROC PRINT`, `PROC MEANS`, `PROC FREQ`, `PROC CONTENTS` en SAS."""),

code("""# ── head() / tail() : voir les premières/dernières lignes ─────
# head(n) = les n premières lignes (défaut : 5)
# tail(n) = les n dernières lignes

print("=== 5 premières lignes de CTR (head) ===")
print(ctr.head())    # affiche automatiquement dans Jupyter
print()
print("=== 3 dernières lignes de CTR (tail) ===")
print(ctr.tail(3))"""),

code("""# ── shape et columns : dimensions et noms des colonnes ───────

print("=== Dimensions du DataFrame ===")
print(f"ctr.shape    = {ctr.shape}")          # tuple (lignes, colonnes)
print(f"Lignes       = {ctr.shape[0]}")
print(f"Colonnes     = {ctr.shape[1]}")
print()

print("=== Liste des colonnes ===")
for i, col in enumerate(ctr.columns):         # .columns = liste des noms de colonnes
    print(f"  {i:>2}. {col}")"""),

code("""# ── info() : types et valeurs manquantes (équivalent PROC CONTENTS) ─
print("=== info() de CTR ===")
ctr.info()
# Affiche : type de chaque colonne, nombre de valeurs non-nulles
# object = texte (str), float64 = nombre décimal, int64 = entier"""),

code("""# ── describe() : statistiques descriptives (équivalent PROC MEANS) ─
print("=== describe() de CTR ===")
# describe() sur les colonnes numériques : count, mean, std, min, quartiles, max
ctr.describe()"""),

code("""# ── isnull() et isna() : compter les valeurs manquantes ──────
print("=== Valeurs manquantes dans CTR ===")
# isnull() retourne True/False pour chaque cellule
# .sum() sur un booléen compte les True (True = 1, False = 0)
manquants = ctr.isnull().sum()     # nombre de NaN par colonne
print(manquants)
print()
print(f"Lignes avec AU MOINS UNE valeur manquante : {ctr.isnull().any(axis=1).sum()}")
print()

# Pourcentage de manquants
pct_manquants = (ctr.isnull().sum() / len(ctr) * 100).round(1)
print("=== Taux de complétion par colonne ===")
for col in ctr.columns:
    pct = pct_manquants[col]
    barre = "█" * int((100-pct)/10) + "░" * int(pct/10)
    print(f"  {col:<20}  {100-pct:>5.1f}%  {barre}")"""),

code("""# ── value_counts() : fréquences (équivalent PROC FREQ) ───────
print("=== Répartition par statut (COD_ECV_CTR) ===")
# value_counts() compte les occurrences de chaque valeur unique
# normalize=True : affiche les proportions au lieu des effectifs
vc = ctr["COD_ECV_CTR"].value_counts()
print(vc)
print()

# Avec les proportions
vc_pct = ctr["COD_ECV_CTR"].value_counts(normalize=True) * 100
print("=== Proportions (%) ===")
print(vc_pct.round(1))
print()

# Table de fréquence croisée : pd.crosstab()
# Équivalent de PROC FREQ avec TABLE var1*var2
print("=== Croisement COD_TYP_TIE × COD_LNG_CTR ===")
print(pd.crosstab(tie["COD_TYP_TIE"], tie["COD_LNG_CTR"]))"""),

# ── EXERCICE 3 ──────────────────────────────────────────────
md("""---
### 🟡 Exercice 3 · Explorer TXN_X_CTR avec Pandas

**À faire :**
1. Afficher `shape`, `columns`, `info()` de `txn`
2. Compter les valeurs manquantes par colonne
3. Analyser la répartition par `COD_LNG_RIU`
4. Donner le nombre de transactions uniques par `IDT_AC` (compter les `IDT_AC` distincts)
5. Afficher les 5 transactions avec le `NUM_ORD_MVT_CPB` le plus élevé"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────

# 1. Shape et colonnes
print(txn.shape)
print(txn.columns.tolist())

# 2. Valeurs manquantes
print(txn.isnull().sum())

# 3. Répartition par langue
print(txn["COD_LNG_RIU"].value_counts())

# 4. Comptes distincts par IDT_AC
# nunique() = nombre de valeurs uniques
print(f"Comptes distincts : {txn['IDT_AC'].nunique()}")

# 5. Top 5 par NUM_ORD_MVT_CPB
print(txn.nlargest(5, "NUM_ORD_MVT_CPB"))"""),

md("""**✅ Correction exercice 3 :**"""),

code("""# ✅ CORRECTION exercice 3 ──────────────────────────────────

print("=== 1. Dimensions ===")
print(f"Shape : {txn.shape}  →  {txn.shape[0]} transactions, {txn.shape[1]} colonnes")
print(f"Colonnes : {txn.columns.tolist()}")
print()

print("=== 2. Valeurs manquantes ===")
manq = txn.isnull().sum()
for col, nb in manq.items():
    if nb > 0:
        print(f"  {col:<25} : {nb:>5} manquants ({nb/len(txn):.1%})")
    else:
        print(f"  {col:<25} : aucun manquant")
print()

print("=== 3. Répartition par langue ===")
vc_lng = txn["COD_LNG_RIU"].value_counts()
for lng, nb in vc_lng.items():
    print(f"  {lng} : {nb:>5} ({nb/len(txn):.1%})")
print()

print("=== 4. Comptes distincts ===")
print(f"  IDT_AC distincts : {txn['IDT_AC'].nunique()} comptes ont des transactions")
print()

print("=== 5. Top 5 NUM_ORD_MVT_CPB ===")
# nlargest(n, colonne) : les n plus grandes valeurs
top5 = txn.nlargest(5, "NUM_ORD_MVT_CPB")[["IDT_AC","NUM_ORD_MVT_CPB","DAT_CRE_MVT_CPB","COD_LNG_RIU"]]
print(top5.to_string(index=False))"""),

# ════════════════════════════════════════════════════════
# SECTION 5 · SÉLECTION DE COLONNES ET LIGNES
# ════════════════════════════════════════════════════════
md("""---
# 5 · Sélectionner des colonnes et des lignes

## 5.1 Sélectionner des colonnes

```python
df["colonne"]         # une seule colonne → Series
df[["col1","col2"]]   # plusieurs colonnes → DataFrame
```

## 5.2 Sélectionner des lignes avec .loc et .iloc

| Méthode | Utilisation | Exemple |
|---------|------------|---------|
| `.loc[label]` | Par étiquette (index ou condition) | `df.loc[df["A"]>0]` |
| `.iloc[n]` | Par position numérique | `df.iloc[0]` = 1ère ligne |
| `.loc[i, "col"]` | Une cellule par étiquette | `df.loc[5, "SLD_CTR"]` |
| `.iloc[i, j]` | Une cellule par position | `df.iloc[0, 3]` |"""),

code("""# ── Sélectionner des colonnes ────────────────────────────────

# Une seule colonne : retourne une Series (liste ordonnée avec index)
statuts = ctr["COD_ECV_CTR"]      # accès par nom de colonne entre crochets
print(f"Type : {type(statuts).__name__}")    # Series
print(f"Premières valeurs :")
print(statuts.head(5))
print()

# Plusieurs colonnes : retourne un DataFrame
# IMPORTANT : double crochets [["col1", "col2"]] ← liste dans les crochets
ctr_selection = ctr[["IDT_AC", "COD_ECV_CTR", "SLD_CTR", "COD_DEV"]]
print(f"Type : {type(ctr_selection).__name__}")   # DataFrame
print(ctr_selection.head(5))"""),

code("""# ── Accès aux cellules avec .iloc ────────────────────────────
# iloc = Integer Location = accès par position numérique (commence à 0)

print("=== Accès par position avec .iloc ===")
print(f"1ère ligne  : {ctr.iloc[0]}")       # toute la première ligne (Series)
print()
print(f"Cellule [0,0] (1ère ligne, 1ère colonne) : {ctr.iloc[0, 0]}")
print(f"Cellule [0,3] (1ère ligne, 4ème colonne) : {ctr.iloc[0, 3]}")
print()

# Sélectionner plusieurs lignes par position
print("=== Lignes 0 à 4 (5 premières) ===")
print(ctr.iloc[:5])     # équivalent de head(5)
print()

print("=== Lignes 5 à 9 ===")
print(ctr.iloc[5:10])

print("=== Dernières 3 lignes ===")
print(ctr.iloc[-3:])"""),

code("""# ── Accès par label avec .loc ────────────────────────────────
# loc = Label Location = accès par étiquette d'index ou condition booléenne

# L'index par défaut est un entier (0, 1, 2, ..., N-1)
print("=== Accès par index avec .loc ===")
print(f"Ligne d'index 0 : \\n{ctr.loc[0]}")
print()

# Sélectionner une colonne spécifique d'une ligne
print(f"Solde de la ligne 0 : {ctr.loc[0, 'SLD_CTR']}")
print()

# Sélectionner plusieurs lignes ET plusieurs colonnes
print("=== Lignes 0-4, colonnes IDT_AC et SLD_CTR ===")
# loc[liste_lignes, liste_colonnes]
print(ctr.loc[0:4, ["IDT_AC", "COD_ECV_CTR", "SLD_CTR"]])
# NOTE : contrairement à iloc, loc inclut la borne supérieure (0:4 = 0,1,2,3,4)"""),

# ── EXERCICE 4 ──────────────────────────────────────────────
md("""---
### 🟡 Exercice 4 · Sélection dans TIE et CTR

**À faire :**
1. Sélectionner uniquement les colonnes `IDT_PI`, `COD_TYP_TIE`, `COD_LNG_CTR`, `COD_SEX` de `tie`
2. Afficher la 10ème ligne de `ctr` avec `.iloc`
3. Afficher la valeur de `SLD_CTR` à la position (5, colonne SLD_CTR) avec `.loc`
4. Sélectionner les colonnes identifiant (`IDT_AC`, `REF_CTR_INN`) et soldes (`SLD_CTR`, `SLD_DSP`) de `ctr`"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────

# 1. Sélection de colonnes dans TIE
tie_selection = tie[...]
print(tie_selection.head())

# 2. 10ème ligne de CTR (iloc)
dixieme = ctr.iloc[...]
print(dixieme)

# 3. Valeur de SLD_CTR à l'index 5
solde_5 = ctr.loc[5, ...]
print(f"Solde ligne 5 : {solde_5}")

# 4. Colonnes id + soldes
ctr_soldes = ctr[["IDT_AC", "REF_CTR_INN", ...]]
print(ctr_soldes.head())"""),

md("""**✅ Correction exercice 4 :**"""),

code("""# ✅ CORRECTION exercice 4 ──────────────────────────────────

# 1. Sélection de colonnes dans TIE
tie_selection = tie[["IDT_PI", "COD_TYP_TIE", "COD_LNG_CTR", "COD_SEX"]]
print("=== 1. Sélection TIE ===")
print(tie_selection.head())
print()

# 2. 10ème ligne de CTR (l'index 9 car on commence à 0)
print("=== 2. 10ème ligne CTR (iloc[9]) ===")
dixieme = ctr.iloc[9]     # position 9 = 10ème ligne
print(dixieme)
print()

# 3. Valeur de SLD_CTR à l'index 5
solde_5 = ctr.loc[5, "SLD_CTR"]    # ligne d'index 5, colonne "SLD_CTR"
print(f"=== 3. SLD_CTR ligne index 5 : {solde_5} ===")
print()

# 4. Colonnes identifiant + soldes
ctr_soldes = ctr[["IDT_AC", "REF_CTR_INN", "SLD_CTR", "SLD_DSP"]]
print("=== 4. CTR identifiants + soldes ===")
print(ctr_soldes.head(8))"""),

# ════════════════════════════════════════════════════════
# SECTION 6 · FILTRER ET TRIER
# ════════════════════════════════════════════════════════
md("""---
# 6 · Filtrer et trier les données

## 6.1 Filtrage par condition

```python
# Crée un masque booléen (True/False pour chaque ligne)
masque = df["colonne"] == "valeur"    # Series de True/False
df_filtre = df[masque]                # garde les lignes True

# En une ligne
df_filtre = df[df["colonne"] == "valeur"]
```

## 6.2 Opérateurs de comparaison dans Pandas

| Pandas | SAS WHERE |
|--------|-----------|
| `df["col"] == "v"` | `WHERE col = "v"` |
| `df["col"] != "v"` | `WHERE col ne "v"` |
| `df["col"] > 0` | `WHERE col > 0` |
| `df["col"].isin(["a","b"])` | `WHERE col in ("a","b")` |
| `df["col"].isna()` | `WHERE col = .` |
| `df["col"].notna()` | `WHERE col ne .` |
| `(cond1) & (cond2)` | `WHERE cond1 AND cond2` |
| `(cond1) \| (cond2)` | `WHERE cond1 OR cond2` |
| `~masque` | `WHERE NOT cond` |

> **⚠ Important :** En Pandas, utilisez `&` (pas `and`), `|` (pas `or`), `~` (pas `not`).
> Mettez chaque condition entre parenthèses : `(cond1) & (cond2)`.
"""),

code("""# ── Filtre simple : contrats actifs ─────────────────────────
print("=== Contrats actifs (COD_ECV_CTR dans 1,2,3) ===")

# Méthode 1 : isin() — recommandée pour les listes de valeurs
# isin() retourne True pour chaque ligne où la valeur est dans la liste
actifs = ctr[ctr["COD_ECV_CTR"].isin(["1","2","3"])]
print(f"Nombre de contrats actifs : {len(actifs)} / {len(ctr)}")
print(actifs[["IDT_AC","COD_ECV_CTR","SLD_CTR"]].head())
print()

# Méthode 2 : condition == avec une seule valeur
ouverts = ctr[ctr["COD_ECV_CTR"] == "1"]
print(f"Contrats ouverts (code 1) : {len(ouverts)}")
print()

# Méthode 3 : exclure des valeurs avec ~isin() (NOT IN)
non_resilies = ctr[~ctr["COD_ECV_CTR"].isin(["5","6"])]    # ~ = NOT
print(f"Contrats hors résiliation : {len(non_resilies)}")"""),

code("""# ── Filtres multiples avec & (AND) et | (OR) ─────────────────
# RÈGLE : chaque condition DOIT être entre parenthèses
# Sinon Python ne sait pas dans quel ordre évaluer

# AND : contrats actifs ET en euros ET solde > 10 000
masque_and = (
    (ctr["COD_ECV_CTR"].isin(["1","2","3"])) &   # actif
    (ctr["COD_DEV"] == "EUR")                   &   # en euros
    (ctr["SLD_CTR"] > 10000)                        # solde > 10k
)
ctr_premium = ctr[masque_and]
print(f"Contrats actifs EUR > 10k : {len(ctr_premium)}")
print(ctr_premium[["IDT_AC","COD_ECV_CTR","SLD_CTR","COD_DEV"]].head())
print()

# OR : solde manquant OU solde négatif (anomalies)
masque_or = (
    (ctr["SLD_CTR"].isna())     |   # solde absent
    (ctr["SLD_CTR"] < 0)            # solde négatif
)
anomalies = ctr[masque_or]
print(f"Anomalies de solde : {len(anomalies)}")
print(anomalies[["IDT_AC","COD_ECV_CTR","SLD_CTR"]].head())"""),

code("""# ── Valeurs manquantes : isna() / notna() ────────────────────

print("=== Lignes avec SLD_CTR manquant ===")
# isna() retourne True pour les NaN (valeurs manquantes)
ctr_sans_solde = ctr[ctr["SLD_CTR"].isna()]
print(f"Sans solde : {len(ctr_sans_solde)}")
print(ctr_sans_solde[["IDT_AC","COD_ECV_CTR","SLD_CTR"]].head())
print()

print("=== Lignes avec SLD_CTR renseigné ===")
# notna() = inverse de isna()
ctr_avec_solde = ctr[ctr["SLD_CTR"].notna()]
print(f"Avec solde : {len(ctr_avec_solde)}")
print()

print("=== Lignes avec DAT_DCS (décès) renseignée dans TIE ===")
# Clients décédés (date de décès renseignée)
clients_decedes = tie[tie["DAT_DCS"].notna()]
print(f"Clients avec DAT_DCS : {len(clients_decedes)}")
print(clients_decedes[["IDT_PI","COD_TYP_TIE","COD_SEX","DAT_DCS"]].head())"""),

code("""# ── sort_values() : trier (équivalent PROC SORT) ─────────────

# Trier par solde décroissant (les plus riches en premier)
ctr_trie = ctr.sort_values("SLD_CTR", ascending=False)
# ascending=False : ordre décroissant (True = croissant, défaut)
print("=== Top 5 soldes les plus élevés ===")
print(ctr_trie[["IDT_AC","COD_ECV_CTR","SLD_CTR","COD_DEV"]].head())
print()

# Tri multi-critères : par statut PUIS par solde décroissant
# Passer une liste de colonnes et un ascendant par colonne
ctr_trie2 = ctr.sort_values(
    by        = ["COD_ECV_CTR", "SLD_CTR"],
    ascending = [True, False]     # statut croissant, solde décroissant
)
print("=== Trié par statut ASC, solde DESC ===")
print(ctr_trie2[["IDT_AC","COD_ECV_CTR","SLD_CTR"]].head(10))
print()

# nlargest / nsmallest : top N directement
print("=== Méthode rapide : nlargest(5) ===")
print(ctr.nlargest(5, "SLD_CTR")[["IDT_AC","SLD_CTR"]])"""),

# ── EXERCICE 5 ──────────────────────────────────────────────
md("""---
### 🟡 Exercice 5 · Filtrer et trier CTR

**À faire :**
1. Extraire les contrats résilié ou en résiliation (`COD_ECV_CTR` = "5" ou "6")
2. Parmi les contrats actifs, garder ceux avec `SLD_CTR > 5000` ET `COD_DEV = "EUR"`
3. Trier ces contrats Premium par `SLD_CTR` décroissant et afficher le top 10
4. Trouver le nombre de contrats avec `SLD_CTR` manquant par statut"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────

# 1. Résiliés ou en résiliation
resilies = ctr[...]
print(f"Résiliation : {len(resilies)}")

# 2. Actifs + solde > 5000 + EUR
actifs_premium = ctr[(ctr["COD_ECV_CTR"].isin(["1","2","3"])) & ...]
print(f"Actifs Premium EUR : {len(actifs_premium)}")

# 3. Top 10 par solde
top10 = actifs_premium.sort_values(..., ascending=False).head(10)
print(top10[["IDT_AC","COD_ECV_CTR","SLD_CTR","COD_DEV"]])

# 4. Manquants par statut
# Astuce : combiner isna() et groupby (section suivante — ou loop)
print(ctr[ctr["SLD_CTR"].isna()]["COD_ECV_CTR"].value_counts())"""),

md("""**✅ Correction exercice 5 :**"""),

code("""# ✅ CORRECTION exercice 5 ──────────────────────────────────

# 1. Résiliés ou en résiliation
resilies = ctr[ctr["COD_ECV_CTR"].isin(["5","6"])]
print(f"=== 1. Résiliés/en résiliation : {len(resilies)} contrats ===")
print(resilies["COD_ECV_CTR"].value_counts().to_string())
print()

# 2. Actifs EUR > 5000
actifs_premium = ctr[
    (ctr["COD_ECV_CTR"].isin(["1","2","3"])) &   # actif
    (ctr["SLD_CTR"] > 5000)                     &   # solde > 5k
    (ctr["COD_DEV"] == "EUR")                       # devise EUR
]
print(f"=== 2. Actifs EUR > 5 000 : {len(actifs_premium)} contrats ===")
print()

# 3. Top 10 par solde décroissant
top10 = actifs_premium.sort_values("SLD_CTR", ascending=False).head(10)
print("=== 3. Top 10 soldes ===")
print(top10[["IDT_AC","COD_ECV_CTR","SLD_CTR","COD_DEV"]].to_string(index=False))
print()

# 4. Manquants par statut
print("=== 4. SLD_CTR manquants par statut ===")
sans_solde = ctr[ctr["SLD_CTR"].isna()]
print(sans_solde["COD_ECV_CTR"].value_counts().to_string())"""),

# ════════════════════════════════════════════════════════
# SECTION 7 · COLONNES CALCULÉES ET TRANSFORMATIONS
# ════════════════════════════════════════════════════════
md("""---
# 7 · Colonnes calculées et transformations

## 7.1 Créer une nouvelle colonne

```python
df["nouvelle_colonne"] = expression
```

## 7.2 Les outils de transformation

| Outil | Utilisation | Exemple |
|-------|-------------|---------|
| Arithmétique directe | Calcul simple | `df["A"] * 2` |
| `.map(dict)` | Remplacer valeur par valeur | Codes → libellés |
| `.fillna(v)` | Remplacer les NaN | Valeur par défaut |
| `np.where(c, a, b)` | Si/Sinon vectorisé | 2 cas |
| `np.select(c, v)` | If/elif chaîné | N cas |
| `.apply(fn)` | Appliquer une fonction | Logique complexe |
| `pd.cut()` | Découper en tranches | Binning |
| `pd.to_datetime()` | Convertir en date | Parsing de dates |"""),

code("""# ── Calcul arithmétique direct ───────────────────────────────
import numpy as np    # numpy : bibliothèque de calcul numérique

print("=== Colonnes calculées dans CTR ===")

# Plus-value : différence entre solde actuel et montant initial
# NaN - NaN = NaN (Pandas gère automatiquement les valeurs manquantes)
ctr["PLUS_VALUE"] = ctr["SLD_CTR"] - ctr["MNT_INI"]

# Ratio : solde disponible / solde total
# Remplacer les divisions par zéro par NaN
ctr["RATIO_DSP"] = ctr["SLD_DSP"] / ctr["SLD_CTR"].replace(0, np.nan)

# Indicateur binaire : solde > 0
# Pandas évalue la condition ligne par ligne → retourne True/False
ctr["FLG_SOLDE_POS"] = ctr["SLD_CTR"] > 0

print(ctr[["IDT_AC","SLD_CTR","MNT_INI","PLUS_VALUE","RATIO_DSP","FLG_SOLDE_POS"]].head(6))"""),

code("""# ── .map(dictionnaire) : coder des libellés ─────────────────
# .map() applique une transformation à chaque valeur d'une colonne
# Équivalent du FORMAT SAS

MAPPING_ECV = {
    "1":"Ouvert","2":"En attente","3":"Suspendu",
    "4":"Cloturé","5":"En résiliation","6":"Résilié"
}
MAPPING_CAT = {
    "1":"Actif","2":"Actif","3":"Actif",
    "4":"Inactif","5":"Inactif","6":"Inactif"
}

# .map(dict) : remplace chaque valeur par la valeur du dictionnaire
# Les valeurs absentes du dictionnaire → NaN
ctr["LIB_ECV"]  = ctr["COD_ECV_CTR"].map(MAPPING_ECV)
ctr["CAT_ECV"]  = ctr["COD_ECV_CTR"].map(MAPPING_CAT)

print("=== Colonnes libellées ===")
print(ctr[["IDT_AC","COD_ECV_CTR","LIB_ECV","CAT_ECV"]].head(8))
print()
print("Vérification : aucun NaN dans LIB_ECV ?", ctr["LIB_ECV"].isna().sum())"""),

code("""# ── np.where() : condition binaire (if/else vectorisé) ──────
# np.where(condition, valeur_si_vrai, valeur_si_faux)
# BEAUCOUP plus rapide que .apply() sur un gros DataFrame

# Cas 1 : flag client actif
ctr["FLG_ACTIF"] = np.where(
    ctr["COD_ECV_CTR"].isin(["1","2","3"]),   # condition
    1,                                           # valeur si Vrai
    0                                            # valeur si Faux
)

# Cas 2 : alerte sur les soldes faibles
ctr["ALERTE_SOLDE"] = np.where(
    ctr["SLD_CTR"] < 500,         # solde < 500 EUR
    "ALERTE",                     # si vrai
    "OK"                          # si faux
)

# Cas 3 : gérer les NaN dans la condition
# np.where sur une colonne avec NaN : les NaN vérifient "< 500" → False → "OK"
# Pour les traiter différemment, il faut enchaîner

print(ctr[["IDT_AC","COD_ECV_CTR","SLD_CTR","FLG_ACTIF","ALERTE_SOLDE"]].head(8))
print()
print("Répartition FLG_ACTIF :", ctr["FLG_ACTIF"].value_counts().to_dict())
print("Répartition ALERTE    :", ctr["ALERTE_SOLDE"].value_counts().to_dict())"""),

code("""# ── np.select() : conditions multiples (if/elif/else vectorisé) ─
# np.select(liste_conditions, liste_valeurs, default=valeur_par_défaut)

# Segmentation clients selon le solde (SLD_CTR)
conditions = [
    ctr["SLD_CTR"].isna(),            # solde manquant
    ctr["SLD_CTR"] < 1000,            # < 1 000 EUR
    ctr["SLD_CTR"] < 10000,           # 1 000 - 9 999 EUR
    ctr["SLD_CTR"] < 50000,           # 10 000 - 49 999 EUR
]
valeurs = [
    "Inconnu",    # si NaN
    "Standard",   # si < 1k
    "Confort",    # si 1k-10k
    "Premium",    # si 10k-50k
]

# np.select teste les conditions dans l'ordre
# La première qui est True détermine la valeur
# default = valeur si AUCUNE condition n'est vraie (ici >= 50k)
ctr["SEGMENT"] = np.select(conditions, valeurs, default="Private")

print("=== Segmentation par solde ===")
print(ctr["SEGMENT"].value_counts().sort_index().to_string())
print()
print(ctr[["IDT_AC","SLD_CTR","SEGMENT"]].head(8))"""),

code("""# ── pd.cut() : tranches (binning) ───────────────────────────
# pd.cut() découpe une colonne numérique en intervalles
# Équivalent de FORMAT ... LOW-1000='Standard' 1000-<10000='Confort'...

# Retirer les NaN pour pd.cut (il ne les accepte pas)
# Puis utiliser pd.cut sur les soldes valides

# bins = limites des tranches (bornes INCLUSES à droite par défaut)
# labels = noms des tranches
bins   = [0, 1000, 10000, 50000, float("inf")]
labels = ["Standard", "Confort", "Premium", "Private"]

ctr["TRANCHE_SOLDE"] = pd.cut(
    ctr["SLD_CTR"],     # colonne à découper
    bins   = bins,      # bornes des tranches
    labels = labels,    # noms des tranches
    right  = True,      # intervalles fermés à droite : (0, 1000]
)

print("=== Tranches de solde (pd.cut) ===")
print(ctr["TRANCHE_SOLDE"].value_counts().sort_index().to_string())
print()
print(ctr[["IDT_AC","SLD_CTR","TRANCHE_SOLDE"]].dropna(subset=["SLD_CTR"]).head(8))"""),

code("""# ── pd.to_datetime() : convertir les colonnes de date ────────
# Les CSV stockent les dates comme du texte → il faut les convertir

print("=== Type AVANT conversion ===")
print(f"DAT_OUV_CTR : {ctr['DAT_OUV_CTR'].dtype}")   # dtype = type de données

# Cas 1 : format standard YYYY-MM-DD (tables CTR, TIE, TXN)
# pd.to_datetime() reconnaît automatiquement YYYY-MM-DD
ctr["DAT_OUV_CTR_DT"] = pd.to_datetime(ctr["DAT_OUV_CTR"], errors="coerce")
# errors="coerce" : les valeurs non convertibles → NaT (Not a Time = date manquante)

print(f"DAT_OUV_CTR_DT après conversion : {ctr['DAT_OUV_CTR_DT'].dtype}")

# Cas 2 : format SAS DDMONYYYY (ex: "24NOV2025") dans TIE_ADR
# Pandas ne reconnaît PAS ce format automatiquement → format explicite obligatoire
tie_adr["DAT_MAJ_ADR_DT"] = pd.to_datetime(
    tie_adr["DAT_MAJ_ADR"],
    format="mixed",    # essayer plusieurs formats
    errors="coerce"
)

print(f"DAT_MAJ_ADR_DT : {tie_adr['DAT_MAJ_ADR_DT'].dtype}")
print()

# Extraire des composantes de date
ctr["ANNEE_OUV"]  = ctr["DAT_OUV_CTR_DT"].dt.year     # .dt.year = année
ctr["MOIS_OUV"]   = ctr["DAT_OUV_CTR_DT"].dt.month    # .dt.month = mois
ctr["JOUR_OUV"]   = ctr["DAT_OUV_CTR_DT"].dt.day      # .dt.day = jour
ctr["MOIS_LABEL"] = ctr["DAT_OUV_CTR_DT"].dt.strftime("%b %Y")  # "Nov 2024"

print(ctr[["IDT_AC","DAT_OUV_CTR","DAT_OUV_CTR_DT","ANNEE_OUV","MOIS_OUV","MOIS_LABEL"]].head(5))"""),

code("""# ── .apply() : appliquer une fonction ligne par ligne ─────────
# apply() est plus lent que np.where/np.select mais utile pour la logique complexe

def enrichir_contrat(ligne):
    '''Enrichit une ligne de CTR. Prend une Series, retourne une string.'''
    cod = str(ligne["COD_ECV_CTR"])
    sld = ligne["SLD_CTR"]

    if cod in ("5","6"):               return "CRITIQUE"
    elif cod == "3":                   return "ATTENTION"
    elif pd.isna(sld) or sld < 0:     return "ANOMALIE"
    elif sld > 50000:                  return "TOP CLIENT"
    else:                              return "NORMAL"

# axis=1 : appliquer la fonction sur chaque ligne (axis=0 = chaque colonne)
ctr["ALERTE_V2"] = ctr.apply(enrichir_contrat, axis=1)

print("=== Alertes (apply) ===")
print(ctr["ALERTE_V2"].value_counts().to_string())
print()
print(ctr[["IDT_AC","COD_ECV_CTR","SLD_CTR","ALERTE_V2"]].head(8))"""),

# ── EXERCICE 6 ──────────────────────────────────────────────
md("""---
### 🟡 Exercice 6 · Colonnes calculées dans TIE

**À faire sur le DataFrame `tie` :**
1. Créer `LIB_TYP` : libellé de `COD_TYP_TIE` (1=Personne physique, 2=Personne morale) avec `.map()`
2. Créer `LIB_LNG` : libellé de `COD_LNG_CTR` (FR=Français, NL=Néerlandais)
3. Créer `FLG_DECEDE` avec `np.where()` : 1 si `DAT_DCS` est renseigné, 0 sinon
4. Créer `AGE_APPROX` : `2026 - annee_naissance` en extrayant l'année de `DAT_NAI` (YYYY-MM-DD)
5. Créer `TRANCHE_AGE` avec `pd.cut()` : `[0,25,35,50,65,120]` → `["<25","25-34","35-49","50-64","65+"]`
6. Afficher les statistiques de la colonne AGE_APPROX"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────
import numpy as np

# 1. Libellé type
MAPPING_TYP = {"1":"Personne physique","2":"Personne morale"}
tie["LIB_TYP"] = tie["COD_TYP_TIE"].map(MAPPING_TYP)

# 2. Libellé langue
...

# 3. Flag décédé
tie["FLG_DECEDE"] = np.where(tie["DAT_DCS"].notna(), 1, 0)

# 4. Âge approximatif
tie["DAT_NAI_DT"]  = pd.to_datetime(tie["DAT_NAI"], errors="coerce")
tie["AGE_APPROX"]  = 2026 - tie["DAT_NAI_DT"].dt.year

# 5. Tranche d'âge
bins_age   = [0, 25, 35, 50, 65, 120]
labels_age = ["<25","25-34","35-49","50-64","65+"]
tie["TRANCHE_AGE"] = pd.cut(tie["AGE_APPROX"], bins=bins_age, labels=labels_age)

# 6. Stats
print(tie["AGE_APPROX"].describe())
print()
print(tie[["IDT_PI","LIB_TYP","LIB_LNG","FLG_DECEDE","AGE_APPROX","TRANCHE_AGE"]].head(8))"""),

md("""**✅ Correction exercice 6 :**"""),

code("""# ✅ CORRECTION exercice 6 ──────────────────────────────────
import numpy as np

# 1. Libellé type de tiers
MAPPING_TYP = {"1":"Personne physique","2":"Personne morale"}
tie["LIB_TYP"] = tie["COD_TYP_TIE"].map(MAPPING_TYP)

# 2. Libellé langue
MAPPING_LNG = {"FR":"Français","NL":"Néerlandais"}
tie["LIB_LNG"] = tie["COD_LNG_CTR"].map(MAPPING_LNG)

# 3. Flag décédé : 1 si DAT_DCS est renseigné (notna()), 0 sinon
tie["FLG_DECEDE"] = np.where(tie["DAT_DCS"].notna(), 1, 0)

# 4. Âge approximatif : convertir d'abord en datetime, extraire l'année
tie["DAT_NAI_DT"] = pd.to_datetime(tie["DAT_NAI"], errors="coerce")
tie["AGE_APPROX"] = 2026 - tie["DAT_NAI_DT"].dt.year

# 5. Tranche d'âge avec pd.cut
bins_age   = [0, 25, 35, 50, 65, 120]
labels_age = ["<25","25-34","35-49","50-64","65+"]
tie["TRANCHE_AGE"] = pd.cut(
    tie["AGE_APPROX"],
    bins   = bins_age,
    labels = labels_age,
    right  = True,         # bornes fermées à droite : (0,25]
)

# 6. Statistiques
print("=== Âge approximatif ===")
print(tie["AGE_APPROX"].describe().round(1))
print()
print("=== Répartition par tranche ===")
print(tie["TRANCHE_AGE"].value_counts().sort_index().to_string())
print()
print("=== Aperçu ===")
print(tie[["IDT_PI","COD_TYP_TIE","LIB_TYP","LIB_LNG","AGE_APPROX","TRANCHE_AGE","FLG_DECEDE"]].head(8))"""),

# ════════════════════════════════════════════════════════
# SECTION 8 · GROUPBY ET AGRÉGATIONS
# ════════════════════════════════════════════════════════
md("""---
# 8 · Groupby et agrégations

## Équivalent SAS et SQL

```sql
-- SQL
SELECT COD_ECV_CTR, COUNT(*), AVG(SLD_CTR), SUM(SLD_CTR)
FROM CTR GROUP BY COD_ECV_CTR

# Pandas
ctr.groupby("COD_ECV_CTR").agg(
    NB_CTR  = ("IDT_AC",  "count"),
    SLD_MOY = ("SLD_CTR", "mean"),
    SLD_SUM = ("SLD_CTR", "sum"),
)
```

## Fonctions d'agrégation disponibles

| Fonction | Résultat |
|----------|----------|
| `"count"` | Nombre de valeurs non-NaN |
| `"size"` | Nombre total de lignes (inclut NaN) |
| `"sum"` | Somme |
| `"mean"` | Moyenne |
| `"median"` | Médiane |
| `"min"` / `"max"` | Min / Max |
| `"std"` | Écart-type |
| `"first"` / `"last"` | Première / Dernière valeur |
| `"nunique"` | Nombre de valeurs uniques |"""),

code("""# ── groupby simple ───────────────────────────────────────────
print("=== Contrats par statut ===")
# groupby("col") : regrouper les lignes par valeur unique de la colonne
# .agg() : appliquer des fonctions d'agrégation
# Syntaxe : NomColonneSortie = ("ColonneSource", "fonction")
par_statut = ctr.groupby("COD_ECV_CTR").agg(
    NB_CTR   = ("IDT_AC",  "count"),    # compter les lignes
    SLD_MOY  = ("SLD_CTR", "mean"),     # solde moyen
    SLD_SUM  = ("SLD_CTR", "sum"),      # solde total
    SLD_MAX  = ("SLD_CTR", "max"),      # solde maximum
).round(2)

# reset_index() : transformer l'index (COD_ECV_CTR) en colonne normale
par_statut = par_statut.reset_index()

# Ajouter le libellé
MAPPING_ECV = {"1":"Ouvert","2":"En attente","3":"Suspendu",
               "4":"Cloturé","5":"En résiliation","6":"Résilié"}
par_statut["LIB_ECV"] = par_statut["COD_ECV_CTR"].map(MAPPING_ECV)

print(par_statut[["COD_ECV_CTR","LIB_ECV","NB_CTR","SLD_MOY","SLD_SUM"]].to_string(index=False))"""),

code("""# ── groupby multi-colonnes ───────────────────────────────────
print("=== Contrats par statut ET par devise ===")
par_statut_dev = ctr.groupby(["COD_ECV_CTR","COD_DEV"]).agg(
    NB   = ("IDT_AC",  "count"),
    SLD  = ("SLD_CTR", "sum"),
).reset_index()
print(par_statut_dev.to_string(index=False))
print()

print("=== Clients par type ET par langue ===")
par_type_lng = tie.groupby(["COD_TYP_TIE","COD_LNG_CTR"]).agg(
    NB_CLIENTS = ("IDT_PI", "count"),
    AGE_MOY    = ("AGE_APPROX", "mean"),
).round(1).reset_index()
print(par_type_lng.to_string(index=False))"""),

code("""# ── Transactions par compte : utilisation réelle ──────────────
print("=== Activité transactionnelle par compte ===")

# Convertir la date de transaction en datetime
txn["DAT_CRE_DT"] = pd.to_datetime(txn["DAT_CRE_MVT_CPB"], errors="coerce")

activite = txn.groupby("IDT_AC").agg(
    NB_TXN     = ("NUM_ORD_MVT_CPB", "count"),   # nombre de transactions
    DATE_PREM  = ("DAT_CRE_DT", "min"),            # première transaction
    DATE_DERN  = ("DAT_CRE_DT", "max"),            # dernière transaction
    NB_MOIS    = ("DAT_CRE_DT", lambda x: x.dt.to_period("M").nunique()),
).reset_index()

# Calculer la fréquence mensuelle
activite["TXN_PAR_MOIS"] = (activite["NB_TXN"] / activite["NB_MOIS"]).round(1)

print(f"Comptes avec transactions : {len(activite)}")
print()
print("Top 10 comptes les plus actifs :")
top_actifs = activite.sort_values("NB_TXN", ascending=False).head(10)
print(top_actifs[["IDT_AC","NB_TXN","NB_MOIS","TXN_PAR_MOIS","DATE_PREM","DATE_DERN"]].to_string(index=False))"""),

# ── EXERCICE 7 ──────────────────────────────────────────────
md("""---
### 🟡 Exercice 7 · Groupby et agrégation

**À faire :**
1. Pour chaque `SEGMENT` de `ctr` : calculer le nombre de contrats, le solde total,
   le solde moyen et le solde max (arrondi à 2 décimales)
2. Pour chaque `TRANCHE_AGE` de `tie` : calculer le nombre de clients PP/PM
   (astuce : groupby sur `["TRANCHE_AGE", "COD_TYP_TIE"]`)
3. Calculer la répartition mensuelle des ouvertures de contrats
   (`MOIS_OUV` de `ctr` — créé en section 7)"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────

# 1. Stats par segment
par_segment = ctr.groupby("SEGMENT").agg(
    NB_CTR  = ("IDT_AC",  "count"),
    SLD_SUM = ("SLD_CTR", "sum"),
    SLD_MOY = ("SLD_CTR", "mean"),
    SLD_MAX = ("SLD_CTR", "max"),
).round(2).reset_index()
print(par_segment.to_string(index=False))

# 2. Clients par tranche d'âge et type
par_tranche_type = tie.groupby(["TRANCHE_AGE","COD_TYP_TIE"]).agg(
    NB = ("IDT_PI","count")
).reset_index()
print(par_tranche_type.to_string(index=False))

# 3. Ouvertures mensuelles
print(ctr.groupby("MOIS_OUV")["IDT_AC"].count().to_string())"""),

md("""**✅ Correction exercice 7 :**"""),

code("""# ✅ CORRECTION exercice 7 ──────────────────────────────────

# 1. Stats par segment
print("=== 1. Statistiques par segment ===")
par_segment = ctr.groupby("SEGMENT").agg(
    NB_CTR  = ("IDT_AC",  "count"),
    SLD_SUM = ("SLD_CTR", "sum"),
    SLD_MOY = ("SLD_CTR", "mean"),
    SLD_MAX = ("SLD_CTR", "max"),
).round(2).reset_index()
par_segment = par_segment.sort_values("SLD_SUM", ascending=False)
print(par_segment.to_string(index=False))
print()

# 2. Clients par tranche d'âge et type
print("=== 2. Clients par tranche d'âge et type ===")
par_tranche_type = tie.groupby(
    ["TRANCHE_AGE","COD_TYP_TIE"], observed=True    # observed=True pour les catégorielles
).agg(
    NB = ("IDT_PI","count")
).reset_index()
par_tranche_type["TYPE_LIB"] = par_tranche_type["COD_TYP_TIE"].map({"1":"PP","2":"PM"})
print(par_tranche_type[["TRANCHE_AGE","TYPE_LIB","NB"]].to_string(index=False))
print()

# 3. Ouvertures mensuelles (mois 1 à 12)
print("=== 3. Ouvertures par mois ===")
ouv_mois = ctr.groupby("MOIS_OUV")["IDT_AC"].count().reset_index()
ouv_mois.columns = ["Mois","Ouvertures"]
noms_mois = {1:"Jan",2:"Fév",3:"Mar",4:"Avr",5:"Mai",6:"Jun",
             7:"Jul",8:"Aoû",9:"Sep",10:"Oct",11:"Nov",12:"Déc"}
for _, row in ouv_mois.iterrows():
    barre = "█" * int(row["Ouvertures"])
    print(f"  {noms_mois.get(row['Mois'],'?'):>3}  {row['Ouvertures']:>4}  {barre}")"""),

# ════════════════════════════════════════════════════════
# SECTION 9 · JOINTURES (MERGE)
# ════════════════════════════════════════════════════════
md("""---
# 9 · Jointures — pd.merge()

`pd.merge()` est l'équivalent de `PROC SQL LEFT JOIN` en SAS.

## Syntaxe

```python
pd.merge(
    left   = df_gauche,       # table de gauche
    right  = df_droite,       # table de droite
    on     = "colonne_cle",   # colonne de jointure (même nom dans les deux)
    how    = "left",          # type : "left", "right", "inner", "outer"
)
```

## Types de jointure

| how | Lignes gardées | Équivalent SQL |
|-----|---------------|----------------|
| `"inner"` | Seulement les correspondances | `INNER JOIN` |
| `"left"` | Toutes les lignes de gauche | `LEFT JOIN` |
| `"right"` | Toutes les lignes de droite | `RIGHT JOIN` |
| `"outer"` | Toutes les lignes des deux tables | `FULL OUTER JOIN` |"""),

code("""# ── Left join : enrichir CTR avec les infos client ────────────
# TIE_X_CTR est la table de lien entre clients (TIE) et contrats (CTR)
# IDT_PI = clé client, IDT_AC = clé contrat

print("=== Étape 1 : CTR + lien TIE_X_CTR ===")
# Jointure CTR (200 lignes) ← TIE_X_CTR (200 lignes) sur IDT_AC
ctr_tie = pd.merge(
    left   = ctr,         # table de gauche : contrats
    right  = txc[["IDT_AC","IDT_PI","FLG_PRE_TTL","COD_ROL_TTL"]],  # colonnes utiles de TIE_X_CTR
    on     = "IDT_AC",    # clé de jointure : identifiant du compte
    how    = "left",      # LEFT JOIN : garder tous les contrats, même sans client lié
)
print(f"  CTR    : {len(ctr)} lignes")
print(f"  Résultat : {len(ctr_tie)} lignes")
print(ctr_tie[["IDT_AC","IDT_PI","COD_ECV_CTR","SLD_CTR","FLG_PRE_TTL"]].head(5))
print()

print("=== Étape 2 : CTR_TIE + infos clients (TIE) ===")
ctr_tie_complet = pd.merge(
    left   = ctr_tie,
    right  = tie[["IDT_PI","COD_TYP_TIE","COD_LNG_CTR","COD_SEX","LIB_TYP","LIB_LNG"]],
    on     = "IDT_PI",    # clé : identifiant du client
    how    = "left",
)
print(f"  Résultat : {len(ctr_tie_complet)} lignes")
print(ctr_tie_complet[["IDT_AC","IDT_PI","LIB_TYP","LIB_LNG","COD_ECV_CTR","SLD_CTR"]].head(5))"""),

code("""# ── Analyser les jointures : vérifier les correspondances ────
print("=== Qualité de la jointure CTR ← TIE ===")

# Combien de contrats ont un client lié ?
avec_client = ctr_tie_complet["IDT_PI"].notna().sum()
sans_client = ctr_tie_complet["IDT_PI"].isna().sum()
print(f"  Avec client  : {avec_client:>5} ({avec_client/len(ctr_tie_complet):.1%})")
print(f"  Sans client  : {sans_client:>5} ({sans_client/len(ctr_tie_complet):.1%})")
print()

# Analyse par langue : répartition des contrats PP vs PM
print("=== Contrats par type de titulaire ===")
par_type = ctr_tie_complet.groupby("LIB_TYP").agg(
    NB_CTR  = ("IDT_AC",  "count"),
    SLD_SUM = ("SLD_CTR", "sum"),
    SLD_MOY = ("SLD_CTR", "mean"),
).round(2).reset_index()
print(par_type.to_string(index=False))
print()

# Répartition par langue
print("=== Contrats par langue du titulaire ===")
par_lng = ctr_tie_complet.groupby("LIB_LNG", dropna=False).agg(
    NB  = ("IDT_AC", "count"),
    SLD = ("SLD_CTR","sum"),
).reset_index()
print(par_lng.to_string(index=False))"""),

code("""# ── Jointure avec les transactions ───────────────────────────
print("=== Contrats avec leur nombre de transactions ===")

# Agréger les transactions par compte
nb_txn_par_ctr = txn.groupby("IDT_AC").agg(
    NB_TXN      = ("NUM_ORD_MVT_CPB", "count"),
    DERN_TXN_DT = ("DAT_CRE_DT", "max"),
).reset_index()

# Joindre avec CTR
ctr_avec_txn = pd.merge(
    left   = ctr[["IDT_AC","COD_ECV_CTR","SLD_CTR","SEGMENT"]],
    right  = nb_txn_par_ctr,
    on     = "IDT_AC",
    how    = "left",      # garder tous les contrats, même sans transaction
)

# Les NaN dans NB_TXN = aucune transaction → 0
ctr_avec_txn["NB_TXN"] = ctr_avec_txn["NB_TXN"].fillna(0).astype(int)

print(f"Contrats avec transactions  : {(ctr_avec_txn['NB_TXN']>0).sum()}")
print(f"Contrats sans transaction   : {(ctr_avec_txn['NB_TXN']==0).sum()}")
print()
print(ctr_avec_txn.sort_values("NB_TXN", ascending=False).head(8).to_string(index=False))"""),

# ── EXERCICE 8 ──────────────────────────────────────────────
md("""---
### 🟡 Exercice 8 · Jointure complète — Vue analytique client-contrat

**À faire :**
1. Créer `vue_client` = TIE jointé avec TIE_X_CTR (`on="IDT_PI"`, `how="left"`)
2. Joindre `vue_client` avec CTR (`on="IDT_AC"`, `how="left"`)
3. Calculer par `IDT_PI` : nombre de contrats, solde total, solde moyen
4. Trier par solde total décroissant et afficher le top 10 des clients
5. Identifier les clients sans aucun contrat (résultat de la jointure avec NaN)"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────

# 1. TIE + TIE_X_CTR
vue_client = pd.merge(
    tie[["IDT_PI","COD_TYP_TIE","COD_LNG_CTR","LIB_TYP"]],
    txc[["IDT_PI","IDT_AC","COD_ROL_TTL"]],
    on="IDT_PI", how="left"
)

# 2. + CTR
vue_complete = pd.merge(
    vue_client,
    ctr[["IDT_AC","COD_ECV_CTR","SLD_CTR","SEGMENT"]],
    on="IDT_AC", how="left"
)

# 3. Stats par client
stats_client = vue_complete.groupby("IDT_PI").agg(
    NB_CTR  = ("IDT_AC",  "count"),
    SLD_SUM = ("SLD_CTR", "sum"),
    SLD_MOY = ("SLD_CTR", "mean"),
).round(2).reset_index()

# 4. Top 10
print(stats_client.sort_values("SLD_SUM", ascending=False).head(10).to_string(index=False))

# 5. Sans contrat
sans_ctr = vue_complete[vue_complete["IDT_AC"].isna()]
print(f"Clients sans contrat : {sans_ctr['IDT_PI'].nunique()}")"""),

md("""**✅ Correction exercice 8 :**"""),

code("""# ✅ CORRECTION exercice 8 ──────────────────────────────────

# 1. TIE ← TIE_X_CTR
vue_client = pd.merge(
    tie[["IDT_PI","COD_TYP_TIE","COD_LNG_CTR","LIB_TYP","LIB_LNG"]],
    txc[["IDT_PI","IDT_AC","COD_ROL_TTL","FLG_PRE_TTL"]],
    on  = "IDT_PI",
    how = "left",     # garder tous les clients, même ceux sans contrat
)
print(f"Étape 1 : {len(vue_client)} lignes (clients × contrats)")

# 2. + CTR
vue_complete = pd.merge(
    vue_client,
    ctr[["IDT_AC","COD_ECV_CTR","LIB_ECV","SLD_CTR","SEGMENT","CAT_ECV"]],
    on  = "IDT_AC",
    how = "left",
)
print(f"Étape 2 : {len(vue_complete)} lignes")
print()

# 3. Statistiques par client
stats_client = vue_complete.groupby("IDT_PI").agg(
    NB_CTR   = ("IDT_AC",  "count"),
    SLD_SUM  = ("SLD_CTR", "sum"),
    SLD_MOY  = ("SLD_CTR", "mean"),
    NB_ACTIF = ("CAT_ECV", lambda x: (x == "Actif").sum()),  # compter les actifs
).round(2).reset_index()
print("=== Top 10 clients par solde total ===")
top10 = stats_client.sort_values("SLD_SUM", ascending=False).head(10)
print(top10[["IDT_PI","NB_CTR","NB_ACTIF","SLD_SUM","SLD_MOY"]].to_string(index=False))
print()

# 5. Clients sans contrat
print("=== Clients sans contrat ===")
sans_ctr = vue_complete[vue_complete["IDT_AC"].isna()]
nb_sans  = sans_ctr["IDT_PI"].nunique()
print(f"  {nb_sans} client(s) n'ont aucun contrat dans la table CTR")
if nb_sans > 0:
    print(sans_ctr[["IDT_PI","COD_TYP_TIE","LIB_TYP"]].drop_duplicates().to_string(index=False))"""),

# ════════════════════════════════════════════════════════
# SECTION 10 · EXPORT ET CONNEXION SQL
# ════════════════════════════════════════════════════════
md("""---
# 10 · Export et connexion SQL

## 10.1 Exporter un DataFrame

```python
df.to_csv("fichier.csv", sep=";", index=False, encoding="utf-8")
df.to_json("fichier.json", orient="records")
df.to_excel("fichier.xlsx", index=False)   # nécessite openpyxl
```

## 10.2 SQLite : simuler Vertica

En formation, nous utilisons **SQLite en mémoire** pour simuler Vertica.
Les requêtes SQL sont identiques (CTE, window functions, etc.)."""),

code("""# ── Exporter les résultats en CSV ────────────────────────────
from pathlib import Path

SORTIE = Path("../Sorties_Beobank")
SORTIE.mkdir(exist_ok=True)

# Exporter la vue analytique complète
# to_csv() : écrire un DataFrame dans un CSV
# index=False : ne pas écrire l'index Pandas (numéro de ligne) dans le fichier
# sep=";" : même format que nos fichiers d'entrée Beobank
vue_export = vue_complete[[
    "IDT_PI","LIB_TYP","LIB_LNG",
    "IDT_AC","LIB_ECV","SEGMENT","SLD_CTR","CAT_ECV"
]].dropna(subset=["IDT_AC"])   # supprimer les clients sans contrat

vue_export.to_csv(
    SORTIE / "vue_client_contrat.csv",
    sep      = ";",
    index    = False,       # ne pas inclure l'index numérique de Pandas
    encoding = "utf-8",
)
print(f"Fichier exporté : {SORTIE / 'vue_client_contrat.csv'}")
print(f"Lignes : {len(vue_export)}")
print()

# Exporter le résumé par segment
par_segment.to_csv(
    SORTIE / "resume_segments.csv",
    sep=";" , index=False, encoding="utf-8"
)
print(f"Résumé segments exporté : {SORTIE / 'resume_segments.csv'}")

# Vérification
import pandas as pd
relecture = pd.read_csv(SORTIE / "vue_client_contrat.csv", sep=";", encoding="utf-8")
print(f"Vérification relecture : {relecture.shape}")"""),

code("""# ── Connexion SQLite (simulation Vertica) ────────────────────
import sqlite3

print("=== Création de la base SQLite en mémoire ===")
# connect(":memory:") : base de données SQLite temporaire en RAM
# Identique à une vraie Vertica pour les requêtes SELECT, CTE, window functions
conn = sqlite3.connect(":memory:")

# Charger les DataFrames dans SQLite
# to_sql(nom_table, connexion, if_exists="replace", index=False)
for nom, df in [("CTR",ctr), ("TIE",tie), ("TIE_ADR",tie_adr),
                ("TIE_X_CTR",txc), ("TXN_X_CTR",txn)]:
    # Exporter uniquement les colonnes originales (sans nos colonnes calculées)
    cols_orig = [c for c in df.columns if not c.isupper() or len(c) < 15]
    df.to_sql(nom, conn, if_exists="replace", index=False)
    print(f"  Table {nom:<12} chargée ({len(df)} lignes)")

print("\\n✓ Base SQLite prête — toutes les tables sont disponibles")"""),

code("""# ── Requêtes SQL avec pd.read_sql() ──────────────────────────
import pandas as pd

print("=== Requête 1 : Contrats actifs ===")
# pd.read_sql(requete, connexion) : exécute le SQL et retourne un DataFrame
sql_1 = '''
    SELECT
        c.IDT_AC,
        c.COD_ECV_CTR,
        c.SLD_CTR,
        c.COD_DEV,
        c.MNT_INI
    FROM CTR c
    WHERE c.COD_ECV_CTR IN ('1','2','3')
      AND c.SLD_CTR > 5000
    ORDER BY c.SLD_CTR DESC
    LIMIT 10
'''
# pd.read_sql() exécute la requête et retourne un DataFrame
actifs_sql = pd.read_sql(sql_1, conn)
print(actifs_sql.to_string(index=False))"""),

code("""# ── CTE (WITH) : requête avancée ─────────────────────────────
print("=== Requête 2 : Clients avec nb de contrats (CTE) ===")
sql_2 = '''
    WITH ctr_par_client AS (
        SELECT
            IDT_PI,
            COUNT(IDT_AC)    AS NB_CONTRATS,
            SUM(SLD_CTR)     AS SOLDE_TOTAL,
            AVG(SLD_CTR)     AS SOLDE_MOY
        FROM TIE_X_CTR txc
        LEFT JOIN CTR c ON txc.IDT_AC = c.IDT_AC
        GROUP BY IDT_PI
    )
    SELECT
        t.IDT_PI,
        t.COD_TYP_TIE,
        t.COD_LNG_CTR,
        cpc.NB_CONTRATS,
        ROUND(cpc.SOLDE_TOTAL, 2) AS SOLDE_TOTAL,
        ROUND(cpc.SOLDE_MOY,   2) AS SOLDE_MOY
    FROM TIE t
    LEFT JOIN ctr_par_client cpc ON t.IDT_PI = cpc.IDT_PI
    ORDER BY cpc.SOLDE_TOTAL DESC
    LIMIT 10
'''
res_cte = pd.read_sql(sql_2, conn)
print(res_cte.to_string(index=False))"""),

# ── EXERCICE 9 ──────────────────────────────────────────────
md("""---
### 🟡 Exercice 9 · Export et SQL

**À faire :**
1. Exporter `stats_client` (résultat de l'exercice 8) en CSV dans `../Sorties_Beobank/stats_clients.csv`
2. Écrire une requête SQL qui retourne : `IDT_AC`, `COD_ECV_CTR`, `SLD_CTR`, `NUM_TIE` du client
   - Jointure CTR → TIE_X_CTR → TIE
   - Filtrer : `COD_ECV_CTR = '1'` et `SLD_CTR > 10000`
   - Trier par `SLD_CTR DESC`
   - Limiter à 15 lignes"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────
from pathlib import Path
import pandas as pd

SORTIE = Path("../Sorties_Beobank")

# 1. Export CSV
stats_client.to_csv(
    SORTIE / "stats_clients.csv",
    sep=";", index=False, encoding="utf-8"
)
print(f"Exporté : {len(stats_client)} lignes")

# 2. Requête SQL
sql = '''
    SELECT
        c.IDT_AC,
        c.COD_ECV_CTR,
        c.SLD_CTR,
        t.NUM_TIE
    FROM CTR c
    LEFT JOIN TIE_X_CTR txc ON c.IDT_AC = txc.IDT_AC
    LEFT JOIN TIE t         ON txc.IDT_PI = t.IDT_PI
    WHERE c.COD_ECV_CTR = '1'
      AND c.SLD_CTR > 10000
    ORDER BY c.SLD_CTR DESC
    LIMIT 15
'''
res = pd.read_sql(sql, conn)
print(res.to_string(index=False))"""),

md("""**✅ Correction exercice 9 :**"""),

code("""# ✅ CORRECTION exercice 9 (même code que ci-dessus — déjà complet)
print("L'exercice 9 est auto-corrigé.")
print()
print("Points importants :")
print("  1. to_csv(index=False) : ne pas écrire l'index Pandas")
print("  2. LEFT JOIN préféré au INNER JOIN pour garder les enregistrements sans correspondance")
print("  3. L'alias txc pour TIE_X_CTR évite les conflits de nom dans la clause ON")"""),

# ════════════════════════════════════════════════════════
# EXERCICE FINAL DU JOUR 2
# ════════════════════════════════════════════════════════
md("""---
# 🏁 Mini-projet final Jour 2 · Rapport mensuel de portefeuille

**Contexte :** Votre manager vous demande le **rapport mensuel** du portefeuille Beobank.
Il doit être exporté en CSV et contenir les informations suivantes pour chaque **client PP actif** :

| Colonne | Calcul |
|---------|--------|
| `IDT_PI` | Identifiant client |
| `NB_CTR_ACTIFS` | Nombre de contrats actifs (ECV 1,2,3) |
| `SOLDE_TOTAL` | Somme des soldes des contrats actifs |
| `SEGMENT_PRINCIPAL` | Le segment le plus fréquent parmi ses contrats |
| `NB_TXN_3M` | Nombre de transactions dans les 3 derniers mois |
| `LNG` | Langue du client (FR/NL) |

**Étapes :**
1. Joindre TIE + TIE_X_CTR + CTR
2. Filtrer les PP actifs avec contrats actifs
3. Calculer les statistiques par client
4. Joindre avec les transactions (regroupées sur 3 mois)
5. Exporter le résultat en CSV"""),

code("""# 🟡 Exercice final — votre code ────────────────────────────
import pandas as pd
import numpy as np
from pathlib import Path

SORTIE = Path("../Sorties_Beobank")
print("À compléter selon les étapes décrites ci-dessus ...")"""),

md("""**✅ Correction mini-projet final :**"""),

code("""# ✅ CORRECTION mini-projet final Jour 2 ────────────────────
import pandas as pd
import numpy as np
from pathlib import Path

SORTIE = Path("../Sorties_Beobank")
SORTIE.mkdir(exist_ok=True)

# ── Étape 1 : joindre TIE + TIE_X_CTR + CTR ────────────────
# a) TIE (clients PP uniquement)
tie_pp = tie[tie["COD_TYP_TIE"] == "1"][["IDT_PI","COD_LNG_CTR"]]

# b) Joindre avec la table de lien
pp_lien = pd.merge(
    tie_pp,
    txc[["IDT_PI","IDT_AC"]],
    on="IDT_PI", how="left"
)

# c) Joindre avec les contrats
pp_ctr = pd.merge(
    pp_lien,
    ctr[["IDT_AC","COD_ECV_CTR","SLD_CTR","SEGMENT"]],
    on="IDT_AC", how="left"
)

# ── Étape 2 : filtrer contrats actifs ────────────────────────
pp_actifs = pp_ctr[pp_ctr["COD_ECV_CTR"].isin(["1","2","3"])]

# ── Étape 3 : statistiques par client ────────────────────────
stats_pp = pp_actifs.groupby("IDT_PI").agg(
    NB_CTR_ACTIFS    = ("IDT_AC",   "count"),
    SOLDE_TOTAL      = ("SLD_CTR",  "sum"),
    SEGMENT_PRINCIPAL = ("SEGMENT", lambda x: x.mode()[0] if len(x)>0 else "Inconnu"),
    LNG              = ("COD_LNG_CTR", "first"),
).round(2).reset_index()

# ── Étape 4 : transactions des 3 derniers mois ───────────────
date_ref = txn["DAT_CRE_DT"].max()   # date la plus récente = référence
date_3m  = date_ref - pd.DateOffset(months=3)

txn_3m = txn[txn["DAT_CRE_DT"] >= date_3m]
nb_txn_pp = txn_3m.groupby("IDT_AC")["NUM_ORD_MVT_CPB"].count().reset_index()
nb_txn_pp.columns = ["IDT_AC","NB_TXN"]

# Joindre par IDT_AC → IDT_PI via TIE_X_CTR
nb_txn_pi = pd.merge(nb_txn_pp, txc[["IDT_AC","IDT_PI"]], on="IDT_AC", how="left")
nb_txn_par_pi = nb_txn_pi.groupby("IDT_PI")["NB_TXN"].sum().reset_index()
nb_txn_par_pi.columns = ["IDT_PI","NB_TXN_3M"]

# ── Étape 5 : assembler et exporter ─────────────────────────
rapport = pd.merge(stats_pp, nb_txn_par_pi, on="IDT_PI", how="left")
rapport["NB_TXN_3M"] = rapport["NB_TXN_3M"].fillna(0).astype(int)
rapport = rapport.sort_values("SOLDE_TOTAL", ascending=False)

chemin_rapport = SORTIE / "rapport_mensuel_pp.csv"
rapport.to_csv(chemin_rapport, sep=";", index=False, encoding="utf-8")

print(f"Rapport mensuel PP exporté : {chemin_rapport}")
print(f"Clients PP actifs : {len(rapport)}")
print()
print("Top 10 clients PP par solde :")
print(rapport.head(10).to_string(index=False))"""),

md("""---
# Récapitulatif du Jour 2

## Ce que vous maîtrisez maintenant

| Concept | Outil Pandas | Équivalent SAS |
|---------|-------------|----------------|
| Lire un CSV | `pd.read_csv(sep=";",na_values=".")` | `proc import` / `data step` |
| Voir les données | `.head()`, `.info()`, `.describe()` | `proc print`, `proc contents` |
| Fréquences | `.value_counts()` | `proc freq` |
| Sélectionner | `df["col"]`, `df[["c1","c2"]]` | `keep` |
| Filtrer | `df[df["col"]=="v"]` | `where` / `if` |
| Trier | `.sort_values()` | `proc sort` |
| Colonnes calculées | `np.where`, `np.select`, `.map()` | `data step` |
| Grouper / agréger | `.groupby().agg()` | `proc means`, `proc sql group by` |
| Joindre | `pd.merge(how="left")` | `proc sql left join` |
| Exporter | `.to_csv()` | `proc export` |
| SQL | `pd.read_sql(sql, conn)` | `proc sql` |

## Demain (Jour 3)

- **SQL analytique** : CTEs, OVER/PARTITION BY, ROW_NUMBER, LAG/LEAD
- **Time series** : fenêtres glissantes 13 mois, agrégations temporelles
- **Visualisation** : graphiques avec Matplotlib
- **Mini-projet** : pipeline complet de bout en bout"""),
]

chemin = os.path.join(OUT, "Jour2_Fichiers_Pandas_SQL.ipynb")
with open(chemin, "w", encoding="utf-8") as f:
    json.dump(nb(cells), f, ensure_ascii=False, indent=1)
print(f"Jour 2 : {os.path.getsize(chemin)//1024} Ko — {len(cells)} cellules")
