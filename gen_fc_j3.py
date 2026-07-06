"""
Formation Complete - Jour 3 - SQL Analytique, Time Series et Visualisation
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
md("""# Jour 3 · SQL Analytique, Time Series et Visualisation
### Formation Python 3 jours · 20 novembre 2026

---

## Objectifs du Jour 3

Aujourd'hui vous complétez votre arsenal Python pour l'analyse bancaire :

1. **SQL Analytique** (CTEs, Window Functions) — pour des analyses complexes en SQL
2. **Time Series** — manipulation de dates, fenêtres glissantes, agrégations temporelles
3. **Matplotlib** — créer des graphiques pour vos rapports
4. **Mini-projet pipeline complet** — de l'import au graphique en 5 étapes

## Rappel des tables disponibles

Les 5 tables Beobank chargées hier sont réutilisées aujourd'hui.
La cellule de setup ci-dessous les recharge toutes."""),

# ════════════════════════════════════════════════════════
# CELLULE SETUP
# ════════════════════════════════════════════════════════
code("""# ── SETUP — Charger toutes les tables et créer SQLite ────────
# Cette cellule doit être exécutée EN PREMIER à chaque session
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path
from datetime import date

# ── Paramètres de chargement ─────────────────────────────────
DATA   = Path("../Orsys")
PARAMS = dict(sep=";", na_values=".", encoding="utf-8")

# ── Charger les 5 tables ─────────────────────────────────────
ctr     = pd.read_csv(DATA / "CTR.csv",       **PARAMS)
tie     = pd.read_csv(DATA / "TIE.csv",       **PARAMS)
tie_adr = pd.read_csv(DATA / "TIE_ADR.csv",   **PARAMS)
txc     = pd.read_csv(DATA / "TIE_X_CTR.csv", **PARAMS)
txn     = pd.read_csv(DATA / "TXN_X_CTR.csv", **PARAMS)

# ── Conversions de dates ─────────────────────────────────────
ctr["DAT_OUV_CTR"]   = pd.to_datetime(ctr["DAT_OUV_CTR"],   errors="coerce")
ctr["DAT_ECV_CTR"]   = pd.to_datetime(ctr["DAT_ECV_CTR"],   errors="coerce")
ctr["DAT_CLO_CTR"]   = pd.to_datetime(ctr["DAT_CLO_CTR"],   errors="coerce")
tie["DAT_NAI"]       = pd.to_datetime(tie["DAT_NAI"],        errors="coerce")
tie["DAT_DCS"]       = pd.to_datetime(tie["DAT_DCS"],        errors="coerce")
txn["DAT_CRE_DT"]    = pd.to_datetime(txn["DAT_CRE_MVT_CPB"],errors="coerce")

# TIE_ADR : format SAS DDMONYYYY (ex: "24NOV2025")
# Certaines valeurs peuvent être au format YYYY-MM-DD aussi
tie_adr["DAT_MAJ_ADR_DT"] = pd.to_datetime(tie_adr["DAT_MAJ_ADR"], format="mixed", errors="coerce")

# ── Colonnes calculées de base ───────────────────────────────
MAPPING_ECV = {"1":"Ouvert","2":"En attente","3":"Suspendu",
               "4":"Cloture","5":"En resiliation","6":"Resilie"}
ctr["LIB_ECV"]  = ctr["COD_ECV_CTR"].map(MAPPING_ECV)
ctr["CAT_ECV"]  = np.where(ctr["COD_ECV_CTR"].isin(["1","2","3"]),"Actif","Inactif")
ctr["SEGMENT"]  = np.select(
    [ctr["SLD_CTR"].isna(), ctr["SLD_CTR"]<1000, ctr["SLD_CTR"]<10000, ctr["SLD_CTR"]<50000],
    ["Inconnu","Standard","Confort","Premium"], default="Private"
)

# ── Créer la base SQLite en mémoire ──────────────────────────
conn = sqlite3.connect(":memory:")
for nom, df in [("CTR",ctr),("TIE",tie),("TIE_ADR",tie_adr),
                ("TIE_X_CTR",txc),("TXN_X_CTR",txn)]:
    df.to_sql(nom, conn, if_exists="replace", index=False)

# ── Vérification ─────────────────────────────────────────────
print("Tables chargées :")
for nom, df in [("CTR",ctr),("TIE",tie),("TIE_ADR",tie_adr),("TIE_X_CTR",txc),("TXN_X_CTR",txn)]:
    print(f"  {nom:<12}: {len(df):>5} lignes × {df.shape[1]} colonnes")
print("\\n✓ Setup Jour 3 terminé")"""),

# ════════════════════════════════════════════════════════
# SECTION 1 · SQL — CTEs
# ════════════════════════════════════════════════════════
md("""---
# 1 · SQL Analytique — CTEs (WITH)

Un **CTE** (Common Table Expression) est une requête nommée temporaire définie
avec le mot-clé `WITH`. Elle améliore la lisibilité et permet de réutiliser
des sous-requêtes.

```sql
WITH nom_cte AS (
    SELECT ...    -- sous-requête
),
autre_cte AS (
    SELECT ... FROM nom_cte    -- peut référencer la CTE précédente
)
SELECT * FROM autre_cte
```

## Avantages vs sous-requêtes

| CTE | Sous-requête imbriquée |
|-----|----------------------|
| Lisible, nommée | Difficile à lire |
| Réutilisable dans la même requête | Doit être réécrite |
| Peut référencer d'autres CTEs | Ordre d'imbrication strict |
| Déboguable individuellement | Débogage difficile |"""),

code("""# ── CTE simple : nombre de contrats par client ────────────────
sql_cte1 = '''
    WITH
    -- CTE 1 : compter les contrats par client
    contrats_par_client AS (
        SELECT
            txc.IDT_PI,
            COUNT(c.IDT_AC)   AS NB_CONTRATS,
            SUM(c.SLD_CTR)    AS SOLDE_TOTAL,
            MAX(c.SLD_CTR)    AS SOLDE_MAX
        FROM TIE_X_CTR txc
        LEFT JOIN CTR c ON txc.IDT_AC = c.IDT_AC
        WHERE c.COD_ECV_CTR IN ('1','2','3')   -- contrats actifs seulement
        GROUP BY txc.IDT_PI
    ),

    -- CTE 2 : enrichir avec les infos client
    clients_enrichis AS (
        SELECT
            t.IDT_PI,
            t.COD_TYP_TIE,
            t.COD_LNG_CTR,
            cpc.NB_CONTRATS,
            ROUND(cpc.SOLDE_TOTAL, 2) AS SOLDE_TOTAL,
            ROUND(cpc.SOLDE_MAX,   2) AS SOLDE_MAX
        FROM TIE t
        LEFT JOIN contrats_par_client cpc ON t.IDT_PI = cpc.IDT_PI
        WHERE t.COD_TYP_TIE = '1'   -- personnes physiques seulement
    )

    -- Requête principale : utilise le résultat des CTEs
    SELECT *
    FROM clients_enrichis
    WHERE NB_CONTRATS IS NOT NULL
    ORDER BY SOLDE_TOTAL DESC
    LIMIT 10
'''

res_cte1 = pd.read_sql(sql_cte1, conn)
print("=== Top 10 clients PP par solde total (contrats actifs) ===")
print(res_cte1.to_string(index=False))"""),

# ── EXERCICE 1 ──────────────────────────────────────────────
md("""---
### 🟡 Exercice 1 · CTE — Activité transactionnelle par langue

**Écrire une requête SQL avec 2 CTEs :**
1. **CTE `activite_par_ctr`** : pour chaque `IDT_AC`, calculer `NB_TXN` et `DERN_TXN` (date max)
2. **CTE `stats_par_lng`** : joindre avec TIE_X_CTR et TIE, grouper par `COD_LNG_CTR`,
   calculer : `NB_CLIENTS_ACTIFS`, `NB_TXN_TOTAL`, `MOY_TXN_PAR_CLIENT`
3. **Requête finale** : afficher le résultat trié par `NB_TXN_TOTAL DESC`"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────
sql_ex1 = '''
    WITH
    activite_par_ctr AS (
        SELECT
            IDT_AC,
            COUNT(*)         AS NB_TXN,
            MAX(DAT_CRE_MVT_CPB) AS DERN_TXN
        FROM TXN_X_CTR
        GROUP BY IDT_AC
    ),

    stats_par_lng AS (
        SELECT
            t.COD_LNG_CTR,
            COUNT(DISTINCT t.IDT_PI)  AS NB_CLIENTS_ACTIFS,
            SUM(a.NB_TXN)             AS NB_TXN_TOTAL,
            ROUND(AVG(a.NB_TXN), 1)   AS MOY_TXN_PAR_CLIENT
        FROM TIE t
        JOIN TIE_X_CTR txc ON t.IDT_PI = txc.IDT_PI
        JOIN activite_par_ctr a ON txc.IDT_AC = a.IDT_AC
        GROUP BY t.COD_LNG_CTR
    )

    SELECT * FROM stats_par_lng ORDER BY NB_TXN_TOTAL DESC
'''
res_ex1 = pd.read_sql(sql_ex1, conn)
print(res_ex1.to_string(index=False))"""),

# ════════════════════════════════════════════════════════
# SECTION 2 · WINDOW FUNCTIONS — OVER / PARTITION BY
# ════════════════════════════════════════════════════════
md("""---
# 2 · Window Functions — OVER / PARTITION BY

