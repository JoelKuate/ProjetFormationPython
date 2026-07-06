"""
Générateur des notebooks de formation Python Beobank
3 jours · Public : analystes data venant de SAS/SaaS
Données : CTR, TIE, TIE_ADR, TIE_X_CTR, TXN_X_CTR (séparateur ;, manquant .)
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


# =============================================================
# JOUR 1 — Fondamentaux Python pour analystes data
# =============================================================

j1 = [

md("""# Jour 1 — Fondamentaux Python pour Analystes Data
## Formation Python Beobank · 18 novembre 2026

**Exécutez chaque cellule avec `Shift + Entrée`.**

### Objectifs de la journée
- Comprendre les différences entre SAS et Python
- Maîtriser les types, variables, conditions et boucles
- Utiliser listes, tuples et dictionnaires
- Écrire des fonctions propres et réutilisables
- Découvrir les lambda expressions"""),

# ----- 1. Python vs SAS -----
md("""---
## 1. Python vs SAS : ce qui change

Vous venez de SAS. Voici les équivalences clés pour ne pas être perdu.

| Concept | SAS | Python |
|---------|-----|--------|
| Afficher une valeur | `put variable;` | `print(variable)` |
| Commentaire | `/* ... */` ou `* ... ;` | `# ligne` ou `\'\'\'bloc\'\'\'` |
| Bloc de code | `DATA ... ; RUN;` | **indentation** (4 espaces) |
| Affecter une variable | `x = 5;` | `x = 5` (pas de `;`) |
| Valeur manquante | `.` ou `' '` | `None` ou `NaN` |
| Chaîne de caractères | `'texte'` | `'texte'` ou `"texte"` |
| Boucle sur observations | `DATA _null_; set ds; ...` | `for ligne in liste:` |

> **Règle d'or Python :** l'indentation (les espaces en début de ligne) DÉLIMITE les blocs.
> Oubliez les `RUN;` et les `;` en fin de ligne !"""),

# ----- 2. Variables et types -----
md("""---
## 2. Variables et types de données"""),

code("""# En Python, pas besoin de déclarer le type : il est déduit automatiquement
nom_client   = "JANSSENS"       # str  → chaîne de caractères
prenom       = "Bart"           # str
age          = 45               # int  → entier
solde        = 1250.75          # float → décimal
est_actif    = True             # bool → booléen (True / False)
date_naiss   = None             # None → valeur manquante (équivalent du . en SAS)

# Afficher les valeurs
print("Client :", prenom, nom_client)
print("Solde  :", solde, "EUR")
print("Actif  :", est_actif)"""),

code("""# Vérifier le type d'une variable
print(type(nom_client))   # <class 'str'>
print(type(solde))        # <class 'float'>
print(type(age))          # <class 'int'>
print(type(est_actif))    # <class 'bool'>"""),

# ----- f-strings -----
md("""### 2.1 Affichage avec les f-strings (la façon moderne en Python)

Équivalent du `put` en SAS, mais bien plus lisible."""),

code("""# f-string : on préfixe la chaîne avec f et on met les variables entre { }
prenom = "Bart"
solde  = 1250.75
devise = "EUR"

message = f"Bonjour {prenom}, votre solde est de {solde:.2f} {devise}"
print(message)

# :.2f = afficher avec 2 décimales
print(f"Solde arrondi : {solde:.2f}")
print(f"Solde entier  : {int(solde)}")"""),

# ----- 3. Conditions -----
md("""---
## 3. Conditions : if / elif / else

Equivalent SAS : `if ... then ... else ...`

> ATTENTION : en Python, les blocs sont délimités par l'indentation, PAS par des mots-clés `end`."""),

code("""# Exemple bancaire : classification d'un contrat selon son code état
cod_ecv_ctr = "4"   # code état du contrat (COD_ECV_CTR dans la table CTR)

if cod_ecv_ctr == "1":
    statut = "Ouvert"
elif cod_ecv_ctr == "4":
    statut = "Clôturé"
elif cod_ecv_ctr == "6":
    statut = "Résilié"
else:
    statut = "Statut inconnu"

print(f"Code état {cod_ecv_ctr} → {statut}")"""),

code("""# Opérateurs de comparaison
solde = 500.0

print(solde > 0)       # True  → solde positif
print(solde == 0)      # False → solde nul
print(solde >= 1000)   # False → solde >= 1000

# Opérateurs logiques : and, or, not
langue = "FR"
sexe   = "M"

if langue == "FR" and sexe == "M":
    civilite = "Monsieur"
elif langue == "FR" and sexe == "F":
    civilite = "Madame"
else:
    civilite = "Client"

print(civilite)"""),

code("""# Condition sur valeur manquante (None)
# En SAS on teste : if solde = . then ...
# En Python :

solde = None   # équivalent du . SAS

if solde is None:
    print("Solde non renseigné")
else:
    print(f"Solde : {solde:.2f} EUR")"""),

# ----- 4. Boucles -----
md("""---
## 4. Boucles : for et while

### 4.1 La boucle for

En SAS, vous itérez sur les observations d'un dataset.
En Python, on itère sur n'importe quelle liste, intervalle ou structure."""),

code("""# Boucle sur une liste de codes devise
devises = ["EUR", "USD", "GBP", "CHF"]

for devise in devises:
    print(f"Devise : {devise}")"""),

code("""# range() : équivalent du do i = 1 to N en SAS
for i in range(1, 6):     # de 1 à 5 inclus
    print(f"Ligne {i}")"""),

code("""# Exemple concret : calculer un intérêt sur plusieurs mois
solde_initial = 10000
taux_mensuel  = 0.003   # 0.3% par mois

solde = solde_initial
for mois in range(1, 13):    # 12 mois
    interet = solde * taux_mensuel
    solde  += interet
    print(f"Mois {mois:02d} → Solde : {solde:,.2f} EUR")"""),

md("""### 4.2 La boucle while et break"""),

code("""# while : continuer tant qu'une condition est vraie
compteur = 0
while compteur < 5:
    print(f"Compteur : {compteur}")
    compteur += 1   # équivalent de compteur = compteur + 1

# break : sortir prématurément d'une boucle
print()
for i in range(100):
    if i == 3:
        print(f"Arrêt à i = {i}")
        break
    print(i)"""),

# ----- 5. Listes -----
md("""---
## 5. Les Listes

La liste est la structure de données la plus utilisée en Python.
Pensez-y comme une colonne SAS que vous pouvez manipuler en dehors d'un dataset."""),

code("""# Créer une liste
codes_contrat = ["0029862201102", "0029912218433", "0029922113324"]

# Accéder à un élément (index commence à 0 !)
print("Premier contrat :", codes_contrat[0])
print("Dernier contrat :", codes_contrat[-1])   # -1 = dernier

# Longueur
print("Nombre de contrats :", len(codes_contrat))"""),

code("""# Modifier une liste
soldes = [1200.0, 850.5, 0.0, 2300.75, 150.0]

# Ajouter un élément
soldes.append(999.99)
print("Après ajout :", soldes)

# Supprimer le dernier
soldes.pop()
print("Après suppression :", soldes)

# Trier
soldes.sort(reverse=True)   # du plus grand au plus petit
print("Trié :", soldes)"""),

code("""# Filtrer une liste (les soldes positifs)
soldes = [1200.0, -50.0, 0.0, 2300.75, -10.5, 150.0]

# Méthode classique avec boucle
soldes_positifs = []
for s in soldes:
    if s > 0:
        soldes_positifs.append(s)

print("Classique :", soldes_positifs)

# Méthode Python moderne : list comprehension (très utilisée !)
# Syntaxe : [expression for element in liste if condition]
soldes_positifs2 = [s for s in soldes if s > 0]
print("Comprehension :", soldes_positifs2)"""),

code("""# Exercice guidé : mapping de codes
# La table CTR a un champ COD_ECV_CTR avec des valeurs "1", "4", "6"
# Créons un mapping vers des libellés lisibles

codes = ["6", "4", "6", "1", "4", "6"]

# Mapper chaque code vers un libellé
mapping = {"1": "Ouvert", "4": "Clôturé", "6": "Résilié"}

libelles = [mapping.get(c, "Inconnu") for c in codes]
print("Codes   :", codes)
print("Libellés:", libelles)"""),

# ----- 6. Tuples -----
md("""---
## 6. Les Tuples

Un tuple est comme une liste, mais **immuable** (on ne peut pas le modifier).
Utile pour représenter des enregistrements fixes ou des paires clé-valeur."""),

code("""# Un client avec ses informations figées
client = ("JANSSENS", "Bart", "1980-01-25", "FR", "M")

# Décomposer (unpacking)
nom, prenom, date_naiss, langue, sexe = client

print(f"Nom    : {nom} {prenom}")
print(f"Naissance : {date_naiss}")
print(f"Langue : {langue} | Sexe : {sexe}")

# Un tuple ne peut pas être modifié :
# client[0] = "DUPONT"  → TypeError !"""),

code("""# Cas d'usage : retourner plusieurs valeurs depuis une fonction
def calculer_stats(valeurs):
    total  = sum(valeurs)
    moyenne = total / len(valeurs)
    minimum = min(valeurs)
    maximum = max(valeurs)
    return total, moyenne, minimum, maximum   # retourne un tuple

soldes = [1200.0, 850.5, 2300.75, 150.0, 500.0]
tot, moy, mn, mx = calculer_stats(soldes)

print(f"Total   : {tot:,.2f} EUR")
print(f"Moyenne : {moy:,.2f} EUR")
print(f"Min     : {mn:,.2f} EUR")
print(f"Max     : {mx:,.2f} EUR")"""),

