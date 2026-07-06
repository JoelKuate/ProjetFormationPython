"""Generateur Jour 2 - Fichiers Pandas et Flux · Formation Beobank"""
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

md("""# Jour 2 — Fichiers, Pandas et Flux de Donnees
## Formation Python Beobank · 19 novembre 2026

**Rappel du contexte :** Vous etes analyste chez Beobank. Votre mission est de produire
un rapport mensuel d'activite. Aujourd'hui vous allez charger les VRAIES tables Beobank
dans Python et commencer a les analyser.

### Objectifs du jour
- Lire et ecrire des fichiers CSV et JSON
- Charger les 5 tables Beobank dans Pandas
- Explorer, filtrer, trier, regrouper les donnees
- Creer des colonnes calculees et des aggreats
- Exporter les resultats
- Simuler le flux Pandas vers Vertica"""),

md("""---
## Recap Jour 1 — Ce que vous savez deja faire

Avant de commencer, voici un recap rapide des outils du Jour 1 que vous utiliserez aujourd'hui."""),

code("""# Recap des notions Jour 1 utiles aujourd'hui

# 1. Dictionnaire de mapping (codes → libelles)
STATUTS_ECV = {
    "1": ("Ouvert",    "Actif"),
    "4": ("Cloture",   "Inactif"),
    "6": ("Resilie",   "Inactif"),
}

# 2. Fonction avec docstring
def categoriser(cod_ecv):
    '''Retourne (libelle, categorie) pour un code etat contrat.'''
    return STATUTS_ECV.get(cod_ecv, ("Inconnu", "Inconnu"))

# 3. List comprehension
codes = ["6", "4", "1", "6", "4"]
libelles = [categoriser(c)[0] for c in codes]
print("Libelles :", libelles)

# 4. Lambda
en_euros = lambda x: f"{x:,.2f} EUR" if x is not None else "N/A"
print(en_euros(1250.75))
print("Jour 1 : OK !")"""),

# ----- SECTION 1 : Fichiers -----
md("""---
# Section 1 — Lire et ecrire des fichiers

## 1.1 Le gestionnaire de contexte with open()

En Python, on lit/ecrit les fichiers avec `open()` dans un bloc `with`.
Le `with` garantit que le fichier est ferme proprement meme si une erreur survient.

```python
# Ecrire
with open("fichier.txt", "w", encoding="utf-8") as f:
    f.write("contenu")

# Lire
with open("fichier.txt", "r", encoding="utf-8") as f:
    contenu = f.read()
```

**Modes d'ouverture :**

| Mode | Signification |
|------|--------------|
| `"r"` | Lecture (READ) — fichier doit exister |
| `"w"` | Ecriture (WRITE) — ecrase si existe |
| `"a"` | Ajout (APPEND) — ajoute a la fin |
| `"r+"` | Lecture ET ecriture |"""),

code("""# Ecrire un fichier de log (utile pour tracer les traitements)
import datetime

ligne_log = f"{datetime.datetime.now():%Y-%m-%d %H:%M} - Demarrage du traitement Beobank"

with open("traitement.log", "w", encoding="utf-8") as f:
    f.write(ligne_log + "\\n")
    f.write("Tables a charger : CTR, TIE, TIE_ADR, TIE_X_CTR, TXN_X_CTR\\n")
    f.write("Separateur : ;\\n")
    f.write("Valeur manquante : .\\n")

print("Fichier log ecrit.")

# Relire le fichier
with open("traitement.log", "r", encoding="utf-8") as f:
    contenu = f.read()

print("--- Contenu du log ---")
print(contenu)"""),

code("""# Lire ligne par ligne (utile pour les grands fichiers)
# On simule la lecture d'un fichier CSV a la main

with open("traitement.log", "r", encoding="utf-8") as f:
    for numero, ligne in enumerate(f, start=1):
        ligne_propre = ligne.rstrip("\\n")   # enlever le saut de ligne
        print(f"Ligne {numero}: {ligne_propre}")"""),

md("""## 1.2 pathlib — manipuler les chemins proprement

`pathlib` est la facon moderne de gerer les chemins de fichiers.
Elle fonctionne sur Windows (\\) et Linux/Mac (/) de facon transparente."""),

code("""from pathlib import Path

# Definir le dossier des donnees Beobank
DATA = Path("../Orsys")

# Verifier l'existence
print("Le dossier existe :", DATA.exists())

# Lister les fichiers CSV
print("\\nFichiers CSV disponibles :")
for fichier in sorted(DATA.glob("*.csv")):
    taille_ko = fichier.stat().st_size / 1024
    print(f"  {fichier.name:25s}  {taille_ko:6.1f} Ko")

# Construire un chemin (portable Windows/Linux)
chemin_ctr = DATA / "CTR.csv"
print(f"\\nChemin CTR : {chemin_ctr}")
print(f"Nom sans extension : {chemin_ctr.stem}")
print(f"Extension : {chemin_ctr.suffix}")"""),

md("""## 1.3 Lire un CSV avec le module csv (pour comprendre la mecanique)

Avant Pandas, voyons comment Python lit un CSV "a la main"."""),

code("""import csv
from pathlib import Path

# Lire les 5 premieres lignes de TIE.csv
chemin = Path("../Orsys/TIE.csv")

with open(chemin, encoding="utf-8", newline="") as f:
    lecteur = csv.DictReader(f, delimiter=";")   # separateur ; comme dans les fichiers Beobank
    lignes = list(lecteur)

print(f"Nombre de lignes : {len(lignes)}")
print(f"Colonnes ({len(lignes[0])}): {list(lignes[0].keys())}")
print()
print("3 premieres lignes :")
for ligne in lignes[:3]:
    print()
    for col, val in ligne.items():
        affichage = val if val and val != "." else "(manquant)"
        print(f"  {col:20s}: {affichage}")"""),