Les **window functions** calculent une valeur pour chaque ligne en tenant compte
d'un groupe (partition) de lignes voisines. Elles ne réduisent pas le nombre de lignes
(contrairement à `GROUP BY`).

## Structure

```sql
FONCTION() OVER (
    PARTITION BY colonne_de_groupe    -- définit la "fenêtre"
    ORDER BY   colonne_de_tri         -- ordre dans la fenêtre (optionnel)
    ROWS BETWEEN ...                  -- limites de la fenêtre (optionnel)
)
```

## Fonctions courantes

| Fonction SQL | Équivalent Pandas | Usage |
|-------------|------------------|-------|
| `ROW_NUMBER()` | `.groupby().cumcount()+1` | Numéroter les lignes |
| `RANK()` | `.groupby().rank()` | Rang avec ex-aequo |
| `SUM() OVER (PARTITION BY)` | `.transform("sum")` | Total de groupe sur chaque ligne |
| `AVG() OVER (PARTITION BY)` | `.transform("mean")` | Moyenne de groupe |
| `LAG(col, 1)` | `.groupby().shift(1)` | Valeur précédente |
| `LEAD(col, 1)` | `.groupby().shift(-1)` | Valeur suivante |
| `FIRST_VALUE()` | `.transform("first")` | 1ère valeur du groupe |"""),

code("""# ── PARTITION BY en SQL ─────────────────────────────────────
sql_part = '''
    SELECT
        c.IDT_AC,
        c.COD_ECV_CTR,
        c.SLD_CTR,
        c.COD_DEV,
        -- Total de solde par devise (PARTITION BY COD_DEV)
        SUM(c.SLD_CTR) OVER (PARTITION BY c.COD_DEV)
            AS SOLDE_TOTAL_DEVISE,
        -- Rang par solde décroissant dans chaque devise
        ROW_NUMBER() OVER (PARTITION BY c.COD_DEV ORDER BY c.SLD_CTR DESC)
            AS RANG_DANS_DEVISE,
        -- Solde moyen dans chaque statut
        ROUND(AVG(c.SLD_CTR) OVER (PARTITION BY c.COD_ECV_CTR), 2)
            AS SLD_MOY_STATUT
    FROM CTR c
    WHERE c.SLD_CTR IS NOT NULL
    ORDER BY c.COD_DEV, c.SLD_CTR DESC
    LIMIT 15
'''
res_part = pd.read_sql(sql_part, conn)
print("=== Window Functions : totaux et rangs ===")
print(res_part.to_string(index=False))"""),

code("""# ── Équivalent Pandas : .groupby().transform() ───────────────
# transform() retourne une Series de MÊME longueur que le DataFrame d'entrée
# C'est l'équivalent de OVER (PARTITION BY) en SQL

# Garder seulement les lignes avec solde renseigné
ctr_solde = ctr[ctr["SLD_CTR"].notna()].copy()

# SUM OVER (PARTITION BY COD_DEV) :
# .groupby("COD_DEV")["SLD_CTR"] regroupe par devise
# .transform("sum") : pour chaque ligne, retourner la SOMME du groupe
ctr_solde["SLD_TOTAL_DEV"] = ctr_solde.groupby("COD_DEV")["SLD_CTR"].transform("sum")

# AVG OVER (PARTITION BY COD_ECV_CTR) :
ctr_solde["SLD_MOY_STATUT"] = ctr_solde.groupby("COD_ECV_CTR")["SLD_CTR"].transform("mean").round(2)

# RANK OVER (PARTITION BY COD_DEV ORDER BY SLD_CTR DESC) :
# .rank(ascending=False, method="first") : rang décroissant, sans ex-aequo
ctr_solde["RANG_DEVISE"] = ctr_solde.groupby("COD_DEV")["SLD_CTR"].rank(ascending=False, method="first").astype(int)

# % du total de la devise
ctr_solde["PCT_DEV"] = (ctr_solde["SLD_CTR"] / ctr_solde["SLD_TOTAL_DEV"] * 100).round(1)

print("=== PARTITION BY en Pandas avec transform() ===")
cols = ["IDT_AC","COD_DEV","SLD_CTR","SLD_TOTAL_DEV","RANG_DEVISE","SLD_MOY_STATUT","PCT_DEV"]
print(ctr_solde[cols].sort_values(["COD_DEV","RANG_DEVISE"]).head(12).to_string(index=False))"""),

# ── EXERCICE 2 ──────────────────────────────────────────────
md("""---
### 🟡 Exercice 2 · Window Functions en Pandas

**Sur le DataFrame `ctr` (avec soldes renseignés) :**
1. Calculer `NB_CTR_SEGMENT` : nombre de contrats dans chaque `SEGMENT` (avec `.transform("count")`)
2. Calculer `SLD_MAX_SEGMENT` : solde maximum dans chaque `SEGMENT` (avec `.transform("max")`)
3. Calculer `RANG_GLOBAL` : rang du contrat par solde décroissant (sur tout le DataFrame, pas par groupe)
4. Afficher les 10 premiers rangs globaux avec leurs métriques"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────

ctr_ex2 = ctr[ctr["SLD_CTR"].notna()].copy()

# 1. Nombre de contrats par segment
ctr_ex2["NB_CTR_SEGMENT"] = ctr_ex2.groupby("SEGMENT")["IDT_AC"].transform("count")

# 2. Solde max par segment
ctr_ex2["SLD_MAX_SEGMENT"] = ctr_ex2.groupby("SEGMENT")["SLD_CTR"].transform("max")

# 3. Rang global
ctr_ex2["RANG_GLOBAL"] = ctr_ex2["SLD_CTR"].rank(ascending=False, method="first").astype(int)

# 4. Top 10
top10 = ctr_ex2.nsmallest(10, "RANG_GLOBAL")
print(top10[["RANG_GLOBAL","IDT_AC","SEGMENT","SLD_CTR","NB_CTR_SEGMENT","SLD_MAX_SEGMENT"]].to_string(index=False))"""),

# ════════════════════════════════════════════════════════
# SECTION 3 · ROW_NUMBER / LAG / LEAD
# ════════════════════════════════════════════════════════
md("""---
# 3 · ROW_NUMBER, LAG et LEAD

## ROW_NUMBER

Numérote les lignes dans une partition selon un ordre donné.
Utile pour : "garder le dernier contrat de chaque client", "N-ième transaction", etc.

## LAG / LEAD

Accèdent à la valeur d'une ligne **précédente (LAG)** ou **suivante (LEAD)**.
Utiles pour : évolution mois/mois, détection de changements."""),

code("""# ── ROW_NUMBER en SQL : dernier contrat par client ───────────
sql_rn = '''
    WITH contrats_ordonnes AS (
        SELECT
            txc.IDT_PI,
            c.IDT_AC,
            c.COD_ECV_CTR,
            c.SLD_CTR,
            c.DAT_OUV_CTR,
            -- Numéroter les contrats par client, du plus récent au plus ancien
            ROW_NUMBER() OVER (
                PARTITION BY txc.IDT_PI
                ORDER BY c.DAT_OUV_CTR DESC   -- le plus récent = rang 1
            ) AS RN
        FROM TIE_X_CTR txc
        JOIN CTR c ON txc.IDT_AC = c.IDT_AC
    )
    -- Garder seulement le dernier contrat de chaque client (RN = 1)
    SELECT IDT_PI, IDT_AC, COD_ECV_CTR, SLD_CTR, DAT_OUV_CTR
    FROM contrats_ordonnes
    WHERE RN = 1
    ORDER BY SLD_CTR DESC
    LIMIT 10
'''
res_rn = pd.read_sql(sql_rn, conn)
print("=== Dernier contrat par client (ROW_NUMBER) ===")
print(res_rn.to_string(index=False))"""),

code("""# ── ROW_NUMBER en Pandas : cumcount() ────────────────────────
# Équivalent de ROW_NUMBER OVER (PARTITION BY col ORDER BY autre_col)

# Joindre TIE_X_CTR et CTR
liens_ctr = pd.merge(
    txc[["IDT_PI","IDT_AC"]],
    ctr[["IDT_AC","COD_ECV_CTR","SLD_CTR","DAT_OUV_CTR"]],
    on="IDT_AC", how="left"
)

# Trier par client ET par date décroissante (le plus récent en premier)
liens_ctr = liens_ctr.sort_values(["IDT_PI","DAT_OUV_CTR"], ascending=[True, False])

# cumcount() : numérote les lignes de chaque groupe à partir de 0
# +1 pour commencer à 1 comme ROW_NUMBER en SQL
liens_ctr["RN"] = liens_ctr.groupby("IDT_PI").cumcount() + 1

