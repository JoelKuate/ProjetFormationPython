"""
Formation Complete - Jour 1 - Fondamentaux Python
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

# ════════════════════════════════════════════════════════════════
# PAGE DE GARDE
# ════════════════════════════════════════════════════════════════
md("""# Jour 1 · Fondamentaux Python pour analystes Beobank
### Formation Python 3 jours · 18 novembre 2026

---

## Votre mission aujourd'hui

Vous êtes **analyste chez Beobank**. Votre direction a décidé de migrer les traitements
analytiques de **SAS vers Python**. Pendant 3 jours, vous allez apprendre Python
en travaillant sur les vraies données Beobank.

## Les 5 tables avec lesquelles vous travaillerez

| Fichier | Contenu | Lignes | Clé |
|---------|---------|--------|-----|
| `CTR.csv` | Contrats (comptes bancaires) | 200 | `IDT_AC` |
| `TIE.csv` | Clients (tiers) | 100 | `IDT_PI` |
| `TIE_ADR.csv` | Adresses des clients | 100 | `IDT_PI` |
| `TIE_X_CTR.csv` | Liens client ↔ contrat | 200 | `IDT_PI` + `IDT_AC` |
| `TXN_X_CTR.csv` | Transactions | 1 260 | `IDT_AC` + `NUM_ORD_MVT_CPB` |

## Mode d'emploi du notebook

- **Cellule grise** = code Python → `Shift + Entrée` pour exécuter
- **Cellule blanche** = explication (markdown) → pas besoin d'exécuter
- **🟡 Exercice** = cellule à compléter vous-même
- **✅ Correction** = cellule de correction juste en dessous

> **Règle d'or :** lisez chaque commentaire `#` dans le code. Ils expliquent tout.

---

## Ce que vous saurez faire à la fin de cette journée

- Utiliser les types de base Python (str, int, float, bool)
- Écrire des conditions `if/elif/else`
- Itérer avec des boucles `for` et `while`
- Manipuler des listes, tuples et dictionnaires
- Écrire et appeler des fonctions
- Gérer les erreurs avec `try/except`
- Lire un fichier CSV Beobank avec Python pur"""),

# ════════════════════════════════════════════════════════════════
# SECTION 1 · POSITIONNEMENT PYTHON / SAS
# ════════════════════════════════════════════════════════════════
md("""---
# 1 · Python vs SAS — ce qui change, ce qui reste

## 1.1 Les différences essentielles

| Point | SAS | Python |
|-------|-----|--------|
| Fin d'instruction | `;` obligatoire | Rien (saut de ligne) |
| Blocs de code | `DO ... END;` | Indentation (4 espaces) |
| Commentaire | `/* ... */` ou `*` | `#` ou `'''...'''` |
| Affichage | `put "texte";` | `print("texte")` |
| Variable | déclarée dans un data step | assignée directement |
| Valeur manquante | `.` (point) | `None` ou `NaN` |
| Exécution | par étape (`run;`) | ligne par ligne |

## 1.2 Ce qui ne change PAS