# ----- 7. Dictionnaires -----
md("""---
## 7. Les Dictionnaires

Un dictionnaire = ensemble de paires clé → valeur.
Pensez-y comme un enregistrement SAS ou une ligne de table avec accès par nom de colonne."""),

code("""# Un contrat représenté comme dictionnaire
contrat = {
    "IDT_AC"      : 65500477817,
    "REF_CTR_INN" : "0025784077205",
    "DAT_OUV_CTR" : "2024-05-29",
    "COD_ECV_CTR" : "4",
    "COD_DEV"     : "EUR",
    "SLD_CTR"     : None,   # valeur manquante (. en SAS)
}

# Accéder à une valeur par sa clé
print("Référence :", contrat["REF_CTR_INN"])
print("Devise    :", contrat["COD_DEV"])
print("Solde     :", contrat["SLD_CTR"])

# Accès sécurisé avec .get() (évite une erreur si la clé n'existe pas)
print("Type      :", contrat.get("COD_TYP", "Non renseigné"))"""),

code("""# Parcourir un dictionnaire
client = {
    "nom"    : "JANSSENS",
    "prenom" : "Bart",
    "langue" : "FR",
    "sexe"   : "M",
}

# Boucle sur clés et valeurs
for cle, valeur in client.items():
    print(f"  {cle:10s} → {valeur}")"""),

code("""# Dictionnaire de mappings (très utilisé en analyse de données)
cod_typ_tie = {
    "1": "Personne physique",
    "2": "Personne morale",
}

cod_sta_fed = {
    "1": "Actif fedéré",
    "2": "Inactif",
    "3": "Prospect",
    "4": "Résilié",
}

# Utilisation
code_type = "1"
code_statut = "3"
print(f"Type : {cod_typ_tie.get(code_type, '?')}")
print(f"Statut : {cod_sta_fed.get(code_statut, '?')}")"""),

code("""# Dict comprehension : créer un dictionnaire depuis deux listes
colonnes = ["IDT_AC", "REF_CTR_INN", "DAT_OUV_CTR", "COD_DEV"]
valeurs  = [65500004701, "0029862201102", "2024-05-29", "EUR"]

ligne = {col: val for col, val in zip(colonnes, valeurs)}
print(ligne)"""),

# ----- 8. Fonctions -----
md("""---
## 8. Fonctions

En SAS, vous utilisez des macros. En Python, on écrit des **fonctions**.
Une bonne fonction fait **une seule chose**, est **documentée** et **testable**."""),

code("""# Définir une fonction simple
def formater_montant(montant, devise="EUR"):
    \"\"\"
    Formate un montant monétaire en chaîne lisible.

    Args:
        montant (float): Montant à formater.
        devise  (str)  : Code devise ISO (défaut : EUR).

    Returns:
        str: Montant formaté, ex: '1 250,75 EUR'
    \"\"\"
    if montant is None:
        return "N/A"
    return f"{montant:,.2f} {devise}".replace(",", " ").replace(".", ",")

# Appels
print(formater_montant(1250.75))
print(formater_montant(0))
print(formater_montant(None))
print(formater_montant(9999.99, "USD"))"""),

code("""# Fonction avec plusieurs paramètres et valeur de retour
def classifier_contrat(cod_ecv_ctr, dat_clo_ctr=None):
    \"\"\"
    Détermine le statut lisible d'un contrat Beobank.

    Args:
        cod_ecv_ctr (str): Code état du contrat.
        dat_clo_ctr (str): Date de clôture (optionnel).

    Returns:
        str: Libellé du statut.
    \"\"\"
    mapping = {
        "1": "Ouvert",
        "2": "En attente",
        "3": "Suspendu",
        "4": "Clôturé",
        "5": "En cours de résiliation",
        "6": "Résilié",
    }
    statut = mapping.get(cod_ecv_ctr, f"Code inconnu ({cod_ecv_ctr})")
    if dat_clo_ctr:
        return f"{statut} le {dat_clo_ctr}"
    return statut

print(classifier_contrat("4", "2025-12-10"))
print(classifier_contrat("6", "2025-02-05"))
print(classifier_contrat("1"))"""),

# ----- 9. Lambda -----
md("""---
## 9. Les Lambda expressions

Une lambda est une **fonction anonyme** en une seule ligne.
Très utilisée avec Pandas pour transformer des colonnes."""),

code("""# Syntaxe : lambda parametre : expression

# Fonction normale
def doubler(x):
    return x * 2

# Equivalent lambda
doubler_lambda = lambda x: x * 2

print(doubler(5))
print(doubler_lambda(5))

# Exemples avec des données bancaires
en_euros = lambda montant: f"{montant:.2f} EUR"
print(en_euros(1250.75))

# Lambda avec condition
categorie_age = lambda age: "Jeune" if age < 30 else ("Senior" if age >= 60 else "Adulte")
print(categorie_age(25))   # Jeune
print(categorie_age(45))   # Adulte
print(categorie_age(65))   # Senior"""),

code("""# Lambda avec sorted()
# Tri d'une liste de tuples (client, solde)
clients = [
    ("JANSSENS Bart", 1250.75),
    ("DUPONT Marie", 8900.0),
    ("MARTIN Paul", 350.50),
    ("LEROY Sophie", 4200.0),
]

# Trier par solde (2ème élément de chaque tuple)
clients_tries = sorted(clients, key=lambda c: c[1], reverse=True)

print("Clients par solde décroissant :")
for nom, solde in clients_tries:
    print(f"  {nom:20s} → {solde:,.2f} EUR")"""),

# ----- 10. Exercices -----
md("""---
## Exercices du Jour 1

### Exercice 1 — Nettoyage d'une liste de codes

La table CTR contient des codes état `COD_ECV_CTR` parfois mal renseignés.
Créez une fonction qui nettoie et valide ces codes."""),

code("""# Données brutes (comme dans un extract CSV)
codes_bruts = ["4", " 6 ", "1", "", None, "4", "99", "  6", "4"]

# TODO : complétez la fonction ci-dessous
def nettoyer_codes(liste_codes, codes_valides=("1","2","3","4","5","6")):
    \"\"\"
    Nettoie une liste de codes : supprime espaces, filtre les valides.

    Args:
        liste_codes   : liste de codes bruts
        codes_valides : tuple des codes acceptés

    Returns:
        list : liste de codes propres (None pour les invalides)
    \"\"\"
    resultats = []
    for code in liste_codes:
        if code is None or str(code).strip() == "":
            resultats.append(None)
        elif str(code).strip() in codes_valides:
            resultats.append(str(code).strip())
        else:
            resultats.append(None)
    return resultats

codes_propres = nettoyer_codes(codes_bruts)
print("Codes bruts  :", codes_bruts)
print("Codes propres:", codes_propres)"""),

md("""### Exercice 2 — Dictionnaire de résumé client

À partir des données d'un client, construisez un dictionnaire de résumé."""),

code("""# Données d'entrée (une ligne de TIE + TIE_ADR)
idt_pi      = 655010249
num_tie     = "2500003178544"
nom         = "JANSSENS"
prenom      = "BART"
dat_nai     = "1980-01-25"
cod_lng     = "FR"
cod_sex     = "M"
nom_vil     = "BRUSSEL"
cod_pay     = "BE"

# TODO : créez la fonction et le dictionnaire résumé
def creer_fiche_client(idt_pi, nom, prenom, dat_nai, cod_lng, cod_sex, ville, pays):
    \"\"\"Construit une fiche client enrichie avec libellés lisibles.\"\"\"
    langues = {"FR": "Français", "NL": "Néerlandais", "DE": "Allemand", "EN": "Anglais"}
    civilites = {"M": "Monsieur", "F": "Madame"}

    return {
        "id"        : idt_pi,
        "civilite"  : civilites.get(cod_sex, ""),
        "nom_complet": f"{prenom.capitalize()} {nom.capitalize()}",
        "naissance" : dat_nai,
        "langue"    : langues.get(cod_lng, cod_lng),
        "localite"  : f"{ville}, {pays}",
    }

fiche = creer_fiche_client(idt_pi, nom, prenom, dat_nai, cod_lng, cod_sex, nom_vil, cod_pay)
for k, v in fiche.items():
    print(f"  {k:12s}: {v}")"""),

md("""### Exercice 3 — De SAS vers Python

Voici une logique SAS. Réécrivez-la en Python.

```sas
data contrats_actifs;
    set CTR;
    if COD_ECV_CTR in ('1','2','3') then statut = 'Actif';
    else if COD_ECV_CTR in ('4','5','6') then statut = 'Inactif';
    else statut = 'Inconnu';

    if statut = 'Actif' then output;
run;
```"""),

code("""# Données simulées (comme si on avait lu la table CTR)
contrats = [
    {"REF_CTR_INN": "0029862201102", "COD_ECV_CTR": "6"},
    {"REF_CTR_INN": "0029912218433", "COD_ECV_CTR": "6"},
    {"REF_CTR_INN": "0029922113324", "COD_ECV_CTR": "4"},
    {"REF_CTR_INN": "0029872222935", "COD_ECV_CTR": "4"},
    {"REF_CTR_INN": "0029882034602", "COD_ECV_CTR": "1"},
    {"REF_CTR_INN": "0029991234567", "COD_ECV_CTR": "2"},
]

def classer_statut(cod_ecv_ctr):
    if cod_ecv_ctr in ("1", "2", "3"):
        return "Actif"
    elif cod_ecv_ctr in ("4", "5", "6"):
        return "Inactif"
    return "Inconnu"

# Ajouter le statut à chaque contrat et filtrer les actifs
contrats_actifs = []
for ctr in contrats:
    statut = classer_statut(ctr["COD_ECV_CTR"])
    if statut == "Actif":
        ctr["STATUT"] = statut
        contrats_actifs.append(ctr)

print(f"Contrats actifs : {len(contrats_actifs)} / {len(contrats)}")
for c in contrats_actifs:
    print(f"  {c['REF_CTR_INN']} → {c['STATUT']}")"""),

