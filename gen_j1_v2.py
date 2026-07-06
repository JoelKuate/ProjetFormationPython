"""
Generateur Jour 1 v2 - Fondamentaux Python
Chaque ligne de code est commentee. Mini-exercices intercales avec corrections.
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

j1 = [

# ============================================================
# PAGE DE GARDE
# ============================================================
md("""# Jour 1 — Fondamentaux Python pour analystes Beobank
## Formation Python 3 jours · 18 novembre 2026

---

### Votre formateur et votre contexte

Vous etes **analyste chez Beobank**. Jusqu'a aujourd'hui vous utilisiez **SAS** pour manipuler des donnees.
Cette formation vous donne les bases Python necessaires pour faire exactement le meme travail, en mieux.

### Fil rouge de la formation

Tout au long des 3 jours, vous allez construire un **rapport mensuel d'activite** a presenter
au comite de direction. Vous travaillerez sur les vraies tables Beobank :

| Table | Contenu | Lignes |
|-------|---------|--------|
| `CTR.csv` | Contrats (comptes) | 200 |
| `TIE.csv` | Clients (tiers) | 100 |
| `TIE_ADR.csv` | Adresses des clients | 100 |
| `TIE_X_CTR.csv` | Liens client-contrat | 200 |
| `TXN_X_CTR.csv` | Transactions | 1260 |

### Comment lire ce notebook

- Les cellules **grises** contiennent du code Python a executer (Shift + Entree)
- Les cellules **blanches** (comme celle-ci) sont des explications
- Chaque exercice a son **corrige** dans la cellule juste en dessous
- **Lisez les commentaires dans le code** : chaque ligne est expliquee

> **Conseil pour les debutants :** Ne cherchez pas a tout memoriser. Comprenez la logique.
> Le reste vient avec la pratique."""),

md("""---
## Pourquoi Python apres SAS ?

Vous vous demandez peut-etre pourquoi changer. Voici la comparaison honnete :

| Critere | SAS | Python |
|---------|-----|--------|
| Cout | Licence chere | Gratuit (open source) |
| Syntaxe | Rigide, verbeuse | Concise, lisible |
| Visualisation | Limitee | Matplotlib, Seaborn, Plotly... |
| Machine learning | Limite | scikit-learn, TensorFlow, PyTorch |
| Communaute | Specialisee | Enorme (millions de developpeurs) |
| Courbe d'apprentissage | Moderate | Un peu plus lente au debut |

**Ce que Python ne change pas :** votre logique metier. Un calcul d'echeance reste
le meme, que vous l'ecriviez en SAS ou en Python.

### Les 3 grandes regles de Python

1. **L'indentation compte** — les blocs de code sont delimites par des espaces (pas par `DO/END`)
2. **Tout est objet** — les donnees ont des methodes (fonctions attachees)
3. **Lisible d'abord** — Python force l'ecriture de code clair"""),

# ============================================================
# SECTION 1 : PREMIERS PAS
# ============================================================
md("""---
# Section 1 — Premiers pas en Python

## 1.1 Votre premiere cellule de code

Avant de charger des donnees Beobank, apprenons les briques de base.
`print()` affiche du texte dans la console. C'est l'equivalent de `put` en SAS."""),

code("""# Le signe # commence un commentaire : Python l'ignore completement
# Les commentaires servent a expliquer le code aux autres (et a vous-meme dans 6 mois)

# print() affiche quelque chose a l'ecran
# Les guillemets indiquent que c'est du texte (une "chaine de caracteres")
print("Bonjour, je suis analyste chez Beobank !")

# On peut afficher plusieurs choses en separant par des virgules
# Python ajoute automatiquement un espace entre chaque element
print("Aujourd'hui nous etudions", "Python", "version", 3)

# On peut aussi calculer directement dans le print()
print("2 + 2 =", 2 + 2)"""),

md("""### Ce que vous venez de voir

- `print(...)` : affiche ce qu'il y a entre les parentheses
- `"texte"` : une chaine de caracteres (toujours entre guillemets)
- `# commentaire` : Python ignore tout ce qui suit le `#`
- Les calculs (`2 + 2`) sont evalues avant l'affichage

**En SAS :** `put "Bonjour";` — meme idee, syntaxe differente."""),

# ============================================================
# SECTION 2 : VARIABLES
# ============================================================
md("""---
## 1.2 Variables — stocker une valeur

Une variable, c'est une **boite avec une etiquette**. Vous choisissez le nom de l'etiquette,
Python se souvient de ce qu'il y a dedans.

**En SAS :** `data _null_; nom_client = "DUPONT"; run;`
**En Python :** `nom_client = "DUPONT"` — plus court, meme resultat."""),

code("""# ── Creer une variable ──────────────────────────────────────
# A gauche du = : le nom de la variable (vous choisissez)
# A droite du = : la valeur a stocker
# Pas de "data step", pas de "run", pas de type a declarer !

nom_client = "DUPONT"      # variable de type texte (str)
prenom     = "Marie"       # autre variable texte
age        = 42            # variable de type entier (int)
solde      = 15234.87      # variable de type decimal (float)
est_actif  = True          # variable de type booleen (True ou False)

# ── Afficher les variables ───────────────────────────────────
# On ecrit juste le nom de la variable dans print()
print("Nom :", nom_client)
print("Prenom :", prenom)
print("Age :", age)
print("Solde :", solde, "EUR")
print("Compte actif :", est_actif)"""),

code("""# ── Les types de donnees en Python ──────────────────────────
# type() retourne le type d'une variable

print("Type de nom_client :", type(nom_client))   # <class 'str'>  = texte
print("Type de age :",        type(age))            # <class 'int'>  = entier
print("Type de solde :",      type(solde))          # <class 'float'>= decimal
print("Type de est_actif :",  type(est_actif))      # <class 'bool'> = booleen

# ── Modifier une variable ────────────────────────────────────
# Vous pouvez changer la valeur a tout moment
age = 43                    # on ecrase l'ancienne valeur
print()                     # afficher une ligne vide
print("Nouvel age :", age)  # affiche 43, pas 42

# ── Combiner des variables (f-string) ───────────────────────
# La lettre f devant les guillemets active les f-strings
# {variable} dans le texte est remplace par la valeur de la variable
message = f"Client : {prenom} {nom_client}, {age} ans"
print(message)"""),

code("""# ── Operations sur les nombres ──────────────────────────────
solde_initial  = 15234.87   # solde de depart
depot          = 500.00     # montant depose
frais          = 12.50      # frais de tenue de compte

solde_final = solde_initial + depot - frais  # calcul en une ligne
print("Solde initial :", solde_initial, "EUR")
print("Depot         :", depot, "EUR")
print("Frais         :", frais, "EUR")
print("Solde final   :", solde_final, "EUR")

print()