# Garder seulement le dernier contrat par client (RN == 1)
dern_ctr_par_cli = liens_ctr[liens_ctr["RN"] == 1].copy()

print(f"Clients distincts : {len(dern_ctr_par_cli)}")
print(dern_ctr_par_cli[["IDT_PI","IDT_AC","COD_ECV_CTR","SLD_CTR","DAT_OUV_CTR"]].head(8).to_string(index=False))"""),

code("""# ── LAG en SQL : variation mois sur mois ────────────────────
# On va agréger les transactions par mois, puis calculer la variation
sql_lag = '''
    WITH mensuel AS (
        SELECT
            SUBSTR(DAT_CRE_MVT_CPB, 1, 7) AS MOIS,   -- "YYYY-MM"
            COUNT(*)                        AS NB_TXN
        FROM TXN_X_CTR
        WHERE DAT_CRE_MVT_CPB IS NOT NULL
        GROUP BY MOIS
        ORDER BY MOIS
    )
    SELECT
        MOIS,
        NB_TXN,
        LAG(NB_TXN, 1) OVER (ORDER BY MOIS) AS NB_TXN_MOIS_PREC,
        ROUND(
            (NB_TXN - LAG(NB_TXN, 1) OVER (ORDER BY MOIS)) * 1.0
            / LAG(NB_TXN, 1) OVER (ORDER BY MOIS) * 100,
            1
        ) AS VAR_PCT
    FROM mensuel
    ORDER BY MOIS
'''
res_lag = pd.read_sql(sql_lag, conn)
print("=== Transactions mensuelles + variation MoM (LAG SQL) ===")
print(res_lag.to_string(index=False))"""),

code("""# ── LAG en Pandas : .shift() ─────────────────────────────────
# .shift(1) décale d'une ligne vers le bas = la ligne précédente
# Équivalent de LAG(col, 1) OVER (ORDER BY ...)

# Agréger les transactions par mois
txn_mensuel = (
    txn.dropna(subset=["DAT_CRE_DT"])          # supprimer les dates manquantes
       .assign(MOIS=txn["DAT_CRE_DT"].dt.to_period("M"))   # créer la colonne MOIS
       .groupby("MOIS", observed=True)["NUM_ORD_MVT_CPB"]
       .count()
       .reset_index()
)
txn_mensuel.columns = ["MOIS","NB_TXN"]
txn_mensuel = txn_mensuel.sort_values("MOIS")

# .shift(1) : valeur du mois précédent (LAG de 1 période)
txn_mensuel["NB_TXN_PREC"] = txn_mensuel["NB_TXN"].shift(1)

# Variation absolue et %
txn_mensuel["VAR_ABS"] = txn_mensuel["NB_TXN"] - txn_mensuel["NB_TXN_PREC"]
txn_mensuel["VAR_PCT"] = (txn_mensuel["VAR_ABS"] / txn_mensuel["NB_TXN_PREC"] * 100).round(1)

# .shift(-1) : valeur du MOIS SUIVANT (LEAD)
txn_mensuel["NB_TXN_SUIV"] = txn_mensuel["NB_TXN"].shift(-1)

print("=== Évolution mensuelle des transactions (LAG/LEAD Pandas) ===")
print(txn_mensuel.to_string(index=False))"""),

# ── EXERCICE 3 ──────────────────────────────────────────────
md("""---
### 🟡 Exercice 3 · LAG sur les soldes de contrats

**Contexte :** La table `CTR` contient `DAT_OUV_CTR` et `SLD_CTR`.
On veut mesurer l'évolution du solde lors de l'ouverture de nouveaux contrats.

**À faire (en Pandas) :**
1. Trier `ctr` par `DAT_OUV_CTR`
2. Créer `SLD_PREC` = solde du contrat précédent (LAG de 1)
3. Créer `VAR_SLD` = `SLD_CTR - SLD_PREC` (variation de solde)
4. Calculer le % de contrats où le solde a augmenté vs diminué vs stable
5. Afficher les 10 premières lignes"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────

ctr_lag = ctr[ctr["SLD_CTR"].notna()].copy()
ctr_lag = ctr_lag.sort_values("DAT_OUV_CTR")

# 1-2. LAG : valeur précédente
ctr_lag["SLD_PREC"] = ctr_lag["SLD_CTR"].shift(1)

# 3. Variation
ctr_lag["VAR_SLD"] = ctr_lag["SLD_CTR"] - ctr_lag["SLD_PREC"]

# 4. Classification
ctr_lag["EVOL"] = np.where(
    ctr_lag["VAR_SLD"].isna(), "Premier",
    np.where(ctr_lag["VAR_SLD"] > 0, "Hausse",
    np.where(ctr_lag["VAR_SLD"] < 0, "Baisse", "Stable"))
)
print(ctr_lag["EVOL"].value_counts().to_string())

# 5. Aperçu
print(ctr_lag[["DAT_OUV_CTR","IDT_AC","SLD_CTR","SLD_PREC","VAR_SLD","EVOL"]].head(10).to_string(index=False))"""),

md("""**✅ Correction exercice 3 :**"""),

code("""# ✅ CORRECTION exercice 3 ──────────────────────────────────

ctr_lag = ctr[ctr["SLD_CTR"].notna()].copy()
ctr_lag = ctr_lag.sort_values("DAT_OUV_CTR").reset_index(drop=True)

# LAG avec .shift(1) : décale d'une position vers le bas
ctr_lag["SLD_PREC"] = ctr_lag["SLD_CTR"].shift(1)   # NaN pour la 1ère ligne

# Variation de solde (NaN pour la 1ère ligne)
ctr_lag["VAR_SLD"]  = ctr_lag["SLD_CTR"] - ctr_lag["SLD_PREC"]

# Classification de l'évolution
ctr_lag["EVOL"] = np.select(
    [ctr_lag["VAR_SLD"].isna(),
     ctr_lag["VAR_SLD"] > 0,
     ctr_lag["VAR_SLD"] < 0,
     ctr_lag["VAR_SLD"] == 0],
    ["Premier", "Hausse", "Baisse", "Stable"],
    default="Inconnu"
)

# Statistiques
print("=== Évolution du solde d'un contrat à l'autre ===")
evol_stats = ctr_lag["EVOL"].value_counts()
total_suiv = len(ctr_lag) - 1   # -1 car le premier n'a pas de précédent
for evol, nb in evol_stats.items():
    pct = nb / len(ctr_lag) * 100
    print(f"  {evol:<10} : {nb:>4} ({pct:>5.1f}%)")
print()

# Top 10
print("=== 10 premières lignes ===")
cols = ["DAT_OUV_CTR","IDT_AC","SLD_CTR","SLD_PREC","VAR_SLD","EVOL"]
print(ctr_lag[cols].head(10).to_string(index=False))"""),

# ════════════════════════════════════════════════════════
# SECTION 4 · TIME SERIES — MANIPULATION DES DATES
# ════════════════════════════════════════════════════════
md("""---
# 4 · Time Series — Manipulation des dates

## Les formats de dates dans vos fichiers Beobank

| Table | Colonne | Format | Parsing |
|-------|---------|--------|---------|
| CTR | DAT_OUV_CTR | `YYYY-MM-DD` | automatique |
| CTR | DAT_ECV_CTR | `YYYY-MM-DD` | automatique |
| TIE | DAT_NAI | `YYYY-MM-DD` | automatique |
| TIE_ADR | DAT_MAJ_ADR | `DDMONYYYY` (SAS) | `format="mixed"` |
| TXN_X_CTR | DAT_CRE_MVT_CPB | `YYYY-MM-DD` | automatique |

## Attributs `.dt` disponibles

```python
serie_dates.dt.year      # année
serie_dates.dt.month     # mois (1-12)
serie_dates.dt.day       # jour
serie_dates.dt.dayofweek # jour de semaine (0=Lundi, 6=Dimanche)
serie_dates.dt.quarter   # trimestre (1-4)
serie_dates.dt.to_period("M")   # période mensuelle "2024-11"
serie_dates.dt.strftime("%b %Y")   # formatage libre "Nov 2024"
```"""),

code("""# ── Extraire des composantes de date ─────────────────────────
print("=== Composantes de date dans CTR ===")

# Utiliser les dates converties dans le setup
ctr_dates = ctr[ctr["DAT_OUV_CTR"].notna()].copy()

ctr_dates["ANNEE_OUV"]    = ctr_dates["DAT_OUV_CTR"].dt.year        # 2024, 2025...
ctr_dates["MOIS_OUV"]     = ctr_dates["DAT_OUV_CTR"].dt.month       # 1 à 12
ctr_dates["TRIM_OUV"]     = ctr_dates["DAT_OUV_CTR"].dt.quarter     # 1 à 4
ctr_dates["JOUR_SEM"]     = ctr_dates["DAT_OUV_CTR"].dt.dayofweek   # 0=Lundi
ctr_dates["LABEL_MOIS"]   = ctr_dates["DAT_OUV_CTR"].dt.strftime("%b %Y")    # "Nov 2024"
ctr_dates["PERIODE_MENS"] = ctr_dates["DAT_OUV_CTR"].dt.to_period("M")       # "2024-11"

