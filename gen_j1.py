'''Générateur Jour 1 — Fondamentaux Python · Formation Beobank'''
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

# ================================================================
# FIL ROUGE — contexte établi dès le départ
# ================================================================
CONTEXTE = md("""# 🏦 Projet fil rouge — Rapport d'activité Beobank

## Votre mission pour ces 3 jours

Vous êtes **analyste data chez Beobank**. Votre responsable vous demande de créer
un **rapport mensuel d'activité** du portefeuille clients, à présenter au comité de direction.

Ce rapport doit répondre à 4 questions :

1. **Inventaire des contrats** — Combien de contrats sont actifs, clôturés, résiliés ?
2. **Profil des clients** — Qui sont nos clients ? Quel âge, quelle langue, quel genre ?
3. **Activité transactionnelle** — Quels comptes sont les plus actifs sur 13 mois ?
4. **Visualisations** — Courbes d'évolution, graphiques de répartition pour le PowerPoint.

---

## Vos 5 sources de données (extraits du SI Beobank)

| Fichier | Contenu | Lignes | Clé |
|---------|---------|--------|-----|
| `CTR.csv` | Contrats bancaires | 200 | `IDT_AC` |
| `TIE.csv` | Clients (tiers) | 100 | `IDT_PI` |
| `TIE_ADR.csv` | Adresses clients | 100 | `IDT_PI` |
| `TIE_X_CTR.csv` | Liens client ↔ contrat | 200 | `IDT_PI` + `IDT_AC` |
| `TXN_X_CTR.csv` | Transactions | 1 260 | `IDT_AC` + date |

> **Format des fichiers :** séparateur `;`, valeur manquante `.` (convention SAS), encodage UTF-8

---

## Plan des 3 jours

- **Jour 1 (aujourd'hui)** — Bases Python : variables, conditions, boucles, listes, dicts, fonctions
- **Jour 2** — Pandas : lire les 5 fichiers, nettoyer, transformer, exporter
- **Jour 3** — SQL analytique, dates, visualisations, mini-projet complet

> Chaque exercice s'appuie sur des données réelles extraites de vos fichiers Beobank.
> À la fin du Jour 3 vous aurez produit le rapport complet.""")

# ================================================================
# JOUR 1
# ================================================================

