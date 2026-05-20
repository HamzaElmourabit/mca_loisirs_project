# 📦 Livrables Finaux — Projet MCA (ACM)

## Structure du projet

```
mca_loisirs_project/
├── mca_loisirs.ipynb          ✨ NOTEBOOK PRINCIPAL (à utiliser)
├── mca_loisirs.py             Script Python autonome (optionnel)
├── requirements.txt            Dépendances Python
├── README.md                   Instructions d'utilisation
├── DELIVERABLES.md            Ce fichier
└── mca_results/                Dossier de sortie (créé à l'exécution)
    ├── row_coordinates.csv
    ├── column_coordinates.csv
    └── inertia.csv
```

---

## 📋 Contenu des fichiers

### 1. **mca_loisirs.ipynb** ⭐ (RECOMMANDÉ)

**Notebook Jupyter interactif** comprenant :

#### Structure du notebook (14 sections)
1. **Installation des dépendances** : Installation auto des packages requis
2. **Imports et configuration** : Configuration matplotlib et seaborn
3. **Chargement des données** : Lecture du CSV et exploration
4. **Prétraitement** : Conversion en catégories, gestion des manquants
5. **Configuration des variables suppl.** : Définition de `quali.sup` et `quanti.sup`
6. **Réalisation de l'ACM** : Calcul MCA via `prince`
7. **Graphique des inerties** : Eigenvalues (inertie par dimension)
8. **Individus (axes 1 & 2)** : Scatter plot coloré par groupe
9. **Individus (axes 2 & 3)** : Alternative avec autres axes
10. **Catégories** : Plan factoriel des modalités avec labels ajustés
11. **Ellipses de confiance** : Ellipses par modalité d'une variable
12. **Corrélations quanti.sup** : Projections de la variable quantitative
13. **Résumé statistique** : Tableau de synthèse
14. **Export des résultats** : Sauvegarde en CSV

#### Caractéristiques principales
- ✅ Installation automatique des dépendances
- ✅ Paramètres facilement modifiables (`QUALI_SUP_INDICES`, `QUANTI_SUP_INDEX`)
- ✅ Exécution progressive et interactive
- ✅ Visualisations inline (figures PNG intégrées)
- ✅ Documentation complète intégrée
- ✅ Export des coordonnées et inerties en CSV
- ✅ Gestion des valeurs manquantes
- ✅ Résumés statistiques détaillés

**Commande d'exécution :**
```powershell
jupyter notebook mca_loisirs.ipynb
```

---

### 2. **mca_loisirs.py**

Script Python autonome pour automatisation / batch processing.

#### Options de ligne de commande
```
--csv              (requis) Chemin du fichier CSV
--sep              (défaut: ';') Séparateur CSV
--encoding         (défaut: 'utf-8') Encodage du fichier
--quali-sup        Indices 1-based des variables quali suppl.
--quanti-sup       Indice 1-base de la variable quanti suppl.
--out-dir          (défaut: 'plots') Dossier de sortie
```

#### Exemple d'utilisation
```powershell
python mca_loisirs.py --csv AnaDo_JeuDonnees_Loisirs.csv \
  --quali-sup 19 20 21 22 --quanti-sup 23 --out-dir my_plots
```

#### Figures générées
- `mca_eigenvalues.png` — Inertie expliquée par dimension
- `mca_individuals_dim1_dim2.png` — Individus axes 1 & 2
- `mca_individuals_dim2_dim3.png` — Individus axes 2 & 3
- `mca_categories_dim1_dim2.png` — Catégories plan factoriel
- `mca_ellipses.png` — Ellipses de confiance par modalité
- `mca_quanti_sup_corrs.png` — Corrélations avec variable quanti suppl.

---

### 3. **requirements.txt**

Dépendances Python (version >= spécifiée) :
- `pandas` — Manipulation de données
- `numpy` — Calculs numériques
- `matplotlib` — Visualisations
- `seaborn` — Graphiques statistiques
- `prince` — Analyse MCA
- `scikit-learn` — Machine learning utilities
- `adjustText` — Ajustement automatique des labels
- `jupyter` — Environnement notebook

---

### 4. **README.md**

Guide complet d'utilisation incluant :
- Installation de l'environnement virtuel
- Instructions pour notebook et script
- Explication des paramètres
- Description des résultats
- Notes techniques

---

## 🚀 Démarrage rapide