print(ctr_dates[["IDT_AC","DAT_OUV_CTR","ANNEE_OUV","MOIS_OUV","TRIM_OUV","LABEL_MOIS"]].head(8).to_string(index=False))
print()

# Répartition par trimestre
print("=== Ouvertures par trimestre ===")
par_trim = ctr_dates.groupby(["ANNEE_OUV","TRIM_OUV"])["IDT_AC"].count().reset_index()
par_trim.columns = ["Année","Trimestre","Ouvertures"]
print(par_trim.to_string(index=False))"""),

code("""# ── Calculs de durée entre dates ─────────────────────────────
print("=== Ancienneté des contrats ===")

ctr_dur = ctr[ctr["DAT_OUV_CTR"].notna()].copy()

# date de référence : aujourd'hui ou la date la plus récente des données
date_ref = pd.Timestamp("2026-11-20")   # date de la formation

# Soustraction de deux Timestamps → Timedelta (durée)
ctr_dur["DUREE_JOURS"] = (date_ref - ctr_dur["DAT_OUV_CTR"]).dt.days
ctr_dur["DUREE_MOIS"]  = (ctr_dur["DUREE_JOURS"] / 30.44).round(1)   # ~30.44 jours/mois
ctr_dur["DUREE_ANS"]   = (ctr_dur["DUREE_JOURS"] / 365.25).round(2)

# Classe d'ancienneté
conditions_anc = [
    ctr_dur["DUREE_ANS"] < 1,      # moins de 1 an
    ctr_dur["DUREE_ANS"] < 3,      # 1 à 3 ans
    ctr_dur["DUREE_ANS"] < 7,      # 3 à 7 ans
]
labels_anc = ["< 1 an", "1-3 ans", "3-7 ans"]
ctr_dur["CLASSE_ANC"] = np.select(conditions_anc, labels_anc, default="> 7 ans")

print(ctr_dur[["IDT_AC","DAT_OUV_CTR","DUREE_JOURS","DUREE_ANS","CLASSE_ANC"]].head(8).to_string(index=False))
print()
print("=== Répartition par ancienneté ===")
print(ctr_dur["CLASSE_ANC"].value_counts().to_string())"""),

code("""# ── Format SAS DDMONYYYY dans TIE_ADR ────────────────────────
print("=== Dates SAS dans TIE_ADR ===")
print()

# Afficher les valeurs brutes
print("Valeurs brutes DAT_MAJ_ADR (5 premières) :")
print(tie_adr["DAT_MAJ_ADR"].head(5).tolist())
print()

# La colonne a été convertie dans le setup avec format="mixed"
print("Valeurs converties DAT_MAJ_ADR_DT (5 premières) :")
print(tie_adr["DAT_MAJ_ADR_DT"].head(5).tolist())
print()

# Vérifier combien ont été converties
nb_conv = tie_adr["DAT_MAJ_ADR_DT"].notna().sum()
nb_tot  = len(tie_adr)
print(f"Conversions réussies : {nb_conv}/{nb_tot} ({nb_conv/nb_tot:.0%})")
print()

# Extraire l'année et le mois
tie_adr["ANNEE_MAJ"] = tie_adr["DAT_MAJ_ADR_DT"].dt.year
tie_adr["MOIS_MAJ"]  = tie_adr["DAT_MAJ_ADR_DT"].dt.month
print("Répartition des mises à jour d'adresse par mois :")
print(tie_adr["MOIS_MAJ"].value_counts().sort_index().to_string())"""),

# ── EXERCICE 4 ──────────────────────────════════════════════
md("""---
### 🟡 Exercice 4 · Analyse temporelle des transactions

**À faire sur `txn` :**
1. Créer `ANNEE`, `MOIS`, `TRIM`, `JOUR_SEM` (0=Lun) à partir de `DAT_CRE_DT`
2. Compter les transactions par `JOUR_SEM` : quel jour y a-t-il le plus de transactions ?
3. Agréger par `ANNEE` et `MOIS` : compter `NB_TXN` et trouver les 3 mois les plus actifs
4. Calculer la durée en jours entre la première et dernière transaction de chaque `IDT_AC`"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────

txn_ex4 = txn[txn["DAT_CRE_DT"].notna()].copy()

# 1. Composantes de date
txn_ex4["ANNEE"]    = txn_ex4["DAT_CRE_DT"].dt.year
txn_ex4["MOIS"]     = txn_ex4["DAT_CRE_DT"].dt.month
txn_ex4["TRIM"]     = txn_ex4["DAT_CRE_DT"].dt.quarter
txn_ex4["JOUR_SEM"] = txn_ex4["DAT_CRE_DT"].dt.dayofweek

# 2. Par jour de la semaine
JOURS = {0:"Lundi",1:"Mardi",2:"Mercredi",3:"Jeudi",4:"Vendredi",5:"Samedi",6:"Dimanche"}
nb_par_jour = txn_ex4["JOUR_SEM"].value_counts().sort_index()
print("Transactions par jour de la semaine :")
for j, nb in nb_par_jour.items():
    print(f"  {JOURS[j]} : {nb}")

# 3. Top 3 mois
par_mois = txn_ex4.groupby(["ANNEE","MOIS"])["NUM_ORD_MVT_CPB"].count().reset_index()
par_mois.columns = ["Annee","Mois","NB_TXN"]
print("\\nTop 3 mois les plus actifs :")
print(par_mois.nlargest(3,"NB_TXN").to_string(index=False))

# 4. Durée d'activité par compte
duree_par_ctr = txn_ex4.groupby("IDT_AC")["DAT_CRE_DT"].agg(["min","max"])
duree_par_ctr["DUREE_J"] = (duree_par_ctr["max"] - duree_par_ctr["min"]).dt.days
print("\\nDurée d'activité par compte (5 premiers) :")
print(duree_par_ctr.sort_values("DUREE_J", ascending=False).head(5).to_string())"""),

# ════════════════════════════════════════════════════════
# SECTION 5 · FENÊTRE GLISSANTE 13 MOIS
# ════════════════════════════════════════════════════════
md("""---
# 5 · Fenêtre glissante — 13 mois glissants

Une **fenêtre glissante de 13 mois** est un rapport qui couvre toujours
les 13 derniers mois complets (M-12 à M, soit 1 an + le mois courant).

C'est le format standard des rapports de portefeuille Beobank."""),

code("""# ── Construire la fenêtre 13 mois ────────────────────────────
from pandas.tseries.offsets import DateOffset

# Date de référence : dernier mois complet avant la formation
DATE_REF   = pd.Timestamp("2026-10-31")    # fin octobre 2026 = dernier mois complet
DATE_DEBUT = DATE_REF - DateOffset(months=12)  # 13 mois avant = nov 2025

print(f"Fenêtre d'analyse : {DATE_DEBUT.strftime('%b %Y')} → {DATE_REF.strftime('%b %Y')}")
print(f"Durée : 13 mois")
print()

# Filtrer les transactions dans la fenêtre
txn_13m = txn[
    (txn["DAT_CRE_DT"] >= DATE_DEBUT) &
    (txn["DAT_CRE_DT"] <= DATE_REF)
].copy()

print(f"Transactions dans la fenêtre 13 mois : {len(txn_13m)}")
print(f"Transactions totales : {len(txn)}")
print(f"Couverture : {len(txn_13m)/len(txn):.1%}")"""),

code("""# ── Agréger par mois et créer la série temporelle ─────────────

# Créer la colonne PERIODE (période mensuelle)
txn_13m["PERIODE"] = txn_13m["DAT_CRE_DT"].dt.to_period("M")

# Agréger par mois
serie_mensuelle = (
    txn_13m
    .groupby("PERIODE")["NUM_ORD_MVT_CPB"]
    .count()
    .reset_index()
)
serie_mensuelle.columns = ["PERIODE","NB_TXN"]

# Générer tous les mois de la fenêtre (même s'il n'y a pas de transactions)
# pd.period_range() : séquence de périodes mensuelles
tous_mois = pd.period_range(
    start = DATE_DEBUT.to_period("M"),   # to_period() : convertir Timestamp → Period
    end   = DATE_REF.to_period("M"),
    freq  = "M"                           # fréquence mensuelle
)
grille_mois = pd.DataFrame({"PERIODE": tous_mois})

# Jointure pour remplir les mois vides
serie_complete = pd.merge(
    grille_mois, serie_mensuelle, on="PERIODE", how="left"
).fillna(0)
serie_complete["NB_TXN"] = serie_complete["NB_TXN"].astype(int)

# Moyenne mobile sur 3 mois
serie_complete["MOY_3M"] = serie_complete["NB_TXN"].rolling(3, min_periods=1).mean().round(1)

print("=== Série mensuelle 13 mois ===")
print(serie_complete.to_string(index=False))
print(f"\\nTotal transactions 13 mois : {serie_complete['NB_TXN'].sum()}")
print(f"Moyenne mensuelle          : {serie_complete['NB_TXN'].mean():.1f}")"""),