# Les operateurs arithmetiques
print("Addition       :", 100 + 50)     # 150
print("Soustraction   :", 100 - 30)     # 70
print("Multiplication :", 100 * 2)      # 200
print("Division       :", 100 / 3)      # 33.333...
print("Division entiere:", 100 // 3)   # 33  (partie entiere seulement)
print("Reste (modulo) :", 100 % 3)      # 1   (reste de 100 / 3)
print("Puissance      :", 2 ** 10)      # 1024"""),

# ============================================================
# MINI-EXERCICE 1
# ============================================================
md("""---
### Mini-exercice 1.A — Variables Beobank

**Contexte :** Vous travaillez sur le contrat numero `CTR-20240529-001` du client `MARTIN Sophie`.
Le contrat a ete ouvert le `29/05/2024` avec un solde initial de `8 500 EUR`.
Les frais mensuels sont de `15 EUR`.

**A faire :**
1. Creer une variable `ref_contrat` avec la reference du contrat
2. Creer `nom_client` avec le nom du client
3. Creer `solde_ini` avec 8500.0
4. Creer `frais_mensuels` avec 15.0
5. Calculer `solde_apres_3_mois` (solde initial moins 3 mois de frais)
6. Afficher un message comme : `"Contrat CTR-... : solde apres 3 mois = XXX EUR"`

**Espace de travail ci-dessous :**"""),

code("""# ── Votre code ici ─────────────────────────────────────────
# Exercice 1.A : Variables Beobank

# 1. Reference du contrat
ref_contrat = "..."         # remplacez ... par la valeur

# 2. Nom du client
nom_client = "..."

# 3. Solde initial
solde_ini = ...

# 4. Frais mensuels
frais_mensuels = ...

# 5. Solde apres 3 mois (solde_ini - 3 * frais_mensuels)
solde_apres_3_mois = ...

# 6. Affichage (utilisez une f-string)
print(f"Contrat {ref_contrat} : solde apres 3 mois = {solde_apres_3_mois} EUR")"""),

md("""**Correction exercice 1.A :**"""),

code("""# ── CORRECTION exercice 1.A ────────────────────────────────

# 1. Reference du contrat
ref_contrat = "CTR-20240529-001"

# 2. Nom du client
nom_client = "MARTIN Sophie"

# 3. Solde initial
solde_ini = 8500.0

# 4. Frais mensuels
frais_mensuels = 15.0

# 5. Calcul : solde initial moins 3 mois de frais
#    3 * frais_mensuels = 3 * 15.0 = 45.0
solde_apres_3_mois = solde_ini - 3 * frais_mensuels

# 6. Affichage avec f-string
#    Les accolades {} dans la f-string sont remplaces par la valeur de la variable
print(f"Contrat {ref_contrat} : solde apres 3 mois = {solde_apres_3_mois} EUR")

# Verification pas a pas
print()
print(f"  Solde initial    : {solde_ini} EUR")
print(f"  Frais (3 mois)   : {3 * frais_mensuels} EUR")
print(f"  Solde resultant  : {solde_apres_3_mois} EUR")"""),

# ============================================================
# SECTION 3 : CONDITIONS
# ============================================================
md("""---
## 1.3 Conditions — prendre une decision

Les conditions permettent d'executer du code **seulement si** une condition est vraie.

**En SAS :**
```sas
if COD_ECV_CTR = '1' then STATUT = 'Ouvert';
else if COD_ECV_CTR = '4' then STATUT = 'Cloture';
else STATUT = 'Autre';
```

**En Python :** meme logique, syntaxe differente (et pas de `;` ni de `then`)"""),

code("""# ── Structure if / elif / else ──────────────────────────────
# if  : SI cette condition est vraie, execute le bloc
# elif: SINON SI cette autre condition est vraie (autant qu'on veut)
# else: SINON (cas par defaut)
# IMPORTANT : les blocs sont delimites par l'INDENTATION (4 espaces)

cod_ecv_ctr = "1"   # code statut d'un contrat Beobank

# Test de la condition
if cod_ecv_ctr == "1":              # == verifie l'egalite (= assigne)
    statut = "Ouvert"               # ce bloc s'execute si cod_ecv_ctr == "1"
    print("Le contrat est OUVERT")  # les 4 espaces d'indentation sont obligatoires
elif cod_ecv_ctr == "2":            # sinon, si cod_ecv_ctr == "2"
    statut = "En attente"
    print("Le contrat est EN ATTENTE")
elif cod_ecv_ctr == "3":            # sinon, si cod_ecv_ctr == "3"
    statut = "Suspendu"
    print("Le contrat est SUSPENDU")
elif cod_ecv_ctr == "4":            # sinon, si cod_ecv_ctr == "4"
    statut = "Cloture"
    print("Le contrat est CLOTURE")
elif cod_ecv_ctr == "5":
    statut = "En resiliation"
    print("Le contrat est EN RESILIATION")
elif cod_ecv_ctr == "6":
    statut = "Resilie"
    print("Le contrat est RESILIE")
else:                               # aucune condition precedente n'est vraie
    statut = "Inconnu"
    print("Code statut inconnu :", cod_ecv_ctr)

# Affichage du statut choisi
print("Statut du contrat :", statut)"""),

code("""# ── Les operateurs de comparaison ───────────────────────────
# Ces operateurs retournent True ou False

x = 10  # valeur de test

print(x == 10)   # True  : est-ce que x est egal a 10 ?
print(x == 20)   # False : est-ce que x est egal a 20 ?
print(x != 5)    # True  : est-ce que x est DIFFERENT de 5 ?
print(x > 5)     # True  : est-ce que x est superieur a 5 ?
print(x >= 10)   # True  : est-ce que x est superieur OU EGAL a 10 ?
print(x < 100)   # True  : est-ce que x est inferieur a 100 ?
print(x <= 10)   # True  : est-ce que x est inferieur OU EGAL a 10 ?

print()  # ligne vide

# ── Conditions combinees : and / or / not ────────────────────
solde = 1500.0  # solde du compte
statut = "1"    # statut du contrat

# and : les DEUX conditions doivent etre vraies
if solde > 0 and statut == "1":
    print("Compte actif avec solde positif")

# or : AU MOINS UNE condition doit etre vraie
if statut == "5" or statut == "6":
    print("Contrat en cours de resiliation ou resilie")
else:
    print("Contrat non resilie")

# not : inverse la condition
if not (statut == "4"):  # si le statut n'est PAS egal a "4"
    print("Le contrat n'est pas cloture")"""),

code("""# ── Condition sur une chaine de caracteres ──────────────────
# in : verifie si une valeur est contenue dans une liste ou un texte
# Tres utile pour les codes bancaires !

cod_ecv = "3"   # code statut

# Verifier si le code correspond a un statut "actif"
# On peut passer une liste de valeurs possibles
if cod_ecv in ("1", "2", "3"):      # parentheses = tuple (explication section 5)
    categorie = "Actif"
elif cod_ecv in ("4", "5", "6"):
    categorie = "Inactif"
else:
    categorie = "Inconnu"

print(f"Code {cod_ecv} → categorie : {categorie}")

print()

# ── Exemples avec les donnees Beobank ───────────────────────
# COD_TYP_TIE : 1 = personne physique, 2 = personne morale
cod_typ = "1"

if cod_typ == "1":
    type_client = "Personne physique"
elif cod_typ == "2":
    type_client = "Personne morale"
else:
    type_client = "Type inconnu"

print(f"Type de client : {type_client}")"""),

# ============================================================
# MINI-EXERCICE 2
# ============================================================
md("""---
### Mini-exercice 1.B — Classer un contrat Beobank

**Contexte :** Le tableau de bord du comite de direction doit afficher
la **priorite de suivi** de chaque contrat selon son statut :

| Statut (`COD_ECV_CTR`) | Libelle | Priorite |
|------------------------|---------|----------|
| 1 | Ouvert | Faible |
| 2 | En attente | Moyenne |
| 3 | Suspendu | Haute |
| 4 | Cloture | Aucune |
| 5 | En resiliation | Critique |
| 6 | Resilie | Aucune |

**A faire :**
1. Creer une variable `cod_ecv` avec la valeur `"3"` (vous la changerez pour tester)
2. Ecrire un bloc if/elif/else qui assigne la bonne `priorite`
3. Afficher : `"Contrat statut 3 (Suspendu) → priorite : Haute"`

Testez ensuite avec les valeurs `"1"`, `"5"`, `"4"` pour verifier."""),

code("""# ── Votre code ici ─────────────────────────────────────────
# Exercice 1.B

cod_ecv = "3"   # changez cette valeur pour tester

# Votre if / elif / else ici :
# ...

# Affichage :
# print(f"Contrat statut {cod_ecv} (...) → priorite : {priorite}")"""),

md("""**Correction exercice 1.B :**"""),

code("""# ── CORRECTION exercice 1.B ────────────────────────────────

cod_ecv = "3"   # changez cette valeur pour tester : "1", "2", "3", "4", "5", "6"

# Mapping code → libelle (on en aura besoin pour l'affichage)
if cod_ecv == "1":
    libelle  = "Ouvert"
    priorite = "Faible"
elif cod_ecv == "2":
    libelle  = "En attente"
    priorite = "Moyenne"
elif cod_ecv == "3":
    libelle  = "Suspendu"
    priorite = "Haute"
elif cod_ecv == "4":
    libelle  = "Cloture"
    priorite = "Aucune"
elif cod_ecv == "5":
    libelle  = "En resiliation"
    priorite = "Critique"
elif cod_ecv == "6":
    libelle  = "Resilie"
    priorite = "Aucune"
else:
    libelle  = "Inconnu"
    priorite = "Inconnue"

# Affichage complet
print(f"Contrat statut {cod_ecv} ({libelle}) → priorite : {priorite}")

# Bonus : affichage conditionnel selon la priorite
if priorite == "Critique":
    print("  *** ACTION REQUISE : contrat en resiliation ***")
elif priorite == "Haute":
    print("  Attention : contrat suspendu, a surveiller")"""),

# ============================================================
# SECTION 4 : BOUCLES
# ============================================================
md("""---
## 1.4 Boucles — repeter une action

Une boucle execute un bloc de code **plusieurs fois**, sur une liste de valeurs.

**En SAS :** `do i = 1 to 10; ... end;` ou traitement implicite du dataset
**En Python :** `for element in liste: ...`"""),

code("""# ── Boucle for sur une liste ────────────────────────────────
# "pour chaque element de la liste, execute le bloc"
# La variable 'statut' prend successivement chaque valeur

statuts = ["Ouvert", "En attente", "Suspendu", "Cloture"]  # une liste Python

for statut in statuts:          # pour chaque statut dans la liste
    print("Statut :", statut)   # afficher le statut (indente = dans la boucle)

# Ce print est en dehors de la boucle (pas indente)
print("--- Fin de la boucle ---")"""),

code("""# ── Boucle for avec range() ─────────────────────────────────
# range(N) genere les entiers de 0 a N-1
# range(debut, fin) genere de debut a fin-1
# range(debut, fin, pas) genere avec un pas

print("range(5) → 0 a 4 :")
for i in range(5):              # i prend les valeurs 0, 1, 2, 3, 4
    print(f"  i = {i}")

print()
print("range(1, 6) → 1 a 5 :")
for i in range(1, 6):           # i prend les valeurs 1, 2, 3, 4, 5
    print(f"  i = {i}")

print()
print("range(0, 13, 3) → 0, 3, 6, 9, 12 :")
for mois in range(0, 13, 3):    # de 0 a 12, pas de 3 (trimestres)
    print(f"  mois = {mois}")"""),

code("""# ── Boucle for sur une liste de codes Beobank ───────────────
# Simulation : iterer sur des codes de statut et afficher leur libelle

codes_statut = ["1", "2", "3", "4", "5", "6"]  # tous les codes CTR

print("Codes de statut Beobank :")
print("-" * 35)  # afficher 35 fois le tiret - (ligne de separation)

for code in codes_statut:           # pour chaque code dans la liste
    # Determiner le libelle avec un if/elif
    if code == "1":
        libelle = "Ouvert"
    elif code == "2":
        libelle = "En attente"
    elif code == "3":
        libelle = "Suspendu"
    elif code == "4":
        libelle = "Cloture"
    elif code == "5":
        libelle = "En resiliation"
    else:
        libelle = "Resilie"
    # Afficher le resultat pour ce code
    print(f"  Code {code} → {libelle}")   # indente = dans la boucle"""),

code("""# ── Compteur dans une boucle ────────────────────────────────
# Tres courant : compter des elements selon un critere

codes = ["1", "1", "3", "4", "1", "6", "2", "4", "1"]  # extrait fictif
total   = 0   # compteur total (commence a zero)
actifs  = 0   # compteur de contrats actifs

for code in codes:          # pour chaque code
    total = total + 1       # incrementer le total a chaque iteration
    if code in ("1", "2", "3"):  # si le code correspond a un statut actif
        actifs = actifs + 1      # incrementer le compteur actifs

print(f"Total contrats analyses : {total}")
print(f"Contrats actifs         : {actifs}")
print(f"Contrats inactifs       : {total - actifs}")
print(f"Taux d'activite         : {actifs / total * 100:.1f}%")
# :.1f signifie : format decimal avec 1 chiffre apres la virgule"""),

code("""# ── Boucle while ────────────────────────────────────────────
# La boucle while continue TANT QUE la condition est vraie
# ATTENTION : s'assurer que la condition devient False, sinon boucle infinie

# Exemple : simuler des penalites de retard mensuelles
solde    = 1000.0   # solde initial
taux     = 0.02     # 2% de penalite par mois
mois     = 0        # compteur de mois

# Continuer tant que le solde est superieur a 500 EUR
while solde > 500:
    solde = solde * (1 - taux)  # reduire le solde de 2%
    mois  = mois + 1            # incrementer le compteur

    # Afficher l'etat actuel
    print(f"Mois {mois:>2} → Solde : {solde:>8.2f} EUR")
    # :>2 = aligne a droite sur 2 caracteres
    # :>8.2f = decimal aligne a droite sur 8 caracteres, 2 decimales

print()
print(f"Seuil de 500 EUR atteint apres {mois} mois")"""),

# ============================================================
# MINI-EXERCICE 3
# ============================================================
md("""---
### Mini-exercice 1.C — Parcourir des contrats

**Contexte :** Voici une liste simplifiee de 8 contrats fictifs avec leur statut :

```python
contrats = [
    {"ref": "CTR-001", "statut": "1", "solde": 12500.0},
    {"ref": "CTR-002", "statut": "4", "solde": 0.0},
    {"ref": "CTR-003", "statut": "1", "solde": 3200.0},
    {"ref": "CTR-004", "statut": "6", "solde": 0.0},
    {"ref": "CTR-005", "statut": "3", "solde": 890.0},
    {"ref": "CTR-006", "statut": "1", "solde": 45000.0},
    {"ref": "CTR-007", "statut": "5", "solde": 150.0},
    {"ref": "CTR-008", "statut": "1", "solde": 7800.0},
]
```

**A faire avec une boucle `for` :**
1. Compter combien de contrats sont actifs (statut 1, 2 ou 3)
2. Calculer le solde total des contrats actifs
3. Afficher chaque contrat avec son statut en texte
4. A la fin, afficher le nombre et le total des actifs"""),

code("""# ── Votre code ici ─────────────────────────────────────────
# Exercice 1.C

contrats = [
    {"ref": "CTR-001", "statut": "1", "solde": 12500.0},
    {"ref": "CTR-002", "statut": "4", "solde": 0.0},
    {"ref": "CTR-003", "statut": "1", "solde": 3200.0},
    {"ref": "CTR-004", "statut": "6", "solde": 0.0},
    {"ref": "CTR-005", "statut": "3", "solde": 890.0},
    {"ref": "CTR-006", "statut": "1", "solde": 45000.0},
    {"ref": "CTR-007", "statut": "5", "solde": 150.0},
    {"ref": "CTR-008", "statut": "1", "solde": 7800.0},
]

# Initialisez vos compteurs ici
nb_actifs    = 0
solde_actifs = 0.0

# Ecrivez votre boucle for ici
# for contrat in contrats:
#     ...

# Affichage final
# print(f"Contrats actifs : {nb_actifs}, Solde total : {solde_actifs} EUR")"""),

md("""**Correction exercice 1.C :**"""),

code("""# ── CORRECTION exercice 1.C ────────────────────────────────

contrats = [
    {"ref": "CTR-001", "statut": "1", "solde": 12500.0},
    {"ref": "CTR-002", "statut": "4", "solde": 0.0},
    {"ref": "CTR-003", "statut": "1", "solde": 3200.0},
    {"ref": "CTR-004", "statut": "6", "solde": 0.0},
    {"ref": "CTR-005", "statut": "3", "solde": 890.0},
    {"ref": "CTR-006", "statut": "1", "solde": 45000.0},
    {"ref": "CTR-007", "statut": "5", "solde": 150.0},
    {"ref": "CTR-008", "statut": "1", "solde": 7800.0},
]

# Dictionnaire de correspondance code → libelle
mapping_statut = {
    "1": "Ouvert", "2": "En attente", "3": "Suspendu",
    "4": "Cloture", "5": "En resiliation", "6": "Resilie"
}

# Initialisation des compteurs avant la boucle
nb_actifs    = 0       # comptera les contrats actifs
solde_actifs = 0.0     # accumulera les soldes des actifs

print(f"{'Reference':<10}  {'Statut':>3}  {'Libelle':<18}  {'Solde':>12}  {'Categorie'}")
print("-" * 65)

for contrat in contrats:         # pour chaque contrat de la liste
    # contrat est un dictionnaire : contrat["ref"], contrat["statut"]...
    ref    = contrat["ref"]      # extraire la reference
    statut = contrat["statut"]   # extraire le code statut
    solde  = contrat["solde"]    # extraire le solde

    # Obtenir le libelle depuis le dictionnaire de mapping
    libelle = mapping_statut.get(statut, "Inconnu")  # get() securise

    # Determiner la categorie
    if statut in ("1", "2", "3"):
        categorie = "Actif"
        nb_actifs    += 1         # += est equivalent a nb_actifs = nb_actifs + 1
        solde_actifs += solde     # accumuler le solde
    else:
        categorie = "Inactif"

    # Afficher la ligne du contrat
    print(f"{ref:<10}  {statut:>3}  {libelle:<18}  {solde:>12,.2f}  {categorie}")
    # :<10 = aligne a gauche sur 10 caracteres
    # :>12,.2f = decimal aligne droite sur 12 car., separateur de milliers, 2 dec.

print("-" * 65)
print()
print(f"Contrats actifs  : {nb_actifs}")
print(f"Solde total actifs : {solde_actifs:,.2f} EUR")
print(f"Solde moyen actifs : {solde_actifs / nb_actifs:,.2f} EUR")"""),

# ============================================================
# SECTION 5 : LISTES
# ============================================================
md("""---
## 1.5 Listes — collections ordonnees

Une liste est une **collection d'elements dans un ordre precis**.
C'est la structure de base pour stocker plusieurs valeurs.

**Analogie SAS :** les listes ressemblent aux colonnes d'un dataset, ou a un tableau a une dimension."""),

code("""# ── Creer une liste ─────────────────────────────────────────
# Les listes sont definies entre crochets [ ]
# Les elements sont separes par des virgules

devises        = ["EUR", "USD", "GBP", "CHF"]   # liste de textes
soldes         = [1200.0, 450.5, 890.0, 15000.0] # liste de decimaux
codes_statut   = ["1", "1", "3", "4", "6"]       # liste mixte
liste_vide     = []                                # liste vide (pour y ajouter ensuite)

# ── Acceder a un element ─────────────────────────────────────
# L'index commence a 0 (pas 1 !)
# devises[0] = premier element, devises[1] = deuxieme, etc.
# devises[-1] = dernier element, devises[-2] = avant-dernier

print("La liste des devises :", devises)
print("Premier element   (index 0)  :", devises[0])   # "EUR"
print("Deuxieme element  (index 1)  :", devises[1])   # "USD"
print("Dernier element   (index -1) :", devises[-1])  # "CHF"
print("Avant-dernier     (index -2) :", devises[-2])  # "GBP"
print("Nombre d'elements : len() =  :", len(devises)) # 4"""),

code("""# ── Modifier une liste ──────────────────────────────────────
langues = ["FR", "NL"]   # langues Beobank

# append() : ajouter un element a la FIN
langues.append("DE")               # ajouter l'allemand
print("Apres append('DE') :", langues)    # ['FR', 'NL', 'DE']

# insert(index, valeur) : inserer a une position precise
langues.insert(1, "EN")            # inserer 'EN' a la position 1
print("Apres insert(1,'EN'):", langues)   # ['FR', 'EN', 'NL', 'DE']

# remove(valeur) : supprimer la PREMIERE occurrence d'une valeur
langues.remove("EN")               # supprimer 'EN'
print("Apres remove('EN')  :", langues)   # ['FR', 'NL', 'DE']

# pop() : supprimer et retourner le DERNIER element
dernier = langues.pop()            # pop() sans argument = dernier element
print("Element retire :", dernier)         # 'DE'
print("Liste restante :", langues)         # ['FR', 'NL']

# len() : nombre d'elements
print("Nombre de langues :", len(langues))  # 2"""),

code("""# ── Trancher une liste (slicing) ────────────────────────────
# liste[debut:fin] extrait les elements de l'index debut a fin-1
# liste[debut:fin:pas] extrait avec un pas

codes = ["1", "2", "3", "4", "5", "6"]   # les 6 codes de statut

print("Tous les codes           :", codes)       # tous
print("Les 3 premiers (0:3)    :", codes[0:3])   # "1", "2", "3"
print("De l'index 2 a 5 (2:5)  :", codes[2:5])  # "3", "4", "5"
print("Les 2 derniers (-2:)    :", codes[-2:])   # "5", "6"
print("Tous sauf le dernier(:-1):", codes[:-1])  # "1" a "5"
print("Un sur deux (::2)       :", codes[::2])   # "1", "3", "5"
print("Inverse (::-1)          :", codes[::-1])  # "6", "5", "4", "3", "2", "1"

print()

# ── Tester si un element est dans la liste ───────────────────
code_recherche = "3"
if code_recherche in codes:     # in verifie la presence dans la liste
    print(f"Le code {code_recherche} est dans la liste")
else:
    print(f"Le code {code_recherche} n'est PAS dans la liste")"""),

code("""# ── Operations utiles sur les listes ────────────────────────
soldes = [1200.0, 450.5, 890.0, 15000.0, 230.0, 4500.0]

# Fonctions integrees sur les listes numeriques
print("Somme     :", sum(soldes))      # additionne tous les elements
print("Minimum   :", min(soldes))      # le plus petit
print("Maximum   :", max(soldes))      # le plus grand
print("Nombre    :", len(soldes))      # nombre d'elements
print("Moyenne   :", sum(soldes) / len(soldes))   # calculee manuellement

# sorted() : retourne une NOUVELLE liste triee (la liste originale n'est pas modifiee)
soldes_tries = sorted(soldes)             # ordre croissant
soldes_desc  = sorted(soldes, reverse=True)  # ordre decroissant
print("Tries croissant  :", soldes_tries)
print("Tries decroissant:", soldes_desc)

# sort() : trie LA liste sur place (modifie la liste originale)
soldes.sort()
print("Apres sort()     :", soldes)"""),

code("""# ── List comprehension : creer une liste en une ligne ────────
# Syntaxe : [expression for element in liste if condition]
# C'est l'equivalent Python de SELECT ... FROM ... WHERE ...

codes = ["1", "2", "3", "4", "5", "6"]

# Extraire seulement les codes "actifs" (1, 2, 3)
# VERSION longue (boucle for classique) :
codes_actifs_long = []
for c in codes:
    if c in ("1", "2", "3"):
        codes_actifs_long.append(c)
print("Version longue    :", codes_actifs_long)

# VERSION courte (list comprehension) - meme resultat :
codes_actifs = [c for c in codes if c in ("1", "2", "3")]
print("List comprehension:", codes_actifs)

print()

# Transformer une liste (convertir les codes en libelles)
mapping = {"1": "Ouvert", "2": "En attente", "3": "Suspendu",
           "4": "Cloture", "5": "En resiliation", "6": "Resilie"}

libelles = [mapping[c] for c in codes]   # remplacer chaque code par son libelle
print("Libelles :", libelles)"""),

# ============================================================
# MINI-EXERCICE 4
# ============================================================
md("""---
### Mini-exercice 1.D — Analyser des soldes de contrats

**Contexte :** Vous avez extrait les soldes de 10 contrats Beobank.

```python
soldes = [12500.0, 0.0, 3200.0, 0.0, 890.0, 45000.0, 150.0, 7800.0, 0.0, 22000.0]
```

**A faire :**
1. Calculer le nombre total de contrats
2. Calculer la somme totale et la moyenne des soldes
3. Creer une liste `soldes_positifs` contenant uniquement les soldes > 0
   (utilisez une list comprehension)
4. Trouver le solde maximum parmi les positifs
5. Afficher un resume complet"""),

code("""# ── Votre code ici ─────────────────────────────────────────
# Exercice 1.D

soldes = [12500.0, 0.0, 3200.0, 0.0, 890.0, 45000.0, 150.0, 7800.0, 0.0, 22000.0]

# 1. Nombre total
nb_total = ...

# 2. Somme et moyenne
somme   = ...
moyenne = ...

# 3. List comprehension pour soldes > 0
soldes_positifs = [...]

# 4. Maximum des positifs
max_solde = ...

# 5. Affichage
print(f"Nombre total     : {nb_total}")
print(f"Somme totale     : {somme:,.2f} EUR")
# etc."""),

md("""**Correction exercice 1.D :**"""),

code("""# ── CORRECTION exercice 1.D ────────────────────────────────

soldes = [12500.0, 0.0, 3200.0, 0.0, 890.0, 45000.0, 150.0, 7800.0, 0.0, 22000.0]

# 1. Nombre total de contrats dans la liste
nb_total = len(soldes)                      # len() = nombre d'elements

# 2. Somme et moyenne
somme   = sum(soldes)                       # sum() = somme de tous les elements
moyenne = somme / nb_total                  # division simple

# 3. List comprehension : garder uniquement les soldes strictement positifs
#    [expression for element in liste if condition]
soldes_positifs = [s for s in soldes if s > 0]

# 4. Maximum parmi les soldes positifs
max_solde    = max(soldes_positifs)         # max() = le plus grand element
nb_positifs  = len(soldes_positifs)
nb_nuls      = nb_total - nb_positifs       # contrats avec solde nul

# 5. Resume complet
print("=" * 40)
print("  RESUME DES SOLDES BEOBANK")
print("=" * 40)
print(f"  Nombre total de contrats : {nb_total}")
print(f"  Contrats avec solde > 0  : {nb_positifs}")
print(f"  Contrats avec solde = 0  : {nb_nuls}")
print()
print(f"  Somme totale             : {somme:>12,.2f} EUR")
print(f"  Moyenne                  : {moyenne:>12,.2f} EUR")
print(f"  Solde maximum            : {max_solde:>12,.2f} EUR")
print()
print(f"  Soldes positifs          : {soldes_positifs}")"""),

# ============================================================
# SECTION 6 : DICTIONNAIRES
# ============================================================
md("""---
## 1.6 Dictionnaires — cle : valeur

Un dictionnaire associe des **cles** a des **valeurs**.
C'est l'outil ideal pour les **mappings** (correspondances de codes) et les **enregistrements** (un client, un contrat).

**Analogie SAS :** un dictionnaire ressemble a une table a une seule ligne, ou a un `format` SAS."""),

code("""# ── Creer un dictionnaire ───────────────────────────────────
# Les dictionnaires sont definis entre accolades { }
# Chaque element est une paire "cle": valeur

# Un enregistrement de contrat (comme une ligne de la table CTR)
contrat = {
    "IDT_AC"      : "AC001",        # identifiant du contrat (texte)
    "REF_CTR_INN" : "CTR-2024-001", # reference interne
    "COD_ECV_CTR" : "1",            # code statut
    "SLD_CTR"     : 12500.87,       # solde
    "COD_DEV"     : "EUR",          # devise
    "DAT_OUV_CTR" : "2024-05-29",   # date d'ouverture
}

# Afficher le dictionnaire complet
print("Contrat complet :", contrat)
print()

# ── Acceder a une valeur ─────────────────────────────────────
# On utilise la cle entre crochets [ ]
print("Identifiant    :", contrat["IDT_AC"])
print("Solde          :", contrat["SLD_CTR"], "EUR")
print("Statut         :", contrat["COD_ECV_CTR"])
print()

# get() : version securisee (retourne None si la cle n'existe pas)
# Evite une erreur KeyError si la cle est absente
libelle = contrat.get("LIB_ECV", "Inconnu")  # "LIB_ECV" n'existe pas → "Inconnu"
print("Libelle statut :", libelle)"""),

code("""# ── Modifier et ajouter des entrees ─────────────────────────
client = {
    "IDT_PI"      : "PI001",
    "NUM_TIE"     : "TIE001",
    "COD_TYP_TIE" : "1",
    "COD_SEX"     : "F",
    "COD_LNG_CTR" : "FR",
}

# Modifier une valeur existante
client["COD_LNG_CTR"] = "NL"        # changer la langue
print("Langue modifiee :", client["COD_LNG_CTR"])

# Ajouter une nouvelle cle
client["AGE"]         = 45          # ajouter l'age (n'existait pas)
client["SEGMENT"]     = "Premium"   # ajouter le segment
print("Client enrichi  :", client)

print()

# ── Parcourir un dictionnaire ────────────────────────────────
print("Contenu du dictionnaire client :")
for cle, valeur in client.items():  # .items() donne les paires (cle, valeur)
    print(f"  {cle:20s}: {valeur}") # aligner les cles sur 20 caracteres"""),

code("""# ── Dictionnaire de mapping (equivalent FORMAT SAS) ─────────
# Tres utile pour convertir des codes en libelles

# Mapping des codes statut CTR → libelle
MAPPING_STATUT = {
    "1": "Ouvert",
    "2": "En attente",
    "3": "Suspendu",
    "4": "Cloture",
    "5": "En resiliation",
    "6": "Resilie",
}

# Mapping des codes langue → libelle
MAPPING_LANGUE = {
    "FR": "Francais",
    "NL": "Neerlandais",
}

# Utilisation du mapping
codes_a_convertir = ["1", "3", "4", "6", "2"]

print("Conversion des codes :")
for code in codes_a_convertir:
    # .get(code, "Inconnu") : si le code n'est pas dans le dict, retourne "Inconnu"
    libelle = MAPPING_STATUT.get(code, "Inconnu")
    print(f"  {code} → {libelle}")"""),

code("""# ── Liste de dictionnaires : simuler une table ───────────────
# Structure tres utilisee avant de charger Pandas
# Chaque dictionnaire = une ligne de la table

clients = [
    {"IDT_PI": "PI001", "NOM": "MARTIN",  "LANGUE": "FR", "TYPE": "1"},
    {"IDT_PI": "PI002", "NOM": "DUPONT",  "LANGUE": "NL", "TYPE": "1"},
    {"IDT_PI": "PI003", "NOM": "BEOBANK", "LANGUE": "FR", "TYPE": "2"},
    {"IDT_PI": "PI004", "NOM": "LEROY",   "LANGUE": "NL", "TYPE": "1"},
]

MAPPING_TYPE = {"1": "Personne physique", "2": "Personne morale"}

print(f"{'IDT_PI':<8}  {'Nom':<10}  {'Langue':<10}  {'Type'}")
print("-" * 50)
for client in clients:            # pour chaque ligne (dictionnaire)
    idt   = client["IDT_PI"]      # extraire chaque champ
    nom   = client["NOM"]
    lng   = MAPPING_LANGUE.get(client["LANGUE"], client["LANGUE"])
    typ   = MAPPING_TYPE.get(client["TYPE"], "?")
    print(f"{idt:<8}  {nom:<10}  {lng:<10}  {typ}")"""),

# ============================================================
# MINI-EXERCICE 5
# ============================================================
md("""---
### Mini-exercice 1.E — Mapping des codes Beobank

**Contexte :** La table `TIE.csv` contient un code `COD_SEX` (M ou F)
et un code `COD_LNG_CTR` (FR ou NL).
Votre manager veut un rapport avec les libelles complets, pas les codes.

**Donnees :**
```python
clients = [
    {"IDT_PI": "PI001", "COD_SEX": "F", "COD_LNG_CTR": "FR"},
    {"IDT_PI": "PI002", "COD_SEX": "M", "COD_LNG_CTR": "NL"},
    {"IDT_PI": "PI003", "COD_SEX": "M", "COD_LNG_CTR": "FR"},
    {"IDT_PI": "PI004", "COD_SEX": "F", "COD_LNG_CTR": "NL"},
    {"IDT_PI": "PI005", "COD_SEX": "M", "COD_LNG_CTR": "FR"},
]
```

**A faire :**
1. Creer un dictionnaire `MAPPING_SEXE` : `"M"` → `"Masculin"`, `"F"` → `"Feminin"`
2. Creer un dictionnaire `MAPPING_LNG` : `"FR"` → `"Francais"`, `"NL"` → `"Neerlandais"`
3. Parcourir la liste et afficher un tableau avec les libelles complets
4. Compter et afficher le nombre de clients par langue"""),

code("""# ── Votre code ici ─────────────────────────────────────────
# Exercice 1.E

clients = [
    {"IDT_PI": "PI001", "COD_SEX": "F", "COD_LNG_CTR": "FR"},
    {"IDT_PI": "PI002", "COD_SEX": "M", "COD_LNG_CTR": "NL"},
    {"IDT_PI": "PI003", "COD_SEX": "M", "COD_LNG_CTR": "FR"},
    {"IDT_PI": "PI004", "COD_SEX": "F", "COD_LNG_CTR": "NL"},
    {"IDT_PI": "PI005", "COD_SEX": "M", "COD_LNG_CTR": "FR"},
]

# 1. Dictionnaire de mapping sexe
MAPPING_SEXE = {...}

# 2. Dictionnaire de mapping langue
MAPPING_LNG = {...}

# 3. Boucle d'affichage
for client in clients:
    ...

# 4. Comptage par langue
...
"""),

md("""**Correction exercice 1.E :**"""),

code("""# ── CORRECTION exercice 1.E ────────────────────────────────

clients = [
    {"IDT_PI": "PI001", "COD_SEX": "F", "COD_LNG_CTR": "FR"},
    {"IDT_PI": "PI002", "COD_SEX": "M", "COD_LNG_CTR": "NL"},
    {"IDT_PI": "PI003", "COD_SEX": "M", "COD_LNG_CTR": "FR"},
    {"IDT_PI": "PI004", "COD_SEX": "F", "COD_LNG_CTR": "NL"},
    {"IDT_PI": "PI005", "COD_SEX": "M", "COD_LNG_CTR": "FR"},
]

# 1. Mapping sexe
MAPPING_SEXE = {
    "M": "Masculin",
    "F": "Feminin",
}

# 2. Mapping langue
MAPPING_LNG = {
    "FR": "Francais",
    "NL": "Neerlandais",
}

# 3. Affichage avec libelles
print(f"{'IDT_PI':<8}  {'Sexe':<12}  {'Langue':<14}")
print("-" * 38)
for client in clients:
    sexe_lib = MAPPING_SEXE.get(client["COD_SEX"],    client["COD_SEX"])
    lng_lib  = MAPPING_LNG.get(client["COD_LNG_CTR"], client["COD_LNG_CTR"])
    print(f"{client['IDT_PI']:<8}  {sexe_lib:<12}  {lng_lib:<14}")

print()

# 4. Comptage par langue
# Utiliser un dictionnaire pour compter (cle=langue, valeur=compteur)
comptage_lng = {}   # dictionnaire vide

for client in clients:
    lng = client["COD_LNG_CTR"]   # code langue du client actuel
    if lng in comptage_lng:        # si la langue est deja dans le comptage
        comptage_lng[lng] += 1     # incrementer le compteur
    else:
        comptage_lng[lng] = 1      # initialiser le compteur a 1

print("Repartition par langue :")
for code_lng, nb in comptage_lng.items():
    libelle = MAPPING_LNG.get(code_lng, code_lng)
    print(f"  {libelle}: {nb} client(s)")"""),

# ============================================================
# SECTION 7 : FONCTIONS
# ============================================================
md("""---
## 1.7 Fonctions — reutiliser du code

Une fonction est un **bloc de code reutilisable** que vous definissez une fois
et appelez autant de fois que necessaire.

**En SAS :** les macros (`%macro/%mend`) ont le meme role.
**En Python :** `def nom_fonction(parametres): ...`"""),

code("""# ── Definir une fonction simple ──────────────────────────────
# def  : mot-cle pour definir une fonction
# nom  : vous choisissez (conventions : minuscules, underscores)
# ()   : les parametres (inputs) entre parentheses
# :    : debut du bloc de la fonction
# return : valeur retournee par la fonction

def saluer(prenom):
    '''Affiche un message de bienvenue.'''  # docstring (documentation)
    message = f"Bonjour, {prenom} !"       # construire le message
    return message                          # retourner le message

# Appel de la fonction
resultat = saluer("Marie")    # appeler avec l'argument "Marie"
print(resultat)               # afficher le resultat

# On peut appeler la fonction autant de fois qu'on veut
print(saluer("Jean"))
print(saluer("Lena"))"""),

code("""# ── Fonction avec plusieurs parametres ──────────────────────
# Les parametres peuvent avoir des valeurs par defaut

def calculer_solde_apres_frais(solde_ini, taux_frais, nb_mois=1):
    '''
    Calcule le solde apres application des frais mensuels.

    solde_ini  : solde initial (float)
    taux_frais : taux de frais mensuel en decimal (ex: 0.02 = 2%)
    nb_mois    : nombre de mois (defaut = 1)
    Retourne le solde final (float).
    '''
    frais_total = solde_ini * taux_frais * nb_mois   # frais cumules
    solde_final = solde_ini - frais_total             # solde restant
    return solde_final                                # retourner le resultat

# Appel avec 2 parametres (nb_mois utilise sa valeur par defaut = 1)
resultat_1m = calculer_solde_apres_frais(10000.0, 0.02)
print(f"Solde apres 1 mois  : {resultat_1m:.2f} EUR")

# Appel avec 3 parametres (on override la valeur par defaut)
resultat_6m = calculer_solde_apres_frais(10000.0, 0.02, 6)
print(f"Solde apres 6 mois  : {resultat_6m:.2f} EUR")

# Appel avec parametres nommes (plus lisible)
resultat_12m = calculer_solde_apres_frais(
    solde_ini  = 10000.0,
    taux_frais = 0.02,
    nb_mois    = 12
)
print(f"Solde apres 12 mois : {resultat_12m:.2f} EUR")"""),

code("""# ── Fonction qui retourne plusieurs valeurs ──────────────────
# Python peut retourner un tuple (plusieurs valeurs)

def analyser_contrat(cod_ecv_ctr, solde):
    '''
    Analyse un contrat et retourne son statut enrichi.
    Retourne un tuple (libelle, categorie, alerte).
    '''
    # Mapper le code vers le libelle
    mapping = {
        "1": "Ouvert", "2": "En attente", "3": "Suspendu",
        "4": "Cloture", "5": "En resiliation", "6": "Resilie"
    }
    libelle = mapping.get(cod_ecv_ctr, "Inconnu")

    # Determiner la categorie
    if cod_ecv_ctr in ("1", "2", "3"):
        categorie = "Actif"
    else:
        categorie = "Inactif"

    # Determiner l'alerte
    if cod_ecv_ctr in ("5", "6"):
        alerte = "CRITIQUE"
    elif cod_ecv_ctr == "3":
        alerte = "ATTENTION"
    elif solde < 0:
        alerte = "SOLDE NEGATIF"
    else:
        alerte = "OK"

    return libelle, categorie, alerte   # retourner 3 valeurs (tuple)

# Appel et deballage du tuple
lib, cat, ale = analyser_contrat("3", 890.0)   # = deballage du tuple
print(f"Libelle   : {lib}")
print(f"Categorie : {cat}")
print(f"Alerte    : {ale}")

print()

# Tester differents cas
for cod, sld in [("1", 5000), ("5", 150), ("4", 0), ("3", -100)]:
    l, c, a = analyser_contrat(cod, sld)
    print(f"Code {cod}, solde {sld:>6} → {l:<18} [{c}] {a}")"""),

code("""# ── Fonctions lambda (fonctions anonymes courtes) ────────────
# lambda : mot-cle pour creer une fonction en une ligne
# Utilise pour des operations simples qu'on ne veut pas nommer formellement

# Version longue avec def
def doubler(x):
    return x * 2

# Version courte avec lambda
doubler_lambda = lambda x: x * 2   # lambda parametre: expression

# Les deux sont equivalents
print("def :", doubler(5))          # 10
print("lambda :", doubler_lambda(5)) # 10

# Les lambdas sont souvent utilises avec sorted() ou map()
contrats = [
    {"ref": "B", "solde": 3000},
    {"ref": "A", "solde": 1000},
    {"ref": "C", "solde": 2000},
]

# Trier les contrats par solde (key = la valeur sur laquelle trier)
tries_par_solde = sorted(contrats, key=lambda c: c["solde"])
print()
print("Trie par solde :")
for c in tries_par_solde:
    print(f"  {c['ref']} : {c['solde']} EUR")

# Trier par ref (alphabetique)
tries_par_ref = sorted(contrats, key=lambda c: c["ref"])
print("Trie par ref :")
for c in tries_par_ref:
    print(f"  {c['ref']} : {c['solde']} EUR")"""),

# ============================================================
# MINI-EXERCICE 6
# ============================================================
md("""---
### Mini-exercice 1.F — Fonctions d'analyse Beobank

**Contexte :** Le service risque veut une fonction qui classe chaque client
selon son **segment** de solde, et une fonction qui verifie si un client est eligible
a une offre Premium.

**Regles metier :**
- Solde < 1 000 EUR → segment `"Standard"`
- 1 000 ≤ Solde < 10 000 EUR → segment `"Confort"`
- Solde ≥ 10 000 EUR → segment `"Premium"`

**Eligible Premium si :** solde >= 10 000 ET statut actif (1, 2 ou 3) ET age >= 25

**A faire :**
1. Ecrire la fonction `classifier_segment(solde)` qui retourne le segment
2. Ecrire la fonction `est_eligible_premium(solde, statut, age)` qui retourne `True` ou `False`
3. Tester avec les contrats de l'exercice 1.C"""),

code("""# ── Votre code ici ─────────────────────────────────────────
# Exercice 1.F

# 1. Fonction classifier_segment
def classifier_segment(solde):
    '''Retourne le segment selon le solde.'''
    # votre code ici
    ...

# 2. Fonction est_eligible_premium
def est_eligible_premium(solde, statut, age):
    '''Retourne True si le client est eligible Premium.'''
    # votre code ici
    ...

# 3. Tests
cas_test = [
    {"solde": 500.0,   "statut": "1", "age": 30},
    {"solde": 5000.0,  "statut": "1", "age": 40},
    {"solde": 12000.0, "statut": "1", "age": 50},
    {"solde": 15000.0, "statut": "4", "age": 60},  # statut inactif
    {"solde": 15000.0, "statut": "1", "age": 20},  # age trop jeune
]

print(f"{'Solde':>10}  {'Statut'}  {'Age'}  {'Segment':<10}  {'Premium ?'}")
print("-" * 55)
for cas in cas_test:
    segment = classifier_segment(cas["solde"])
    premium = est_eligible_premium(cas["solde"], cas["statut"], cas["age"])
    print(f"{cas['solde']:>10,.0f}  {cas['statut']:>6}  {cas['age']:>3}  {segment:<10}  {premium}")"""),

md("""**Correction exercice 1.F :**"""),

code("""# ── CORRECTION exercice 1.F ────────────────────────────────

# 1. Classifier selon le solde
def classifier_segment(solde):
    '''Retourne le segment selon le solde.'''
    if solde < 1000:              # solde sous 1000
        return "Standard"
    elif solde < 10000:           # entre 1000 et 9999.99
        return "Confort"
    else:                         # 10000 et plus
        return "Premium"

# 2. Verifier l'eligibilite Premium
def est_eligible_premium(solde, statut, age):
    '''Retourne True si toutes les conditions Premium sont remplies.'''
    condition_solde  = solde  >= 10000       # solde suffisant
    condition_statut = statut in ("1","2","3") # contrat actif
    condition_age    = age    >= 25           # age suffisant
    # Les 3 conditions doivent etre vraies (and)
    return condition_solde and condition_statut and condition_age

# 3. Tests sur les cas
cas_test = [
    {"solde": 500.0,   "statut": "1", "age": 30},
    {"solde": 5000.0,  "statut": "1", "age": 40},
    {"solde": 12000.0, "statut": "1", "age": 50},
    {"solde": 15000.0, "statut": "4", "age": 60},
    {"solde": 15000.0, "statut": "1", "age": 20},
]

print(f"{'Solde':>10}  {'Statut':>6}  {'Age':>3}  {'Segment':<10}  {'Premium ?':<10}  Raison")
print("-" * 70)
for cas in cas_test:
    segment = classifier_segment(cas["solde"])
    premium = est_eligible_premium(cas["solde"], cas["statut"], cas["age"])

    # Expliquer pourquoi non-eligible
    if not premium:
        if cas["solde"] < 10000:
            raison = "Solde insuffisant"
        elif cas["statut"] not in ("1","2","3"):
            raison = "Statut inactif"
        elif cas["age"] < 25:
            raison = "Age < 25 ans"
        else:
            raison = ""
    else:
        raison = "Toutes conditions OK"

    prem_str = "OUI" if premium else "NON"
    print(f"{cas['solde']:>10,.0f}  {cas['statut']:>6}  {cas['age']:>3}  {segment:<10}  {prem_str:<10}  {raison}")"""),

# ============================================================
# SECTION 8 : TUPLES ET SETS
# ============================================================
md("""---
## 1.8 Tuples et ensembles (rapide)

### Tuples
Un tuple est comme une liste, mais **immutable** (on ne peut pas le modifier).
On les utilise pour des valeurs fixes (coordonnees, retours multiples de fonction).

```python
point = (48.8566, 2.3522)   # latitude, longitude de Paris
```

### Sets (ensembles)
Un set est une collection **sans doublons** et **sans ordre**.
Tres utile pour trouver les valeurs uniques."""),

code("""# ── Tuples ──────────────────────────────────────────────────
# Definis avec des parentheses ( )

coordonnees  = (50.8503, 4.3517)   # Bruxelles (lat, lon) - immuable
currencies   = ("EUR", "USD")       # paire de devises

# Acceder aux elements comme une liste
print("Latitude  :", coordonnees[0])
print("Longitude :", coordonnees[1])

# Deballage du tuple
lat, lon = coordonnees   # assigner chaque element a une variable
print(f"Ville: Bruxelles, lat={lat}, lon={lon}")

# On ne peut PAS modifier un tuple
# coordonnees[0] = 51.0  # → TypeError ! (c'est voulu)

print()

# ── Sets (ensembles) ────────────────────────────────────────
# Definis avec des accolades { } (sans cle:valeur)
# Pas de doublons, ordre non garanti

# Extraire les devises uniques utilisees dans nos contrats
devises_avec_doublons = ["EUR", "USD", "EUR", "EUR", "CHF", "USD", "EUR"]
devises_uniques = set(devises_avec_doublons)  # supprimer les doublons
print("Devises avec doublons :", devises_avec_doublons)
print("Devises uniques       :", devises_uniques)   # ordre variable

# Compter les uniques
print("Nombre de devises distinctes :", len(devises_uniques))

# Verifier la presence (plus rapide que dans une liste)
if "CHF" in devises_uniques:
    print("Le franc suisse est utilise")"""),

# ============================================================
# SECTION 9 : GESTION DES ERREURS
# ============================================================
md("""---
## 1.9 Gerer les erreurs avec try / except

En analyse de donnees, les donnees manquantes et les erreurs de format sont frequentes.
`try/except` permet de continuer le traitement sans que le programme s'arrete.

**En SAS :** les options `_ERROR_` et `NOERRORABEND` ont un role similaire."""),

code("""# ── Erreur sans protection ──────────────────────────────────
# Decommenter la ligne suivante pour voir l'erreur :
# int("abc")   # ValueError: invalid literal for int() with base 10: 'abc'

# ── Protection avec try / except ────────────────────────────
# try  : Python essaie d'executer ce bloc
# except : si une erreur survient, ce bloc est execute a la place

valeurs_brutes = ["12500", "N/A", "890", "", "45000", "abc", "7800"]

print("Conversion des valeurs en nombres :")
for val in valeurs_brutes:
    try:
        nombre = float(val)       # tenter la conversion en decimal
        print(f"  '{val}' → {nombre:.2f} (OK)")
    except ValueError:            # si la conversion echoue (ValueError)
        print(f"  '{val}' → ERREUR DE FORMAT (traite comme 0)")
        nombre = 0.0              # valeur par defaut en cas d'erreur"""),

code("""# ── Gestion des valeurs manquantes Beobank ──────────────────
# Dans nos fichiers CSV, les valeurs manquantes sont notees "."  (convention SAS)
# Pandas les gere automatiquement, mais il faut les connaitre en Python pur

donnees_brutes = {
    "IDT_AC"      : "AC001",
    "SLD_CTR"     : "15234.87",
    "DAT_CLO_CTR" : ".",          # valeur manquante SAS
    "COD_DEV"     : "EUR",
    "MNT_INI"     : ".",          # valeur manquante SAS
}

print("Lecture securisee des donnees :")
for cle, val in donnees_brutes.items():
    if val == "." or val == "" or val is None:
        # Valeur manquante : afficher avec indication
        print(f"  {cle:20s}: [MANQUANT]")
    else:
        # Valeur presente : essayer de convertir en nombre si applicable
        try:
            valeur_num = float(val)
            print(f"  {cle:20s}: {valeur_num}")
        except ValueError:
            # Pas convertible en nombre : c'est du texte
            print(f"  {cle:20s}: {val}")"""),

# ============================================================
# MINI-EXERCICE 7
# ============================================================
md("""---
### Mini-exercice 1.G — Nettoyer des donnees brutes

**Contexte :** Vous recevez un extrait brut d'un fichier Beobank avec des problemes :
certains soldes sont des chaines vides, d'autres contiennent `.` (manquant SAS),
et un est clairement une erreur de saisie.

```python
extrait = [
    {"ref": "CTR-001", "solde_brut": "12500.50"},
    {"ref": "CTR-002", "solde_brut": "."},
    {"ref": "CTR-003", "solde_brut": ""},
    {"ref": "CTR-004", "solde_brut": "N/A"},
    {"ref": "CTR-005", "solde_brut": "8900"},
    {"ref": "CTR-006", "solde_brut": "abc123"},
    {"ref": "CTR-007", "solde_brut": "45000.00"},
]
```

**A faire :**
1. Creer une fonction `nettoyer_solde(valeur_brute)` qui :
   - Retourne `None` si la valeur est `.` ou vide
   - Retourne le float si la conversion reussit
   - Retourne `None` si la conversion echoue (try/except)
2. Appliquer cette fonction sur chaque ligne
3. Afficher : valeur brute → valeur nettoyee (ou "MANQUANT")
4. Compter les valeurs valides et les manquantes"""),

code("""# ── Votre code ici ─────────────────────────────────────────
# Exercice 1.G

extrait = [
    {"ref": "CTR-001", "solde_brut": "12500.50"},
    {"ref": "CTR-002", "solde_brut": "."},
    {"ref": "CTR-003", "solde_brut": ""},
    {"ref": "CTR-004", "solde_brut": "N/A"},
    {"ref": "CTR-005", "solde_brut": "8900"},
    {"ref": "CTR-006", "solde_brut": "abc123"},
    {"ref": "CTR-007", "solde_brut": "45000.00"},
]

def nettoyer_solde(valeur_brute):
    '''Nettoie une valeur de solde brute. Retourne float ou None.'''
    # votre code ici
    ...

# Application et affichage
nb_valides   = 0
nb_manquants = 0
for ligne in extrait:
    ...
"""),

md("""**Correction exercice 1.G :**"""),

code("""# ── CORRECTION exercice 1.G ────────────────────────────────

extrait = [
    {"ref": "CTR-001", "solde_brut": "12500.50"},
    {"ref": "CTR-002", "solde_brut": "."},
    {"ref": "CTR-003", "solde_brut": ""},
    {"ref": "CTR-004", "solde_brut": "N/A"},
    {"ref": "CTR-005", "solde_brut": "8900"},
    {"ref": "CTR-006", "solde_brut": "abc123"},
    {"ref": "CTR-007", "solde_brut": "45000.00"},
]

def nettoyer_solde(valeur_brute):
    '''
    Nettoie une valeur de solde brute.
    Retourne un float si la valeur est valide, None sinon.
    '''
    # Etape 1 : verifier si c'est une valeur manquante connue
    if valeur_brute in (".", "", "N/A", None):
        return None   # valeur manquante : retourner None

    # Etape 2 : tenter la conversion en float
    try:
        return float(valeur_brute)   # si ca marche, retourner le nombre
    except ValueError:
        return None   # si ca plante, retourner None

# Application et affichage
print(f"{'Reference':<10}  {'Valeur brute':<15}  {'Valeur nettoyee':<18}  {'Statut'}")
print("-" * 62)

nb_valides   = 0
nb_manquants = 0

for ligne in extrait:
    ref        = ligne["ref"]
    solde_brut = ligne["solde_brut"]
    solde_net  = nettoyer_solde(solde_brut)  # appel de la fonction

    if solde_net is not None:   # is not None : verifier que ce n'est pas None
        nb_valides += 1
        affichage  = f"{solde_net:>12,.2f} EUR"
        statut     = "Valide"
    else:
        nb_manquants += 1
        affichage    = "MANQUANT"
        statut       = "Ignore"

    print(f"{ref:<10}  {repr(solde_brut):<15}  {affichage:<18}  {statut}")
    # repr() affiche la chaine avec ses guillemets (pour voir les vides)

print("-" * 62)
print(f"Valeurs valides   : {nb_valides}")
print(f"Valeurs manquantes: {nb_manquants}")"""),

# ============================================================
# SECTION 10 : LIRE UN VRAI FICHIER BEOBANK
# ============================================================
md("""---
## 1.10 Premiere lecture d'un fichier Beobank (sans Pandas)

Avant d'utiliser Pandas (Jour 2), comprenons comment Python lit un fichier CSV.
Cela vous aidera a comprendre ce que Pandas fait en coulisses."""),

code("""# ── Lire CTR.csv avec le module csv de Python ────────────────
import csv          # module standard Python pour les fichiers CSV
from pathlib import Path  # module pour manipuler les chemins de fichiers

# Path() cree un objet "chemin" qui fonctionne sur Windows et Mac/Linux
dossier_data = Path("../Orsys")  # aller dans le dossier parent, puis Orsys

# Ouvrir le fichier
# "r" = read (lecture), encoding="utf-8" = encodage des accents
print("Lecture du fichier CTR.csv...")
print()

with open(dossier_data / "CTR.csv", "r", encoding="utf-8") as fichier:
    # with ... as : ouvre le fichier et le ferme automatiquement apres le bloc
    # csv.DictReader : lit chaque ligne comme un dictionnaire
    lecteur = csv.DictReader(fichier, delimiter=";")  # separateur = ;

    # Lire la premiere ligne (en-tete) pour voir les colonnes
    colonnes = lecteur.fieldnames   # liste des noms de colonnes
    print("Colonnes disponibles :")
    for col in colonnes:
        print(f"  - {col}")

print()
print(f"Total colonnes : {len(colonnes)}")"""),

code("""# ── Lire et analyser les premieres lignes de CTR.csv ────────
import csv
from pathlib import Path

dossier_data = Path("../Orsys")
contrats_lus = []   # liste vide pour stocker les contrats lus

with open(dossier_data / "CTR.csv", "r", encoding="utf-8") as fichier:
    lecteur = csv.DictReader(fichier, delimiter=";")

    for ligne in lecteur:     # pour chaque ligne du fichier
        # ligne est un dictionnaire : cle = nom de colonne, valeur = valeur cellule
        contrats_lus.append(ligne)   # ajouter la ligne a notre liste

# Afficher les 3 premieres lignes
print(f"Nombre de contrats lus : {len(contrats_lus)}")
print()
print("Les 3 premiers contrats :")
print("-" * 70)

for contrat in contrats_lus[:3]:    # [:3] = les 3 premiers
    print(f"IDT_AC  : {contrat['IDT_AC']}")
    print(f"REF     : {contrat['REF_CTR_INN']}")
    print(f"ECV     : {contrat['COD_ECV_CTR']}")
    print(f"SOLDE   : {contrat['SLD_CTR']}")
    print(f"DEVISE  : {contrat['COD_DEV']}")
    print(f"OUV     : {contrat['DAT_OUV_CTR']}")
    print("-" * 70)"""),

code("""# ── Analyser les contrats lus ────────────────────────────────
# Utiliser ce qu'on a appris (boucles, dicts, conditions, fonctions)

import csv
from pathlib import Path

dossier_data = Path("../Orsys")
contrats_lus = []

with open(dossier_data / "CTR.csv", "r", encoding="utf-8") as fichier:
    lecteur = csv.DictReader(fichier, delimiter=";")
    for ligne in lecteur:
        contrats_lus.append(ligne)

# Compter par statut
comptage_statut = {}   # dictionnaire vide

MAPPING_STATUT = {
    "1": "Ouvert", "2": "En attente", "3": "Suspendu",
    "4": "Cloture", "5": "En resiliation", "6": "Resilie"
}

for contrat in contrats_lus:
    code = contrat["COD_ECV_CTR"]           # code statut de ce contrat
    if code in comptage_statut:              # si le code est deja dans le dict
        comptage_statut[code] += 1           # incrementer
    else:
        comptage_statut[code] = 1            # initialiser a 1

# Afficher le tableau de repartition
print(f"Analyse de {len(contrats_lus)} contrats CTR.csv")
print()
print(f"{'Code':>5}  {'Libelle':<20}  {'Nb':>5}  {'Pct':>7}")
print("-" * 42)

total = len(contrats_lus)
for code, nb in sorted(comptage_statut.items()):   # trier par code
    lib = MAPPING_STATUT.get(code, "Inconnu")
    pct = nb / total * 100
    print(f"{code:>5}  {lib:<20}  {nb:>5}  {pct:>6.1f}%")

print("-" * 42)
print(f"{'TOTAL':>5}  {'':20}  {total:>5}  {100.0:>6.1f}%")"""),

# ============================================================
# EXERCICE FINAL DU JOUR 1
# ============================================================
md("""---
# Exercice final du Jour 1

## Synthese — Rapport d'inventaire des contrats Beobank

**Contexte :** Le directeur veut un rapport simple sur l'etat du portefeuille.
Vous devez produire ce rapport en Python pur (sans Pandas, seulement ce qu'on a vu aujourd'hui).

**Donnees :** `CTR.csv` et `TIE.csv` dans le dossier `../Orsys/`

**A produire :**
1. Nombre total de contrats par statut (comptage + %)
2. Repartition par devise (COD_DEV)
3. Identifier les contrats avec solde manquant (SLD_CTR = ".")
4. Calculer la moyenne des soldes disponibles
5. Afficher un rapport structure

**Conseil :** relisez les sections 4 (boucles), 6 (dictionnaires) et 10 (lecture fichier)."""),

code("""# ── EXERCICE FINAL - Votre code ────────────────────────────
import csv
from pathlib import Path

DOSSIER = Path("../Orsys")
MAPPING = {
    "1":"Ouvert","2":"En attente","3":"Suspendu",
    "4":"Cloture","5":"En resiliation","6":"Resilie"
}

# Chargez CTR.csv et produisez le rapport
# ...
print("A completer !")"""),

md("""**Correction de l'exercice final :**"""),

code("""# ── CORRECTION EXERCICE FINAL ──────────────────────────────
import csv
from pathlib import Path

DOSSIER = Path("../Orsys")
MAPPING_STATUT = {
    "1":"Ouvert","2":"En attente","3":"Suspendu",
    "4":"Cloture","5":"En resiliation","6":"Resilie"
}
MAPPING_CAT = {
    "1":"Actif","2":"Actif","3":"Actif",
    "4":"Inactif","5":"Inactif","6":"Inactif"
}

# ── 1. Charger CTR.csv ───────────────────────────────────────
contrats = []
with open(DOSSIER / "CTR.csv", "r", encoding="utf-8") as f:
    for ligne in csv.DictReader(f, delimiter=";"):
        contrats.append(ligne)

total = len(contrats)

# ── 2. Comptage par statut ───────────────────────────────────
par_statut = {}
par_devise = {}
soldes_valides = []
nb_manquants = 0

for c in contrats:
    # Statut
    ecv = c["COD_ECV_CTR"]
    par_statut[ecv] = par_statut.get(ecv, 0) + 1

    # Devise
    dev = c["COD_DEV"] if c["COD_DEV"] != "." else "INCONNUE"
    par_devise[dev] = par_devise.get(dev, 0) + 1

    # Solde
    sld = c["SLD_CTR"]
    if sld == "." or sld == "" or sld is None:
        nb_manquants += 1
    else:
        try:
            soldes_valides.append(float(sld))
        except ValueError:
            nb_manquants += 1

# ── 3. Afficher le rapport ───────────────────────────────────
print("=" * 55)
print("  RAPPORT D'INVENTAIRE CONTRATS BEOBANK")
print("=" * 55)
print()

print("  1. REPARTITION PAR STATUT")
print(f"  {'Code':>4}  {'Libelle':<20}  {'N':>5}  {'%':>7}  {'Categorie'}")
print("  " + "-" * 50)
for code in sorted(par_statut):
    nb  = par_statut[code]
    lib = MAPPING_STATUT.get(code, "Inconnu")
    cat = MAPPING_CAT.get(code, "?")
    pct = nb / total * 100
    print(f"  {code:>4}  {lib:<20}  {nb:>5}  {pct:>6.1f}%  {cat}")
print("  " + "-" * 50)
print(f"  {'':4}  {'TOTAL':<20}  {total:>5}  {100.0:>6.1f}%")

print()
print("  2. REPARTITION PAR DEVISE")
print(f"  {'Devise':>7}  {'N':>5}  {'%':>7}")
print("  " + "-" * 22)
for dev in sorted(par_devise):
    nb  = par_devise[dev]
    pct = nb / total * 100
    print(f"  {dev:>7}  {nb:>5}  {pct:>6.1f}%")

print()
print("  3. QUALITE DES SOLDES")
nb_valides = len(soldes_valides)
print(f"  Soldes renseignes  : {nb_valides}")
print(f"  Soldes manquants   : {nb_manquants}")
print(f"  Taux de remplissage: {nb_valides/total*100:.1f}%")
if nb_valides > 0:
    print()
    print("  4. STATISTIQUES DES SOLDES")
    print(f"  Somme    : {sum(soldes_valides):>15,.2f} EUR")
    print(f"  Moyenne  : {sum(soldes_valides)/nb_valides:>15,.2f} EUR")
    print(f"  Minimum  : {min(soldes_valides):>15,.2f} EUR")
    print(f"  Maximum  : {max(soldes_valides):>15,.2f} EUR")
print()
print("=" * 55)
print("  Fin du rapport")
print("=" * 55)"""),

# ============================================================
# SYNTHESE JOUR 1
# ============================================================
md("""---
# Synthese du Jour 1

## Ce que vous avez appris aujourd'hui

| Notion | Python | Equivalent SAS |
|--------|--------|----------------|
| Affichage | `print("texte")` | `put "texte";` |
| Variable texte | `nom = "DUPONT"` | `nom = "DUPONT";` |
| Variable numerique | `solde = 1234.5` | `solde = 1234.5;` |
| Condition | `if x == "1": ...` | `if x = "1" then ...;` |
| Boucle | `for x in liste: ...` | `do i = 1 to n; ... end;` |
| Commentaire | `# commentaire` | `/* commentaire */` |
| Liste | `[a, b, c]` | Array SAS / colonne dataset |
| Dictionnaire | `{"cle": valeur}` | Format SAS / table de mapping |
| Fonction | `def ma_fonction(): ...` | `%macro ma_macro; %mend;` |
| Try/except | `try: ... except: ...` | `_ERROR_` / `NOERRORABEND` |
| Lire un CSV | `csv.DictReader(...)` | `proc import` |

## Exercices pratiques realises
- **1.A** Variables et calcul de solde
- **1.B** Classification des statuts de contrat
- **1.C** Boucle sur une liste de contrats
- **1.D** Analyse des soldes avec list comprehension
- **1.E** Mapping des codes Beobank en libelles
- **1.F** Fonctions de classification et d'eligibilite
- **1.G** Nettoyage de donnees brutes
- **Final** Rapport d'inventaire complet sur CTR.csv

## Ce qui vous attend demain (Jour 2)

Demain vous ferez tout ca **en 3 lignes** grace a **Pandas** :
```python
import pandas as pd
df = pd.read_csv("CTR.csv", sep=";", na_values=".")
df["COD_ECV_CTR"].value_counts()
```
Mais maintenant vous savez **ce que Pandas fait en coulisses** !"""),

]  # fin j1

path = os.path.join(OUTPUT_DIR, "Jour1_Fondamentaux_Python.ipynb")
with open(path, "w", encoding="utf-8") as f:
    json.dump(notebook(j1), f, ensure_ascii=False, indent=1)
print(f"Jour 1 v2 cree : {os.path.getsize(path)//1024} Ko — {len(j1)} cellules")