code("""# Ce qu'on voit : le CSV brut contient des "." pour les manquants
# et les nombres sont des chaines de caracteres
# C'est pourquoi on utilise Pandas : il gere tout ca automatiquement

import csv
from pathlib import Path

with open(Path("../Orsys/CTR.csv"), encoding="utf-8", newline="") as f:
    lecteur = csv.DictReader(f, delimiter=";")
    premiere = next(lecteur)

print("Extrait brut de CTR.csv :")
for col, val in premiere.items():
    type_python = type(val).__name__
    print(f"  {col:20s}: {repr(val):25s}  → type: {type_python}")

print()
print("Observation : TOUT est en str (chaine). SLD_CTR = '.' signifie manquant.")
print("Pandas convertira tout ca proprement avec na_values='.'")"""),

md("""## 1.4 JSON — lire et ecrire du JSON

JSON est un format d'echange tres courant (APIs, web services, NoSQL)."""),

code("""import json

# Creer des donnees (liste de clients)
clients_json = [
    {"IDT_PI": 655010249, "NOM": "JANSSENS", "PRENOM": "BART", "LANGUE": "FR"},
    {"IDT_PI": 655010248, "NOM": "VIRJXBF",  "PRENOM": "NTASEIJZR", "LANGUE": "FR"},
]

# Ecrire en JSON
with open("clients_sample.json", "w", encoding="utf-8") as f:
    json.dump(clients_json, f, ensure_ascii=False, indent=2)

print("JSON ecrit.")

# Relire le JSON
with open("clients_sample.json", encoding="utf-8") as f:
    clients_lus = json.load(f)

print(f"Nombre de clients lus : {len(clients_lus)}")
for c in clients_lus:
    print(f"  ID {c['IDT_PI']} : {c['PRENOM']} {c['NOM']} ({c['LANGUE']})")"""),

# ----- SECTION 2 : Introduction Pandas -----
md("""---
# Section 2 — Introduction a Pandas

Pandas est **la** bibliotheque Python pour l'analyse de donnees tabulaires.
C'est l'equivalent de SAS datasets + proc sort + proc means + proc freq, le tout dans un outil.

## 2.1 DataFrame vs Series

| Concept Pandas | Equivalent SAS | Description |
|---------------|----------------|-------------|
| `DataFrame` | Dataset | Tableau 2D : lignes et colonnes |
| `Series` | Vecteur / colonne | Une seule colonne |
| `Index` | Numero d'observation | L'identifiant de chaque ligne |
| `NaN` | `.` (manquant numerique) | Valeur manquante |

## 2.2 Charger les 5 tables Beobank

Les parametres importants pour nos fichiers :
- `sep=";"` : separateur point-virgule
- `na_values="."` : convertir le `.` SAS en NaN Python
- `encoding="utf-8"` : encodage du fichier"""),

code("""import pandas as pd
from pathlib import Path

# Chemin vers les donnees
DATA = Path("../Orsys")

# Parametres communs a tous nos fichiers Beobank
PARAMS = dict(sep=";", na_values=".", encoding="utf-8")

print("Chargement des 5 tables Beobank...")
ctr       = pd.read_csv(DATA / "CTR.csv",       **PARAMS)
tie       = pd.read_csv(DATA / "TIE.csv",       **PARAMS)
tie_adr   = pd.read_csv(DATA / "TIE_ADR.csv",   **PARAMS)
tie_x_ctr = pd.read_csv(DATA / "TIE_X_CTR.csv", **PARAMS)
txn       = pd.read_csv(DATA / "TXN_X_CTR.csv", **PARAMS)

print()
print(f"{'Table':25s}  {'Lignes':>7}  {'Colonnes':>9}  {'Taille memoire':>15}")
print("-" * 65)
for nom, df in [("CTR (Contrats)", ctr), ("TIE (Clients)", tie),
                ("TIE_ADR (Adresses)", tie_adr),
                ("TIE_X_CTR (Liens)", tie_x_ctr),
                ("TXN (Transactions)", txn)]:
    mem = df.memory_usage(deep=True).sum() / 1024
    print(f"  {nom:23s}  {df.shape[0]:>7,}  {df.shape[1]:>9}  {mem:>12.1f} Ko")

print()
print("Toutes les tables chargees !")"""),

# ----- Explorer un DataFrame -----
md("""## 2.3 Explorer un DataFrame : les commandes essentielles

Equivalent SAS : `proc print`, `proc contents`, `proc means`, `proc freq`"""),

code("""# Afficher les premieres lignes — equiv proc print (obs=5)
print("=== CTR — 5 premieres lignes ===")
ctr.head()"""),

code("""# Structure du DataFrame — equiv proc contents
print("=== Structure de CTR ===")
ctr.info()"""),

code("""# Les colonnes et leurs types
print("Colonnes de CTR :")
for col, dtype in ctr.dtypes.items():
    print(f"  {col:20s}  {str(dtype):10s}")"""),

code("""# Statistiques descriptives — equiv proc means
print("=== Statistiques de CTR ===")
ctr.describe()"""),

code("""# Valeurs manquantes — TRES important pour la qualite des donnees
print("=== Valeurs manquantes dans CTR ===")
manquants = ctr.isnull().sum()
pct       = (manquants / len(ctr) * 100).round(1)

resume = pd.DataFrame({
    "Colonne"    : manquants.index,
    "Manquants"  : manquants.values,
    "Pct (%)"    : pct.values
}).set_index("Colonne")
resume[resume["Manquants"] > 0]"""),

code("""# Frequences — equiv proc freq
print("=== COD_ECV_CTR — Etat du contrat ===")
print(ctr["COD_ECV_CTR"].value_counts(dropna=False).to_frame("Effectif"))
print()
print("=== COD_DEV — Devise ===")
print(ctr["COD_DEV"].value_counts(dropna=False).to_frame("Effectif"))"""),

code("""# Exploration de TIE (clients)
print("=== Table TIE — 5 premieres lignes ===")
tie.head(5)"""),