# ── EXERCICE 5 ──────────────────────────────────────────────
md("""---
### 🟡 Exercice 5 · Ouvertures de contrats 13 mois glissants

**À faire :**
1. Définir une fenêtre 13 mois (oct 2025 → oct 2026)
2. Filtrer `ctr` sur `DAT_OUV_CTR` dans cette fenêtre
3. Agréger par mois : `NB_OUVERTURES`, `SLD_MOYEN` (arrondi à 2 décimales)
4. Calculer `CUMUL_OUV` (somme cumulée des ouvertures avec `.cumsum()`)
5. Identifier le mois avec le plus d'ouvertures"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────

# 1. Fenêtre
DATE_REF_OUV   = pd.Timestamp("2026-10-31")
DATE_DEBUT_OUV = DATE_REF_OUV - DateOffset(months=12)

# 2. Filtrer
ctr_13m = ctr[
    (ctr["DAT_OUV_CTR"] >= DATE_DEBUT_OUV) &
    (ctr["DAT_OUV_CTR"] <= DATE_REF_OUV)
].copy()
ctr_13m["PERIODE"] = ctr_13m["DAT_OUV_CTR"].dt.to_period("M")

# 3. Agréger
ouv_mensuel = ctr_13m.groupby("PERIODE").agg(
    NB_OUVERTURES = ("IDT_AC",  "count"),
    SLD_MOYEN     = ("SLD_CTR", "mean"),
).round(2).reset_index()

# 4. Cumul
ouv_mensuel["CUMUL_OUV"] = ouv_mensuel["NB_OUVERTURES"].cumsum()

# 5. Mois max
mois_max = ouv_mensuel.loc[ouv_mensuel["NB_OUVERTURES"].idxmax()]
print(ouv_mensuel.to_string(index=False))
print(f"\\nMois le plus actif : {mois_max['PERIODE']} ({mois_max['NB_OUVERTURES']} ouvertures)")"""),

# ════════════════════════════════════════════════════════
# SECTION 6 · MATPLOTLIB — GRAPHIQUES
# ════════════════════════════════════════════════════════
md("""---
# 6 · Visualisation avec Matplotlib

Matplotlib est la bibliothèque de référence pour les graphiques en Python.
Elle est utilisée dans les rapports Power BI, les exports PDF, et les notebooks.

## Structure de base

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 5))   # créer la figure et les axes
ax.bar(x, y)                               # tracer le graphique
ax.set_title("Titre")                      # titre
ax.set_xlabel("Axe X")                    # étiquette axe X
ax.set_ylabel("Axe Y")                    # étiquette axe Y
plt.tight_layout()                         # ajuster les marges
plt.show()                                 # afficher
```

## Types de graphiques

| Type | Code | Usage |
|------|------|-------|
| Barres verticales | `ax.bar(x, y)` | Comparaison de catégories |
| Barres horizontales | `ax.barh(y, x)` | Long texte sur l'axe |
| Courbe | `ax.plot(x, y)` | Évolution temporelle |
| Camembert | `ax.pie(tailles, labels=...)` | Répartition en % |
| Nuage de points | `ax.scatter(x, y)` | Corrélation |"""),

code("""# ── Graphique 1 : barres verticales — contrats par statut ─────
import matplotlib.pyplot as plt

# Données : répartition par statut
par_statut = ctr["LIB_ECV"].value_counts()    # .value_counts() trie par fréquence

# Couleur par catégorie (actif/inactif)
COULEURS_STATUT = {
    "Ouvert":          "#2196F3",   # bleu
    "En attente":      "#03A9F4",   # bleu clair
    "Suspendu":        "#FF9800",   # orange
    "Cloture":         "#9E9E9E",   # gris
    "En resiliation":  "#F44336",   # rouge
    "Resilie":         "#B71C1C",   # rouge foncé
}
couleurs = [COULEURS_STATUT.get(s, "#607D8B") for s in par_statut.index]

# Créer la figure
fig, ax = plt.subplots(figsize=(10, 5))    # largeur 10 pouces, hauteur 5 pouces

# Tracer les barres
# par_statut.index = noms des statuts (axe X)
# par_statut.values = effectifs (axe Y)
barres = ax.bar(par_statut.index, par_statut.values, color=couleurs,
                edgecolor="white", linewidth=0.5)

# Ajouter les valeurs au-dessus des barres
for barre in barres:
    hauteur = barre.get_height()   # hauteur = valeur de la barre
    ax.text(
        barre.get_x() + barre.get_width()/2,   # position X = milieu de la barre
        hauteur + 0.5,                          # position Y = juste au-dessus
        str(int(hauteur)),                      # texte = valeur
        ha="center", va="bottom", fontsize=10, fontweight="bold"
    )

# Mise en forme
ax.set_title("Répartition des contrats par statut", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Statut du contrat", fontsize=11)
ax.set_ylabel("Nombre de contrats", fontsize=11)
ax.set_ylim(0, par_statut.max() * 1.15)   # marge en haut pour les labels
ax.grid(axis="y", alpha=0.3, linestyle="--")   # grille horizontale discrète
ax.spines[["top","right"]].set_visible(False)  # supprimer les bordures inutiles

plt.xticks(rotation=20, ha="right")   # incliner les étiquettes X
plt.tight_layout()                     # ajuster les marges automatiquement
plt.show()
print("Graphique 1 affiché.")"""),

code("""# ── Graphique 2 : barres horizontales — top 10 soldes ────────
# Les barres horizontales sont préférables quand les étiquettes sont longues

ctr_avec_solde = ctr[ctr["SLD_CTR"].notna()].nlargest(10, "SLD_CTR")

fig, ax = plt.subplots(figsize=(10, 6))

# barh(y, x) : y = étiquettes (axe vertical), x = valeurs (axe horizontal)
barres_h = ax.barh(
    ctr_avec_solde["IDT_AC"],      # axe Y : identifiants des contrats
    ctr_avec_solde["SLD_CTR"],     # axe X : soldes
    color="#1565C0",               # bleu Beobank
    edgecolor="white"
)

# Valeurs sur les barres
for barre in barres_h:
    largeur = barre.get_width()
    ax.text(
        largeur + 200,             # légèrement à droite de la barre
        barre.get_y() + barre.get_height()/2,   # au milieu vertical de la barre
        f"{largeur:,.0f} EUR",
        va="center", fontsize=9
    )

ax.set_title("Top 10 contrats par solde", fontsize=13, fontweight="bold")
ax.set_xlabel("Solde (EUR)", fontsize=11)
ax.set_ylabel("Identifiant du contrat", fontsize=11)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.spines[["top","right"]].set_visible(False)

plt.tight_layout()
plt.show()
print("Graphique 2 affiché.")"""),

code("""# ── Graphique 3 : courbe temporelle avec double axe ──────────
# La série mensuelle de transactions + taux de variation

if len(serie_complete) > 0:
    # Préparer les données
    x_labels   = [str(p) for p in serie_complete["PERIODE"]]    # "2025-11", "2025-12"...
    x_positions = range(len(x_labels))                            # 0, 1, 2, ...

    # Créer la figure avec deux axes Y (twinx = même axe X, deux axes Y)
    fig, ax1 = plt.subplots(figsize=(12, 5))
    ax2 = ax1.twinx()   # créer un 2ème axe Y superposé

    # ── Axe 1 (gauche) : nombre de transactions (barres) ─────
    barres_t = ax1.bar(x_positions, serie_complete["NB_TXN"],
                       color="#90CAF9", alpha=0.7, label="Nb transactions")

    # ── Axe 1 (gauche) : moyenne mobile (courbe) ─────────────
    ax1.plot(x_positions, serie_complete["MOY_3M"],
             color="#1565C0", linewidth=2.5, marker="o", markersize=5,
             label="Moy. mobile 3 mois", zorder=5)

    # ── Configuration des axes ────────────────────────────────
    ax1.set_xlabel("Mois", fontsize=11)
    ax1.set_ylabel("Nombre de transactions", fontsize=11, color="#1565C0")
    ax1.set_ylim(0, serie_complete["NB_TXN"].max() * 1.25)
    ax1.set_xticks(x_positions)
    ax1.set_xticklabels(x_labels, rotation=45, ha="right", fontsize=9)
    ax1.grid(axis="y", alpha=0.3, linestyle="--")
    ax1.spines[["top","right"]].set_visible(False)

    # ── Titre et légendes ─────────────────────────────────────
    fig.suptitle("Activité transactionnelle — 13 mois glissants",
                 fontsize=13, fontweight="bold")
    lines1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(lines1, labels1, loc="upper left", framealpha=0.9)

    plt.tight_layout()
    plt.show()
    print("Graphique 3 affiché.")
else:
    print("Pas de données pour la fenêtre 13 mois — vérifier les dates.")"""),