md("""---
## Résumé du Jour 1

| Ce que vous savez faire | Equivalent SAS |
|-------------------------|----------------|
| `print(f"...")` | `put variable;` |
| `if / elif / else` | `if ... then ... else ...` |
| `for item in liste:` | `do over array;` |
| `[x for x in liste if ...]` | `where` dans un dataset |
| `def ma_fonction(params):` | `%macro ma_macro(...);` |
| `lambda x: x * 2` | fonction anonyme en ligne |
| `dict["cle"]` | accès à une variable par nom |

**Demain : on charge les vraies tables Beobank avec Pandas !**"""),

] # fin j1


# =============================================================
# JOUR 2 — Fichiers, Pandas et Flux de Données
# =============================================================

j2 = [

md("""# Jour 2 — Fichiers, Pandas et Flux de Données
## Formation Python Beobank · 19 novembre 2026

**Prérequis : avoir suivi le Jour 1 ou connaître les bases Python.**

### Objectifs de la journée
- Lire et écrire des fichiers CSV et JSON
- Charger les tables Beobank dans Pandas
- Explorer, filtrer, transformer des DataFrames
- Regrouper et agréger des données
- Exporter les résultats
- Comprendre le flux Pandas ↔ Vertica"""),

# ----- Section 1 : Fichiers -----
md("""---
## 1. Lecture et écriture de fichiers

### 1.1 Ouvrir un fichier texte avec `open()`

En SAS : `infile 'chemin' dlm=';';`
En Python : `open('chemin', mode)`"""),

code("""# Écrire un fichier texte simple
with open("test_beobank.txt", "w", encoding="utf-8") as f:
    f.write("Formation Python Beobank\\n")
    f.write("Jour 2 — Fichiers et Pandas\\n")
    f.write("Date : 19 novembre 2026\\n")

print("Fichier écrit.")

# Lire le fichier
with open("test_beobank.txt", "r", encoding="utf-8") as f:
    contenu = f.read()

print(contenu)"""),

md("""### 1.2 pathlib : manipuler les chemins de façon propre

`pathlib` est la façon moderne de gérer les chemins de fichiers en Python."""),

code("""from pathlib import Path

# Dossier des données Beobank
dossier_data = Path("../Orsys")

# Lister les fichiers CSV
for fichier in dossier_data.glob("*.csv"):
    taille = fichier.stat().st_size / 1024
    print(f"{fichier.name:25s}  {taille:.1f} Ko")"""),

code("""# Construire un chemin de façon portable (Windows et Linux)
from pathlib import Path

data_dir = Path("../Orsys")

chemin_ctr = data_dir / "CTR.csv"
print("Chemin CTR    :", chemin_ctr)
print("Existe ?      :", chemin_ctr.exists())
print("Extension     :", chemin_ctr.suffix)
print("Nom sans ext  :", chemin_ctr.stem)"""),

# ----- Section 1.3 : CSV natif -----
md("""### 1.3 Lire un CSV avec le module `csv`

Utile pour comprendre la mécanique. En pratique, on utilisera Pandas."""),

code("""import csv
from pathlib import Path

chemin = Path("../Orsys/TIE.csv")

with open(chemin, encoding="utf-8", newline="") as f:
    lecteur = csv.DictReader(f, delimiter=";")   # séparateur ; comme dans les tables Beobank

    lignes = list(lecteur)

print(f"Nombre de lignes : {len(lignes)}")
print("\\nPremière ligne :")
for col, val in lignes[0].items():
    print(f"  {col:20s} : {val}")"""),

# ----- Section 2 : Pandas -----
md("""---
## 2. Introduction à Pandas

Pandas est **la** bibliothèque Python pour analyser des données tabulaires.
Si SAS a les datasets, Python a les **DataFrames**.

| SAS | Pandas |
|-----|--------|
| `data` set | `DataFrame` |
| `proc print` | `df.head()` / `print(df)` |
| `proc contents` | `df.info()` / `df.dtypes` |
| `proc means` | `df.describe()` |
| `where ...` | `df[df['col'] == valeur]` |
| `keep` / `drop` | `df[['col1','col2']]` / `df.drop(...)` |
| `proc sort` | `df.sort_values(...)` |
| `proc freq` | `df['col'].value_counts()` |"""),

code("""import pandas as pd
from pathlib import Path

DATA = Path("../Orsys")

# Lecture de la table CTR (Contrats)
# sep=';'         : séparateur point-virgule
# na_values='.'   : le point (.) est la valeur manquante SAS → on le convertit en NaN
ctr = pd.read_csv(DATA / "CTR.csv", sep=";", na_values=".", encoding="utf-8")

print("=== Table CTR — Contrats ===")
print(f"Dimensions : {ctr.shape[0]} lignes × {ctr.shape[1]} colonnes")
print("\\nColonnes :")
print(ctr.dtypes)"""),

code("""# Les premières lignes — équivalent de proc print (obs=5)
ctr.head()"""),

code("""# Résumé statistique — équivalent de proc means
ctr.describe()"""),

code("""# Valeurs manquantes par colonne
print("Valeurs manquantes par colonne :")
manquants = ctr.isnull().sum()
pct       = (manquants / len(ctr) * 100).round(1)

resumé = pd.DataFrame({"Manquants": manquants, "Pct %": pct})
resumé[resumé["Manquants"] > 0]"""),

# ----- Chargement de toutes les tables -----
md("""### 2.1 Chargement de toutes les tables Beobank"""),

code("""import pandas as pd
from pathlib import Path

DATA = Path("../Orsys")

# Paramètres communs
params = dict(sep=";", na_values=".", encoding="utf-8")

ctr         = pd.read_csv(DATA / "CTR.csv",     **params)
tie         = pd.read_csv(DATA / "TIE.csv",     **params)
tie_adr     = pd.read_csv(DATA / "TIE_ADR.csv", **params)
tie_x_ctr   = pd.read_csv(DATA / "TIE_X_CTR.csv", **params)
txn_x_ctr   = pd.read_csv(DATA / "TXN_X_CTR.csv", **params)

# Résumé des tables chargées
tables = {
    "CTR (Contrats)"    : ctr,
    "TIE (Clients)"     : tie,
    "TIE_ADR (Adresses)": tie_adr,
    "TIE_X_CTR (Liens)" : tie_x_ctr,
    "TXN (Transactions)": txn_x_ctr,
}

print(f"{'Table':25s} {'Lignes':>8} {'Colonnes':>10}")
print("-" * 45)
for nom, df in tables.items():
    print(f"{nom:25s} {df.shape[0]:>8,} {df.shape[1]:>10}")"""),

# ----- Section 3 : Explorer -----
md("""---
## 3. Explorer un DataFrame

### 3.1 La table TIE — Clients"""),

code("""# Aperçu de la table TIE (Tiers/Clients)
tie.head(5)"""),

code("""# Fréquences — équivalent proc freq
print("=== COD_TYP_TIE (Type de tiers) ===")
print(tie["COD_TYP_TIE"].value_counts().to_frame("Effectif"))

print("\\n=== COD_STA_FED (Statut fédéral) ===")
print(tie["COD_STA_FED"].value_counts().to_frame("Effectif"))

print("\\n=== COD_LNG_CTR (Langue) ===")
print(tie["COD_LNG_CTR"].value_counts(dropna=False).to_frame("Effectif"))

print("\\n=== COD_SEX (Sexe) ===")
print(tie["COD_SEX"].value_counts(dropna=False).to_frame("Effectif"))"""),

# ----- Section 4 : Filtrage et sélection -----
md("""---
## 4. Filtrage et sélection de colonnes

### 4.1 Sélectionner des colonnes"""),

code("""# Sélectionner une colonne → Series
langues = tie["COD_LNG_CTR"]
print(type(langues))
print(langues.head())

# Sélectionner plusieurs colonnes → DataFrame
colonnes_clés = ["IDT_PI", "NUM_TIE", "COD_TYP_TIE", "DAT_NAI", "COD_SEX"]
tie_reduit = tie[colonnes_clés]
tie_reduit.head()"""),

md("""### 4.2 Filtrer les lignes"""),

code("""# Filtrer les personnes physiques (COD_TYP_TIE = '1')
# Equivalent SAS : where COD_TYP_TIE = '1';

personnes_physiques = tie[tie["COD_TYP_TIE"] == "1"]
print(f"Personnes physiques : {len(personnes_physiques)}")
print(f"Personnes morales   : {len(tie[tie['COD_TYP_TIE'] == '2'])}")"""),

code("""# Filtres multiples avec & (et) et | (ou)
# Equivalent SAS : where COD_TYP_TIE = '1' and COD_SEX = 'M';

hommes_physiques = tie[
    (tie["COD_TYP_TIE"] == "1") &
    (tie["COD_SEX"] == "M")
]
print(f"Hommes personnes physiques : {len(hommes_physiques)}")

# Filtrer avec isin() — équivalent de in ('1','2') en SAS
statuts_actifs = tie[tie["COD_STA_FED"].isin(["1", "2"])]
print(f"Statuts actifs (1 ou 2) : {len(statuts_actifs)}")"""),

code("""# Filtrer les valeurs non nulles
# Equivalent SAS : where DAT_NAI ne .;

clients_avec_naissance = tie[tie["DAT_NAI"].notna()]
print(f"Clients avec date de naissance : {len(clients_avec_naissance)} / {len(tie)}")"""),

# ----- Section 5 : Colonnes calculées -----
md("""---
## 5. Créer des colonnes calculées

Equivalent SAS : `variable = expression;` dans un step DATA"""),

code("""# Ajouter un libellé lisible pour COD_TYP_TIE
mapping_type = {"1": "Personne physique", "2": "Personne morale"}
tie["LIB_TYP_TIE"] = tie["COD_TYP_TIE"].map(mapping_type)

# Ajouter un libellé pour COD_STA_FED
mapping_statut = {"1": "Actif fedéré", "2": "Inactif", "3": "Prospect", "4": "Résilié"}
tie["LIB_STA_FED"] = tie["COD_STA_FED"].map(mapping_statut).fillna("Autre")

# Vérifier
tie[["IDT_PI", "COD_TYP_TIE", "LIB_TYP_TIE", "COD_STA_FED", "LIB_STA_FED"]].head(8)"""),

code("""# Calcul de l'âge à partir de DAT_NAI
import pandas as pd

# Convertir la colonne date (elle est au format YYYY-MM-DD ici)
tie["DAT_NAI_DT"] = pd.to_datetime(tie["DAT_NAI"], errors="coerce")

aujourd_hui = pd.Timestamp.today()

# Calculer l'âge en années
tie["AGE"] = ((aujourd_hui - tie["DAT_NAI_DT"]).dt.days / 365.25).astype("Int64")

print("Age minimum :", tie["AGE"].min())
print("Age maximum :", tie["AGE"].max())
print("Age moyen   :", round(tie["AGE"].mean(), 1))

tie[["IDT_PI", "DAT_NAI", "AGE"]].dropna().head(8)"""),

# ----- Section 6 : Tri et agrégation -----
md("""---
## 6. Tri, regroupement et agrégation

### 6.1 Trier — équivalent proc sort"""),

code("""# Trier par date de naissance (plus jeune en premier)
tie_trie = tie[["IDT_PI", "DAT_NAI", "AGE", "COD_SEX"]].dropna()
tie_trie = tie_trie.sort_values("AGE", ascending=True)
tie_trie.head(5)"""),

md("""### 6.2 Grouper et agréger — équivalent proc means / proc summary"""),

code("""# Compter les clients par type et sexe
resume_type = (
    tie
    .groupby(["LIB_TYP_TIE", "COD_SEX"])
    .size()
    .reset_index(name="Effectif")
    .sort_values("Effectif", ascending=False)
)
print(resume_type.to_string(index=False))"""),

code("""# Agréger les transactions par contrat
# Nombre de transactions et labels uniques par contrat
resume_txn = (
    txn_x_ctr
    .groupby("IDT_AC")
    .agg(
        nb_transactions = ("NUM_ORD_MVT_CPB", "count"),
        nb_folios       = ("NUM_FOL_XTR", "nunique"),
        premiere_date   = ("DAT_CRE_MVT_CPB", "min"),
        derniere_date   = ("DAT_CRE_MVT_CPB", "max"),
    )
    .reset_index()
    .sort_values("nb_transactions", ascending=False)
)

print(f"Contrats avec transactions : {len(resume_txn)}")
resume_txn.head(10)"""),

# ----- Section 7 : Export -----
md("""---
## 7. Exporter les résultats

### 7.1 Export en CSV"""),

code("""# Exporter un DataFrame en CSV
# Equivalent SAS : proc export data=... outfile='...' dbms=csv; run;

resume_txn.to_csv("resume_transactions.csv",
                  sep=";",           # même séparateur que les sources
                  index=False,       # ne pas exporter l'index numérique
                  encoding="utf-8")

print("Fichier CSV exporté : resume_transactions.csv")"""),

md("""### 7.2 Export en JSON"""),

code("""# Exporter en JSON (utile pour les APIs et échanges inter-systèmes)
# Prendre les 10 premiers clients avec leurs infos

clients_export = tie[["IDT_PI", "NUM_TIE", "COD_TYP_TIE", "DAT_NAI", "COD_LNG_CTR"]].head(10)

# orient='records' = une liste de dicts (le format le plus courant)
clients_export.to_json("clients_sample.json",
                       orient="records",
                       indent=2,
                       force_ascii=False)

print("Fichier JSON exporté : clients_sample.json")

# Vérifier en relisant
import json
with open("clients_sample.json", encoding="utf-8") as f:
    data = json.load(f)
print(f"\\n{len(data)} clients dans le JSON")
print("Premier enregistrement :", data[0])"""),

# ----- Section 8 : Vertica (simulation) -----
md("""---
## 8. Flux Pandas ↔ Vertica

### 8.1 Principe général

Dans votre environnement Beobank, vous accéderez à Vertica via un driver Python.
Le flux habituel est le suivant :

```
Fichier CSV/JSON
      ↓  pd.read_csv()
  DataFrame Pandas
      ↓  to_sql()     ← injection dans Vertica
    Vertica DB
      ↓  pd.read_sql() ← extraction depuis Vertica
  DataFrame Pandas
      ↓  to_csv() / to_json()
  Fichier de sortie
```

### 8.2 Connexion type Vertica (à adapter selon votre environnement)

```python
import vertica_python   # ou sqlalchemy + vertica_python

conn_info = {
    'host'     : 'vertica-beobank.intranet',
    'port'     : 5433,
    'user'     : 'VOTRE_USERID',
    'password' : 'VOTRE_MOT_DE_PASSE',
    'database' : 'beobank_db',
}

with vertica_python.connect(**conn_info) as conn:
    df = pd.read_sql("SELECT * FROM SIDU.CTR LIMIT 100", conn)
```"""),

md("""### 8.3 Simulation avec SQLite (exercice sans connexion Vertica)

SQLite permet de simuler une base relationnelle localement pour pratiquer."""),

code("""import sqlite3
import pandas as pd
from pathlib import Path

DATA = Path("../Orsys")
params = dict(sep=";", na_values=".", encoding="utf-8")

# Charger les tables
ctr       = pd.read_csv(DATA / "CTR.csv",     **params)
tie       = pd.read_csv(DATA / "TIE.csv",     **params)
txn_x_ctr = pd.read_csv(DATA / "TXN_X_CTR.csv", **params)

# Créer une base en mémoire
conn = sqlite3.connect(":memory:")

# Injecter les DataFrames comme des tables SQL
ctr.to_sql("CTR", conn, if_exists="replace", index=False)
tie.to_sql("TIE", conn, if_exists="replace", index=False)
txn_x_ctr.to_sql("TXN", conn, if_exists="replace", index=False)

print("Tables injectées dans SQLite :")
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
print(tables["name"].tolist())"""),

code("""# Requête SQL : nombre de contrats par statut
sql = '''
SELECT
    COD_ECV_CTR,
    COUNT(*) AS nb_contrats
FROM CTR
GROUP BY COD_ECV_CTR
ORDER BY nb_contrats DESC
'''

result = pd.read_sql(sql, conn)
print("Contrats par statut :")
print(result.to_string(index=False))"""),

code("""# Requête SQL : transactions récentes
sql_txn = '''
SELECT
    IDT_AC,
    COUNT(*) AS nb_txn,
    MIN(DAT_CRE_MVT_CPB) AS premiere_txn,
    MAX(DAT_CRE_MVT_CPB) AS derniere_txn
FROM TXN
GROUP BY IDT_AC
ORDER BY nb_txn DESC
LIMIT 10
'''

top_comptes = pd.read_sql(sql_txn, conn)
print("Top 10 comptes par volume de transactions :")
top_comptes"""),

# ----- Exercices -----
md("""---
## Exercices du Jour 2

### Exercice 1 — Qualité de données sur la table CTR"""),

code("""import pandas as pd
from pathlib import Path

DATA = Path("../Orsys")
ctr = pd.read_csv(DATA / "CTR.csv", sep=";", na_values=".", encoding="utf-8")

# TODO : répondez aux questions suivantes

# 1. Combien de contrats n'ont pas de date de clôture (DAT_CLO_CTR) ?
sans_cloture = ctr["DAT_CLO_CTR"].isna().sum()
print(f"1. Contrats sans date de clôture : {sans_cloture}")

# 2. Quelle est la distribution des codes devise (COD_DEV) ?
print("\\n2. Distribution des devises :")
print(ctr["COD_DEV"].value_counts(dropna=False))

# 3. Combien de contrats ont un solde (SLD_CTR) renseigné ?
avec_solde = ctr["SLD_CTR"].notna().sum()
print(f"\\n3. Contrats avec solde renseigné : {avec_solde} / {len(ctr)}")

# 4. Quels sont les codes état présents (COD_ECV_CTR) ?
print("\\n4. Codes état :")
print(ctr["COD_ECV_CTR"].value_counts())"""),

md("""### Exercice 2 — Pipeline complet : charger → enrichir → exporter"""),

code("""import pandas as pd
from pathlib import Path

DATA = Path("../Orsys")
params = dict(sep=";", na_values=".", encoding="utf-8")

# Charger
ctr = pd.read_csv(DATA / "CTR.csv",     **params)
tie = pd.read_csv(DATA / "TIE.csv",     **params)
tie_adr = pd.read_csv(DATA / "TIE_ADR.csv", **params)
tie_x_ctr = pd.read_csv(DATA / "TIE_X_CTR.csv", **params)

# Enrichir CTR avec le libellé du statut
mapping_ecv = {
    "1": "Ouvert", "2": "En attente", "3": "Suspendu",
    "4": "Clôturé", "5": "En cours résiliation", "6": "Résilié"
}
ctr["LIB_ECV"] = ctr["COD_ECV_CTR"].map(mapping_ecv).fillna("Inconnu")

# Convertir les dates
ctr["DAT_OUV_CTR_DT"] = pd.to_datetime(ctr["DAT_OUV_CTR"], errors="coerce")

# Filtrer : contrats ouverts depuis 2024
ctr_2024 = ctr[ctr["DAT_OUV_CTR_DT"].dt.year >= 2024]
print(f"Contrats ouverts depuis 2024 : {len(ctr_2024)}")

# Distribution par statut
print("\\nRépartition par statut :")
print(ctr_2024["LIB_ECV"].value_counts().to_string())

# Exporter
ctr_2024.to_csv("contrats_2024.csv", sep=";", index=False, encoding="utf-8")
print("\\nExporté : contrats_2024.csv")"""),

md("""---
## Résumé du Jour 2

| Ce que vous savez faire | Equivalent SAS |
|-------------------------|----------------|
| `pd.read_csv(...)` | `proc import` |
| `df.head()` | `proc print (obs=5)` |
| `df.info()` / `df.dtypes` | `proc contents` |
| `df.describe()` | `proc means` |
| `df[df['col'] == val]` | `where col = val;` |
| `df['col'].value_counts()` | `proc freq` |
| `df.groupby().agg()` | `proc summary` |
| `df.to_csv(...)` | `proc export` |
| `pd.read_sql(sql, conn)` | `proc sql` avec connexion |

**Demain : Vertica SQL avancé, time series, jointures et visualisation !**"""),

] # fin j2