code("""print("=== Distribution des clients ===")
print()
print("-- Type de tiers --")
print(tie["COD_TYP_TIE"].value_counts().to_frame("Effectif"))
print()
print("-- Sexe --")
print(tie["COD_SEX"].value_counts(dropna=False).to_frame("Effectif"))
print()
print("-- Langue de communication --")
print(tie["COD_LNG_CTR"].value_counts(dropna=False).to_frame("Effectif"))"""),

code("""# Exploration de TXN (transactions)
print("=== Table TXN — 5 premieres lignes ===")
txn.head(5)"""),

code("""print("=== Distribution des transactions ===")
print()
print("-- Langue des operations --")
print(txn["COD_LNG_RIU"].value_counts(dropna=False).to_frame("Effectif"))
print()
print("-- Top 10 types d'operations --")
print(txn["LIB_OPE_INL_1"].value_counts(dropna=False).head(10).to_frame("Effectif"))"""),

# ----- Section 3 : Selection et filtrage -----
md("""---
# Section 3 — Selectionner et filtrer les donnees

## 3.1 Selectionner des colonnes"""),

code("""# Selectionner une colonne → Series (une seule colonne)
etats = ctr["COD_ECV_CTR"]
print(type(etats))    # <class 'pandas.core.series.Series'>
print(etats.head())

# Selectionner plusieurs colonnes → DataFrame
colonnes_cles = ["IDT_AC", "REF_CTR_INN", "DAT_OUV_CTR", "COD_ECV_CTR", "COD_DEV"]
ctr_reduit = ctr[colonnes_cles]
print()
print("DataFrame reduit :")
ctr_reduit.head()"""),

md("""## 3.2 loc et iloc — selectionner des lignes et colonnes

| Methode | Utilisation | Exemple |
|---------|-------------|---------|
| `loc[ligne, colonne]` | Par **etiquette** (nom) | `df.loc[0:3, "NOM"]` |
| `iloc[ligne, colonne]` | Par **position** (index numerique) | `df.iloc[0:3, 2]` |"""),

code("""# loc : selection par etiquette
# Lignes 0 a 4, colonnes par nom
extrait = ctr.loc[0:4, ["IDT_AC", "REF_CTR_INN", "DAT_OUV_CTR", "COD_ECV_CTR"]]
print("loc [0:4, colonnes_nommees] :")
print(extrait)

print()
# iloc : selection par position numerique
# Lignes 0 a 4, colonnes 0, 1, 3
extrait2 = ctr.iloc[0:5, [0, 1, 3]]
print("iloc [0:5, positions 0,1,3] :")
print(extrait2)"""),

md("""## 3.3 Filtrer les lignes avec des conditions"""),

code("""# Filtre simple : equiv where COD_ECV_CTR = '4'
clotures = ctr[ctr["COD_ECV_CTR"] == "4"]
print(f"Contrats clotures (code 4) : {len(clotures)}")

# Filtre simple : contrats ouverts
ouverts = ctr[ctr["COD_ECV_CTR"] == "1"]
print(f"Contrats ouverts (code 1)  : {len(ouverts)}")

# Filtre sur chaine : equiv contains
print()
print("Apercu des contrats clotures :")
clotures[["IDT_AC", "REF_CTR_INN", "DAT_OUV_CTR", "DAT_CLO_CTR"]].head()"""),

code("""# Filtres multiples avec & (ET) et | (OU)
# IMPORTANT : chaque condition doit etre entre parentheses !

# Contrats clotures OU resilies
inactifs = ctr[ctr["COD_ECV_CTR"].isin(["4", "5", "6"])]
print(f"Contrats inactifs (4/5/6) : {len(inactifs)}")

# Contrats actifs (1/2/3)
actifs = ctr[ctr["COD_ECV_CTR"].isin(["1", "2", "3"])]
print(f"Contrats actifs (1/2/3)   : {len(actifs)}")

# Distribution
print()
print("Distribution par categorie :")
print(f"  Actifs   : {len(actifs):>5} ({len(actifs)/len(ctr):.1%})")
print(f"  Inactifs : {len(inactifs):>5} ({len(inactifs)/len(ctr):.1%})")"""),

code("""# Filtrer les valeurs non nulles — equiv where COL ne .
ctr_avec_cloture = ctr[ctr["DAT_CLO_CTR"].notna()]
ctr_sans_cloture = ctr[ctr["DAT_CLO_CTR"].isna()]

print(f"Avec date de cloture   : {len(ctr_avec_cloture)}")
print(f"Sans date de cloture   : {len(ctr_sans_cloture)}")
print(f"Total                  : {len(ctr)}")"""),

code("""# Exercice de filtrage : personnes physiques de sexe M
pp_masculin = tie[
    (tie["COD_TYP_TIE"] == "1") &   # personne physique
    (tie["COD_SEX"] == "M")          # masculin
]
print(f"Hommes personnes physiques : {len(pp_masculin)}")

# Personnes physiques feminin
pp_feminin = tie[
    (tie["COD_TYP_TIE"] == "1") &
    (tie["COD_SEX"] == "F")
]
print(f"Femmes personnes physiques : {len(pp_feminin)}")

# Personnes morales
pm = tie[tie["COD_TYP_TIE"] == "2"]
print(f"Personnes morales          : {len(pm)}")"""),

# ----- Section 4 : Colonnes calculees -----
md("""---
# Section 4 — Creer des colonnes calculees

## 4.1 Colonnes de mapping

Equivalent SAS : `if COD_ECV_CTR = '1' then LIB_ECV = 'Ouvert';`
En Pandas, on utilise `.map()` avec un dictionnaire."""),