code("""# ── Graphique 4 : camembert — répartition par langue ─────────
# Le camembert est utile pour les répartitions (max 5-6 parts)

nb_par_lng = tie["COD_LNG_CTR"].value_counts()
LABEL_LNG  = {"FR":"Français","NL":"Néerlandais","":"N/A"}
labels_aff  = [LABEL_LNG.get(l, l) for l in nb_par_lng.index]

fig, ax = plt.subplots(figsize=(7, 6))

# autopct='%1.1f%%' : affiche le pourcentage sur chaque part (1 décimale)
# startangle=90 : commencer à midi (12h)
# pctdistance=0.85 : distance du centre pour les pourcentages
wedges, texts, autotexts = ax.pie(
    nb_par_lng.values,
    labels      = labels_aff,
    autopct     = "%1.1f%%",
    startangle  = 90,
    colors      = ["#1E88E5","#FDD835","#43A047"],
    wedgeprops  = {"edgecolor": "white", "linewidth": 2},
    pctdistance = 0.80,
)

# Personnaliser les textes
for text in texts:
    text.set_fontsize(12)
for autotext in autotexts:
    autotext.set_fontsize(11)
    autotext.set_fontweight("bold")
    autotext.set_color("white")

ax.set_title("Répartition des clients par langue", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.show()
print("Graphique 4 affiché.")"""),

# ── EXERCICE 6 ──────────────────────────────────────────────
md("""---
### 🟡 Exercice 6 · Graphique Matplotlib

**Créer un graphique en barres horizontales montrant :**
- Les 6 tranches d'âge de `tie["TRANCHE_AGE"]` (créées au Jour 2)
- Pour chaque tranche : le nombre de clients
- Barres colorées selon la tranche (dégradé)
- Titre, étiquettes, valeurs sur les barres

**Contraintes :**
- Utiliser `ax.barh()`
- Ajouter les valeurs numériques à droite de chaque barre
- `figsize=(9, 5)`"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────
# Calculer les données d'abord
if "TRANCHE_AGE" not in tie.columns:
    # Recréer si besoin
    tie["DAT_NAI_DT"] = pd.to_datetime(tie["DAT_NAI"], errors="coerce")
    tie["AGE_APPROX"]  = 2026 - tie["DAT_NAI_DT"].dt.year
    bins_age = [0,25,35,50,65,120]
    labels_age = ["<25","25-34","35-49","50-64","65+"]
    tie["TRANCHE_AGE"] = pd.cut(tie["AGE_APPROX"], bins=bins_age, labels=labels_age)

nb_par_tranche = tie["TRANCHE_AGE"].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(9, 5))
couleurs = ["#BBDEFB","#64B5F6","#2196F3","#1565C0","#0D47A1"][:len(nb_par_tranche)]

barres_age = ax.barh(nb_par_tranche.index.astype(str), nb_par_tranche.values,
                     color=couleurs, edgecolor="white")

for barre in barres_age:
    l = barre.get_width()
    ax.text(l + 0.3, barre.get_y() + barre.get_height()/2,
            str(int(l)), va="center", fontsize=10)

ax.set_title("Répartition des clients par tranche d'âge", fontsize=13, fontweight="bold")
ax.set_xlabel("Nombre de clients")
ax.set_ylabel("Tranche d'âge")
ax.spines[["top","right"]].set_visible(False)
plt.tight_layout()
plt.show()"""),

# ════════════════════════════════════════════════════════
# SECTION 7 · DASHBOARD GridSpec
# ════════════════════════════════════════════════════════
md("""---
# 7 · Dashboard multi-graphiques avec GridSpec

`GridSpec` permet de créer plusieurs graphiques dans une même figure,
avec des tailles différentes — idéal pour un **dashboard de rapport mensuel**."""),

code("""# ── Dashboard Rapport Mensuel Beobank ────────────────────────
import matplotlib.gridspec as gridspec

# ── Préparer les données ──────────────────────────────────────
# 1. Répartition par statut
par_statut_dash = ctr["LIB_ECV"].value_counts()

# 2. Répartition par segment
par_segment_dash = ctr["SEGMENT"].value_counts()

# 3. Série temporelle
txn_dash = txn[txn["DAT_CRE_DT"].notna()].copy()
txn_dash["PERIODE"] = txn_dash["DAT_CRE_DT"].dt.to_period("M")
serie_dash = txn_dash.groupby("PERIODE")["NUM_ORD_MVT_CPB"].count().reset_index()
serie_dash.columns = ["PERIODE","NB_TXN"]
serie_dash = serie_dash.sort_values("PERIODE").tail(12)   # 12 derniers mois

# 4. Répartition par langue
nb_lng_dash = tie["COD_LNG_CTR"].value_counts()

# ── Créer la figure avec GridSpec ─────────────────────────────
fig = plt.figure(figsize=(16, 10))
fig.suptitle("Rapport Mensuel Beobank — Portefeuille & Transactions",
             fontsize=16, fontweight="bold", y=0.98)

# GridSpec(nb_lignes, nb_colonnes) : grille 2×3
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

# ── Graphique A (haut gauche, large) : statuts ────────────────
ax_a = fig.add_subplot(gs[0, :2])   # ligne 0, colonnes 0-1 (les deux premières)
barres_a = ax_a.bar(par_statut_dash.index, par_statut_dash.values,
                    color=["#2196F3","#03A9F4","#FF9800","#9E9E9E","#F44336","#B71C1C"])
ax_a.set_title("Contrats par statut", fontsize=12, fontweight="bold")
ax_a.set_ylabel("Nombre")
for b in barres_a:
    ax_a.text(b.get_x()+b.get_width()/2, b.get_height()+0.3,
              str(int(b.get_height())), ha="center", fontsize=9)
ax_a.grid(axis="y", alpha=0.3)
ax_a.spines[["top","right"]].set_visible(False)
plt.setp(ax_a.get_xticklabels(), rotation=15, ha="right", fontsize=9)

# ── Graphique B (haut droite) : langues camembert ─────────────
ax_b = fig.add_subplot(gs[0, 2])   # ligne 0, colonne 2
lab_b = [{"FR":"FR","NL":"NL"}.get(l,l) for l in nb_lng_dash.index]
ax_b.pie(nb_lng_dash.values, labels=lab_b, autopct="%1.0f%%",
         colors=["#1E88E5","#FDD835","#43A047"],
         startangle=90, wedgeprops={"edgecolor":"white","linewidth":2},
         pctdistance=0.75)
ax_b.set_title("Clients par langue", fontsize=12, fontweight="bold")

# ── Graphique C (bas gauche) : segments ──────────────────────
ax_c = fig.add_subplot(gs[1, 0])   # ligne 1, colonne 0
ax_c.barh(par_segment_dash.index, par_segment_dash.values,
          color=["#1565C0","#1976D2","#42A5F5","#90CAF9","#E3F2FD"][:len(par_segment_dash)])
ax_c.set_title("Contrats par segment", fontsize=12, fontweight="bold")
ax_c.set_xlabel("Nb contrats")
ax_c.spines[["top","right"]].set_visible(False)
for b in ax_c.patches:
    ax_c.text(b.get_width()+0.3, b.get_y()+b.get_height()/2,
              str(int(b.get_width())), va="center", fontsize=8)

# ── Graphique D (bas centre+droite) : série temporelle ───────
ax_d = fig.add_subplot(gs[1, 1:])   # ligne 1, colonnes 1-2
x_d   = range(len(serie_dash))
labs_d = [str(p) for p in serie_dash["PERIODE"]]
ax_d.bar(x_d, serie_dash["NB_TXN"], color="#90CAF9", alpha=0.7)
ax_d.plot(x_d, serie_dash["NB_TXN"].rolling(3,min_periods=1).mean(),
          color="#1565C0", linewidth=2.5, marker="o", markersize=4)
ax_d.set_title("Transactions mensuelles (12 mois)", fontsize=12, fontweight="bold")
ax_d.set_ylabel("Nb transactions")
ax_d.set_xticks(x_d)
ax_d.set_xticklabels(labs_d, rotation=45, ha="right", fontsize=8)
ax_d.grid(axis="y", alpha=0.3)
ax_d.spines[["top","right"]].set_visible(False)

plt.savefig("../Sorties_Beobank/dashboard_mensuel.png", dpi=150, bbox_inches="tight")
plt.show()
print("Dashboard exporté → ../Sorties_Beobank/dashboard_mensuel.png")"""),

# ────────────────────────────────────────────────────────
# SECTION 8 · MINI-PROJET PIPELINE COMPLET
# ════════════════════════════════════════════════════════
md("""---
# 8 · Mini-projet final — Pipeline complet en 5 étapes

**Contexte :** Votre manager attend le **rapport mensuel de novembre 2026**.
Il doit couvrir les 13 derniers mois d'activité et contenir :
- Un tableau synthétique des KPIs
- Une analyse par segment de clientèle
- L'évolution mensuelle des transactions
- Un graphique exporté en PNG

**Les 5 étapes du pipeline :**
1. **Import** — recharger les 5 tables
2. **Nettoyage** — valeurs manquantes, conversions de types
3. **Transformation** — colonnes calculées, jointures, agrégations
4. **SQL** — requête analytique avec CTE
5. **Export + Visualisation** — CSV + graphique"""),

