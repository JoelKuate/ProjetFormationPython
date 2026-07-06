"""
Generateur Jour 3 v2 - SQL Analytique, Time Series, Visualisation
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

j3 = [

md("""# Jour 3 — SQL Analytique, Time Series et Visualisation
## Formation Python Beobank · 20 novembre 2026

---

### Rappel du contexte et de ce que vous avez appris

**Jour 1 :** Variables, conditions, boucles, listes, dictionnaires, fonctions
**Jour 2 :** Pandas — charger, filtrer, grouper, joindre, exporter

**Aujourd'hui :** le rapport prend forme graphiquement.

### Plan du jour
1. SQL analytique Vertica : CTEs, OVER/PARTITION BY, LAG/LEAD
2. Gestion avancee des dates (13 mois glissants, periodes)
3. Pandas avance : nettoyage, pivot, texte
4. Visualisation Matplotlib : 4 types de graphiques
5. Mini-projet final : pipeline complet de bout en bout

> **Conseil :** executez d'abord la cellule de setup ci-dessous."""),

# ============================================================
# SETUP
# ============================================================
md("""---
## Cellule de setup — executer EN PREMIER

Charge les 5 tables, les prepare et cree la base SQLite."""),

code("""# ── Imports ──────────────────────────────────────────────────
import pandas as pd                  # manipulation de donnees
import numpy as np                   # calculs numeriques
import sqlite3                       # base de donnees SQLite (simulation Vertica)
import matplotlib.pyplot as plt      # visualisation
from pathlib import Path             # chemins de fichiers
from pandas.tseries.offsets import DateOffset  # calculs de periodes

# ── Configuration Matplotlib ─────────────────────────────────
# rcParams : dictionnaire de configuration global de Matplotlib
plt.rcParams.update({
    "figure.dpi"      : 110,         # resolution des figures
    "font.size"       : 10,          # taille de police par defaut
    "axes.titlesize"  : 12,          # taille du titre des axes
    "axes.titleweight": "bold",      # titre en gras
    "axes.spines.top" : False,       # supprimer le bord haut
    "axes.spines.right": False,      # supprimer le bord droit
})

# ── Chargement des donnees ────────────────────────────────────
DATA   = Path("../Orsys")
PARAMS = dict(sep=";", na_values=".", encoding="utf-8")

ctr       = pd.read_csv(DATA / "CTR.csv",       **PARAMS)
tie       = pd.read_csv(DATA / "TIE.csv",       **PARAMS)
tie_adr   = pd.read_csv(DATA / "TIE_ADR.csv",   **PARAMS)
tie_x_ctr = pd.read_csv(DATA / "TIE_X_CTR.csv", **PARAMS)
txn       = pd.read_csv(DATA / "TXN_X_CTR.csv", **PARAMS)

# ── Conversions de dates ──────────────────────────────────────
# Convertir les colonnes de dates texte en objets datetime Python
ctr["DAT_OUV_DT"] = pd.to_datetime(ctr["DAT_OUV_CTR"], errors="coerce")
ctr["DAT_CLO_DT"] = pd.to_datetime(ctr["DAT_CLO_CTR"], errors="coerce")
txn["DAT_TXN_DT"] = pd.to_datetime(txn["DAT_CRE_MVT_CPB"], errors="coerce")
tie["DAT_NAI_DT"] = pd.to_datetime(tie["DAT_NAI"], errors="coerce")

# ── Colonnes derivees CTR ─────────────────────────────────────
MAPPING_ECV = {"1":"Ouvert","2":"En attente","3":"Suspendu",
               "4":"Cloture","5":"En resiliation","6":"Resilie"}
MAPPING_CAT = {"1":"Actif","2":"Actif","3":"Actif",
               "4":"Inactif","5":"Inactif","6":"Inactif"}
ctr["LIB_ECV"]  = ctr["COD_ECV_CTR"].map(MAPPING_ECV).fillna("Inconnu")
ctr["CAT_ECV"]  = ctr["COD_ECV_CTR"].map(MAPPING_CAT).fillna("Inconnu")
ctr["ANNEE_OUV"]= ctr["DAT_OUV_DT"].dt.year

# ── Colonnes derivees TIE ─────────────────────────────────────
tie["AGE"] = ((pd.Timestamp.today() - tie["DAT_NAI_DT"]).dt.days / 365.25).round(0).astype("Int64")
tie["TRANCHE_AGE"] = pd.cut(
    tie["AGE"].astype(float),
    bins=[0,25,35,50,65,120],
    labels=["<25 ans","25-34 ans","35-49 ans","50-64 ans","65+ ans"],
    right=False
)

# ── Nettoyage adresses ────────────────────────────────────────
tie_adr["NOM_TIE_C"] = tie_adr["NOM_TIE"].fillna("").str.strip().str.upper()
tie_adr["PRN_C"]     = tie_adr["PRN"].fillna("").str.strip().str.title()

# ── Base SQLite (simulation Vertica) ─────────────────────────
# connect(":memory:") : base en memoire (perdue quand Python s'arrete)
conn = sqlite3.connect(":memory:")
ctr.to_sql("CTR",         conn, if_exists="replace", index=False)
tie.to_sql("TIE",         conn, if_exists="replace", index=False)
tie_adr.to_sql("TIE_ADR", conn, if_exists="replace", index=False)
tie_x_ctr.to_sql("TIE_X_CTR", conn, if_exists="replace", index=False)
txn.to_sql("TXN",         conn, if_exists="replace", index=False)

print("Setup termine !")
print()
for nom, df in [("ctr",ctr),("tie",tie),("tie_adr",tie_adr),("tie_x_ctr",tie_x_ctr),("txn",txn)]:
    print(f"  {nom:12s}: {df.shape[0]:>5} lignes x {df.shape[1]} colonnes")"""),

# ============================================================
# SECTION 1 : CTE
# ============================================================
md("""---
# Section 1 — SQL Vertica Analytique

## 1.1 CTEs — Common Table Expressions

Un CTE est une **sous-requete nommee** qui simplifie la lecture.
C'est comme creer plusieurs tables temporaires intermediaires en SAS.

**Syntaxe :**
```sql
WITH
    cte_1 AS (SELECT ... FROM table WHERE ...),
    cte_2 AS (SELECT ... FROM cte_1 JOIN table2 ON ...)
SELECT * FROM cte_2
```

**Avantage :** le code est lisible, on peut debugger etape par etape.
**En SAS :** equivalent de plusieurs `CREATE TABLE AS SELECT`."""),

code("""# ── CTE simple : compter les transactions par contrat ────────
# Le CTE decompose la requete en 2 etapes nommees

sql_cte1 = '''
WITH
    -- Etape 1 : selectionner les contrats actifs
    contrats_actifs AS (
        SELECT
            IDT_AC,
            REF_CTR_INN,
            DAT_OUV_CTR,
            LIB_ECV,
            SLD_CTR
        FROM CTR
        WHERE CAT_ECV = "Actif"   -- filtrer sur les actifs
    ),

    -- Etape 2 : compter les transactions par contrat
    volumes AS (
        SELECT
            IDT_AC,
            COUNT(*)  AS nb_txn   -- compter les lignes
        FROM TXN
        GROUP BY IDT_AC           -- une ligne par contrat
    )

-- Requete finale : joindre les deux CTEs
SELECT
    ca.IDT_AC,
    ca.REF_CTR_INN,
    ca.LIB_ECV,
    ca.SLD_CTR,
    COALESCE(v.nb_txn, 0)  AS nb_txn  -- COALESCE = remplacer NULL par 0
FROM contrats_actifs ca
LEFT JOIN volumes v ON ca.IDT_AC = v.IDT_AC
ORDER BY nb_txn DESC
LIMIT 10
'''

# Executer la requete et recuperer un DataFrame
df_cte1 = pd.read_sql(sql_cte1, conn)

print("Top 10 contrats actifs par volume de transactions :")
print(df_cte1.to_string(index=False))"""),

code("""# ── CTE avec plusieurs etapes ────────────────────────────────
# 3 etapes : clients → contrats → agregation finale

sql_cte2 = '''
WITH
    -- Etape 1 : profil client (jointure TIE + TIE_ADR)
    profil_client AS (
        SELECT
            t.IDT_PI,
            t.COD_TYP_TIE,
            t.COD_LNG_CTR,
            a.NOM_TIE,
            a.PRN,
            a.NOM_VIL
        FROM TIE t
        LEFT JOIN TIE_ADR a ON t.IDT_PI = a.IDT_PI
    ),

    -- Etape 2 : contrats du client (via table de lien)
    contrats_client AS (
        SELECT
            lk.IDT_PI,
            lk.IDT_AC,
            lk.FLG_PRE_TTL,
            c.LIB_ECV,
            c.CAT_ECV,
            c.SLD_CTR
        FROM TIE_X_CTR lk
        JOIN CTR c ON lk.IDT_AC = c.IDT_AC
    ),

    -- Etape 3 : agregation : 1 ligne par client
    resume_client AS (
        SELECT
            IDT_PI,
            COUNT(*)          AS nb_contrats,
            SUM(SLD_CTR)      AS solde_total,
            SUM(CASE WHEN CAT_ECV = "Actif" THEN 1 ELSE 0 END) AS nb_actifs
        FROM contrats_client
        GROUP BY IDT_PI
    )

-- Resultat final
SELECT
    pc.NOM_TIE,
    pc.PRN,
    pc.NOM_VIL,
    rc.nb_contrats,
    rc.solde_total,
    rc.nb_actifs
FROM profil_client pc
JOIN resume_client rc ON pc.IDT_PI = rc.IDT_PI
ORDER BY solde_total DESC
LIMIT 8
'''

df_cte2 = pd.read_sql(sql_cte2, conn)
print("Resume par client (via CTE) :")
print(df_cte2.to_string(index=False))"""),

