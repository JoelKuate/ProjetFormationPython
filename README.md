# Formation Python 3 jours — Beobank · Orsys

Formation complète de transition **SAS → Python** pour les analystes de données Beobank.
Durée : 3 jours · Niveau : débutant absolu en Python · Public : analystes SAS/données bancaires.

---

## Contenu du dossier

```
Beobank/
│
├── README.md                          ← ce fichier
├── programme_final_valide_python_beobank.txt   ← syllabus officiel
├── ORSYS - Programme Python - Beobank (1).pdf  ← programme Orsys
│
├── Orsys/                             ← données réelles Beobank (5 tables CSV)
│   ├── CTR.csv                        ← Contrats (200 lignes)
│   ├── TIE.csv                        ← Clients / Tiers (100 lignes)
│   ├── TIE_ADR.csv                    ← Adresses (100 lignes)
│   ├── TIE_X_CTR.csv                  ← Liens client ↔ contrat (200 lignes)
│   └── TXN_X_CTR.csv                  ← Transactions (1 260 lignes)
│
├── Formation_Complete/                ← ✅ VERSION FINALE RECOMMANDÉE
│   ├── Jour1_Fondamentaux_Python.ipynb
│   ├── Jour2_Fichiers_Pandas_SQL.ipynb
│   └── Jour3_SQL_TimeSeries_Visualisation.ipynb
│
├── Notebooks/                         ← Version intermédiaire (v2)
│   ├── Jour1_Fondamentaux_Python.ipynb
│   ├── Jour2_Fichiers_Pandas.ipynb
│   └── Jour3_SQL_TimeSeries_Visualisation.ipynb
│
└── (générateurs Python — voir section Technique)
```

---

## Les données Beobank

Toutes les tables sont en format CSV avec les conventions suivantes :

| Paramètre | Valeur |
|-----------|--------|
| Séparateur | `;` (point-virgule) |
| Valeur manquante | `.` (convention SAS) |
| Encodage | `UTF-8` |
| Dates standard | `YYYY-MM-DD` |
| Dates SAS (TIE_ADR) | `DDMONYYYY` ex : `24NOV2025` |

### Description des tables

| Table | Contenu | Lignes | Clé primaire |
|-------|---------|--------|--------------|
| `CTR.csv` | Contrats (comptes bancaires) | 200 | `IDT_AC` |
| `TIE.csv` | Clients (tiers) | 100 | `IDT_PI` |
| `TIE_ADR.csv` | Adresses des clients | 100 | `IDT_PI` |
| `TIE_X_CTR.csv` | Liens client ↔ contrat | 200 | `IDT_PI` + `IDT_AC` |
| `TXN_X_CTR.csv` | Transactions | 1 260 | `IDT_AC` + `NUM_ORD_MVT_CPB` |

### Colonnes principales

**CTR.csv — Contrats**

| Colonne | Type | Description |
|---------|------|-------------|
| `IDT_AC` | str | Identifiant du compte (clé) |
| `REF_CTR_INN` | str | Référence interne du contrat |
| `DAT_OUV_CTR` | date | Date d'ouverture |
| `COD_ECV_CTR` | str | Statut : 1=Ouvert, 2=En attente, 3=Suspendu, 4=Clôturé, 5=En résiliation, 6=Résilié |
| `COD_DEV` | str | Devise (EUR, USD...) |
| `SLD_CTR` | float | Solde du contrat |
| `MNT_INI` | float | Montant initial |
| `SLD_DSP` | float | Solde disponible |

**TIE.csv — Clients**

| Colonne | Type | Description |
|---------|------|-------------|
| `IDT_PI` | str | Identifiant client (clé) |
| `COD_TYP_TIE` | str | Type : 1=Personne physique, 2=Personne morale |
| `COD_SEX` | str | Sexe : M / F |
| `COD_LNG_CTR` | str | Langue : FR / NL |
| `DAT_NAI` | date | Date de naissance (YYYY-MM-DD) |
| `DAT_DCS` | date | Date de décès (si applicable) |

---

## Les notebooks — quelle version choisir ?

### ✅ `Formation_Complete/` — Version finale recommandée

La version la plus complète, conçue pour des débutants absolus.