code("""# Ajouter des libelles lisibles aux codes

# Mapping code etat → libelle + categorie
MAPPING_ECV_LIB = {
    "1": "Ouvert",
    "2": "En attente",
    "3": "Suspendu",
    "4": "Cloture",
    "5": "En resiliation",
    "6": "Resilie",
}
MAPPING_ECV_CAT = {
    "1": "Actif", "2": "Actif", "3": "Actif",
    "4": "Inactif", "5": "Inactif", "6": "Inactif",
}

# Creer les colonnes
ctr["LIB_ECV"]   = ctr["COD_ECV_CTR"].map(MAPPING_ECV_LIB).fillna("Inconnu")
ctr["CAT_ECV"]   = ctr["COD_ECV_CTR"].map(MAPPING_ECV_CAT).fillna("Inconnu")

print("Verif mapping :")
ctr[["COD_ECV_CTR", "LIB_ECV", "CAT_ECV"]].drop_duplicates().sort_values("COD_ECV_CTR")"""),

code("""# Ajouter des libelles sur la table TIE
MAPPING_TYP = {"1": "Personne physique", "2": "Personne morale"}
MAPPING_STA = {"1": "Actif", "2": "Inactif", "3": "Prospect", "4": "Resilie"}
MAPPING_LNG = {"FR": "Francais", "NL": "Neerlandais", "DE": "Allemand"}

tie["LIB_TYP"] = tie["COD_TYP_TIE"].map(MAPPING_TYP).fillna("Autre")
tie["LIB_STA"] = tie["COD_STA_FED"].map(MAPPING_STA).fillna("Autre")
tie["LIB_LNG"] = tie["COD_LNG_CTR"].map(MAPPING_LNG).fillna(tie["COD_LNG_CTR"])

print("Distribution apres ajout des libelles :")
print(tie["LIB_TYP"].value_counts().to_string())"""),

md("""## 4.2 Colonnes avec calculs"""),

code("""import pandas as pd

# Convertir les dates (format YYYY-MM-DD → datetime)
ctr["DAT_OUV_CTR_DT"] = pd.to_datetime(ctr["DAT_OUV_CTR"], errors="coerce")
ctr["DAT_CLO_CTR_DT"] = pd.to_datetime(ctr["DAT_CLO_CTR"], errors="coerce")

# Extraire l'annee d'ouverture
ctr["ANNEE_OUV"] = ctr["DAT_OUV_CTR_DT"].dt.year

# Calculer la duree du contrat (en jours) pour les contrats clotures
ctr["DUREE_JOURS"] = (ctr["DAT_CLO_CTR_DT"] - ctr["DAT_OUV_CTR_DT"]).dt.days

print("Annee d'ouverture — distribution :")
print(ctr["ANNEE_OUV"].value_counts().sort_index().to_frame("Effectif"))
print()
clotures_duree = ctr[ctr["DUREE_JOURS"].notna()]
print(f"Contrats clotures avec duree calculee : {len(clotures_duree)}")
print(f"Duree moyenne  : {clotures_duree['DUREE_JOURS'].mean():.0f} jours")
print(f"Duree mediane  : {clotures_duree['DUREE_JOURS'].median():.0f} jours")"""),

code("""# Calculer l'age des clients dans TIE
tie["DAT_NAI_DT"] = pd.to_datetime(tie["DAT_NAI"], errors="coerce")
aujourd_hui       = pd.Timestamp.today()

tie["AGE"] = ((aujourd_hui - tie["DAT_NAI_DT"]).dt.days / 365.25).round(0).astype("Int64")

# Tranches d'age avec pd.cut()
tie["TRANCHE_AGE"] = pd.cut(
    tie["AGE"].astype(float),
    bins=[0, 25, 35, 50, 65, 120],
    labels=["Moins de 25 ans", "25-34 ans", "35-49 ans", "50-64 ans", "65 ans et plus"],
    right=False
)

print("Distribution par tranche d'age :")
print(tie["TRANCHE_AGE"].value_counts(dropna=False).sort_index().to_frame("Effectif"))"""),

md("""## 4.3 Colonnes conditionnelles avec numpy.where"""),

code("""import numpy as np

# np.where(condition, valeur_si_vrai, valeur_si_faux)
# Equivalent SAS : if condition then col = X; else col = Y;

# Marquer les contrats comme Actif / Inactif
ctr["IS_ACTIF"] = np.where(
    ctr["COD_ECV_CTR"].isin(["1", "2", "3"]),
    1,    # actif
    0     # inactif
)

print("Repartition Actif/Inactif :")
print(ctr["IS_ACTIF"].value_counts().to_frame("Effectif"))

# Avec plusieurs conditions (np.select)
conditions = [
    ctr["COD_ECV_CTR"].isin(["1", "2", "3"]),
    ctr["COD_ECV_CTR"].isin(["4"]),
    ctr["COD_ECV_CTR"].isin(["5", "6"]),
]
choix = ["Actif", "Cloture", "Resilie_ou_resiliation"]
ctr["SEGMENT"] = np.select(conditions, choix, default="Inconnu")

print()
print("Repartition par segment :")
print(ctr["SEGMENT"].value_counts().to_frame("Effectif"))"""),

# ----- Section 5 : Tri et GroupBy -----
md("""---
# Section 5 — Trier, regrouper et agreger

## 5.1 Trier — equiv proc sort"""),

code("""# Trier par une colonne (ascending=True par defaut)
ctr_trie = ctr.sort_values("DAT_OUV_CTR_DT", ascending=False)
print("Contrats du plus recent au plus ancien :")
ctr_trie[["REF_CTR_INN", "DAT_OUV_CTR", "COD_ECV_CTR", "LIB_ECV"]].head(8)"""),

code("""# Trier par plusieurs colonnes
tie_trie = tie.sort_values(
    by=["COD_TYP_TIE", "AGE"],
    ascending=[True, False]   # type ASC, age DESC
)
print("Clients tries par type puis par age decroissant :")
tie_trie[["IDT_PI", "COD_TYP_TIE", "LIB_TYP", "AGE", "COD_SEX"]].head(10)"""),

md("""## 5.2 GroupBy et agregations — equiv proc summary / proc means"""),