# ============================================================
# MINI-EXERCICE 1
# ============================================================
md("""---
### Mini-exercice 3.A — CTE pour le rapport

**Contexte :** Votre manager veut voir les **10 villes** avec le plus
de clients actifs (ayant au moins un contrat de statut 1, 2 ou 3).

**A faire :**
Ecrire une requete SQL avec un CTE en 2 etapes :
1. `clients_actifs` : selectionner les IDT_PI qui ont au moins un contrat actif
   (tables TIE_X_CTR + CTR, filtrer sur `CAT_ECV = "Actif"`)
2. Requete finale : joindre avec TIE_ADR pour avoir la ville,
   grouper par ville, compter, trier decroissant, limiter a 10"""),

code("""# ── Votre code ici ─────────────────────────────────────────
# Exercice 3.A

sql_villes = '''
WITH
    clients_actifs AS (
        SELECT DISTINCT lk.IDT_PI
        FROM TIE_X_CTR lk
        JOIN CTR c ON lk.IDT_AC = c.IDT_AC
        WHERE c.CAT_ECV = "Actif"
    )
SELECT
    a.NOM_VIL                  AS ville,
    COUNT(*)                   AS nb_clients_actifs
FROM clients_actifs ca
JOIN TIE_ADR a ON ca.IDT_PI = a.IDT_PI
WHERE a.NOM_VIL IS NOT NULL
GROUP BY a.NOM_VIL
ORDER BY nb_clients_actifs DESC
LIMIT 10
'''

# Executer
df_villes = pd.read_sql(sql_villes, conn)
print(df_villes.to_string(index=False))"""),

md("""**Correction exercice 3.A :**"""),

code("""# ── CORRECTION exercice 3.A ─────────────────────────────────

sql_villes_corrige = '''
WITH
    -- CTE : identifiants des clients ayant au moins un contrat actif
    clients_actifs AS (
        SELECT DISTINCT lk.IDT_PI     -- DISTINCT : eviter les doublons
        FROM TIE_X_CTR lk
        JOIN CTR c ON lk.IDT_AC = c.IDT_AC
        WHERE c.CAT_ECV = "Actif"    -- seulement les contrats actifs
    )

-- Requete finale : jointure avec les adresses + agregation par ville
SELECT
    a.NOM_VIL                        AS ville,
    COUNT(*)                         AS nb_clients_actifs,
    ROUND(COUNT(*) * 100.0 /
          (SELECT COUNT(*) FROM clients_actifs), 1)  AS pct
FROM clients_actifs ca
JOIN TIE_ADR a ON ca.IDT_PI = a.IDT_PI   -- jointure pour avoir la ville
WHERE a.NOM_VIL IS NOT NULL              -- exclure les villes manquantes
GROUP BY a.NOM_VIL                       -- 1 ligne par ville
ORDER BY nb_clients_actifs DESC          -- tri decroissant
LIMIT 10
'''

df_villes = pd.read_sql(sql_villes_corrige, conn)

print("Top 10 villes par nombre de clients actifs :")
print()
print(f"{'Ville':<20}  {'Nb clients':>10}  {'Part':>6}")
print("-" * 40)
for _, row in df_villes.iterrows():
    print(f"  {str(row['ville']):<18}  {row['nb_clients_actifs']:>10}  {row['pct']:>5.1f}%")"""),

# ============================================================
# SECTION 2 : OVER / PARTITION BY
# ============================================================
md("""---
## 1.2 Fonctions analytiques : OVER et PARTITION BY

C'est **la** fonction qui fait la difference en analyse bancaire.

`OVER (PARTITION BY col ORDER BY col2)` calcule une valeur **pour chaque ligne**
en tenant compte d'un groupe, sans reduire le nombre de lignes.

**En SAS :** equivalent de `RETAIN` et calculs avec `BY group`.

```sql
SELECT
    IDT_AC,
    DAT_CRE_MVT_CPB,
    COUNT(*) OVER (PARTITION BY IDT_AC)  -- total du compte pour CHAQUE ligne
FROM TXN;
```

| Fonction | Ce qu'elle calcule |
|----------|--------------------|
| `COUNT(*) OVER (PARTITION BY x)` | Total du groupe pour chaque ligne |
| `SUM(col) OVER (PARTITION BY x)` | Somme du groupe pour chaque ligne |
| `ROW_NUMBER() OVER (ORDER BY col)` | Rang unique (1, 2, 3...) |
| `RANK() OVER (ORDER BY col)` | Rang avec ex-aequo |
| `LAG(col,1) OVER (ORDER BY col)` | Valeur de la ligne precedente |
| `LEAD(col,1) OVER (ORDER BY col)` | Valeur de la ligne suivante |"""),

code("""# ── OVER + PARTITION BY en SQL ───────────────────────────────

sql_over = '''
SELECT
    IDT_AC,
    DAT_CRE_MVT_CPB,
    LIB_OPE_INL_1,
    -- Compter toutes les transactions du meme compte (pour chaque ligne)
    COUNT(*) OVER (PARTITION BY IDT_AC)        AS total_txn_du_compte,
    -- Compter au global (toutes transactions, toutes lignes)
    COUNT(*) OVER ()                            AS total_txn_global,
    -- Numerotation chronologique dans chaque compte (1er, 2eme, 3eme...)
    ROW_NUMBER() OVER (
        PARTITION BY IDT_AC           -- dans le groupe du compte
        ORDER BY DAT_CRE_MVT_CPB      -- tri chronologique
    )                                          AS rang_dans_compte
FROM TXN
ORDER BY IDT_AC, DAT_CRE_MVT_CPB
LIMIT 15
'''

df_over = pd.read_sql(sql_over, conn)

print("Fonctions OVER (15 premieres lignes) :")
print(df_over.to_string(index=False))"""),

code("""# ── Equivalent Pandas de OVER / PARTITION BY ─────────────────
# En Pandas, ces calculs se font avec .groupby() + .transform()
# .transform() applique la fonction PAR GROUPE et retourne le meme nb de lignes

# Tri prealable (equivalent ORDER BY)
txn_s = txn.sort_values(["IDT_AC", "DAT_TXN_DT"]).copy()

# COUNT(*) OVER (PARTITION BY IDT_AC)
# .transform("count") : taille du groupe, repetee pour chaque ligne du groupe
txn_s["total_txn_compte"] = (
    txn_s
    .groupby("IDT_AC")["IDT_AC"]  # grouper par compte
    .transform("count")            # compter les lignes du groupe
)

# ROW_NUMBER() OVER (PARTITION BY IDT_AC ORDER BY date)
# .cumcount() + 1 : incrementer un compteur dans chaque groupe
txn_s["rang_dans_compte"] = (
    txn_s
    .groupby("IDT_AC")            # grouper par compte
    .cumcount() + 1               # numetraoter a partir de 1
)

# Pourcentage de chaque transaction dans son compte
# 1 / total_txn * 100 = % de contribution
txn_s["pct_dans_compte"] = (1 / txn_s["total_txn_compte"] * 100).round(1)

# Afficher les 3 colonnes calculees
cols = ["IDT_AC", "DAT_TXN_DT", "total_txn_compte", "rang_dans_compte", "pct_dans_compte"]
print("Equivalents OVER avec Pandas :")
print(txn_s[cols].head(12).to_string(index=False))"""),

# ============================================================
# SECTION 3 : LAG ET LEAD
# ============================================================
md("""---
## 1.3 LAG et LEAD — naviguer d'une ligne a l'autre

`LAG(col, N)` : valeur de N lignes **AVANT** dans l'ordre
`LEAD(col, N)` : valeur de N lignes **APRES** dans l'ordre

**Cas d'usage bancaire :**
- Calculer l'ecart de temps entre deux transactions consecutives
- Detecter si un rejet suit un virement
- Calculer l'evolution d'un solde mois par mois

**Equivalent Pandas :** `.shift(1)` (lag) et `.shift(-1)` (lead)"""),

code("""# ── LAG en SQL ───────────────────────────────────────────────

sql_lag = '''
SELECT
    IDT_AC,
    DAT_CRE_MVT_CPB,
    LIB_OPE_INL_1,
    -- LAG : date de la transaction precedente du MEME compte
    LAG(DAT_CRE_MVT_CPB, 1) OVER (
        PARTITION BY IDT_AC          -- dans le groupe du compte
        ORDER BY DAT_CRE_MVT_CPB     -- ordre chronologique
    )                               AS date_txn_precedente
FROM TXN
ORDER BY IDT_AC, DAT_CRE_MVT_CPB
LIMIT 12
'''

df_lag = pd.read_sql(sql_lag, conn)
print("LAG en SQL :")
print(df_lag.to_string(index=False))"""),

