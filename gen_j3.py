"""Generateur Jour 3 - SQL Vertica, Time Series, Visualisation · Formation Beobank"""
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

j3 = [

md("""# Jour 3 - Vertica SQL, Time Series, Pandas Avance et Visualisation
## Formation Python Beobank - 20 novembre 2026

**Rappel du contexte :**
Vous etes analyste chez Beobank. Apres 2 jours de preparation, vous avez :
- Les bases Python (Jour 1)
- Les 5 tables chargees et nettoyees dans Pandas (Jour 2)

Aujourd'hui vous finalisez le **rapport mensuel d'activite** :
- Requetes SQL analytiques (CTEs, fonctions de fenetre)
- Calculs sur les dates et les periodes glissantes
- Visualisations Matplotlib pour le comite de direction
- Mini-projet : pipeline complet de bout en bout

### Objectifs du jour
- Maitriser les CTEs et fonctions analytiques Vertica (OVER, PARTITION BY, LAG, LEAD)
- Convertir et calculer sur les dates (formats SAS et ISO)
- Creer des periodes glissantes et des agregations temporelles
- Produire des graphiques propres et exportables
- Assembler le rapport final complet"""),

# ----- SETUP -----
md("""---
## Cellule de setup - a executer EN PREMIER

Cette cellule charge les 5 tables et prepare les variables que vous utiliserez toute la journee."""),

code("""import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path
from pandas.tseries.offsets import DateOffset

# Configuration
DATA = Path("../Orsys")
PARAMS = dict(sep=";", na_values=".", encoding="utf-8")

plt.rcParams.update({
    "figure.dpi"     : 110,
    "font.size"      : 10,
    "axes.titlesize" : 12,
    "axes.titleweight": "bold",
    "axes.spines.top" : False,
    "axes.spines.right": False,
})

# Chargement des 5 tables
print("Chargement des tables...")
ctr       = pd.read_csv(DATA / "CTR.csv",       **PARAMS)
tie       = pd.read_csv(DATA / "TIE.csv",       **PARAMS)
tie_adr   = pd.read_csv(DATA / "TIE_ADR.csv",   **PARAMS)
tie_x_ctr = pd.read_csv(DATA / "TIE_X_CTR.csv", **PARAMS)
txn       = pd.read_csv(DATA / "TXN_X_CTR.csv", **PARAMS)

# Conversions de dates
ctr["DAT_OUV_DT"]    = pd.to_datetime(ctr["DAT_OUV_CTR"], errors="coerce")
ctr["DAT_CLO_DT"]    = pd.to_datetime(ctr["DAT_CLO_CTR"], errors="coerce")
txn["DAT_TXN_DT"]    = pd.to_datetime(txn["DAT_CRE_MVT_CPB"], errors="coerce")
tie["DAT_NAI_DT"]    = pd.to_datetime(tie["DAT_NAI"], errors="coerce")

# Mappings
MAPPING_ECV_LIB = {"1":"Ouvert","2":"En attente","3":"Suspendu",
                   "4":"Cloture","5":"En resiliation","6":"Resilie"}
MAPPING_ECV_CAT = {"1":"Actif","2":"Actif","3":"Actif",
                   "4":"Inactif","5":"Inactif","6":"Inactif"}
ctr["LIB_ECV"] = ctr["COD_ECV_CTR"].map(MAPPING_ECV_LIB).fillna("Inconnu")
ctr["CAT_ECV"] = ctr["COD_ECV_CTR"].map(MAPPING_ECV_CAT).fillna("Inconnu")

# Enrichissement TIE
tie["AGE"] = ((pd.Timestamp.today() - tie["DAT_NAI_DT"]).dt.days / 365.25).round(0).astype("Int64")
tie["TRANCHE_AGE"] = pd.cut(
    tie["AGE"].astype(float),
    bins=[0, 25, 35, 50, 65, 120],
    labels=["<25 ans", "25-34 ans", "35-49 ans", "50-64 ans", "65+ ans"],
    right=False
)

# Base SQLite pour la simulation Vertica
conn = sqlite3.connect(":memory:")
ctr.to_sql("CTR",         conn, if_exists="replace", index=False)
tie.to_sql("TIE",         conn, if_exists="replace", index=False)
tie_adr.to_sql("TIE_ADR", conn, if_exists="replace", index=False)
tie_x_ctr.to_sql("TIE_X_CTR", conn, if_exists="replace", index=False)
txn.to_sql("TXN",         conn, if_exists="replace", index=False)

print()
for nom, df in [("ctr",ctr),("tie",tie),("tie_adr",tie_adr),("tie_x_ctr",tie_x_ctr),("txn",txn)]:
    print(f"  {nom:12s}: {df.shape[0]:>5} lignes x {df.shape[1]} colonnes")
print()
print("Setup termine. Bonne journee !")"""),

# ================================================================
# SECTION 1 : VERTICA SQL
# ================================================================
md("""---
# Section 1 - Vertica SQL pour analystes data

## 1.1 Pourquoi ecrire du SQL depuis Python ?

En SAS, vous utilisez `proc sql`. En Python, le flux est le meme :
1. Vous ecrivez votre requete SQL dans une variable Python (chaine de caracteres)
2. Vous l'envoyez a Vertica (ou SQLite ici) avec `pd.read_sql()`
3. Le resultat arrive directement dans un DataFrame

L'avantage : vous combinez la puissance de SQL (analytiques, CTEs, fenetres)
avec la flexibilite de Python (boucles, visualisations, exports).

```
Requete SQL (str Python)
         |  pd.read_sql(sql, conn)
         v
    DataFrame Pandas
         |  .plot() / .to_csv() / ...
         v
    Graphique / Fichier
```"""),

md("""## 1.2 CTEs - Common Table Expressions

Un CTE decompose une requete complexe en etapes nommees et lisibles.
Equivalent SAS : enchaener plusieurs `proc sql create table` intermediaires.

**Syntaxe Vertica :**
```sql
WITH
    cte_1 AS (SELECT ... FROM table1 WHERE ...),
    cte_2 AS (SELECT ... FROM cte_1 JOIN table2 ON ...)
SELECT * FROM cte_2;
```"""),

code("""# CTE 1 : contrats actifs avec leur nombre de transactions
sql_cte1 = '''
WITH
    actifs AS (
        SELECT IDT_AC, REF_CTR_INN, DAT_OUV_CTR, COD_ECV_CTR
        FROM CTR
        WHERE COD_ECV_CTR IN ("1", "2", "3")
    ),
    volumes AS (
        SELECT IDT_AC, COUNT(*) AS nb_txn
        FROM TXN
        GROUP BY IDT_AC
    )
SELECT
    a.IDT_AC,
    a.REF_CTR_INN,
    a.DAT_OUV_CTR,
    a.COD_ECV_CTR,
    COALESCE(v.nb_txn, 0) AS nb_txn
FROM actifs a
LEFT JOIN volumes v ON a.IDT_AC = v.IDT_AC
ORDER BY nb_txn DESC
LIMIT 10
'''

df_cte1 = pd.read_sql(sql_cte1, conn)
print("Top 10 contrats actifs par volume de transactions :")
print(df_cte1.to_string(index=False))"""),

code("""# CTE 2 : profil complet client-contrat (simulation vue SIDU)
sql_cte2 = '''
WITH
    clients AS (
        SELECT t.IDT_PI, t.COD_TYP_TIE, t.COD_LNG_CTR, t.COD_SEX,
               a.NOM_TIE, a.PRN, a.NOM_VIL
        FROM TIE t
        LEFT JOIN TIE_ADR a ON t.IDT_PI = a.IDT_PI
    ),
    contrats AS (
        SELECT lk.IDT_PI, lk.IDT_AC, lk.FLG_PRE_TTL,
               c.REF_CTR_INN, c.DAT_OUV_CTR, c.COD_ECV_CTR
        FROM TIE_X_CTR lk
        JOIN CTR c ON lk.IDT_AC = c.IDT_AC
    )
SELECT
    cl.NOM_TIE, cl.PRN,
    cl.COD_TYP_TIE, cl.COD_LNG_CTR,
    ct.REF_CTR_INN, ct.DAT_OUV_CTR, ct.COD_ECV_CTR,
    ct.FLG_PRE_TTL
FROM clients cl
JOIN contrats ct ON cl.IDT_PI = ct.IDT_PI
LIMIT 10
'''

df_cte2 = pd.read_sql(sql_cte2, conn)
print(f"Vue client-contrat : {len(df_cte2)} lignes")
df_cte2"""),

md("""## 1.3 Fonctions analytiques : OVER / PARTITION BY

Les fonctions analytiques calculent une valeur **pour chaque ligne**
en tenant compte d'un groupe (PARTITION BY) et/ou d'un ordre (ORDER BY).

| Fonction | Description | Equivalent Pandas |
|----------|-------------|-------------------|
| `COUNT(*) OVER (PARTITION BY col)` | Total du groupe pour chaque ligne | `.transform('count')` |
| `SUM(val) OVER (PARTITION BY col)` | Somme du groupe pour chaque ligne | `.transform('sum')` |
| `ROW_NUMBER() OVER (ORDER BY ...)` | Rang 1,2,3... dans le groupe | `.cumcount() + 1` |
| `RANK() OVER (ORDER BY ...)` | Rang avec ex-aequo | `.rank(method='min')` |
| `LAG(col, 1) OVER (ORDER BY ...)` | Valeur de la ligne precedente | `.shift(1)` |
| `LEAD(col, 1) OVER (ORDER BY ...)` | Valeur de la ligne suivante | `.shift(-1)` |"""),

code("""# OVER + PARTITION BY : total par groupe ramene a chaque ligne
sql_over = '''
SELECT
    IDT_AC,
    DAT_CRE_MVT_CPB,
    LIB_OPE_INL_1,
    COUNT(*) OVER (PARTITION BY IDT_AC)         AS total_txn_compte,
    COUNT(*) OVER ()                             AS total_txn_global,
    ROW_NUMBER() OVER (
        PARTITION BY IDT_AC
        ORDER BY DAT_CRE_MVT_CPB
    )                                            AS rang_chronologique
FROM TXN
ORDER BY IDT_AC, DAT_CRE_MVT_CPB
LIMIT 20
'''

df_over = pd.read_sql(sql_over, conn)
print("Fonctions OVER - 20 premieres lignes :")
df_over"""),

code("""# Meme resultat en Pandas (plus pratique pour les traitements suivants)
txn_sorted = txn.sort_values(["IDT_AC", "DAT_TXN_DT"]).copy()

# COUNT OVER PARTITION BY IDT_AC
txn_sorted["total_txn_compte"] = txn_sorted.groupby("IDT_AC")["NUM_ORD_MVT_CPB"].transform("count")

# ROW_NUMBER OVER (PARTITION BY IDT_AC ORDER BY date)
txn_sorted["rang_chrono"] = txn_sorted.groupby("IDT_AC").cumcount() + 1

# Pourcentage de la contribution de chaque transaction dans son compte
txn_sorted["pct_dans_compte"] = (1 / txn_sorted["total_txn_compte"] * 100).round(1)

colonnes = ["IDT_AC", "DAT_TXN_DT", "total_txn_compte", "rang_chrono", "pct_dans_compte"]
txn_sorted[colonnes].head(15)"""),

md("""## 1.4 LAG et LEAD - naviguer dans le temps

`LAG(col, N)` : valeur de N lignes AVANT dans l'ordre
`LEAD(col, N)` : valeur de N lignes APRES dans l'ordre

**Cas d'usage bancaire :** comparer la transaction courante avec la precedente
pour detecter les ruptures ou calculer les ecarts temporels.

**Vertica SQL :**
```sql
SELECT
    IDT_AC,
    DAT_CRE_MVT_CPB,
    LAG(DAT_CRE_MVT_CPB, 1) OVER (
        PARTITION BY IDT_AC
        ORDER BY DAT_CRE_MVT_CPB
    ) AS date_txn_prec
FROM SIDU.TXN_X_CTR;
```"""),

code("""# LAG avec Pandas : shift(1) dans le groupe
txn_lag = txn.sort_values(["IDT_AC", "DAT_TXN_DT"]).copy()

# LAG(1) : date de la transaction precedente du meme compte
txn_lag["date_prec"] = txn_lag.groupby("IDT_AC")["DAT_TXN_DT"].shift(1)

# LEAD(1) : date de la prochaine transaction du meme compte
txn_lag["date_suiv"] = txn_lag.groupby("IDT_AC")["DAT_TXN_DT"].shift(-1)

# Ecart en jours entre deux transactions consecutives
txn_lag["ecart_jours"] = (txn_lag["DAT_TXN_DT"] - txn_lag["date_prec"]).dt.days

print("Statistiques sur l'ecart inter-transactions (jours) :")
ecarts = txn_lag["ecart_jours"].dropna()
print(f"  Moyenne  : {ecarts.mean():.1f} jours")
print(f"  Mediane  : {ecarts.median():.1f} jours")
print(f"  Min      : {ecarts.min():.0f} jours")
print(f"  Max      : {ecarts.max():.0f} jours")
print()

cols = ["IDT_AC", "DAT_TXN_DT", "date_prec", "date_suiv", "ecart_jours"]
txn_lag[cols].dropna(subset=["date_prec"]).head(10)"""),

code("""# LEAD : identifier la prochaine operation pour chaque compte
# Utile pour les analyses de sequences (ex: apres un rejet, que se passe-t-il ?)

txn_lag["op_suivante"] = txn_lag.groupby("IDT_AC")["LIB_OPE_INL_1"].shift(-1)

# Trouver les transactions suivies d'une domiciliation
avec_domiciliation_suiv = txn_lag[
    txn_lag["op_suivante"].fillna("").str.contains("Domicili", case=False, na=False)
]
print(f"Transactions suivies d'une domiciliation : {len(avec_domiciliation_suiv)}")
if len(avec_domiciliation_suiv) > 0:
    cols2 = ["IDT_AC", "DAT_TXN_DT", "LIB_OPE_INL_1", "op_suivante"]
    print(avec_domiciliation_suiv[cols2].head(5).to_string(index=False))"""),

md("""## 1.5 Fonctions de dates Vertica

| Vertica | Python Pandas | Description |
|---------|--------------|-------------|
| `ADD_MONTHS(date, n)` | `date + DateOffset(months=n)` | Ajouter N mois |
| `DATE_TRUNC('month', date)` | `date.dt.to_period('M').dt.to_timestamp()` | Premier jour du mois |
| `DATEDIFF('day', d1, d2)` | `(d2 - d1).dt.days` | Ecart en jours |
| `YEAR(date)` | `date.dt.year` | Extraire l'annee |
| `MONTH(date)` | `date.dt.month` | Extraire le mois |
| `LAST_DAY(date)` | `date + pd.offsets.MonthEnd(0)` | Dernier jour du mois |"""),

code("""# Demonstration de toutes les fonctions de dates
from pandas.tseries.offsets import DateOffset
import pandas as pd

dates_test = pd.to_datetime(["2024-05-29", "2024-08-07", "2022-01-12", "2025-01-07"])

df_dates = pd.DataFrame({"date_originale": dates_test})

df_dates["annee"]             = df_dates["date_originale"].dt.year
df_dates["mois"]              = df_dates["date_originale"].dt.month
df_dates["jour"]              = df_dates["date_originale"].dt.day
df_dates["premier_jour_mois"] = df_dates["date_originale"].dt.to_period("M").dt.to_timestamp()
df_dates["dernier_jour_mois"] = df_dates["date_originale"] + pd.offsets.MonthEnd(0)
df_dates["plus_1_mois"]       = df_dates["date_originale"] + DateOffset(months=1)
df_dates["plus_13_mois"]      = df_dates["date_originale"] + DateOffset(months=13)
df_dates["nom_mois"]          = df_dates["date_originale"].dt.strftime("%B %Y")

df_dates"""),

# ================================================================
# SECTION 2 : TIME SERIES ET PERIODES GLISSANTES
# ================================================================
md("""---
# Section 2 - Gestion des dates et Time Series

## 2.1 Les deux formats de dates dans nos fichiers Beobank

Nos 5 tables utilisent **deux formats de dates differents** :

| Table | Colonne | Format | Exemple |
|-------|---------|--------|---------|
| CTR | DAT_OUV_CTR | `YYYY-MM-DD` (ISO) | `2024-05-29` |
| TIE | DAT_NAI | `YYYY-MM-DD` (ISO) | `1980-01-25` |
| TXN | DAT_CRE_MVT_CPB | `YYYY-MM-DD` (ISO) | `2026-05-08` |
| TIE_ADR | DAT_MAJ_ADR | **SAS** `DDMONYYYY` | `24NOV2025` |

Le format SAS `DDMONYYYY` est l'export natif SAS et necessite un traitement specifique."""),

code("""# Charger TIE_ADR et voir le format de date brut
tie_adr_raw = pd.read_csv(DATA / "TIE_ADR.csv", sep=";", na_values=".", encoding="utf-8")
print("Format brut de DAT_MAJ_ADR :")
print(tie_adr_raw["DAT_MAJ_ADR"].dropna().head(10).to_string())"""),

code("""# Parser le format SAS DDMONYYYY (ex: 24NOV2025)
# Pandas comprend directement ce format avec format='%d%b%Y'
# MAIS les mois sont en anglais (JAN, FEB, MAR...) meme dans les exports SAS francophones

# Tester directement
test_dates = ["24NOV2025", "09JAN2026", "25NOV2025"]
parsed = pd.to_datetime(test_dates, format="%d%b%Y")
print("Dates parsees depuis format SAS :")
for brut, parsed_date in zip(test_dates, parsed):
    print(f"  {brut} → {parsed_date.date()}")

print()

# Appliquer sur la vraie colonne
tie_adr["DAT_MAJ_ADR_DT"] = pd.to_datetime(
    tie_adr_raw["DAT_MAJ_ADR"],
    format="%d%b%Y",
    errors="coerce"   # mettre NaT si le format ne correspond pas
)

print("Verification :")
visu = pd.DataFrame({
    "brut"   : tie_adr_raw["DAT_MAJ_ADR"].head(6).values,
    "converti": tie_adr["DAT_MAJ_ADR_DT"].head(6).dt.date.values
})
print(visu.to_string(index=False))"""),

md("""## 2.2 Calculs sur les dates"""),

code("""# DATEDIFF : calculer la duree d'un contrat
ctr["DUREE_JOURS"] = (ctr["DAT_CLO_DT"] - ctr["DAT_OUV_DT"]).dt.days
ctr["DUREE_MOIS"]  = ((ctr["DAT_CLO_DT"] - ctr["DAT_OUV_DT"]).dt.days / 30.44).round(1)
ctr["DUREE_ANS"]   = (ctr["DUREE_JOURS"] / 365.25).round(2)

clotures = ctr[ctr["DUREE_JOURS"].notna()].copy()
print(f"Contrats clotures avec duree calculee : {len(clotures)}")
print()
print("Statistiques sur la duree des contrats :")
stats = clotures["DUREE_JOURS"].describe().round(1)
print(f"  Minimum   : {stats['min']:.0f} jours")
print(f"  Moyenne   : {stats['mean']:.0f} jours ({stats['mean']/365.25:.1f} ans)")
print(f"  Mediane   : {stats['50%']:.0f} jours")
print(f"  Maximum   : {stats['max']:.0f} jours ({stats['max']/365.25:.1f} ans)")
print()
clotures[["REF_CTR_INN","DAT_OUV_CTR","DAT_CLO_CTR","DUREE_JOURS","DUREE_MOIS"]].head(8)"""),

code("""# ADD_MONTHS : generer une serie de dates (12 mois a partir d'une date)
from pandas.tseries.offsets import DateOffset

date_debut = pd.Timestamp("2026-01-01")
print("Serie de 13 mois a partir de janvier 2026 :")
print()
print(f"{'Mois':>4}  {'Date debut':12}  {'Date fin':12}  {'Label'}")
print("-" * 50)
for i in range(13):
    d = date_debut + DateOffset(months=i)
    fin = d + DateOffset(months=1) - pd.Timedelta(days=1)
    print(f"  {i+1:>2}  {d.strftime('%Y-%m-%d'):12}  {fin.strftime('%Y-%m-%d'):12}  {d.strftime('%B %Y')}")"""),

md("""## 2.3 Periode glissante sur 13 mois

En analyse bancaire, on travaille souvent sur une **fenetre glissante de 13 mois**
(N-12 au mois courant) pour avoir une vision annuelle complete avec le mois courant."""),

code("""# Calculer la fenetre 13 mois glissants
aujourd_hui = pd.Timestamp.today().normalize()
debut_13m   = aujourd_hui - DateOffset(months=13)

print(f"Date du jour    : {aujourd_hui.date()}")
print(f"Debut 13 mois   : {debut_13m.date()}")
print(f"Nb jours couverts : {(aujourd_hui - debut_13m).days}")
print()

# Filtrer les transactions sur cette fenetre
txn_13m = txn[
    (txn["DAT_TXN_DT"] >= debut_13m) &
    (txn["DAT_TXN_DT"] <= aujourd_hui)
].copy()

print(f"Transactions total    : {len(txn):>6,}")
print(f"Transactions 13 mois  : {len(txn_13m):>6,} ({len(txn_13m)/len(txn):.1%})")
print()

# Transactions AVANT la fenetre
txn_avant = txn[txn["DAT_TXN_DT"] < debut_13m]
print(f"Transactions anterieures : {len(txn_avant):,}")"""),

code("""# Agregation mensuelle des transactions
txn_13m["MOIS_PERIODE"] = txn_13m["DAT_TXN_DT"].dt.to_period("M")
txn_13m["DEBUT_MOIS"]   = txn_13m["DAT_TXN_DT"].dt.to_period("M").dt.to_timestamp()
txn_13m["MOIS_STR"]     = txn_13m["DAT_TXN_DT"].dt.strftime("%Y-%m")

# Agregation par mois
evol_mensuelle = (
    txn_13m
    .groupby("MOIS_STR")
    .agg(
        nb_transactions  = ("NUM_ORD_MVT_CPB", "count"),
        nb_comptes       = ("IDT_AC",            "nunique"),
        nb_folios        = ("NUM_FOL_XTR",        "nunique"),
    )
    .reset_index()
    .sort_values("MOIS_STR")
)

print("Evolution mensuelle sur 13 mois :")
print()
print(f"{'Mois':>7}  {'Transactions':>13}  {'Comptes':>8}  {'Folios':>7}")
print("-" * 42)
for _, row in evol_mensuelle.iterrows():
    print(f"  {row['MOIS_STR']:>5}  {row['nb_transactions']:>13,}  {row['nb_comptes']:>8,}  {row['nb_folios']:>7,}")
print("-" * 42)
print(f"  {'TOTAL':>5}  {evol_mensuelle['nb_transactions'].sum():>13,}  {'-':>8}  {'-':>7}")"""),

code("""# Agregation par trimestre
txn_13m["TRIMESTRE"] = txn_13m["DAT_TXN_DT"].dt.to_period("Q").astype(str)

evol_trim = (
    txn_13m
    .groupby("TRIMESTRE")
    .agg(
        nb_txn     = ("NUM_ORD_MVT_CPB", "count"),
        nb_comptes = ("IDT_AC", "nunique"),
    )
    .reset_index()
)

print("Evolution par trimestre :")
print(evol_trim.to_string(index=False))"""),

code("""# Exercice de calcul : contrats ouverts et clotures par mois
ctr_ouv_mois = (
    ctr.dropna(subset=["DAT_OUV_DT"])
    .assign(MOIS_OUV = lambda df: df["DAT_OUV_DT"].dt.strftime("%Y-%m"))
    .groupby("MOIS_OUV")
    .size()
    .reset_index(name="nb_ouverts")
)

ctr_clo_mois = (
    ctr.dropna(subset=["DAT_CLO_DT"])
    .assign(MOIS_CLO = lambda df: df["DAT_CLO_DT"].dt.strftime("%Y-%m"))
    .groupby("MOIS_CLO")
    .size()
    .reset_index(name="nb_clotures")
)

mouvements = ctr_ouv_mois.merge(
    ctr_clo_mois.rename(columns={"MOIS_CLO": "MOIS_OUV"}),
    on="MOIS_OUV",
    how="outer"
).fillna(0).sort_values("MOIS_OUV")
mouvements[["nb_ouverts","nb_clotures"]] = mouvements[["nb_ouverts","nb_clotures"]].astype(int)

print("Flux d'ouvertures et de clotures de contrats par mois :")
print(mouvements.to_string(index=False))"""),

# ================================================================
# SECTION 3 : PANDAS AVANCE
# ================================================================
md("""---
# Section 3 - Pandas Avance

## 3.1 Nettoyage des donnees"""),

code("""# Identifier et traiter les doublons
print("=== Doublons dans CTR ===")
dbl_ctr = ctr.duplicated(subset=["IDT_AC"]).sum()
print(f"Doublons sur IDT_AC : {dbl_ctr}")

print()
print("=== Doublons dans TXN ===")
cles_txn = ["IDT_AC", "DAT_CRE_MVT_CPB", "NUM_ORD_MVT_CPB"]
dbl_txn = txn.duplicated(subset=cles_txn).sum()
print(f"Doublons sur cles : {dbl_txn}")

# Supprimer les doublons (si necessaire)
# txn_clean = txn.drop_duplicates(subset=cles_txn, keep="first")"""),

code("""# Nettoyage des chaines de caracteres dans TIE_ADR
print("Avant nettoyage - echantillon NOM_TIE :")
print(tie_adr["NOM_TIE"].head(8).to_list())

tie_adr["NOM_TIE_CLEAN"] = (
    tie_adr["NOM_TIE"]
    .fillna("")
    .str.strip()       # enlever espaces debut/fin
    .str.upper()       # tout en majuscules (normaliser)
    .str.replace(r'\s+', ' ', regex=True)  # espaces multiples -> un seul
)

tie_adr["PRN_CLEAN"] = (
    tie_adr["PRN"]
    .fillna("")
    .str.strip()
    .str.title()       # Capitaliser comme un prenom
)

print()
print("Apres nettoyage - NOM_TIE_CLEAN / PRN_CLEAN :")
tie_adr[["NOM_TIE", "NOM_TIE_CLEAN", "PRN", "PRN_CLEAN"]].head(6)"""),

code("""# Gestion avancee des valeurs manquantes
print("=== Strategie de traitement des manquants dans CTR ===")
print()

# 1. Inspecter
manquants = ctr.isnull().sum()
pct = (manquants / len(ctr) * 100).round(1)
df_manq = pd.DataFrame({"N_manquants": manquants, "Pct": pct})
print(df_manq[df_manq["N_manquants"] > 0])

print()
# 2. Appliquer des strategies differentes selon la colonne
ctr_clean = ctr.copy()

# COD_DEV : remplacer par EUR (valeur par defaut evidente)
ctr_clean["COD_DEV"] = ctr_clean["COD_DEV"].fillna("EUR")

# DAT_CLO_CTR : garder le NaN (le contrat n'est pas cloture, c'est normal)
# SLD_CTR : mettre 0 si manquant serait incorrect → laisser NaN

print("Colonnes restant avec des manquants apres traitement :")
print(ctr_clean.isnull().sum()[ctr_clean.isnull().sum() > 0])"""),

code("""# Pivot table : repartition des contrats par annee et statut
ctr["ANNEE_OUV"] = ctr["DAT_OUV_DT"].dt.year

pivot_contrats = pd.pivot_table(
    ctr,
    values="IDT_AC",
    index="ANNEE_OUV",
    columns="LIB_ECV",
    aggfunc="count",
    fill_value=0
)

print("Pivot : Contrats par annee d'ouverture et statut")
print(pivot_contrats)"""),

code("""# Jointure complete des 5 tables - Vue analytique finale
print("Construction de la vue analytique complete...")

vue_complete = (
    tie_x_ctr[["IDT_PI", "IDT_AC", "FLG_PRE_TTL"]]
    .merge(
        tie[["IDT_PI", "COD_TYP_TIE", "COD_SEX", "COD_LNG_CTR", "AGE", "TRANCHE_AGE"]],
        on="IDT_PI", how="left"
    )
    .merge(
        tie_adr[["IDT_PI", "NOM_TIE_CLEAN", "PRN_CLEAN", "NOM_VIL", "COD_PST", "COD_PAY_ISO"]],
        on="IDT_PI", how="left"
    )
    .merge(
        ctr[["IDT_AC", "REF_CTR_INN", "DAT_OUV_CTR", "LIB_ECV", "CAT_ECV", "COD_DEV", "ANNEE_OUV"]],
        on="IDT_AC", how="left"
    )
)

# Ajouter les statistiques de transactions
resume_txn = txn.groupby("IDT_AC").agg(
    nb_txn_total   = ("NUM_ORD_MVT_CPB", "count"),
    premiere_txn   = ("DAT_TXN_DT", "min"),
    derniere_txn   = ("DAT_TXN_DT", "max"),
).reset_index()

vue_complete = vue_complete.merge(resume_txn, on="IDT_AC", how="left")

print(f"Vue complete : {len(vue_complete):,} lignes x {vue_complete.shape[1]} colonnes")
print()
colonnes_affich = ["NOM_TIE_CLEAN", "PRN_CLEAN", "REF_CTR_INN",
                   "LIB_ECV", "CAT_ECV", "nb_txn_total", "ANNEE_OUV"]
vue_complete[colonnes_affich].head(8)"""),

# ================================================================
# SECTION 4 : VISUALISATION
# ================================================================
md("""---
# Section 4 - Visualisation avec Matplotlib

## 4.1 Philosophie de Matplotlib

Matplotlib fonctionne avec deux niveaux :
- `plt.xxx()` : interface rapide (pour les graphiques simples)
- `fig, ax = plt.subplots()` : interface orientee objet (pour les graphiques avances)

**Recommandation :** utilisez toujours `fig, ax = plt.subplots()` pour avoir un controle complet.

```python
fig, ax = plt.subplots(figsize=(10, 5))  # creer figure + axes
ax.bar(x, y)                              # tracer
ax.set_title("Titre")                     # configurer
ax.set_xlabel("Axe X")
plt.tight_layout()                        # optimiser l'espacement
plt.savefig("graphique.png", dpi=120)     # sauvegarder
plt.show()                                # afficher
```"""),

md("""## 4.2 Bar chart - repartition des contrats par statut"""),

code("""# Donnees
repartition_ecv = ctr["LIB_ECV"].value_counts()
labels = repartition_ecv.index.tolist()
valeurs = repartition_ecv.values
total = valeurs.sum()

# Couleurs par categorie
couleurs = []
for lab in labels:
    if lab in ("Ouvert", "En attente", "Suspendu"):
        couleurs.append("#2ecc71")   # vert = actif
    elif lab == "Cloture":
        couleurs.append("#3498db")   # bleu = cloture
    else:
        couleurs.append("#e74c3c")   # rouge = resilie

# Graphique
fig, ax = plt.subplots(figsize=(10, 5))

barres = ax.bar(labels, valeurs, color=couleurs, edgecolor="white", linewidth=0.8)

# Ajouter les valeurs au-dessus de chaque barre
for barre, val in zip(barres, valeurs):
    pct = val / total * 100
    ax.text(
        barre.get_x() + barre.get_width() / 2,
        barre.get_height() + 0.5,
        f"{val}\n({pct:.1f}%)",
        ha="center", va="bottom", fontsize=9, fontweight="bold"
    )

ax.set_title("Repartition des contrats par statut - Beobank", pad=15)
ax.set_xlabel("Statut du contrat")
ax.set_ylabel("Nombre de contrats")
ax.set_ylim(0, max(valeurs) * 1.2)
ax.grid(axis="y", alpha=0.3, linestyle="--")

plt.tight_layout()
plt.savefig("bar_statuts_contrats.png", dpi=120, bbox_inches="tight")
plt.show()
print("Sauvegarde : bar_statuts_contrats.png")"""),

md("""## 4.3 Line chart - evolution des transactions"""),

code("""# Donnees : toutes les transactions par mois (pas seulement 13 mois)
txn["MOIS_STR"] = txn["DAT_TXN_DT"].dt.strftime("%Y-%m")
evol_all = (
    txn.dropna(subset=["MOIS_STR"])
    .groupby("MOIS_STR")
    .agg(
        nb_txn     = ("NUM_ORD_MVT_CPB", "count"),
        nb_comptes = ("IDT_AC", "nunique"),
    )
    .reset_index()
    .sort_values("MOIS_STR")
)

x_positions = range(len(evol_all))

# Graphique double axe Y
fig, ax1 = plt.subplots(figsize=(13, 5))
ax2 = ax1.twinx()   # deuxieme axe Y partageant le meme axe X

# Axe 1 : transactions (barres)
ax1.bar(x_positions, evol_all["nb_txn"],
        color="#3498db", alpha=0.6, label="Nb transactions")
ax1.set_ylabel("Nombre de transactions", color="#3498db")
ax1.tick_params(axis="y", labelcolor="#3498db")
ax1.set_ylim(0, evol_all["nb_txn"].max() * 1.3)

# Axe 2 : comptes actifs (ligne)
ax2.plot(x_positions, evol_all["nb_comptes"],
         color="#e74c3c", marker="o", linewidth=2,
         markersize=5, label="Comptes actifs")
ax2.set_ylabel("Comptes actifs", color="#e74c3c")
ax2.tick_params(axis="y", labelcolor="#e74c3c")

# Axe X
ax1.set_xticks(list(x_positions))
ax1.set_xticklabels(evol_all["MOIS_STR"], rotation=45, ha="right", fontsize=8)
ax1.set_xlabel("Mois")

# Legendes combinées
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

ax1.set_title("Evolution mensuelle - Transactions et comptes actifs", pad=12)
ax1.grid(axis="y", alpha=0.3, linestyle="--")

plt.tight_layout()
plt.savefig("line_evolution_mensuelle.png", dpi=120, bbox_inches="tight")
plt.show()
print("Sauvegarde : line_evolution_mensuelle.png")"""),

md("""## 4.4 Pie chart - profil des clients"""),

code("""# Repartition par type de tiers
repartition_type = tie["COD_TYP_TIE"].value_counts()
labels_type = [{"1": "Personnes physiques", "2": "Personnes morales"}.get(k, k)
               for k in repartition_type.index]

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Graphique 1 : type de tiers
wedges, texts, autotexts = axes[0].pie(
    repartition_type.values,
    labels=labels_type,
    autopct="%1.1f%%",
    colors=["#3498db", "#e67e22"],
    startangle=90,
    explode=[0.04] * len(labels_type),
    textprops={"fontsize": 11}
)
for at in autotexts:
    at.set_fontweight("bold")
axes[0].set_title("Type de tiers")

# Graphique 2 : langue de communication
repartition_lng = tie["COD_LNG_CTR"].value_counts(dropna=False)
labels_lng = [{"FR": "Francais", "NL": "Neerlandais"}.get(str(k), str(k))
              for k in repartition_lng.index]

wedges2, texts2, autotexts2 = axes[1].pie(
    repartition_lng.values,
    labels=labels_lng,
    autopct="%1.1f%%",
    colors=["#2ecc71", "#9b59b6", "#95a5a6"],
    startangle=90,
    explode=[0.04] * len(labels_lng),
    textprops={"fontsize": 11}
)
for at in autotexts2:
    at.set_fontweight("bold")
axes[1].set_title("Langue de communication")

fig.suptitle("Profil des clients Beobank", fontsize=14, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig("pie_profil_clients.png", dpi=120, bbox_inches="tight")
plt.show()
print("Sauvegarde : pie_profil_clients.png")"""),

md("""## 4.5 Graphiques avances : subplot multiple"""),

code("""# Tableau de bord en 4 graphiques (2x2)
fig, axes = plt.subplots(2, 2, figsize=(14, 9))
fig.suptitle("Tableau de bord Beobank - Vue d'ensemble",
             fontsize=15, fontweight="bold", y=1.01)

# --- Graphique 1 (haut gauche) : Contrats par annee d'ouverture ---
ax1 = axes[0, 0]
ctr_annee = ctr.groupby("ANNEE_OUV").size().reset_index(name="nb")
ctr_annee = ctr_annee.dropna(subset=["ANNEE_OUV"])
ctr_annee["ANNEE_OUV"] = ctr_annee["ANNEE_OUV"].astype(int)
ax1.bar(ctr_annee["ANNEE_OUV"].astype(str), ctr_annee["nb"],
        color="#3498db", edgecolor="white")
ax1.set_title("Contrats par annee d'ouverture")
ax1.set_xlabel("Annee")
ax1.set_ylabel("Nombre")
for barre, val in zip(ax1.patches, ctr_annee["nb"]):
    ax1.text(barre.get_x() + barre.get_width()/2, barre.get_height() + 0.2,
             str(val), ha="center", va="bottom", fontsize=8)
ax1.grid(axis="y", alpha=0.3)

# --- Graphique 2 (haut droite) : Transactions par mois (13 mois) ---
ax2 = axes[0, 1]
evol_13m = evol_mensuelle if len(evol_mensuelle) > 0 else evol_all.tail(13)
ax2.plot(range(len(evol_13m)), evol_13m["nb_transactions"],
         marker="o", color="#e74c3c", linewidth=2, markersize=5)
ax2.set_xticks(range(len(evol_13m)))
ax2.set_xticklabels(evol_13m["MOIS_STR"] if "MOIS_STR" in evol_13m.columns else evol_13m["MOIS_STR"],
                    rotation=45, ha="right", fontsize=7)
ax2.set_title("Transactions / mois (13 mois glissants)")
ax2.set_ylabel("Nb transactions")
ax2.fill_between(range(len(evol_13m)), evol_13m["nb_transactions"], alpha=0.15, color="#e74c3c")
ax2.grid(alpha=0.3)

# --- Graphique 3 (bas gauche) : Distribution des ages ---
ax3 = axes[1, 0]
tranches = tie["TRANCHE_AGE"].value_counts().sort_index()
ax3.barh(tranches.index.astype(str), tranches.values, color="#2ecc71", edgecolor="white")
ax3.set_title("Distribution par tranche d'age")
ax3.set_xlabel("Nombre de clients")
for i, val in enumerate(tranches.values):
    ax3.text(val + 0.1, i, str(val), va="center", fontsize=9)
ax3.grid(axis="x", alpha=0.3)

# --- Graphique 4 (bas droite) : Statut des contrats ---
ax4 = axes[1, 1]
couleurs_statut = {"Ouvert":"#2ecc71","En attente":"#f1c40f","Suspendu":"#f39c12",
                   "Cloture":"#3498db","En resiliation":"#e67e22","Resilie":"#e74c3c"}
repartition_ecv2 = ctr["LIB_ECV"].value_counts()
colors4 = [couleurs_statut.get(l, "#95a5a6") for l in repartition_ecv2.index]
ax4.pie(repartition_ecv2.values, labels=repartition_ecv2.index,
        autopct="%1.1f%%", colors=colors4, startangle=90,
        textprops={"fontsize": 9})
ax4.set_title("Repartition par statut")

plt.tight_layout()
plt.savefig("tableau_de_bord_4graphiques.png", dpi=120, bbox_inches="tight")
plt.show()
print("Sauvegarde : tableau_de_bord_4graphiques.png")"""),

# ================================================================
# EXERCICES
# ================================================================
md("""---
# Exercices du Jour 3

## Exercice 1 - Analyser l'activite mensuelle avec LAG

**Contexte :** Pour le rapport, votre manager veut voir la variation mensuelle
du nombre de transactions (mois N vs mois N-1) et identifier les mois en hausse
ou en baisse.

**Taches :**
1. Calculer l'evolution mensuelle des transactions
2. Ajouter une colonne `variation_pct` (variation % par rapport au mois precedent)
3. Ajouter une colonne `tendance` : "Hausse" si > 0%, "Baisse" si < 0%, "Stable" si = 0%
4. Afficher le resultat trie par mois"""),

code("""# ============================================================
# EXERCICE 1 - Variation mensuelle avec LAG
# ============================================================

import pandas as pd
from pathlib import Path

DATA = Path("../Orsys")
txn = pd.read_csv(DATA / "TXN_X_CTR.csv", sep=";", na_values=".", encoding="utf-8")
txn["DAT_TXN_DT"] = pd.to_datetime(txn["DAT_CRE_MVT_CPB"], errors="coerce")

# ETAPE 1 : agregation mensuelle
evol = (
    txn.dropna(subset=["DAT_TXN_DT"])
    .assign(MOIS=lambda df: df["DAT_TXN_DT"].dt.strftime("%Y-%m"))
    .groupby("MOIS")
    .size()
    .reset_index(name="nb_txn")
    .sort_values("MOIS")
)

# ETAPE 2 : LAG avec shift(1) - valeur du mois precedent
evol["nb_txn_mois_prec"] = evol["nb_txn"].shift(1)

# ETAPE 3 : calcul de la variation
evol["variation_abs"] = evol["nb_txn"] - evol["nb_txn_mois_prec"]
evol["variation_pct"] = (evol["variation_abs"] / evol["nb_txn_mois_prec"] * 100).round(1)

# ETAPE 4 : tendance
import numpy as np
evol["tendance"] = np.select(
    [evol["variation_pct"] > 0, evol["variation_pct"] < 0, evol["variation_pct"] == 0],
    ["Hausse", "Baisse", "Stable"],
    default="N/A"
)

print("Evolution mensuelle des transactions :")
print()
print(f"{'Mois':>7}  {'N txn':>6}  {'Precedent':>9}  {'Variation':>10}  {'Pct':>6}  {'Tendance'}")
print("-" * 60)
for _, row in evol.iterrows():
    prec  = f"{int(row['nb_txn_mois_prec']):>9,}" if pd.notna(row['nb_txn_mois_prec']) else f"{'N/A':>9}"
    var   = f"{int(row['variation_abs']):>+10,}"  if pd.notna(row['variation_abs'])   else f"{'N/A':>10}"
    pct   = f"{row['variation_pct']:>+5.1f}%"      if pd.notna(row['variation_pct'])   else f"{'N/A':>6}"
    tend  = row["tendance"]
    print(f"  {row['MOIS']:>5}  {row['nb_txn']:>6,}  {prec}  {var}  {pct}  {tend}")"""),

md("""## Exercice 2 - Graphique de l'evolution avec tendance coloree

**Contexte :** Visualisez l'evolution calculee dans l'exercice 1 :
une ligne chart avec les barres colorees selon la tendance (vert=hausse, rouge=baisse).

**Tache :** Produire et sauvegarder ce graphique."""),

code("""# ============================================================
# EXERCICE 2 - Graphique evolution avec tendance
# ============================================================

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Donnees (reprend evol de l'exercice 1)
evol_plot = evol.dropna(subset=["variation_pct"]).copy()
x = range(len(evol_plot))

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 8),
                                 gridspec_kw={"height_ratios": [2, 1]})
fig.suptitle("Evolution mensuelle des transactions - Beobank",
             fontsize=14, fontweight="bold")

# --- Graphique 1 : ligne des transactions ---
ax1.plot(range(len(evol)), evol["nb_txn"],
         marker="o", color="#2980b9", linewidth=2, markersize=5, zorder=3)
ax1.fill_between(range(len(evol)), evol["nb_txn"], alpha=0.15, color="#2980b9")
ax1.set_xticks(range(len(evol)))
ax1.set_xticklabels(evol["MOIS"], rotation=45, ha="right", fontsize=8)
ax1.set_ylabel("Nombre de transactions")
ax1.set_title("Volume mensuel des transactions")
ax1.grid(alpha=0.3)
ax1.axhline(y=evol["nb_txn"].mean(), color="orange", linestyle="--",
            linewidth=1, label=f"Moyenne : {evol['nb_txn'].mean():.0f}")
ax1.legend(fontsize=9)

# --- Graphique 2 : barres de variation ---
couleurs_var = ["#2ecc71" if t == "Hausse" else "#e74c3c" if t == "Baisse" else "#95a5a6"
                for t in evol_plot["tendance"]]
barres = ax2.bar(range(len(evol_plot)), evol_plot["variation_pct"],
                 color=couleurs_var, edgecolor="white", linewidth=0.5)
ax2.axhline(y=0, color="black", linewidth=0.8)
ax2.set_xticks(range(len(evol_plot)))
ax2.set_xticklabels(evol_plot["MOIS"], rotation=45, ha="right", fontsize=8)
ax2.set_ylabel("Variation (%)")
ax2.set_title("Variation vs mois precedent (%)")
ax2.grid(axis="y", alpha=0.3)

# Legende
patch_h = mpatches.Patch(color="#2ecc71", label="Hausse")
patch_b = mpatches.Patch(color="#e74c3c", label="Baisse")
ax2.legend(handles=[patch_h, patch_b], fontsize=9)

plt.tight_layout()
plt.savefig("evolution_variation_mensuelle.png", dpi=120, bbox_inches="tight")
plt.show()
print("Sauvegarde : evolution_variation_mensuelle.png")"""),

md("""## Exercice 3 - Analyse des operations par type

**Contexte :** Le rapport doit inclure une analyse des types d'operations.
Chaque transaction a un libelle dans `LIB_OPE_INL_1`.
Ces libelles contiennent des mots-cles (SEPA, Domicili, REJ, BEOBANK...).

**Taches :**
1. Creer une colonne `TYPE_OPE` qui categorise chaque transaction
   selon les mots-cles de `LIB_OPE_INL_1`
2. Calculer la repartition par type
3. Visualiser en bar chart horizontal"""),

code("""# ============================================================
# EXERCICE 3 - Categorisation des types d'operations
# ============================================================

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

DATA = Path("../Orsys")
txn = pd.read_csv(DATA / "TXN_X_CTR.csv", sep=";", na_values=".", encoding="utf-8")
txn["DAT_TXN_DT"] = pd.to_datetime(txn["DAT_CRE_MVT_CPB"], errors="coerce")

# Regle de categorisation basee sur les mots-cles
def categoriser_operation(lib):
    '''Categorise une operation bancaire selon son libelle.'''
    if pd.isna(lib) or lib == "":
        return "Inconnu"
    lib_up = str(lib).upper()
    if "SEPA" in lib_up:
        return "Virement SEPA"
    elif "DOMICILI" in lib_up:
        return "Domiciliation"
    elif "REJ" in lib_up or "REJET" in lib_up:
        return "Rejet"
    elif "BEOBANK" in lib_up:
        return "Operation interne Beobank"
    elif "NATIONALE" in lib_up or "BNB" in lib_up:
        return "Operation Banque Nationale"
    else:
        return "Autre"

txn["TYPE_OPE"] = txn["LIB_OPE_INL_1"].apply(categoriser_operation)

# Repartition
repartition_ops = txn["TYPE_OPE"].value_counts().reset_index()
repartition_ops.columns = ["TYPE_OPE", "nb_txn"]
repartition_ops["pct"] = (repartition_ops["nb_txn"] / len(txn) * 100).round(1)

print("Repartition par type d'operation :")
print()
print(f"{'Type':30s}  {'N':>6}  {'%':>6}")
print("-" * 46)
for _, row in repartition_ops.iterrows():
    print(f"  {row['TYPE_OPE']:28s}  {row['nb_txn']:>6,}  {row['pct']:>5.1f}%")

# Graphique
fig, ax = plt.subplots(figsize=(10, 5))
couleurs_ops = ["#3498db", "#2ecc71", "#e74c3c", "#f39c12", "#9b59b6", "#95a5a6"]
barres = ax.barh(repartition_ops["TYPE_OPE"], repartition_ops["nb_txn"],
                 color=couleurs_ops[:len(repartition_ops)], edgecolor="white")
for barre, (val, pct) in zip(barres, zip(repartition_ops["nb_txn"], repartition_ops["pct"])):
    ax.text(barre.get_width() + 5, barre.get_y() + barre.get_height()/2,
            f"{val:,}  ({pct:.1f}%)", va="center", fontsize=9)
ax.set_xlabel("Nombre de transactions")
ax.set_title("Repartition des transactions par type d'operation")
ax.set_xlim(0, repartition_ops["nb_txn"].max() * 1.3)
ax.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.savefig("bar_types_operations.png", dpi=120, bbox_inches="tight")
plt.show()"""),

# ================================================================
# SECTION 5 : MINI-PROJET FINAL
# ================================================================
md("""---
# Section 5 - Mini-projet final : Rapport d'activite Beobank

## Objectif

Vous avez tout appris. Maintenant vous assemblez le **rapport complet**
qui repond aux 4 questions de votre manager :

1. Inventaire des contrats (statuts, annees)
2. Profil des clients (type, age, langue)
3. Activite transactionnelle sur 13 mois
4. Visualisations finales

Le pipeline suit ces etapes :
```
Chargement des 5 tables
        |
Nettoyage et preparation
        |
Construction de la vue analytique
        |
Indicateurs temporels (13 mois)
        |
Rapport textuel + Graphiques
        |
Export CSV + JSON
```

**Executez les cellules dans l'ordre - chaque cellule s'appuie sur la precedente.**"""),

code("""# ============================================================
# ETAPE 1 - Chargement et preparation
# ============================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from pandas.tseries.offsets import DateOffset

DATA = Path("../Orsys")
PARAMS = dict(sep=";", na_values=".", encoding="utf-8")
AUJOURD_HUI = pd.Timestamp.today().normalize()
DEBUT_13M   = AUJOURD_HUI - DateOffset(months=13)

print(f"Rapport d'activite Beobank")
print(f"Periode d'analyse : {DEBUT_13M.date()} → {AUJOURD_HUI.date()}")
print(f"{'='*50}")
print()

# Chargement
ctr       = pd.read_csv(DATA / "CTR.csv",       **PARAMS)
tie       = pd.read_csv(DATA / "TIE.csv",       **PARAMS)
tie_adr   = pd.read_csv(DATA / "TIE_ADR.csv",   **PARAMS)
tie_x_ctr = pd.read_csv(DATA / "TIE_X_CTR.csv", **PARAMS)
txn       = pd.read_csv(DATA / "TXN_X_CTR.csv", **PARAMS)

# Conversions
ctr["DAT_OUV_DT"] = pd.to_datetime(ctr["DAT_OUV_CTR"], errors="coerce")
ctr["DAT_CLO_DT"] = pd.to_datetime(ctr["DAT_CLO_CTR"], errors="coerce")
txn["DAT_TXN_DT"] = pd.to_datetime(txn["DAT_CRE_MVT_CPB"], errors="coerce")
tie["DAT_NAI_DT"] = pd.to_datetime(tie["DAT_NAI"], errors="coerce")

# Mappings
MAPPING_ECV = {"1":"Ouvert","2":"En attente","3":"Suspendu",
               "4":"Cloture","5":"En resiliation","6":"Resilie"}
MAPPING_CAT = {"1":"Actif","2":"Actif","3":"Actif",
               "4":"Inactif","5":"Inactif","6":"Inactif"}
MAPPING_TYP = {"1":"Personne physique","2":"Personne morale"}
MAPPING_LNG = {"FR":"Francais","NL":"Neerlandais"}

ctr["LIB_ECV"] = ctr["COD_ECV_CTR"].map(MAPPING_ECV).fillna("Inconnu")
ctr["CAT_ECV"] = ctr["COD_ECV_CTR"].map(MAPPING_CAT).fillna("Inconnu")
ctr["ANNEE_OUV"] = ctr["DAT_OUV_DT"].dt.year
tie["LIB_TYP"] = tie["COD_TYP_TIE"].map(MAPPING_TYP).fillna("Autre")
tie["AGE"] = ((AUJOURD_HUI - tie["DAT_NAI_DT"]).dt.days / 365.25).round(0).astype("Int64")
tie["TRANCHE_AGE"] = pd.cut(
    tie["AGE"].astype(float),
    bins=[0, 25, 35, 50, 65, 120],
    labels=["<25 ans", "25-34 ans", "35-49 ans", "50-64 ans", "65+ ans"],
    right=False
)

# Nettoyage adresses
tie_adr["NOM_TIE_C"] = tie_adr["NOM_TIE"].fillna("").str.strip().str.upper()
tie_adr["PRN_C"]     = tie_adr["PRN"].fillna("").str.strip().str.title()

print(f"CTR       : {len(ctr):>5} contrats")
print(f"TIE       : {len(tie):>5} clients")
print(f"TIE_ADR   : {len(tie_adr):>5} adresses")
print(f"TIE_X_CTR : {len(tie_x_ctr):>5} liens")
print(f"TXN       : {len(txn):>5} transactions")
print()
print("ETAPE 1 terminee")"""),

code("""# ============================================================
# ETAPE 2 - Vue analytique complete
# ============================================================

vue = (
    tie_x_ctr[["IDT_PI","IDT_AC","FLG_PRE_TTL"]]
    .merge(tie[["IDT_PI","COD_TYP_TIE","LIB_TYP","COD_LNG_CTR","COD_SEX","AGE","TRANCHE_AGE"]], on="IDT_PI", how="left")
    .merge(tie_adr[["IDT_PI","NOM_TIE_C","PRN_C","NOM_VIL","COD_PST","COD_PAY_ISO"]], on="IDT_PI", how="left")
    .merge(ctr[["IDT_AC","REF_CTR_INN","DAT_OUV_CTR","LIB_ECV","CAT_ECV","COD_DEV","ANNEE_OUV"]], on="IDT_AC", how="left")
)

# Statistiques transactions par compte (sur 13 mois)
txn_13m = txn[txn["DAT_TXN_DT"] >= DEBUT_13M].copy()
stats_txn = (
    txn_13m
    .groupby("IDT_AC")
    .agg(
        nb_txn_13m   = ("NUM_ORD_MVT_CPB", "count"),
        mois_actif   = ("DAT_TXN_DT",      lambda x: x.dt.to_period("M").nunique()),
        premiere_txn = ("DAT_TXN_DT",      "min"),
        derniere_txn = ("DAT_TXN_DT",      "max"),
    )
    .reset_index()
)

vue = vue.merge(stats_txn, on="IDT_AC", how="left")
vue["est_actif_13m"] = (vue["nb_txn_13m"] > 0).astype(int)

print(f"Vue analytique : {len(vue):,} lignes x {vue.shape[1]} colonnes")
print()
print("Repartition par categorie de contrat :")
print(vue["CAT_ECV"].value_counts().to_frame("Effectif").to_string())
print()
print("ETAPE 2 terminee")"""),

code("""# ============================================================
# ETAPE 3 - Indicateurs cles du rapport
# ============================================================

print("=" * 55)
print("  RAPPORT D'ACTIVITE BEOBANK")
print(f"  Au {AUJOURD_HUI.strftime('%d/%m/%Y')}")
print("=" * 55)

# --- SECTION A : CONTRATS ---
print()
print("  A. PORTEFEUILLE CONTRATS")
print(f"  {'─'*50}")
total_ctr = len(ctr)
actifs_n  = (ctr["CAT_ECV"] == "Actif").sum()
inactifs_n= (ctr["CAT_ECV"] == "Inactif").sum()

print(f"  Contrats total     : {total_ctr:>6,}")
print(f"  Contrats actifs    : {actifs_n:>6,}  ({actifs_n/total_ctr:.1%})")
print(f"  Contrats inactifs  : {inactifs_n:>6,}  ({inactifs_n/total_ctr:.1%})")
print()
for lib, nb in ctr["LIB_ECV"].value_counts().items():
    print(f"    {lib:22s}: {nb:>4,}  ({nb/total_ctr:.1%})")

# --- SECTION B : CLIENTS ---
print()
print("  B. PROFIL CLIENTS")
print(f"  {'─'*50}")
total_cli = len(tie)
pp_n = (tie["COD_TYP_TIE"] == "1").sum()
pm_n = (tie["COD_TYP_TIE"] == "2").sum()
print(f"  Clients total          : {total_cli:>5,}")
print(f"  Personnes physiques    : {pp_n:>5,}  ({pp_n/total_cli:.1%})")
print(f"  Personnes morales      : {pm_n:>5,}  ({pm_n/total_cli:.1%})")
age_moyen = tie["AGE"].mean()
print(f"  Age moyen (PP)         : {age_moyen:.1f} ans")

# --- SECTION C : ACTIVITE 13 MOIS ---
print()
print(f"  C. ACTIVITE TRANSACTIONNELLE ({DEBUT_13M.strftime('%Y-%m')} → {AUJOURD_HUI.strftime('%Y-%m')})")
print(f"  {'─'*50}")
print(f"  Transactions 13 mois   : {len(txn_13m):>6,}")
print(f"  Comptes actifs 13 mois : {txn_13m['IDT_AC'].nunique():>6,}")

evol_m = (txn_13m.assign(MOIS=lambda df: df["DAT_TXN_DT"].dt.strftime("%Y-%m"))
          .groupby("MOIS").size().reset_index(name="n").sort_values("MOIS"))
if len(evol_m) > 0:
    max_mois = evol_m.loc[evol_m["n"].idxmax()]
    min_mois = evol_m.loc[evol_m["n"].idxmin()]
    print(f"  Mois le plus actif     : {max_mois['MOIS']} ({max_mois['n']:,} txn)")
    print(f"  Mois le moins actif    : {min_mois['MOIS']} ({min_mois['n']:,} txn)")
    print(f"  Moyenne mensuelle      : {evol_m['n'].mean():.0f} txn/mois")

print()
print("  ETAPE 3 terminee")"""),

code("""# ============================================================
# ETAPE 4 - Tableau de bord graphique final
# ============================================================

fig = plt.figure(figsize=(16, 11))
fig.suptitle(f"Rapport d'activite Beobank - {AUJOURD_HUI.strftime('%d/%m/%Y')}",
             fontsize=16, fontweight="bold", y=0.98)

# Layout en grille (3 lignes, 3 colonnes)
from matplotlib.gridspec import GridSpec
gs = GridSpec(3, 3, figure=fig, hspace=0.5, wspace=0.4)

# --- G1 (ligne 0, col 0) : Pie statuts contrats ---
ax1 = fig.add_subplot(gs[0, 0])
r_ecv = ctr["LIB_ECV"].value_counts()
col_ecv = ["#2ecc71","#f1c40f","#f39c12","#3498db","#e67e22","#e74c3c"]
ax1.pie(r_ecv.values, labels=r_ecv.index, autopct="%1.0f%%",
        colors=col_ecv[:len(r_ecv)], startangle=90, textprops={"fontsize":8})
ax1.set_title("Statut des contrats", fontsize=10)

# --- G2 (ligne 0, col 1) : Bar type clients ---
ax2 = fig.add_subplot(gs[0, 1])
r_typ = tie["LIB_TYP"].value_counts()
ax2.bar(r_typ.index, r_typ.values, color=["#3498db","#e67e22"], edgecolor="white")
for b, v in zip(ax2.patches, r_typ.values):
    ax2.text(b.get_x()+b.get_width()/2, b.get_height()+0.5, str(v),
             ha="center", fontsize=9, fontweight="bold")
ax2.set_title("Type de clients", fontsize=10)
ax2.set_ylabel("Effectif")
ax2.grid(axis="y", alpha=0.3)

# --- G3 (ligne 0, col 2) : Bar tranches age ---
ax3 = fig.add_subplot(gs[0, 2])
r_age = tie["TRANCHE_AGE"].value_counts().sort_index()
ax3.barh(r_age.index.astype(str), r_age.values, color="#9b59b6", edgecolor="white")
ax3.set_title("Tranche d'age (PP)", fontsize=10)
ax3.set_xlabel("Effectif")
ax3.grid(axis="x", alpha=0.3)

# --- G4 (ligne 1, toute la largeur) : Evolution mensuelle ---
ax4 = fig.add_subplot(gs[1, :])
evol_m_sorted = evol_m.sort_values("MOIS")
x4 = range(len(evol_m_sorted))
ax4.bar(x4, evol_m_sorted["n"], color="#2980b9", alpha=0.7)
ax4.plot(x4, evol_m_sorted["n"], marker="o", color="#e74c3c",
         linewidth=1.5, markersize=4, zorder=3)
ax4.axhline(evol_m_sorted["n"].mean(), color="orange", linestyle="--",
            linewidth=1.2, label=f"Moyenne : {evol_m_sorted['n'].mean():.0f}")
ax4.set_xticks(list(x4))
ax4.set_xticklabels(evol_m_sorted["MOIS"], rotation=45, ha="right", fontsize=8)
ax4.set_title(f"Transactions mensuelles ({DEBUT_13M.strftime('%Y-%m')} → {AUJOURD_HUI.strftime('%Y-%m')})", fontsize=10)
ax4.set_ylabel("Nb transactions")
ax4.legend(fontsize=9)
ax4.grid(axis="y", alpha=0.3)

# --- G5 (ligne 2, col 0-1) : Top 10 comptes actifs ---
ax5 = fig.add_subplot(gs[2, :2])
top10_comptes = (
    txn_13m.groupby("IDT_AC")
    .size()
    .nlargest(10)
    .reset_index(name="nb_txn")
)
top10_comptes["IDT_AC_STR"] = top10_comptes["IDT_AC"].astype(str).str[-6:]
ax5.barh(top10_comptes["IDT_AC_STR"][::-1], top10_comptes["nb_txn"][::-1],
         color="#27ae60", edgecolor="white")
ax5.set_title("Top 10 comptes (13 mois)", fontsize=10)
ax5.set_xlabel("Nb transactions")
ax5.grid(axis="x", alpha=0.3)

# --- G6 (ligne 2, col 2) : Pie langue ---
ax6 = fig.add_subplot(gs[2, 2])
r_lng = tie["COD_LNG_CTR"].value_counts(dropna=False)
lbls_lng = [MAPPING_LNG.get(str(k), str(k)) for k in r_lng.index]
ax6.pie(r_lng.values, labels=lbls_lng, autopct="%1.1f%%",
        colors=["#1abc9c","#e74c3c","#95a5a6"],
        startangle=90, textprops={"fontsize":9})
ax6.set_title("Langue", fontsize=10)

plt.savefig("rapport_beobank_final.png", dpi=120, bbox_inches="tight")
plt.show()
print("Sauvegarde : rapport_beobank_final.png")"""),

code("""# ============================================================
# ETAPE 5 - Export final
# ============================================================

# Export 1 : vue analytique complete
export_vue = vue.copy()
# Formater les dates pour l'export
for col in ["premiere_txn", "derniere_txn"]:
    if col in export_vue.columns:
        export_vue[col] = pd.to_datetime(export_vue[col]).dt.strftime("%Y-%m-%d")
for col in export_vue.select_dtypes(include=["category"]).columns:
    export_vue[col] = export_vue[col].astype(str)
for col in export_vue.select_dtypes(include=["Int64"]).columns:
    export_vue[col] = export_vue[col].astype(object)

export_vue.to_csv("beobank_vue_analytique_complete.csv",
                  sep=";", index=False, encoding="utf-8")
print(f"Export 1 : beobank_vue_analytique_complete.csv ({len(export_vue):,} lignes)")

# Export 2 : resume indicateurs (JSON)
import json, datetime
indicateurs = {
    "date_rapport"         : AUJOURD_HUI.strftime("%Y-%m-%d"),
    "periode_13m_debut"    : DEBUT_13M.strftime("%Y-%m-%d"),
    "periode_13m_fin"      : AUJOURD_HUI.strftime("%Y-%m-%d"),
    "nb_contrats_total"    : int(len(ctr)),
    "nb_contrats_actifs"   : int((ctr["CAT_ECV"]=="Actif").sum()),
    "nb_contrats_inactifs" : int((ctr["CAT_ECV"]=="Inactif").sum()),
    "nb_clients"           : int(len(tie)),
    "nb_pp"                : int((tie["COD_TYP_TIE"]=="1").sum()),
    "nb_pm"                : int((tie["COD_TYP_TIE"]=="2").sum()),
    "age_moyen"            : round(float(tie["AGE"].mean()), 1),
    "nb_txn_13m"           : int(len(txn_13m)),
    "nb_comptes_actifs_13m": int(txn_13m["IDT_AC"].nunique()),
    "moy_txn_mensuelle"    : round(float(evol_m["n"].mean()), 1),
}

with open("beobank_indicateurs.json", "w", encoding="utf-8") as f:
    json.dump(indicateurs, f, ensure_ascii=False, indent=2)
print(f"Export 2 : beobank_indicateurs.json")

# Export 3 : evolution mensuelle
evol_m.to_csv("beobank_evolution_mensuelle.csv",
              sep=";", index=False, encoding="utf-8")
print(f"Export 3 : beobank_evolution_mensuelle.csv ({len(evol_m)} mois)")

print()
print("=" * 55)
print("  MINI-PROJET TERMINE !")
print()
print("  Vous avez produit :")
print("  - 1 vue analytique complete (CSV, 200+ lignes)")
print("  - 1 fichier d'indicateurs (JSON)")
print("  - 1 evolution mensuelle (CSV)")
print("  - 4 graphiques (PNG)")
print()
print("  Competences utilisees (Jours 1, 2 et 3) :")
print("  - Variables, fonctions, boucles, dicts     (Jour 1)")
print("  - Pandas : chargement, nettoyage, jointures (Jour 2)")
print("  - Dates, periodes glissantes, visualisation (Jour 3)")
print("=" * 55)"""),

# ================================================================
# RESUME FINAL
# ================================================================
md("""---
# Resume general de la formation

Vous avez parcouru en 3 jours **tout le parcours d'un analyste data Python chez Beobank**.

## Ce que vous savez faire

| Jour | Competence | Outil Python |
|------|-----------|--------------|
| **1** | Variables, conditions, boucles | `if/elif/else`, `for`, `while` |
| **1** | Structures de donnees | `list`, `tuple`, `dict` |
| **1** | Fonctions reutilisables | `def`, `return`, `lambda` |
| **2** | Lire des fichiers | `open()`, `pathlib`, `csv`, `json` |
| **2** | Charger les tables Beobank | `pd.read_csv(sep=';', na_values='.')` |
| **2** | Explorer, filtrer, aggreger | `head()`, `isin()`, `groupby()`, `agg()` |
| **2** | Joindre des tables | `df.merge(..., how='left')` |
| **2** | Exporter les resultats | `to_csv()`, `to_json()` |
| **3** | Requetes SQL analytiques | `pd.read_sql()`, CTEs, OVER |
| **3** | Fonctions de fenetres | `shift()`, `cumcount()`, `transform()` |
| **3** | Dates et periodes glissantes | `pd.to_datetime()`, `DateOffset` |
| **3** | Visualisations | `matplotlib` : bar, line, pie |
| **3** | Pipeline de bout en bout | Chargement → Analyse → Rapport |

## Correspondances SAS → Python

| SAS | Python |
|-----|--------|
| `proc import; infile dlm=';'` | `pd.read_csv(sep=';', na_values='.')` |
| `proc print (obs=10)` | `df.head(10)` |
| `proc contents` | `df.info()` |
| `proc means` | `df.describe()` |
| `proc freq` | `df['col'].value_counts()` |
| `proc sort by col` | `df.sort_values('col')` |
| `proc summary / proc means by group` | `df.groupby('col').agg(...)` |
| `proc sql left join` | `df.merge(..., how='left')` |
| `data step LAG()` | `df.groupby(...).shift(1)` |
| `intck('month', d1, d2)` | `(d2 - d1).dt.days / 30.44` |
| `add_months(d, n)` | `d + DateOffset(months=n)` |
| `proc gplot` / `proc sgplot` | `matplotlib.pyplot` |
| `proc export` | `df.to_csv(sep=';')` |

## Ressources pour continuer

- **Documentation Pandas** : pandas.pydata.org/docs
- **Documentation Matplotlib** : matplotlib.org/stable/gallery
- **Python pour la data science** : realpython.com
- **Exercices pratiques** : kaggle.com/learn/pandas
- **Vertica Python driver** : docs.vertica.com (vertica_python)"""),

] # fin j3

path = os.path.join(OUTPUT_DIR, "Jour3_SQL_TimeSeries_Visualisation.ipynb")
with open(path, "w", encoding="utf-8") as f:
    json.dump(notebook(j3), f, ensure_ascii=False, indent=1)
print(f"Jour 3 cree : {os.path.getsize(path)//1024} Ko — {len(j3)} cellules")