code("""# GroupBy simple : compter les contrats par etat
nb_par_etat = (
    ctr
    .groupby("LIB_ECV")
    .size()
    .reset_index(name="nb_contrats")
    .sort_values("nb_contrats", ascending=False)
)
print("Contrats par etat :")
print(nb_par_etat.to_string(index=False))"""),

code("""# GroupBy avec plusieurs agregations
# Transactions par compte

txn["DAT_CRE_MVT_CPB_DT"] = pd.to_datetime(txn["DAT_CRE_MVT_CPB"], errors="coerce")

resume_comptes = (
    txn
    .groupby("IDT_AC")
    .agg(
        nb_transactions  = ("NUM_ORD_MVT_CPB", "count"),
        nb_folios        = ("NUM_FOL_XTR", "nunique"),
        premiere_txn     = ("DAT_CRE_MVT_CPB_DT", "min"),
        derniere_txn     = ("DAT_CRE_MVT_CPB_DT", "max"),
    )
    .reset_index()
    .sort_values("nb_transactions", ascending=False)
)

print(f"Comptes avec transactions : {len(resume_comptes)}")
print()
print("Top 10 comptes les plus actifs :")
resume_comptes.head(10)"""),

code("""# GroupBy multi-niveaux : contrats par annee et par etat
contrats_par_annee_etat = (
    ctr
    .groupby(["ANNEE_OUV", "LIB_ECV"])
    .size()
    .reset_index(name="nb")
    .sort_values(["ANNEE_OUV", "nb"], ascending=[True, False])
)
print("Contrats par annee et par etat :")
print(contrats_par_annee_etat.to_string(index=False))"""),

code("""# transform() : calculer une valeur agregee SANS reduire le DataFrame
# Utile pour calculer le pourcentage par rapport au total de son groupe

# Nb total de transactions par compte (ramene a chaque ligne)
txn["total_txn_du_compte"] = txn.groupby("IDT_AC")["NUM_ORD_MVT_CPB"].transform("count")

# Rang chronologique de la transaction dans son compte (ROW_NUMBER en SQL)
txn_sorted = txn.sort_values(["IDT_AC", "DAT_CRE_MVT_CPB_DT"])
txn_sorted["rang_txn"] = txn_sorted.groupby("IDT_AC").cumcount() + 1

print("Apercu avec rang et total par compte :")
txn_sorted[["IDT_AC", "DAT_CRE_MVT_CPB_DT", "LIB_OPE_INL_1", "rang_txn", "total_txn_du_compte"]].head(12)"""),

# ----- Section 6 : Jointures -----
md("""---
# Section 6 — Jointures entre les tables

## 6.1 Types de jointures

| Type | Pandas | SAS | Comportement |
|------|--------|-----|--------------|
| Interne | `how="inner"` | `merge=... (in both)` | Seulement les lignes presentes dans les 2 tables |
| Gauche | `how="left"` | `(in left)` | Toutes les lignes de gauche + correspondances |
| Droite | `how="right"` | `(in right)` | Toutes les lignes de droite + correspondances |
| Totale | `how="outer"` | `(in union)` | Toutes les lignes des 2 tables |

## 6.2 Le schema des relations Beobank

```
TIE ──(IDT_PI)──> TIE_ADR
 |
 └──(IDT_PI)──> TIE_X_CTR ──(IDT_AC)──> CTR
                                             |
                                             └──(IDT_AC)──> TXN
```"""),

code("""# Jointure 1 : TIE + TIE_ADR (enrichir les clients avec leurs adresses)
# Equivalent SAS : proc sql; create table ... as select * from TIE t
#                  left join TIE_ADR a on t.IDT_PI = a.IDT_PI;

clients_enrichis = tie.merge(
    tie_adr[["IDT_PI", "NOM_TIE", "PRN", "NOM_VIL", "COD_PST", "ADR_EMA"]],
    on="IDT_PI",
    how="left"    # left join : garder tous les clients, meme sans adresse
)

print(f"TIE seul          : {len(tie)} lignes")
print(f"TIE + TIE_ADR     : {len(clients_enrichis)} lignes")
print()
clients_enrichis[["IDT_PI", "NOM_TIE", "PRN", "NOM_VIL", "COD_PST", "LIB_TYP"]].head(6)"""),

code("""# Jointure 2 : Clients → Contrats (via TIE_X_CTR)
clients_contrats = (
    clients_enrichis
    .merge(
        tie_x_ctr[["IDT_PI", "IDT_AC", "FLG_PRE_TTL", "COD_ROL_TTL"]],
        on="IDT_PI",
        how="left"
    )
    .merge(
        ctr[["IDT_AC", "REF_CTR_INN", "DAT_OUV_CTR", "LIB_ECV", "CAT_ECV", "COD_DEV"]],
        on="IDT_AC",
        how="left"
    )
)

print(f"Vue clients-contrats : {len(clients_contrats):,} lignes x {clients_contrats.shape[1]} colonnes")
colonnes_affich = ["NOM_TIE", "PRN", "REF_CTR_INN", "DAT_OUV_CTR", "LIB_ECV", "CAT_ECV"]
clients_contrats[colonnes_affich].head(8)"""),

code("""# Verifier la qualite de la jointure
# Combien de clients ont des contrats ?
clients_avec_contrats = clients_contrats[clients_contrats["IDT_AC"].notna()]["IDT_PI"].nunique()
clients_sans_contrats = clients_contrats[clients_contrats["IDT_AC"].isna()]["IDT_PI"].nunique()

print(f"Clients avec au moins 1 contrat : {clients_avec_contrats}")
print(f"Clients sans contrat            : {clients_sans_contrats}")

# Nombre de contrats par client
nb_ctr_par_client = (
    clients_contrats
    .groupby("IDT_PI")
    .agg(nb_contrats=("IDT_AC", "count"))
    .reset_index()
)
print()
print("Distribution du nb de contrats par client :")
print(nb_ctr_par_client["nb_contrats"].value_counts().sort_index().to_frame("Effectif"))"""),