code("""# ── LAG avec Pandas : .shift() ──────────────────────────────
# .shift(1)  : decaler d'une ligne vers le bas (= valeur precedente)
# .shift(-1) : decaler d'une ligne vers le haut (= valeur suivante)
# groupby garantit qu'on reste dans le meme groupe (compte)

txn_lag = txn.sort_values(["IDT_AC", "DAT_TXN_DT"]).copy()

# LAG(1) : date de la transaction precedente (dans le meme compte)
txn_lag["date_prec"] = (
    txn_lag
    .groupby("IDT_AC")["DAT_TXN_DT"]  # grouper par compte
    .shift(1)                           # decaler de 1 = valeur precedente
)

# LEAD(1) : date de la prochaine transaction (dans le meme compte)
txn_lag["date_suiv"] = (
    txn_lag
    .groupby("IDT_AC")["DAT_TXN_DT"]
    .shift(-1)                          # decaler de -1 = valeur suivante
)

# Calculer l'ecart en jours entre deux transactions consecutives
# soustraction de deux dates = Timedelta → .dt.days = nombre de jours
txn_lag["ecart_jours"] = (txn_lag["DAT_TXN_DT"] - txn_lag["date_prec"]).dt.days

print("Transactions avec LAG/LEAD :")
cols = ["IDT_AC", "DAT_TXN_DT", "date_prec", "date_suiv", "ecart_jours"]
print(txn_lag[cols].dropna(subset=["date_prec"]).head(10).to_string(index=False))"""),

code("""# ── Analyser les ecarts inter-transactions ───────────────────

ecarts = txn_lag["ecart_jours"].dropna()  # enlever les NaN (premiere txn de chaque compte)

print("Statistiques sur l'ecart entre transactions consecutives :")
print()
print(f"  Nombre de paires analysees : {len(ecarts):,}")
print(f"  Ecart moyen                : {ecarts.mean():.1f} jours")
print(f"  Ecart median               : {ecarts.median():.1f} jours")
print(f"  Ecart minimum              : {ecarts.min():.0f} jours")
print(f"  Ecart maximum              : {ecarts.max():.0f} jours")
print()

# Repartition par intervalles
bins = [0, 1, 7, 30, 90, 365, 9999]
labels = ["Meme jour", "1-6 jours", "1-4 sem.", "1-3 mois", "3-12 mois", "> 1 an"]
repartition_ecart = pd.cut(ecarts, bins=bins, labels=labels, right=False)
print("Repartition :")
for cat, nb in repartition_ecart.value_counts().sort_index().items():
    pct = nb / len(ecarts) * 100
    print(f"  {str(cat):<12}: {nb:>5,}  ({pct:.1f}%)")"""),

# ============================================================
# MINI-EXERCICE 2
# ============================================================
md("""---
### Mini-exercice 3.B — LAG pour la variation mensuelle

**Contexte :** Le rapport mensuel doit montrer l'evolution
du volume de transactions mois par mois (en nb et en %).

**A faire :**
1. Calculer le nombre de transactions par mois (`evol_mensuelle`)
2. Utiliser `.shift(1)` pour avoir le mois precedent (`nb_txn_mois_prec`)
3. Calculer la variation absolue et en %
4. Categoriser : "Hausse" si > 0%, "Baisse" si < 0%, "Stable" sinon
5. Afficher le tableau complet"""),

code("""# ── Votre code ici ─────────────────────────────────────────
# Exercice 3.B

# 1. Aggregation mensuelle
txn["MOIS"] = txn["DAT_TXN_DT"].dt.strftime("%Y-%m")
evol = (
    txn.dropna(subset=["MOIS"])
    .groupby("MOIS")
    .size()
    .reset_index(name="nb_txn")
    .sort_values("MOIS")
)

# 2. Colonne mois precedent avec shift(1)
evol["nb_mois_prec"] = evol["nb_txn"].shift(...)

# 3. Variation
evol["variation_abs"] = evol["nb_txn"] - evol["nb_mois_prec"]
evol["variation_pct"] = (evol["variation_abs"] / evol["nb_mois_prec"] * 100).round(1)

# 4. Tendance
evol["tendance"] = np.select(
    [evol["variation_pct"] > 0, evol["variation_pct"] < 0],
    ["Hausse", "Baisse"],
    default="Stable"
)

# 5. Affichage
print(evol.to_string(index=False))"""),

md("""**Correction exercice 3.B :**"""),

code("""# ── CORRECTION exercice 3.B ─────────────────────────────────

# 1. Aggregation mensuelle (recalcul)
txn["MOIS"] = txn["DAT_TXN_DT"].dt.strftime("%Y-%m")
evol = (
    txn.dropna(subset=["MOIS"])
    .groupby("MOIS")
    .size()
    .reset_index(name="nb_txn")
    .sort_values("MOIS")
    .reset_index(drop=True)  # remettre l'index a 0,1,2...
)

# 2. LAG : valeur du mois precedent
evol["nb_mois_prec"] = evol["nb_txn"].shift(1)  # shift(1) = decaler de 1 ligne

# 3. Variations
evol["variation_abs"] = evol["nb_txn"] - evol["nb_mois_prec"]
evol["variation_pct"] = (evol["variation_abs"] / evol["nb_mois_prec"] * 100).round(1)

# 4. Tendance avec np.select (plusieurs conditions)
conditions = [
    evol["variation_pct"] > 0,   # condition Hausse
    evol["variation_pct"] < 0,   # condition Baisse
]
choix = ["Hausse", "Baisse"]
evol["tendance"] = np.select(conditions, choix, default="Stable")

# 5. Affichage formate
print(f"{'Mois':>7}  {'N txn':>7}  {'Prec':>7}  {'Var abs':>8}  {'Var %':>7}  {'Tendance'}")
print("-" * 55)
for _, row in evol.iterrows():
    prec  = f"{int(row['nb_mois_prec']):>7,}" if pd.notna(row['nb_mois_prec']) else f"{'N/A':>7}"
    varab = f"{int(row['variation_abs']):>+8,}" if pd.notna(row['variation_abs']) else f"{'N/A':>8}"
    varpct= f"{row['variation_pct']:>+6.1f}%"   if pd.notna(row['variation_pct']) else f"{'N/A':>7}"
    print(f"  {row['MOIS']:>5}  {row['nb_txn']:>7,}  {prec}  {varab}  {varpct}  {row['tendance']}")"""),

# ============================================================
# SECTION 4 : DATES ET PERIODES
# ============================================================
md("""---
# Section 2 — Gestion des dates et periodes glissantes

## 2.1 Les deux formats de dates dans nos fichiers

| Table | Colonne | Format brut | Exemple |
|-------|---------|-------------|---------|
| CTR, TIE, TXN | dates | `YYYY-MM-DD` (ISO) | `2024-05-29` |
| TIE_ADR | DAT_MAJ_ADR | `DDMONYYYY` (SAS) | `24NOV2025` |

Le format SAS `DDMONYYYY` (ex: `24NOV2025`) est l'export natif SAS.
Python le comprend avec le code de format `%d%b%Y`."""),

code("""# ── Convertir le format SAS DDMONYYYY ───────────────────────
# Charger TIE_ADR sans conversion automatique
tie_adr_raw = pd.read_csv(DATA / "TIE_ADR.csv", sep=";", na_values=".", encoding="utf-8")

# Voir le format brut
print("Format brut de DAT_MAJ_ADR :")
print(tie_adr_raw["DAT_MAJ_ADR"].dropna().head(8).to_string())
print()

# Convertir avec le format %d%b%Y
# %d  = jour sur 2 chiffres (01-31)
# %b  = mois abrege en anglais (JAN, FEB, MAR, ...)
# %Y  = annee sur 4 chiffres
tie_adr["DAT_MAJ_DT"] = pd.to_datetime(
    tie_adr_raw["DAT_MAJ_ADR"],
    format   = "%d%b%Y",   # format SAS/anglais
    errors   = "coerce"    # mettre NaT si la conversion echoue
)

# Verifier la conversion
visu = pd.DataFrame({
    "format_brut"    : tie_adr_raw["DAT_MAJ_ADR"].head(5).values,
    "format_converti": tie_adr["DAT_MAJ_DT"].head(5).dt.strftime("%Y-%m-%d").values
})
print("Conversion DDMONYYYY → YYYY-MM-DD :")
print(visu.to_string(index=False))"""),