| Notebook | Contenu | Cellules |
|----------|---------|----------|
| `Jour1_Fondamentaux_Python.ipynb` | Bases Python : variables, conditions, boucles, listes, dicts, fonctions, try/except, lecture CSV | 81 |
| `Jour2_Fichiers_Pandas_SQL.ipynb` | Pathlib, Pandas complet, jointures, groupby, export, SQLite | 86 |
| `Jour3_SQL_TimeSeries_Visualisation.ipynb` | CTEs, window functions, time series, Matplotlib, dashboard, pipeline complet | 51 |

**Caractéristiques :**
- Chaque ligne de code est commentée
- Un exercice après chaque concept (pas seulement à la fin de la section)
- Correction fournie immédiatement après chaque exercice
- Tout le code s'appuie sur les vraies données Beobank
- Fil rouge : analyste produisant le rapport mensuel du portefeuille

### `Notebooks/` — Version intermédiaire (v2)

Version avec exercices par section (moins granulaire que Formation_Complete).
Peut servir de référence ou de support complémentaire.

---

## Programme jour par jour

### Jour 1 · Fondamentaux Python

> *Objectif : maîtriser les briques de base pour comprendre ce que Pandas fait en coulisses*

| Heure | Thème | Exercice |
|-------|-------|---------|
| Matin | Python vs SAS — syntaxe, variables, types, f-strings | Ex. 1 : calcul d'intérêts |
| Matin | Conditions `if/elif/else`, opérateurs `and/or/not` | Ex. 2 : classifier statut ECV |
| Après-midi | Boucles `for`, `while`, `range()`, `enumerate()` | Ex. 3 : analyse de codes statut |
| Après-midi | Listes, list comprehensions | Ex. 4 : filtrer les soldes |
| Après-midi | Tuples et déballage | Ex. 5 : classifier les clients |
| Fin de journée | Dictionnaires et mappings | Ex. 6 : libellés depuis codes |
| Fin de journée | Fonctions, lambda, try/except | Ex. 7-8 : enrichissement robuste |
| Fin de journée | Lecture CSV avec `csv.DictReader` | Ex. 9 + Final : rapport d'inventaire |

### Jour 2 · Fichiers, Pandas et SQL

> *Objectif : remplacer PROC IMPORT, PROC MEANS, PROC SORT, PROC SQL en quelques lignes*

| Heure | Thème | Exercice |
|-------|-------|---------|
| Matin | `pathlib.Path`, lecture/écriture CSV et JSON | Ex. 1-2 |
| Matin | Chargement des 5 tables avec `pd.read_csv(sep=";", na_values=".")` | — |
| Matin | Exploration : `head()`, `info()`, `describe()`, `value_counts()` | Ex. 3 |
| Après-midi | Sélection `.loc`, `.iloc`, colonnes multiples | Ex. 4 |
| Après-midi | Filtres booléens `&`, `|`, `~`, `isin()`, `isna()`, `sort_values()` | Ex. 5 |
| Après-midi | Colonnes calculées : `np.where`, `np.select`, `.map()`, `pd.cut()`, `pd.to_datetime()` | Ex. 6 |
| Fin de journée | `groupby().agg()` — agrégations multi-colonnes | Ex. 7 |
| Fin de journée | `pd.merge()` — jointures left/inner/outer | Ex. 8 |
| Fin de journée | Export CSV/JSON, connexion SQLite, `pd.read_sql()` | Ex. 9 + Final |

### Jour 3 · SQL Analytique, Time Series et Visualisation

> *Objectif : maîtriser les analyses avancées et produire des graphiques pour les rapports*

| Heure | Thème | Exercice |
|-------|-------|---------|
| Matin | CTEs (WITH) : sous-requêtes nommées | Ex. 1 |
| Matin | Window functions : `OVER PARTITION BY`, `.transform()` | Ex. 2 |
| Matin | `ROW_NUMBER`, `LAG`, `LEAD` — `.cumcount()`, `.shift()` | Ex. 3 |
| Après-midi | Manipulation des dates, composantes `.dt`, durées | Ex. 4 |
| Après-midi | Fenêtre glissante 13 mois — `DateOffset`, `rolling()` | Ex. 5 |
| Après-midi | Matplotlib : barres, barres horizontales, courbes, camembert | Ex. 6 |
| Fin de journée | Dashboard GridSpec multi-graphiques | — |
| Fin de journée | **Pipeline complet 5 étapes** : Import → Nettoyage → Transform → SQL → Export+Viz | Final |

---

## Prérequis techniques

### Environnement recommandé

```
Python 3.9+
JupyterLab ou Jupyter Notebook (ou VS Code avec extension Jupyter)
```

### Installation des bibliothèques