# ----- Section 7 : Export -----
md("""---
# Section 7 — Exporter les resultats

## 7.1 Export CSV — equiv proc export"""),

code("""# Preparer un DataFrame propre a exporter
rapport_contrats = (
    clients_contrats[clients_contrats["IDT_AC"].notna()]
    [["IDT_PI", "NOM_TIE", "PRN", "NOM_VIL",
      "REF_CTR_INN", "DAT_OUV_CTR", "LIB_ECV", "CAT_ECV", "COD_DEV"]]
    .sort_values(["NOM_TIE", "DAT_OUV_CTR"])
)

# Export CSV
rapport_contrats.to_csv(
    "rapport_contrats.csv",
    sep=";",           # meme separateur que les sources
    index=False,       # ne pas exporter l'index numerique
    encoding="utf-8",
    date_format="%Y-%m-%d"
)

print(f"Export CSV : rapport_contrats.csv ({len(rapport_contrats):,} lignes)")

# Verifier en relisant
df_check = pd.read_csv("rapport_contrats.csv", sep=";", encoding="utf-8")
print(f"Verification lecture : {len(df_check):,} lignes - OK" if len(df_check) == len(rapport_contrats) else "ERREUR")"""),

md("""## 7.2 Export JSON"""),

code("""# Export JSON (utile pour les APIs ou les tableaux de bord web)
resume_clients = (
    tie[["IDT_PI", "LIB_TYP", "LIB_STA", "AGE", "TRANCHE_AGE", "COD_SEX", "COD_LNG_CTR"]]
    .head(10)
    .copy()
)

# Convertir les types non-serialisables (Int64, category → standard Python)
resume_clients["AGE"]          = resume_clients["AGE"].astype(object)
resume_clients["TRANCHE_AGE"]  = resume_clients["TRANCHE_AGE"].astype(str)

resume_clients.to_json(
    "resume_clients.json",
    orient="records",    # une liste de dicts
    indent=2,
    force_ascii=False
)

import json
with open("resume_clients.json", encoding="utf-8") as f:
    data = json.load(f)
print(f"JSON exporte : {len(data)} clients")
print("Exemple :", data[0])"""),

# ----- Section 8 : Vertica simulation -----
md("""---
# Section 8 — Flux Pandas vers Vertica

## 8.1 Architecture du flux

Dans votre environnement Beobank, le flux habituel est :

```
Fichier CSV/JSON
      |  pd.read_csv()
      v
  DataFrame Pandas
      |  to_sql() / vertica_python
      v
  Base Vertica (SIDU)
      |  pd.read_sql() / vertica_python
      v
  DataFrame Pandas
      |  to_csv() / to_json()
      v
  Rapport final
```

## 8.2 Connexion Vertica (schema a adapter avec votre USERID)

```python
# Avec vertica_python (driver officiel Vertica)
import vertica_python

conn_info = {
    'host'    : 'vertica-host.beobank.be',
    'port'    : 5433,
    'user'    : 'VOTRE_USERID',
    'password': 'VOTRE_PASSWORD',
    'database': 'beobank',
}

with vertica_python.connect(**conn_info) as conn:
    # Lire une table
    df = pd.read_sql("SELECT * FROM SIDU.CTR LIMIT 100", conn)

    # Ecrire un DataFrame
    df.to_sql("MA_TABLE", conn, schema="MON_SCHEMA",
              if_exists="replace", index=False)
```"""),

md("""## 8.3 Simulation avec SQLite (sans connexion Vertica requise)"""),

code("""import sqlite3

# Creer une base SQLite en memoire (simule Vertica)
conn = sqlite3.connect(":memory:")

# Injecter les DataFrames dans la base
ctr.to_sql("CTR",         conn, if_exists="replace", index=False)
tie.to_sql("TIE",         conn, if_exists="replace", index=False)
tie_adr.to_sql("TIE_ADR", conn, if_exists="replace", index=False)
txn.to_sql("TXN",         conn, if_exists="replace", index=False)

print("Tables injectees dans SQLite :")
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
for t in tables["name"]:
    nb = pd.read_sql(f"SELECT COUNT(*) as n FROM {t}", conn)["n"][0]
    print(f"  {t:15s} : {nb:,} lignes")"""),

code("""# Requete SQL : contrats par statut
sql_statuts = '''
SELECT
    COD_ECV_CTR,
    COUNT(*) AS nb_contrats,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct
FROM CTR
GROUP BY COD_ECV_CTR
ORDER BY nb_contrats DESC
'''

df_statuts = pd.read_sql(sql_statuts, conn)
print("Contrats par statut (avec pourcentage) :")
df_statuts"""),

code("""# Requete SQL : top 10 comptes par volume de transactions
sql_top = '''
SELECT
    t.IDT_AC,
    COUNT(*)          AS nb_txn,
    MIN(t.DAT_CRE_MVT_CPB) AS premiere_txn,
    MAX(t.DAT_CRE_MVT_CPB) AS derniere_txn
FROM TXN t
GROUP BY t.IDT_AC
ORDER BY nb_txn DESC
LIMIT 10
'''

df_top = pd.read_sql(sql_top, conn)
print("Top 10 comptes par transactions :")
df_top"""),

# ----- Exercices -----
md("""---
# Exercices du Jour 2

## Exercice 1 — Qualite de donnees sur CTR

**Contexte :** Avant de produire le rapport, votre responsable veut un bilan
de la qualite des donnees de la table CTR.

**Taches :**
1. Combien de contrats ont un solde (`SLD_CTR`) renseigne ?
2. Parmi les contrats "clotures" (code 4), combien ont une `DAT_CLO_CTR` renseignee ?
3. Y a-t-il des contrats avec `DAT_CLO_CTR` ANTERIEURE a `DAT_OUV_CTR` (anomalie) ?
4. Quelle est la plage des dates d'ouverture (min / max) ?"""),

