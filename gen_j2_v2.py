"""
Generateur Jour 2 v2 - Fichiers, Pandas et Flux de donnees
Chaque ligne commentee, mini-exercices intercales avec corrections.
Formation Beobank - niveau debutant absolu.
"""
import json, os

OUTPUT_DIR = r"C:\Users\axiat\Desktop\orsys\Beobank\Notebooks"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def md(src):
    lines = src.strip().split('\n')
    s = [l + '\n' for l in lines[:-1]] + [lines[-1]]
    return {"cell_type": "markdown", "metadata": {}, "source": s}

def code(src):
    lines = src.strip().split('\n')
    s = [l + '\n' for l in lines[:-1]] + [lines[-1]]
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": s}

def notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.10.0"}
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

j2 = [

md("""# Jour 2 — Fichiers, Pandas et Flux de donnees
## Formation Python Beobank · 19 novembre 2026

---

### Rappel du contexte

Hier (Jour 1) vous avez appris les bases : variables, conditions, boucles, listes, dictionnaires, fonctions.
Vous avez meme lu `CTR.csv` a la main avec le module `csv`.

Aujourd'hui vous decouvrez **Pandas** : la bibliotheque qui transforme 50 lignes de code hier
en 3 lignes aujourd'hui. C'est l'outil numero 1 de l'analyste data Python.

### Ce que vous allez construire aujourd'hui

Le **rapport mensuel Beobank** avance : vous allez :
1. Charger les 5 tables en une seule cellule
2. Explorer et nettoyer les donnees
3. Creer des colonnes calculees (age, segment, categorie)
4. Joindre les 5 tables pour construire une vue analytique
5. Aggreger et exporter les resultats

> **Rappel :** Shift + Entree pour executer une cellule"""),

md("""---
## Pourquoi Pandas ?

Hier vous avez ecrit 30 lignes pour lire CTR.csv et compter les statuts.
En Pandas ce sera 4 lignes. Voici la comparaison :

```python
# Hier (Python pur) - 30 lignes pour lire + analyser
import csv
contrats = []
with open("CTR.csv", "r") as f:
    for ligne in csv.DictReader(f, delimiter=";"):
        contrats.append(ligne)
# ... 20 lignes de boucles pour compter ...

# Aujourd'hui (Pandas) - 4 lignes
import pandas as pd
ctr = pd.read_csv("CTR.csv", sep=";", na_values=".")
print(ctr.shape)                       # dimensions
print(ctr["COD_ECV_CTR"].value_counts())  # comptage
```

**Pandas** = Python + tables de donnees (comme Excel ou SAS).
Un **DataFrame** Pandas est l'equivalent d'un **dataset SAS**."""),

# ============================================================
# SECTION 1 : SETUP
# ============================================================
md("""---
# Section 1 — Chargement des 5 tables Beobank

## 1.1 Cellule de setup — executer en PREMIER

Cette cellule importe les biblioteques necessaires et charge les 5 tables.
Elle doit etre executee avant toutes les autres."""),

code("""# ── Importer les bibliotheques ───────────────────────────────
# import : charger une bibliotheque externe
# as pd : raccourci pour ne pas ecrire "pandas." a chaque fois

import pandas as pd         # pandas : manipulation de donnees tabulaires
import numpy as np          # numpy  : calculs numeriques (utilise par pandas)
from pathlib import Path    # pathlib: manipulation de chemins de fichiers

# ── Definir le chemin du dossier de donnees ──────────────────
# Path() cree un objet chemin portable (fonctionne Windows, Mac, Linux)
# ".." signifie "remonter d'un niveau dans l'arborescence"
DATA = Path("../Orsys")

# ── Parametres communs de lecture ────────────────────────────
# Ces 3 parametres sont les memes pour tous nos fichiers Beobank
# On les met dans un dictionnaire pour ne pas les repeter
PARAMS = dict(
    sep      = ";",        # separateur de colonnes (point-virgule)
    na_values= ".",        # valeur representant "manquant" (convention SAS)
    encoding = "utf-8"     # encodage des caracteres (gere les accents)
)

# ── Charger les 5 tables ─────────────────────────────────────
# pd.read_csv() : lit un fichier CSV et le transforme en DataFrame
# DATA / "CTR.csv" : construire le chemin complet (operateur / de pathlib)
# **PARAMS : "depaqueter" le dictionnaire = passer ses cles comme arguments

print("Chargement des tables Beobank...")

ctr       = pd.read_csv(DATA / "CTR.csv",       **PARAMS)  # 200 contrats
tie       = pd.read_csv(DATA / "TIE.csv",       **PARAMS)  # 100 clients
tie_adr   = pd.read_csv(DATA / "TIE_ADR.csv",   **PARAMS)  # 100 adresses
tie_x_ctr = pd.read_csv(DATA / "TIE_X_CTR.csv", **PARAMS)  # 200 liens
txn       = pd.read_csv(DATA / "TXN_X_CTR.csv", **PARAMS)  # 1260 transactions

# ── Verifier le chargement ───────────────────────────────────
# .shape : tuple (nombre_lignes, nombre_colonnes)
print()
print(f"{'Table':<12}  {'Lignes':>7}  {'Colonnes':>9}  Description")
print("-" * 60)
print(f"{'ctr':<12}  {ctr.shape[0]:>7,}  {ctr.shape[1]:>9}  Contrats (comptes)")
print(f"{'tie':<12}  {tie.shape[0]:>7,}  {tie.shape[1]:>9}  Clients (tiers)")
print(f"{'tie_adr':<12}  {tie_adr.shape[0]:>7,}  {tie_adr.shape[1]:>9}  Adresses")
print(f"{'tie_x_ctr':<12}  {tie_x_ctr.shape[0]:>7,}  {tie_x_ctr.shape[1]:>9}  Liens client-contrat")
print(f"{'txn':<12}  {txn.shape[0]:>7,}  {txn.shape[1]:>9}  Transactions")
print()
print("Chargement termine !")"""),

md("""---
## 1.2 Explorer un DataFrame — les fonctions essentielles

Equivalences avec SAS :

| Pandas | SAS |
|--------|-----|
| `df.head(10)` | `proc print data=... (obs=10);` |
| `df.info()` | `proc contents;` |
| `df.describe()` | `proc means;` |
| `df["col"].value_counts()` | `proc freq;` |
| `df.shape` | `nobs` et `nvars` |"""),

code("""# ── head() : afficher les premieres lignes ───────────────────
# head(N) : les N premieres lignes (par defaut N=5)
# C'est l'equivalent de proc print (obs=10)

print("Les 5 premieres lignes de CTR :")
ctr.head(5)    # dans Jupyter, le DataFrame est affiche automatiquement"""),

code("""# ── tail() : afficher les dernieres lignes ───────────────────
# tail(N) : les N dernieres lignes
# Utile pour verifier la fin du fichier

print("Les 3 dernieres lignes de CTR :")
ctr.tail(3)"""),

code("""# ── info() : structure du DataFrame ─────────────────────────
# info() affiche :
#   - Le nombre de lignes et de colonnes
#   - Le nom de chaque colonne
#   - Le type de chaque colonne (int64, float64, object=texte)
#   - Le nombre de valeurs non-nulles (pour detecter les manquants)
# Equivalent de proc contents

print("Structure de CTR :")
ctr.info()"""),

code("""# ── describe() : statistiques descriptives ──────────────────
# describe() calcule pour chaque colonne numerique :
#   count = nombre de valeurs non-nulles
#   mean  = moyenne
#   std   = ecart-type
#   min   = minimum
#   25%   = 1er quartile
#   50%   = mediane
#   75%   = 3eme quartile
#   max   = maximum
# Equivalent de proc means

print("Statistiques de CTR :")
ctr.describe()"""),

code("""# ── columns : liste des colonnes ────────────────────────────
# .columns retourne un Index (liste des noms de colonnes)

print("Colonnes de CTR :")
print(list(ctr.columns))  # list() pour un affichage plus lisible

print()
print("Colonnes de TIE :")
print(list(tie.columns))

print()
print("Colonnes de TXN :")
print(list(txn.columns))"""),

code("""# ── dtypes : types de chaque colonne ────────────────────────
# object  = texte (str)
# int64   = entier (nombre sans decimales)
# float64 = decimal (nombre avec decimales)
# bool    = booleen (True/False)

print("Types des colonnes de CTR :")
print(ctr.dtypes)"""),

code("""# ── isnull() : detecter les valeurs manquantes ───────────────
# isnull() : retourne True/False pour chaque cellule (True = manquant)
# .sum()  : additionne les True (True = 1, False = 0) pour compter

print("Valeurs manquantes par colonne dans CTR :")
manquants = ctr.isnull().sum()    # compter les NaN par colonne
total      = len(ctr)             # nombre total de lignes

# Afficher avec le pourcentage
for col in ctr.columns:
    nb_man = manquants[col]       # nb de manquants pour cette colonne
    pct    = nb_man / total * 100 # pourcentage
    print(f"  {col:<20} : {nb_man:>5} manquants ({pct:>5.1f}%)")"""),

# ============================================================
# MINI-EXERCICE 1
# ============================================================
md("""---
### Mini-exercice 2.A — Explorer TIE.csv

Vous venez de voir comment explorer `ctr`. Faites la meme chose sur `tie` (la table des clients).

**A faire :**
1. Afficher les 5 premieres lignes de `tie`
2. Afficher la structure avec `info()`
3. Compter les valeurs manquantes
4. Afficher les statistiques avec `describe()`"""),

code("""# ── Votre code ici ─────────────────────────────────────────
# Exercice 2.A - Exploration de TIE

# 1. Premieres lignes
tie.head(...)

# 2. Structure
tie.info()

# 3. Manquants
# ...

# 4. Statistiques
tie.describe()"""),

md("""**Correction exercice 2.A :**"""),

code("""# ── CORRECTION exercice 2.A ─────────────────────────────────

# 1. Les 5 premieres lignes
print("=== 5 premieres lignes de TIE ===")
print(tie.head(5))
print()

# 2. Structure
print("=== Structure de TIE ===")
tie.info()
print()

# 3. Manquants
print("=== Valeurs manquantes dans TIE ===")
manquants_tie = tie.isnull().sum()
for col, nb in manquants_tie.items():
    pct = nb / len(tie) * 100
    flag = " ← ATTENTION" if pct > 10 else ""
    print(f"  {col:<20}: {nb:>4} manquants ({pct:>5.1f}%){flag}")
print()

# 4. Statistiques (seulement les colonnes numeriques)
print("=== Statistiques de TIE ===")
print(tie.describe())"""),

# ============================================================
# SECTION 2 : SELECTIONNER ET FILTRER
# ============================================================
md("""---
# Section 2 — Selectionner et filtrer les donnees

## 2.1 Selectionner des colonnes

En SAS, on utilise `keep` ou on specifie les colonnes dans `proc print`.
En Pandas, on utilise les crochets `[ ]`."""),

code("""# ── Selectionner UNE colonne → Series ───────────────────────
# df["colonne"] retourne une Series (liste de valeurs avec index)
# C'est comme une seule colonne d'un dataset SAS

# Extraire les codes statut
statuts = ctr["COD_ECV_CTR"]   # Series des codes statut

print("Type:", type(statuts))    # pandas.Series
print()
print("Les 10 premiers codes :")
print(statuts.head(10))
print()
print("Nombre de valeurs :", len(statuts))"""),

code("""# ── Selectionner PLUSIEURS colonnes → DataFrame ──────────────
# df[["col1", "col2"]] : noter les DOUBLES crochets !
# Retourne un DataFrame (sous-ensemble de colonnes)

# Garder seulement les colonnes utiles pour le rapport
colonnes_rapport = ["IDT_AC", "REF_CTR_INN", "DAT_OUV_CTR",
                    "COD_ECV_CTR", "COD_DEV", "SLD_CTR"]

ctr_reduit = ctr[colonnes_rapport]   # creer un DataFrame avec ces colonnes seulement

print(f"DataFrame original  : {ctr.shape}")
print(f"DataFrame reduit    : {ctr_reduit.shape}")
print()
ctr_reduit.head(5)"""),

md("""## 2.2 Filtrer des lignes

En SAS : `where COD_ECV_CTR = '1';` ou `if COD_ECV_CTR = '1' then ...;`
En Pandas : `df[df["col"] == valeur]`"""),

code("""# ── Filtre simple : une condition ───────────────────────────
# df["colonne"] == valeur : cree un masque True/False pour chaque ligne
# df[masque] : garde seulement les lignes ou le masque est True

# Contrats avec statut "1" (Ouvert)
masque_ouvert  = ctr["COD_ECV_CTR"] == "1"   # masque : True/False par ligne
print("Masque (5 premieres valeurs) :")
print(masque_ouvert.head(5))                   # Series de bool

print()

# Appliquer le masque
ctr_ouverts = ctr[masque_ouvert]              # garder les lignes True
print(f"Contrats ouverts (statut 1) : {len(ctr_ouverts)} sur {len(ctr)}")
ctr_ouverts.head(4)"""),

code("""# ── Filtres courants sur nos tables Beobank ─────────────────

# 1. Contrats actifs (statut 1, 2 ou 3) avec isin()
# isin(liste) : equivalent de "IN (1, 2, 3)" en SQL
actifs = ctr[ctr["COD_ECV_CTR"].isin(["1", "2", "3"])]
print(f"Contrats actifs : {len(actifs)}")

# 2. Clients de langue francaise
fr_clients = tie[tie["COD_LNG_CTR"] == "FR"]
print(f"Clients FR      : {len(fr_clients)}")

# 3. Transactions recentes (apres une date)
# D'abord, convertir la colonne en date (on verra ca en detail plus tard)
txn["DAT_TXN_DT"] = pd.to_datetime(txn["DAT_CRE_MVT_CPB"], errors="coerce")
txn_2025 = txn[txn["DAT_TXN_DT"].dt.year >= 2025]
print(f"Transactions 2025+ : {len(txn_2025)}")

# 4. Contrats sans date de cloture (= encore ouverts)
sans_cloture = ctr[ctr["DAT_CLO_CTR"].isna()]   # isna() = True si manquant
print(f"Contrats sans cloture : {len(sans_cloture)}")"""),

code("""# ── Filtres combines : & (et) et | (ou) ─────────────────────
# IMPORTANT : en Pandas, chaque condition doit etre entre parentheses !
# Pas "and" / "or" : utiliser "&" / "|"

# En SQL : WHERE COD_ECV_CTR IN ('1','2','3') AND COD_DEV = 'EUR'
actifs_eur = ctr[
    (ctr["COD_ECV_CTR"].isin(["1","2","3"])) &   # ET actif
    (ctr["COD_DEV"] == "EUR")                      # ET en EUR
]
print(f"Contrats actifs en EUR : {len(actifs_eur)}")

# Contrats clotures OU resilies
fermes = ctr[
    (ctr["COD_ECV_CTR"] == "4") |   # OU cloture
    (ctr["COD_ECV_CTR"] == "6")     # OU resilie
]
print(f"Contrats fermes (4 ou 6) : {len(fermes)}")

# Clients personnes physiques de langue NL
pp_nl = tie[
    (tie["COD_TYP_TIE"] == "1") &   # personne physique
    (tie["COD_LNG_CTR"] == "NL")    # de langue NL
]
print(f"PP neerlandophones : {len(pp_nl)}")"""),

# ============================================================
# MINI-EXERCICE 2
# ============================================================
md("""---
### Mini-exercice 2.B — Filtrer les contrats du rapport

**Contexte :** Pour le rapport mensuel, votre manager veut voir uniquement
les **contrats actifs en EUR** dont le **solde est superieur a 1 000 EUR**.

**A faire :**
1. Filtrer `ctr` pour garder : statut actif (1, 2 ou 3) ET devise EUR ET solde > 1000
2. Compter combien de contrats passent ce filtre
3. Calculer la somme totale de leurs soldes
4. Afficher les 5 premiers"""),

code("""# ── Votre code ici ─────────────────────────────────────────
# Exercice 2.B

# 1. Filtre combine (3 conditions avec &)
filtre = ctr[
    # condition 1 : statut actif
    (ctr["COD_ECV_CTR"].isin([...])) &
    # condition 2 : devise EUR
    (ctr["COD_DEV"] == ...) &
    # condition 3 : solde > 1000 (SLD_CTR est numerique grace a na_values=".")
    (ctr["SLD_CTR"] > ...)
]

# 2. Compter
print(f"Contrats selectionnes : {len(filtre)}")

# 3. Somme des soldes
# .sum() sur une colonne calcule la somme (en ignorant les NaN)
somme = filtre["SLD_CTR"].sum()
print(f"Solde total          : {somme:,.2f} EUR")

# 4. Afficher les 5 premiers
filtre.head(5)"""),

md("""**Correction exercice 2.B :**"""),

code("""# ── CORRECTION exercice 2.B ─────────────────────────────────

# 1. Filtre combine avec 3 conditions
#    Chaque condition entre parentheses, reliees par &
filtre = ctr[
    (ctr["COD_ECV_CTR"].isin(["1", "2", "3"])) &  # actif
    (ctr["COD_DEV"] == "EUR") &                     # en euros
    (ctr["SLD_CTR"] > 1000)                         # solde > 1000
]

# 2. Compter et afficher
nb_total      = len(ctr)
nb_selectionnes = len(filtre)
print(f"Contrats totaux          : {nb_total}")
print(f"Contrats selectionnes    : {nb_selectionnes}")
print(f"Taux de selection        : {nb_selectionnes/nb_total:.1%}")
print()

# 3. Statistiques sur le sous-ensemble filtre
somme   = filtre["SLD_CTR"].sum()     # somme des soldes
moyenne = filtre["SLD_CTR"].mean()    # moyenne
maxi    = filtre["SLD_CTR"].max()     # maximum
print(f"Somme totale des soldes  : {somme:>15,.2f} EUR")
print(f"Solde moyen              : {moyenne:>15,.2f} EUR")
print(f"Solde maximum            : {maxi:>15,.2f} EUR")
print()

# 4. Afficher les 5 premiers (colonnes utiles seulement)
colonnes = ["IDT_AC", "REF_CTR_INN", "COD_ECV_CTR", "COD_DEV", "SLD_CTR"]
filtre[colonnes].head(5)"""),

# ============================================================
# SECTION 3 : COLONNES CALCULEES ET TRANSFORMATIONS
# ============================================================
md("""---
# Section 3 — Creer des colonnes calculees

## 3.1 Ajouter une colonne au DataFrame

En SAS : dans un data step, on cree une variable derivee.
En Pandas : `df["nouvelle_col"] = expression`"""),

code("""# ── Creer une colonne calculee ───────────────────────────────
# On assigne directement au DataFrame
# df["nouveau_nom"] = expression (calculee sur toutes les lignes a la fois)

# Exemple 1 : colonne de libelle de statut (mapping)
# .map(dictionnaire) : applique un mapping sur toute la colonne
MAPPING_ECV = {
    "1":"Ouvert", "2":"En attente", "3":"Suspendu",
    "4":"Cloture", "5":"En resiliation", "6":"Resilie"
}

# Creer la colonne LIB_ECV
# .map() remplace chaque code par le libelle correspondant
# .fillna("Inconnu") remplace les NaN par "Inconnu"
ctr["LIB_ECV"] = ctr["COD_ECV_CTR"].map(MAPPING_ECV).fillna("Inconnu")

print("Colonne LIB_ECV creee :")
ctr[["IDT_AC", "COD_ECV_CTR", "LIB_ECV"]].head(6)"""),

code("""# ── Colonne categorielle (Actif / Inactif) ───────────────────
# np.where(condition, valeur_si_vrai, valeur_si_faux)
# Equivalent de if/else applique sur toute une colonne

# Version avec np.where (1 condition)
ctr["CAT_ECV"] = np.where(
    ctr["COD_ECV_CTR"].isin(["1","2","3"]),  # condition
    "Actif",                                  # si vrai
    "Inactif"                                 # si faux
)

# Verifier la creation
print("Colonnes ajoutees :")
ctr[["COD_ECV_CTR", "LIB_ECV", "CAT_ECV"]].head(8)"""),

code("""# ── Colonnes avec .apply() ──────────────────────────────────
# .apply(fonction) : appliquer une fonction a chaque ligne ou colonne
# Utile quand la logique est complexe (plusieurs conditions)

def classifier_statut_complet(code):
    '''Retourne un tuple (libelle, categorie, priorite) pour un code ECV.'''
    infos = {
        "1": ("Ouvert",         "Actif",   "Normale"),
        "2": ("En attente",     "Actif",   "Surveillance"),
        "3": ("Suspendu",       "Actif",   "Urgente"),
        "4": ("Cloture",        "Inactif", "Aucune"),
        "5": ("En resiliation", "Inactif", "Critique"),
        "6": ("Resilie",        "Inactif", "Aucune"),
    }
    return infos.get(str(code), ("Inconnu", "Inconnu", "Inconnue"))

# Appliquer la fonction et depaqueter le tuple en 3 colonnes
# zip(*...) : "transpose" la liste de tuples en 3 listes separees
resultats = ctr["COD_ECV_CTR"].apply(classifier_statut_complet)
ctr["LIB_ECV2"], ctr["CAT_ECV2"], ctr["PRIORITE"] = zip(*resultats)

print("Colonnes enrichies :")
ctr[["COD_ECV_CTR", "LIB_ECV2", "CAT_ECV2", "PRIORITE"]].head(6)"""),

code("""# ── Colonnes de dates ────────────────────────────────────────
# pd.to_datetime() : convertir une colonne texte en dates Python
# errors="coerce" : mettre NaT (manquant) si la conversion echoue

# Convertir les dates de CTR
ctr["DAT_OUV_DT"] = pd.to_datetime(ctr["DAT_OUV_CTR"], errors="coerce")
ctr["DAT_CLO_DT"] = pd.to_datetime(ctr["DAT_CLO_CTR"], errors="coerce")

print("Types avant/apres conversion :")
print(f"  DAT_OUV_CTR (texte)  : {ctr['DAT_OUV_CTR'].dtype}")
print(f"  DAT_OUV_DT  (date)   : {ctr['DAT_OUV_DT'].dtype}")
print()

# Extraire des composantes de date avec .dt
# .dt.year  : annee
# .dt.month : mois (1 a 12)
# .dt.day   : jour
# .dt.strftime('%Y-%m') : formater en texte

ctr["ANNEE_OUV"]  = ctr["DAT_OUV_DT"].dt.year    # colonne d'annee
ctr["MOIS_OUV"]   = ctr["DAT_OUV_DT"].dt.month   # colonne de mois (1-12)
ctr["MOIS_STR"]   = ctr["DAT_OUV_DT"].dt.strftime("%Y-%m")  # ex: "2024-05"

print("Colonnes de dates extraites :")
ctr[["DAT_OUV_CTR", "DAT_OUV_DT", "ANNEE_OUV", "MOIS_OUV", "MOIS_STR"]].head(5)"""),

code("""# ── Calcul d'age pour TIE ────────────────────────────────────
# Calculer l'age des clients a partir de leur date de naissance

# 1. Convertir la date de naissance
tie["DAT_NAI_DT"] = pd.to_datetime(tie["DAT_NAI"], errors="coerce")

# 2. Calculer l'age
# pd.Timestamp.today() : date et heure actuelles
# .dt.days : convertir une duree en nombre de jours
# / 365.25 : diviser pour obtenir des annees (365.25 pour les annees bissextiles)
tie["AGE"] = ((pd.Timestamp.today() - tie["DAT_NAI_DT"]).dt.days / 365.25).round(0)

# 3. Convertir en entier nullable (Int64 avec majuscule gere les NaN)
tie["AGE"] = tie["AGE"].astype("Int64")

print("Ages calcules :")
tie[["IDT_PI", "DAT_NAI", "AGE"]].dropna().head(8)
# .dropna() : enlever les lignes avec des NaN pour l'affichage"""),

code("""# ── pd.cut() : creer des tranches d'age ─────────────────────
# pd.cut(serie, bins=..., labels=...) : decouper en intervalles
# C'est l'equivalent de PROC FORMAT + tranches en SAS

# Definir les bornes des tranches
# [0, 25) : de 0 a 24 ans → "<25 ans"
# [25, 35): de 25 a 34 ans → "25-34 ans"
# etc.

tie["TRANCHE_AGE"] = pd.cut(
    tie["AGE"].astype(float),           # convertir en float pour pd.cut
    bins   = [0, 25, 35, 50, 65, 120], # les bornes des intervalles
    labels = ["<25 ans", "25-34 ans", "35-49 ans", "50-64 ans", "65+ ans"],
    right  = False                      # False = bornes gauches incluses
)

print("Repartition par tranche d'age :")
print(tie["TRANCHE_AGE"].value_counts().sort_index())
# .value_counts() : compter les occurrences de chaque valeur
# .sort_index()   : trier par index (ici = l'ordre des tranches)"""),

# ============================================================
# MINI-EXERCICE 3
# ============================================================
md("""---
### Mini-exercice 2.C — Enrichir CTR avec des colonnes calculees

**Contexte :** Pour le tableau de bord, vous avez besoin d'enrichir `ctr`
avec 3 nouvelles colonnes :
1. `DUREE_JOURS` : nombre de jours depuis l'ouverture du contrat jusqu'a aujourd'hui
   (si pas cloture) ou jusqu'a la date de cloture (si cloture)
2. `ANCIENNETE` : categorie selon `DUREE_JOURS`
   - < 365 jours → `"< 1 an"`
   - 365 a 730 jours → `"1-2 ans"`
   - > 730 jours → `"> 2 ans"`
3. `DEVISE_LIB` : libelle complet de la devise (EUR → "Euro", USD → "Dollar US",
   GBP → "Livre sterling", toute autre → "Autre")

**Hint :** Pour la duree, utiliser `pd.Timestamp.today()` et `.dt.days`"""),

code("""# ── Votre code ici ─────────────────────────────────────────
# Exercice 2.C

# 1. Calculer DUREE_JOURS
# (la date de reference est la date de cloture si elle existe, sinon aujourd'hui)
today = pd.Timestamp.today()

# date_ref : DAT_CLO_DT si elle existe, sinon today
# hint : utilisez .where() ou .fillna()
ctr["DATE_REF"] = ctr["DAT_CLO_DT"].fillna(today)   # fillna remplace NaT par today
ctr["DUREE_JOURS"] = (ctr["DATE_REF"] - ctr["DAT_OUV_DT"]).dt.days

# 2. ANCIENNETE avec pd.cut() ou np.select()
# ...

# 3. DEVISE_LIB avec .map()
MAPPING_DEV = {"EUR": "Euro", "USD": "Dollar US", "GBP": "Livre sterling"}
# ...

# Verifier
ctr[["IDT_AC", "DAT_OUV_CTR", "DUREE_JOURS", "ANCIENNETE", "COD_DEV", "DEVISE_LIB"]].head(6)"""),

md("""**Correction exercice 2.C :**"""),

code("""# ── CORRECTION exercice 2.C ─────────────────────────────────
import numpy as np

today = pd.Timestamp.today()

# 1. Date de reference : cloture si disponible, sinon aujourd'hui
#    .fillna(today) : remplace les NaT (manquants de date) par today
ctr["DATE_REF"]    = ctr["DAT_CLO_DT"].fillna(today)

# Calculer la duree en jours
# soustraction de deux dates = Timedelta
# .dt.days : convertir Timedelta en nombre de jours
ctr["DUREE_JOURS"] = (ctr["DATE_REF"] - ctr["DAT_OUV_DT"]).dt.days

# 2. ANCIENNETE : categoriser avec np.select (plusieurs conditions)
conditions = [
    ctr["DUREE_JOURS"] < 365,                                   # < 1 an
    (ctr["DUREE_JOURS"] >= 365) & (ctr["DUREE_JOURS"] <= 730), # 1-2 ans
    ctr["DUREE_JOURS"] > 730                                    # > 2 ans
]
choix = ["< 1 an", "1-2 ans", "> 2 ans"]
ctr["ANCIENNETE"] = np.select(conditions, choix, default="Inconnu")

# 3. DEVISE_LIB : mapping avec fillna pour les devises non listees
MAPPING_DEV = {
    "EUR": "Euro",
    "USD": "Dollar US",
    "GBP": "Livre sterling"
}
# .map() remplace les valeurs, .fillna("Autre") pour les devises inconnues
ctr["DEVISE_LIB"] = ctr["COD_DEV"].map(MAPPING_DEV).fillna("Autre")

# Verification
print("Colonnes creees :")
print()
colonnes = ["IDT_AC", "DAT_OUV_CTR", "DUREE_JOURS", "ANCIENNETE",
            "COD_DEV", "DEVISE_LIB", "LIB_ECV"]
print(ctr[colonnes].head(8).to_string(index=False))

print()
print("Repartition par anciennete :")
print(ctr["ANCIENNETE"].value_counts())"""),

# ============================================================
# SECTION 4 : TRIER ET AGRÉGER
# ============================================================
md("""---
# Section 4 — Trier, grouper et agreger

## 4.1 Trier

Equivalent SAS : `proc sort by ...;`"""),

code("""# ── sort_values() : trier un DataFrame ──────────────────────
# by    : nom de la colonne ou liste de colonnes
# ascending : True = croissant (defaut), False = decroissant
# na_position : "last" = les NaN a la fin (defaut)

# Trier par solde decroissant
ctr_trie_solde = ctr.sort_values("SLD_CTR", ascending=False)
print("Top 5 soldes les plus eleves :")
ctr_trie_solde[["IDT_AC", "LIB_ECV", "SLD_CTR", "COD_DEV"]].head(5)"""),

code("""# ── Trier sur plusieurs colonnes ────────────────────────────
# sort_values(["col1", "col2"]) : trier d'abord par col1, puis col2 a egalite

ctr_multi = ctr.sort_values(
    ["CAT_ECV", "SLD_CTR"],       # trier par categorie puis par solde
    ascending = [True, False]     # categorie croissant, solde decroissant
)

print("Tri par categorie (asc) puis solde (desc) :")
ctr_multi[["IDT_AC", "CAT_ECV", "LIB_ECV", "SLD_CTR"]].head(8)"""),

md("""## 4.2 Grouper et agreger : groupby()

C'est l'outil le plus puissant de Pandas pour l'analyse.
Equivalent SAS : `proc summary` / `proc means` avec `BY group;`

```
df.groupby("col_groupe")   ← definir les groupes (BY en SAS)
  .agg(                     ← definir les calculs
      nouveau_nom = ("col_source", "fonction")
  )
```"""),

code("""# ── groupby simple : compter par statut ─────────────────────
# groupby("colonne") : creer des groupes
# .size()           : compter le nombre de lignes dans chaque groupe
# .reset_index()    : remettre les index en colonnes

repartition_statut = (
    ctr
    .groupby("LIB_ECV")    # grouper par libelle de statut
    .size()                 # compter les contrats dans chaque groupe
    .reset_index(name="nb_contrats")  # nommer la colonne de comptage
    .sort_values("nb_contrats", ascending=False)  # trier par nb
)

print("Repartition des contrats par statut :")
print(repartition_statut.to_string(index=False))"""),

code("""# ── groupby avec agg() : plusieurs calculs ──────────────────
# agg() permet de calculer plusieurs indicateurs en meme temps
# Syntaxe : nouveau_nom = ("colonne_source", "fonction_aggregation")
# Fonctions : "count", "sum", "mean", "min", "max", "median", "nunique"

stats_par_statut = (
    ctr
    .groupby("LIB_ECV")    # grouper par statut
    .agg(
        nb_contrats   = ("IDT_AC",    "count"),  # compter les contrats
        solde_total   = ("SLD_CTR",   "sum"),    # sommer les soldes
        solde_moyen   = ("SLD_CTR",   "mean"),   # moyenne des soldes
        solde_max     = ("SLD_CTR",   "max"),    # solde le plus eleve
        nb_devises    = ("COD_DEV",   "nunique") # nb de devises differentes
    )
    .reset_index()          # remettre LIB_ECV en colonne
    .sort_values("nb_contrats", ascending=False)
)

# .round(2) : arrondir les decimaux a 2 chiffres
stats_par_statut["solde_total"] = stats_par_statut["solde_total"].round(2)
stats_par_statut["solde_moyen"] = stats_par_statut["solde_moyen"].round(2)

print("Statistiques par statut de contrat :")
print(stats_par_statut.to_string(index=False))"""),

code("""# ── groupby sur plusieurs colonnes ──────────────────────────
# Grouper sur deux colonnes = creer des sous-groupes

stats_annee_cat = (
    ctr
    .groupby(["ANNEE_OUV", "CAT_ECV"])   # grouper par annee ET categorie
    .agg(
        nb     = ("IDT_AC",  "count"),
        solde  = ("SLD_CTR", "sum"),
    )
    .reset_index()
    .sort_values(["ANNEE_OUV", "CAT_ECV"])
)

print("Contrats par annee d'ouverture et categorie :")
print(stats_annee_cat.dropna().to_string(index=False))"""),

code("""# ── value_counts() : comptage rapide ────────────────────────
# .value_counts() : compte les occurrences de chaque valeur unique
# C'est un raccourci pour groupby + count quand on veut juste compter

print("=== value_counts() sur COD_ECV_CTR ===")
vc = ctr["COD_ECV_CTR"].value_counts()
print(vc)
print()

# normalize=True : en proportion (%)
print("=== En pourcentage (normalize=True) ===")
vc_pct = ctr["COD_ECV_CTR"].value_counts(normalize=True) * 100
print(vc_pct.round(1))
print()

# dropna=False : inclure les NaN dans le comptage
print("=== COD_DEV (avec NaN) ===")
print(ctr["COD_DEV"].value_counts(dropna=False))"""),

# ============================================================
# MINI-EXERCICE 4
# ============================================================
md("""---
### Mini-exercice 2.D — Rapport mensuel de transactions

**Contexte :** La table `txn` contient toutes les transactions.
Votre manager veut voir l'**activite mensuelle** : combien de transactions
par mois, combien de comptes distincts, etc.

**A faire :**
1. S'assurer que `txn["DAT_TXN_DT"]` est bien une date (conversion si besoin)
2. Creer une colonne `MOIS` au format "2025-01" avec `.dt.strftime()`
3. Grouper par `MOIS` et calculer :
   - `nb_txn` : nombre de transactions
   - `nb_comptes` : nombre de comptes distincts (`nunique`)
4. Trier par mois et afficher"""),

code("""# ── Votre code ici ─────────────────────────────────────────
# Exercice 2.D

# 1. Conversion date
txn["DAT_TXN_DT"] = pd.to_datetime(txn["DAT_CRE_MVT_CPB"], errors="coerce")

# 2. Creer colonne MOIS
txn["MOIS"] = txn["DAT_TXN_DT"].dt.strftime(...)

# 3. Groupby + agg
stats_mensuelles = (
    txn
    .groupby("MOIS")
    .agg(
        nb_txn     = ...,
        nb_comptes = ...,
    )
    .reset_index()
    .sort_values("MOIS")
)

# 4. Affichage
print(stats_mensuelles.to_string(index=False))"""),

md("""**Correction exercice 2.D :**"""),

code("""# ── CORRECTION exercice 2.D ─────────────────────────────────

# 1. Conversion de la colonne en date
txn["DAT_TXN_DT"] = pd.to_datetime(txn["DAT_CRE_MVT_CPB"], errors="coerce")

# 2. Creer la colonne MOIS au format "YYYY-MM"
# .dt.strftime("%Y-%m") : formater la date en texte
# %Y = annee 4 chiffres, %m = mois 2 chiffres
txn["MOIS"] = txn["DAT_TXN_DT"].dt.strftime("%Y-%m")

# 3. Aggregation mensuelle
stats_mensuelles = (
    txn
    .dropna(subset=["MOIS"])    # eliminer les lignes sans date
    .groupby("MOIS")            # grouper par mois
    .agg(
        nb_txn     = ("NUM_ORD_MVT_CPB", "count"),   # compter les transactions
        nb_comptes = ("IDT_AC",           "nunique"), # nb de comptes uniques
        nb_folios  = ("NUM_FOL_XTR",      "nunique"), # nb de folios uniques
    )
    .reset_index()
    .sort_values("MOIS")
)

# 4. Affichage formate
print(f"{'Mois':>7}  {'Transactions':>13}  {'Comptes':>8}  {'Folios':>8}")
print("-" * 42)
for _, row in stats_mensuelles.iterrows():
    print(f"  {row['MOIS']:>5}  {row['nb_txn']:>13,}  {row['nb_comptes']:>8,}  {row['nb_folios']:>8,}")
print("-" * 42)
print(f"  {'TOTAL':>5}  {stats_mensuelles['nb_txn'].sum():>13,}")"""),

# ============================================================
# SECTION 5 : JOINTURES
# ============================================================
md("""---
# Section 5 — Jointures entre les tables

## 5.1 Comprendre les jointures

Les jointures permettent de combiner plusieurs tables.
Equivalent SAS : `proc sql select * from A left join B on A.key = B.key`

| Pandas | SQL | SAS |
|--------|-----|-----|
| `how="left"` | LEFT JOIN | LEFT JOIN |
| `how="inner"` | INNER JOIN | (defaut) |
| `how="outer"` | FULL OUTER JOIN | FULL JOIN |

**Nos cles de jointure :**
- `CTR.IDT_AC` = `TIE_X_CTR.IDT_AC` (cle contrat)
- `TIE.IDT_PI` = `TIE_X_CTR.IDT_PI` = `TIE_ADR.IDT_PI` (cle tiers)"""),

code("""# ── merge() : joindre deux DataFrames ───────────────────────
# pd.merge(left, right, on="cle", how="left")
# left  : DataFrame de gauche (la "table principale")
# right : DataFrame de droite (la "table de reference")
# on    : nom de la colonne de jointure (meme nom dans les deux tables)
# how   : type de jointure ("left", "inner", "outer", "right")

# Jointure 1 : TIE_X_CTR + CTR
# → pour chaque lien client-contrat, avoir les infos du contrat
lien_ctr = pd.merge(
    tie_x_ctr,                  # table de gauche : les liens
    ctr[["IDT_AC", "REF_CTR_INN", "LIB_ECV", "CAT_ECV", "SLD_CTR", "COD_DEV"]],
    on  = "IDT_AC",             # cle de jointure commune
    how = "left"                # LEFT JOIN : garder tous les liens
)

print(f"TIE_X_CTR         : {len(tie_x_ctr):>5} lignes")
print(f"Apres join CTR    : {len(lien_ctr):>5} lignes (doit etre identique)")
print()
lien_ctr.head(5)"""),

code("""# ── Jointure 2 : ajouter les infos client ───────────────────

# Joindre les infos du tiers (TIE)
vue = pd.merge(
    lien_ctr,                                  # a gauche : lien + contrat
    tie[["IDT_PI", "COD_TYP_TIE", "COD_SEX",  # colonnes utiles de TIE
         "COD_LNG_CTR", "AGE", "TRANCHE_AGE"]],
    on  = "IDT_PI",                            # cle de jointure
    how = "left"
)

print(f"Apres join TIE    : {len(vue):>5} lignes")
print()
vue.head(4)"""),

code("""# ── Jointure 3 : ajouter les adresses ───────────────────────

# Joindre TIE_ADR
vue = pd.merge(
    vue,
    tie_adr[["IDT_PI", "NOM_TIE", "PRN", "NOM_VIL", "COD_PST", "COD_PAY_ISO"]],
    on  = "IDT_PI",
    how = "left"
)

print(f"Apres join TIE_ADR: {len(vue):>5} lignes")
print()

# Afficher un extrait de la vue complete
colonnes_affich = ["NOM_TIE", "PRN", "REF_CTR_INN", "LIB_ECV",
                   "SLD_CTR", "NOM_VIL", "TRANCHE_AGE"]
vue[colonnes_affich].dropna(subset=["NOM_TIE"]).head(6)"""),

code("""# ── Jointure avec les transactions ──────────────────────────
# Combien de transactions par contrat ?

# D'abord, aggreger les transactions par compte
stats_txn_par_ctr = (
    txn
    .groupby("IDT_AC")
    .agg(
        nb_txn_total = ("NUM_ORD_MVT_CPB", "count"),   # nb total de transactions
        premiere_txn = ("DAT_TXN_DT",       "min"),    # date de la premiere txn
        derniere_txn = ("DAT_TXN_DT",       "max"),    # date de la derniere txn
    )
    .reset_index()
)

# Joindre ces stats a la vue principale
vue = pd.merge(
    vue,
    stats_txn_par_ctr,
    on  = "IDT_AC",
    how = "left"
)

# Les comptes sans transactions auront NaN → on les met a 0
vue["nb_txn_total"] = vue["nb_txn_total"].fillna(0).astype(int)

print(f"Vue complete finale : {len(vue):>5} lignes x {vue.shape[1]} colonnes")
print()
print("Distribution des transactions par contrat :")
print(vue["nb_txn_total"].describe().round(1))"""),

# ============================================================
# MINI-EXERCICE 5
# ============================================================
md("""---
### Mini-exercice 2.E — Jointure TIE + TIE_ADR

**Contexte :** Votre manager veut une liste des clients avec leur ville,
le nombre de contrats qu'ils detiennent, et leur tranche d'age.

**A faire :**
1. Joindre `tie` et `tie_adr` sur `IDT_PI` (LEFT JOIN)
2. Joindre le resultat avec `tie_x_ctr` sur `IDT_PI`
3. Grouper par `IDT_PI` + `NOM_TIE` + `TRANCHE_AGE` pour compter le nombre de contrats
4. Afficher les clients avec le plus de contrats"""),

code("""# ── Votre code ici ─────────────────────────────────────────
# Exercice 2.E

# 1. TIE + TIE_ADR
clients_adresses = pd.merge(
    tie[["IDT_PI", "COD_TYP_TIE", "TRANCHE_AGE", "COD_LNG_CTR"]],
    tie_adr[["IDT_PI", "NOM_TIE", "PRN", "NOM_VIL"]],
    on  = ...,
    how = "left"
)

# 2. + TIE_X_CTR pour compter les contrats
clients_ctr = pd.merge(
    clients_adresses,
    tie_x_ctr[["IDT_PI", "IDT_AC"]],
    on  = ...,
    how = "left"
)

# 3. Groupby pour compter les contrats par client
nb_ctr_par_client = (
    clients_ctr
    .groupby(["IDT_PI", "NOM_TIE", "PRN", "TRANCHE_AGE", "NOM_VIL"])
    .agg(nb_contrats = ...)
    .reset_index()
    .sort_values("nb_contrats", ascending=False)
)

# 4. Affichage
nb_ctr_par_client.head(8)"""),

md("""**Correction exercice 2.E :**"""),

code("""# ── CORRECTION exercice 2.E ─────────────────────────────────

# 1. TIE + TIE_ADR : infos clients + adresses
clients_adresses = pd.merge(
    tie[["IDT_PI", "COD_TYP_TIE", "AGE", "TRANCHE_AGE", "COD_LNG_CTR", "COD_SEX"]],
    tie_adr[["IDT_PI", "NOM_TIE", "PRN", "NOM_VIL", "COD_PST"]],
    on  = "IDT_PI",    # cle commune entre TIE et TIE_ADR
    how = "left"       # garder tous les clients, meme sans adresse
)

print(f"TIE + TIE_ADR : {len(clients_adresses)} lignes")

# 2. + TIE_X_CTR : ajouter les liens contrats
clients_ctr = pd.merge(
    clients_adresses,
    tie_x_ctr[["IDT_PI", "IDT_AC", "FLG_PRE_TTL"]],
    on  = "IDT_PI",
    how = "left"
)

print(f"+ TIE_X_CTR   : {len(clients_ctr)} lignes (plusieurs lignes par client normal)")

# 3. Grouper par client et compter les contrats
nb_ctr_par_client = (
    clients_ctr
    .groupby(["IDT_PI", "NOM_TIE", "PRN", "TRANCHE_AGE", "NOM_VIL"])
    .agg(nb_contrats = ("IDT_AC", "count"))   # compter les contrats
    .reset_index()
    .sort_values("nb_contrats", ascending=False)   # plus de contrats en premier
)

# 4. Affichage des 8 clients avec le plus de contrats
print()
print("Clients avec le plus de contrats :")
print()
colonnes = ["NOM_TIE", "PRN", "TRANCHE_AGE", "NOM_VIL", "nb_contrats"]
print(nb_ctr_par_client[colonnes].head(8).to_string(index=False))"""),

# ============================================================
# SECTION 6 : LIRE ET ECRIRE DES FICHIERS
# ============================================================
md("""---
# Section 6 — Lire et ecrire des fichiers

## 6.1 Formats supportes par Pandas"""),

code("""# ── Lecture de fichiers ──────────────────────────────────────
# Vous savez deja lire des CSV. Voici les autres formats courants.

from pathlib import Path
DATA = Path("../Orsys")

# CSV : read_csv() - vous le connaissez
# ctr = pd.read_csv("CTR.csv", sep=";", na_values=".", encoding="utf-8")

# ── Ecriture CSV ─────────────────────────────────────────────
# to_csv() : sauvegarder un DataFrame en CSV

# Exporter la table CTR enrichie
sortie_csv = "CTR_enrichi.csv"
ctr.to_csv(
    sortie_csv,
    sep       = ";",          # separateur point-virgule (compatible SAS/Excel)
    index     = False,        # ne pas exporter la colonne d'index (0,1,2...)
    encoding  = "utf-8"       # encodage
)
print(f"Export CSV : {sortie_csv}")

# Verifier l'export
ctr_relu = pd.read_csv(sortie_csv, sep=";", encoding="utf-8")
print(f"Lignes relues : {len(ctr_relu)}")
print(f"Colonnes      : {list(ctr_relu.columns)[:5]}...")  # 5 premieres colonnes"""),

code("""# ── Ecriture JSON ────────────────────────────────────────────
# Plusieurs formats JSON disponibles

# Format "records" : liste de dictionnaires [{...}, {...}]
# Tres lisible et compatible avec beaucoup d'outils

extrait_ctr = ctr[["IDT_AC", "LIB_ECV", "CAT_ECV", "SLD_CTR"]].head(5)

# Exporter en JSON
extrait_ctr.to_json(
    "extrait_ctr.json",
    orient  = "records",   # format liste de dicts
    indent  = 2,           # indentation pour lisibilite
    force_ascii = False    # garder les accents
)
print("Export JSON : extrait_ctr.json")

# Afficher le contenu JSON
import json
with open("extrait_ctr.json", "r", encoding="utf-8") as f:
    data = json.load(f)
print("Contenu JSON (2 premiers elements) :")
for item in data[:2]:
    print(" ", item)"""),

code("""# ── Lire et ecrire des fichiers texte simples ───────────────
# open() : ouvrir un fichier
# "w"    : mode ecriture (write) - cree ou ecrase le fichier
# "a"    : mode ajout (append) - ajoute a la fin
# "r"    : mode lecture (read) - defaut

# Ecrire un fichier de log
with open("rapport_log.txt", "w", encoding="utf-8") as f:
    # f.write() ecrit une chaine dans le fichier
    f.write("=== RAPPORT DE TRAITEMENT BEOBANK ===\n")  # \n = saut de ligne
    f.write(f"Date : {pd.Timestamp.today().strftime('%d/%m/%Y %H:%M')}\n")
    f.write(f"Contrats charges    : {len(ctr)}\n")
    f.write(f"Clients charges     : {len(tie)}\n")
    f.write(f"Transactions        : {len(txn)}\n")
    f.write("======================================\n")

print("Fichier de log ecrit.")
print()

# Relire et afficher le fichier
with open("rapport_log.txt", "r", encoding="utf-8") as f:
    contenu = f.read()   # lire tout le contenu en une seule chaine

print(contenu)"""),

# ============================================================
# MINI-EXERCICE 6
# ============================================================
md("""---
### Mini-exercice 2.F — Exporter le rapport mensuel

**Contexte :** Vous avez calcule les statistiques mensuelles dans l'exercice 2.D.
Votre manager veut le rapport dans 2 formats :
1. Un fichier CSV pour l'envoyer a l'equipe Finance
2. Un fichier JSON pour l'API interne Beobank

**A faire :**
1. Reprendre `stats_mensuelles` de l'exercice 2.D (ou la recalculer)
2. Exporter en CSV avec separateur `;`
3. Exporter en JSON format `records`
4. Relire le CSV et verifier qu'il a le bon nombre de lignes"""),

code("""# ── Votre code ici ─────────────────────────────────────────
# Exercice 2.F

# stats_mensuelles est deja disponible si vous avez execute l'exercice 2.D
# Sinon, recalculez-la ici

# 1. Export CSV
stats_mensuelles.to_csv(
    "rapport_mensuel.csv",
    sep   = ...,
    index = ...
)
print("Export CSV : rapport_mensuel.csv")

# 2. Export JSON
stats_mensuelles.to_json(
    "rapport_mensuel.json",
    orient = ...,
    indent = 2
)
print("Export JSON : rapport_mensuel.json")

# 3. Verifier le CSV
verifie = pd.read_csv("rapport_mensuel.csv", sep=...)
print(f"Lignes relues : {len(verifie)}")"""),

md("""**Correction exercice 2.F :**"""),

code("""# ── CORRECTION exercice 2.F ─────────────────────────────────

# Recalculer stats_mensuelles si besoin
txn["DAT_TXN_DT"] = pd.to_datetime(txn["DAT_CRE_MVT_CPB"], errors="coerce")
txn["MOIS"] = txn["DAT_TXN_DT"].dt.strftime("%Y-%m")

stats_mensuelles = (
    txn
    .dropna(subset=["MOIS"])
    .groupby("MOIS")
    .agg(
        nb_txn     = ("NUM_ORD_MVT_CPB", "count"),
        nb_comptes = ("IDT_AC",           "nunique"),
        nb_folios  = ("NUM_FOL_XTR",      "nunique"),
    )
    .reset_index()
    .sort_values("MOIS")
)

# 1. Export CSV avec separateur ;
stats_mensuelles.to_csv(
    "rapport_mensuel.csv",
    sep   = ";",     # separateur point-virgule
    index = False    # ne pas inclure l'index numerique
)
print("Export CSV  : rapport_mensuel.csv")

# 2. Export JSON format "records"
stats_mensuelles.to_json(
    "rapport_mensuel.json",
    orient      = "records",  # liste de dictionnaires
    indent      = 2,          # indentation pour lisibilite
    force_ascii = False       # conserver les caracteres speciaux
)
print("Export JSON : rapport_mensuel.json")

# 3. Verifier le CSV
verifie = pd.read_csv("rapport_mensuel.csv", sep=";")
print(f"\nVerification CSV :")
print(f"  Lignes  : {len(verifie)} (attendu : {len(stats_mensuelles)})")
print(f"  Colonnes: {list(verifie.columns)}")
print()
print(verifie.head(4).to_string(index=False))"""),

# ============================================================
# SECTION 7 : CONNEXION SQL (SQLITE)
# ============================================================
md("""---
# Section 7 — SQL et Pandas : le flux Vertica

## 7.1 Architecture : comment Python parle a Vertica

```
Python / Pandas
      |
      | Connexion (driver vertica_python)
      v
  Vertica
      |
      | Resultat (SELECT ...)
      v
Python / Pandas (DataFrame)
      |
      | .to_csv(), .to_json()...
      v
  Fichier / Excel
```

En formation, nous utilisons **SQLite** (base de donnees legere incluse dans Python)
pour simuler Vertica. La syntaxe SQL est identique pour nos requetes."""),

code("""# ── Creer une base SQLite et charger nos tables ──────────────
import sqlite3  # module SQLite integre dans Python (pas besoin d'installer)

# Creer une connexion a une base en memoire (":memory:" = pas de fichier disque)
# En production : conn = vertica_python.connect(host=..., user=..., password=...)
conn = sqlite3.connect(":memory:")

# Charger nos 5 tables dans SQLite
# to_sql() : ecrire un DataFrame dans une table SQL
# if_exists="replace" : remplacer la table si elle existe deja
# index=False : ne pas ecrire la colonne d'index

ctr.to_sql("CTR",         conn, if_exists="replace", index=False)
tie.to_sql("TIE",         conn, if_exists="replace", index=False)
tie_adr.to_sql("TIE_ADR", conn, if_exists="replace", index=False)
tie_x_ctr.to_sql("TIE_X_CTR", conn, if_exists="replace", index=False)
txn.to_sql("TXN",         conn, if_exists="replace", index=False)

print("Tables chargees dans SQLite :")
# Lister les tables existantes
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
print(tables.to_string(index=False))"""),

code("""# ── pd.read_sql() : executer une requete SQL ─────────────────
# pd.read_sql(requete, connexion) : execute le SQL et retourne un DataFrame

# Requete 1 : TOP 10 contrats par solde
sql_top10 = '''
SELECT
    IDT_AC,
    REF_CTR_INN,
    LIB_ECV,
    SLD_CTR,
    COD_DEV
FROM CTR
WHERE SLD_CTR IS NOT NULL
ORDER BY SLD_CTR DESC
LIMIT 10
'''
# Executer et recuperer dans un DataFrame
top10_soldes = pd.read_sql(sql_top10, conn)

print("Top 10 contrats par solde :")
print(top10_soldes.to_string(index=False))"""),

code("""# ── Requete avec jointure en SQL ─────────────────────────────
# Equivalent de ce que vous faites avec pd.merge()

sql_jointure = '''
SELECT
    t.IDT_PI,
    a.NOM_TIE,
    a.PRN,
    a.NOM_VIL,
    c.REF_CTR_INN,
    c.LIB_ECV,
    c.SLD_CTR
FROM TIE_X_CTR  lk
JOIN TIE         t  ON lk.IDT_PI = t.IDT_PI
LEFT JOIN TIE_ADR a  ON t.IDT_PI  = a.IDT_PI
LEFT JOIN CTR     c  ON lk.IDT_AC  = c.IDT_AC
WHERE c.CAT_ECV = "Actif"
ORDER BY c.SLD_CTR DESC
LIMIT 8
'''

vue_sql = pd.read_sql(sql_jointure, conn)
print("Vue jointe via SQL :")
print(vue_sql.to_string(index=False))"""),

code("""# ── Requete d'agregation en SQL ──────────────────────────────
sql_agreg = '''
SELECT
    LIB_ECV                         AS statut,
    CAT_ECV                         AS categorie,
    COUNT(*)                        AS nb_contrats,
    ROUND(SUM(SLD_CTR), 2)          AS solde_total,
    ROUND(AVG(SLD_CTR), 2)          AS solde_moyen
FROM CTR
GROUP BY LIB_ECV, CAT_ECV
ORDER BY nb_contrats DESC
'''

stats_sql = pd.read_sql(sql_agreg, conn)
print("Statistiques par statut (SQL) :")
print(stats_sql.to_string(index=False))"""),

# ============================================================
# MINI-EXERCICE 7
# ============================================================
md("""---
### Mini-exercice 2.G — Requete SQL sur les transactions

**Contexte :** Votre manager veut une requete SQL qui donne,
pour chaque mois, le nombre de transactions et le nombre de comptes actifs.

**A faire :**
1. Ecrire une requete SQL sur la table `TXN`
   (colonnes disponibles : `IDT_AC`, `DAT_CRE_MVT_CPB`, `NUM_ORD_MVT_CPB`, etc.)
2. Grouper par mois (format YYYY-MM)
3. Calculer : nb transactions, nb comptes distincts
4. Trier par mois
5. Executer avec `pd.read_sql()` et afficher le resultat

**Hint :** En SQLite : `SUBSTR(date, 1, 7)` extrait les 7 premiers caracteres (YYYY-MM)"""),

code("""# ── Votre code ici ─────────────────────────────────────────
# Exercice 2.G

sql_mensuel = '''
SELECT
    SUBSTR(DAT_CRE_MVT_CPB, 1, 7)  AS mois,
    COUNT(*)                         AS nb_txn,
    COUNT(DISTINCT IDT_AC)           AS nb_comptes
FROM TXN
WHERE DAT_CRE_MVT_CPB IS NOT NULL
GROUP BY mois
ORDER BY mois
'''

resultat = pd.read_sql(sql_mensuel, conn)
print(resultat.to_string(index=False))"""),

md("""**Correction exercice 2.G :**"""),

code("""# ── CORRECTION exercice 2.G ─────────────────────────────────

sql_mensuel = '''
SELECT
    SUBSTR(DAT_CRE_MVT_CPB, 1, 7)  AS mois,
    COUNT(*)                         AS nb_txn,
    COUNT(DISTINCT IDT_AC)           AS nb_comptes,
    COUNT(DISTINCT NUM_FOL_XTR)      AS nb_folios
FROM TXN
WHERE DAT_CRE_MVT_CPB IS NOT NULL
  AND DAT_CRE_MVT_CPB != "."
GROUP BY mois
ORDER BY mois
'''

# Executer la requete SQL et recuperer dans un DataFrame
resultat_sql = pd.read_sql(sql_mensuel, conn)

# Affichage formate
print("Evolution mensuelle des transactions (SQL) :")
print()
print(f"{'Mois':>7}  {'Transactions':>13}  {'Comptes':>8}  {'Folios':>8}")
print("-" * 42)
for _, row in resultat_sql.iterrows():
    print(f"  {row['mois']:>5}  {row['nb_txn']:>13,}  {row['nb_comptes']:>8,}  {row['nb_folios']:>8,}")
print("-" * 42)
print(f"  TOTAL  {resultat_sql['nb_txn'].sum():>13,}")
print()
print(f"Mois avec le + de transactions : {resultat_sql.loc[resultat_sql['nb_txn'].idxmax(), 'mois']}")
print(f"Mois avec le - de transactions : {resultat_sql.loc[resultat_sql['nb_txn'].idxmin(), 'mois']}")"""),

# ============================================================
# EXERCICE FINAL DU JOUR 2
# ============================================================
md("""---
# Exercice final du Jour 2

## Synthese — Vue analytique complete et export

**Contexte :** Pour le rapport du comite de direction, votre manager veut
un fichier CSV unique qui joint toutes les informations disponibles.

**Ce fichier doit contenir :**
- Les infos du contrat (ref, statut, solde, devise)
- Les infos du client (type, langue, age, tranche age)
- La ville du client
- Le nombre de transactions de chaque contrat
- Le segment client base sur le solde

**Regles metier :**
- Segment `"Standard"` si SLD_CTR < 2 000 EUR
- Segment `"Confort"` si 2 000 ≤ SLD_CTR < 15 000 EUR
- Segment `"Premium"` si SLD_CTR ≥ 15 000 EUR
- Segment `"Inconnu"` si SLD_CTR manquant

**Livrable :** fichier `vue_analytique_complete.csv`"""),

code("""# ── Votre code ici ─────────────────────────────────────────
# Exercice final Jour 2

# 1. Construire la vue en jointures
# 2. Creer la colonne SEGMENT
# 3. Exporter
print("A completer !")"""),

md("""**Correction exercice final Jour 2 :**"""),

code("""# ── CORRECTION EXERCICE FINAL JOUR 2 ───────────────────────

import pandas as pd
import numpy as np
from pathlib import Path

DATA   = Path("../Orsys")
PARAMS = dict(sep=";", na_values=".", encoding="utf-8")

# ── Chargement propre ─────────────────────────────────────────
ctr       = pd.read_csv(DATA / "CTR.csv",       **PARAMS)
tie       = pd.read_csv(DATA / "TIE.csv",       **PARAMS)
tie_adr   = pd.read_csv(DATA / "TIE_ADR.csv",   **PARAMS)
tie_x_ctr = pd.read_csv(DATA / "TIE_X_CTR.csv", **PARAMS)
txn       = pd.read_csv(DATA / "TXN_X_CTR.csv", **PARAMS)

# ── Preparation CTR ───────────────────────────────────────────
MAPPING_ECV = {"1":"Ouvert","2":"En attente","3":"Suspendu",
               "4":"Cloture","5":"En resiliation","6":"Resilie"}
MAPPING_CAT = {"1":"Actif","2":"Actif","3":"Actif",
               "4":"Inactif","5":"Inactif","6":"Inactif"}

ctr["LIB_ECV"] = ctr["COD_ECV_CTR"].map(MAPPING_ECV).fillna("Inconnu")
ctr["CAT_ECV"] = ctr["COD_ECV_CTR"].map(MAPPING_CAT).fillna("Inconnu")

# Segment base sur le solde
ctr["SEGMENT"] = np.select(
    [ctr["SLD_CTR"].isna(),
     ctr["SLD_CTR"] < 2000,
     (ctr["SLD_CTR"] >= 2000) & (ctr["SLD_CTR"] < 15000),
     ctr["SLD_CTR"] >= 15000],
    ["Inconnu", "Standard", "Confort", "Premium"],
    default="Inconnu"
)

# ── Preparation TIE ───────────────────────────────────────────
tie["DAT_NAI_DT"] = pd.to_datetime(tie["DAT_NAI"], errors="coerce")
tie["AGE"] = ((pd.Timestamp.today() - tie["DAT_NAI_DT"]).dt.days / 365.25).round(0).astype("Int64")
tie["TRANCHE_AGE"] = pd.cut(
    tie["AGE"].astype(float),
    bins=[0, 25, 35, 50, 65, 120],
    labels=["<25 ans","25-34 ans","35-49 ans","50-64 ans","65+ ans"],
    right=False
).astype(str)

# ── Stats transactions ────────────────────────────────────────
txn["DAT_TXN_DT"] = pd.to_datetime(txn["DAT_CRE_MVT_CPB"], errors="coerce")
stats_txn = (
    txn
    .groupby("IDT_AC")
    .agg(
        nb_txn_total = ("NUM_ORD_MVT_CPB", "count"),
        premiere_txn = ("DAT_TXN_DT",       "min"),
        derniere_txn = ("DAT_TXN_DT",       "max"),
    )
    .reset_index()
)

# ── Jointures successives ─────────────────────────────────────
vue = (
    tie_x_ctr[["IDT_PI","IDT_AC","FLG_PRE_TTL"]]
    .merge(tie[["IDT_PI","COD_TYP_TIE","COD_LNG_CTR","COD_SEX","AGE","TRANCHE_AGE"]], on="IDT_PI", how="left")
    .merge(tie_adr[["IDT_PI","NOM_TIE","PRN","NOM_VIL","COD_PST","COD_PAY_ISO"]],     on="IDT_PI", how="left")
    .merge(ctr[["IDT_AC","REF_CTR_INN","DAT_OUV_CTR","LIB_ECV","CAT_ECV","COD_DEV","SLD_CTR","SEGMENT"]], on="IDT_AC", how="left")
    .merge(stats_txn, on="IDT_AC", how="left")
)

vue["nb_txn_total"] = vue["nb_txn_total"].fillna(0).astype(int)

# ── Export ────────────────────────────────────────────────────
# Convertir les colonnes de dates en texte pour l'export
for col in ["premiere_txn","derniere_txn"]:
    vue[col] = pd.to_datetime(vue[col]).dt.strftime("%Y-%m-%d")

vue.to_csv("vue_analytique_complete.csv", sep=";", index=False, encoding="utf-8")

print("=" * 55)
print("  VUE ANALYTIQUE COMPLETE EXPORTEE")
print("=" * 55)
print(f"  Fichier : vue_analytique_complete.csv")
print(f"  Lignes  : {len(vue):,}")
print(f"  Colonnes: {vue.shape[1]}")
print()
print("  Repartition par segment :")
for seg, nb in vue["SEGMENT"].value_counts().items():
    print(f"    {seg:<10} : {nb:>4} contrats ({nb/len(vue):.1%})")
print()
print("  Repartition par categorie :")
for cat, nb in vue["CAT_ECV"].value_counts().items():
    print(f"    {cat:<10} : {nb:>4} ({nb/len(vue):.1%})")
print("=" * 55)"""),

md("""---
# Synthese du Jour 2

## Ce que vous avez appris

| Action | SAS | Python Pandas |
|--------|-----|---------------|
| Charger un CSV | `proc import` | `pd.read_csv(sep=";", na_values=".")` |
| Voir les donnees | `proc print (obs=10)` | `df.head(10)` |
| Structure | `proc contents` | `df.info()` |
| Statistiques | `proc means` | `df.describe()` |
| Comptage | `proc freq` | `df["col"].value_counts()` |
| Filtrer | `where col = "1"` | `df[df["col"] == "1"]` |
| Trier | `proc sort by col` | `df.sort_values("col")` |
| Agreger | `proc summary by group` | `df.groupby("col").agg(...)` |
| Creer une colonne | Data step | `df["nouveau"] = expression` |
| Jointure | `proc sql left join` | `pd.merge(..., how="left")` |
| Exporter CSV | `proc export` | `df.to_csv(sep=";")` |
| Exporter JSON | (externe) | `df.to_json(orient="records")` |
| Requete SQL | `proc sql` | `pd.read_sql(sql, conn)` |

## Exercices realises
- **2.A** Explorer TIE.csv
- **2.B** Filtrer les contrats du rapport
- **2.C** Enrichir CTR avec colonnes calculees
- **2.D** Rapport mensuel de transactions
- **2.E** Jointure TIE + TIE_ADR + TIE_X_CTR
- **2.F** Exporter le rapport mensuel en CSV et JSON
- **2.G** Requete SQL sur les transactions
- **Final** Vue analytique complete (5 tables)

## Ce qui vous attend demain (Jour 3)

- SQL Vertica : CTEs, fonctions de fenetre (`OVER`, `PARTITION BY`, `LAG`)
- Dates : periodes glissantes sur 13 mois, `DATE_TRUNC`, `ADD_MONTHS`
- Pandas avance : nettoyage, pivot, fonctions sur texte
- Visualisation : bar chart, line chart, pie chart avec Matplotlib
- Mini-projet final : pipeline complet de bout en bout"""),

]  # fin j2

path = os.path.join(OUTPUT_DIR, "Jour2_Fichiers_Pandas.ipynb")
with open(path, "w", encoding="utf-8") as f:
    json.dump(notebook(j2), f, ensure_ascii=False, indent=1)
print(f"Jour 2 v2 cree : {os.path.getsize(path)//1024} Ko — {len(j2)} cellules")