j1 = [

md("""# Jour 1 — Fondamentaux Python pour Analystes Data
## Formation Python Beobank · 18 novembre 2026

**Mode d'emploi de ce notebook**
- Exécutez chaque cellule avec **`Shift + Entrée`**
- Le résultat s'affiche juste en dessous
- Si une cellule contient une erreur, lisez le message : il indique la ligne concernée
- Vous pouvez modifier et ré-exécuter n'importe quelle cellule"""),

CONTEXTE,

# ----- SECTION 1 : Python vs SAS -----
md("""---
# Section 1 — Pourquoi Python ? Python vs SAS

## 1.1 Les différences fondamentales

Vous venez de SAS. Voici les équivalences les plus importantes pour ne pas être dépaysé.

| Concept | SAS | Python |
|---------|-----|--------|
| Afficher une valeur | `put variable;` | `print(variable)` |
| Commentaire sur une ligne | `* mon commentaire;` | `# mon commentaire` |
| Commentaire sur plusieurs lignes | `/* ... */` | `''''' ... '''` ou `# ` sur chaque ligne |
| Affecter une variable | `x = 5;` | `x = 5` (pas de `;`) |
| Bloc de code | `DATA ... ; RUN;` | **indentation obligatoire** (4 espaces) |
| Valeur manquante numérique | `.` | `None` ou `float('nan')` |
| Valeur manquante texte | `' '` | `None` ou `''` |
| Chaîne de caractères | `'texte'` | `'texte'` ou `"texte"` |

## 1.2 La règle numéro 1 : l'indentation

En SAS, vous délimitez les blocs avec `DATA...RUN;` ou `PROC...RUN;`.
En Python, **l'indentation (les espaces en début de ligne) EST la délimitation**.

```
SAS :                          Python :
if x > 0 then do;              if x > 0:
    y = x * 2;                     y = x * 2
end;                               z = y + 1
```

Conseil : utilisez **toujours 4 espaces** (pas des tabulations). Jupyter le fait automatiquement."""),

code("""# Votre première cellule Python
# Le # indique un commentaire — Python ignore tout ce qui suit

print("Bonjour, je suis analyste chez Beobank !")
print("Je vais apprendre Python en 3 jours.")

# Un calcul simple
100 + 200"""),

code("""# Python comme calculatrice
print(10 + 3)    # addition
print(10 - 3)    # soustraction
print(10 * 3)    # multiplication
print(10 / 3)    # division (retourne un float)
print(10 // 3)   # division entière
print(10 % 3)    # modulo (reste de la division)
print(10 ** 2)   # puissance (10²)"""),

# ----- SECTION 2 : Variables et types -----
md("""---
# Section 2 — Variables et types de données

## 2.1 Créer une variable

En Python, vous n'avez **pas besoin de déclarer le type** à l'avance.
Python le déduit automatiquement selon la valeur que vous assignez.

```python
x = 5        # Python sait que x est un entier
y = 3.14     # Python sait que y est un décimal
z = "texte"  # Python sait que z est une chaîne
```

En SAS :
```sas
length nom $20;
nom = 'JANSSENS';
age = 45;
```"""),

code("""# Les 5 types de base que vous utiliserez tous les jours

# 1. int — entier
identifiant = 655010249

# 2. float — décimal (virgule flottante)
solde = 1250.75

# 3. str — chaîne de caractères (string)
nom_client = "JANSSENS"
prenom     = "Bart"
code_etat  = "4"        # même si c'est un chiffre, ici c'est du texte !

# 4. bool — booléen (vrai/faux)
est_actif  = True
est_cloture = False

# 5. None — valeur manquante (équivalent du . en SAS)
date_cloture = None   # le contrat n'est pas encore clôturé

# Afficher toutes les valeurs
print("Identifiant  :", identifiant)
print("Solde        :", solde, "EUR")
print("Nom          :", nom_client, prenom)
print("Code état    :", code_etat)
print("Actif        :", est_actif)
print("Date clôture :", date_cloture)"""),

code("""# Vérifier le type d'une variable avec type()
identifiant  = 655010249
solde        = 1250.75
nom          = "JANSSENS"
est_actif    = True
sans_valeur  = None

print(type(identifiant))   # <class 'int'>
print(type(solde))         # <class 'float'>
print(type(nom))           # <class 'str'>
print(type(est_actif))     # <class 'bool'>
print(type(sans_valeur))   # <class 'NoneType'>"""),

code("""# Convertir d'un type à l'autre
# Utile quand vous lisez des données CSV (tout arrive en texte)

code_str = "4"          # lu depuis le CSV : c'est une chaîne "4"
code_int = int(code_str)  # convertir en entier
print(code_int, type(code_int))

montant_str = "1250.75"
montant_float = float(montant_str)
print(montant_float, type(montant_float))

# L'inverse : convertir en texte
id_num = 655010249
id_str = str(id_num)
print(id_str, type(id_str))

# Attention : convertir "." (SAS manquant) en float provoque une erreur !
# float(".")  → ValueError !
# Il faudra gérer ce cas avec Pandas (on le verra Jour 2)"""),

# ----- SECTION 3 : Chaînes -----
md("""---
# Section 3 — Opérations sur les chaînes de caractères

Les chaînes (str) sont au cœur de l'analyse de données : noms de colonnes,
codes, libellés, nettoyage de données textuelles.

## 3.1 Les f-strings : la façon moderne d'afficher

En SAS : `put "Bonjour " nom " votre solde est " solde;`
En Python (f-string) : `f"Bonjour {nom}, votre solde est {solde}"`"""),

code("""# f-string : préfixez avec f, mettez les variables entre { }
prenom = "Bart"
nom    = "Janssens"
solde  = 1250.75
devise = "EUR"

# Syntaxe de base
message = f"Bonjour {prenom} {nom} !"
print(message)

# Formatage des nombres
print(f"Solde : {solde:.2f} {devise}")         # 2 décimales
print(f"Solde : {solde:,.2f} {devise}")        # avec séparateur milliers
print(f"Identifiant : {655010249:,}")          # entier formaté
print(f"Pourcentage : {0.1523:.1%}")           # format pourcentage"""),

code("""# Méthodes utiles sur les chaînes — très utiles pour nettoyer des données

texte = "  JANSSENS bart  "   # chaîne avec espaces, casse mixte

print(texte.strip())          # supprimer espaces début et fin → "JANSSENS bart"
print(texte.lower())          # tout en minuscules
print(texte.upper())          # tout en majuscules
print(texte.title())          # Première lettre en majuscule
print(texte.strip().title())  # les deux ensemble → "Janssens Bart"

# Tester le contenu
code = "  6 "
print(code.strip() == "6")   # True (après nettoyage)
print("6" in code)           # True (contient "6")
print(code.isdigit())        # False (à cause des espaces)
print(code.strip().isdigit()) # True"""),

code("""# split() : découper une chaîne — très utile pour parser des données
adresse = "RUE DE L'ABRICOTIER 5"
mots = adresse.split(" ")    # découper par espace
print(mots)
print("Nombre de mots :", len(mots))

# Exemple avec un libellé de transaction
lib_ope = "SEPA THAIS BBA ZIEKENFONDS"
parties = lib_ope.split(" ")
print("Premier mot :", parties[0])   # "SEPA"
print("Reste :", " ".join(parties[1:]))  # "THAIS BBA ZIEKENFONDS"

# replace() : remplacer une sous-chaîne
email = "BART.JANSSENS@GMAIL.COM"
email_propre = email.lower().replace("@gmail.com", "")
print("Nom d'utilisateur :", email_propre)

# startswith() et endswith()
ref = "0029862201102"
print(ref.startswith("002"))   # True
print(ref.endswith("102"))     # True"""),

code("""# Application sur les données Beobank
# Nettoyage de noms de villes (comme dans TIE_ADR.csv)

villes_brutes = ["  BRUXELLES  ", "bruxelles", "BRUSSEL ", " Bruxelles", "LIÈGE"]

# Normaliser : enlever espaces, mettre en majuscules
villes_propres = [v.strip().upper() for v in villes_brutes]
print("Avant :", villes_brutes)
print("Après :", villes_propres)

# Vérifier si c'est Bruxelles (plusieurs orthographes)
for ville in villes_propres:
    if "BRUX" in ville or "BRUSSEL" in ville:
        print(f"  {ville} → région bruxelloise")
    else:
        print(f"  {ville} → autre"  )"""),

# ----- SECTION 4 : Conditions -----
md("""---
# Section 4 — Conditions : if / elif / else

## 4.1 Syntaxe de base

```python
if condition:
    # code exécuté si condition est True
elif autre_condition:
    # code exécuté si autre_condition est True
else:
    # code exécuté si aucune condition n'est True
```

**Important :** le `:` en fin de ligne et l'indentation de 4 espaces sont obligatoires !"""),

code("""# Exemple 1 : classifier un contrat selon COD_ECV_CTR
# Données réelles de la table CTR

cod_ecv = "4"   # code état du contrat

if cod_ecv == "1":
    statut = "Ouvert"
elif cod_ecv == "2":
    statut = "En attente"
elif cod_ecv == "3":
    statut = "Suspendu"
elif cod_ecv == "4":
    statut = "Clôturé"
elif cod_ecv == "5":
    statut = "En cours de résiliation"
elif cod_ecv == "6":
    statut = "Résilié"
else:
    statut = f"Code inconnu : {cod_ecv}"

print(f"Code {cod_ecv} → {statut}")"""),

code("""# Exemple 2 : opérateurs de comparaison
age = 45

print(age > 18)    # True
print(age < 18)    # False
print(age >= 45)   # True
print(age <= 44)   # False
print(age == 45)   # True  (attention : == pour comparer, = pour affecter)
print(age != 45)   # False (différent de)

# Tester None (valeur manquante)
date_naissance = None

if date_naissance is None:     # TOUJOURS utiliser "is None", pas "== None"
    print("Date de naissance non renseignée")
else:
    print(f"Né(e) le {date_naissance}")"""),

code("""# Exemple 3 : opérateurs logiques (and, or, not)
# Contexte : classifier un client pour une offre commerciale

cod_typ_tie = "1"     # 1 = personne physique
cod_sex     = "M"
langue      = "FR"
age         = 35

# and : les deux conditions doivent être vraies
if cod_typ_tie == "1" and age < 40:
    print("Client cible : jeune adulte personne physique")

# or : au moins une condition doit être vraie
if langue == "FR" or langue == "NL":
    print(f"Langue reconnue : {langue}")
else:
    print("Langue non reconnue")

# not : inverser une condition
est_decede = False
if not est_decede:
    print("Client actif (non décédé)")

# Combinaison : critères de segmentation
if cod_typ_tie == "1" and age >= 25 and age <= 60 and not est_decede:
    print("Segment : adulte actif personne physique")"""),

code("""# Exemple 4 : condition sur appartenance à une liste (in)
# Equivalent SAS : if cod_ecv_ctr in ('1','2','3')

cod_ecv = "4"

# in : vérifie si une valeur est dans une collection
if cod_ecv in ("1", "2", "3"):
    categorie = "Actif"
elif cod_ecv in ("4", "5", "6"):
    categorie = "Inactif"
else:
    categorie = "Inconnu"

print(f"Catégorie : {categorie}")

# not in : vérifie qu'une valeur n'est PAS dans la collection
codes_valides = ["1", "2", "3", "4", "5", "6"]
code_test = "9"
if code_test not in codes_valides:
    print(f"ERREUR : code '{code_test}' non valide"  )"""),

# ----- Exercice conditions -----
md("""## Exercice 4.1 — Classifier les contrats Beobank

**Contexte :** Pour votre rapport, vous devez créer un libellé lisible pour chaque contrat
et une catégorie binaire Actif/Inactif.

**Tâche :** Complétez la fonction `classifier_contrat()` et testez-la sur les 6 codes possibles."""),

code("""# ============================================================
# EXERCICE 4.1 — Classifier les contrats
# ============================================================

def classifier_contrat(cod_ecv_ctr):
    '''
    Retourne (libelle, categorie) pour un code état contrat.

    Args:
        cod_ecv_ctr (str): Code état du contrat ("1" à "6")

    Returns:
        tuple: (libelle str, categorie str "Actif"/"Inactif"/"Inconnu")

    Exemples:
        classifier_contrat("1") → ("Ouvert", "Actif")
        classifier_contrat("4") → ("Clôturé", "Inactif")
    '''
    # TODO : compléter le mapping
    mapping = {
        "1": ("Ouvert",                  "Actif"),
        "2": ("En attente",              "Actif"),
        "3": ("Suspendu",                "Actif"),
        "4": ("Clôturé",                 "Inactif"),
        "5": ("En cours de résiliation", "Inactif"),
        "6": ("Résilié",                 "Inactif"),
    }
    if cod_ecv_ctr in mapping:
        return mapping[cod_ecv_ctr]
    return (f"Inconnu ({cod_ecv_ctr})", "Inconnu")


# TEST : parcourir tous les codes possibles
print(f"{'Code':>6}  {'Libellé':30}  {'Catégorie'}")
print("-" * 55)
for code in ["1", "2", "3", "4", "5", "6", "9"]:
    lib, cat = classifier_contrat(code)
    print(f"  {code:>4}   {lib:30}  {cat}")"""),

# ----- SECTION 5 : Boucles -----
md("""---
# Section 5 — Boucles : for et while

## 5.1 La boucle for

En SAS vous itérez sur des observations avec `DATA _null_; set ds;`.
En Python, `for` itère sur **n'importe quelle séquence** : liste, texte, plage de nombres..."""),

code("""# Boucle for de base — sur une liste
# Contexte : lister les codes état présents dans CTR

codes_present = ["6", "4", "6", "1", "4", "6", "4", "4"]

for code in codes_present:
    print(f"Code : {code}")"""),

code("""# range() — générer une séquence de nombres
# Equivalent SAS : do i = 1 to 5; ... end;

for i in range(1, 6):      # de 1 à 5 inclus (6 EXCLUS)
    print(f"Ligne {i}")

print()

# range(début, fin, pas)
for mois in range(1, 13):   # 12 mois
    print(f"  Mois {mois:02d}/2026")"""),

code("""# enumerate() — obtenir l'index ET la valeur en même temps
# Très utile quand vous avez besoin du numéro de ligne

noms_colonnes = ["IDT_AC", "REF_CTR_INN", "DAT_OUV_CTR", "COD_ECV_CTR", "COD_DEV"]

for index, colonne in enumerate(noms_colonnes, start=1):
    print(f"  Colonne {index} : {colonne}")"""),

code("""# Accumulation dans une boucle — compter et sommer
codes = ["6", "4", "6", "1", "4", "6", "4", "6", "1"]

compteur_actif   = 0
compteur_inactif = 0

for code in codes:
    if code in ("1", "2", "3"):
        compteur_actif += 1       # équivalent de compteur_actif = compteur_actif + 1
    elif code in ("4", "5", "6"):
        compteur_inactif += 1

total = len(codes)
print(f"Total contrats  : {total}")
print(f"Actifs          : {compteur_actif} ({compteur_actif/total:.0%})")
print(f"Inactifs        : {compteur_inactif} ({compteur_inactif/total:.0%})")"""),

code("""# Boucle sur deux listes simultanément avec zip()
# Utile pour associer colonnes et valeurs (comme une ligne de CSV)

colonnes = ["IDT_AC",      "DAT_OUV_CTR", "COD_ECV_CTR", "COD_DEV"]
valeurs  = [65500004701,   "2024-05-29",  "6",           "EUR"]

for col, val in zip(colonnes, valeurs):
    print(f"  {col:20s} : {val}")"""),

md("""## 5.2 break et continue"""),

code("""# break : arrêter la boucle quand une condition est remplie
refs = ["0029862201102", "0029912218433", "ERREUR", "0029922113324", "0029872222935"]

print("Vérification des références :")
for ref in refs:
    if not ref.startswith("002"):
        print(f"  ⚠ Référence invalide détectée : '{ref}' — arrêt du traitement")
        break
    print(f"  ✓ {ref}")

print("Fin du traitement")"""),

code("""# continue : sauter l'itération courante et passer à la suivante
codes = ["6", None, "4", "", "1", None, "6"]

print("Codes valides uniquement :")
for code in codes:
    if code is None or code == "":
        continue    # sauter les valeurs manquantes
    print(f"  Code : {code}")"""),

md("""## 5.3 La boucle while"""),

code("""# while : répéter TANT QUE la condition est vraie
# Utile pour des tentatives répétées ou des simulations

# Simulation : combien de mois pour qu'un solde atteigne 10 000 € ?
solde   = 5000.0
taux    = 0.005    # 0.5% par mois
mois    = 0
cible   = 10000.0

while solde < cible:
    solde  = solde * (1 + taux)
    mois  += 1

print(f"Solde initial : 5 000,00 EUR")
print(f"Solde final   : {solde:,.2f} EUR")
print(f"Durée         : {mois} mois ({mois//12} ans et {mois%12} mois)")"""),

# ----- Exercice boucles -----
md("""## Exercice 5.1 — Analyse des codes état

**Contexte :** Votre manager veut savoir, pour chaque code état présent dans CTR,
combien de contrats il y a et quel pourcentage du total il représente.

**Tâche :** À partir de la liste `codes_ctr` ci-dessous, produisez un résumé
avec boucle et dictionnaire de comptage.

> C'est exactement ce que vous ferez avec Pandas en Jour 2, mais ici on le fait
> "à la main" pour bien comprendre la logique."""),

code("""# ============================================================
# EXERCICE 5.1 — Résumé des codes état contrat
# ============================================================

# Données simulées (extrait de CTR.csv - colonne COD_ECV_CTR)
codes_ctr = [
    "6","4","4","4","4","4","4","4","4","1","4","4","4","4","6","6","4","4","6","4",
    "4","4","4","4","4","4","4","4","4","4","4","4","4","4","4","4","6","4","6","4",
    "4","4","4","4","4","4","4","4","4","4","4","4","4","4","4","4","4","4","4","4",
    "4","4","4","4","4","4","4","4","4","4","6","4","4","4","4","4","4","4","4","4",
]

mapping_libelle = {
    "1": "Ouvert",
    "2": "En attente",
    "3": "Suspendu",
    "4": "Clôturé",
    "5": "En résiliation",
    "6": "Résilié",
}

# ÉTAPE 1 : compter les occurrences de chaque code
comptage = {}
for code in codes_ctr:
    if code in comptage:
        comptage[code] += 1
    else:
        comptage[code] = 1

# ÉTAPE 2 : afficher le résumé trié par effectif décroissant
total = len(codes_ctr)
print(f"{'Code':>6}  {'Libellé':22}  {'Effectif':>9}  {'%':>7}")
print("-" * 52)
for code, nb in sorted(comptage.items(), key=lambda x: -x[1]):
    lib = mapping_libelle.get(code, "Inconnu")
    pct = nb / total
    print(f"  {code:>4}   {lib:22}  {nb:>9,}  {pct:>7.1%}")
print("-" * 52)
print(f"  {'TOTAL':>4}   {'':22}  {total:>9,}  {'100.0%':>7}")"""),

# ----- SECTION 6 : Listes -----
md("""---
# Section 6 — Les Listes

Une liste est une séquence **ordonnée** et **modifiable** d'éléments.
Pensez-y comme une colonne SAS que vous pouvez manipuler librement en dehors d'un dataset.

## 6.1 Créer et accéder à une liste"""),

code("""# Créer une liste
references = [
    "0029862201102",
    "0029912218433",
    "0029922113324",
    "0029872222935",
    "0029882034602",
]

# Accéder par index — ATTENTION : l'index commence à 0 en Python !
print("Première réf  :", references[0])    # index 0 = premier
print("Deuxième réf  :", references[1])    # index 1 = deuxième
print("Dernière réf  :", references[-1])   # index -1 = dernier
print("Avant-dern.   :", references[-2])   # index -2 = avant-dernier

print()
print("Longueur      :", len(references))  # nombre d'éléments"""),

code("""# Trancher une liste (slicing)
# syntaxe : liste[début:fin]   (fin EXCLUE)

numeros = [10, 20, 30, 40, 50, 60, 70, 80]

print("Tout               :", numeros)
print("3 premiers         :", numeros[:3])     # indices 0, 1, 2
print("Du 3ème au 5ème    :", numeros[2:5])    # indices 2, 3, 4
print("3 derniers         :", numeros[-3:])    # 3 derniers
print("Un sur deux        :", numeros[::2])    # pas de 2
print("Inverser           :", numeros[::-1])   # ordre inverse"""),

code("""# Modifier une liste
soldes = [1200.0, 850.5, 0.0, 2300.75, 150.0]
print("Initial :", soldes)

# Ajouter à la fin
soldes.append(999.99)
print("Après append :", soldes)

# Insérer à une position
soldes.insert(2, 500.0)    # insérer 500.0 à l'index 2
print("Après insert :", soldes)

# Supprimer le dernier élément
dernier = soldes.pop()
print("Dernier supprimé :", dernier)
print("Après pop :", soldes)

# Supprimer par valeur
soldes.remove(0.0)
print("Après remove(0.0) :", soldes)

# Trier
soldes.sort(reverse=True)     # tri en place (modifie la liste)
print("Trié décroissant :", soldes)"""),

code("""# List comprehension — la façon "Pythonique" de créer des listes filtrées/transformées
# Syntaxe : [expression   for element in liste   if condition]

soldes = [1200.0, -50.0, 0.0, 2300.75, -10.5, 150.0, 0.0, 890.0]

# Méthode classique (avec boucle)
positifs_boucle = []
for s in soldes:
    if s > 0:
        positifs_boucle.append(s)

# Méthode list comprehension (une ligne, plus rapide)
positifs_comp = [s for s in soldes if s > 0]

print("Méthode boucle      :", positifs_boucle)
print("Méthode comprehension:", positifs_comp)

# Transformation : convertir en euros avec 2 décimales
montants_formates = [f"{s:.2f} EUR" for s in soldes if s > 0]
print("Formatés :", montants_formates)"""),

code("""# Application Beobank : mapper les codes vers des libellés
codes_ecv = ["6", "4", "6", "1", "4", "6", "4", "4", "1", "6"]

mapping = {
    "1": "Ouvert",
    "2": "En attente",
    "3": "Suspendu",
    "4": "Clôturé",
    "5": "En résiliation",
    "6": "Résilié",
}

# Transformer les codes en libellés (list comprehension avec .get())
libelles = [mapping.get(c, "Inconnu") for c in codes_ecv]
print("Codes   :", codes_ecv)
print("Libellés:", libelles)

# Compter les actifs uniquement
actifs = [c for c in codes_ecv if c in ("1", "2", "3")]
print(f"\nContrats actifs : {len(actifs)} / {len(codes_ecv)}")"""),

md("""## Exercice 6.1 — Extraction de données d'une liste

**Contexte :** On vous remet un extrait brut de 20 références de contrats (comme si vous
lisiez la colonne REF_CTR_INN du CSV à la main). Certaines sont mal formatées.

**Tâches :**
1. Compter les références valides (commence par "002", longueur 13)
2. Lister les références invalides
3. Extraire les 5 premières références valides"""),

code("""# ============================================================
# EXERCICE 6.1 — Nettoyage de références de contrats
# ============================================================

refs_brutes = [
    "0029862201102", "0029912218433", "ERR001", "0029922113324",
    "0029872222935", "002988203", "0029882205525", "0029882205526",
    "0029882205527", None, "0029882205528", "0029882205529",
    "0029882205530", "MANQUANT", "0029882205531", "0029882205532",
    "0029882205533", "0029882205534", "", "0029882205535",
]

# Règle de validation : commence par "002" ET longueur exacte de 13 caractères
def est_valide(ref):
    if ref is None or ref == "":
        return False
    return ref.startswith("002") and len(ref) == 13

# TÂCHE 1 : séparer valides et invalides
valides   = [r for r in refs_brutes if est_valide(r)]
invalides = [r for r in refs_brutes if not est_valide(r)]

print(f"Total         : {len(refs_brutes)}")
print(f"Valides       : {len(valides)}")
print(f"Invalides     : {len(invalides)}")

# TÂCHE 2 : lister les invalides
print("\nRéférences invalides :")
for ref in invalides:
    print(f"  ├ {repr(ref)}")

# TÂCHE 3 : 5 premières valides
print("\n5 premières références valides :")
for ref in valides[:5]:
    print(f"  ├ {ref}")"""),

# ----- SECTION 7 : Tuples -----
md("""---
# Section 7 — Les Tuples

Un tuple est comme une liste, mais **immuable** : une fois créé, on ne peut plus le modifier.
Utilisez les tuples pour des données qui **ne doivent pas changer** : codes valides, coordonnées,
résultats de fonctions.

## 7.1 Créer et utiliser un tuple"""),

code("""# Créer un tuple (parenthèses ou simplement une virgule)
codes_valides = ("1", "2", "3", "4", "5", "6")   # codes ECV valides

# Accès identique aux listes
print("Premier code :", codes_valides[0])
print("Longueur     :", len(codes_valides))
print("'4' est dans les codes valides ?", "4" in codes_valides)

# Un tuple ne peut pas être modifié :
# codes_valides[0] = "X"  → TypeError: 'tuple' object does not support item assignment
# C'est fait exprès ! Cela protège vos données de référence."""),

code("""# Unpacking — décomposer un tuple en variables
# Très utile quand une fonction retourne plusieurs valeurs

# Exemple : une ligne de la table TIE
ligne_tie = (655010249, "2500003178544", "1", "1", "1980-01-25", "FR", "M")

# Unpacking : assigner chaque élément à une variable
idt_pi, num_tie, cod_typ, cod_sta, dat_nai, cod_lng, cod_sex = ligne_tie

print(f"ID client  : {idt_pi}")
print(f"Numéro tiers: {num_tie}")
print(f"Type       : {cod_typ}")
print(f"Naissance  : {dat_nai}")
print(f"Langue     : {cod_lng}")
print(f"Sexe       : {cod_sex}")"""),

code("""# Tuples dans les fonctions : retourner plusieurs valeurs
def analyser_contrat(cod_ecv_ctr, dat_ouv_ctr, dat_clo_ctr=None):
    '''
    Analyse un contrat et retourne ses informations enrichies.

    Returns:
        tuple: (libelle, categorie, duree_jours_ou_None)
    '''
    mapping = {
        "1": ("Ouvert",    "Actif"),
        "4": ("Clôturé",   "Inactif"),
        "6": ("Résilié",   "Inactif"),
    }
    libelle, categorie = mapping.get(cod_ecv_ctr, ("Inconnu", "Inconnu"))

    # Calculer la durée si les deux dates sont présentes
    duree = None
    if dat_ouv_ctr and dat_clo_ctr:
        from datetime import date
        d_ouv = date.fromisoformat(dat_ouv_ctr)
        d_clo = date.fromisoformat(dat_clo_ctr)
        duree = (d_clo - d_ouv).days

    return libelle, categorie, duree   # retourne un tuple


# Utilisation
lib, cat, dur = analyser_contrat("4", "2024-05-29", "2025-12-10")
print(f"Libellé   : {lib}")
print(f"Catégorie : {cat}")
if dur is not None:
    print(f"Durée     : {dur} jours ({dur//365} an(s) et {dur%365} jours)")
else:
    print("Durée     : N/A (contrat non clôturé)")"""),

# ----- SECTION 8 : Dictionnaires -----
md("""---
# Section 8 — Les Dictionnaires

Un dictionnaire stocke des **paires clé → valeur**.
C'est l'équivalent Python d'un enregistrement SAS ou d'une ligne de table avec accès par nom de colonne.

## 8.1 Créer et accéder à un dictionnaire"""),

code("""# Un contrat représenté comme dictionnaire (une "ligne" de la table CTR)
contrat = {
    "IDT_AC"      : 65500004701,
    "REF_CTR_INN" : "0029862201102",
    "DAT_OUV_CTR" : "2024-05-29",
    "COD_ECV_CTR" : "6",
    "DAT_CLO_CTR" : "2025-12-10",
    "COD_DEV"     : "EUR",
    "SLD_CTR"     : None,     # valeur manquante (. en SAS)
}

# Accéder à une valeur par sa clé
print("Référence :", contrat["REF_CTR_INN"])
print("Devise    :", contrat["COD_DEV"])
print("Solde     :", contrat["SLD_CTR"])

# Accès SÉCURISÉ avec .get() — retourne None si la clé n'existe pas
# (évite un KeyError si la colonne est absente)
print("Solde dispo :", contrat.get("SLD_DSP", "Non disponible"))
print("Type        :", contrat.get("COD_TYP", "Non disponible"))"""),

code("""# Modifier, ajouter, supprimer des clés
client = {
    "IDT_PI"      : 655010249,
    "COD_TYP_TIE" : "1",
    "COD_LNG_CTR" : "FR",
    "COD_SEX"     : "M",
}

# Ajouter une nouvelle clé
client["LIB_TYP"] = "Personne physique"
client["AGE"]     = 45

# Modifier une valeur existante
client["COD_LNG_CTR"] = "NL"   # mise à jour de la langue

# Supprimer une clé
del client["AGE"]

print("Client enrichi :")
for cle, valeur in client.items():
    print(f"  {cle:15s} : {valeur}")"""),

code("""# Parcourir un dictionnaire
mapping_ecv = {
    "1": "Ouvert",
    "2": "En attente",
    "3": "Suspendu",
    "4": "Clôturé",
    "5": "En résiliation",
    "6": "Résilié",
}

# Boucle sur les clés
print("Clés disponibles :", list(mapping_ecv.keys()))

# Boucle sur les valeurs
print("Libellés :", list(mapping_ecv.values()))

# Boucle sur les paires clé-valeur
print("\nMapping complet :")
for code, libelle in mapping_ecv.items():
    categorie = "Actif" if code in ("1","2","3") else "Inactif"
    print(f"  Code {code} → {libelle:22s} [{categorie}]")"""),

code("""# Dictionnaire de dictionnaires (structure imbriquée)
# Utile pour représenter un client avec toutes ses infos

clients = {
    655010249: {
        "nom"    : "JANSSENS",
        "prenom" : "Bart",
        "langue" : "FR",
        "nb_ctr" : 3,
    },
    655010248: {
        "nom"    : "VIRJXBF",
        "prenom" : "NTASEIJZR",
        "langue" : "FR",
        "nb_ctr" : 1,
    },
}

# Accéder aux informations d'un client spécifique
idt_pi = 655010249
print(f"Client {idt_pi} :")
print(f"  Nom    : {clients[idt_pi]['prenom']} {clients[idt_pi]['nom']}")
print(f"  Langue : {clients[idt_pi]['langue']}")
print(f"  Contrats : {clients[idt_pi]['nb_ctr']}")

# Vérifier si un client existe
idt_inexistant = 999999
if idt_inexistant in clients:
    print(f"\nClient {idt_inexistant} trouvé")
else:
    print(f"\nClient {idt_inexistant} non trouvé dans le dictionnaire")"""),

code("""# Dict comprehension — créer un dictionnaire depuis une liste
codes = ["1", "2", "3", "4", "5", "6"]
libelles = ["Ouvert", "En attente", "Suspendu", "Clôturé", "En résiliation", "Résilié"]

# Créer le mapping en une ligne
mapping = {code: lib for code, lib in zip(codes, libelles)}
print("Mapping créé :", mapping)

# Inverser un dictionnaire (valeur → clé)
mapping_inverse = {lib: code for code, lib in mapping.items()}
print("Inverse      :", mapping_inverse)"""),

md("""## Exercice 8.1 — Construire une fiche client enrichie

**Contexte :** Pour le rapport, vous devez présenter une fiche synthétique par client
avec des libellés lisibles (pas des codes).

**Tâche :** Créez la fonction `construire_fiche()` et testez-la sur les 3 clients fournis."""),

code("""# ============================================================
# EXERCICE 8.1 — Fiche client enrichie
# ============================================================

# Données brutes (comme lues depuis TIE + TIE_ADR)
clients_bruts = [
    {
        "IDT_PI": 655010249, "NUM_TIE": "2500003178544",
        "NOM_TIE": "JANSSENS", "PRN": "BART",
        "COD_TYP_TIE": "1", "COD_STA_FED": "1",
        "DAT_NAI": "1980-01-25", "COD_LNG_CTR": "FR", "COD_SEX": "M",
        "NOM_VIL": "BRUSSEL", "COD_PAY_ISO": "BE",
    },
    {
        "IDT_PI": 655010248, "NUM_TIE": "2500003178512",
        "NOM_TIE": "VIRJXBF", "PRN": "NTASEIJZR",
        "COD_TYP_TIE": "1", "COD_STA_FED": "3",
        "DAT_NAI": "2004-03-28", "COD_LNG_CTR": "FR", "COD_SEX": "M",
        "NOM_VIL": "BRUXELLES", "COD_PAY_ISO": "BE",
    },
    {
        "IDT_PI": 655010234, "NUM_TIE": "2500003178436",
        "NOM_TIE": "CEBBCACFZAAAFZTIER", "PRN": "",
        "COD_TYP_TIE": "2", "COD_STA_FED": "4",
        "DAT_NAI": None, "COD_LNG_CTR": "FR", "COD_SEX": "",
        "NOM_VIL": "BRUXELLES", "COD_PAY_ISO": "BE",
    },
]

# Dictionnaires de référence
LANGUES   = {"FR": "Français", "NL": "Néerlandais", "DE": "Allemand", "EN": "Anglais"}
TYPES     = {"1": "Personne physique", "2": "Personne morale"}
STATUTS   = {"1": "Actif", "2": "Inactif", "3": "Prospect", "4": "Résilié"}
CIVILITES = {"M": "Monsieur", "F": "Madame"}

def construire_fiche(client_brut):
    '''
    Construit une fiche client enrichie avec libellés lisibles.

    Args:
        client_brut (dict): ligne brute de TIE + TIE_ADR

    Returns:
        dict: fiche enrichie avec libellés
    '''
    nom    = client_brut["NOM_TIE"].strip().title() if client_brut["NOM_TIE"] else ""
    prenom = client_brut["PRN"].strip().title()      if client_brut["PRN"]     else ""

    if prenom:
        nom_complet = f"{prenom} {nom}"
    else:
        nom_complet = nom   # personne morale : pas de prénom

    return {
        "id"          : client_brut["IDT_PI"],
        "nom_complet" : nom_complet.strip(),
        "type"        : TYPES.get(client_brut["COD_TYP_TIE"], "Inconnu"),
        "statut"      : STATUTS.get(client_brut["COD_STA_FED"], "Inconnu"),
        "naissance"   : client_brut.get("DAT_NAI") or "Non renseignée",
        "langue"      : LANGUES.get(client_brut["COD_LNG_CTR"], client_brut["COD_LNG_CTR"]),
        "civilite"    : CIVILITES.get(client_brut["COD_SEX"], ""),
        "ville"       : client_brut["NOM_VIL"].strip().title() if client_brut["NOM_VIL"] else "",
        "pays"        : client_brut["COD_PAY_ISO"],
    }


# Tester sur les 3 clients
for client in clients_bruts:
    fiche = construire_fiche(client)
    print(f"\n{'='*50}")
    print(f"ID {fiche['id']} — {fiche['nom_complet']}")
    print(f"  Type    : {fiche['type']}")
    print(f"  Statut  : {fiche['statut']}")
    print(f"  Langue  : {fiche['langue']}")
    print(f"  Né(e)   : {fiche['naissance']}")
    print(f"  Ville   : {fiche['ville']}, {fiche['pays']}")"""),

# ----- SECTION 9 : Fonctions -----
md("""---
# Section 9 — Fonctions

Les fonctions permettent de **réutiliser du code** et de le rendre **lisible et testable**.
En SAS, vous utilisez des macros. En Python, les fonctions sont plus simples et plus puissantes.

## 9.1 Définir une fonction

```python
def nom_fonction(parametre1, parametre2="valeur_par_defaut"):
    # corps de la fonction
    return resultat
```

**Règles :**
1. Le mot-clé `def` démarre la définition
2. Le nom de la fonction suit les mêmes règles que les variables (minuscules, underscore)
3. Le `:` en fin de ligne est obligatoire
4. Le corps est indenté de 4 espaces
5. `return` envoie la valeur de résultat (sans `return`, la fonction retourne `None`)"""),

code("""# Fonction simple avec documentation
def formater_montant(montant, devise="EUR", decimales=2):
    '''
    Formate un montant monétaire en chaîne lisible.

    Args:
        montant   (float | None): Montant à formater.
        devise    (str)          : Code devise ISO 4217. Défaut : 'EUR'.
        decimales (int)          : Nombre de décimales. Défaut : 2.

    Returns:
        str: Montant formaté (ex: '1 250,75 EUR') ou 'N/A' si None.
    '''
    if montant is None:
        return "N/A"
    # Formater avec séparateurs et décimales
    formate = f"{montant:,.{decimales}f}"
    # Convertir la virgule anglaise en virgule française
    formate = formate.replace(",", " ").replace(".", ",")
    return f"{formate} {devise}"


# Tests
print(formater_montant(1250.75))
print(formater_montant(1250.75, "USD"))
print(formater_montant(None))
print(formater_montant(9999999.99, decimales=0))
print(formater_montant(0.0))"""),

code("""# Paramètres par défaut et paramètres nommés
def creer_ligne_rapport(ref_ctr, cod_ecv, dat_ouv, dat_clo=None, devise="EUR"):
    '''Crée une ligne formatée pour le rapport.'''
    STATUTS = {
        "1": "Ouvert", "2": "En attente", "3": "Suspendu",
        "4": "Clôturé", "5": "En résiliation", "6": "Résilié",
    }
    statut = STATUTS.get(cod_ecv, f"[{cod_ecv}]")
    fin = dat_clo if dat_clo else "en cours"
    return f"{ref_ctr} | {statut:22s} | {dat_ouv} → {fin} | {devise}"


# Appels avec différentes combinaisons de paramètres
print(creer_ligne_rapport("0029862201102", "6", "2024-05-29", "2025-12-10"))
print(creer_ligne_rapport("0029872222935", "4", "2025-01-07", "2025-01-07"))
print(creer_ligne_rapport("0029922113324", "4", "2022-01-12"))   # sans date de clôture

# Appel avec paramètres nommés (ordre libre)
print(creer_ligne_rapport(
    cod_ecv  = "1",
    ref_ctr  = "0029991234567",
    dat_ouv  = "2026-01-01",
    devise   = "USD",
))"""),

code("""# Fonctions qui appellent d'autres fonctions
def calculer_age(date_naissance_str):
    '''Calcule l'âge en années à partir d'une date ISO (YYYY-MM-DD).'''
    if not date_naissance_str:
        return None
    from datetime import date
    naissance = date.fromisoformat(date_naissance_str)
    aujourd_hui = date.today()
    age = aujourd_hui.year - naissance.year
    # Ajustement si l'anniversaire n'est pas encore passé cette année
    if (aujourd_hui.month, aujourd_hui.day) < (naissance.month, naissance.day):
        age -= 1
    return age

def segmenter_age(age):
    '''Retourne le segment d'âge d'un client.'''
    if age is None:
        return "Non renseigné"
    if age < 25:
        return "Jeune adulte (< 25 ans)"
    elif age < 40:
        return "Adulte (25-39 ans)"
    elif age < 60:
        return "Senior actif (40-59 ans)"
    else:
        return "Senior (60+ ans)"

def fiche_age(date_naissance_str):
    '''Retourne l'âge et le segment combinés.'''
    age = calculer_age(date_naissance_str)
    segment = segmenter_age(age)
    age_str = str(age) + " ans" if age is not None else "N/A"
    return age_str, segment


# Tests sur des dates réelles de TIE.csv
for dat_nai in ["1980-01-25", "2004-03-28", "2001-05-18", None]:
    age_str, segment = fiche_age(dat_nai)
    print(f"  {str(dat_nai):12s} → {age_str:8s} | {segment}")"""),

# ----- SECTION 10 : Lambda -----
md("""---
# Section 10 — Lambda expressions

Une **lambda** est une fonction anonyme en une seule ligne.
Syntaxe : `lambda paramètres : expression`

Utilisée principalement avec `sorted()`, `map()`, `filter()` et plus tard avec `pandas.apply()`."""),

code("""# Comparaison fonction normale vs lambda

# Fonction normale
def doubler(x):
    return x * 2

# Lambda équivalente
doubler_lambda = lambda x: x * 2

print(doubler(5))         # 10
print(doubler_lambda(5))  # 10

# Lambda avec plusieurs paramètres
calculer_taux = lambda montant, taux: montant * taux / 100
print(calculer_taux(1000, 5))   # 50.0

# Lambda avec condition (ternaire)
categorie_solde = lambda s: "Positif" if s > 0 else ("Nul" if s == 0 else "Négatif")
print(categorie_solde(1250.0))
print(categorie_solde(0.0))
print(categorie_solde(-50.0))"""),

code("""# Lambda avec sorted() — trier une liste de tuples

# Liste de (référence_contrat, date_ouverture)
contrats = [
    ("0029922113324", "2022-01-12"),
    ("0029862201102", "2024-05-29"),
    ("0029872222935", "2025-01-07"),
    ("0029912218433", "2024-08-07"),
    ("0029882034602", "2024-03-15"),
]

# Trier par date d'ouverture (2ème élément du tuple)
par_date = sorted(contrats, key=lambda ctr: ctr[1])
print("Triés par date d'ouverture :")
for ref, date in par_date:
    print(f"  {ref}  ouvert le {date}")

# Trier par référence
par_ref = sorted(contrats, key=lambda ctr: ctr[0])
print("\nTriés par référence :")
for ref, date in par_ref:
    print(f"  {ref}")"""),

code("""# Lambda avec map() et filter() — équivalent des list comprehensions
soldes = [1200.0, -50.0, 0.0, 2300.75, -10.5, 150.0]

# filter() : garder les éléments qui satisfont la condition
positifs = list(filter(lambda s: s > 0, soldes))
print("Positifs :", positifs)

# map() : appliquer une transformation à chaque élément
en_centimes = list(map(lambda s: int(s * 100), positifs))
print("En centimes :", en_centimes)

# Note : en pratique on utilise souvent les list comprehensions
# positifs     = [s for s in soldes if s > 0]
# en_centimes  = [int(s * 100) for s in positifs]
# Les deux approches sont correctes"""),

# ----- EXERCICES FINAUX -----
md("""---
# Exercices de fin de Jour 1

Ces exercices reprennent l'ensemble des notions vues aujourd'hui dans le contexte
du projet fil rouge Beobank.

---

## Exercice Final 1 — Pipeline de nettoyage CSV (simulation)

**Contexte :** Vous recevez une liste de lignes brutes représentant un extrait de la table CTR.
Chaque ligne est une chaîne de caractères avec des champs séparés par `;`.

**Tâche :** Parsez, nettoyez et transformez ces données en liste de dictionnaires."""),

code("""# ============================================================
# EXERCICE FINAL 1 — Pipeline de nettoyage CSV
# ============================================================

# Données brutes — extrait fictif de CTR.csv
lignes_csv = [
    "IDT_AC;REF_CTR_INN;DAT_OUV_CTR;COD_ECV_CTR;COD_DEV",
    "65500004701;0029862201102;2024-05-29;6;EUR",
    "65500006391;0029912218433;2024-08-07;6;EUR",
    "65500007774;0029922113324;2022-01-12;4;EUR",
    "65500008787;0029872222935;2025-01-07;4;EUR",
    ";;ERREUR;;",                        # ligne invalide
    "65500009999;0029882034602;2024-03-15;1;EUR",
]

MAPPING_ECV = {
    "1": ("Ouvert",    "Actif"),
    "2": ("En attente","Actif"),
    "3": ("Suspendu",  "Actif"),
    "4": ("Clôturé",   "Inactif"),
    "5": ("En résil.", "Inactif"),
    "6": ("Résilié",   "Inactif"),
}

def parser_ligne_ctr(ligne_str, colonnes):
    '''Parse une ligne CSV en dictionnaire nettoyé.'''
    valeurs = ligne_str.split(";")
    if len(valeurs) != len(colonnes):
        return None   # ligne invalide

    enregistrement = {}
    for col, val in zip(colonnes, valeurs):
        enregistrement[col] = val.strip() if val.strip() != "" else None

    # Valider que IDT_AC est un nombre
    if enregistrement.get("IDT_AC") is None:
        return None

    return enregistrement

def enrichir_contrat(ctr):
    '''Ajoute les libellés lisibles à un contrat parsé.'''
    if ctr is None:
        return None
    cod = ctr.get("COD_ECV_CTR", "")
    lib, cat = MAPPING_ECV.get(cod, ("Inconnu", "Inconnu"))
    ctr["LIB_ECV"]     = lib
    ctr["CATEGORIE"]   = cat
    return ctr

# Extraire l'en-tête
colonnes = lignes_csv[0].split(";")
print("Colonnes :", colonnes)
print()

# Traiter les lignes de données
contrats_propres = []
erreurs = 0
for ligne in lignes_csv[1:]:
    parsed  = parser_ligne_ctr(ligne, colonnes)
    enrichi = enrichir_contrat(parsed)
    if enrichi:
        contrats_propres.append(enrichi)
    else:
        erreurs += 1

print(f"Contrats parsés  : {len(contrats_propres)}")
print(f"Lignes ignorées  : {erreurs}")
print()
print(f"{'IDT_AC':>12}  {'REF_CTR_INN':15}  {'Statut':22}  {'Catégorie'}")
print("-" * 70)
for ctr in contrats_propres:
    print(f"{ctr['IDT_AC']:>12}  {ctr['REF_CTR_INN']:15}  {ctr['LIB_ECV']:22}  {ctr['CATEGORIE']}")"""),

md("""## Exercice Final 2 — Simulation d'un proc freq SAS

**Contexte :** En SAS vous utilisez `proc freq` pour obtenir des distributions.
Ici vous allez recréer cette logique en Python pur.

**Tâche :** Créez une fonction `freq_table()` générique qui accepte une liste et retourne
le tableau de fréquences trié, avec effectifs et pourcentages."""),

code("""# ============================================================
# EXERCICE FINAL 2 — Tableau de fréquences (proc freq Python)
# ============================================================

def freq_table(valeurs, titre="Fréquence", top_n=None):
    '''
    Calcule et affiche un tableau de fréquences.

    Args:
        valeurs (list): Valeurs à analyser (None autorisé).
        titre   (str) : Titre du tableau.
        top_n   (int) : Si renseigné, afficher seulement les top_n valeurs.

    Returns:
        dict: {valeur: (effectif, pourcentage)}
    '''
    total = len(valeurs)

    # Compter les occurrences
    comptage = {}
    for val in valeurs:
        cle = val if val is not None else "(manquant)"
        comptage[cle] = comptage.get(cle, 0) + 1

    # Trier par effectif décroissant
    items_tries = sorted(comptage.items(), key=lambda x: -x[1])
    if top_n:
        items_tries = items_tries[:top_n]

    # Afficher
    print(f"\n{'='*55}")
    print(f"  {titre}")
    print(f"  Base : {total:,} observations")
    print(f"{'='*55}")
    print(f"  {'Valeur':20s}  {'Effectif':>9}  {'%':>7}  {'Cum %':>7}")
    print(f"  {'-'*47}")
    cumul = 0
    for val, nb in items_tries:
        pct  = nb / total
        cumul += pct
        print(f"  {str(val):20s}  {nb:>9,}  {pct:>7.1%}  {cumul:>7.1%}")
    print(f"  {'-'*47}")
    print(f"  {'TOTAL':20s}  {total:>9,}  {'100.0%':>7}")

    return {val: (nb, nb/total) for val, nb in comptage.items()}


# Données réelles de TIE.csv
cod_typ_tie = ["1","1","2","1","1","1","1","2","1","1","1","1","1","1","1",
               "1","1","1","1","2","1","1","1","1","1","1","1","1","1","1"]
cod_sex_tie = ["M","M","","M","M","M","","M","M","M","F","M","M","M","M",
               "","M","M","","M","M","F","M","","M","M","M","M","M",""]
cod_lng_tie = ["FR","FR","FR","FR","FR","FR","FR","FR","FR","FR","FR","NL",
               "FR","FR","FR","FR","FR","NL","FR","FR","FR","FR","FR","FR","FR","FR"]

freq_table(cod_typ_tie, "COD_TYP_TIE — Type de tiers")
freq_table(cod_sex_tie, "COD_SEX — Genre des clients")
freq_table(cod_lng_tie, "COD_LNG_CTR — Langue")"""),

md("""## Exercice Final 3 — Logique SAS → Python

**Contexte :** Voici un programme SAS qui prépare un tableau de bord.
Votre mission est de le réécrire entièrement en Python.

```sas
data tableau_bord;
    set CTR;

    /* Calcul du statut */
    if COD_ECV_CTR in ('1','2','3') then do;
        CATEGORIE = 'Actif';
        SCORE_ACT = 1;
    end;
    else if COD_ECV_CTR in ('4','5','6') then do;
        CATEGORIE = 'Inactif';
        SCORE_ACT = 0;
    end;
    else do;
        CATEGORIE = 'Inconnu';
        SCORE_ACT = .;
    end;

    /* Année d'ouverture */
    ANNEE_OUV = year(input(DAT_OUV_CTR, yymmdd10.));

run;

proc print data=tableau_bord (obs=5); run;
proc freq data=tableau_bord; tables CATEGORIE ANNEE_OUV; run;
```"""),

code("""# ============================================================
# EXERCICE FINAL 3 — Réécriture SAS → Python
# ============================================================

# Données simulées (extrait CTR.csv)
contrats_raw = [
    {"REF_CTR_INN": "0029862201102", "COD_ECV_CTR": "6", "DAT_OUV_CTR": "2024-05-29"},
    {"REF_CTR_INN": "0029912218433", "COD_ECV_CTR": "6", "DAT_OUV_CTR": "2024-08-07"},
    {"REF_CTR_INN": "0029922113324", "COD_ECV_CTR": "4", "DAT_OUV_CTR": "2022-01-12"},
    {"REF_CTR_INN": "0029872222935", "COD_ECV_CTR": "4", "DAT_OUV_CTR": "2025-01-07"},
    {"REF_CTR_INN": "0029882034602", "COD_ECV_CTR": "1", "DAT_OUV_CTR": "2024-03-15"},
    {"REF_CTR_INN": "0029991234567", "COD_ECV_CTR": "2", "DAT_OUV_CTR": "2023-11-01"},
    {"REF_CTR_INN": "0029882205525", "COD_ECV_CTR": "4", "DAT_OUV_CTR": "2021-06-15"},
    {"REF_CTR_INN": "0029882205526", "COD_ECV_CTR": "4", "DAT_OUV_CTR": "2020-03-10"},
    {"REF_CTR_INN": "0029882205527", "COD_ECV_CTR": "6", "DAT_OUV_CTR": "2023-07-22"},
    {"REF_CTR_INN": "0029882205528", "COD_ECV_CTR": "3", "DAT_OUV_CTR": "2025-05-01"},
]

# ÉTAPE 1 : Enrichissement (équivalent du DATA step)
tableau_bord = []
for ctr in contrats_raw:
    cod = ctr["COD_ECV_CTR"]

    # Calcul CATEGORIE et SCORE_ACT
    if cod in ("1", "2", "3"):
        categorie  = "Actif"
        score_act  = 1
    elif cod in ("4", "5", "6"):
        categorie  = "Inactif"
        score_act  = 0
    else:
        categorie  = "Inconnu"
        score_act  = None

    # Extraction de l'année d'ouverture
    annee_ouv = int(ctr["DAT_OUV_CTR"][:4])  # "2024-05-29" → 2024

    tableau_bord.append({
        **ctr,               # copie tous les champs existants
        "CATEGORIE": categorie,
        "SCORE_ACT": score_act,
        "ANNEE_OUV": annee_ouv,
    })

# ÉTAPE 2 : proc print (obs=5)
print("=== 5 premiers enregistrements ===")
print(f"{'REF_CTR_INN':15}  {'COD_ECV':>7}  {'CATEGORIE':10}  {'SCORE':>6}  {'ANNEE':>6}")
print("-" * 55)
for ctr in tableau_bord[:5]:
    score = str(ctr['SCORE_ACT']) if ctr['SCORE_ACT'] is not None else "."
    print(f"{ctr['REF_CTR_INN']:15}  {ctr['COD_ECV_CTR']:>7}  {ctr['CATEGORIE']:10}  {score:>6}  {ctr['ANNEE_OUV']:>6}")

# ÉTAPE 3 : proc freq (CATEGORIE)
print("\n=== Distribution CATEGORIE ===")
freq_table([c["CATEGORIE"] for c in tableau_bord], "CATEGORIE")

# ÉTAPE 4 : proc freq (ANNEE_OUV)
freq_table([c["ANNEE_OUV"] for c in tableau_bord], "ANNEE_OUV — Année d'ouverture")"""),

md("""---
# Résumé du Jour 1

Vous maîtrisez maintenant les **fondations de Python** pour l'analyse de données.

| Notion | Équivalent SAS | Utilisation Beobank |
|--------|---------------|---------------------|
| Variables et types | `length`, `format` | Codes, soldes, dates |
| Chaînes et f-strings | `cat()`, `put` | Nettoyage NOM_TIE, libellés |
| Conditions `if/elif/else` | `if ... then ... else` | Classifier COD_ECV_CTR |
| Boucles `for` | `DATA _null_; set ds;` | Itérer sur des contrats |
| Listes | `array` | Colonnes, codes valides |
| Dictionnaires | — | Mappings code → libellé |
| Fonctions | `%macro` | Réutiliser des traitements |
| Lambda | — | Transformations rapides |

---

**Demain (Jour 2) :** Vous chargerez les **vraies** tables Beobank avec Pandas et
vous ferez toutes ces opérations sur 200 contrats et 1 260 transactions en quelques lignes !"""),

] # fin j1

path = os.path.join(OUTPUT_DIR, "Jour1_Fondamentaux_Python.ipynb")
with open(path, "w", encoding="utf-8") as f:
    json.dump(notebook(j1), f, ensure_ascii=False, indent=1)
print(f"Jour 1 créé : {os.path.getsize(path)//1024} Ko — {len(j1)} cellules")