code("""# ============================================================
# EXERCICE 1 — Qualite de donnees sur CTR
# ============================================================

import pandas as pd
from pathlib import Path

DATA = Path("../Orsys")
ctr = pd.read_csv(DATA / "CTR.csv", sep=";", na_values=".", encoding="utf-8")
ctr["DAT_OUV_DT"] = pd.to_datetime(ctr["DAT_OUV_CTR"], errors="coerce")
ctr["DAT_CLO_DT"] = pd.to_datetime(ctr["DAT_CLO_CTR"], errors="coerce")

# TACHE 1 : Contrats avec solde renseigne
avec_solde = ctr["SLD_CTR"].notna().sum()
print(f"1. Contrats avec SLD_CTR renseigne : {avec_solde} / {len(ctr)}")

# TACHE 2 : Clotures avec date de cloture
clotures = ctr[ctr["COD_ECV_CTR"] == "4"]
clotures_avec_date = clotures["DAT_CLO_CTR"].notna().sum()
print(f"2. Clotures (code 4) avec DAT_CLO  : {clotures_avec_date} / {len(clotures)}")

# TACHE 3 : Anomalie date cloture < date ouverture
anomalies = ctr[
    ctr["DAT_CLO_DT"].notna() &
    (ctr["DAT_CLO_DT"] < ctr["DAT_OUV_DT"])
]
print(f"3. Anomalies (cloture < ouverture) : {len(anomalies)}")
if len(anomalies) > 0:
    print(anomalies[["REF_CTR_INN", "DAT_OUV_CTR", "DAT_CLO_CTR"]].to_string())

# TACHE 4 : Plage des dates d'ouverture
print(f"4. Dates ouverture : {ctr['DAT_OUV_DT'].min().date()} → {ctr['DAT_OUV_DT'].max().date()}")"""),

md("""## Exercice 2 — Profil des clients pour le rapport

**Contexte :** La section "Profil des clients" du rapport doit inclure :
- Repartition par type (physique/morale)
- Repartition par sexe (pour les personnes physiques)
- Distribution par tranche d'age
- Repartition par langue

**Tache :** Produisez ce resume de profil en utilisant Pandas."""),

code("""# ============================================================
# EXERCICE 2 — Profil des clients
# ============================================================

import pandas as pd
from pathlib import Path

DATA = Path("../Orsys")
tie = pd.read_csv(DATA / "TIE.csv", sep=";", na_values=".", encoding="utf-8")

# --- Mappings ---
MAPPING_TYP = {"1": "Personne physique", "2": "Personne morale"}
MAPPING_STA = {"1": "Actif", "2": "Inactif", "3": "Prospect", "4": "Resilie"}
MAPPING_LNG = {"FR": "Francais", "NL": "Neerlandais"}
MAPPING_SEX = {"M": "Masculin", "F": "Feminin"}

tie["LIB_TYP"] = tie["COD_TYP_TIE"].map(MAPPING_TYP).fillna("Autre")
tie["LIB_STA"] = tie["COD_STA_FED"].map(MAPPING_STA).fillna("Autre")
tie["LIB_LNG"] = tie["COD_LNG_CTR"].map(MAPPING_LNG).fillna(tie["COD_LNG_CTR"])
tie["LIB_SEX"] = tie["COD_SEX"].map(MAPPING_SEX).fillna("Non renseigne")

# Age
tie["DAT_NAI_DT"] = pd.to_datetime(tie["DAT_NAI"], errors="coerce")
tie["AGE"] = ((pd.Timestamp.today() - tie["DAT_NAI_DT"]).dt.days / 365.25).round(0).astype("Int64")
tie["TRANCHE_AGE"] = pd.cut(
    tie["AGE"].astype(float),
    bins=[0, 25, 35, 50, 65, 120],
    labels=["Moins de 25 ans", "25-34 ans", "35-49 ans", "50-64 ans", "65 ans et plus"],
    right=False
)

# --- Affichage du profil ---
def print_freq(serie, titre):
    total = len(serie)
    counts = serie.value_counts(dropna=False)
    print(f"\n  [{titre}]")
    print(f"  {'Valeur':25s}  {'N':>5}  {'%':>6}")
    print(f"  {'-'*40}")
    for val, n in counts.items():
        print(f"  {str(val):25s}  {n:>5}  {n/total:>5.1%}")

print("=" * 45)
print("  PROFIL DES CLIENTS BEOBANK")
print("=" * 45)
print_freq(tie["LIB_TYP"],     "Type de tiers")
print_freq(tie["LIB_LNG"],     "Langue")
print_freq(tie["LIB_SEX"],     "Sexe")
print_freq(tie["TRANCHE_AGE"], "Tranche d'age")
print_freq(tie["LIB_STA"],     "Statut federal")"""),

md("""## Exercice 3 — Top 10 comptes actifs (pour le rapport)

**Contexte :** Votre rapport doit identifier les 10 comptes les plus actifs
sur les 13 derniers mois avec : nb de transactions, premier et dernier mouvement,
et le libelle de l'operation la plus frequente.

**Tache :** Produisez ce tableau en utilisant groupby et agg sur TXN_X_CTR."""),