code("""# ── Fonctions de dates Python / Pandas ──────────────────────
# Equivalences avec les fonctions Vertica

# Date de test
date_test = pd.Timestamp("2024-08-15")

print(f"Date de reference : {date_test.date()}")
print()

# YEAR(), MONTH(), DAY() Vertica → .year, .month, .day Python
print(f"  Annee   (YEAR)      : {date_test.year}")
print(f"  Mois    (MONTH)     : {date_test.month}")
print(f"  Jour    (DAY)       : {date_test.day}")
print()

# DATE_TRUNC('month', date) → .to_period('M').to_timestamp()
# Premier jour du mois
premier_du_mois = date_test.to_period("M").to_timestamp()
print(f"  DATE_TRUNC (1er du mois) : {premier_du_mois.date()}")

# Dernier jour du mois
dernier_du_mois = date_test + pd.offsets.MonthEnd(0)
print(f"  LAST_DAY             : {dernier_du_mois.date()}")
print()

# ADD_MONTHS(date, n) → date + DateOffset(months=n)
print(f"  +1 mois  (ADD_MONTHS 1) : {(date_test + DateOffset(months=1)).date()}")
print(f"  +3 mois  (ADD_MONTHS 3) : {(date_test + DateOffset(months=3)).date()}")
print(f"  +13 mois (ADD_MONTHS 13): {(date_test + DateOffset(months=13)).date()}")
print()

# DATEDIFF('day', d1, d2) → (d2 - d1).days
date2 = pd.Timestamp("2025-01-01")
diff = (date2 - date_test).days
print(f"  DATEDIFF jours ({date_test.date()} → {date2.date()}): {diff} jours")"""),

code("""# ── Fenetre glissante de 13 mois ─────────────────────────────
# En analyse bancaire : on compare souvent N-12 mois au mois courant
# "13 mois" = le mois courant + les 12 mois precedents

# Date du jour (normalisee = minuit)
AUJOURD_HUI = pd.Timestamp.today().normalize()

# Debut de la fenetre : 13 mois en arriere
# DateOffset(months=13) = soustrait exactement 13 mois (gere les fins de mois)
DEBUT_13M = AUJOURD_HUI - DateOffset(months=13)

print(f"Fenetre d'analyse 13 mois :")
print(f"  De  : {DEBUT_13M.strftime('%Y-%m-%d')} ({DEBUT_13M.strftime('%B %Y')})")
print(f"  A   : {AUJOURD_HUI.strftime('%Y-%m-%d')} ({AUJOURD_HUI.strftime('%B %Y')})")
print(f"  Soit: {(AUJOURD_HUI - DEBUT_13M).days} jours")
print()

# Filtrer les transactions sur cette fenetre
txn_13m = txn[
    (txn["DAT_TXN_DT"] >= DEBUT_13M) &   # apres le debut de la fenetre
    (txn["DAT_TXN_DT"] <= AUJOURD_HUI)    # avant aujourd'hui
].copy()

print(f"Transactions total  : {len(txn):>6,}")
print(f"Transactions 13 mois: {len(txn_13m):>6,} ({len(txn_13m)/len(txn):.1%} du total)")"""),

code("""# ── Agregation par mois sur la fenetre 13 mois ───────────────

# Creer la colonne de mois (format YYYY-MM)
txn_13m["MOIS"] = txn_13m["DAT_TXN_DT"].dt.strftime("%Y-%m")

# Aggregation mensuelle sur la fenetre glissante
evol_13m = (
    txn_13m
    .groupby("MOIS")          # grouper par mois
    .agg(
        nb_txn     = ("NUM_ORD_MVT_CPB", "count"),   # nb transactions
        nb_comptes = ("IDT_AC",           "nunique"), # nb comptes distincts
    )
    .reset_index()
    .sort_values("MOIS")
)

# Ajouter la variation mensuelle (LAG)
evol_13m["nb_prec"]   = evol_13m["nb_txn"].shift(1)
evol_13m["var_pct"]   = ((evol_13m["nb_txn"] - evol_13m["nb_prec"]) / evol_13m["nb_prec"] * 100).round(1)

print("Evolution mensuelle sur fenetre 13 mois :")
print()
print(f"{'Mois':>7}  {'Transactions':>13}  {'Comptes':>8}  {'Var%':>7}")
print("-" * 40)
for _, row in evol_13m.iterrows():
    var = f"{row['var_pct']:>+6.1f}%" if pd.notna(row["var_pct"]) else "    N/A"
    print(f"  {row['MOIS']:>5}  {row['nb_txn']:>13,}  {row['nb_comptes']:>8,}  {var}")"""),

# ============================================================
# MINI-EXERCICE 3
# ============================================================
md("""---
### Mini-exercice 3.C — Calculer la duree des contrats

**Contexte :** Pour le rapport, vous devez calculer la duree de vie
de chaque contrat cloture, et les classer par tranche.

**A faire :**
1. Filtrer les contrats clotures (`DAT_CLO_DT` non nulle)
2. Calculer `DUREE_JOURS` = `DAT_CLO_DT` - `DAT_OUV_DT` en jours
3. Classer en tranches :
   - < 180 jours → "< 6 mois"
   - 180 a 730 jours → "6 mois - 2 ans"
   - > 730 jours → "> 2 ans"
4. Compter et afficher la repartition"""),

code("""# ── Votre code ici ─────────────────────────────────────────
# Exercice 3.C

# 1. Filtrer les clotures
ctr_clos = ctr[ctr["DAT_CLO_DT"].notna()].copy()

# 2. Duree en jours
ctr_clos["DUREE_JOURS"] = (ctr_clos["DAT_CLO_DT"] - ctr_clos["DAT_OUV_DT"]).dt.days

# 3. Tranches
ctr_clos["TRANCHE_DUREE"] = pd.cut(
    ctr_clos["DUREE_JOURS"],
    bins   = [0, 180, 730, 99999],
    labels = ["< 6 mois", "6 mois - 2 ans", "> 2 ans"],
    right  = False
)

# 4. Repartition
print(ctr_clos["TRANCHE_DUREE"].value_counts().sort_index())
print()
print(f"Duree moyenne : {ctr_clos['DUREE_JOURS'].mean():.0f} jours")"""),

md("""**Correction exercice 3.C :**"""),

code("""# ── CORRECTION exercice 3.C ─────────────────────────────────

# 1. Filtrer sur les contrats CLOTURES (DAT_CLO_DT non nulle)
#    .notna() : True si la valeur N'est PAS nulle
ctr_clos = ctr[ctr["DAT_CLO_DT"].notna()].copy()
print(f"Contrats clotures : {len(ctr_clos)}")

# 2. Calculer la duree
#    Soustraction de deux datetime → Timedelta
#    .dt.days → convertir Timedelta en entier (jours)
ctr_clos["DUREE_JOURS"] = (ctr_clos["DAT_CLO_DT"] - ctr_clos["DAT_OUV_DT"]).dt.days

# 3. Classer en tranches avec pd.cut
ctr_clos["TRANCHE_DUREE"] = pd.cut(
    ctr_clos["DUREE_JOURS"],            # la colonne a decouper
    bins   = [0, 180, 730, 99999],      # les bornes
    labels = ["< 6 mois", "6 mois - 2 ans", "> 2 ans"],  # les etiquettes
    right  = False                       # borne gauche incluse, droite exclue
)

# 4. Repartition
print()
repartition = ctr_clos["TRANCHE_DUREE"].value_counts().sort_index()
total = len(ctr_clos)

print(f"{'Tranche':<20}  {'N':>5}  {'%':>7}")
print("-" * 36)
for tranche, nb in repartition.items():
    pct = nb / total * 100
    print(f"  {str(tranche):<18}  {nb:>5}  {pct:>6.1f}%")
print("-" * 36)
print(f"  {'TOTAL':<18}  {total:>5}  {100.0:>6.1f}%")
print()
print(f"Duree moyenne      : {ctr_clos['DUREE_JOURS'].mean():.0f} jours")
print(f"Duree mediane      : {ctr_clos['DUREE_JOURS'].median():.0f} jours")
print(f"Duree minimum      : {ctr_clos['DUREE_JOURS'].min():.0f} jours")
print(f"Duree maximum      : {ctr_clos['DUREE_JOURS'].max():.0f} jours")"""),

# ============================================================
# SECTION 5 : VISUALISATION
# ============================================================
md("""---
# Section 3 — Visualisation avec Matplotlib

## 3.1 Structure d'un graphique Matplotlib

Tout graphique Matplotlib se structure en 3 etapes :
1. **Creer la figure** : `fig, ax = plt.subplots(figsize=(largeur, hauteur))`
2. **Tracer** : `ax.bar(x, y)` / `ax.plot(x, y)` / `ax.pie(...)`
3. **Configurer et afficher** : titres, labels, sauvegarde, `plt.show()`

```python
# Structure type (a copier-coller pour chaque graphique)
fig, ax = plt.subplots(figsize=(10, 5))  # 1. figure
ax.bar(x, y)                              # 2. tracer
ax.set_title("Mon titre")                 # 3. configurer
ax.set_xlabel("Axe X")
ax.set_ylabel("Axe Y")
plt.tight_layout()   # optimiser l'espacement automatiquement
plt.savefig("graphique.png", dpi=120)     # sauvegarder
plt.show()           # afficher dans Jupyter
```"""),

md("""## 3.2 Bar chart — graphique a barres (repartition des statuts)"""),