### Étape 1 : Installation
```powershell
# Créer environnement virtuel
python -m venv .venv

# Activer
.\.venv\Scripts\Activate.ps1

# Installer dépendances
pip install -r requirements.txt
```

### Étape 2 : Lancer le notebook
```powershell
jupyter notebook mca_loisirs.ipynb
```

### Étape 3 : Adapter les paramètres
Dans la cellule 5 du notebook, modifiez si nécessaire :
```python
QUALI_SUP_INDICES = [19, 20, 21, 22]  # À adapter à votre dataset
QUANTI_SUP_INDEX = 23                  # À adapter à votre dataset
```

### Étape 4 : Exécuter l'analyse
- Démarrer depuis la cellule 1 et exécuter progressivement
- Ajuster le chemin du CSV en cellule 3 si nécessaire
- Toutes les figures s'affichent inline
- Les résultats sont exportés optionnellement en CSV

---

## 📊 Analyses proposées

### 1. Analyse descriptive
- Dimensions du dataset
- Types de variables
- Détection des valeurs manquantes

### 2. Analyse MCA
- Calcul des axes factoriels
- Inertie expliquée par dimension
- Contribution des variables

### 3. Visualisations
- Nuages de points des individus
- Plans factoriels des catégories
- Ellipses de confiance par groupe
- Graphes des inerties

### 4. Variables supplémentaires
- Projections qualitatives suppl.
- Corrélations quantitatives suppl.

### 5. Export des résultats
- Coordonnées des individus (CSV)
- Coordonnées des catégories (CSV)
- Inerties et valeurs propres (CSV)

---

## 🔧 Adaptation à votre dataset

### Si votre dataset a une structure différente

1. **Identifier les colonnes** :
   - Colonnes qualitatives actives (pour MCA)
   - Colonnes qualitatives supplémentaires
   - Colonne quantitative supplémentaire (si applicable)

2. **Dans le notebook, cellule 5** :
   ```python
   QUALI_SUP_INDICES = [col1, col2, col3, ...]  # Indices 1-based
   QUANTI_SUP_INDEX = 999  # Indice 1-base (ou None)
   ```

3. **Vérifier le chemin du CSV (cellule 3)** :
   ```python
   CSV_PATH = r"C:\chemin\vers\votre\fichier.csv"
   ```

4. **Ajuster le séparateur si nécessaire** (cellule 3) :
   ```python
   df = pd.read_csv(CSV_PATH, sep=',', ...)  # ou sep='\t', etc.
   ```

---

## 📈 Interprétation des résultats

### Eigenvalues
- Montre l'inertie (variance) expliquée par chaque dimension
- Les premiers axes capturent le plus de variance
- Cumulatif indique la qualité de la réduction dimensionnelle

### Plan factoriel (individus)
- **Proximité** = similarité entre individus
- **Distance à l'origine** = contribution à l'inertie
- **Coloration** = groupement par variable supplémentaire

### Plan factoriel (catégories)
- **Position** = opposition entre modalités
- **Distance à l'origine** = force de l'association
- **Clusters** = groupes de catégories connexes

### Ellipses
- **Centre** = barycenter des individus du groupe
- **Largeur/hauteur** = dispersion du groupe
- **Chevauchement** = similarité entre groupes

---

## ✅ Checklist de livrables

- [x] Notebook Jupyter complet (`mca_loisirs.ipynb`)
- [x] Script Python autonome (`mca_loisirs.py`)
- [x] Fichier de dépendances (`requirements.txt`)
- [x] Documentation README
- [x] Ce fichier DELIVERABLES.md
- [x] 14 cellules notebook (installation → export)
- [x] Support pour quali.sup et quanti.sup
- [x] Gestion automatique des manquants
- [x] 6 figures principales
- [x] Export CSV des résultats

---

## 📞 Support & Troubleshooting

### Le notebook ne démarre pas
```powershell
pip install jupyter --upgrade
jupyter notebook mca_loisirs.ipynb
```

### Erreur "module prince not found"
```powershell
pip install prince
# Puis relancer le notebook
```

### Problème de chemin CSV
- Vérifier l'encodage (UTF-8 par défaut)
- Vérifier le séparateur (`;` par défaut)
- Utiliser le chemin absolu complet

### Labels qui se chevauchent
- Le notebook utilise `adjustText` pour auto-ajuster
- Si encore problématique, augmenter la taille de figure

---

**Version finale : Mai 2026**
**Dataset : AnaDo_JeuDonnees_Loisirs.csv**
**Basé sur : Script R FactoMineR fourni**