code("""# ============================================================
# EXERCICE 3 — Top 10 comptes actifs
# ============================================================

import pandas as pd
from pathlib import Path
from pandas.tseries.offsets import DateOffset

DATA = Path("../Orsys")
txn = pd.read_csv(DATA / "TXN_X_CTR.csv", sep=";", na_values=".", encoding="utf-8")
txn["DAT_DT"] = pd.to_datetime(txn["DAT_CRE_MVT_CPB"], errors="coerce")

# Filtrer sur 13 mois glissants
aujourd_hui = pd.Timestamp.today().normalize()
debut_13m   = aujourd_hui - DateOffset(months=13)
txn_13m = txn[txn["DAT_DT"] >= debut_13m].copy()

print(f"Transactions sur 13 mois : {len(txn_13m):,} / {len(txn):,} au total")
print(f"Periode : {debut_13m.date()} → {aujourd_hui.date()}")
print()

# Fonction pour trouver la valeur la plus frequente (mode)
def mode_str(serie):
    vals = serie.dropna()
    if len(vals) == 0:
        return ""
    return vals.value_counts().index[0]

# Agreger par compte
top10 = (
    txn_13m
    .groupby("IDT_AC")
    .agg(
        nb_txn      = ("NUM_ORD_MVT_CPB", "count"),
        premiere    = ("DAT_DT", "min"),
        derniere    = ("DAT_DT", "max"),
        op_freq     = ("LIB_OPE_INL_1", mode_str),
    )
    .reset_index()
    .sort_values("nb_txn", ascending=False)
    .head(10)
)

top10["premiere"] = top10["premiere"].dt.date
top10["derniere"] = top10["derniere"].dt.date
top10["op_freq"]  = top10["op_freq"].str[:30]   # tronquer si trop long

print("TOP 10 comptes actifs (13 mois glissants) :")
print(top10.to_string(index=False))"""),

md("""## Exercice 4 — Pipeline complet : charge → enrichi → exporte

**Contexte :** Preparez le dataset principal du rapport : une vue client-contrat
avec toutes les informations enrichies, filtree sur les contrats actifs.

**Tache :** Construisez ce pipeline en chaine (`df.merge().assign().query()...`)."""),

code("""# ============================================================
# EXERCICE 4 — Pipeline complet
# ============================================================

import pandas as pd
import numpy as np
from pathlib import Path

DATA = Path("../Orsys")
PARAMS = dict(sep=";", na_values=".", encoding="utf-8")

# Charger
ctr       = pd.read_csv(DATA / "CTR.csv",       **PARAMS)
tie       = pd.read_csv(DATA / "TIE.csv",       **PARAMS)
tie_adr   = pd.read_csv(DATA / "TIE_ADR.csv",   **PARAMS)
tie_x_ctr = pd.read_csv(DATA / "TIE_X_CTR.csv", **PARAMS)

# Pipeline avec method chaining
vue_rapport = (
    # 1. Commencer par les liens client-contrat
    tie_x_ctr[["IDT_PI", "IDT_AC", "FLG_PRE_TTL"]]

    # 2. Jointure avec les clients
    .merge(
        tie[["IDT_PI", "COD_TYP_TIE", "COD_STA_FED", "DAT_NAI", "COD_LNG_CTR", "COD_SEX"]],
        on="IDT_PI", how="left"
    )

    # 3. Jointure avec les adresses
    .merge(
        tie_adr[["IDT_PI", "NOM_TIE", "PRN", "NOM_VIL", "COD_PST", "COD_PAY_ISO"]],
        on="IDT_PI", how="left"
    )

    # 4. Jointure avec les contrats
    .merge(
        ctr[["IDT_AC", "REF_CTR_INN", "DAT_OUV_CTR", "DAT_CLO_CTR", "COD_ECV_CTR", "COD_DEV"]],
        on="IDT_AC", how="left"
    )

    # 5. Colonnes calculees
    .assign(
        NOM_COMPLET  = lambda df: (
            df["PRN"].fillna("").str.strip().str.title() + " " +
            df["NOM_TIE"].fillna("").str.strip().str.title()
        ).str.strip(),
        LIB_ECV = lambda df: df["COD_ECV_CTR"].map({
            "1":"Ouvert","2":"En attente","3":"Suspendu",
            "4":"Cloture","5":"En resiliation","6":"Resilie"
        }).fillna("Inconnu"),
        CAT_ECV = lambda df: np.where(
            df["COD_ECV_CTR"].isin(["1","2","3"]), "Actif", "Inactif"
        ),
        DAT_OUV_DT = lambda df: pd.to_datetime(df["DAT_OUV_CTR"], errors="coerce"),
        ANNEE_OUV  = lambda df: pd.to_datetime(df["DAT_OUV_CTR"], errors="coerce").dt.year,
    )
)

print(f"Vue rapport : {len(vue_rapport):,} lignes x {vue_rapport.shape[1]} colonnes")
print()
print("Repartition par categorie de contrat :")
print(vue_rapport["CAT_ECV"].value_counts().to_frame("Effectif"))
print()

# Exporter
vue_rapport.to_csv("vue_rapport_jour2.csv", sep=";", index=False, encoding="utf-8")
print("Exporte : vue_rapport_jour2.csv")

# Apercu
cols_affich = ["NOM_COMPLET", "REF_CTR_INN", "DAT_OUV_CTR", "LIB_ECV", "CAT_ECV", "NOM_VIL"]
vue_rapport[cols_affich].head(8)"""),

md("""---
# Resume du Jour 2

Vous avez charge et manipule les **vraies tables Beobank** !

| Ce que vous savez faire | Equivalent SAS |
|-------------------------|----------------|
| `pd.read_csv(sep=";", na_values=".")` | `proc import; infile dlm=';'` |
| `df.head()` / `df.info()` | `proc print (obs=5)` / `proc contents` |
| `df.describe()` | `proc means` |
| `df['col'].value_counts()` | `proc freq` |
| `df[df['col'] == val]` | `where col = val;` |
| `df['col'].isin([...])` | `if col in ('x','y')` |
| `df['col'].notna()` | `where col ne .` |
| `df.groupby().agg()` | `proc summary` |
| `df.merge(..., how='left')` | `proc sql left join` |
| `df.to_csv()` | `proc export` |

**Demain (Jour 3) :** Vertica SQL avancé (CTEs, OVER, LAG), dates et périodes glissantes,
visualisations Matplotlib, et mini-projet de bout en bout !"""),

] # fin j2

path = os.path.join(OUTPUT_DIR, "Jour2_Fichiers_Pandas.ipynb")
with open(path, "w", encoding="utf-8") as f:
    json.dump(notebook(j2), f, ensure_ascii=False, indent=1)
print(f"Jour 2 cree : {os.path.getsize(path)//1024} Ko — {len(j2)} cellules")