# =============================================================
# JOUR 3 — SQL Vertica, Time Series, Pandas Avancé, Visualisation
# =============================================================

j3 = [

md("""# Jour 3 — Vertica SQL, Time Series, Pandas Avancé & Visualisation
## Formation Python Beobank · 20 novembre 2026

### Objectifs de la journée
- Maîtriser les fonctions analytiques Vertica (CTEs, OVER, LAG/LEAD)
- Joindre les 5 tables Beobank avec Pandas
- Traiter les dates et séries temporelles
- Visualiser les résultats avec Matplotlib
- Réaliser le mini-projet de bout en bout"""),

# ----- Setup -----
code("""# Cellule de setup — exécuter en premier
import pandas as pd
import numpy as np
import sqlite3
from pathlib import Path

DATA = Path("../Orsys")
params = dict(sep=";", na_values=".", encoding="utf-8")

# Chargement des 5 tables
ctr       = pd.read_csv(DATA / "CTR.csv",       **params)
tie       = pd.read_csv(DATA / "TIE.csv",       **params)
tie_adr   = pd.read_csv(DATA / "TIE_ADR.csv",   **params)
tie_x_ctr = pd.read_csv(DATA / "TIE_X_CTR.csv", **params)
txn       = pd.read_csv(DATA / "TXN_X_CTR.csv", **params)

print("Tables chargées :")
for nom, df in [("ctr",ctr),("tie",tie),("tie_adr",tie_adr),("tie_x_ctr",tie_x_ctr),("txn",txn)]:
    print(f"  {nom:12s}: {df.shape[0]:>5} lignes × {df.shape[1]} colonnes")"""),

# ----- Section 1 : Vertica SQL -----
md("""---
## 1. Vertica SQL pour analystes

### 1.1 CTEs — Common Table Expressions

Les CTEs rendent les requêtes complexes lisibles. En SAS, l'équivalent est d'enchaîner plusieurs step DATA ou proc sql.

**Syntaxe Vertica :**
```sql
WITH
    cte1 AS (
        SELECT ...
        FROM SIDU.CTR
        WHERE ...
    ),
    cte2 AS (
        SELECT ...
        FROM cte1
        JOIN SIDU.TIE ON ...
    )
SELECT * FROM cte2;
```"""),

code("""# Simulation Vertica avec SQLite — même logique SQL
conn = sqlite3.connect(":memory:")

# Injection des tables dans SQLite
ctr.to_sql("CTR", conn, if_exists="replace", index=False)
tie.to_sql("TIE", conn, if_exists="replace", index=False)
tie_adr.to_sql("TIE_ADR", conn, if_exists="replace", index=False)
tie_x_ctr.to_sql("TIE_X_CTR", conn, if_exists="replace", index=False)
txn.to_sql("TXN", conn, if_exists="replace", index=False)

# Requête avec CTE
sql_cte = '''
WITH
    contrats_actifs AS (
        SELECT IDT_AC, REF_CTR_INN, DAT_OUV_CTR, COD_ECV_CTR
        FROM CTR
        WHERE COD_ECV_CTR IN ('1', '2', '3')
    ),
    liens AS (
        SELECT c.IDT_AC, c.REF_CTR_INN, c.DAT_OUV_CTR,
               t.NUM_TIE
        FROM contrats_actifs c
        JOIN TIE_X_CTR t ON c.IDT_AC = t.IDT_AC
    )
SELECT *
FROM liens
LIMIT 10
'''

result_cte = pd.read_sql(sql_cte, conn)
print(f"CTE → {len(result_cte)} lignes")
result_cte"""),

# ----- Fonctions analytiques -----
md("""### 1.2 Fonctions analytiques — OVER / PARTITION BY

Les fonctions analytiques calculent une valeur **pour chaque ligne** en fonction d'un groupe.
Très utile pour les comparaisons intra-groupe, les rangs, les valeurs précédentes/suivantes.

| Fonction Vertica | Equivalent Pandas |
|-----------------|-------------------|
| `COUNT(*) OVER (PARTITION BY col)` | `df.groupby('col')['x'].transform('count')` |
| `SUM(val) OVER (PARTITION BY col)` | `df.groupby('col')['val'].transform('sum')` |
| `LAG(val, 1) OVER (ORDER BY date)` | `df.sort_values('date')['val'].shift(1)` |
| `LEAD(val, 1) OVER (ORDER BY date)` | `df.sort_values('date')['val'].shift(-1)` |
| `ROW_NUMBER() OVER (...)` | `df.groupby(...).cumcount() + 1` |"""),

code("""# Exemple SQL avec OVER (simulation SQLite)
# SQLite supporte window functions depuis la version 3.25 (2018)

sql_window = '''
SELECT
    IDT_AC,
    DAT_CRE_MVT_CPB,
    NUM_FOL_XTR,
    COUNT(*) OVER (PARTITION BY IDT_AC) AS total_txn_compte,
    ROW_NUMBER() OVER (
        PARTITION BY IDT_AC
        ORDER BY DAT_CRE_MVT_CPB
    ) AS num_ordre
FROM TXN
ORDER BY IDT_AC, DAT_CRE_MVT_CPB
LIMIT 20
'''

result_window = pd.read_sql(sql_window, conn)
result_window"""),

code("""# Même résultat avec Pandas (plus flexible pour la suite du traitement)
txn_sorted = txn.sort_values(["IDT_AC", "DAT_CRE_MVT_CPB"])

# Nombre total de transactions par compte (OVER PARTITION BY)
txn_sorted["total_txn_compte"] = txn_sorted.groupby("IDT_AC")["NUM_ORD_MVT_CPB"].transform("count")

# Numéro d'ordre chronologique (ROW_NUMBER OVER PARTITION BY ... ORDER BY ...)
txn_sorted["num_ordre"] = txn_sorted.groupby("IDT_AC").cumcount() + 1

txn_sorted[["IDT_AC", "DAT_CRE_MVT_CPB", "total_txn_compte", "num_ordre"]].head(15)"""),

md("""### 1.3 LAG / LEAD — navigation dans le temps

`LAG` : valeur de la ligne précédente (mois N-1)
`LEAD` : valeur de la ligne suivante (mois N+1)

**Vertica SQL :**
```sql
SELECT
    IDT_AC,
    DAT_CRE_MVT_CPB,
    LAG(DAT_CRE_MVT_CPB, 1) OVER (
        PARTITION BY IDT_AC
        ORDER BY DAT_CRE_MVT_CPB
    ) AS date_txn_precedente
FROM SIDU.TXN_X_CTR;
```"""),

code("""# Pandas : LAG avec shift(1)
txn_lag = txn.sort_values(["IDT_AC", "DAT_CRE_MVT_CPB"]).copy()
txn_lag["DAT_CRE_MVT_CPB"] = pd.to_datetime(txn_lag["DAT_CRE_MVT_CPB"], errors="coerce")

# LAG(1) par compte = date de la transaction précédente du même compte
txn_lag["date_precedente"] = txn_lag.groupby("IDT_AC")["DAT_CRE_MVT_CPB"].shift(1)

# Calcul de l'écart en jours entre deux transactions consécutives
txn_lag["ecart_jours"] = (txn_lag["DAT_CRE_MVT_CPB"] - txn_lag["date_precedente"]).dt.days

# Statistiques sur l'écart inter-transactions
print("Ecart moyen entre transactions (jours) :", round(txn_lag["ecart_jours"].mean(), 1))
print("Ecart médian                            :", round(txn_lag["ecart_jours"].median(), 1))

txn_lag[["IDT_AC", "DAT_CRE_MVT_CPB", "date_precedente", "ecart_jours"]].dropna().head(10)"""),

# ----- Section 2 : Jointures -----
md("""---
## 2. Jointures entre les 5 tables Beobank

### Schéma des relations

```
TIE (100 clients)
 │  IDT_PI
 │       ↓
TIE_ADR (100 adresses)   ── IDT_PI ──> TIE_X_CTR (200 liens)
                                              │ IDT_AC
                                              ↓
                                         CTR (200 contrats)
                                              │ IDT_AC
                                              ↓
                                         TXN (1260 transactions)
```"""),

code("""# Jointure 1 : TIE + TIE_ADR (enrichissement client)
# Equivalent SAS : proc sql; create table ... as select * from TIE t join TIE_ADR a on t.IDT_PI = a.IDT_PI;

clients = tie.merge(
    tie_adr[["IDT_PI", "NOM_TIE", "PRN", "NOM_VIL", "COD_PST", "COD_PAY_ISO", "ADR_EMA"]],
    on="IDT_PI",
    how="left"
)

print(f"Clients enrichis : {len(clients)} lignes")
clients[["IDT_PI", "COD_TYP_TIE", "COD_SEX", "NOM_TIE", "PRN", "NOM_VIL"]].head(6)"""),

code("""# Jointure 2 : Clients → Contrats (via la table de lien TIE_X_CTR)
clients_contrats = clients.merge(
    tie_x_ctr[["IDT_PI", "IDT_AC", "FLG_PRE_TTL", "COD_ROL_TTL"]],
    on="IDT_PI",
    how="left"
).merge(
    ctr[["IDT_AC", "REF_CTR_INN", "DAT_OUV_CTR", "COD_ECV_CTR", "COD_DEV"]],
    on="IDT_AC",
    how="left"
)

print(f"Clients-Contrats : {len(clients_contrats)} lignes")
print(f"Colonnes         : {clients_contrats.shape[1]}")

# Afficher un extrait
cols_affich = ["NOM_TIE", "PRN", "REF_CTR_INN", "DAT_OUV_CTR", "COD_ECV_CTR", "COD_DEV"]
clients_contrats[cols_affich].head(8)"""),

code("""# Vue complète : clients → contrats → transactions
vue_complete = clients_contrats.merge(
    txn[["IDT_AC", "DAT_CRE_MVT_CPB", "NUM_FOL_XTR", "LIB_OPE_INL_1"]],
    on="IDT_AC",
    how="left"
)

print(f"Vue complète : {len(vue_complete):,} lignes × {vue_complete.shape[1]} colonnes")
vue_complete[["NOM_TIE", "PRN", "REF_CTR_INN", "DAT_CRE_MVT_CPB", "LIB_OPE_INL_1"]].head(10)"""),

# ----- Section 3 : Dates -----
md("""---
## 3. Gestion des dates et Time Series

### 3.1 Conversion des colonnes date

Les tables Beobank utilisent deux formats :
- `YYYY-MM-DD` dans CTR, TIE, TXN
- `DDMONYYYY` (format SAS : `24NOV2025`) dans TIE_ADR"""),

code("""import pandas as pd

# Format standard : YYYY-MM-DD
ctr["DAT_OUV_CTR_DT"] = pd.to_datetime(ctr["DAT_OUV_CTR"], errors="coerce")
ctr["DAT_CLO_CTR_DT"] = pd.to_datetime(ctr["DAT_CLO_CTR"], errors="coerce")
ctr["DAT_ECV_CTR_DT"] = pd.to_datetime(ctr["DAT_ECV_CTR"], errors="coerce")

print("Dates CTR converties :")
ctr[["DAT_OUV_CTR", "DAT_OUV_CTR_DT", "DAT_CLO_CTR", "DAT_CLO_CTR_DT"]].head(4)"""),

code("""# Format SAS : DDMONYYYY (ex: 24NOV2025) dans TIE_ADR
# Pandas peut le parser avec format='%d%b%Y' et locale anglaise (NOV = mois anglais)

# Remplacer les abrév. françaises si besoin, puis parser
mois_fr_to_en = {
    "JAN":"JAN","FEV":"FEB","MAR":"MAR","AVR":"APR","MAI":"MAY","JUI":"JUN",
    "JUL":"JUL","AOU":"AUG","SEP":"SEP","OCT":"OCT","NOV":"NOV","DEC":"DEC"
}

def parse_date_sas(s):
    # Parse une date au format SAS DDMONYYYY (ex: 24NOV2025)
    if pd.isna(s) or str(s).strip() == "":
        return pd.NaT
    s = str(s).strip().upper()
    for fr, en in mois_fr_to_en.items():
        s = s.replace(fr, en)
    try:
        return pd.to_datetime(s, format="%d%b%Y")
    except Exception:
        return pd.NaT

tie_adr["DAT_MAJ_ADR_DT"] = tie_adr["DAT_MAJ_ADR"].apply(parse_date_sas)

print("Exemples de conversion :")
tie_adr[["DAT_MAJ_ADR", "DAT_MAJ_ADR_DT"]].dropna().head(5)"""),

# ----- Calculs sur dates -----
md("""### 3.2 Calculs sur les dates

Equivalents Vertica SQL :
- `DATEDIFF('day', date1, date2)` → `(date2 - date1).dt.days`
- `ADD_MONTHS(date, n)` → `date + pd.DateOffset(months=n)`
- `DATE_TRUNC('month', date)` → `date.dt.to_period('M').dt.to_timestamp()`"""),

code("""# Calcul de la durée d'un contrat (en jours)
ctr["DAT_OUV_CTR_DT"] = pd.to_datetime(ctr["DAT_OUV_CTR"], errors="coerce")
ctr["DAT_CLO_CTR_DT"] = pd.to_datetime(ctr["DAT_CLO_CTR"], errors="coerce")

# DATEDIFF('day', DAT_OUV_CTR, DAT_CLO_CTR)
ctr["DUREE_JOURS"] = (ctr["DAT_CLO_CTR_DT"] - ctr["DAT_OUV_CTR_DT"]).dt.days

contrats_clos = ctr[ctr["DUREE_JOURS"].notna()]
print(f"Contrats clôturés : {len(contrats_clos)}")
print(f"Durée moyenne     : {contrats_clos['DUREE_JOURS'].mean():.0f} jours")
print(f"Durée médiane     : {contrats_clos['DUREE_JOURS'].median():.0f} jours")

contrats_clos[["REF_CTR_INN", "DAT_OUV_CTR", "DAT_CLO_CTR", "DUREE_JOURS"]].head(8)"""),

code("""# ADD_MONTHS : ajouter N mois à une date
from pandas.tseries.offsets import DateOffset

date_ref = pd.Timestamp("2026-01-01")

print("Date de référence :", date_ref.strftime("%Y-%m-%d"))
for n in [1, 3, 6, 12, 13]:
    date_calculee = date_ref + DateOffset(months=n)
    print(f"  + {n:2d} mois → {date_calculee.strftime('%Y-%m-%d')}")"""),

code("""# DATE_TRUNC : premier jour du mois (très utilisé en bancaire)
txn["DAT_CRE_MVT_CPB_DT"] = pd.to_datetime(txn["DAT_CRE_MVT_CPB"], errors="coerce")

# DATE_TRUNC('month', date)
txn["MOIS"] = txn["DAT_CRE_MVT_CPB_DT"].dt.to_period("M")
txn["DEBUT_MOIS"] = txn["DAT_CRE_MVT_CPB_DT"].dt.to_period("M").dt.to_timestamp()

print("Aperçu des dates arrondies au mois :")
txn[["DAT_CRE_MVT_CPB_DT", "MOIS", "DEBUT_MOIS"]].dropna().head(6)"""),

# ----- Périodes glissantes -----
md("""### 3.3 Période glissante sur 13 mois

Cas typique en analyse bancaire : analyser les 13 derniers mois glissants."""),

code("""import pandas as pd
from pandas.tseries.offsets import DateOffset

# Date de référence = aujourd'hui
aujourd_hui = pd.Timestamp.today().normalize()
debut_13m   = aujourd_hui - DateOffset(months=13)

print(f"Période : {debut_13m.strftime('%Y-%m-%d')} → {aujourd_hui.strftime('%Y-%m-%d')}")

# Filtrer les transactions sur 13 mois glissants
txn["DAT_CRE_MVT_CPB_DT"] = pd.to_datetime(txn["DAT_CRE_MVT_CPB"], errors="coerce")

txn_13m = txn[
    (txn["DAT_CRE_MVT_CPB_DT"] >= debut_13m) &
    (txn["DAT_CRE_MVT_CPB_DT"] <= aujourd_hui)
].copy()

print(f"\\nTransactions sur 13 mois : {len(txn_13m):,} / {len(txn):,} au total")"""),

code("""# Agrégation mensuelle des transactions
txn["DAT_CRE_MVT_CPB_DT"] = pd.to_datetime(txn["DAT_CRE_MVT_CPB"], errors="coerce")
txn["MOIS"] = txn["DAT_CRE_MVT_CPB_DT"].dt.to_period("M")

evolution_mensuelle = (
    txn
    .groupby("MOIS")
    .agg(
        nb_transactions  = ("NUM_ORD_MVT_CPB", "count"),
        nb_comptes       = ("IDT_AC", "nunique"),
        nb_folios        = ("NUM_FOL_XTR", "nunique"),
    )
    .reset_index()
    .sort_values("MOIS")
)

evolution_mensuelle["MOIS_STR"] = evolution_mensuelle["MOIS"].astype(str)
print(evolution_mensuelle.to_string(index=False))"""),

# ----- Section 4 : Pandas avancé -----
md("""---
## 4. Pandas Avancé

### 4.1 Nettoyage et gestion des valeurs manquantes"""),

code("""# Identifier les manquants
print("=== Table CTR — valeurs manquantes ===")
manquants = ctr.isnull().sum()
pct       = (manquants / len(ctr) * 100).round(1)
res = pd.DataFrame({"Manquants": manquants, "Pct %": pct})
print(res[res["Manquants"] > 0].to_string())"""),

code("""# Stratégies de remplacement des valeurs manquantes

# 1. Remplacer par une valeur fixe
ctr["COD_DEV_CLEAN"] = ctr["COD_DEV"].fillna("EUR")

# 2. Remplacer par la médiane (pour les numériques)
# ctr["SLD_CTR_FILL"] = ctr["SLD_CTR"].fillna(ctr["SLD_CTR"].median())

# 3. Supprimer les lignes sans date d'ouverture
ctr_complet = ctr.dropna(subset=["DAT_OUV_CTR"])
print(f"CTR après suppression sans DAT_OUV_CTR : {len(ctr_complet)} / {len(ctr)} lignes")"""),

md("""### 4.2 Conversions de types"""),

code("""# Convertir des colonnes et vérifier les types
print("Types avant conversion :")
print(ctr[["IDT_AC", "COD_ECV_CTR", "COD_DEV"]].dtypes)

# IDT_AC est numérique (float64 à cause des NaN), on peut le forcer en Int64 nullable
ctr["IDT_AC"] = ctr["IDT_AC"].astype("Int64")

# COD_ECV_CTR est une chaîne : vérifier
ctr["COD_ECV_CTR"] = ctr["COD_ECV_CTR"].astype(str).str.strip()

print("\\nTypes après conversion :")
print(ctr[["IDT_AC", "COD_ECV_CTR", "COD_DEV"]].dtypes)"""),

md("""### 4.3 Application de fonctions sur colonnes"""),

code("""# apply() : appliquer une fonction à chaque valeur d'une colonne
def cat_statut(code):
    if code in ("1", "2", "3"):
        return "Actif"
    elif code in ("4", "5", "6"):
        return "Inactif"
    return "Inconnu"

ctr["CAT_STATUT"] = ctr["COD_ECV_CTR"].apply(cat_statut)

# apply() sur une lambda
tie["NOM_COMPLET"] = tie_adr["NOM_TIE"].apply(lambda x: str(x).strip().title() if pd.notna(x) else "N/A")

print(ctr[["REF_CTR_INN", "COD_ECV_CTR", "CAT_STATUT"]].head(8).to_string(index=False))"""),

md("""### 4.4 Pipeline de traitement"""),

code("""# Un pipeline simple avec le chaînage de méthodes Pandas (method chaining)
# Inspiré du style proc sql avec plusieurs étapes

pipeline_clients = (
    tie
    .merge(tie_adr[["IDT_PI", "NOM_TIE", "PRN", "NOM_VIL", "ADR_EMA"]], on="IDT_PI", how="left")
    .assign(
        NOM_COMPLET = lambda df: (
            df["PRN"].fillna("").str.strip().str.title() + " " +
            df["NOM_TIE"].fillna("").str.strip().str.title()
        ).str.strip(),
        TRANCHE_AGE = lambda df: pd.cut(
            ((pd.Timestamp.today() - pd.to_datetime(df["DAT_NAI"], errors="coerce")).dt.days / 365.25),
            bins=[0, 25, 35, 50, 65, 120],
            labels=["< 25 ans", "25-34 ans", "35-49 ans", "50-64 ans", "65+ ans"],
            right=False
        )
    )
    [["IDT_PI", "NOM_COMPLET", "COD_SEX", "TRANCHE_AGE", "COD_LNG_CTR", "NOM_VIL", "ADR_EMA"]]
)

print(f"Pipeline clients : {len(pipeline_clients)} lignes")
pipeline_clients.head(8)"""),

# ----- Section 5 : Visualisation -----
md("""---
## 5. Visualisation avec Matplotlib

### 5.1 Bar chart — transactions par mois"""),

code("""import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Données : transactions par mois
txn["DAT_CRE_MVT_CPB_DT"] = pd.to_datetime(txn["DAT_CRE_MVT_CPB"], errors="coerce")
txn["MOIS_STR"] = txn["DAT_CRE_MVT_CPB_DT"].dt.strftime("%Y-%m")

agg_mois = (
    txn.dropna(subset=["MOIS_STR"])
    .groupby("MOIS_STR")
    .size()
    .reset_index(name="nb_txn")
    .sort_values("MOIS_STR")
)

# Bar chart
fig, ax = plt.subplots(figsize=(12, 5))

ax.bar(agg_mois["MOIS_STR"], agg_mois["nb_txn"], color="#1f77b4", edgecolor="white")

ax.set_title("Nombre de transactions par mois", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("Mois", fontsize=11)
ax.set_ylabel("Nombre de transactions", fontsize=11)
ax.tick_params(axis="x", rotation=45)
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("bar_transactions_mois.png", dpi=120, bbox_inches="tight")
plt.show()
print("Graphique sauvegardé : bar_transactions_mois.png")"""),

md("""### 5.2 Line chart — évolution mensuelle"""),

code("""import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Données
txn["MOIS_DT"] = txn["DAT_CRE_MVT_CPB_DT"].dt.to_period("M").dt.to_timestamp()

evol = txn.groupby("MOIS_DT").agg(
    nb_txn     = ("NUM_ORD_MVT_CPB", "count"),
    nb_comptes = ("IDT_AC", "nunique")
).reset_index().sort_values("MOIS_DT")

# Line chart avec deux axes Y
fig, ax1 = plt.subplots(figsize=(12, 5))

color_txn = "#1f77b4"
color_cpt = "#ff7f0e"

# Axe 1 : transactions
ax1.plot(evol["MOIS_DT"], evol["nb_txn"], color=color_txn, marker="o", linewidth=2, label="Nb transactions")
ax1.set_ylabel("Transactions", color=color_txn, fontsize=11)
ax1.tick_params(axis="y", labelcolor=color_txn)
ax1.tick_params(axis="x", rotation=45)

# Axe 2 : comptes
ax2 = ax1.twinx()
ax2.plot(evol["MOIS_DT"], evol["nb_comptes"], color=color_cpt, marker="s", linewidth=2, linestyle="--", label="Nb comptes actifs")
ax2.set_ylabel("Comptes actifs", color=color_cpt, fontsize=11)
ax2.tick_params(axis="y", labelcolor=color_cpt)

ax1.set_title("Évolution mensuelle des transactions et comptes actifs", fontsize=13, fontweight="bold")
ax1.grid(alpha=0.3)

# Légende combinée
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

plt.tight_layout()
plt.savefig("line_evolution_mensuelle.png", dpi=120, bbox_inches="tight")
plt.show()"""),

md("""### 5.3 Pie chart — répartition par type de client"""),

code("""import matplotlib.pyplot as plt

# Données
repartition = tie["COD_TYP_TIE"].value_counts()
mapping_type = {"1": "Personnes physiques", "2": "Personnes morales"}
labels = [mapping_type.get(str(k), str(k)) for k in repartition.index]
valeurs = repartition.values

# Pie chart
fig, ax = plt.subplots(figsize=(7, 7))

couleurs = ["#1f77b4", "#ff7f0e", "#2ca02c"]
explode = [0.05] * len(labels)

wedges, texts, autotexts = ax.pie(
    valeurs,
    labels=labels,
    autopct="%1.1f%%",
    colors=couleurs[:len(labels)],
    explode=explode,
    startangle=90,
    textprops={"fontsize": 12}
)

for autotext in autotexts:
    autotext.set_fontweight("bold")

ax.set_title("Répartition des clients par type", fontsize=14, fontweight="bold", pad=15)

plt.tight_layout()
plt.savefig("pie_type_clients.png", dpi=120, bbox_inches="tight")
plt.show()"""),

# ----- Mini-projet -----
md("""---
## 6. Mini-projet fil rouge — Tableau de bord Beobank

### Objectif
Produire un rapport complet à partir des 5 tables Beobank :
1. Charger et nettoyer toutes les tables
2. Joindre pour obtenir une vue client-contrat-transaction
3. Calculer des indicateurs temporels (13 mois)
4. Visualiser les tendances
5. Exporter le résultat

Exécutez les cellules dans l'ordre."""),

code("""# ÉTAPE 1 : Chargement et nettoyage
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from pandas.tseries.offsets import DateOffset

DATA = Path("../Orsys")
params = dict(sep=";", na_values=".", encoding="utf-8")

print("=== ÉTAPE 1 : Chargement des données ===")
ctr       = pd.read_csv(DATA / "CTR.csv",       **params)
tie       = pd.read_csv(DATA / "TIE.csv",       **params)
tie_adr   = pd.read_csv(DATA / "TIE_ADR.csv",   **params)
tie_x_ctr = pd.read_csv(DATA / "TIE_X_CTR.csv", **params)
txn       = pd.read_csv(DATA / "TXN_X_CTR.csv", **params)

# Conversion des dates
for col in ["DAT_OUV_CTR", "DAT_CLO_CTR", "DAT_ECV_CTR"]:
    ctr[col] = pd.to_datetime(ctr[col], errors="coerce")
tie["DAT_NAI"] = pd.to_datetime(tie["DAT_NAI"], errors="coerce")
txn["DAT_CRE_MVT_CPB"] = pd.to_datetime(txn["DAT_CRE_MVT_CPB"], errors="coerce")

# Nettoyage des chaînes
ctr["COD_ECV_CTR"] = ctr["COD_ECV_CTR"].astype(str).str.strip()
ctr["COD_DEV"] = ctr["COD_DEV"].fillna("EUR")

print(f"  CTR       : {len(ctr):>5} lignes")
print(f"  TIE       : {len(tie):>5} lignes")
print(f"  TIE_ADR   : {len(tie_adr):>5} lignes")
print(f"  TIE_X_CTR : {len(tie_x_ctr):>5} lignes")
print(f"  TXN       : {len(txn):>5} lignes")
print("OK")"""),

code("""# ÉTAPE 2 : Construction de la vue analytique
print("=== ÉTAPE 2 : Jointures ===")

# Client enrichi
clients = tie.merge(
    tie_adr[["IDT_PI", "NOM_TIE", "PRN", "NOM_VIL", "COD_PAY_ISO"]],
    on="IDT_PI", how="left"
)
clients["NOM_COMPLET"] = (
    clients["PRN"].fillna("").str.strip().str.title() + " " +
    clients["NOM_TIE"].fillna("").str.strip().str.title()
).str.strip()

# Jointure Clients → Contrats
vue = (
    tie_x_ctr[["IDT_PI", "IDT_AC", "FLG_PRE_TTL"]]
    .merge(clients[["IDT_PI", "NOM_COMPLET", "COD_TYP_TIE", "COD_SEX", "COD_LNG_CTR"]], on="IDT_PI", how="left")
    .merge(ctr[["IDT_AC", "REF_CTR_INN", "DAT_OUV_CTR", "COD_ECV_CTR", "COD_DEV"]], on="IDT_AC", how="left")
)

print(f"Vue client-contrat : {len(vue):,} lignes × {vue.shape[1]} colonnes")
print("OK")"""),

code("""# ÉTAPE 3 : Indicateurs temporels (13 mois)
print("=== ÉTAPE 3 : Indicateurs sur 13 mois glissants ===")

aujourd_hui = pd.Timestamp.today().normalize()
debut_13m   = aujourd_hui - DateOffset(months=13)

txn_13m = txn[txn["DAT_CRE_MVT_CPB"] >= debut_13m].copy()
txn_13m["MOIS"] = txn_13m["DAT_CRE_MVT_CPB"].dt.to_period("M")

resume_comptes = txn_13m.groupby("IDT_AC").agg(
    nb_txn_13m     = ("NUM_ORD_MVT_CPB", "count"),
    mois_actif_13m = ("MOIS", "nunique"),
    premiere_txn   = ("DAT_CRE_MVT_CPB", "min"),
    derniere_txn   = ("DAT_CRE_MVT_CPB", "max"),
).reset_index()

print(f"Comptes actifs sur 13 mois  : {len(resume_comptes)}")
print(f"Total transactions 13 mois  : {resume_comptes['nb_txn_13m'].sum():,}")
print(f"Moyenne txn/compte/13mois   : {resume_comptes['nb_txn_13m'].mean():.1f}")
print("OK")"""),

code("""# ÉTAPE 4 : Visualisations du tableau de bord
print("=== ÉTAPE 4 : Visualisations ===")

# Données pour les graphiques
evol_mois = txn_13m.groupby("MOIS").size().reset_index(name="nb_txn").sort_values("MOIS")
evol_mois["MOIS_STR"] = evol_mois["MOIS"].astype(str)

repartition_ecv = ctr["COD_ECV_CTR"].value_counts()
mapping_ecv = {"1":"Ouvert","2":"En attente","3":"Suspendu","4":"Clôturé","5":"En résil.","6":"Résilié"}

repartition_type = tie["COD_TYP_TIE"].value_counts()
mapping_type = {"1":"Pers. physique","2":"Pers. morale"}

# Figure avec 3 graphiques
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle("Tableau de bord Beobank — " + aujourd_hui.strftime("%d/%m/%Y"),
             fontsize=15, fontweight="bold", y=1.02)

# Graphique 1 : line chart — évolution mensuelle
ax1 = axes[0]
ax1.plot(range(len(evol_mois)), evol_mois["nb_txn"], marker="o", color="#1f77b4", linewidth=2)
ax1.set_xticks(range(len(evol_mois)))
ax1.set_xticklabels(evol_mois["MOIS_STR"], rotation=45, ha="right", fontsize=8)
ax1.set_title("Transactions / mois (13 mois)", fontsize=12, fontweight="bold")
ax1.set_ylabel("Nb transactions")
ax1.grid(axis="y", alpha=0.3)

# Graphique 2 : bar chart — contrats par statut
labels_ecv = [mapping_ecv.get(str(k), str(k)) for k in repartition_ecv.index]
ax2 = axes[1]
bars = ax2.bar(labels_ecv, repartition_ecv.values, color=["#2ca02c","#ff7f0e","#d62728","#9467bd","#8c564b","#1f77b4"][:len(labels_ecv)])
ax2.set_title("Contrats par statut", fontsize=12, fontweight="bold")
ax2.set_ylabel("Nb contrats")
ax2.tick_params(axis="x", rotation=30)
ax2.grid(axis="y", alpha=0.3)
for bar, val in zip(bars, repartition_ecv.values):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, str(val), ha="center", fontsize=9)

# Graphique 3 : pie chart — type de clients
labels_type = [mapping_type.get(str(k), str(k)) for k in repartition_type.index]
ax3 = axes[2]
ax3.pie(repartition_type.values, labels=labels_type, autopct="%1.1f%%",
        colors=["#1f77b4","#ff7f0e"], startangle=90,
        textprops={"fontsize": 11})
ax3.set_title("Répartition clients", fontsize=12, fontweight="bold")

plt.tight_layout()
plt.savefig("tableau_de_bord_beobank.png", dpi=120, bbox_inches="tight")
plt.show()
print("Tableau de bord sauvegardé : tableau_de_bord_beobank.png")"""),

code("""# ÉTAPE 5 : Export final
print("=== ÉTAPE 5 : Export ===")

# Vue analytique enrichie avec les indicateurs 13 mois
export_final = (
    vue
    .merge(resume_comptes[["IDT_AC", "nb_txn_13m", "mois_actif_13m", "premiere_txn", "derniere_txn"]],
           on="IDT_AC", how="left")
)

# Ajout du libellé statut
export_final["LIB_ECV"] = export_final["COD_ECV_CTR"].map(mapping_ecv).fillna("Inconnu")

# Export CSV
export_final.to_csv("beobank_vue_analytique.csv", sep=";", index=False, encoding="utf-8")

# Export JSON (10 premières lignes pour illustration)
sample_json = export_final.head(10).copy()
for col in sample_json.select_dtypes(include=["datetime64"]).columns:
    sample_json[col] = sample_json[col].astype(str)
sample_json.to_json("beobank_sample.json", orient="records", indent=2, force_ascii=False)

print(f"CSV exporté  : beobank_vue_analytique.csv ({len(export_final):,} lignes)")
print(f"JSON exporté : beobank_sample.json (10 lignes)")
print()
print("=== MINI-PROJET TERMINÉ ===")
print("Vous avez :")
print("  ✓ Chargé et nettoyé 5 tables Beobank")
print("  ✓ Joint les tables pour créer une vue analytique")
print("  ✓ Calculé des indicateurs sur 13 mois glissants")
print("  ✓ Produit 3 visualisations")
print("  ✓ Exporté les résultats en CSV et JSON")"""),

md("""---
## Résumé du Jour 3 — et de la formation

### Ce que vous avez appris en 3 jours

| Jour | Compétences acquises |
|------|---------------------|
| **Jour 1** | Variables, conditions, boucles, listes, dictionnaires, fonctions, lambda |
| **Jour 2** | Lecture de fichiers, Pandas (chargement, exploration, filtrage, export), flux Vertica |
| **Jour 3** | Jointures multi-tables, dates et time series, Vertica SQL analytique, Matplotlib |

### Correspondances SAS → Python

| SAS | Python / Pandas |
|-----|----------------|
| `DATA ... ; RUN;` | `df = df.assign(...)` |
| `PROC SQL; CREATE TABLE ...` | `df.merge(...)` |
| `LAG()` | `.shift(1)` |
| `INTCK('month', d1, d2)` | `(d2 - d1) / pd.DateOffset(months=1)` |
| `ADD_MONTHS(d, n)` | `d + DateOffset(months=n)` |
| `INTNX('month', d, 0, 'B')` | `d.to_period('M').to_timestamp()` |
| `PROC GPLOT` | `matplotlib.pyplot` |

### Ressources pour continuer
- **Pandas** : https://pandas.pydata.org/docs/
- **Matplotlib** : https://matplotlib.org/stable/gallery/
- **Real Python** (tutoriels) : https://realpython.com
- **Kaggle** (exercices) : https://www.kaggle.com/learn/pandas

**Bravo — vous êtes maintenant opérationnels sur Python pour l'analyse de données !**"""),

] # fin j3


# ========== Sauvegarde ==========
for nom, nb in [
    ("Jour1_Fondamentaux_Python.ipynb",              notebook(j1)),
    ("Jour2_Fichiers_Pandas.ipynb",                  notebook(j2)),
    ("Jour3_SQL_TimeSeries_Visualisation.ipynb",     notebook(j3)),
]:
    path = os.path.join(OUTPUT_DIR, nom)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    taille = os.path.getsize(path) / 1024
    print(f"Créé : {nom}  ({taille:.0f} Ko)")

print("\\nTous les notebooks sont prêts dans : " + OUTPUT_DIR)
