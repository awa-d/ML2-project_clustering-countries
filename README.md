# Sigma Pulse - Clustering de pays

## Vue d’ensemble

SigmaPulse est un projet académique de Machine Learning consacré à l’optimisation de l’allocation de l’aide humanitaire à travers une approche analytique, explicable et orientée données.

Dans un contexte mondial marqué par l’intensification des crises humanitaires et la limitation des ressources financières, le projet vise à construire un cadre d’analyse robuste permettant d’identifier des groupes de pays présentant des vulnérabilités similaires sur les plans économique, sanitaire, social et sécuritaire.

Le projet combine :

* Des indicateurs macro-économiques
* Des indicateurs de santé publique
* Des indicateurs de vulnérabilité sociale
* Des indicateurs de fragilité étatique et sécuritaire
* Des techniques de Machine Learning non supervisé

L’objectif est de proposer une stratégie d’allocation des ressources humanitaires plus transparente, cohérente et fondée sur les données.

---

# Vision du projet

> « L’aide humanitaire de demain ne peut plus reposer uniquement sur des intuitions géopolitiques. Avec des ressources limitées, chaque décision d’allocation compte. SigmaPulse mobilise la puissance du Machine Learning pour transformer des indicateurs macro-économiques et humanitaires complexes en une stratégie d’allocation rigoureuse, éthique et data-driven. »
>
> — Équipe SigmaPulse

---

# Stack Technique

## Langages

* Python 3.11+
* SQL
* Markdown

## Data Science & Machine Learning

* pandas
* numpy
* scikit-learn
* scipy
* statsmodels
* imbalanced-learn

## Visualisation

* matplotlib
* seaborn
* plotly

## Environnement de développement

* Jupyter Notebook
* Google Colab
* VS Code

## Versioning

* Git
* GitHub

---

# Architecture du dépôt

```text
SigmaPulse/
│
├── data/
│   ├── raw/                  # Jeux de données bruts
│   └── processed/             # Bases finales prêtes pour le ML
│
├── notebooks/
│   ├── P0_init-merge.ipynb
│   ├── P1_EDA.ipynb
│   ├── P2_modeling.ipynb
│   └── P5_interpretation.ipynb
│
├── outputs/
│   ├── figures/
│   ├── tables/
│   ├── reports/
│   └── datasets_agreges/
│
├── src/
│   ├── preprocessing/
│   ├── feature_engineering/
│   ├── modeling/
│   ├── visualization/
│   └── utils/
│
├── docs/
│   ├── methodology/
│   ├── references/
│   └── presentations/
│
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

---

# Sources de données

Le projet mobilise plusieurs bases internationales relatives au développement, à la santé publique et à la fragilité des États.

## Sources principales

* World Bank Open Data
* Fragile States Index (FSI)
* WDI
* WHO
* Kaggle

## Data Augmentation

Dans le cadre académique du projet, une base initiale nous a été fournie : https://www.kaggle.com/datasets/rohan0301/unsupervised-learning-on-country-data/data.

Cependant, afin d’enrichir la qualité analytique et la robustesse des modèles, l’équipe a procédé à une importante phase de data augmentation.

Plusieurs bases complémentaires ont été collectées, harmonisées, nettoyées et fusionnées afin d’améliorer :

* La couverture géographique des pays
* La diversité des indicateurs
* La représentation des vulnérabilités humanitaires
* La robustesse du clustering
* La richesse de l’analyse socio-économique

---

# Pipeline Machine Learning

## 1. Fusion et harmonisation des données

* Standardisation des noms de pays
* Harmonisation des codes ISO
* Fusion multi-sources
* Alignement des variables

## 2. Nettoyage des données

* Gestion des valeurs manquantes
* Sélection des variables
* Transformation des variables
* Transformations logarithmiques

## 3. Analyse exploratoire

* Analyse des distributions
* Matrice de corrélation
* Détection des valeurs extrêmes
* Profilage des pays

## 4. Clustering

Méthodes de Machine Learning non supervisé :

* K-Means
* Clustering hiérarchique
* ACP / PCA pour la visualisation

## 5. Interprétation

* Profilage des clusters
* Cartographie des vulnérabilités
* Recommandations stratégiques d’allocation

---

# Variables retenues

## Santé

* Espérance de vie
* Mortalité infantile
* Mortalité maternelle
* Prévalence du VIH
* Couverture vaccinale DPT
* Médecins pour 1000 habitants

## Économie

* PIB par habitant
* Inflation

## Vulnérabilité sociale

* Sous-alimentation
* Scolarisation

## Sécurité et fragilité

* Security apparatus
* Group grievance
* Refugees and IDPs
* External intervention

---

# Équipe Projet

## Équipe SigmaPulse

* [Awa Diaw](https://github.com/awa-d)

* [Moussa Dieme](https://github.com/Mafieuu)

* [Ndeye Ramatoulaye Ndoye Fall](https://github.com/Vimdie)

* [Hildegarde Edima Biyenda](https://github.com/HildaEDIMA)

---

# Supervision académique

Projet réalisé sous la supervision de : [Mously Diaw](https://github.com/mouslydiaw), Senior Machine Learning & Data Science Supervisor

---

# Notes méthodologiques

## Gestion des valeurs aberrantes

Certaines variables présentent des valeurs extrêmes visibles à travers les boxplots.

Ces valeurs n’ont volontairement pas été imputées ni supprimées car elles traduisent des écarts réels de développement entre les pays.

Dans le cadre d’une analyse humanitaire mondiale, ces différences structurelles constituent précisément l’information que le modèle cherche à capturer.

Une suppression artificielle des extrêmes réduirait donc la représentativité des vulnérabilités observées.

---

# Reproductibilité

## Cloner le dépôt

```bash
git clone https://github.com/Vimdie/clustering_countries.git
```

## Installer les dépendances

```bash
pip install -r requirements.txt
```

## Exécuter les notebooks

Utiliser :

* Jupyter Notebook
* VS Code
* Google Colab

---

# Perspectives futures

* Intégration d’indicateurs humanitaires en temps réel
* Prévision temporelle des risques
* Explainable AI (XAI)
* Cartographie géospatiale des vulnérabilités
* Système dynamique d’allocation de ressources

---

# Licence

Ce dépôt s’inscrit dans le cadre d’un projet académique.

Son utilisation est autorisée à des fins éducatives et de recherche.

*SigmaPulse: Calculated compassion, where Data Science meets human dignity.*
