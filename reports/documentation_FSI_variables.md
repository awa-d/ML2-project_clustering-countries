# Documentation — Fragile States Index (FSI)
## Variables, Méthodologie & Usage en Machine Learning

> **Source :** Fund for Peace (FFP) — [fragilestatesindex.org](https://fragilestatesindex.org)  
> **Cadre analytique :** CAST — Conflict Assessment System Tool  
> **Couverture :** 178 pays · Annuel depuis 2006 · Période cible : 2015

---

## 1. Structure générale du dataset

| Variable | Type | Description courte |
|---|---|---|
| `Country` | Texte | Nom du pays (clé de jointure) |
| `Year` | Entier | Année de publication du rapport |
| `Rank` | Entier | Classement mondial (1 = le plus fragile) |
| `Total` | Flottant | Score composite total · **Échelle : 0 – 120** |
| `C1` à `X1` | Flottant | 12 indicateurs thématiques · **Échelle : 0 – 10 chacun** |

> **Attention au timing des données :** Le rapport publié en année N contient les données collectées durant l'année N-1. Ex : FSI 2015 = données observées en 2014.

---

## 2. Règle de lecture universelle

```
Score = 0    →  Situation idéale, aucune pression détectée  (pays le plus stable)
Score = 10   →  Pression maximale, état en situation critique (pays le plus fragile)
Score Total = somme des 12 indicateurs  →  min 0 / max 120
```

**Catégories de classification FSI (basées sur le Total) :**

| Catégorie | Fourchette Total | Couleur |
|---|---|---|
| Very High Alert | 100–120 | Rouge foncé |
| High Alert | 90–100 | Rouge |
| Alert | 80–90 | Orange |
| High Warning | 70–80 | Jaune orangé |
| Warning | 60–70 | Jaune |
| Stable | 40–60 | Vert clair |
| More Stable | 20–40 | Vert |
| Sustainable | 0–20 | Vert foncé |

---

## 3. Description détaillée des 12 indicateurs

### DIMENSION COHÉSION (C) — *Solidité interne de l'État*

---

#### `C1: Security Apparatus` — Appareil sécuritaire
**Ce que ça mesure :** La capacité de l'État à maintenir un monopole légitime de la force et à assurer la sécurité intérieure.

**Sous-indicateurs pris en compte :**
- Intensité des conflits armés internes (batailles, rébellions, mutineries)
- Présence de groupes armés non-étatiques rivaux
- Risque de coup d'État militaire
- Violations des droits humains par les forces de sécurité
- Activités terroristes et attentats
- Criminalité organisée et violente

**Ordre de grandeur typique :**
- `< 3.0` : Pays stables (Europe de l'Ouest, Canada)
- `5.0 – 7.0` : Tensions modérées (Colombie 2013, Côte d'Ivoire 2013)
- `> 8.5` : États en guerre (Syrie, Soudan du Sud, Afghanistan)

**Pertinence humanitaire :** ★★★★★ — Indicateur direct de danger pour les opérations de terrain.

---

#### `C2: Factionalized Elites` — Fragmentation des élites
**Ce que ça mesure :** Le degré de division au sein des élites politiques, économiques et militaires, et leurs effets sur la gouvernance.

**Sous-indicateurs pris en compte :**
- Fragmentation institutionnelle selon des lignes ethniques, claniques ou religieuses
- Rhétorique nationaliste ou xénophobe des dirigeants
- Blocages politiques et crises de gouvernement
- Transitions de pouvoir conflictuelles
- Réseaux de patronage et corruption au sommet
- Absence de leadership représentatif de tous les citoyens

**Ordre de grandeur typique :**
- `< 3.5` : Démocraties consolidées
- `5.0 – 7.5` : Systèmes semi-autoritaires
- `> 8.0` : États en guerre civile ou dictatures fragmentées

**Pertinence humanitaire :** ★★★★☆ — Un score élevé prédit des difficultés d'accès humanitaire et de coordination.

---

#### `C3: Group Grievance` — Griefs intergroupe
**Ce que ça mesure :** L'intensité des tensions et discriminations perçues entre groupes sociaux (ethniques, religieux, régionaux).

**Sous-indicateurs pris en compte :**
- Historique de violence ou de vengeance intergroupe
- Discriminations dans l'accès aux services publics selon le groupe
- Exclusion politique de minorités
- Discours de haine et incitation à la violence
- Mémoire collective des injustices (génocides, expropriations)

**Ordre de grandeur typique :**
- `< 2.5` : Sociétés très homogènes ou bien intégrées
- `4.0 – 7.0` : Tensions latentes (ex : Inde, Kenya, Bolivie)
- `> 8.5` : Conflits actifs à caractère identitaire (Syrie, Myanmar)

**Pertinence humanitaire :** ★★★★☆ — Détermine quelles populations sont les plus vulnérables et marginalisées.

---

### DIMENSION ÉCONOMIQUE (E) — *Viabilité et équité économique*

---

#### `E1: Economy` — Déclin économique
**Ce que ça mesure :** La trajectoire économique globale du pays et sa capacité à assurer les conditions de vie minimales.

**Sous-indicateurs pris en compte :**
- Taux de croissance du PIB (trajectoire)
- Taux de chômage et emploi informel
- Inflation et dépréciation monétaire
- Niveau d'endettement public
- Dépendance aux exportations primaires (matières premières)
- Accès au crédit et activité du secteur privé

**Ordre de grandeur typique :**
- `< 3.0` : Économies diversifiées et stables
- `5.0 – 7.0` : Économies fragiles ou en transition
- `> 8.0` : Effondrements économiques (Zimbabwe 2008, Venezuela 2017)

**Pertinence humanitaire :** ★★★★☆ — Proxy de la pauvreté et des besoins en aide alimentaire.

---

#### `E2: Economic Inequality` — Inégalités économiques
**Ce que ça mesure :** L'inégalité de distribution des richesses et des opportunités économiques au sein d'un pays.

**Sous-indicateurs pris en compte :**
- Coefficient de Gini (inégalités de revenus)
- Inégalités entre groupes (ethniques, régionaux, de genre)
- Accès différentiel à l'éducation, la santé, l'emploi
- Concentration de la propriété foncière
- Contrastes urbain/rural

**Ordre de grandeur typique :**
- `< 4.0` : Pays nordiques, certains pays d'Europe de l'Est
- `5.0 – 7.0` : Pays d'Afrique subsaharienne, Amérique latine
- `> 8.0` : Inégalités extrêmes (Afrique du Sud, certains États du Golfe)

**Pertinence humanitaire :** ★★★★★ — Essentiel pour cibler les populations les plus défavorisées au sein d'un même pays.

---

#### `E3: Human Flight and Brain Drain` — Fuite des cerveaux
**Ce que ça mesure :** L'émigration des élites économiques et intellectuelles, signal d'une perte de confiance dans l'avenir du pays.

**Sous-indicateurs pris en compte :**
- Émigration des professionnels qualifiés (médecins, ingénieurs, enseignants)
- Transferts de capitaux à l'étranger (flight capital)
- Fuite des entrepreneurs et investisseurs
- Nombre d'étudiants ne revenant pas après leurs études

**Ordre de grandeur typique :**
- `< 3.0` : Pays attractifs (immigration nette)
- `4.0 – 6.5` : Émigration modérée
- `> 7.5` : Exode massif des compétences (Haïti, Érythrée, Syrie)

**Pertinence humanitaire :** ★★★☆☆ — Indicateur de fragilité à moyen terme, moins direct pour l'urgence.

---

### DIMENSION POLITIQUE (P) — *Légitimité et capacité de l'État*

---

#### `P1: State Legitimacy` — Légitimité de l'État
**Ce que ça mesure :** Le niveau de confiance et de soutien de la population envers ses institutions politiques.

**Sous-indicateurs pris en compte :**
- Qualité et équité des processus électoraux
- Niveau de corruption perçue
- Confiance dans le système judiciaire
- Représentativité politique des minorités
- Présence de groupes armés contestant l'autorité de l'État
- Protestations populaires et mouvements insurrectionnels

**Ordre de grandeur typique :**
- `< 3.0` : Démocraties consolidées avec forte confiance institutionnelle
- `5.0 – 7.5` : États autoritaires ou en transition
- `> 8.5` : États faillis ou occupés

**Pertinence humanitaire :** ★★★★☆ — Un État illégitime ne peut pas être partenaire fiable dans la distribution d'aide.

---

#### `P2: Public Services` — Services publics
**Ce que ça mesure :** La capacité de l'État à fournir des services essentiels à sa population.

**Sous-indicateurs pris en compte :**
- Accès à l'eau potable et assainissement
- Couverture sanitaire (hôpitaux, médecins pour 1 000 habitants)
- Taux d'alphabétisation et accès à l'éducation
- Infrastructures de transport et communication
- Collecte des ordures / services municipaux
- Fourniture d'électricité

**Ordre de grandeur typique :**
- `< 2.0` : Standards OCDE élevés
- `4.0 – 7.0` : Services partiels ou inégalement distribués
- `> 8.0` : Effondrement des services (Haïti, Yémen, RDC)

**Pertinence humanitaire :** ★★★★★ — Mesure directe des besoins humanitaires en services essentiels.

---

#### `P3: Human Rights` — Droits de l'homme
**Ce que ça mesure :** Le degré de respect des droits humains fondamentaux et de l'état de droit.

**Sous-indicateurs pris en compte :**
- Liberté de presse et d'expression
- Détentions arbitraires et prisonniers politiques
- Torture et traitements inhumains
- Égalité devant la loi (genre, minorités)
- Violence contre les civils par forces étatiques
- Impunité pour crimes graves

**Ordre de grandeur typique :**
- `< 2.0` : Démocraties libérales
- `5.0 – 7.5` : Régimes semi-autoritaires
- `> 8.5` : Régimes totalitaires ou en guerre civile

**Pertinence humanitaire :** ★★★★☆ — Indicateur de la protection des populations civiles ; essentiel pour le droit international humanitaire.

---

### DIMENSION SOCIALE (S) — *Pressions démographiques et mouvements de population*

---

#### `S1: Demographic Pressures` — Pressions démographiques
**Ce que ça mesure :** Les tensions liées à la croissance démographique, aux ressources naturelles et aux catastrophes environnementales.

**Sous-indicateurs pris en compte :**
- Pression sur les ressources naturelles (eau, terres arables, forêts)
- Croissance démographique vs. capacité d'absorption
- Malnutrition et insécurité alimentaire chronique
- Risques de catastrophes naturelles (sécheresses, inondations)
- Mortalité infantile et espérance de vie
- Maladies et pandémies

**Ordre de grandeur typique :**
- `< 3.0` : Pays avec ressources abondantes et démographie maîtrisée
- `5.0 – 7.5` : Sahel, Corne de l'Afrique, Asie du Sud
- `> 8.5` : Crises combinées (Somalie, RDC, Niger)

**Pertinence humanitaire :** ★★★★★ — Indicateur clé pour prédire les besoins en aide alimentaire et sanitaire.

---

#### `S2: Refugees and IDPs` — Réfugiés et déplacés internes
**Ce que ça mesure :** La pression exercée par les mouvements forcés de populations sur les États d'origine et d'accueil.

**Sous-indicateurs pris en compte :**
- Nombre de réfugiés produits par le pays (sortants)
- Nombre de déplacés internes (IDPs)
- Réfugiés accueillis depuis d'autres pays (entrants)
- Conditions dans les camps (surpopulation, conditions sanitaires)
- Hostilités envers les réfugiés dans le pays hôte

**Ordre de grandeur typique :**
- `< 2.0` : Pays sans déplacements significatifs
- `4.0 – 7.0` : Crises modérées (Mali 2013, RCA 2013)
- `> 8.5` : Crises massives (Syrie, Soudan du Sud, Afghanistan)

**Pertinence humanitaire :** ★★★★★ — Variable directement liée aux besoins d'aide humanitaire d'urgence. À croiser impérativement avec UNHCR.

---

### DIMENSION TRANSVERSALE (X) — *Facteurs externes*

---

#### `X1: External Intervention` — Intervention extérieure
**Ce que ça mesure :** Le degré d'implication d'acteurs étrangers dans les affaires internes d'un État, comme signal de son incapacité à fonctionner seul.

**Sous-indicateurs pris en compte :**
- Niveau d'aide étrangère (dépendance aux donors)
- Présence de missions de maintien de la paix (ONU, UA)
- Présence militaire étrangère
- Sanctions internationales
- Influence d'États voisins ou de puissances régionales
- Notation de crédit et influence des institutions financières internationales

**Ordre de grandeur typique :**
- `< 3.0` : États indépendants avec peu d'interventions extérieures
- `5.0 – 7.5` : Dépendance modérée à l'aide internationale
- `> 8.0` : État sous tutelle ou occupation partielle (Afghanistan, Mali, Haïti)

**Pertinence humanitaire :** ★★★★☆ — Un score élevé signale déjà un fort engagement humanitaire international ; utile pour calibrer les allocations supplémentaires.

---

## 4. Méthodologie de calcul FSI

### Le cadre CAST (Conflict Assessment System Tool)

Les scores FSI sont produits par **triangulation de 3 sources** :

```
                    ┌─────────────────────┐
                    │   Score FSI Final   │
                    └──────────┬──────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
    ┌──────▼──────┐    ┌───────▼───────┐   ┌──────▼──────┐
    │  Analyse de │    │  Données      │   │  Révision   │
    │  contenu    │    │  quantitatives│   │  qualitative│
    │  (CAST)     │    │  (ONU, BM...  │   │  d'experts  │
    └─────────────┘    └───────────────┘   └─────────────┘
    45–50M articles    Normalisées 0–10    Panel de revue
    /an analysés       et intégrées        final
```

### Étapes de production

1. **Collecte** : 45 à 50 millions d'articles/rapports en anglais analysés chaque année depuis 10 000+ sources
2. **Analyse de contenu automatisée** : Le logiciel CAST filtre les documents par mots-clés booléens liés à chaque sous-indicateur
3. **Intégration quantitative** : Les statistiques officielles (ONU, Banque Mondiale, OMS) sont normalisées et intégrées
4. **Score provisoire** : Attribution d'un score 0–10 par indicateur basé sur la saillance détectée
5. **Révision experte** : Un panel de chercheurs valide et ajuste les scores pour assurer la cohérence entre pays
6. **Score final** : Agrégation — `Total = C1 + C2 + C3 + E1 + E2 + E3 + P1 + P2 + P3 + S1 + S2 + X1`

---

## 5. Tableau récapitulatif des variables

| Code | Nom | Dimension | Échelle | Pertinence Aid |
|---|---|---|---|---|
| `C1` | Security Apparatus | Cohésion | 0–10 | ★★★★★ |
| `C2` | Factionalized Elites | Cohésion | 0–10 | ★★★★☆ |
| `C3` | Group Grievance | Cohésion | 0–10 | ★★★★☆ |
| `E1` | Economy | Économique | 0–10 | ★★★★☆ |
| `E2` | Economic Inequality | Économique | 0–10 | ★★★★★ |
| `E3` | Human Flight & Brain Drain | Économique | 0–10 | ★★★☆☆ |
| `P1` | State Legitimacy | Politique | 0–10 | ★★★★☆ |
| `P2` | Public Services | Politique | 0–10 | ★★★★★ |
| `P3` | Human Rights | Politique | 0–10 | ★★★★☆ |
| `S1` | Demographic Pressures | Social | 0–10 | ★★★★★ |
| `S2` | Refugees and IDPs | Social | 0–10 | ★★★★★ |
| `X1` | External Intervention | Transversal | 0–10 | ★★★★☆ |
| `Total` | Score composite | — | 0–120 | ★★★★★ |
| `Rank` | Classement mondial | — | 1–178 | ★★★★☆ |

---

## 6. Utilisation en Machine Learning — Clustering

### Le FSI est-il adapté au clustering ?

**OUI, et c'est l'un de ses usages les plus naturels.** Voici pourquoi :

| Critère ML | Situation FSI | Verdict |
|---|---|---|
| Variables numériques continues | Oui — scores 0–10 flottants | ✅ |
| Même échelle | Oui — toutes en 0–10 | ✅ (normalisation déjà faite) |
| Pas de valeurs manquantes majeures | Quasi-complet | ✅ |
| Variables corrélées | Oui — C1/C2/C3 corrèlent | ⚠️ À gérer |

---

### Algorithmes de clustering recommandés

#### 1. K-Means (recommandé en premier)
```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

features = ['C1','C2','C3','E1','E2','E3','P1','P2','P3','S1','S2','X1']
X = df[features]

# Normalisation (déjà en 0-10 mais utile quand même)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Choix du k avec la méthode Elbow
inertias = []
for k in range(2, 10):
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(X_scaled)
    inertias.append(km.inertia_)
```
**Avantage :** Simple, interprétable, rapide. **Limite :** Sensible aux outliers (ex : Somalie, Yémen distordent les clusters).

#### 2. Hierarchical Clustering (pour visualiser la structure)
```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

Z = linkage(X_scaled, method='ward')
# Dendrogramme révèle naturellement les groupes
```
**Avantage :** Pas besoin de fixer k à l'avance. Idéal pour un dataset de 178 pays.

#### 3. DBSCAN (pour détecter les cas atypiques)
```python
from sklearn.cluster import DBSCAN

db = DBSCAN(eps=1.5, min_samples=5)
labels = db.fit_predict(X_scaled)
# Labels = -1 → pays "outliers" (cas extrêmes uniques)
```
**Avantage :** Identifie les États totalement en dehors des patterns normaux.

---

### Clusters attendus sur données 2012–2015

D'après la littérature, un clustering sur le FSI révèle généralement **4 à 6 groupes cohérents** :

| Cluster probable | Score Total typique | Exemples pays |
|---|---|---|
| États en crise aiguë | 95–120 | Somalie, Soudan du Sud, Syrie, Afghanistan |
| États fragiles actifs | 80–95 | RDC, Haïti, Pakistan, Niger, Mali |
| États en tension modérée | 60–80 | Nigéria, Égypte, Éthiopie, Cambodge |
| États en développement stables | 40–60 | Sénégal, Maroc, Indonésie, Bolivie |
| États stables | 20–40 | Brésil, Mexique, Turquie, Afrique du Sud |
| États consolidés | 0–20 | Europe de l'Ouest, Canada, Australie, Japon |

---

### Précautions importantes pour le ML

**1. Multicollinéarité :**
Les variables C1, C2, C3 (cohésion) sont souvent corrélées. Utiliser une **ACP (PCA)** avant le clustering pour réduire la redondance.

**2. Ne pas utiliser `Rank` et `Total` comme features de clustering** si vous voulez travailler sur les profils thématiques — ce sont des dérivées des 12 indicateurs.

**3. Interprétation temporelle :**
Si vous clusterisez sur 2012–2015, distinguer bien l'axe pays de l'axe temporel. Un pays peut changer de cluster d'une année à l'autre (ex : Libye, pré et post-2011).

---

*Documentation produite pour projet d'allocation d'aide humanitaire — Sources : Fund for Peace, fragilestatesindex.org/methodology, fragilestatesindex.org/indicators*