- Votre logique métier (calcul d'écheance, classification de solde...)
- Les concepts SQL (JOIN, GROUP BY, ORDER BY)
- La structure des données tabulaires (lignes × colonnes)
- Votre expertise du domaine bancaire Beobank"""),

code("""# ── Votre premier programme Python ─────────────────────────
# print() : la fonction d'affichage Python (équivalent de PUT en SAS)
# Les guillemets délimitent une chaîne de caractères

print("Bonjour, je suis analyste chez Beobank !")

# On peut afficher plusieurs éléments séparés par une virgule
# Python ajoute automatiquement un espace entre eux
print("Tables disponibles :", 5)

# On peut faire des calculs directement dans print()
print("200 contrats + 100 clients =", 200 + 100, "enregistrements")

# Une ligne vide : print() sans argument
print()
print("Python est prêt.")"""),

# ════════════════════════════════════════════════════════════════
# SECTION 2 · VARIABLES ET TYPES
# ════════════════════════════════════════════════════════════════
md("""---
# 2 · Variables et types de données

## 2.1 Créer une variable

En Python, pas besoin de déclarer le type : Python le déduit automatiquement.

```python
# SAS (data step)               # Python
nom = "DUPONT";                  nom = "DUPONT"
age = 42;                        age = 42
solde = 15234.87;                solde = 15234.87
actif = 1;                       actif = True
```

## 2.2 Les 4 types de base

| Type | Nom Python | Exemple | Usage |
|------|-----------|---------|-------|
| Texte | `str` | `"EUR"`, `"CTR-001"` | Codes, références, noms |
| Entier | `int` | `200`, `-5`, `0` | Comptages, indices |
| Décimal | `float` | `15234.87`, `0.02` | Soldes, taux |
| Booléen | `bool` | `True`, `False` | Flags, conditions |"""),

code("""# ── Les 4 types de base illustrés avec des données Beobank ──
# Chaque ligne : NomVariable = Valeur
# Python choisit le type automatiquement selon la valeur assignée

# str (string) : texte — toujours entre guillemets simples ou doubles
code_statut = "1"               # COD_ECV_CTR : statut d'un contrat
ref_contrat = "CTR-2024-00137"  # référence interne du contrat
devise      = "EUR"             # devise : EUR, USD, GBP...
langue      = "FR"              # langue : FR ou NL chez Beobank

# int (integer) : nombre entier — sans guillemets, sans point décimal
nb_contrats = 200               # nombre total de contrats dans CTR.csv
nb_clients  = 100               # nombre total de clients dans TIE.csv
nb_txn      = 1260              # nombre de transactions dans TXN_X_CTR.csv
rang        = 1                 # position dans un classement

# float (floating point) : nombre décimal — le point est le séparateur décimal
solde_ctr   = 15234.87          # solde du contrat (SLD_CTR)
montant_ini = 10000.00          # montant initial (MNT_INI)
taux_frais  = 0.0125            # taux de frais = 1.25 %
solde_dsp   = 8750.50           # solde disponible (SLD_DSP)

# bool (boolean) : vrai ou faux — TOUJOURS avec majuscule initiale
est_actif     = True            # le contrat est-il actif ?
est_titulaire = False           # est-ce le titulaire principal ?

# ── Afficher et vérifier les types ───────────────────────────
# type() retourne le type de la variable
print(f"code_statut = '{code_statut}'   → type : {type(code_statut).__name__}")
print(f"nb_contrats = {nb_contrats}       → type : {type(nb_contrats).__name__}")
print(f"solde_ctr   = {solde_ctr}   → type : {type(solde_ctr).__name__}")
print(f"est_actif   = {est_actif}         → type : {type(est_actif).__name__}")"""),

code("""# ── Les f-strings : formater l'affichage ─────────────────────
# La lettre f devant les guillemets active les f-strings
# {variable} dans le texte est remplacé par la valeur de la variable
# {:format} permet de contrôler l'affichage

ref_contrat = "CTR-2024-00137"
solde_ctr   = 15234.87
devise      = "EUR"
code_statut = "1"

# f-string simple : insertion d'une variable
print(f"Contrat : {ref_contrat}")

# f-string avec format numérique
# ,.2f = séparateur de milliers, 2 décimales, format flottant
print(f"Solde : {solde_ctr:,.2f} {devise}")

# f-string avec alignement
# >10 = aligné à droite sur 10 caractères
# <15 = aligné à gauche sur 15 caractères
print(f"{'Référence':<20} : {ref_contrat}")
print(f"{'Solde':<20} : {solde_ctr:>12,.2f} {devise}")
print(f"{'Statut':<20} : {code_statut}")

# Concatenation alternative avec +
# str() convertit n'importe quoi en texte
message = "Contrat " + ref_contrat + " → statut " + str(code_statut)
print(message)"""),

code("""# ── Opérations arithmétiques ─────────────────────────────────
# Les 7 opérateurs arithmétiques Python

solde_ini     = 20000.00   # solde de départ
depot         = 1500.00    # dépôt reçu
retrait       = 800.00     # retrait effectué
taux_annuel   = 0.015      # taux annuel = 1.5 %

# Addition : +
solde_apres_depot = solde_ini + depot
print(f"Après dépôt    : {solde_apres_depot:,.2f} EUR")

# Soustraction : -
solde_apres_retrait = solde_ini - retrait
print(f"Après retrait  : {solde_apres_retrait:,.2f} EUR")

# Multiplication : *
interets_annuels = solde_ini * taux_annuel
print(f"Intérêts/an    : {interets_annuels:,.2f} EUR")

# Division : /  (toujours donne un float)
taux_mensuel = taux_annuel / 12
print(f"Taux mensuel   : {taux_mensuel:.4f} ({taux_mensuel*100:.3f} %)")

# Division entière : // (partie entière seulement)
nb_mois_complets = int(solde_ini) // 1000
print(f"Tranches de 1k : {nb_mois_complets}")

# Modulo : %  (reste de la division entière)
reste = 200 % 7    # 200 divisé par 7 → quotient 28, reste 4
print(f"200 mod 7      : {reste}")

# Puissance : **
capital_fin_5ans = solde_ini * (1 + taux_annuel) ** 5
print(f"Capital 5 ans  : {capital_fin_5ans:,.2f} EUR")"""),

# ── EXERCICE 1 ──────────────────────────────────────────────
md("""---
### 🟡 Exercice 1 · Variables et calculs Beobank

**Contexte :** Un client Beobank vient d'ouvrir un contrat avec les caractéristiques suivantes :
- Référence : `"CTR-2026-00842"`
- Solde initial : `25 000 EUR`
- Frais mensuels de tenue de compte : `18.50 EUR`
- Taux d'intérêt annuel : `0.75 %`
- Langue du client : `"NL"`

**À faire :**
1. Créer une variable pour chaque information
2. Calculer : `solde_apres_1_an` = solde initial + intérêts d'un an − frais de 12 mois
3. Calculer : `gain_net` = solde_apres_1_an − solde initial
4. Afficher un résumé avec f-strings formatées"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────

# 1. Créer les variables
ref_contrat    = ...
solde_ini      = ...
frais_mensuel  = ...
taux_annuel    = ...
langue         = ...

# 2. Calculs
interets_annuels  = ...   # solde_ini * taux_annuel
frais_annuels     = ...   # frais_mensuel * 12
solde_apres_1_an  = ...   # solde_ini + interets - frais

# 3. Gain net
gain_net = ...

# 4. Affichage
print(f"Contrat          : {ref_contrat}")
print(f"Solde initial    : ... EUR")
print(f"Intérêts (1 an)  : ... EUR")
print(f"Frais (12 mois)  : ... EUR")
print(f"Solde après 1 an : ... EUR")
print(f"Gain net         : ... EUR")"""),

md("""**✅ Correction exercice 1 :**"""),

code("""# ✅ CORRECTION exercice 1 ──────────────────────────────────

# 1. Variables
ref_contrat   = "CTR-2026-00842"
solde_ini     = 25000.0
frais_mensuel = 18.50
taux_annuel   = 0.0075    # 0.75 % en décimal
langue        = "NL"

# 2. Calculs intermédiaires
interets_annuels = solde_ini * taux_annuel     # 25000 × 0.0075 = 187.50
frais_annuels    = frais_mensuel * 12          # 18.50 × 12 = 222.00
solde_apres_1_an = solde_ini + interets_annuels - frais_annuels  # 24 965.50

# 3. Gain net (peut être négatif)
gain_net = solde_apres_1_an - solde_ini        # 187.50 − 222.00 = −34.50

# 4. Affichage formaté
print("=" * 40)
print(f"  Contrat : {ref_contrat}")
print(f"  Langue  : {langue}")
print("=" * 40)
print(f"  Solde initial     : {solde_ini:>12,.2f} EUR")
print(f"  Intérêts (1 an)   : {interets_annuels:>12,.2f} EUR")
print(f"  Frais (12 mois)   : {frais_annuels:>12,.2f} EUR")
print(f"  Solde après 1 an  : {solde_apres_1_an:>12,.2f} EUR")
print(f"  Gain net          : {gain_net:>+12,.2f} EUR")   # + = toujours afficher le signe
print("=" * 40)
if gain_net < 0:
    print(f"  ⚠ Les frais dépassent les intérêts de {abs(gain_net):.2f} EUR")
else:
    print(f"  ✓ Le compte est bénéficiaire")"""),

# ════════════════════════════════════════════════════════════════
# SECTION 3 · CONDITIONS
# ════════════════════════════════════════════════════════════════
md("""---
# 3 · Conditions — if / elif / else

## 3.1 Structure

```python
if condition_1:          # SI la condition 1 est vraie
    ...                  # exécuter ce bloc (indenté de 4 espaces)
elif condition_2:        # SINON SI la condition 2 est vraie
    ...
else:                    # SINON (aucune condition n'est vraie)
    ...
```

## 3.2 Opérateurs de comparaison

| Opérateur | Signification | Exemple |
|-----------|--------------|---------|
| `==` | égal à | `cod == "1"` |
| `!=` | différent de | `dev != "EUR"` |
| `>` | strictement supérieur | `solde > 0` |
| `>=` | supérieur ou égal | `age >= 18` |
| `<` | strictement inférieur | `solde < 0` |
| `<=` | inférieur ou égal | `taux <= 0.05` |
| `in` | appartient à | `cod in ("1","2","3")` |
| `not in` | n'appartient pas à | `dev not in ("EUR","USD")` |
| `is None` | est manquant | `dat_clo is None` |

## 3.3 Combinaison : and / or / not

| Opérateur | Signification | Vrai si |
|-----------|--------------|---------|
| `and` | ET logique | les DEUX conditions sont vraies |
| `or` | OU logique | AU MOINS UNE condition est vraie |
| `not` | NON logique | la condition est fausse |"""),

code("""# ── Classifier le statut d'un contrat CTR ────────────────────
# COD_ECV_CTR : code statut dans la table CTR.csv
# 1=Ouvert, 2=En attente, 3=Suspendu, 4=Cloturé, 5=En résiliation, 6=Résilié

cod_ecv_ctr = "3"   # ← modifiez cette valeur pour tester (1 à 6)

# Structure if/elif/else : Python teste les conditions dans l'ordre
# et exécute le PREMIER bloc dont la condition est vraie
if cod_ecv_ctr == "1":           # si le code est exactement "1"
    libelle   = "Ouvert"
    categorie = "Actif"
    priorite  = "Normale"
elif cod_ecv_ctr == "2":         # sinon si le code est "2"
    libelle   = "En attente"
    categorie = "Actif"
    priorite  = "Surveillance"
elif cod_ecv_ctr == "3":         # sinon si le code est "3"
    libelle   = "Suspendu"
    categorie = "Actif"
    priorite  = "Urgente"
elif cod_ecv_ctr == "4":
    libelle   = "Cloturé"
    categorie = "Inactif"
    priorite  = "Aucune"
elif cod_ecv_ctr == "5":
    libelle   = "En résiliation"
    categorie = "Inactif"
    priorite  = "Critique"
elif cod_ecv_ctr == "6":
    libelle   = "Résilié"
    categorie = "Inactif"
    priorite  = "Aucune"
else:                            # aucune condition précédente n'est vraie
    libelle   = "Inconnu"
    categorie = "Inconnu"
    priorite  = "Inconnue"

print(f"Code    : {cod_ecv_ctr}")
print(f"Libellé : {libelle}")
print(f"Catégorie : {categorie}")
print(f"Priorité  : {priorite}")"""),

code("""# ── Conditions combinées avec and / or ───────────────────────
# IMPORTANT : en Python (contrairement à SAS), pas de "and then"
# Les opérateurs logiques s'écrivent : and, or, not (en minuscules)

solde      = 15234.87   # solde du contrat
cod_ecv    = "1"        # statut
cod_dev    = "EUR"      # devise
age_client = 45         # âge du client

# Condition AND : les deux doivent être vraies
if solde > 10000 and cod_ecv in ("1", "2", "3"):
    print("Contrat Premium actif")   # affiché seulement si solde > 10k ET actif

# Condition OR : au moins une doit être vraie
if cod_ecv == "5" or cod_ecv == "6":
    print("Action requise : résiliation")
else:
    print("Pas de résiliation en cours")

# NOT : inverse la condition
if not (cod_dev == "EUR"):          # si la devise n'est PAS l'euro
    print(f"Attention : devise {cod_dev} (non-EUR)")
else:
    print("Devise EUR (standard)")

# Condition complexe (3 critères)
# Éligible à l'offre Private si : solde > 50k ET actif ET client > 30 ans
if solde > 50000 and cod_ecv in ("1","2","3") and age_client > 30:
    offre = "Private Banking"
elif solde > 10000 and cod_ecv in ("1","2","3"):
    offre = "Premium"
elif cod_ecv in ("1","2","3"):
    offre = "Standard"
else:
    offre = "Aucune (compte inactif)"

print(f"Offre recommandée : {offre}")"""),

code("""# ── Condition sur une valeur manquante ───────────────────────
# En Python, None représente l'absence de valeur (équivalent du "." SAS)
# Attention : None != 0 et None != ""

dat_clo_ctr  = None          # date de clôture manquante (contrat non clôturé)
dat_nai      = "1978-09-15"  # date de naissance renseignée

# is None : tester si une valeur est manquante
if dat_clo_ctr is None:
    print("Contrat en cours (pas de date de clôture)")
else:
    print(f"Contrat clôturé le {dat_clo_ctr}")

# is not None : tester si une valeur est présente
if dat_nai is not None:
    print(f"Date de naissance renseignée : {dat_nai}")
else:
    print("Date de naissance manquante")

# ── Expression ternaire (if en une ligne) ─────────────────────
# valeur_si_vrai if condition else valeur_si_faux
# Utile pour les assignations simples

solde = 5000.0
segment = "Premium" if solde >= 10000 else "Standard"   # une seule ligne
print(f"Segment : {segment}")

# Équivalent long :
# if solde >= 10000:
#     segment = "Premium"
# else:
#     segment = "Standard" """),

# ── EXERCICE 2 ──────────────────────────────────────────────
md("""---
### 🟡 Exercice 2 · Conditions Beobank

**Contexte :** La table `TIE.csv` contient `COD_TYP_TIE` (1=PP, 2=PM)
et `COD_SEX` (M=Masculin, F=Féminin). La table `CTR.csv` contient `SLD_CTR`.

**À faire avec les variables données ci-dessous :**
1. Déterminer `type_client` : "Personne physique" ou "Personne morale"
2. Déterminer `civilite` : "M." si M, "Mme" si F, "Inconnu" sinon (seulement pour PP)
3. Déterminer `segment_solde` selon les règles :
   - `SLD_CTR` manquant → "Inconnu"
   - `< 1 000` → "Standard"
   - `1 000 à 9 999` → "Confort"
   - `10 000 à 49 999` → "Premium"
   - `>= 50 000` → "Private"
4. Afficher un résumé complet"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────

cod_typ_tie = "1"        # 1=PP, 2=PM
cod_sex     = "F"        # M ou F
sld_ctr     = 12500.0    # solde — testez aussi avec None

# 1. Type client
# ...

# 2. Civilité (uniquement si personne physique)
# ...

# 3. Segment selon le solde
# ...

# 4. Affichage
# print(f"Type    : {type_client}")
# print(f"Civilité: {civilite}")
# print(f"Segment : {segment_solde}")"""),

md("""**✅ Correction exercice 2 :**"""),

code("""# ✅ CORRECTION exercice 2 ──────────────────────────────────

cod_typ_tie = "1"        # changez pour tester : "1" ou "2"
cod_sex     = "F"        # changez pour tester : "M", "F", ou "X"
sld_ctr     = 12500.0    # changez pour tester : None, 500, 5000, 12500, 75000

# 1. Type client
if cod_typ_tie == "1":
    type_client = "Personne physique"
elif cod_typ_tie == "2":
    type_client = "Personne morale"
else:
    type_client = "Type inconnu"

# 2. Civilité — ne s'applique qu'aux personnes physiques
if cod_typ_tie == "1":       # seulement pour les PP
    if cod_sex == "M":
        civilite = "M."
    elif cod_sex == "F":
        civilite = "Mme"
    else:
        civilite = "Inconnu"
else:
    civilite = "N/A"         # pas de civilité pour une personne morale

# 3. Segment selon le solde
# On teste d'abord None car None > 0 lèverait une erreur
if sld_ctr is None:
    segment_solde = "Inconnu"
elif sld_ctr < 1000:
    segment_solde = "Standard"
elif sld_ctr < 10000:        # implicitement >= 1000 (cas < 1000 déjà traité)
    segment_solde = "Confort"
elif sld_ctr < 50000:
    segment_solde = "Premium"
else:
    segment_solde = "Private"

# 4. Résumé
print(f"Type client   : {type_client}")
print(f"Civilité      : {civilite}")
sld_aff = f"{sld_ctr:,.2f} EUR" if sld_ctr is not None else "N/A"
print(f"Solde         : {sld_aff}")
print(f"Segment       : {segment_solde}")"""),

# ════════════════════════════════════════════════════════════════
# SECTION 4 · BOUCLES
# ════════════════════════════════════════════════════════════════
md("""---
# 4 · Boucles — répéter des instructions

## 4.1 Boucle for

Exécute un bloc pour chaque élément d'une séquence.

```python
for element in sequence:    # pour chaque élément de la séquence
    ...                     # ce bloc s'exécute à chaque itération
```

## 4.2 Boucle while

Exécute un bloc tant qu'une condition est vraie.

```python
while condition:    # tant que la condition est vraie
    ...             # ⚠ s'assurer que la condition deviendra False !
```

## 4.3 range()

Génère une séquence de nombres.

| Appel | Résultat |
|-------|----------|
| `range(5)` | 0, 1, 2, 3, 4 |
| `range(1, 6)` | 1, 2, 3, 4, 5 |
| `range(0, 12, 3)` | 0, 3, 6, 9 |
| `range(10, 0, -1)` | 10, 9, 8, ..., 1 |"""),

code("""# ── Boucle for sur une liste de codes ────────────────────────
# La variable de boucle (ici 'code') prend successivement
# chaque valeur de la liste

codes_ecv = ["1", "2", "3", "4", "5", "6"]   # tous les codes statut Beobank

print("Tous les statuts de contrat :")
print("-" * 35)

for code in codes_ecv:              # pour chaque code dans la liste
    # Déterminer le libellé correspondant
    if code == "1":   libelle = "Ouvert"
    elif code == "2": libelle = "En attente"
    elif code == "3": libelle = "Suspendu"
    elif code == "4": libelle = "Cloturé"
    elif code == "5": libelle = "En résiliation"
    else:             libelle = "Résilié"

    # Ce print est DANS la boucle (indenté) → s'exécute à chaque itération
    print(f"  Code {code} → {libelle}")

# Ce print est HORS de la boucle (non indenté) → s'exécute UNE SEULE fois
print("-" * 35)
print(f"Total : {len(codes_ecv)} codes traités")"""),

code("""# ── Compteurs et accumulateurs dans une boucle ───────────────
# Patron très courant : initialiser AVANT la boucle, incrémenter DEDANS

# Simuler un extrait de la table CTR (soldes et statuts)
soldes  = [12500.0, 0.0, 3200.0, None, 890.0, 45000.0, 150.0, 7800.0, None, 22000.0]
statuts = ["1",     "4", "1",    "6",  "3",   "1",     "5",   "1",    "4",  "1"]

# Initialiser les compteurs AVANT la boucle
nb_total        = 0       # comptera toutes les lignes
nb_actifs       = 0       # comptera les contrats actifs
nb_manquants    = 0       # comptera les soldes manquants (None)
somme_soldes    = 0.0     # accumulera les soldes (pour la moyenne)

for i in range(len(soldes)):        # i prend les valeurs 0, 1, 2, ..., 9
    nb_total += 1                   # += est un raccourci pour nb_total = nb_total + 1
    sld = soldes[i]                 # solde à la position i
    sta = statuts[i]                # statut à la position i

    if sta in ("1", "2", "3"):      # si le statut est actif
        nb_actifs += 1              # incrémenter le compteur d'actifs

    if sld is None:                 # si le solde est manquant
        nb_manquants += 1
    else:
        somme_soldes += sld         # accumuler les soldes valides

# Calcul de la moyenne après la boucle
nb_valides = nb_total - nb_manquants
moyenne = somme_soldes / nb_valides if nb_valides > 0 else 0.0

print(f"Contrats analysés  : {nb_total}")
print(f"Contrats actifs    : {nb_actifs} ({nb_actifs/nb_total:.0%})")
print(f"Soldes manquants   : {nb_manquants}")
print(f"Solde total        : {somme_soldes:,.2f} EUR")
print(f"Solde moyen        : {moyenne:,.2f} EUR")"""),

code("""# ── range() : générer des séquences ─────────────────────────

# range(N) : de 0 à N-1
print("Mois 1 à 12 :")
for mois in range(1, 13):                    # de 1 à 12 inclus
    # strftime simulation : nommer les mois
    noms = ["","Jan","Fév","Mar","Avr","Mai","Jun",
            "Jul","Aoû","Sep","Oct","Nov","Déc"]
    print(f"  Mois {mois:>2} : {noms[mois]}", end="")   # end="" : pas de saut de ligne
    if mois % 4 == 0:                        # tous les 4 mois : saut de ligne
        print()
print()
print()

# range() pour simuler des frais mensuels sur 24 mois
solde    = 10000.0
frais    = 12.50
mois_cnt = 0

print("Évolution du solde sur 24 mois :")
for mois in range(1, 25):                    # de 1 à 24
    solde = solde - frais                    # déduire les frais
    mois_cnt += 1
    if mois % 6 == 0:                        # afficher tous les 6 mois
        print(f"  Mois {mois:>2} : solde = {solde:>10,.2f} EUR")

print(f"Solde final après {mois_cnt} mois : {solde:,.2f} EUR")"""),

code("""# ── enumerate() : numéroter les éléments d'une boucle ─────────
# enumerate(liste) retourne (index, valeur) pour chaque élément
# Très utile quand on a besoin du numéro de ligne ET de la valeur

villes = ["Bruxelles", "Liège", "Anvers", "Gand", "Namur"]

print("Agences Beobank :")
for numero, ville in enumerate(villes, start=1):  # start=1 : commencer à 1 (pas 0)
    print(f"  Agence {numero:>2} : {ville}")

print()

# ── zip() : parcourir deux listes en parallèle ────────────────
# zip(liste1, liste2) : paires (liste1[i], liste2[i])
# S'arrête à la liste la plus courte

refs    = ["CTR-001", "CTR-002", "CTR-003", "CTR-004"]
soldes2 = [12500.0,   0.0,       3200.0,    45000.0]

print("Contrats et soldes :")
for ref, solde in zip(refs, soldes2):     # parcourir les deux listes en même temps
    flag = "★ TOP" if solde >= 10000 else ""
    print(f"  {ref} : {solde:>10,.2f} EUR  {flag}")"""),

code("""# ── Boucle while : simulation de remboursement ───────────────
# while est utile quand on ne sait pas à l'avance combien d'itérations

capital_restant = 15000.0   # capital dû à la banque
mensualite      = 500.0     # paiement mensuel
taux_mensuel    = 0.004     # taux d'intérêt mensuel = 0.4 %
mois            = 0         # compteur de mois

print(f"Capital initial : {capital_restant:,.2f} EUR")
print(f"Mensualité : {mensualite:.2f} EUR / Taux : {taux_mensuel*100:.1f} %/mois")
print()
print(f"{'Mois':>5}  {'Intérêts':>10}  {'Capital':>10}  {'Restant':>12}")
print("-" * 45)

while capital_restant > 0:              # continuer tant qu'il reste du capital
    mois += 1

    interets_mois = capital_restant * taux_mensuel   # intérêts du mois
    remboursement = mensualite - interets_mois        # part de capital remboursée

    if remboursement >= capital_restant:             # si on rembourse plus que le reste
        remboursement = capital_restant              # limiter au capital restant
        capital_restant = 0.0
    else:
        capital_restant -= remboursement             # réduire le capital restant

    if mois <= 5 or capital_restant < 500:           # afficher les 5 premiers mois
        print(f"{mois:>5}  {interets_mois:>10.2f}  {remboursement:>10.2f}  {capital_restant:>12,.2f}")

print(f"\nRemboursement complet en {mois} mois")"""),

# ── EXERCICE 3 ──────────────────────────────────────────────
md("""---
### 🟡 Exercice 3 · Boucles Beobank

**Contexte :** Vous avez une liste des codes statut de 10 contrats extraits de `CTR.csv`.

```python
codes = ["1", "1", "3", "4", "1", "6", "2", "4", "1", "5"]
soldes = [12500.0, 3200.0, 890.0, 0.0, 45000.0, 0.0, 7800.0, 0.0, 22000.0, 150.0]
```

**À faire avec une boucle `for` :**
1. Compter le nombre de contrats par catégorie (Actif / Inactif)
2. Calculer la somme des soldes des contrats actifs seulement
3. Trouver le solde maximum parmi les actifs
4. Afficher un résumé (nb actifs, nb inactifs, solde total actifs, solde max)"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────

codes  = ["1", "1", "3", "4", "1", "6", "2", "4", "1", "5"]
soldes = [12500.0, 3200.0, 890.0, 0.0, 45000.0, 0.0, 7800.0, 0.0, 22000.0, 150.0]

nb_actifs   = 0
nb_inactifs = 0
somme_actifs = 0.0
max_actif    = 0.0

for i in range(len(codes)):
    code  = codes[i]
    solde = soldes[i]
    # votre code ici...

print(f"Actifs    : {nb_actifs}")
print(f"Inactifs  : {nb_inactifs}")
print(f"Somme actifs : {somme_actifs:,.2f} EUR")
print(f"Max actifs   : {max_actif:,.2f} EUR")"""),

md("""**✅ Correction exercice 3 :**"""),

code("""# ✅ CORRECTION exercice 3 ──────────────────────────────────

codes  = ["1", "1", "3", "4", "1", "6", "2", "4", "1", "5"]
soldes = [12500.0, 3200.0, 890.0, 0.0, 45000.0, 0.0, 7800.0, 0.0, 22000.0, 150.0]

# Initialiser les accumulateurs AVANT la boucle
nb_actifs    = 0
nb_inactifs  = 0
somme_actifs = 0.0
max_actif    = 0.0

CODES_ACTIFS = ("1", "2", "3")    # tuple des codes considérés comme actifs

for i in range(len(codes)):       # i = 0, 1, 2, ..., 9
    code  = codes[i]              # accéder par index
    solde = soldes[i]

    if code in CODES_ACTIFS:      # si le contrat est actif
        nb_actifs    += 1
        somme_actifs += solde
        if solde > max_actif:     # mettre à jour le maximum
            max_actif = solde
    else:
        nb_inactifs += 1

# Affichage
total = nb_actifs + nb_inactifs
print(f"Total contrats   : {total}")
print(f"Actifs           : {nb_actifs} ({nb_actifs/total:.0%})")
print(f"Inactifs         : {nb_inactifs} ({nb_inactifs/total:.0%})")
print(f"Solde total actifs : {somme_actifs:,.2f} EUR")
print(f"Solde moyen actifs : {somme_actifs/nb_actifs if nb_actifs else 0:,.2f} EUR")
print(f"Solde max actifs   : {max_actif:,.2f} EUR")"""),

# ════════════════════════════════════════════════════════════════
# SECTION 5 · LISTES
# ════════════════════════════════════════════════════════════════
md("""---
# 5 · Listes — collections ordonnées

Une liste est une **séquence ordonnée** d'éléments. Elle peut contenir
des éléments de types différents. Elle est **modifiable**.

```python
ma_liste = [element1, element2, element3, ...]
```

## Opérations essentielles

| Opération | Syntaxe | Description |
|-----------|---------|-------------|
| Accès par index | `liste[0]`, `liste[-1]` | Premier / dernier |
| Tranche | `liste[1:4]`, `liste[:3]` | Sous-liste |
| Ajouter fin | `liste.append(val)` | Ajouter un élément |
| Insérer | `liste.insert(i, val)` | Insérer à la position i |
| Supprimer | `liste.remove(val)` | Supprimer la valeur |
| Trier | `liste.sort()` | Trier sur place |
| Longueur | `len(liste)` | Nombre d'éléments |
| Contient ? | `val in liste` | Test d'appartenance |
| Somme | `sum(liste)` | Somme des numériques |
| Min/Max | `min()`, `max()` | Extrêmes |"""),

code("""# ── Créer et accéder à une liste ─────────────────────────────
# Les listes s'écrivent entre crochets [ ]
# L'index commence à 0 (pas 1 !)

codes_statut = ["1", "2", "3", "4", "5", "6"]   # liste des codes ECV
devises      = ["EUR", "USD", "GBP", "CHF"]      # liste des devises

# Accès par index positif (de gauche à droite)
print("Codes statut :")
print(f"  Premier (index 0)  : {codes_statut[0]}")   # "1"
print(f"  Troisième (index 2): {codes_statut[2]}")   # "3"
print(f"  Dernier  (index -1): {codes_statut[-1]}")  # "6" (-1 = dernier)
print(f"  Avant-dernier (-2) : {codes_statut[-2]}")  # "5"
print()

# Tranche (slicing) : [debut:fin] — fin EXCLUE
print("Tranches :")
print(f"  [:3]   (3 premiers) : {codes_statut[:3]}")    # "1","2","3"
print(f"  [3:]   (à partir de 3) : {codes_statut[3:]}") # "4","5","6"
print(f"  [1:4]  (index 1 à 3) : {codes_statut[1:4]}")  # "2","3","4"
print(f"  [::2]  (un sur deux) : {codes_statut[::2]}")  # "1","3","5"
print(f"  [::-1] (inversé)     : {codes_statut[::-1]}") # "6","5","4","3","2","1"
print()

# Longueur
print(f"Nb codes : {len(codes_statut)}")
print(f"Nb devises : {len(devises)}")"""),

code("""# ── Modifier une liste ──────────────────────────────────────
langues_beobank = ["FR", "NL"]    # langues principales de Beobank

# append() : ajouter un élément à la FIN de la liste
langues_beobank.append("DE")      # ajouter l'allemand
print(f"Après append('DE')  : {langues_beobank}")   # ['FR', 'NL', 'DE']

# insert(index, valeur) : insérer à une position précise
langues_beobank.insert(1, "EN")   # insérer 'EN' à la position 1
print(f"Après insert(1,'EN'): {langues_beobank}")   # ['FR', 'EN', 'NL', 'DE']

# remove(valeur) : supprimer la première occurrence de cette valeur
langues_beobank.remove("EN")
print(f"Après remove('EN')  : {langues_beobank}")   # ['FR', 'NL', 'DE']

# pop() : supprimer et retourner le dernier élément (ou celui à l'index donné)
dernier = langues_beobank.pop()
print(f"pop() a retiré : {dernier}, liste : {langues_beobank}")  # 'DE', ['FR','NL']

# Modifier un élément par index
langues_beobank[0] = "Français"   # remplacer 'FR' par 'Français'
print(f"Après modification : {langues_beobank}")

# Trier
soldes_bruts = [15234.87, 3200.0, 890.0, 45000.0, 7800.0]
soldes_tries = sorted(soldes_bruts)           # sorted() retourne une NOUVELLE liste
soldes_bruts.sort(reverse=True)              # sort() modifie la liste originale
print(f"Trié asc  : {soldes_tries}")
print(f"Trié desc : {soldes_bruts}")"""),

code("""# ── List comprehension : créer une liste en une ligne ─────────
# Syntaxe : [expression for variable in iterable if condition]
# C'est comme un SELECT ... FROM ... WHERE en SQL, mais pour créer des listes

codes   = ["1", "2", "3", "4", "5", "6"]
soldes2 = [12500.0, 3200.0, 890.0, 0.0, 45000.0, 150.0]

# Exemple 1 : filtrer les codes actifs (1, 2, 3)
# Version longue :
actifs_long = []
for c in codes:
    if c in ("1","2","3"):
        actifs_long.append(c)

# Version list comprehension :
actifs_court = [c for c in codes if c in ("1","2","3")]

print(f"Codes actifs (long)  : {actifs_long}")
print(f"Codes actifs (court) : {actifs_court}")
print()

# Exemple 2 : transformer chaque solde (convertir EUR en centimes)
centimes = [int(s * 100) for s in soldes2]    # multiplier chaque élément par 100
print(f"Soldes en centimes : {centimes}")
print()

# Exemple 3 : liste de tuples (ref, solde formaté)
refs     = ["CTR-001", "CTR-002", "CTR-003", "CTR-004", "CTR-005", "CTR-006"]
resumes  = [(r, f"{s:,.2f} EUR") for r, s in zip(refs, soldes2)]
print("Résumés :")
for ref, montant in resumes:
    print(f"  {ref} : {montant}")"""),

# ── EXERCICE 4 ──────────────────────────────────────────────
md("""---
### 🟡 Exercice 4 · Listes et list comprehension

**Données :**
```python
soldes = [12500.0, 0.0, 3200.0, 0.0, 890.0, 45000.0, 150.0, 7800.0, 0.0, 22000.0]
refs   = ["CTR-001","CTR-002","CTR-003","CTR-004","CTR-005",
          "CTR-006","CTR-007","CTR-008","CTR-009","CTR-010"]
```

**À faire avec des list comprehensions :**
1. `soldes_positifs` : liste des soldes strictement > 0
2. `refs_zero` : liste des refs dont le solde est 0
3. `soldes_keur` : liste des soldes convertis en milliers d'EUR (arrondi à 1 décimale)
4. Calculer la somme et la moyenne des `soldes_positifs`
5. Afficher les résultats"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────

soldes = [12500.0, 0.0, 3200.0, 0.0, 890.0, 45000.0, 150.0, 7800.0, 0.0, 22000.0]
refs   = ["CTR-001","CTR-002","CTR-003","CTR-004","CTR-005",
          "CTR-006","CTR-007","CTR-008","CTR-009","CTR-010"]

# 1. List comprehension : soldes > 0
soldes_positifs = [...]

# 2. List comprehension : refs avec solde == 0
refs_zero = [...]

# 3. List comprehension : soldes en kEUR (round(..., 1))
soldes_keur = [...]

# 4. Statistiques
somme_pos  = sum(soldes_positifs)
moyenne_pos = ...

print(f"Soldes positifs : {soldes_positifs}")
print(f"Refs à 0        : {refs_zero}")
print(f"En kEUR         : {soldes_keur}")
print(f"Somme positifs  : {somme_pos:,.2f} EUR")
print(f"Moyenne positifs: {moyenne_pos:,.2f} EUR")"""),

md("""**✅ Correction exercice 4 :**"""),

code("""# ✅ CORRECTION exercice 4 ──────────────────────────────────

soldes = [12500.0, 0.0, 3200.0, 0.0, 890.0, 45000.0, 150.0, 7800.0, 0.0, 22000.0]
refs   = ["CTR-001","CTR-002","CTR-003","CTR-004","CTR-005",
          "CTR-006","CTR-007","CTR-008","CTR-009","CTR-010"]

# 1. Soldes strictement positifs
# [expression for var in liste if condition]
soldes_positifs = [s for s in soldes if s > 0]

# 2. Refs avec solde = 0
# zip() couple chaque ref avec son solde correspondant
refs_zero = [r for r, s in zip(refs, soldes) if s == 0]

# 3. Soldes en kEUR (diviser par 1000, arrondir à 1 décimale)
soldes_keur = [round(s / 1000, 1) for s in soldes]

# 4. Statistiques sur les soldes positifs
nb_pos      = len(soldes_positifs)
somme_pos   = sum(soldes_positifs)
moyenne_pos = somme_pos / nb_pos if nb_pos > 0 else 0.0

# Affichage
print(f"Soldes positifs ({nb_pos})   : {soldes_positifs}")
print(f"Refs à zéro ({len(refs_zero)}) : {refs_zero}")
print(f"En kEUR            : {soldes_keur}")
print()
print(f"Somme positifs   : {somme_pos:>12,.2f} EUR")
print(f"Moyenne positifs : {moyenne_pos:>12,.2f} EUR")
print(f"Max positif      : {max(soldes_positifs):>12,.2f} EUR")
print(f"Min positif      : {min(soldes_positifs):>12,.2f} EUR")"""),

# ════════════════════════════════════════════════════════════════
# SECTION 6 · TUPLES
# ════════════════════════════════════════════════════════════════
md("""---
# 6 · Tuples — collections immutables

Un tuple est comme une liste, mais **on ne peut pas le modifier** après création.
On l'utilise pour des données qui ne doivent pas changer (codes valides, coordonnées...).

```python
mon_tuple = (valeur1, valeur2, valeur3)
```

**Différence clé avec les listes :**
- Liste `[...]` : modifiable → `.append()`, `.remove()` etc. fonctionnent
- Tuple `(...)` : immutable → aucune modification possible (c'est un garde-fou)"""),

code("""# ── Tuples Beobank ──────────────────────────────────────────
# Usage 1 : constantes métier (valeurs qui ne changent jamais)
CODES_ACTIFS    = ("1", "2", "3")       # codes ECV des contrats actifs — IMMUABLE
CODES_INACTIFS  = ("4", "5", "6")       # codes ECV inactifs
DEVISES_VALIDES = ("EUR", "USD", "GBP", "CHF")  # devises autorisées
LANGUES_BEOBANK = ("FR", "NL")          # langues officielles Beobank

# Usage 2 : coordonnées (paires de valeurs liées)
siege_beobank   = (50.8503, 4.3517)     # latitude, longitude du siège
mois_annee      = (11, 2026)            # mois novembre, année 2026

# Accès par index (comme une liste, l'index commence à 0)
print(f"Codes actifs   : {CODES_ACTIFS}")
print(f"Premier code   : {CODES_ACTIFS[0]}")
print(f"Latitude       : {siege_beobank[0]}")
print(f"Longitude      : {siege_beobank[1]}")

# Déballage (unpacking) : assigner chaque élément à une variable
lat, lon = siege_beobank      # déballage en 2 variables
mois, an = mois_annee

print(f"\nSiège : lat={lat}, lon={lon}")
print(f"Période : mois {mois} / {an}")

# Test d'appartenance : in fonctionne exactement comme pour les listes
cod_test = "3"
if cod_test in CODES_ACTIFS:
    print(f"\nCode {cod_test} est ACTIF")

# Tentative de modification : va lever une erreur (comportement voulu !)
try:
    CODES_ACTIFS[0] = "X"     # essayer de modifier
except TypeError as e:
    print(f"\nTuple immuable (normal) : {e}")"""),

code("""# ── Tuples comme valeurs de retour de fonctions ───────────────
# C'est l'usage le plus courant des tuples en Python

def analyser_contrat_complet(cod_ecv, solde, devise):
    '''
    Analyse un contrat et retourne 4 indicateurs.
    Retourne un tuple : (libellé, catégorie, segment, alerte).
    '''
    # Libellé
    mapping = {"1":"Ouvert","2":"En attente","3":"Suspendu",
               "4":"Cloturé","5":"En résiliation","6":"Résilié"}
    libelle = mapping.get(str(cod_ecv), "Inconnu")

    # Catégorie
    categorie = "Actif" if cod_ecv in ("1","2","3") else "Inactif"

    # Segment selon solde
    if solde is None:   segment = "Inconnu"
    elif solde < 1000:  segment = "Standard"
    elif solde < 10000: segment = "Confort"
    elif solde < 50000: segment = "Premium"
    else:               segment = "Private"

    # Alerte
    if cod_ecv in ("5","6"):  alerte = "CRITIQUE"
    elif cod_ecv == "3":      alerte = "ATTENTION"
    elif solde is not None and solde < 0: alerte = "SOLDE NÉGATIF"
    else:                     alerte = "OK"

    return libelle, categorie, segment, alerte   # retourner un tuple de 4 valeurs

# Appel et déballage du tuple en 4 variables
lib, cat, seg, ale = analyser_contrat_complet("3", 12500.0, "EUR")
print(f"Libellé   : {lib}")
print(f"Catégorie : {cat}")
print(f"Segment   : {seg}")
print(f"Alerte    : {ale}")
print()

# Tester plusieurs cas
for cod, sld in [("1", 75000), ("2", 5000), ("5", 100), ("4", 0), ("3", -50)]:
    l, c, s, a = analyser_contrat_complet(cod, sld, "EUR")
    print(f"Code {cod}  solde {sld:>7} → {l:<18} [{c}] {s:<10} {a}")"""),

# ── EXERCICE 5 ──────────────────────────────────────────────
md("""---
### 🟡 Exercice 5 · Tuples et déballage

**À faire :**
1. Créer un tuple `SEGMENTS_ORDRES` contenant les segments dans l'ordre croissant :
   `("Standard", "Confort", "Premium", "Private")`
2. Écrire une fonction `classifier_client(solde, cod_typ_tie)` qui retourne
   le tuple `(segment, type_client, est_eligible_premium)` où :
   - `segment` : selon les seuils de l'exercice 2
   - `type_client` : "PP" ou "PM"
   - `est_eligible_premium` : `True` si segment Premium ou Private ET cod_typ_tie == "1"
3. Tester avec 5 cas différents en déballant le tuple retourné"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────

SEGMENTS_ORDRES = (...)   # définir le tuple

def classifier_client(solde, cod_typ_tie):
    '''Retourne (segment, type_client, est_eligible_premium).'''
    # segment
    ...
    # type_client
    ...
    # est_eligible_premium
    ...
    return segment, type_client, est_eligible_premium

# Tests
cas = [(500, "1"), (5000, "1"), (25000, "1"), (80000, "2"), (15000, "1")]
for solde, typ in cas:
    seg, tc, elig = classifier_client(solde, typ)
    print(f"Solde {solde:>7,.0f} | {tc} → {seg:<10} | Éligible Premium : {elig}")"""),

md("""**✅ Correction exercice 5 :**"""),

code("""# ✅ CORRECTION exercice 5 ──────────────────────────────────

SEGMENTS_ORDRES = ("Standard", "Confort", "Premium", "Private")

def classifier_client(solde, cod_typ_tie):
    '''Retourne (segment, type_client, est_eligible_premium).'''
    # Segment selon le solde
    if solde is None:    segment = "Inconnu"
    elif solde < 1000:   segment = "Standard"
    elif solde < 10000:  segment = "Confort"
    elif solde < 50000:  segment = "Premium"
    else:                segment = "Private"

    # Type client
    type_client = "PP" if cod_typ_tie == "1" else "PM"

    # Éligibilité Premium : segment >= Premium ET personne physique
    est_premium_plus = segment in ("Premium", "Private")
    est_eligible_premium = est_premium_plus and cod_typ_tie == "1"

    return segment, type_client, est_eligible_premium   # tuple de 3 valeurs

# Tests
cas = [(500, "1"), (5000, "1"), (25000, "1"), (80000, "2"), (15000, "1")]
print(f"{'Solde':>10}  {'Type':>4}  {'Segment':<10}  {'Éligible Premium'}")
print("-" * 50)
for solde, typ in cas:
    seg, tc, elig = classifier_client(solde, typ)   # déballage du tuple
    elig_str = "✓ OUI" if elig else "✗ NON"
    print(f"{solde:>10,.0f}  {tc:>4}  {seg:<10}  {elig_str}")"""),

# ════════════════════════════════════════════════════════════════
# SECTION 7 · DICTIONNAIRES
# ════════════════════════════════════════════════════════════════
md("""---
# 7 · Dictionnaires — clé : valeur

Un dictionnaire associe des **clés** à des **valeurs**.
Structure idéale pour les mappings (codes → libellés) et les enregistrements (une ligne de table).

```python
mon_dict = {"cle1": valeur1, "cle2": valeur2, ...}
```

## Opérations essentielles

| Opération | Syntaxe | Description |
|-----------|---------|-------------|
| Créer | `d = {"k": v}` | Créer un dictionnaire |
| Lire | `d["k"]` | Lire la valeur (erreur si absent) |
| Lire sécurisé | `d.get("k", defaut)` | Lire sans erreur |
| Modifier | `d["k"] = v` | Modifier ou ajouter |
| Supprimer | `del d["k"]` | Supprimer une clé |
| Clés | `d.keys()` | Liste des clés |
| Valeurs | `d.values()` | Liste des valeurs |
| Paires | `d.items()` | Paires (clé, valeur) |
| Contient ? | `"k" in d` | Test de présence d'une clé |"""),

code("""# ── Dictionnaire de mapping (équivalent FORMAT SAS) ──────────
# Usage le plus courant en analyse Beobank : convertir des codes en libellés

# Mapping COD_ECV_CTR → libellé (FORMAT SAS équivalent)
MAPPING_ECV = {
    "1": "Ouvert",
    "2": "En attente",
    "3": "Suspendu",
    "4": "Cloturé",
    "5": "En résiliation",
    "6": "Résilié",
}

# Accès direct : dict["clé"]
print("Accès direct :")
print(f"  Code 1 : {MAPPING_ECV['1']}")
print(f"  Code 4 : {MAPPING_ECV['4']}")

# Accès sécurisé : dict.get("clé", valeur_par_défaut)
# NE lève pas d'erreur si la clé est absente
print("\nAccès sécurisé avec .get() :")
print(f"  Code '3' : {MAPPING_ECV.get('3', 'Inconnu')}")    # clé présente
print(f"  Code 'X' : {MAPPING_ECV.get('X', 'Inconnu')}")    # clé absente → défaut

# Parcourir toutes les paires
print("\nTous les statuts :")
for code, libelle in MAPPING_ECV.items():   # .items() donne les paires (clé, valeur)
    print(f"  {code} → {libelle}")"""),

code("""# ── Dictionnaire comme enregistrement (une ligne de table) ───
# Simuler une ligne de la table CTR.csv

contrat = {
    "IDT_AC"      : "AC00001",        # identifiant du compte
    "REF_CTR_INN" : "CTR-2024-00137", # référence interne
    "DAT_OUV_CTR" : "2024-05-29",     # date d'ouverture
    "COD_ECV_CTR" : "1",              # code statut
    "COD_DEV"     : "EUR",            # devise
    "SLD_CTR"     : 15234.87,         # solde
    "MNT_INI"     : 10000.0,          # montant initial
}

# Lire les champs
print(f"Contrat : {contrat['REF_CTR_INN']}")
print(f"Statut  : {contrat['COD_ECV_CTR']} → {MAPPING_ECV.get(contrat['COD_ECV_CTR'], '?')}")
print(f"Solde   : {contrat['SLD_CTR']:,.2f} {contrat['COD_DEV']}")

# Ajouter des champs calculés
contrat["LIB_ECV"]  = MAPPING_ECV.get(contrat["COD_ECV_CTR"], "Inconnu")
contrat["PLUS_VALUE"] = contrat["SLD_CTR"] - contrat["MNT_INI"]

print(f"\nLibellé    : {contrat['LIB_ECV']}")
print(f"Plus-value : {contrat['PLUS_VALUE']:+,.2f} EUR")

# Tester la présence d'une clé
if "DAT_CLO_CTR" not in contrat:     # la clé n'existe pas
    print("\nDate de clôture : non renseignée")"""),

code("""# ── Liste de dictionnaires : simuler une table complète ───────
# Structure de données fondamentale avant d'utiliser Pandas

# 5 lignes de la table CTR (données fictives mais réalistes)
table_ctr = [
    {"IDT_AC": "AC001", "COD_ECV_CTR": "1", "SLD_CTR": 12500.0, "COD_DEV": "EUR"},
    {"IDT_AC": "AC002", "COD_ECV_CTR": "4", "SLD_CTR": 0.0,     "COD_DEV": "EUR"},
    {"IDT_AC": "AC003", "COD_ECV_CTR": "1", "SLD_CTR": 45000.0, "COD_DEV": "EUR"},
    {"IDT_AC": "AC004", "COD_ECV_CTR": "6", "SLD_CTR": 0.0,     "COD_DEV": "USD"},
    {"IDT_AC": "AC005", "COD_ECV_CTR": "3", "SLD_CTR": 890.0,   "COD_DEV": "EUR"},
]

MAPPING_ECV = {"1":"Ouvert","2":"En attente","3":"Suspendu",
               "4":"Cloturé","5":"En résiliation","6":"Résilié"}

print(f"{'IDT_AC':<8}  {'Statut':>6}  {'Libellé':<20}  {'Solde':>12}  {'Devise'}")
print("-" * 58)
for ligne in table_ctr:               # parcourir chaque "ligne" (dictionnaire)
    idt  = ligne["IDT_AC"]            # extraire chaque champ
    cod  = ligne["COD_ECV_CTR"]
    sld  = ligne["SLD_CTR"]
    dev  = ligne["COD_DEV"]
    lib  = MAPPING_ECV.get(cod, "Inconnu")
    print(f"{idt:<8}  {cod:>6}  {lib:<20}  {sld:>12,.2f}  {dev}")

# Comptage groupé avec un dictionnaire
comptage = {}                         # dictionnaire vide pour compter
for ligne in table_ctr:
    cod = ligne["COD_ECV_CTR"]
    # dict.get(clé, défaut) + 1 : compter sans initialiser
    comptage[cod] = comptage.get(cod, 0) + 1

print("\nRépartition :")
for cod, nb in sorted(comptage.items()):
    print(f"  Code {cod} ({MAPPING_ECV.get(cod,'?')}) : {nb}")"""),

# ── EXERCICE 6 ──────────────────────────────────────────────
md("""---
### 🟡 Exercice 6 · Dictionnaires et mappings Beobank

**Contexte :** La table `TIE.csv` contient `COD_TYP_TIE` (1=PP, 2=PM),
`COD_SEX` (M/F), `COD_LNG_CTR` (FR/NL), `COD_STA_FED` (état civil).

**À faire :**
1. Créer les 4 dictionnaires de mapping
2. Créer une liste de 5 clients (dictionnaires) avec ces codes
3. Boucle sur les clients : afficher un tableau avec les libellés
4. Compter les clients par langue et afficher la répartition"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────

# 1. Mappings
MAPPING_TYP = {"1": "Personne physique", "2": "Personne morale"}
MAPPING_SEX = {"M": "Masculin", "F": "Féminin"}
MAPPING_LNG = {"FR": "Français", "NL": "Néerlandais"}
MAPPING_STA = {"C": "Célibataire", "M": "Marié(e)", "D": "Divorcé(e)", "V": "Veuf/ve"}

# 2. Liste de clients
clients = [
    {"IDT_PI": "PI001", "COD_TYP_TIE": "1", "COD_SEX": "F", "COD_LNG_CTR": "FR", "COD_STA_FED": "M"},
    {"IDT_PI": "PI002", "COD_TYP_TIE": "1", "COD_SEX": "M", "COD_LNG_CTR": "NL", "COD_STA_FED": "C"},
    {"IDT_PI": "PI003", "COD_TYP_TIE": "2", "COD_SEX": None,"COD_LNG_CTR": "FR", "COD_STA_FED": None},
    {"IDT_PI": "PI004", "COD_TYP_TIE": "1", "COD_SEX": "M", "COD_LNG_CTR": "NL", "COD_STA_FED": "D"},
    {"IDT_PI": "PI005", "COD_TYP_TIE": "1", "COD_SEX": "F", "COD_LNG_CTR": "FR", "COD_STA_FED": "V"},
]

# 3. Tableau avec libellés
print(f"{'IDT_PI':<8}  {'Type':<20}  {'Sexe':<12}  {'Langue':<14}  {'État civil'}")
print("-" * 72)
for client in clients:
    typ = MAPPING_TYP.get(client["COD_TYP_TIE"], "Inconnu")
    sex = MAPPING_SEX.get(client.get("COD_SEX"), "N/A") if client["COD_SEX"] else "N/A"
    lng = MAPPING_LNG.get(client["COD_LNG_CTR"], "Inconnu")
    sta = MAPPING_STA.get(client.get("COD_STA_FED"), "N/A") if client["COD_STA_FED"] else "N/A"
    print(f"{client['IDT_PI']:<8}  {typ:<20}  {sex:<12}  {lng:<14}  {sta}")

# 4. Comptage par langue
print()
comptage_lng = {}
for client in clients:
    lng = client["COD_LNG_CTR"]
    comptage_lng[lng] = comptage_lng.get(lng, 0) + 1

print("Répartition par langue :")
for cod, nb in comptage_lng.items():
    print(f"  {MAPPING_LNG.get(cod, cod)} : {nb} client(s)")"""),

md("""**✅ Correction exercice 6 :**"""),

code("""# ✅ CORRECTION exercice 6 (même code que l'exercice — déjà complet ci-dessus)
print("Voir le code de l'exercice ci-dessus — la correction est intégrée.")
print("Points importants à noter :")
print("  1. dict.get(clé, défaut) évite une KeyError si la clé manque")
print("  2. client.get('COD_SEX') retourne None si la clé est absente")
print("  3. client['COD_SEX'] if client['COD_SEX'] else 'N/A' gère les None")
print("  4. comptage.get(lng, 0) + 1 initialise à 0 si lng n'est pas encore dans le dict")"""),

# ════════════════════════════════════════════════════════════════
# SECTION 8 · FONCTIONS
# ════════════════════════════════════════════════════════════════
md("""---
# 8 · Fonctions — structurer et réutiliser le code

## 8.1 Définir une fonction

```python
def nom_fonction(parametre1, parametre2, parametre3="defaut"):
    '''Docstring : description de la fonction.'''
    # corps de la fonction
    resultat = ...
    return resultat
```

## 8.2 Règles clés

- `def` : mot-clé pour définir une fonction
- Le corps est **indenté** (4 espaces)
- `return` : retourner une valeur (sans `return` → retourne `None`)
- Les paramètres peuvent avoir des **valeurs par défaut**
- On peut retourner **plusieurs valeurs** (tuple)
- La **docstring** `'''...'''` documente la fonction

## 8.3 Fonctions lambda

```python
double = lambda x: x * 2      # équivalent de def double(x): return x * 2
```"""),

code("""# ── Fonction simple avec docstring ───────────────────────────

def libelle_statut(cod_ecv):
    '''
    Retourne le libellé d'un code statut ECV.

    Paramètre:
        cod_ecv (str) : code statut CTR (1 à 6)
    Retourne:
        str : libellé du statut ou "Inconnu"
    '''
    # Dictionnaire local à la fonction
    mapping = {
        "1": "Ouvert",       "2": "En attente",
        "3": "Suspendu",     "4": "Cloturé",
        "5": "En résiliation", "6": "Résilié",
    }
    # .get() avec valeur par défaut "Inconnu"
    return mapping.get(str(cod_ecv), "Inconnu")


# Appeler la fonction
print(libelle_statut("1"))    # "Ouvert"
print(libelle_statut("5"))    # "En résiliation"
print(libelle_statut("X"))    # "Inconnu"
print(libelle_statut(4))      # "Cloturé" (str() gère le cas int)

# Appeler dans une liste comprehension
codes = ["1", "2", "3", "4", "5", "6", "X"]
libelles = [libelle_statut(c) for c in codes]
print(libelles)"""),

code("""# ── Fonction avec paramètres par défaut ──────────────────────

def calculer_interets(capital, taux_annuel, nb_mois=12, capitalisation=True):
    '''
    Calcule les intérêts sur un capital.

    capital        : float — capital de départ
    taux_annuel    : float — taux annuel (ex: 0.015 = 1.5 %)
    nb_mois        : int   — durée en mois (défaut = 12)
    capitalisation : bool  — True = intérêts composés, False = simples
    Retourne : float — montant des intérêts
    '''
    taux_mensuel = taux_annuel / 12   # convertir le taux annuel en mensuel

    if capitalisation:
        # Intérêts composés : le capital grossit chaque mois
        capital_final  = capital * (1 + taux_mensuel) ** nb_mois
        interets       = capital_final - capital
    else:
        # Intérêts simples : calculés uniquement sur le capital initial
        interets = capital * taux_annuel * (nb_mois / 12)

    return round(interets, 2)   # arrondir à 2 décimales

# Appels avec paramètres positionnels (dans l'ordre)
i1 = calculer_interets(10000, 0.015)             # 12 mois, composés (défauts)
i2 = calculer_interets(10000, 0.015, 24)         # 24 mois, composés
i3 = calculer_interets(10000, 0.015, 12, False)  # 12 mois, simples

print(f"10 000 EUR / 1.5% an / 12 mois composés  : {i1:>10,.2f} EUR")
print(f"10 000 EUR / 1.5% an / 24 mois composés  : {i2:>10,.2f} EUR")
print(f"10 000 EUR / 1.5% an / 12 mois simples   : {i3:>10,.2f} EUR")

# Appels avec paramètres nommés (dans n'importe quel ordre)
i4 = calculer_interets(capital=25000, taux_annuel=0.02, nb_mois=6)
print(f"25 000 EUR / 2.0% an /  6 mois composés  : {i4:>10,.2f} EUR")"""),

code("""# ── Fonctions retournant plusieurs valeurs ────────────────────

def enrichir_contrat(cod_ecv, solde, devise="EUR"):
    '''
    Enrichit un contrat avec des colonnes calculées.
    Retourne un tuple : (libellé, catégorie, segment, alerte).
    '''
    MAPPING = {"1":"Ouvert","2":"En attente","3":"Suspendu",
               "4":"Cloturé","5":"En résiliation","6":"Résilié"}

    libelle   = MAPPING.get(str(cod_ecv), "Inconnu")
    categorie = "Actif" if cod_ecv in ("1","2","3") else "Inactif"

    if solde is None:       segment = "Inconnu"
    elif solde < 1000:      segment = "Standard"
    elif solde < 10000:     segment = "Confort"
    elif solde < 50000:     segment = "Premium"
    else:                   segment = "Private"

    if cod_ecv in ("5","6"):               alerte = "CRITIQUE"
    elif cod_ecv == "3":                   alerte = "ATTENTION"
    elif solde is not None and solde < 0:  alerte = "SOLDE NÉGATIF"
    else:                                  alerte = "OK"

    return libelle, categorie, segment, alerte

# Test sur une liste de contrats
contrats = [
    {"ref": "CTR-001", "ecv": "1", "sld": 25000.0},
    {"ref": "CTR-002", "ecv": "5", "sld": 150.0},
    {"ref": "CTR-003", "ecv": "3", "sld": 890.0},
    {"ref": "CTR-004", "ecv": "4", "sld": 0.0},
    {"ref": "CTR-005", "ecv": "1", "sld": 65000.0},
]

print(f"{'Réf':<10}  {'Libellé':<20}  {'Catégorie':<10}  {'Segment':<10}  {'Alerte'}")
print("-" * 68)
for ctr in contrats:
    lib, cat, seg, ale = enrichir_contrat(ctr["ecv"], ctr["sld"])
    print(f"{ctr['ref']:<10}  {lib:<20}  {cat:<10}  {seg:<10}  {ale}")"""),

code("""# ── Fonctions lambda ────────────────────────────────────────
# lambda parametre: expression
# Utile pour des transformations simples (souvent passées à sorted() ou map())

# Equivalent en def
def doubler(x):
    return x * 2

# Même chose en lambda
doubler_lambda = lambda x: x * 2
print(f"def     : {doubler(7)}")
print(f"lambda  : {doubler_lambda(7)}")

# Lambda avec sorted() : trier par un critère personnalisé
contrats = [
    {"ref": "CTR-B", "solde": 3000},
    {"ref": "CTR-A", "solde": 1000},
    {"ref": "CTR-D", "solde": 8000},
    {"ref": "CTR-C", "solde": 500},
]

# Trier par solde décroissant
par_solde = sorted(contrats, key=lambda c: c["solde"], reverse=True)
print("\nTrié par solde décroissant :")
for c in par_solde:
    print(f"  {c['ref']} : {c['solde']:,} EUR")

# Trier par référence alphabétique
par_ref = sorted(contrats, key=lambda c: c["ref"])
print("\nTrié par référence :")
for c in par_ref:
    print(f"  {c['ref']} : {c['solde']:,} EUR")"""),

# ── EXERCICE 7 ──────────────────────────────────────────────
md("""---
### 🟡 Exercice 7 · Fonctions d'analyse Beobank

**À faire :**
1. Écrire `classer_age(date_naissance)` :
   - Paramètre : chaîne `"YYYY-MM-DD"`
   - Retourne : tuple `(age_en_ans, tranche)` où tranche ∈
     `"<25"`, `"25-34"`, `"35-49"`, `"50-64"`, `"65+"`
   - Indice : `from datetime import date` puis `date.today().year - int(annee)`

2. Écrire `evaluer_risque(cod_ecv, solde, jours_depuis_ouverture)` :
   - Retourne : `"Faible"`, `"Moyen"` ou `"Élevé"` selon :
     - Élevé si cod_ecv in (5,6) ou solde < 0
     - Moyen si cod_ecv == 3 ou (solde < 500 et jours_depuis_ouverture > 180)
     - Faible sinon

3. Tester les deux fonctions"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────
from datetime import date

def classer_age(date_naissance):
    '''Retourne (age_en_ans, tranche_age).'''
    annee = int(date_naissance[:4])      # extraire les 4 premiers caractères
    age   = date.today().year - annee    # âge approximatif
    # tranches
    if age < 25:     tranche = "<25"
    elif age < 35:   tranche = "25-34"
    elif age < 50:   tranche = "35-49"
    elif age < 65:   tranche = "50-64"
    else:            tranche = "65+"
    return age, tranche

def evaluer_risque(cod_ecv, solde, jours_depuis_ouverture):
    '''Retourne "Faible", "Moyen" ou "Élevé".'''
    # votre code ici
    ...

# Tests
nais_test = ["1958-03-15", "1990-07-22", "1978-11-05", "2002-01-30", "1945-06-01"]
for nais in nais_test:
    age, tranche = classer_age(nais)
    print(f"  {nais} → {age} ans  ({tranche})")"""),

md("""**✅ Correction exercice 7 :**"""),

code("""# ✅ CORRECTION exercice 7 ──────────────────────────────────
from datetime import date

def classer_age(date_naissance):
    '''Retourne (age_en_ans, tranche_age) depuis une date "YYYY-MM-DD".'''
    annee = int(date_naissance[:4])        # [:4] = 4 premiers caractères = année
    mois  = int(date_naissance[5:7])       # [5:7] = mois
    jour  = int(date_naissance[8:10])      # [8:10] = jour

    auj   = date.today()
    # Âge précis : soustraction de date
    age   = auj.year - annee - ((auj.month, auj.day) < (mois, jour))

    if age < 25:     tranche = "<25"
    elif age < 35:   tranche = "25-34"
    elif age < 50:   tranche = "35-49"
    elif age < 65:   tranche = "50-64"
    else:            tranche = "65+"

    return age, tranche

def evaluer_risque(cod_ecv, solde, jours_depuis_ouverture):
    '''Évalue le risque d'un contrat. Retourne "Faible", "Moyen" ou "Élevé".'''
    # Risque élevé : résiliation ou solde négatif
    if cod_ecv in ("5", "6") or (solde is not None and solde < 0):
        return "Élevé"

    # Risque moyen : suspendu ou petit solde sur vieux compte
    elif cod_ecv == "3" or (solde is not None and solde < 500 and jours_depuis_ouverture > 180):
        return "Moyen"

    # Sinon faible
    return "Faible"

# Tests classer_age
print("=== Test classer_age ===")
nais_test = ["1958-03-15", "1990-07-22", "1978-11-05", "2002-01-30", "1945-06-01"]
for nais in nais_test:
    age, tranche = classer_age(nais)
    print(f"  {nais} → {age} ans  tranche : {tranche}")

print()
print("=== Test evaluer_risque ===")
risque_test = [
    ("1", 15000.0, 400),    # actif, bon solde, récent
    ("3", 200.0,  300),     # suspendu
    ("5", 100.0,  700),     # en résiliation
    ("1", 200.0,  250),     # petit solde mais récent
    ("1", 200.0,  200),     # petit solde sur vieux compte
]
for cod, sld, jours in risque_test:
    risque = evaluer_risque(cod, sld, jours)
    print(f"  Statut {cod} | Solde {sld:>8,.0f} | {jours:>3}j → Risque : {risque}")"""),

# ════════════════════════════════════════════════════════════════
# SECTION 9 · TRY / EXCEPT
# ════════════════════════════════════════════════════════════════
md("""---
# 9 · Gestion des erreurs — try / except

Les données réelles contiennent toujours des surprises.
`try/except` permet de gérer les erreurs sans faire planter le programme.

```python
try:
    # code qui peut lever une erreur
    resultat = float("abc")   # ValueError !
except ValueError:
    # code exécuté si ValueError est levée
    resultat = None
except (TypeError, KeyError) as e:
    # gérer plusieurs types d'erreur
    print(f"Erreur : {e}")
finally:
    # toujours exécuté (optionnel)
    ...
```

## Erreurs courantes en analyse de données

| Erreur | Cause | Solution |
|--------|-------|----------|
| `ValueError` | Conversion impossible (`float("abc")`) | `try/except ValueError` |
| `KeyError` | Clé absente dans un dict | `.get(cle, defaut)` |
| `IndexError` | Index hors limites de liste | Vérifier `len()` |
| `ZeroDivisionError` | Division par zéro | Vérifier diviseur != 0 |
| `TypeError` | Opération sur mauvais type | Convertir avec `str()`, `int()`, `float()` |"""),

code("""# ── try/except avec les données Beobank ──────────────────────
# Les fichiers CSV contiennent souvent des valeurs inattendues

valeurs_brutes = ["15234.87", ".", "N/A", "", "8900", "abc", "0", "-500"]

print(f"{'Valeur brute':<15}  {'Résultat':<15}  {'Statut'}")
print("-" * 48)

for val in valeurs_brutes:
    # Essayer la conversion
    if val in (".", "", None):          # valeur manquante SAS ou vide
        resultat = None
        statut   = "MANQUANT"
    else:
        try:
            resultat = float(val)       # tenter la conversion en nombre
            statut   = "OK"
        except ValueError:              # si la conversion échoue
            resultat = None
            statut   = "FORMAT INVALIDE"

    # Afficher le résultat
    res_str = f"{resultat:,.2f}" if resultat is not None else "None"
    print(f"  {repr(val):<13}  {res_str:<15}  {statut}")"""),

code("""# ── Fonction robuste de conversion ──────────────────────────

def convertir_solde(valeur_brute):
    '''
    Convertit une valeur brute en float.
    Retourne None si la valeur est manquante ou invalide.

    Valeurs reconnues comme manquantes : ".", "", "N/A", "NA", None
    '''
    # Étape 1 : vérifier si c'est une valeur manquante connue
    VALEURS_MANQUANTES = {".", "", "N/A", "NA", "NULL", "null"}
    if valeur_brute is None or str(valeur_brute).strip() in VALEURS_MANQUANTES:
        return None          # retourner None pour "valeur manquante"

    # Étape 2 : tenter la conversion
    try:
        return float(str(valeur_brute).strip().replace(",", "."))
    except (ValueError, TypeError):
        return None          # retourner None si la conversion échoue

def convertir_entier(valeur_brute, defaut=0):
    '''Convertit en entier, retourne defaut si impossible.'''
    resultat = convertir_solde(valeur_brute)
    if resultat is None:
        return defaut
    return int(resultat)

# Tests
cas_test = ["15234.87", ".", "", "N/A", "8 900", "abc", None, "0", " 3200 "]
print("Test convertir_solde :")
for cas in cas_test:
    res = convertir_solde(cas)
    print(f"  {repr(cas):>12} → {res}")"""),

# ── EXERCICE 8 ──────────────────────────────────────────────
md("""---
### 🟡 Exercice 8 · Nettoyage robuste avec try/except

**Contexte :** Vous recevez un extrait brut de `CTR.csv` avec des données sales.

```python
extrait = [
    {"ref": "CTR-001", "solde": "12500.50", "ecv": "1"},
    {"ref": "CTR-002", "solde": ".",         "ecv": "4"},
    {"ref": "CTR-003", "solde": "",          "ecv": "1"},
    {"ref": "CTR-004", "solde": "N/A",       "ecv": "X"},
    {"ref": "CTR-005", "solde": "45000",     "ecv": "1"},
    {"ref": "CTR-006", "solde": "abc",       "ecv": "3"},
    {"ref": "CTR-007", "solde": "-200.0",    "ecv": "5"},
]
```

**À faire :**
1. Pour chaque ligne : convertir `solde` avec votre fonction `convertir_solde()`
2. Classer le contrat : utiliser `libelle_statut()` et `enrichir_contrat()` définies plus haut
3. Compter les lignes valides / invalides
4. Afficher un tableau propre"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────

extrait = [
    {"ref": "CTR-001", "solde": "12500.50", "ecv": "1"},
    {"ref": "CTR-002", "solde": ".",         "ecv": "4"},
    {"ref": "CTR-003", "solde": "",          "ecv": "1"},
    {"ref": "CTR-004", "solde": "N/A",       "ecv": "X"},
    {"ref": "CTR-005", "solde": "45000",     "ecv": "1"},
    {"ref": "CTR-006", "solde": "abc",       "ecv": "3"},
    {"ref": "CTR-007", "solde": "-200.0",    "ecv": "5"},
]

nb_valides   = 0
nb_invalides = 0

print(f"{'Réf':<10}  {'Solde brut':<12}  {'Solde net':>12}  {'Statut':<20}  {'Alerte'}")
print("-" * 70)

for ligne in extrait:
    sld_net = convertir_solde(ligne["solde"])   # convertir le solde
    lib, cat, seg, ale = enrichir_contrat(ligne["ecv"], sld_net)
    sld_str = f"{sld_net:,.2f} EUR" if sld_net is not None else "MANQUANT"

    if sld_net is not None:
        nb_valides += 1
    else:
        nb_invalides += 1

    print(f"{ligne['ref']:<10}  {ligne['solde']:<12}  {sld_str:>12}  {lib:<20}  {ale}")

print("-" * 70)
print(f"Valides : {nb_valides} | Invalides : {nb_invalides}")"""),

md("""**✅ Correction exercice 8 :**"""),

code("""# ✅ CORRECTION exercice 8 (même code que ci-dessus — déjà complet)
print("L'exercice 8 est déjà auto-corrigé (convertir_solde et enrichir_contrat)")
print("sont définies dans les sections précédentes du notebook.")
print()
print("Points clés :")
print("  1. Toujours tester 'None' AVANT de faire des calculs sur la valeur")
print("  2. try/except permet de continuer même si une ligne est invalide")
print("  3. Compter séparément valides et invalides pour la qualité de données")"""),

# ════════════════════════════════════════════════════════════════
# SECTION 10 · LIRE UN FICHIER CSV
# ════════════════════════════════════════════════════════════════
md("""---
# 10 · Lire un fichier CSV Beobank avec Python pur

Avant d'utiliser Pandas (demain), il faut comprendre comment Python lit les fichiers.
Cela vous permet de comprendre ce que Pandas fait "en coulisses".

## Modules utilisés

- `pathlib.Path` : chemins de fichiers portables (Windows / Mac / Linux)
- `csv.DictReader` : lecture CSV ligne par ligne comme dictionnaires
- `open()` : ouvrir un fichier (avec `with` pour fermeture automatique)"""),

code("""# ── Lire CTR.csv ligne par ligne ─────────────────────────────
import csv                      # module standard Python pour les fichiers CSV
from pathlib import Path        # module pour les chemins portables

# Path() crée un objet "chemin" portable
# ".." remonte d'un niveau dans l'arborescence
# Path("..") / "Orsys" / "CTR.csv" = "../Orsys/CTR.csv"
dossier_data = Path("../Orsys")
chemin_ctr   = dossier_data / "CTR.csv"

print(f"Lecture de : {chemin_ctr}")
print()

# with open(...) as f : ouvre le fichier et le ferme automatiquement après le bloc
# "r" = read (lecture), encoding="utf-8" = encodage qui gère les accents
with open(chemin_ctr, "r", encoding="utf-8") as fichier:
    # csv.DictReader lit chaque ligne comme un dictionnaire
    # delimiter=";" = le séparateur dans nos fichiers Beobank
    lecteur = csv.DictReader(fichier, delimiter=";")

    # .fieldnames = liste des colonnes (lue depuis la 1ère ligne du CSV)
    print("Colonnes disponibles dans CTR.csv :")
    for col in lecteur.fieldnames:
        print(f"  • {col}")
    print(f"\nTotal colonnes : {len(lecteur.fieldnames)}")"""),

code("""# ── Lire et afficher les premières lignes ────────────────────
import csv
from pathlib import Path

DATA  = Path("../Orsys")
lignes_lues = []    # liste vide qui accumulera les lignes

with open(DATA / "CTR.csv", "r", encoding="utf-8") as f:
    lecteur = csv.DictReader(f, delimiter=";")
    for ligne in lecteur:          # pour chaque ligne du CSV
        lignes_lues.append(ligne)  # ajouter le dictionnaire à la liste

print(f"Lignes lues : {len(lignes_lues)}")
print()
print("Détail des 3 premières lignes :")
print("=" * 50)

for i, ligne in enumerate(lignes_lues[:3], start=1):   # les 3 premières seulement
    print(f"\n--- Ligne {i} ---")
    for col, val in ligne.items():            # parcourir les colonnes
        val_aff = val if val != "." else "None (manquant)"   # afficher les "." clairement
        print(f"  {col:<20}: {val_aff}")"""),

code("""# ── Analyser CTR.csv avec les outils du Jour 1 ────────────────
import csv
from pathlib import Path

DATA  = Path("../Orsys")

MAPPING_ECV = {"1":"Ouvert","2":"En attente","3":"Suspendu",
               "4":"Cloturé","5":"En résiliation","6":"Résilié"}
MAPPING_CAT = {"1":"Actif","2":"Actif","3":"Actif",
               "4":"Inactif","5":"Inactif","6":"Inactif"}

# Compteurs et accumulateurs
comptage_statut = {}   # {code: nb}
comptage_devise = {}   # {devise: nb}
soldes_valides  = []   # liste des soldes numériques
nb_manquants    = 0

with open(DATA / "CTR.csv", "r", encoding="utf-8") as f:
    for ligne in csv.DictReader(f, delimiter=";"):
        # ── Statut ───────────────────────────────────────────
        cod = ligne["COD_ECV_CTR"]
        comptage_statut[cod] = comptage_statut.get(cod, 0) + 1

        # ── Devise ───────────────────────────────────────────
        dev = ligne.get("COD_DEV", ".")
        if dev != "." and dev != "":
            comptage_devise[dev] = comptage_devise.get(dev, 0) + 1

        # ── Solde ────────────────────────────────────────────
        sld_brut = ligne.get("SLD_CTR", ".")
        sld = convertir_solde(sld_brut)   # fonction définie en section 9
        if sld is not None:
            soldes_valides.append(sld)
        else:
            nb_manquants += 1

total = sum(comptage_statut.values())

# ── Rapport ───────────────────────────────────────────────
print(f"{'='*52}")
print(f"  ANALYSE CTR.csv — {total} contrats")
print(f"{'='*52}")
print()
print(f"  RÉPARTITION PAR STATUT :")
for cod in sorted(comptage_statut):
    nb  = comptage_statut[cod]
    lib = MAPPING_ECV.get(cod, "Inconnu")
    cat = MAPPING_CAT.get(cod, "?")
    print(f"    {cod} {lib:<20} {nb:>4} ({nb/total:>5.1%}) [{cat}]")

print()
print(f"  RÉPARTITION PAR DEVISE :")
for dev in sorted(comptage_devise):
    nb = comptage_devise[dev]
    print(f"    {dev:<5} {nb:>4} ({nb/total:>5.1%})")

print()
print(f"  SOLDES :")
print(f"    Renseignés  : {len(soldes_valides):>4} ({len(soldes_valides)/total:.1%})")
print(f"    Manquants   : {nb_manquants:>4} ({nb_manquants/total:.1%})")
if soldes_valides:
    print(f"    Somme       : {sum(soldes_valides):>14,.2f} EUR")
    print(f"    Moyenne     : {sum(soldes_valides)/len(soldes_valides):>14,.2f} EUR")
    print(f"    Min         : {min(soldes_valides):>14,.2f} EUR")
    print(f"    Max         : {max(soldes_valides):>14,.2f} EUR")"""),

# ── EXERCICE 9 ──────────────────────────────────────────────
md("""---
### 🟡 Exercice 9 · Analyser TIE.csv

**À faire :**
1. Lire `TIE.csv` avec `csv.DictReader`
2. Compter les clients par `COD_TYP_TIE` (PP/PM)
3. Compter par `COD_LNG_CTR` (FR/NL)
4. Compter par `COD_SEX` (M/F/manquant)
5. Calculer l'âge moyen approximatif (année courante − année de `DAT_NAI`)
6. Afficher un rapport"""),

code("""# 🟡 Votre code ici ─────────────────────────────────────────
import csv
from pathlib import Path
from datetime import date

DATA = Path("../Orsys")

comptage_typ = {}
comptage_lng = {}
comptage_sex = {}
ages         = []

with open(DATA / "TIE.csv", "r", encoding="utf-8") as f:
    for ligne in csv.DictReader(f, delimiter=";"):
        # 1. Type
        typ = ligne.get("COD_TYP_TIE", "?")
        comptage_typ[typ] = comptage_typ.get(typ, 0) + 1
        # 2. Langue
        ...
        # 3. Sexe
        ...
        # 4. Âge (si DAT_NAI renseigné et != ".")
        dat_nai = ligne.get("DAT_NAI", ".")
        if dat_nai and dat_nai != ".":
            try:
                annee = int(dat_nai[:4])
                ages.append(date.today().year - annee)
            except:
                pass

# Afficher le rapport
total = sum(comptage_typ.values())
print(f"Clients analysés : {total}")
print(f"Type  : {comptage_typ}")
print(f"Langue: {comptage_lng}")
print(f"Sexe  : {comptage_sex}")
if ages:
    print(f"Âge moyen : {sum(ages)/len(ages):.1f} ans")"""),

md("""**✅ Correction exercice 9 :**"""),

code("""# ✅ CORRECTION exercice 9 ──────────────────────────────────
import csv
from pathlib import Path
from datetime import date

DATA = Path("../Orsys")

MAPPING_TYP = {"1":"Personne physique","2":"Personne morale"}
MAPPING_LNG = {"FR":"Français","NL":"Néerlandais"}

comptage_typ = {}
comptage_lng = {}
comptage_sex = {}
ages         = []

with open(DATA / "TIE.csv", "r", encoding="utf-8") as f:
    for ligne in csv.DictReader(f, delimiter=";"):
        # Type
        typ = ligne.get("COD_TYP_TIE", "?")
        comptage_typ[typ] = comptage_typ.get(typ, 0) + 1

        # Langue
        lng = ligne.get("COD_LNG_CTR", "?")
        lng_key = lng if lng and lng != "." else "N/A"
        comptage_lng[lng_key] = comptage_lng.get(lng_key, 0) + 1

        # Sexe
        sex = ligne.get("COD_SEX", ".")
        sex_key = sex if sex and sex != "." else "N/A"
        comptage_sex[sex_key] = comptage_sex.get(sex_key, 0) + 1

        # Âge approximatif
        dat_nai = ligne.get("DAT_NAI", ".")
        if dat_nai and dat_nai not in (".", ""):
            try:
                annee_nai = int(dat_nai[:4])
                age_approx = date.today().year - annee_nai
                if 0 < age_approx < 120:       # filtre anti-aberrant
                    ages.append(age_approx)
            except (ValueError, IndexError):
                pass

total = sum(comptage_typ.values())
print(f"{'='*48}")
print(f"  ANALYSE TIE.csv — {total} clients")
print(f"{'='*48}")
print()
print("  TYPE DE TIERS :")
for cod in sorted(comptage_typ):
    nb  = comptage_typ[cod]
    lib = MAPPING_TYP.get(cod, f"Code {cod}")
    print(f"    {lib:<22}: {nb:>4} ({nb/total:>5.1%})")

print()
print("  LANGUE DE COMMUNICATION :")
for cod in sorted(comptage_lng):
    nb  = comptage_lng[cod]
    lib = MAPPING_LNG.get(cod, cod)
    print(f"    {lib:<22}: {nb:>4} ({nb/total:>5.1%})")

print()
print("  GENRE :")
for cod in sorted(comptage_sex):
    nb  = comptage_sex[cod]
    lib = {"M":"Masculin","F":"Féminin","N/A":"Non renseigné"}.get(cod, cod)
    print(f"    {lib:<22}: {nb:>4} ({nb/total:>5.1%})")

if ages:
    print()
    print("  ÂGES :")
    print(f"    Âge moyen   : {sum(ages)/len(ages):.1f} ans")
    print(f"    Âge minimum : {min(ages)} ans")
    print(f"    Âge maximum : {max(ages)} ans")"""),

# ════════════════════════════════════════════════════════════════
# EXERCICE FINAL DU JOUR 1
# ════════════════════════════════════════════════════════════════
md("""---
# 🏁 Exercice final Jour 1 · Rapport d'inventaire complet

**Contexte :** Fin de journée. Votre manager veut un rapport synthétique
sur l'état du portefeuille Beobank.

**À faire — en utilisant TOUT ce que vous avez appris aujourd'hui :**
1. Lire `CTR.csv` ET `TIE.csv` avec `csv.DictReader`
2. Lire `TIE_X_CTR.csv` pour compter le nombre de contrats par client
3. Produire un rapport texte structuré avec :
   - Nombre de contrats par statut (tableau)
   - Nombre de clients PP/PM
   - Top 3 des clients avec le plus de contrats
   - Statistiques des soldes (somme, moyenne, min, max)

**Contraintes :** utiliser uniquement Python pur (pas de Pandas aujourd'hui)."""),

code("""# 🟡 Exercice final — votre code ────────────────────────────
import csv
from pathlib import Path

DATA = Path("../Orsys")

# Charger les 3 fichiers et produire le rapport
print("À compléter ...")"""),

md("""**✅ Correction exercice final :**"""),

code("""# ✅ CORRECTION exercice final ──────────────────────────────
import csv
from pathlib import Path

DATA = Path("../Orsys")

MAPPING_ECV = {"1":"Ouvert","2":"En attente","3":"Suspendu",
               "4":"Cloturé","5":"En résiliation","6":"Résilié"}
MAPPING_CAT = {"1":"Actif","2":"Actif","3":"Actif",
               "4":"Inactif","5":"Inactif","6":"Inactif"}
MAPPING_TYP = {"1":"PP","2":"PM"}

# ── 1. Lire CTR.csv ─────────────────────────────────────────
ctr_lignes = []
with open(DATA / "CTR.csv", "r", encoding="utf-8") as f:
    for ligne in csv.DictReader(f, delimiter=";"):
        ctr_lignes.append(ligne)

# ── 2. Lire TIE.csv ─────────────────────────────────────────
tie_lignes = []
with open(DATA / "TIE.csv", "r", encoding="utf-8") as f:
    for ligne in csv.DictReader(f, delimiter=";"):
        tie_lignes.append(ligne)

# ── 3. Lire TIE_X_CTR.csv : compter contrats par client ────
nb_ctr_par_client = {}   # {IDT_PI: nb_contrats}
with open(DATA / "TIE_X_CTR.csv", "r", encoding="utf-8") as f:
    for ligne in csv.DictReader(f, delimiter=";"):
        pi = ligne["IDT_PI"]
        nb_ctr_par_client[pi] = nb_ctr_par_client.get(pi, 0) + 1

# ── Analyser CTR ─────────────────────────────────────────────
comptage_ecv  = {}
soldes_valides = []
for l in ctr_lignes:
    cod = l["COD_ECV_CTR"]
    comptage_ecv[cod] = comptage_ecv.get(cod, 0) + 1
    sld = convertir_solde(l.get("SLD_CTR", "."))
    if sld is not None:
        soldes_valides.append(sld)

# ── Analyser TIE ─────────────────────────────────────────────
comptage_typ = {}
for l in tie_lignes:
    typ = l.get("COD_TYP_TIE", "?")
    comptage_typ[typ] = comptage_typ.get(typ, 0) + 1

# ── Top 3 clients ────────────────────────────────────────────
top3 = sorted(nb_ctr_par_client.items(), key=lambda x: x[1], reverse=True)[:3]

# ── RAPPORT ──────────────────────────────────────────────────
total_ctr = len(ctr_lignes)
total_cli = len(tie_lignes)

print("╔" + "═"*54 + "╗")
print("║        RAPPORT D'INVENTAIRE BEOBANK              ║")
print("╠" + "═"*54 + "╣")
print()
print(f"  PORTEFEUILLE : {total_ctr} CONTRATS")
print(f"  {'─'*48}")
print(f"  {'Code':<4}  {'Libellé':<22}  {'N':>5}  {'%':>6}  {'Catégorie'}")
print(f"  {'─'*48}")
for cod in sorted(comptage_ecv):
    nb  = comptage_ecv[cod]
    lib = MAPPING_ECV.get(cod, "Inconnu")
    cat = MAPPING_CAT.get(cod, "?")
    print(f"  {cod:<4}  {lib:<22}  {nb:>5}  {nb/total_ctr:>5.1%}  {cat}")

print()
print(f"  CLIENTS : {total_cli}")
print(f"  {'─'*48}")
for cod in sorted(comptage_typ):
    nb  = comptage_typ[cod]
    lib = {"1":"Personnes physiques","2":"Personnes morales"}.get(cod, cod)
    print(f"  {lib:<25}: {nb:>4} ({nb/total_cli:.1%})")

print()
print(f"  TOP 3 CLIENTS PAR NB DE CONTRATS :")
print(f"  {'─'*48}")
for rang, (pi, nb) in enumerate(top3, 1):
    print(f"  {rang}. {pi:<12} : {nb} contrat(s)")

print()
print(f"  SOLDES ({len(soldes_valides)} renseignés / {total_ctr} total) :")
print(f"  {'─'*48}")
if soldes_valides:
    print(f"  Somme   : {sum(soldes_valides):>16,.2f} EUR")
    print(f"  Moyenne : {sum(soldes_valides)/len(soldes_valides):>16,.2f} EUR")
    print(f"  Min     : {min(soldes_valides):>16,.2f} EUR")
    print(f"  Max     : {max(soldes_valides):>16,.2f} EUR")

print()
print("╚" + "═"*54 + "╝")"""),

md("""---
# Récapitulatif du Jour 1

## Ce que vous maîtrisez maintenant

| Concept | Syntaxe clé | Exercice |
|---------|------------|---------|
| Variables et types | `nom = valeur` | Ex. 1 |
| Affichage formaté | `f"{var:,.2f}"` | Ex. 1 |
| Conditions | `if / elif / else` | Ex. 2 |
| Boucle for | `for x in liste:` | Ex. 3 |
| Listes | `[a,b,c]`, comprehension | Ex. 4 |
| Tuples | `(a,b,c)` immuable | Ex. 5 |
| Dictionnaires | `{"k":v}`, `.get()` | Ex. 6 |
| Fonctions | `def f(x): return y` | Ex. 7 |
| Gestion erreurs | `try/except` | Ex. 8 |
| Lecture CSV | `csv.DictReader` | Ex. 9 |
| Rapport complet | tout combiné | Final |

## Demain (Jour 2)

Vous allez faire tout ça en **3 lignes** avec Pandas :
```python
import pandas as pd
ctr = pd.read_csv("../Orsys/CTR.csv", sep=";", na_values=".")
ctr["COD_ECV_CTR"].value_counts()
```
Mais grâce à aujourd'hui, vous comprenez ce que Pandas fait en coulisses !"""),
]

chemin = os.path.join(OUT, "Jour1_Fondamentaux_Python.ipynb")
with open(chemin, "w", encoding="utf-8") as f:
    json.dump(nb(cells), f, ensure_ascii=False, indent=1)
print(f"Jour 1 : {os.path.getsize(chemin)//1024} Ko — {len(cells)} cellules")