code("""# ── ÉTAPE 1 : Import ─────────────────────────────────────────
print("ÉTAPE 1 : Import des données")
print("="*50)

import pandas as pd, numpy as np, sqlite3, matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path
from pandas.tseries.offsets import DateOffset

DATA   = Path("../Orsys")
SORTIE = Path("../Sorties_Beobank")
SORTIE.mkdir(exist_ok=True)
PARAMS = dict(sep=";", na_values=".", encoding="utf-8")

ctr_p  = pd.read_csv(DATA/"CTR.csv",       **PARAMS)
tie_p  = pd.read_csv(DATA/"TIE.csv",       **PARAMS)
txc_p  = pd.read_csv(DATA/"TIE_X_CTR.csv", **PARAMS)
txn_p  = pd.read_csv(DATA/"TXN_X_CTR.csv", **PARAMS)

print(f"  CTR      : {len(ctr_p):>5} lignes")
print(f"  TIE      : {len(tie_p):>5} lignes")
print(f"  TIE_X_CTR: {len(txc_p):>5} lignes")
print(f"  TXN_X_CTR: {len(txn_p):>5} lignes")
print("  ✓ Import terminé")"""),

code("""# ── ÉTAPE 2 : Nettoyage ──────────────────────────────────────
print("\\nÉTAPE 2 : Nettoyage")
print("="*50)

# Conversions de dates
ctr_p["DAT_OUV_CTR"] = pd.to_datetime(ctr_p["DAT_OUV_CTR"], errors="coerce")
txn_p["DAT_CRE_DT"]  = pd.to_datetime(txn_p["DAT_CRE_MVT_CPB"], errors="coerce")
tie_p["DAT_NAI"]     = pd.to_datetime(tie_p["DAT_NAI"], errors="coerce")

# Signaler les manquants
print("  Soldes manquants CTR    :", ctr_p["SLD_CTR"].isna().sum())
print("  Dates OUV manquantes CTR:", ctr_p["DAT_OUV_CTR"].isna().sum())
print("  Dates TXN manquantes    :", txn_p["DAT_CRE_DT"].isna().sum())

# Doublons éventuels
print(f"  Doublons CTR (IDT_AC)   : {ctr_p['IDT_AC'].duplicated().sum()}")
print(f"  Doublons TIE (IDT_PI)   : {tie_p['IDT_PI'].duplicated().sum()}")
print("  ✓ Nettoyage terminé")"""),

code("""# ── ÉTAPE 3 : Transformation ─────────────────────────────────
print("\\nÉTAPE 3 : Transformation")
print("="*50)

MAPPING_ECV = {"1":"Ouvert","2":"En attente","3":"Suspendu",
               "4":"Cloture","5":"En resiliation","6":"Resilie"}

ctr_p["LIB_ECV"]  = ctr_p["COD_ECV_CTR"].map(MAPPING_ECV)
ctr_p["CAT_ECV"]  = np.where(ctr_p["COD_ECV_CTR"].isin(["1","2","3"]), "Actif", "Inactif")
ctr_p["SEGMENT"]  = np.select(
    [ctr_p["SLD_CTR"].isna(), ctr_p["SLD_CTR"]<1000, ctr_p["SLD_CTR"]<10000, ctr_p["SLD_CTR"]<50000],
    ["Inconnu","Standard","Confort","Premium"], default="Private"
)

# Fenêtre 13 mois
DATE_REF    = pd.Timestamp("2026-10-31")
DATE_DEBUT  = DATE_REF - DateOffset(months=12)

txn_13m_p   = txn_p[(txn_p["DAT_CRE_DT"]>=DATE_DEBUT)&(txn_p["DAT_CRE_DT"]<=DATE_REF)].copy()
txn_13m_p["PERIODE"] = txn_13m_p["DAT_CRE_DT"].dt.to_period("M")

# Agréger transactions par compte
act_ctr = txn_13m_p.groupby("IDT_AC")["NUM_ORD_MVT_CPB"].count().reset_index()
act_ctr.columns = ["IDT_AC","NB_TXN_13M"]

# Vue synthétique
vue_p = (
    pd.merge(ctr_p[["IDT_AC","COD_ECV_CTR","LIB_ECV","CAT_ECV","SEGMENT","SLD_CTR"]],
             txc_p[["IDT_AC","IDT_PI"]], on="IDT_AC", how="left")
    .pipe(pd.merge, tie_p[["IDT_PI","COD_TYP_TIE","COD_LNG_CTR"]], on="IDT_PI", how="left")
    .pipe(pd.merge, act_ctr, on="IDT_AC", how="left")
)
vue_p["NB_TXN_13M"] = vue_p["NB_TXN_13M"].fillna(0).astype(int)

print(f"  Vue synthétique : {len(vue_p)} lignes")
print("  ✓ Transformation terminée")"""),

code("""# ── ÉTAPE 4 : SQL analytique ─────────────────────────────────
print("\\nÉTAPE 4 : SQL analytique")
print("="*50)

conn_p = sqlite3.connect(":memory:")
vue_p.to_sql("VUE_PORTEFEUILLE", conn_p, if_exists="replace", index=False)

sql_kpi = '''
    WITH kpi_segment AS (
        SELECT
            SEGMENT,
            CAT_ECV,
            COUNT(*)               AS NB_CTR,
            ROUND(SUM(SLD_CTR),2)  AS SLD_TOTAL,
            ROUND(AVG(SLD_CTR),2)  AS SLD_MOY,
            ROUND(AVG(NB_TXN_13M),1) AS MOY_TXN_13M
        FROM VUE_PORTEFEUILLE
        GROUP BY SEGMENT, CAT_ECV
    )
    SELECT *
    FROM kpi_segment
    ORDER BY SLD_TOTAL DESC
'''
kpi = pd.read_sql(sql_kpi, conn_p)
print("  KPIs par segment :")
print(kpi.to_string(index=False))
print("  ✓ SQL terminé")"""),

code("""# ── ÉTAPE 5 : Export + Visualisation ─────────────────────────
print("\\nÉTAPE 5 : Export et Visualisation")
print("="*50)

# Export CSV
vue_p.to_csv(SORTIE/"rapport_mensuel_complet.csv", sep=";", index=False, encoding="utf-8")
kpi.to_csv(SORTIE/"kpi_segments_nov2026.csv", sep=";", index=False, encoding="utf-8")

# Série temporelle 13 mois
serie_pipe = (
    txn_13m_p.groupby("PERIODE")["NUM_ORD_MVT_CPB"]
    .count().reset_index()
)
serie_pipe.columns = ["PERIODE","NB_TXN"]
serie_pipe = serie_pipe.sort_values("PERIODE")

# ── DASHBOARD FINAL ───────────────────────────────────────────
fig = plt.figure(figsize=(16, 9))
fig.suptitle("Rapport Mensuel Beobank — Novembre 2026",
             fontsize=16, fontweight="bold", y=0.98)
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

# A : KPIs par segment (barres H)
ax_a = fig.add_subplot(gs[0, :2])
kpi_actif = kpi[kpi["CAT_ECV"]=="Actif"].sort_values("SLD_TOTAL")
colors_seg = ["#E3F2FD","#90CAF9","#2196F3","#0D47A1"][:len(kpi_actif)]
bars_a = ax_a.barh(kpi_actif["SEGMENT"], kpi_actif["SLD_TOTAL"]/1e6,
                    color=colors_seg, edgecolor="white")
ax_a.set_title("Solde total par segment (M EUR)", fontsize=12, fontweight="bold")
ax_a.set_xlabel("M EUR")
for b in bars_a:
    ax_a.text(b.get_width()+0.02, b.get_y()+b.get_height()/2,
              f"{b.get_width():.1f}M", va="center", fontsize=9)
ax_a.spines[["top","right"]].set_visible(False)

# B : camembert actif/inactif
ax_b = fig.add_subplot(gs[0, 2])
cat_counts = vue_p["CAT_ECV"].value_counts()
ax_b.pie(cat_counts.values, labels=cat_counts.index,
         autopct="%1.0f%%", colors=["#2196F3","#B0BEC5"],
         startangle=90, wedgeprops={"edgecolor":"white","linewidth":2})
ax_b.set_title("Actif / Inactif", fontsize=12, fontweight="bold")

# C : langue (barres)
ax_c = fig.add_subplot(gs[1, 0])
lng_ctr = vue_p["COD_LNG_CTR"].value_counts()
ax_c.bar(lng_ctr.index, lng_ctr.values, color=["#1E88E5","#FDD835"], edgecolor="white")
ax_c.set_title("Contrats par langue", fontsize=12, fontweight="bold")
ax_c.set_ylabel("Nb contrats")
ax_c.spines[["top","right"]].set_visible(False)
for b in ax_c.patches:
    ax_c.text(b.get_x()+b.get_width()/2, b.get_height()+0.5,
              str(int(b.get_height())), ha="center", fontsize=10)

# D : série temporelle
ax_d = fig.add_subplot(gs[1, 1:])
x_d   = range(len(serie_pipe))
labs_d = [str(p) for p in serie_pipe["PERIODE"]]
ax_d.bar(x_d, serie_pipe["NB_TXN"], color="#90CAF9", alpha=0.7)
ax_d.plot(x_d, serie_pipe["NB_TXN"].rolling(3,min_periods=1).mean(),
          "o-", color="#1565C0", linewidth=2, markersize=5)
ax_d.set_title("Transactions 13 mois glissants", fontsize=12, fontweight="bold")
ax_d.set_ylabel("Nb transactions")
ax_d.set_xticks(x_d)
ax_d.set_xticklabels(labs_d, rotation=45, ha="right", fontsize=8)
ax_d.grid(axis="y", alpha=0.3)
ax_d.spines[["top","right"]].set_visible(False)

# Export PNG
chemin_png = SORTIE/"rapport_final_nov2026.png"
plt.savefig(chemin_png, dpi=150, bbox_inches="tight")
plt.show()

print(f"  Exporté : {SORTIE/'rapport_mensuel_complet.csv'}")
print(f"  Exporté : {SORTIE/'kpi_segments_nov2026.csv'}")
print(f"  Exporté : {chemin_png}")
print("  ✓ Pipeline complet terminé")"""),