code("""# ── Bar chart : repartition des statuts de contrats ─────────

# Donnees
repartition = ctr["LIB_ECV"].value_counts()   # compter par statut
labels  = repartition.index.tolist()           # liste des libelles
valeurs = repartition.values                   # tableau des valeurs
total   = sum(valeurs)                         # total pour le %

# Couleurs selon la categorie du statut
couleurs = []
for lab in labels:
    if lab in ("Ouvert", "En attente", "Suspendu"):
        couleurs.append("#2ecc71")    # vert = actif
    elif lab == "Cloture":
        couleurs.append("#3498db")    # bleu = cloture
    else:
        couleurs.append("#e74c3c")    # rouge = resilie

# ── Creer la figure ──────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))  # 10 cm de large, 5 de haut

# ── Tracer les barres ────────────────────────────────────────
# ax.bar(positions_x, hauteurs_y, ...)
barres = ax.bar(
    labels,                  # axe X : les libelles
    valeurs,                 # axe Y : les hauteurs
    color      = couleurs,   # liste de couleurs
    edgecolor  = "white",    # bord blanc
    linewidth  = 0.8         # epaisseur du bord
)

# ── Ajouter les valeurs au-dessus de chaque barre ────────────
for barre, val in zip(barres, valeurs):
    pct = val / total * 100
    # ax.text(x, y, texte, ...)
    ax.text(
        barre.get_x() + barre.get_width() / 2,  # x = centre de la barre
        barre.get_height() + 0.3,                # y = dessus de la barre + 0.3
        f"{val}\n({pct:.1f}%)",                  # texte : nb + %
        ha         = "center",    # alignement horizontal centre
        va         = "bottom",    # alignement vertical bas
        fontsize   = 9,
        fontweight = "bold"
    )

# ── Configurer le graphique ──────────────────────────────────
ax.set_title("Repartition des contrats par statut - Beobank", pad=15)
ax.set_xlabel("Statut du contrat")
ax.set_ylabel("Nombre de contrats")
ax.set_ylim(0, max(valeurs) * 1.25)  # agrandir l'axe Y pour les etiquettes
ax.grid(axis="y", alpha=0.3, linestyle="--")  # grille horizontale discrete

# ── Sauvegarder et afficher ──────────────────────────────────
plt.tight_layout()  # eviter que les labels soient coupes
plt.savefig("bar_statuts.png", dpi=120, bbox_inches="tight")
plt.show()
print("Sauvegarde : bar_statuts.png")"""),

# ============================================================
# MINI-EXERCICE 4
# ============================================================
md("""---
### Mini-exercice 3.D — Bar chart des transactions par mois

**Contexte :** Reproduire le bar chart de l'evolution mensuelle
des transactions sur la fenetre 13 mois.

**A faire :**
1. Utiliser `evol_13m` (calcule avant)
2. Creer un bar chart avec les mois en X et `nb_txn` en Y
3. Ajouter une ligne horizontale pour la moyenne (`ax.axhline`)
4. Sauvegarder en `"bar_txn_mensuel.png"`

**Hint :** Pour avoir les mois en X, convertir l'index en numeros :
`x = range(len(evol_13m))`
puis `ax.set_xticks(list(x))` et `ax.set_xticklabels(evol_13m["MOIS"], rotation=45)`"""),

code("""# ── Votre code ici ─────────────────────────────────────────
# Exercice 3.D

# Positions numeriques pour l'axe X (Matplotlib prefere les numeros)
x = range(len(evol_13m))

fig, ax = plt.subplots(figsize=(12, 5))

# Tracer les barres
ax.bar(x, evol_13m["nb_txn"], color="#3498db", alpha=0.8)

# Ligne de moyenne
moyenne = evol_13m["nb_txn"].mean()
ax.axhline(y=moyenne, color="orange", linestyle="--", linewidth=1.5,
           label=f"Moyenne : {moyenne:.0f}")

# Configurer les axes X avec les mois
ax.set_xticks(list(x))
ax.set_xticklabels(evol_13m["MOIS"], rotation=45, ha="right")

# Titres et labels
ax.set_title("Transactions mensuelles (13 mois glissants)")
ax.set_xlabel("Mois")
ax.set_ylabel("Nombre de transactions")
ax.legend()
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("bar_txn_mensuel.png", dpi=120, bbox_inches="tight")
plt.show()
print("Sauvegarde : bar_txn_mensuel.png")"""),

md("""**Correction exercice 3.D :**"""),

code("""# ── CORRECTION exercice 3.D ─────────────────────────────────

# Positions X numeriques
x = range(len(evol_13m))

# Couleurs conditionnelles : vert si hausse vs mois prec, rouge sinon
couleurs_bar = []
for i, row in evol_13m.iterrows():
    if pd.isna(row["var_pct"]):
        couleurs_bar.append("#3498db")   # bleu = premier mois (pas de prec)
    elif row["var_pct"] >= 0:
        couleurs_bar.append("#2ecc71")   # vert = hausse
    else:
        couleurs_bar.append("#e74c3c")   # rouge = baisse

fig, ax = plt.subplots(figsize=(12, 5))

# ── Barres ───────────────────────────────────────────────────
barres = ax.bar(x, evol_13m["nb_txn"], color=couleurs_bar, edgecolor="white", linewidth=0.5)

# Valeurs au-dessus des barres
for barre, val in zip(barres, evol_13m["nb_txn"]):
    ax.text(
        barre.get_x() + barre.get_width() / 2,
        barre.get_height() + 0.5,
        str(val),
        ha="center", va="bottom", fontsize=7
    )

# ── Ligne de moyenne ─────────────────────────────────────────
# ax.axhline : tracer une ligne horizontale a une valeur y donnee
moyenne = evol_13m["nb_txn"].mean()
ax.axhline(
    y         = moyenne,      # position verticale
    color     = "orange",     # couleur
    linestyle = "--",         # style pointille
    linewidth = 1.5,          # epaisseur
    label     = f"Moyenne : {moyenne:.0f} txn/mois"  # etiquette de legende
)

# ── Axe X avec les mois ──────────────────────────────────────
ax.set_xticks(list(x))                              # position des ticks
ax.set_xticklabels(                                  # etiquettes des ticks
    evol_13m["MOIS"],
    rotation = 45,    # incliner de 45 degres pour lisibilite
    ha       = "right"  # aligner a droite apres rotation
)

# ── Configuration ─────────────────────────────────────────────
ax.set_title("Transactions mensuelles - Fenetre 13 mois glissants", pad=12)
ax.set_xlabel("Mois")
ax.set_ylabel("Nombre de transactions")
ax.legend(fontsize=9)
ax.grid(axis="y", alpha=0.3, linestyle="--")

import matplotlib.patches as mpatches
patch_h = mpatches.Patch(color="#2ecc71", label="Hausse vs mois prec.")
patch_b = mpatches.Patch(color="#e74c3c", label="Baisse vs mois prec.")
patch_n = mpatches.Patch(color="#3498db", label="1er mois")
ax.legend(handles=[patch_h, patch_b, patch_n,
                   plt.Line2D([0],[0], color="orange", linestyle="--", label=f"Moy: {moyenne:.0f}")],
          fontsize=8, loc="upper left")

plt.tight_layout()
plt.savefig("bar_txn_mensuel.png", dpi=120, bbox_inches="tight")
plt.show()
print("Sauvegarde : bar_txn_mensuel.png")"""),

md("""## 3.3 Line chart — graphique en ligne"""),

code("""# ── Line chart : evolution avec double axe Y ─────────────────
# Deux series sur le meme graphique avec des echelles differentes
# ax1 = axe Y gauche (transactions) → barres
# ax2 = axe Y droit (comptes actifs) → ligne

# Donnees
x = range(len(evol_13m))

fig, ax1 = plt.subplots(figsize=(12, 5))

# ── Axe 1 (gauche) : barres de transactions ───────────────────
# couleur #3498db pour les barres
ax1.bar(x, evol_13m["nb_txn"],
        color="steelblue", alpha=0.5, label="Transactions")
ax1.set_ylabel("Nombre de transactions", color="steelblue")  # label axe Y gauche
ax1.tick_params(axis="y", labelcolor="steelblue")            # couleur des ticks

# ── Axe 2 (droit) : ligne des comptes actifs ─────────────────
# ax1.twinx() cree un DEUXIEME axe Y partageant le meme axe X
ax2 = ax1.twinx()
ax2.plot(
    x,                         # axe X
    evol_13m["nb_comptes"],    # axe Y
    color     = "#e74c3c",     # rouge
    marker    = "o",           # cercles aux points de donnees
    linewidth = 2,             # epaisseur de la ligne
    markersize= 5,             # taille des cercles
    label     = "Comptes actifs"
)
ax2.set_ylabel("Comptes actifs", color="#e74c3c")       # label axe Y droit
ax2.tick_params(axis="y", labelcolor="#e74c3c")         # couleur des ticks

# ── Axe X commun ─────────────────────────────────────────────
ax1.set_xticks(list(x))
ax1.set_xticklabels(evol_13m["MOIS"], rotation=45, ha="right", fontsize=8)

# ── Titre et grille ───────────────────────────────────────────
ax1.set_title("Evolution mensuelle : transactions et comptes actifs")
ax1.grid(axis="y", alpha=0.3, linestyle="--")

# ── Legendes combinées ────────────────────────────────────────
# Fusionner les legendes des deux axes
l1, lab1 = ax1.get_legend_handles_labels()
l2, lab2 = ax2.get_legend_handles_labels()
ax1.legend(l1 + l2, lab1 + lab2, loc="upper left", fontsize=9)

plt.tight_layout()
plt.savefig("line_evolution.png", dpi=120, bbox_inches="tight")
plt.show()
print("Sauvegarde : line_evolution.png")"""),