```bash
pip install pandas numpy matplotlib jupyter
```

### Lancer les notebooks

```bash
# Depuis le dossier Beobank/
jupyter lab
# Ouvrir Formation_Complete/Jour1_Fondamentaux_Python.ipynb
```

> **Important :** les notebooks utilisent le chemin relatif `../Orsys/` pour accéder aux données.
> Ils doivent être ouverts depuis le dossier `Formation_Complete/` ou `Notebooks/`.

---

## Chargement standard des données

Copier-coller ce bloc en début de session pour charger les 5 tables :

```python
import pandas as pd
import numpy as np
from pathlib import Path

DATA   = Path("../Orsys")
PARAMS = dict(sep=";", na_values=".", encoding="utf-8")

ctr     = pd.read_csv(DATA / "CTR.csv",       **PARAMS)   # 200 contrats
tie     = pd.read_csv(DATA / "TIE.csv",       **PARAMS)   # 100 clients
tie_adr = pd.read_csv(DATA / "TIE_ADR.csv",   **PARAMS)   # 100 adresses
txc     = pd.read_csv(DATA / "TIE_X_CTR.csv", **PARAMS)   # 200 liens
txn     = pd.read_csv(DATA / "TXN_X_CTR.csv", **PARAMS)   # 1 260 transactions
```

---

## Correspondance SAS → Python

| SAS | Python / Pandas |
|-----|----------------|
| `data work.CTR; set "CTR.csv"; run;` | `ctr = pd.read_csv("CTR.csv", sep=";", na_values=".")` |
| `proc print data=CTR(obs=5);` | `ctr.head(5)` |
| `proc contents data=CTR;` | `ctr.info()` |
| `proc means data=CTR;` | `ctr.describe()` |
| `proc freq data=CTR; tables COD_ECV_CTR;` | `ctr["COD_ECV_CTR"].value_counts()` |
| `proc sort data=CTR by SLD_CTR;` | `ctr.sort_values("SLD_CTR")` |
| `where COD_ECV_CTR in ("1","2","3");` | `ctr[ctr["COD_ECV_CTR"].isin(["1","2","3"])]` |
| `where SLD_CTR = .;` | `ctr[ctr["SLD_CTR"].isna()]` |
| `data CTR2; set CTR; SEGMENT=...; run;` | `ctr["SEGMENT"] = np.select(conditions, valeurs)` |
| `proc sql; select ... group by ...; quit;` | `ctr.groupby("col").agg(N=("col","count"))` |
| `proc sql; left join ...; quit;` | `pd.merge(ctr, tie, on="IDT_AC", how="left")` |
| `proc export; outfile="out.csv"; run;` | `ctr.to_csv("out.csv", sep=";", index=False)` |
| `FORMAT COD_ECV_CTR $STATUT.;` | `ctr["LIB"] = ctr["COD_ECV_CTR"].map({"1":"Ouvert",...})` |
| `LAG(col)` | `df["col"].shift(1)` |
| `OVER (PARTITION BY col)` | `df.groupby("col")["val"].transform("sum")` |

---

## Fichiers techniques (générateurs)

Les notebooks sont générés par des scripts Python. En cas de modification souhaitée,
éditer le générateur correspondant puis le ré-exécuter :

| Générateur | Notebook produit | Version |
|-----------|-----------------|---------|
| `gen_fc_j1.py` | `Formation_Complete/Jour1_Fondamentaux_Python.ipynb` | Finale |
| `gen_fc_j2.py` | `Formation_Complete/Jour2_Fichiers_Pandas_SQL.ipynb` | Finale |
| `gen_fc_j3.py` | `Formation_Complete/Jour3_SQL_TimeSeries_Visualisation.ipynb` | Finale |
| `gen_j1_v2.py` | `Notebooks/Jour1_Fondamentaux_Python.ipynb` | V2 |
| `gen_j2_v2.py` | `Notebooks/Jour2_Fichiers_Pandas.ipynb` | V2 |
| `gen_j3_v2.py` | `Notebooks/Jour3_SQL_TimeSeries_Visualisation.ipynb` | V2 |

```bash
# Régénérer tous les notebooks Formation_Complete
python gen_fc_j1.py
python gen_fc_j2.py
python gen_fc_j3.py
```

---

## Contact et contexte

Formation assurée par **Orsys** pour les équipes analytiques de **Beobank**.  
Objectif : migration des traitements SAS vers Python dans le cadre de la modernisation
de la chaîne analytique data de Beobank.