# ── EXERCICE FINAL ──────────────────────────────────────────
md("""---
# 🏁 Exercice final Jour 3 · Rapport analytique par langue

**Votre mission :** Créer un rapport qui compare l'activité des clients
francophones vs néerlandophones.

**Métriques à calculer :**
- Nombre de clients actifs PP par langue
- Solde moyen des contrats actifs par langue
- Nombre moyen de transactions 13 mois par client et par langue
- Évolution mensuelle des transactions par langue (courbe)

**Format attendu :**
- Tableau synthétique (DataFrame)
- Graphique : deux courbes (FR et NL) sur le même axe
- Export CSV

**Indice :** utiliser `groupby(["PERIODE","COD_LNG_CTR"])` pour la série temporelle par langue."""),

code("""# 🟡 Exercice final — votre code ────────────────────────────
print("À compléter !")"""),

md("""**✅ Correction exercice final :**"""),

code("""# ✅ CORRECTION exercice final ──────────────────────────────

# ── Données de base ───────────────────────────────────────────
DATE_REF_F   = pd.Timestamp("2026-10-31")
DATE_DEBUT_F = DATE_REF_F - DateOffset(months=12)

# Filtrer PP uniquement
vue_pp = vue_p[vue_p["COD_TYP_TIE"]=="1"].copy()

# ── KPIs par langue ────────────────────────────────────────────
kpi_lng = vue_pp[vue_pp["CAT_ECV"]=="Actif"].groupby("COD_LNG_CTR").agg(
    NB_CLIENTS_ACTIFS = ("IDT_PI",     "nunique"),
    NB_CTR_ACTIFS     = ("IDT_AC",     "count"),
    SLD_MOY           = ("SLD_CTR",    "mean"),
    MOY_TXN_PAR_CTR   = ("NB_TXN_13M", "mean"),
).round(2).reset_index()
kpi_lng["LABEL_LNG"] = kpi_lng["COD_LNG_CTR"].map({"FR":"Français","NL":"Néerlandais"})

print("=== KPIs par langue (PP actifs) ===")
print(kpi_lng[["LABEL_LNG","NB_CLIENTS_ACTIFS","NB_CTR_ACTIFS","SLD_MOY","MOY_TXN_PAR_CTR"]].to_string(index=False))

# ── Série temporelle par langue ───────────────────────────────
# Joindre txn_13m_p avec la langue du client
txn_lng = pd.merge(
    txn_13m_p[["IDT_AC","PERIODE","NUM_ORD_MVT_CPB"]],
    txc_p[["IDT_AC","IDT_PI"]], on="IDT_AC", how="left"
)
txn_lng = pd.merge(txn_lng, tie_p[["IDT_PI","COD_LNG_CTR"]], on="IDT_PI", how="left")

serie_lng = (
    txn_lng.groupby(["PERIODE","COD_LNG_CTR"], observed=True)["NUM_ORD_MVT_CPB"]
    .count()
    .reset_index()
)
serie_lng.columns = ["PERIODE","LANGUE","NB_TXN"]
serie_lng = serie_lng.sort_values(["LANGUE","PERIODE"])

# Pivoter pour avoir FR et NL en colonnes
serie_pivot = serie_lng.pivot(index="PERIODE", columns="LANGUE", values="NB_TXN").fillna(0)

# ── Graphique comparatif ──────────────────────────────────────
fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(12, 8))
fig.suptitle("Activité par langue — 13 mois glissants (PP)", fontsize=14, fontweight="bold")

# Courbes FR vs NL
x_pos = range(len(serie_pivot))
lab_x  = [str(p) for p in serie_pivot.index]
if "FR" in serie_pivot.columns:
    ax_top.plot(x_pos, serie_pivot["FR"], "o-", color="#1E88E5", linewidth=2.5,
                markersize=6, label="Français (FR)")
if "NL" in serie_pivot.columns:
    ax_top.plot(x_pos, serie_pivot["NL"], "s--", color="#FDD835", linewidth=2.5,
                markersize=6, label="Néerlandais (NL)")
ax_top.set_title("Transactions mensuelles FR vs NL", fontsize=12)
ax_top.set_ylabel("Nb transactions")
ax_top.set_xticks(x_pos)
ax_top.set_xticklabels(lab_x, rotation=45, ha="right", fontsize=8)
ax_top.legend()
ax_top.grid(alpha=0.3)
ax_top.spines[["top","right"]].set_visible(False)

# Barres KPIs
ax_bot.bar(kpi_lng["LABEL_LNG"], kpi_lng["SLD_MOY"], color=["#1E88E5","#FDD835"],
           edgecolor="white")
ax_bot.set_title("Solde moyen des contrats actifs par langue", fontsize=12)
ax_bot.set_ylabel("EUR")
ax_bot.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax_bot.spines[["top","right"]].set_visible(False)
for b in ax_bot.patches:
    ax_bot.text(b.get_x()+b.get_width()/2, b.get_height()+50,
                f"{b.get_height():,.0f}", ha="center", fontsize=11)

plt.tight_layout()
plt.savefig(SORTIE/"rapport_langue_fr_nl.png", dpi=150, bbox_inches="tight")
plt.show()
print(f"Graphique exporté → {SORTIE/'rapport_langue_fr_nl.png'}")"""),

md("""---
# Récapitulatif de la formation 3 jours

## Ce que vous maîtrisez maintenant

### Jour 1 — Fondamentaux Python
- Variables, types (str, int, float, bool)
- Conditions `if/elif/else`, opérateurs `and/or/not`
- Boucles `for`, `while`, `range()`, `enumerate()`, `zip()`
- Listes, tuples, dictionnaires
- Fonctions avec `def`, paramètres par défaut, `return`, `lambda`
- Gestion des erreurs `try/except`
- Lecture CSV avec `csv.DictReader`

### Jour 2 — Fichiers, Pandas, SQL
- `pathlib.Path` : chemins portables
- `csv`, `json` : lecture/écriture de fichiers
- Chargement des 5 tables Beobank avec `pd.read_csv(sep=";", na_values=".")`
- Exploration : `head()`, `info()`, `describe()`, `value_counts()`
- Sélection `.loc`, `.iloc`, filtres booléens
- Colonnes calculées : `np.where`, `np.select`, `.map()`, `.apply()`, `pd.cut()`
- Dates : `pd.to_datetime()`, `.dt.year`, `.dt.to_period()`
- `groupby().agg()` : agrégations
- `pd.merge()` : jointures left/inner/outer
- Export `to_csv()`, connexion SQLite, `pd.read_sql()`

### Jour 3 — SQL Analytique, Time Series, Visualisation
- CTEs (WITH) : sous-requêtes nommées et chaînées
- Window functions : `OVER PARTITION BY`, `ROW_NUMBER`, `LAG`, `LEAD`
- Équivalents Pandas : `.transform()`, `.cumcount()`, `.shift()`
- Fenêtre glissante 13 mois avec `DateOffset`
- Séries temporelles : `to_period()`, `rolling()`, `cumsum()`
- Matplotlib : `bar`, `barh`, `plot`, `pie`, double axe `twinx()`
- Dashboard avec `GridSpec`
- Pipeline complet : Import → Nettoyage → Transform → SQL → Export + Viz

## Ressources pour continuer

- **Pandas** : pandas.pydata.org/docs
- **Matplotlib** : matplotlib.org/stable/gallery
- **SQL in Python** : docs.python.org/3/library/sqlite3.html
- **Exercices pratiques** : kaggle.com/learn (Python + Pandas gratuits)
- **Communauté** : stackoverflow.com/questions/tagged/pandas"""),
]

chemin = os.path.join(OUT, "Jour3_SQL_TimeSeries_Visualisation.ipynb")
with open(chemin, "w", encoding="utf-8") as f:
    json.dump(nb(cells), f, ensure_ascii=False, indent=1)
print(f"Jour 3 : {os.path.getsize(chemin)//1024} Ko — {len(cells)} cellules")