md("""## 3.4 Pie chart — graphique circulaire"""),

code("""# ── Pie chart : profil des clients ──────────────────────────
# subplots(1, 2) : 1 ligne, 2 colonnes = 2 graphiques cote a cote

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
# axes[0] = graphique gauche
# axes[1] = graphique droit

# ── Graphique gauche : type de tiers ─────────────────────────
repartition_type = tie["COD_TYP_TIE"].value_counts()
labels_type = [{"1":"Personnes physiques","2":"Personnes morales"}.get(k,k)
               for k in repartition_type.index]

# ax.pie(...) : tracer un graphique en camembert
wedges1, texts1, autotexts1 = axes[0].pie(
    repartition_type.values,     # les valeurs (tailles des parts)
    labels     = labels_type,    # etiquettes des parts
    autopct    = "%1.1f%%",      # format du % (1 decimale)
    colors     = ["#3498db", "#e67e22"],   # couleurs
    startangle = 90,             # angle de depart (12h00)
    explode    = [0.04, 0.04],   # "exploser" les parts de 4%
    textprops  = {"fontsize": 10}
)
for at in autotexts1:
    at.set_fontweight("bold")   # mettre les % en gras

axes[0].set_title("Type de clients")

# ── Graphique droit : langue de communication ─────────────────
repartition_lng = tie["COD_LNG_CTR"].value_counts(dropna=False)
labels_lng = [{"FR":"Francais","NL":"Neerlandais"}.get(str(k),str(k))
              for k in repartition_lng.index]

wedges2, texts2, autotexts2 = axes[1].pie(
    repartition_lng.values,
    labels     = labels_lng,
    autopct    = "%1.1f%%",
    colors     = ["#2ecc71", "#9b59b6", "#95a5a6"],
    startangle = 90,
    explode    = [0.04] * len(labels_lng),
    textprops  = {"fontsize": 10}
)
for at in autotexts2:
    at.set_fontweight("bold")

axes[1].set_title("Langue de communication")

# ── Titre general ─────────────────────────────────────────────
# fig.suptitle : titre global de la figure (au-dessus des deux graphiques)
fig.suptitle("Profil des clients Beobank", fontsize=13, fontweight="bold", y=1.02)

plt.tight_layout()
plt.savefig("pie_clients.png", dpi=120, bbox_inches="tight")
plt.show()
print("Sauvegarde : pie_clients.png")"""),

# ============================================================
# MINI-EXERCICE 5
# ============================================================
md("""---
### Mini-exercice 3.E — Graphique des tranches d'age

**Contexte :** Visualiser la repartition des clients par tranche d'age
avec un **bar chart horizontal** (barh).

**A faire :**
1. Calculer `repartition_age = tie["TRANCHE_AGE"].value_counts().sort_index()`
2. Creer un bar chart horizontal avec `ax.barh(categories, valeurs)`
3. Ajouter les valeurs a droite de chaque barre avec `ax.text()`
4. Configurer le titre, les labels et la grille
5. Sauvegarder en `"barh_age.png"`"""),

code("""# ── Votre code ici ─────────────────────────────────────────
# Exercice 3.E

# Donnees
repartition_age = tie["TRANCHE_AGE"].value_counts().sort_index()
categories = repartition_age.index.astype(str).tolist()
valeurs    = repartition_age.values

fig, ax = plt.subplots(figsize=(9, 5))

# Tracer les barres horizontales
ax.barh(categories, valeurs, color="#9b59b6", edgecolor="white")

# Valeurs a droite de chaque barre
for i, val in enumerate(valeurs):
    ax.text(val + 0.2, i, str(val), va="center", fontsize=10)

ax.set_title("Repartition des clients par tranche d'age")
ax.set_xlabel("Nombre de clients")
ax.grid(axis="x", alpha=0.3)

plt.tight_layout()
plt.savefig("barh_age.png", dpi=120, bbox_inches="tight")
plt.show()
print("Sauvegarde : barh_age.png")"""),

md("""**Correction exercice 3.E :**"""),

code("""# ── CORRECTION exercice 3.E ─────────────────────────────────

# Donnees : compter et trier par ordre de tranche
repartition_age = tie["TRANCHE_AGE"].value_counts().sort_index()
categories = repartition_age.index.astype(str).tolist()
valeurs    = repartition_age.values
total      = sum(valeurs)

fig, ax = plt.subplots(figsize=(9, 5))

# ── Barres horizontales ───────────────────────────────────────
# ax.barh(categories_y, valeurs_x) : inverse de ax.bar
barres = ax.barh(
    categories,              # axe Y = les categories
    valeurs,                 # axe X = les valeurs (longueur des barres)
    color     = "#9b59b6",  # violet
    edgecolor = "white",
    linewidth = 0.5
)

# ── Valeurs et % a droite de chaque barre ────────────────────
for i, (barre, val) in enumerate(zip(barres, valeurs)):
    pct = val / total * 100
    # ax.text(x, y, texte) : x = apres la barre, y = centre de la barre
    ax.text(
        barre.get_width() + 0.1,                       # x : juste apres la barre
        barre.get_y() + barre.get_height() / 2,        # y : centre vertical
        f"{val}  ({pct:.1f}%)",                        # texte
        va = "center",  # aligner verticalement au centre
        fontsize = 9
    )

# ── Configuration ─────────────────────────────────────────────
ax.set_title("Repartition des clients par tranche d'age", pad=12)
ax.set_xlabel("Nombre de clients")
ax.set_ylabel("Tranche d'age")
ax.set_xlim(0, max(valeurs) * 1.35)  # agrandir pour les etiquettes
ax.grid(axis="x", alpha=0.3, linestyle="--")

plt.tight_layout()
plt.savefig("barh_age.png", dpi=120, bbox_inches="tight")
plt.show()
print("Sauvegarde : barh_age.png")"""),

md("""## 3.5 Tableau de bord : GridSpec (plusieurs graphiques)"""),

code("""# ── Dashboard 4 graphiques avec GridSpec ─────────────────────
# GridSpec permet un controle precis de la disposition des graphiques
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(15, 10))

# Creer une grille 2 lignes x 3 colonnes
gs = GridSpec(2, 3, figure=fig, hspace=0.5, wspace=0.4)
# hspace : espace vertical entre les graphiques
# wspace : espace horizontal entre les graphiques

# ── G1 : haut gauche - Pie statuts ───────────────────────────
ax1 = fig.add_subplot(gs[0, 0])  # ligne 0, colonne 0
r_ecv = ctr["LIB_ECV"].value_counts()
col_ecv = ["#2ecc71","#f1c40f","#f39c12","#3498db","#e67e22","#e74c3c"]
ax1.pie(r_ecv.values, labels=r_ecv.index, autopct="%1.0f%%",
        colors=col_ecv[:len(r_ecv)], startangle=90, textprops={"fontsize":7})
ax1.set_title("Statuts des contrats", fontsize=10)

# ── G2 : haut milieu - Bar type clients ───────────────────────
ax2 = fig.add_subplot(gs[0, 1])  # ligne 0, colonne 1
r_typ = tie["COD_TYP_TIE"].value_counts()
lbls_typ = [{"1":"PP","2":"PM"}.get(k,k) for k in r_typ.index]
ax2.bar(lbls_typ, r_typ.values, color=["#3498db","#e67e22"], edgecolor="white")
for b, v in zip(ax2.patches, r_typ.values):
    ax2.text(b.get_x()+b.get_width()/2, b.get_height()+0.3, str(v), ha="center", fontsize=9)
ax2.set_title("Type de clients", fontsize=10)
ax2.set_ylabel("Effectif")
ax2.grid(axis="y", alpha=0.3)

# ── G3 : haut droit - Barh tranches age ───────────────────────
ax3 = fig.add_subplot(gs[0, 2])  # ligne 0, colonne 2
r_age = tie["TRANCHE_AGE"].value_counts().sort_index()
ax3.barh(r_age.index.astype(str), r_age.values, color="#9b59b6", edgecolor="white")
ax3.set_title("Tranche d'age (PP)", fontsize=10)
ax3.grid(axis="x", alpha=0.3)

# ── G4 : bas, toute la largeur - Evolution mensuelle ──────────
ax4 = fig.add_subplot(gs[1, :])  # ligne 1, toutes les colonnes (0 a 2)
x = range(len(evol_13m))
ax4.bar(x, evol_13m["nb_txn"], color="steelblue", alpha=0.7, label="Transactions")
ax4.plot(x, evol_13m["nb_txn"], "o-", color="#e74c3c", linewidth=1.5, markersize=4)
ax4.axhline(evol_13m["nb_txn"].mean(), color="orange", linestyle="--",
            linewidth=1.2, label=f"Moy: {evol_13m['nb_txn'].mean():.0f}")
ax4.set_xticks(list(x))
ax4.set_xticklabels(evol_13m["MOIS"], rotation=45, ha="right", fontsize=7)
ax4.set_title("Transactions mensuelles - 13 mois glissants", fontsize=10)
ax4.set_ylabel("Nb transactions")
ax4.legend(fontsize=8)
ax4.grid(axis="y", alpha=0.3)

# ── Titre global ──────────────────────────────────────────────
fig.suptitle("Tableau de bord Beobank", fontsize=15, fontweight="bold")

plt.savefig("dashboard_beobank.png", dpi=120, bbox_inches="tight")
plt.show()
print("Sauvegarde : dashboard_beobank.png")"""),

