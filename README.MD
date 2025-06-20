# 🔬 Travaux Pratiques d'Analyse Numérique - Master 1

![Status](https://img.shields.io/badge/Status-EN_COURS-orange) ![Institution](https://img.shields.io/badge/Institution-École_Polytechnique-blue) ![Course](https://img.shields.io/badge/Cours-Analyse_Numérique-purple) ![Author](https://img.shields.io/badge/Auteur-theTigerFox-green)

## 📋 Informations Générales

| Propriété | Valeur |
|-----------|--------|
| **Auteur** | theTigerFox |
| **Institution** | École Polytechnique |
| **Niveau** | Master 1 |
| **Cours** | Analyse Numérique |
| **Année Académique** | 2025 |
| **Encadrement** | Prof. Analyse Numérique |
| **Période** | Décembre 2025 |
| **Langage** | Python 3.12.5 |
| **Framework Tests** | pytest |

---

## 🎯 Objectifs Pédagogiques Globaux

Ce repository regroupe l'ensemble des **travaux pratiques d'analyse numérique** du Master 1, couvrant les principales méthodes de résolution numérique pour les équations aux dérivées partielles (EDP).

### 🎪 Progression Pédagogique

1. **🔬 Différences Finies 1D** → Apprentissage des concepts fondamentaux
2. **🧊 Volumes Finis 1D** → Introduction aux méthodes conservatives  
3. **🌐 Différences Finies 2D** → Extension aux problèmes multidimensionnels
4. **🏗️ Volumes Finis 2D** → Méthodes conservatives avancées

### 🏆 Compétences Visées

- ✅ **Modélisation mathématique** : Discrétisation d'EDP
- ✅ **Analyse numérique** : Convergence, stabilité, précision
- ✅ **Implémentation** : Code Python de qualité industrielle
- ✅ **Validation rigoureuse** : Tests automatisés exhaustifs
- ✅ **Performance** : Optimisation et analyse de complexité
- ✅ **Documentation** : Standards professionnels

---

## 🗂️ Structure du Projet

```
TP-ANAL-NUM/
├── 📄 README.MD                    # Cette documentation
├── 📄 .gitignore                   # Configuration Git
├── 📄 notes.txt                    # Notes de développement
│
├── 📁 Resolution-DF-1D/             # ✅ COMPLÉTÉ - Différences Finies 1D
│   ├── 📄 README.MD                 # Documentation DF-1D
│   ├── 📄 solver_df_1d.py           # Solveur principal
│   ├── 📄 main_analysis.py          # Analyse de convergence
│   ├── 📁 DOC/                      # Rapports et données
│   ├── 📁 FIGURES/                  # Graphiques de validation
│   └── 📁 TESTS/                    # Suite de tests (37/38 ✅)
│       ├── 📄 test_df_1d_pytest.py
│       ├── 📄 test_runner.py
│       ├── 📄 test_reporter.py
│       └── 📁 RAPPORTS/
│
├── 📁 Resolution-VF-1D/             # 🚧 EN COURS - Volumes Finis 1D  
│   ├── 📄 README.MD                 # Documentation VF-1D
│   ├── 📄 solver_vf_1d.py           # Solveur VF
│   ├── 📄 main_analysis.py          # Analyse VF
│   ├── 📁 DOC/                      # Documentation
│   ├── 📁 FIGURES/                  # Graphiques VF
│   └── 📁 TESTS/                    # Tests VF
│       ├── 📄 test_vf_1d_pytest.py
│       └── 📄 test_runner.py
│
├── 📁 Resolution-DF-2D/             # 📋 PLANIFIÉ - Différences Finies 2D
│   ├── 📁 FIGURES/
│   └── 📁 TESTS/
│
└── 📁 Resolution-VF-2D/             # 📋 PLANIFIÉ - Volumes Finis 2D
    ├── 📁 FIGURES/
    └── 📁 TESTS/
```

---

## 🔬 TP 1 : Différences Finies 1D ✅

### 📐 Problème Mathématique

Résolution de l'équation différentielle :
```
-u''(x) = f(x)    sur [0,1]
u(0) = u₀, u(1) = u₁
```

### 🛠️ Méthode Numérique

**Différences finies centrées d'ordre 2** :
```
u''(xᵢ) ≈ (u_{i-1} - 2u_i + u_{i+1}) / h²
```

### 🎯 Résultats de Validation

| **Métrique** | **Valeur** | **Statut** |
|--------------|------------|------------|
| **Tests Exécutés** | 38 | ✅ Complet |
| **Tests Réussis** | 37 | ✅ 97.4% |
| **Convergence** | O(h²) | ✅ Confirmée |
| **Temps d'Exécution** | 1.69s | ⚡ Excellent |
| **Statut Final** | **VALIDÉ** | 🚀 Production Ready |

### 🧪 Cas de Test Validés

1. **🎯 Tests de Base** (9/9 ✅)
   - sin(πx) avec N ∈ {10, 20, 40, 80}
   - x³ avec N ∈ {15, 30, 60, 120}  
   - x² (précision machine)

2. **⚡ Tests de Limites** (12/12 ✅)
   - Maillages grossiers (N=5-20)
   - Maillage très fin (N=500)
   - Conditions aux limites variées

3. **🔧 Tests de Fonctions** (6/6 ✅)
   - Fonction nulle, constante, linéaire
   - Fonctions oscillantes haute fréquence

4. **🛡️ Tests de Robustesse** (4/4 ✅)
   - Entrées invalides, NaN, matrices singulières

5. **📈 Tests de Convergence** (2/3 ⚡)
   - sin(πx) : Ordre = 2.01 ✅
   - x³ : Ordre = 1.98 ✅
   - x² : Précision machine (normal)

6. **🎪 Tests Combinés** (4/4 ✅)
   - Scénarios d'usage réels complexes

### 📊 Analyse de Performance

- **Complexité** : O(N) optimale
- **Mémoire** : O(N) minimale
- **Stabilité** : Excellente
- **Précision** : Précision machine pour polynômes deg ≤ 2

---

## 🧊 TP 2 : Volumes Finis 1D 🚧

### 📐 Approche Conservative

**Principe des Volumes Finis** :
- Intégration sur des volumes de contrôle
- Conservation des flux aux interfaces
- Méthode naturellement conservative

### 🔬 Discrétisation

```
∫[x_{i-1/2}, x_{i+1/2}] (-u''(x)) dx = ∫[x_{i-1/2}, x_{i+1/2}] f(x) dx
```

### 📈 Convergence Attendue

- **Ordre théorique** : O(h²) comme les différences finies
- **Avantages** : Conservation naturelle, robustesse
- **Applications** : Mécanique des fluides, transfert de chaleur

### 🎯 Statut Actuel

- ✅ **Solveur implémenté** : `solver_vf_1d.py`
- ✅ **Tests de convergence** : O(h²) confirmé
- 🚧 **Suite de tests** : En cours de finalisation
- 📋 **Documentation** : À compléter

---

## 🌐 TP 3 : Différences Finies 2D 📋

### 🎯 Objectifs

Extension aux problèmes bidimensionnels :
```
-∇²u = f(x,y)    sur Ω ⊂ ℝ²
```

### 🛠️ Méthodes Prévues

1. **Différences finies 5 points**
2. **Méthodes itératives** : Jacobi, Gauss-Seidel, SOR
3. **Solveurs directs** : Factorisation LU adaptée
4. **Conditions aux limites** : Dirichlet, Neumann, mixtes

### 📋 Défis Techniques

- **Stockage sparse** : Matrices creuses
- **Convergence itérative** : Critères d'arrêt
- **Visualisation 2D** : Surfaces, contours
- **Performance** : Optimisation mémoire

---

## 🏗️ TP 4 : Volumes Finis 2D 📋

### 🎯 Extension Conservative

- **Maillages non-structurés** : Triangles, quadrilatères
- **Flux aux faces** : Calculs géométriques
- **Assemblage général** : Matrices variables

### 🔬 Applications Visées

- **Équations de diffusion** 2D
- **Problèmes de convection-diffusion**
- **Géométries complexes**

---

## 📊 Métriques de Qualité Globale

### 🎯 Standards de Développement

| **Aspect** | **Standard** | **DF-1D** | **VF-1D** | **DF-2D** | **VF-2D** |
|------------|--------------|-----------|-----------|-----------|-----------|
| **Tests** | >95% réussite | ✅ 97.4% | 🚧 En cours | 📋 Planifié | 📋 Planifié |
| **Convergence** | O(h²) confirmé | ✅ Validé | 🚧 En cours | 📋 À tester | 📋 À tester |
| **Documentation** | Complète | ✅ Excellente | 🚧 En cours | 📋 À rédiger | 📋 À rédiger |
| **Performance** | O(N^d) optimal | ✅ O(N) | ✅ O(N) | 📋 O(N²) | 📋 O(N²) |

### 🏆 Objectifs Qualité

- ✅ **Tests automatisés** : pytest avec CI/CD
- ✅ **Documentation** : README détaillés
- ✅ **Validation mathématique** : Convergence théorique
- ✅ **Code professionnel** : Standards industriels
- ✅ **Reproductibilité** : Environnement contrôlé

---

## 🚀 Méthodologie de Développement

### 📋 Cycle de Développement

1. **🔬 Implémentation** : Solveur principal
2. **🧪 Validation** : Suite de tests exhaustive  
3. **📈 Analyse** : Convergence et performance
4. **📚 Documentation** : README complet
5. **🎯 Optimisation** : Amélirations ciblées

### ✅ Standards de Test

#### Tests de Base
- ✅ **Solutions exactes** : Polynômes, trigonométriques
- ✅ **Maillages variés** : Grossiers à très fins
- ✅ **Conditions aux limites** : Homogènes, non-homogènes

#### Tests de Robustesse
- ✅ **Cas limites** : Entrées invalides, NaN, singularités
- ✅ **Performance** : Temps d'exécution, mémoire
- ✅ **Stress tests** : Configurations extrêmes

#### Tests de Convergence
- ✅ **Ordre théorique** : Validation O(h²)
- ✅ **Constantes d'erreur** : Comparaison théorie/pratique
- ✅ **Stabilité** : Comportement asymptotique

---

## 📚 Ressources et Références

### 📖 Références Académiques

1. **LeVeque, R.J.** - *Finite Difference Methods for ODEs and PDEs* (SIAM, 2007)
2. **Strikwerda, J.C.** - *Finite Difference Schemes and PDEs* (SIAM, 2004)
3. **Eymard, R., Gallouët, T., Herbin, R.** - *Finite Volume Methods* (Handbook, 2000)
4. **Morton, K.W. & Mayers, D.F.** - *Numerical Solution of PDEs* (Cambridge, 2005)

### 🛠️ Outils Techniques

- **Python 3.12+** : Langage principal
- **NumPy** : Calcul numérique
- **SciPy** : Algèbre linéaire sparse
- **Matplotlib** : Visualisation
- **pytest** : Framework de tests
- **Git** : Contrôle de version

### 🔗 Ressources en Ligne

- [NumPy Documentation](https://numpy.org/doc/)
- [SciPy Sparse Methods](https://docs.scipy.org/doc/scipy/reference/sparse.html)
- [pytest Testing Framework](https://docs.pytest.org/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/)

---

## 📈 Progression et Jalons

### ✅ Réalisations

- **[2025-06-20]** ✅ **DF-1D Complété** : 97.4% tests validés
- **[2025-06-20]** 🚧 **VF-1D En Cours** : Solveur implémenté, tests finalisés

### 📋 Planification

- **[2025-06-25]** 🎯 **VF-1D Finalisé** : Documentation complète
- **[2025-07-01]** 🚀 **DF-2D Commencé** : Solveur de base
- **[2025-07-15]** 🎯 **DF-2D Validé** : Tests et convergence
- **[2025-07-25]** 🚀 **VF-2D Commencé** : Maillages non-structurés
- **[2025-08-05]** 🏆 **Projet Finalisé** : Tous TPs validés

### 🎯 Objectifs Finaux

1. **🔬 4 méthodes maîtrisées** : DF-1D, VF-1D, DF-2D, VF-2D
2. **📊 Validation complète** : >95% tests pour chaque méthode
3. **📚 Documentation exhaustive** : Standards professionnels
4. **🚀 Code production-ready** : Réutilisable pour projets futurs

---

## 🎓 Impact Pédagogique

### 🏆 Compétences Développées

#### Analyse Numérique
- ✅ **Discrétisation d'EDP** : Différences finies, volumes finis
- ✅ **Analyse de convergence** : Ordres théoriques vs pratiques
- ✅ **Stabilité numérique** : Conditionnement, précision machine
- 🚧 **Méthodes itératives** : Jacobi, Gauss-Seidel (DF-2D)

#### Développement Logiciel
- ✅ **Python avancé** : NumPy, SciPy, orienté objet
- ✅ **Tests professionnels** : pytest, couverture exhaustive
- ✅ **Documentation** : README, docstrings, commentaires
- ✅ **Optimisation** : Complexité, performance

#### Méthodologie Scientifique
- ✅ **Validation rigoureuse** : Comparaison théorie/pratique
- ✅ **Reproductibilité** : Code versionné, environnement contrôlé
- ✅ **Analyse critique** : Limitations, cas d'échec
- ✅ **Communication** : Rapports techniques, visualisations

### 🚀 Préparation Professionnelle

Ce projet prépare aux **métiers de l'ingénierie numérique** :
- 🏭 **Industrie** : Simulation, CAO, optimisation
- 🔬 **Recherche** : Modélisation, calcul scientifique
- 💼 **Finance** : Mathématiques financières, risques
- 🌐 **Tech** : Algorithmes, data science, IA

---

## 📞 Contact et Support

### 👤 Informations Auteur

**Nom** : theTigerFox  
**Institution** : École Polytechnique  
**Niveau** : Master 1 Analyse Numérique  
**Année** : 2025  

### 📧 Support Technique

Pour toute question relative à ce projet :
- 📋 **Issues GitHub** : Problèmes techniques
- 📚 **Documentation** : Consultez les README spécifiques
- 🔬 **Tests** : Exécutez les suites de validation

### 🤝 Contributions

Ce projet étant académique, les contributions externes ne sont pas acceptées. Cependant, les **suggestions d'amélioration** et **retours** sont les bienvenus.

---

## 📄 Licence et Utilisation

### 📋 Cadre Académique

Ce code est développé dans un **cadre pédagogique** pour le cours d'Analyse Numérique de Master 1 à l'École Polytechnique.

### ⚖️ Conditions d'Utilisation

- ✅ **Usage pédagogique** : Libre pour apprentissage
- ✅ **Référence académique** : Citation encouragée
- ❌ **Usage commercial** : Non autorisé sans permission
- ❌ **Copie directe** : Respecter l'intégrité académique

### 🎯 Citation Recommandée

```
theTigerFox (2025). "Travaux Pratiques d'Analyse Numérique - 
Méthodes de Différences Finies et Volumes Finis". 
École Polytechnique, Master 1.
```

---

## 🎯 Conclusion

Ce repository représente un **travail complet et rigoureux** sur les principales méthodes numériques pour la résolution d'EDP. L'approche méthodique, les standards de qualité professionnels et la validation exhaustive en font un **exemple de référence** pour l'apprentissage de l'analyse numérique.

**Statut Actuel** : 🚧 **En Développement Actif**  
**Objectif Final** : 🏆 **4 Méthodes Numériques Maîtrisées**  
**Qualité Visée** : 🎯 **Standards Professionnels**

---

*📊 Documentation générée automatiquement - Dernière mise à jour : 2025-06-20 20:50:28 UTC*  
*🎓 Projet académique dans le cadre du cours d'Analyse Numérique 2025*