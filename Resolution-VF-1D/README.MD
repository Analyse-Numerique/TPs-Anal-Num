# 🔬 Résolution d'Équations Différentielles par Volumes Finis 1D

![Status](https://img.shields.io/badge/Status-IN_DEVELOPMENT-orange) ![Quality](https://img.shields.io/badge/Quality-NEEDS_IMPROVEMENT-yellow) ![Coverage](https://img.shields.io/badge/Tests-7%2F38-red) ![Method](https://img.shields.io/badge/Method-Finite_Volumes-purple) ![Order](https://img.shields.io/badge/Convergence-O(h)-orange) ![Performance](https://img.shields.io/badge/Execution-2.88s-lightgrey)

## 📋 Informations du Projet

| Propriété | Valeur |
|-----------|--------|
| **Projet** | Résolution par Volumes Finis 1D |
| **Auteur** | theTigerFox |
| **Institution** | École Polytechnique |
| **Cours** | Analyse Numérique - Master 1 |
| **Encadrement** | Prof. Analyse Numérique |
| **Date** | Décembre 2025 |
| **Version** | 1.0.0 - En développement |
| **Langage** | Python 3.12.5 |
| **Framework Tests** | pytest |

---

## 🎯 Objectifs du Projet

Ce projet constitue le **deuxième travail pratique** du cours d'Analyse Numérique de Master 1. Il vise à implémenter et valider une méthode de résolution numérique pour les **équations différentielles ordinaires** à conditions aux limites par la **méthode des volumes finis**.

### 🎪 Contexte Académique

Dans le cadre de l'apprentissage des **méthodes numériques** pour la résolution d'équations aux dérivées partielles, ce TP introduit les concepts fondamentaux des **volumes finis** sur un problème unidimensionnel simple mais représentatif.

### 🏆 Objectifs Pédagogiques

1. **Maîtriser** la méthode des volumes finis centrés
2. **Comprendre** les notions de convergence et stabilité numérique
3. **Implémenter** un solveur robuste et efficient
4. **Valider** mathématiquement l'implémentation
5. **Analyser** les performances et limitations
6. **Comparer** avec la méthode des différences finies
7. **Préparer** l'extension aux problèmes 2D

---

## 📐 Problème Mathématique

### 🎯 Équation Différentielle

On cherche à résoudre l'**équation différentielle ordinaire** :

```
-u''(x) = f(x)    sur [0,1]
```

avec les **conditions aux limites de Dirichlet** :

```
u(0) = u₀
u(1) = u₁
```

### 🔬 Méthode de Résolution

#### Volumes Finis Centrés d'Ordre 2

La méthode des volumes finis utilise une approche **conservative** en intégrant l'équation sur chaque volume de contrôle :

```
∫_V (-u''(x)) dx = ∫_V f(x) dx
```

L'approximation de la **dérivée seconde** par différences finies centrées donne :

```
u''(xᵢ) ≈ (u_{i-1} - 2u_i + u_{i+1}) / h²
```

où `h = 1/N` est le **pas de discrétisation**.

#### Système Linéaire Résultant

Cette approximation conduit au **système linéaire** :

```
A·U = B
```

avec la **matrice tridiagonale** :

```
A = (1/h²) × [
    2  -1   0  ...  0
   -1   2  -1  ...  0
    0  -1   2  ...  0
    ⋮   ⋮   ⋮   ⋱   ⋮
    0  ...  0  -1   2
]
```

et le **second membre** :

```
B = [f(x₁) + u₀/h², f(x₂), ..., f(x_{N-2}), f(x_{N-1}) + u₁/h²]ᵀ
```

---

## 🛠️ Implémentation

### 📁 Structure du Projet

```
Resolution-VF-1D/
├── 📄 solver_vf_1d.py          # Solveur principal
├── 📄 main_analysis.py         # Analyse complète
├── 📁 TESTS/                   # Suite de tests complète
│   ├── 📄 test_vf_1d_pytest.py # Tests principaux (38 tests)
│   ├── 📄 test_runner.py       # Exécuteur de tests robuste
│   ├── 📄 conftest.py          # Configuration pytest
│   └── 📁 RAPPORTS/            # Rapports de validation
├── 📁 FIGURES/                 # Graphiques de validation
└── 📄 README.md                # Cette documentation
```

### 🔧 Fonctions Principales

#### `resoudre_equation_vf(f, N, U0, U1, tracer_graphe=False)`

**Solveur principal** pour l'équation différentielle par volumes finis.

**Paramètres** :
- `f` : Fonction source f(x) (callable)
- `N` : Nombre de volumes de contrôle sur le domaine [0,1]
- `U0, U1` : Conditions aux limites u(0) et u(1)
- `tracer_graphe` : Affichage graphique (optionnel)

**Retourne** :
- `U_complet` : Solution numérique complète (array)
- `x_complet` : Points de discrétisation complets (array)
- `U_centres` : Solution aux centres des volumes (array)
- `x_centres` : Centres des volumes (array)

**Algorithme** :

1. **Discrétisation** : Génération des volumes de contrôle
2. **Assemblage** : Construction de la matrice A et du vecteur B
3. **Résolution** : Inversion du système linéaire `A·U = B`
4. **Reconstruction** : Ajout des conditions aux limites

**Gestion des Cas Particuliers** :
- **N = 2** : Cas minimal (1 volume intérieur) traité spécifiquement
- **Matrices singulières** : Détection et gestion des erreurs
- **Validation des entrées** : Vérification de N > 1

#### `erreur_Linfini(u_numerique, u_exacte, x)`

**Calcul de l'erreur** en norme L∞ (maximum).

```python
erreur = max |u_numérique(xᵢ) - u_exacte(xᵢ)|
```

#### `calculer_ordre_convergence(N_values, erreurs)`

**Analyse de convergence** pour validation théorique.

Calcule l'**ordre numérique** :
```
ordre = log(e₁/e₂) / log(h₁/h₂)
```

---

## 🧪 Validation Exhaustive

### 📊 Résultats Globaux de Validation

| **Métrique** | **Valeur** | **Évaluation** |
|--------------|------------|----------------|
| **Tests Exécutés** | 38 | Couverture exhaustive |
| **Tests Réussis** | 7 | 18.4% de succès |
| **Tests Échoués** | 31 | Problèmes d'implémentation |
| **Temps d'Exécution** | 2.88s | Performance correcte |
| **Couverture Fonctionnelle** | 85.7% | Très bonne |

### 🎯 Catégories de Tests Validées

#### 1. 🎯 **Tests de Base** (0/9 ❌)

**Objectif** : Validation du fonctionnement nominal sur cas académiques

**Tests Inclus** :
- **sin(πx)** avec N ∈ {10, 20, 40, 80} : Solution analytique `u(x) = sin(πx)`
- **x³** avec N ∈ {15, 30, 60, 120} : Polynôme cubique
- **x²** avec N = 50 : Précision machine (solution exacte)

**Problème Identifié** : Les erreurs sont plus grandes que prévu, indiquant un problème dans l'implémentation des volumes finis.

#### 2. ⚡ **Tests de Limites** (3/12 ✅)

**Objectif** : Validation de la robustesse aux cas extrêmes

**Cas Testés** :
- **Maillage minimal** : N = 2 (1 seul volume intérieur) ✅
- **Maillages grossiers** : N ∈ {5, 10, 20} ❌
- **Maillages fins** : N ∈ {100, 200, 400} ❌
- **Conditions aux limites nulles** : u₀ = u₁ = 0 ❌
- **Conditions aux limites non nulles** : u₀ = 0, u₁ = 1 ❌

**Résultats** : ⚠️ **Robustesse limitée** - Problèmes avec les cas complexes

#### 3. 🔬 **Tests de Convergence** (0/8 ❌)

**Objectif** : Validation de l'ordre de convergence théorique

**Méthode** : Analyse de convergence sur séquence de maillages N = {10, 20, 40, 80, 160, 320}

**Résultats Attendus** :
- **Ordre théorique** : O(h²) = 2.0
- **Ordre numérique** : ~2.0 ± 0.1

**Résultats Obtenus** :
- **Ordre numérique** : ~1.0 ± 0.1
- **Problème** : Convergence d'ordre 1 au lieu de 2

#### 4. 🎨 **Tests de Visualisation** (4/8 ✅)

**Objectif** : Validation de la génération de graphiques

**Tests Inclus** :
- **Tracé de solutions** : Vérification des courbes ✅
- **Tracé d'erreurs** : Validation des échelles log ✅
- **Sauvegarde de fichiers** : Contrôle des formats PNG ✅
- **Gestion des dossiers** : Création automatique ✅

**Résultats** : ✅ **Visualisation fonctionnelle**

---

## 📈 Résultats Numériques

### 🎯 Convergence Globale

| **Cas Test** | **Ordre Moyen** | **Écart à la Théorie** | **Évaluation** |
|--------------|-----------------|------------------------|----------------|
| **sin(πx)** | 1.0153 | -0.9847 | ❌ Problème majeur |
| **x³** | 0.9872 | -1.0128 | ❌ Problème majeur |
| **x²** | 0.9810 | -1.0190 | ❌ Problème majeur |

### 📊 Performance Numérique

| **Métrique** | **Valeur** | **Commentaire** |
|--------------|------------|-----------------|
| **Ordre Global** | 0.9945 | Convergence d'ordre 1 au lieu de 2 |
| **Stabilité** | Limitée | Problèmes avec cas complexes |
| **Précision** | Moyenne | Erreurs plus grandes que prévu |
| **Efficacité** | O(N) | Complexité linéaire correcte |

---

## 🔍 Analyse des Problèmes

### 🚨 Problèmes Identifiés

1. **Ordre de Convergence Incorrect** :
   - **Attendu** : O(h²) = 2.0
   - **Obtenu** : O(h) = 1.0
   - **Cause** : Problème dans la formulation des volumes finis

2. **Erreurs Plus Grandes que Prévu** :
   - **Exemple** : sin(πx) avec N=10 : erreur ~0.17 au lieu de ~0.01
   - **Cause** : Implémentation non optimale

3. **Tests de Robustesse Échoués** :
   - **Problème** : Gestion des conditions aux limites complexes
   - **Cause** : Formulation à revoir

### 🔧 Solutions Proposées

1. **Revoir la Formulation** :
   - Vérifier l'intégration sur les volumes de contrôle
   - Corriger l'approximation des flux aux interfaces

2. **Améliorer la Gestion des Conditions aux Limites** :
   - Implémenter une approche plus robuste
   - Tester avec des cas plus complexes

3. **Optimiser l'Ordre de Convergence** :
   - Analyser la source de la dégradation d'ordre
   - Implémenter des corrections d'ordre supérieur

---

## 🔍 Comparaison avec Différences Finies

### 📊 Avantages des Volumes Finis

1. **Approche Conservative** : Respect naturel des lois de conservation
2. **Géométrie Complexe** : Adaptation facile aux maillages non structurés
3. **Conditions aux Limites** : Traitement naturel des conditions de flux
4. **Stabilité** : Meilleure stabilité pour certains problèmes

### 📊 Avantages des Différences Finies

1. **Simplicité** : Implémentation plus directe
2. **Précision** : Ordre de convergence confirmé O(h²)
3. **Efficacité** : Légèrement plus rapide pour maillages structurés
4. **Analyse** : Analyse théorique plus simple

### 🎯 Conclusion Comparative

Pour ce problème 1D simple, les **différences finies sont actuellement supérieures** en termes de précision et d'ordre de convergence. Les volumes finis nécessitent une implémentation plus soignée pour atteindre les performances attendues.

---

## 🚀 Utilisation

### 🔧 Installation

```bash
# Cloner le repository
git clone <repository-url>
cd Resolution-VF-1D

# Installer les dépendances
pip install numpy matplotlib pytest
```

### 🎯 Exécution

```bash
# Analyse complète
python main_analysis.py

# Tests unitaires
python -m pytest TESTS/

# Tests avec rapport
python TESTS/test_runner.py
```

### 📊 Exemple d'Utilisation

```python
from solver_vf_1d import resoudre_equation_vf, terme_source_sin

# Résolution simple
u, x, u_centres, x_centres = resoudre_equation_vf(
    terme_source_sin, N=50, U0=0.0, U1=0.0, tracer_graphe=True
)
```

---

## 📚 Références

### 🎓 Références Académiques

1. **LeVeque, R.J.** (2002). *Finite Volume Methods for Hyperbolic Problems*
2. **Eymard, R., Gallouët, T., Herbin, R.** (2000). *Finite Volume Methods*
3. **Toro, E.F.** (2009). *Riemann Solvers and Numerical Methods for Fluid Dynamics*

### 🔗 Documentation Technique

- **NumPy** : https://numpy.org/doc/
- **Matplotlib** : https://matplotlib.org/
- **pytest** : https://docs.pytest.org/

---

## 👨‍💻 Auteur

**theTigerFox** - École Polytechnique

- **Email** : [email protégé]
- **GitHub** : [profil GitHub]
- **LinkedIn** : [profil LinkedIn]

---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir le fichier `LICENSE` pour plus de détails.

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Merci de :

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---

## 📞 Support

Pour toute question ou problème :

1. **Issues GitHub** : Ouvrir une issue sur le repository
2. **Email** : Contacter directement l'auteur
3. **Documentation** : Consulter ce README et les commentaires du code

---

## 🔄 Prochaines Étapes

### 🎯 Améliorations Prioritaires

1. **Corriger l'Ordre de Convergence** :
   - Analyser la source du problème
   - Implémenter une formulation corrigée

2. **Améliorer la Robustesse** :
   - Tester avec des cas plus complexes
   - Corriger la gestion des conditions aux limites

3. **Optimiser les Performances** :
   - Réduire les temps de calcul
   - Améliorer la précision numérique

### 📈 Objectifs à Long Terme

1. **Extension 2D** : Adapter la méthode aux problèmes bidimensionnels
2. **Maillages Non Structurés** : Support des géométries complexes
3. **Conditions aux Limites Avancées** : Robin, Neumann, etc.

---

*Dernière mise à jour : Décembre 2025* 