# ============================================================
# SECTION 6 : MINI-PROJET
# ============================================================
md("""---
# Section 4 — Mini-projet final : Pipeline complet

## Objectif

Vous allez maintenant executer le pipeline complet qui produit
le rapport mensuel Beobank de bout en bout.

```
CHARGEMENT          → 5 tables CSV
PREPARATION         → conversions, colonnes derivees
VUE ANALYTIQUE      → jointure des 5 tables
INDICATEURS         → agregations, statistiques
VISUALISATIONS      → 4 graphiques
RAPPORT TEXTUEL     → chiffres cles
EXPORTS             → CSV + JSON + PNG
```

**Executez les 5 cellules dans l'ordre.**"""),

code("""# ── PIPELINE ETAPE 1 : CHARGEMENT ET PREPARATION ─────────────
print("ETAPE 1 : Chargement et preparation")
print("=" * 50)

AUJOURD_HUI = pd.Timestamp.today().normalize()
DEBUT_13M   = AUJOURD_HUI - DateOffset(months=13)
print(f"Fenetre d'analyse : {DEBUT_13M.date()} → {AUJOURD_HUI.date()}")
print()

# Recharger proprement
ctr       = pd.read_csv(DATA / "CTR.csv",       **PARAMS)
tie       = pd.read_csv(DATA / "TIE.csv",       **PARAMS)
tie_adr   = pd.read_csv(DATA / "TIE_ADR.csv",   **PARAMS)
tie_x_ctr = pd.read_csv(DATA / "TIE_X_CTR.csv", **PARAMS)
txn       = pd.read_csv(DATA / "TXN_X_CTR.csv", **PARAMS)

# Conversions CTR
ctr["DAT_OUV_DT"] = pd.to_datetime(ctr["DAT_OUV_CTR"], errors="coerce")
ctr["DAT_CLO_DT"] = pd.to_datetime(ctr["DAT_CLO_CTR"], errors="coerce")
ctr["LIB_ECV"] = ctr["COD_ECV_CTR"].map({
    "1":"Ouvert","2":"En attente","3":"Suspendu",
    "4":"Cloture","5":"En resiliation","6":"Resilie"
}).fillna("Inconnu")
ctr["CAT_ECV"] = ctr["COD_ECV_CTR"].map({
    "1":"Actif","2":"Actif","3":"Actif",
    "4":"Inactif","5":"Inactif","6":"Inactif"
}).fillna("Inconnu")
ctr["SEGMENT"] = np.select(
    [ctr["SLD_CTR"].isna(), ctr["SLD_CTR"]<2000,
     (ctr["SLD_CTR"]>=2000)&(ctr["SLD_CTR"]<15000), ctr["SLD_CTR"]>=15000],
    ["Inconnu","Standard","Confort","Premium"], default="Inconnu"
)

# Conversions TIE
tie["DAT_NAI_DT"] = pd.to_datetime(tie["DAT_NAI"], errors="coerce")
tie["AGE"] = ((AUJOURD_HUI - tie["DAT_NAI_DT"]).dt.days / 365.25).round(0).astype("Int64")
tie["TRANCHE_AGE"] = pd.cut(
    tie["AGE"].astype(float),
    bins=[0,25,35,50,65,120],
    labels=["<25 ans","25-34 ans","35-49 ans","50-64 ans","65+ ans"],
    right=False
).astype(str)

# Nettoyage adresses
tie_adr["NOM_TIE_C"] = tie_adr["NOM_TIE"].fillna("").str.strip().str.upper()
tie_adr["PRN_C"]     = tie_adr["PRN"].fillna("").str.strip().str.title()

# Conversions TXN
txn["DAT_TXN_DT"] = pd.to_datetime(txn["DAT_CRE_MVT_CPB"], errors="coerce")
txn["MOIS"]       = txn["DAT_TXN_DT"].dt.strftime("%Y-%m")

print(f"  CTR       : {len(ctr):>5} lignes")
print(f"  TIE       : {len(tie):>5} lignes")
print(f"  TIE_ADR   : {len(tie_adr):>5} lignes")
print(f"  TIE_X_CTR : {len(tie_x_ctr):>5} lignes")
print(f"  TXN       : {len(txn):>5} lignes")
print()
print("ETAPE 1 terminee")"""),

code("""# ── PIPELINE ETAPE 2 : VUE ANALYTIQUE ────────────────────────
print("ETAPE 2 : Construction de la vue analytique")
print("=" * 50)

# Stats transactions par compte
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

# Stats 13 mois
txn_13m = txn[(txn["DAT_TXN_DT"] >= DEBUT_13M) & (txn["DAT_TXN_DT"] <= AUJOURD_HUI)]
stats_13m = (
    txn_13m
    .groupby("IDT_AC")
    .agg(nb_txn_13m = ("NUM_ORD_MVT_CPB", "count"))
    .reset_index()
)

# Jointures successives
vue = (
    tie_x_ctr[["IDT_PI","IDT_AC","FLG_PRE_TTL"]]
    .merge(tie[["IDT_PI","COD_TYP_TIE","COD_LNG_CTR","COD_SEX","AGE","TRANCHE_AGE"]], on="IDT_PI", how="left")
    .merge(tie_adr[["IDT_PI","NOM_TIE_C","PRN_C","NOM_VIL","COD_PST","COD_PAY_ISO"]], on="IDT_PI", how="left")
    .merge(ctr[["IDT_AC","REF_CTR_INN","DAT_OUV_CTR","LIB_ECV","CAT_ECV","COD_DEV","SLD_CTR","SEGMENT"]], on="IDT_AC", how="left")
    .merge(stats_txn, on="IDT_AC", how="left")
    .merge(stats_13m, on="IDT_AC", how="left")
)
vue["nb_txn_total"] = vue["nb_txn_total"].fillna(0).astype(int)
vue["nb_txn_13m"]   = vue["nb_txn_13m"].fillna(0).astype(int)

print(f"  Vue analytique : {len(vue):,} lignes x {vue.shape[1]} colonnes")
print()
print("ETAPE 2 terminee")"""),

code("""# ── PIPELINE ETAPE 3 : INDICATEURS CLES ─────────────────────
print("ETAPE 3 : Calcul des indicateurs")
print("=" * 50)

# Evolution mensuelle 13 mois
evol_13m = (
    txn_13m
    .groupby("MOIS")
    .agg(
        nb_txn     = ("NUM_ORD_MVT_CPB", "count"),
        nb_comptes = ("IDT_AC",           "nunique"),
    )
    .reset_index()
    .sort_values("MOIS")
)
evol_13m["nb_prec"] = evol_13m["nb_txn"].shift(1)
evol_13m["var_pct"] = ((evol_13m["nb_txn"] - evol_13m["nb_prec"]) / evol_13m["nb_prec"] * 100).round(1)

print()
print("=" * 60)
print("  RAPPORT D'ACTIVITE BEOBANK")
print(f"  Au {AUJOURD_HUI.strftime('%d/%m/%Y')}")
print("=" * 60)
print()
print("  A. PORTEFEUILLE CONTRATS")
print(f"     Total         : {len(ctr):>6,}")
print(f"     Actifs        : {(ctr['CAT_ECV']=='Actif').sum():>6,}  ({(ctr['CAT_ECV']=='Actif').mean():.1%})")
print(f"     Inactifs      : {(ctr['CAT_ECV']=='Inactif').sum():>6,}  ({(ctr['CAT_ECV']=='Inactif').mean():.1%})")
print()
print("  B. CLIENTS")
print(f"     Total         : {len(tie):>6,}")
print(f"     Age moyen     : {tie['AGE'].mean():.1f} ans")
print()
print("  C. ACTIVITE 13 MOIS")
print(f"     Transactions  : {len(txn_13m):>6,}")
print(f"     Comptes actifs: {txn_13m['IDT_AC'].nunique():>6,}")
if len(evol_13m) > 0:
    max_m = evol_13m.loc[evol_13m["nb_txn"].idxmax()]
    print(f"     Mois record   : {max_m['MOIS']} ({max_m['nb_txn']:,} txn)")
print()
print("ETAPE 3 terminee")"""),

code("""# ── PIPELINE ETAPE 4 : VISUALISATIONS ───────────────────────
print("ETAPE 4 : Generation des visualisations")

fig = plt.figure(figsize=(16, 10))
fig.suptitle(f"Rapport Beobank - {AUJOURD_HUI.strftime('%d/%m/%Y')}",
             fontsize=14, fontweight="bold")

from matplotlib.gridspec import GridSpec
gs = GridSpec(2, 3, figure=fig, hspace=0.5, wspace=0.4)

# G1 : Pie statuts
ax1 = fig.add_subplot(gs[0, 0])
r = ctr["LIB_ECV"].value_counts()
c = ["#2ecc71","#f1c40f","#f39c12","#3498db","#e67e22","#e74c3c"]
ax1.pie(r.values, labels=r.index, autopct="%1.0f%%",
        colors=c[:len(r)], startangle=90, textprops={"fontsize":7})
ax1.set_title("Statuts contrats")

# G2 : Bar segments
ax2 = fig.add_subplot(gs[0, 1])
seg = ctr["SEGMENT"].value_counts()
ax2.bar(seg.index, seg.values, color=["#3498db","#2ecc71","#f39c12","#95a5a6"], edgecolor="w")
for b,v in zip(ax2.patches, seg.values):
    ax2.text(b.get_x()+b.get_width()/2, b.get_height()+0.2, str(v), ha="center", fontsize=8)
ax2.set_title("Segments clients")
ax2.grid(axis="y", alpha=0.3)

# G3 : Barh tranches age
ax3 = fig.add_subplot(gs[0, 2])
ra = tie["TRANCHE_AGE"].value_counts().sort_index()
ax3.barh(ra.index.astype(str), ra.values, color="#9b59b6", edgecolor="w")
for i,v in enumerate(ra.values):
    ax3.text(v+0.1, i, str(v), va="center", fontsize=8)
ax3.set_title("Tranche d'age")
ax3.grid(axis="x", alpha=0.3)

# G4 : Evolution 13 mois (toute la ligne du bas)
ax4 = fig.add_subplot(gs[1, :])
x4 = range(len(evol_13m))
ax4.bar(x4, evol_13m["nb_txn"], color="steelblue", alpha=0.7)
ax4.plot(x4, evol_13m["nb_txn"], "o-", color="#e74c3c", lw=1.5, ms=4)
ax4.axhline(evol_13m["nb_txn"].mean(), color="orange", ls="--", lw=1.2,
            label=f"Moy: {evol_13m['nb_txn'].mean():.0f}")
ax4.set_xticks(list(x4))
ax4.set_xticklabels(evol_13m["MOIS"], rotation=45, ha="right", fontsize=7)
ax4.set_title("Transactions mensuelles - 13 mois glissants")
ax4.legend(fontsize=8)
ax4.grid(axis="y", alpha=0.3)

plt.savefig("rapport_final_beobank.png", dpi=120, bbox_inches="tight")
plt.show()
print("Sauvegarde : rapport_final_beobank.png")
print()
print("ETAPE 4 terminee")"""),

code("""# ── PIPELINE ETAPE 5 : EXPORTS ────────────────────────────────
print("ETAPE 5 : Exports")
print("=" * 50)
import json as json_mod

# Export 1 : vue analytique
for col in ["premiere_txn","derniere_txn"]:
    if col in vue.columns:
        vue[col] = pd.to_datetime(vue[col]).dt.strftime("%Y-%m-%d")
for col in vue.select_dtypes(include=["category"]).columns:
    vue[col] = vue[col].astype(str)
for col in vue.select_dtypes(include=["Int64"]).columns:
    vue[col] = vue[col].astype(object)

vue.to_csv("rapport_vue_analytique.csv", sep=";", index=False, encoding="utf-8")
print(f"  Export 1 : rapport_vue_analytique.csv ({len(vue):,} lignes)")

# Export 2 : evolution mensuelle
evol_13m.to_csv("rapport_evolution_mensuelle.csv", sep=";", index=False, encoding="utf-8")
print(f"  Export 2 : rapport_evolution_mensuelle.csv ({len(evol_13m)} mois)")

# Export 3 : indicateurs JSON
indicateurs = {
    "date_rapport"         : AUJOURD_HUI.strftime("%Y-%m-%d"),
    "periode_debut"        : DEBUT_13M.strftime("%Y-%m-%d"),
    "periode_fin"          : AUJOURD_HUI.strftime("%Y-%m-%d"),
    "nb_contrats"          : int(len(ctr)),
    "nb_contrats_actifs"   : int((ctr["CAT_ECV"]=="Actif").sum()),
    "nb_clients"           : int(len(tie)),
    "age_moyen"            : round(float(tie["AGE"].mean()), 1),
    "nb_txn_13m"           : int(len(txn_13m)),
    "nb_comptes_actifs_13m": int(txn_13m["IDT_AC"].nunique()),
}
with open("rapport_indicateurs.json", "w", encoding="utf-8") as f:
    json_mod.dump(indicateurs, f, ensure_ascii=False, indent=2)
print(f"  Export 3 : rapport_indicateurs.json")

print()
print("=" * 60)
print("  PIPELINE COMPLET TERMINE !")
print()
print("  Fichiers produits :")
print("    - rapport_vue_analytique.csv")
print("    - rapport_evolution_mensuelle.csv")
print("    - rapport_indicateurs.json")
print("    - rapport_final_beobank.png")
print()
print("  Competences mobilisees sur 3 jours :")
print("    Jour 1 : Python de base (variables, boucles, fonctions)")
print("    Jour 2 : Pandas (chargement, filtres, groupby, jointures, exports)")
print("    Jour 3 : SQL, LAG/LEAD, dates, 13 mois, Matplotlib")
print("=" * 60)"""),

# ============================================================
# SYNTHESE FINALE
# ============================================================
md("""---
# Synthese generale de la formation

## Tableau de correspondances SAS → Python (complet)

| SAS | Python |
|-----|--------|
| `proc import; infile dlm=';'` | `pd.read_csv(sep=';', na_values='.')` |
| `proc print (obs=10)` | `df.head(10)` |
| `proc contents` | `df.info()` |
| `proc means` | `df.describe()` |
| `proc freq` | `df["col"].value_counts()` |
| `proc sort by col` | `df.sort_values("col")` |
| `where col = "1"` | `df[df["col"] == "1"]` |
| `where col in ("1","2")` | `df[df["col"].isin(["1","2"])]` |
| `proc summary / means by group` | `df.groupby("col").agg(...)` |
| Data step : variable calculee | `df["new"] = expression` |
| `if x then y = "A"; else y = "B"` | `np.where(cond, "A", "B")` |
| Format SAS | dictionnaire + `.map()` |
| `proc sql left join` | `df.merge(..., how="left")` |
| `LAG(var)` | `.shift(1)` sur groupby |
| `intck('month', d1, d2)` | `(d2 - d1).dt.days / 30.44` |
| `intnx('month', date, 1)` | `date + DateOffset(months=1)` |
| `datepart()` → `year()` | `.dt.year` |
| `put(date, yymmn6.)` | `.dt.strftime("%Y-%m")` |
| `proc gplot` / `proc sgplot` | `matplotlib.pyplot` |
| `proc export` | `df.to_csv(sep=';')` |
| `%macro / %mend` | `def ma_fonction(): ...` |

## Exercices realises sur 3 jours

| Jour | Exercice | Sujet |
|------|----------|-------|
| **1** | 1.A | Variables et calcul de solde |
| **1** | 1.B | Classifier les statuts de contrat |
| **1** | 1.C | Boucle sur des contrats |
| **1** | 1.D | Analyser des soldes avec list comprehension |
| **1** | 1.E | Mapping des codes en libelles |
| **1** | 1.F | Fonctions de classification et eligibilite |
| **1** | 1.G | Nettoyage de donnees brutes |
| **1** | Final | Rapport d'inventaire complet CTR.csv |
| **2** | 2.A | Explorer TIE.csv |
| **2** | 2.B | Filtrer les contrats du rapport |
| **2** | 2.C | Colonnes calculees (duree, anciennete, devise) |
| **2** | 2.D | Rapport mensuel de transactions |
| **2** | 2.E | Jointure 3 tables |
| **2** | 2.F | Export CSV et JSON |
| **2** | 2.G | Requete SQL sur les transactions |
| **2** | Final | Vue analytique 5 tables |
| **3** | 3.A | CTE : top 10 villes par clients actifs |
| **3** | 3.B | LAG : variation mensuelle des transactions |
| **3** | 3.C | Duree des contrats clotures |
| **3** | 3.D | Bar chart transactions mensuelles |
| **3** | 3.E | Bar chart horizontal tranches d'age |
| **3** | Final | Pipeline complet bout-en-bout |

## Pour continuer apres la formation

- **Documentation officielle Pandas** : pandas.pydata.org/docs
- **Documentation Matplotlib** : matplotlib.org/stable/gallery
- **Exercices en ligne** : kaggle.com/learn/pandas (gratuit)
- **Vertica Python driver** : pip install vertica-python, docs.vertica.com"""),

]  # fin j3

path = os.path.join(OUTPUT_DIR, "Jour3_SQL_TimeSeries_Visualisation.ipynb")
with open(path, "w", encoding="utf-8") as f:
    json.dump(notebook(j3), f, ensure_ascii=False, indent=1)
print(f"Jour 3 v2 cree : {os.path.getsize(path)//1024} Ko — {len(j3)} cellules")
