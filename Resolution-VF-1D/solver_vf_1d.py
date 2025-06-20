"""
SOLVEUR VOLUMES FINIS 1D - VERSION PROFESSIONNELLE
================================================

Résolution de l'équation différentielle :
    -u''(x) = f(x) sur [0,1]
    u(0) = u0, u(1) = u1

par la méthode des Volumes Finis avec:
- Discrétisation conservative
- Convergence d'ordre 2 (O(h²))
- Gestion robuste des cas limites
- Interface identique au solver DF

Auteur: theTigerFox
Date: 2025-06-20
Méthode: Volumes Finis centrés
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime


def resoudre_equation_diff_vf(f, N, U0, U1, tracer_graphe=False):
    """
    Résout l'équation différentielle -u''(x) = f(x) par Volumes Finis
    
    Méthode des Volumes Finis:
    - Division du domaine [0,1] en N volumes (cellules)
    - Conservation des flux aux interfaces
    - Convergence d'ordre 2 garantie
    
    Paramètres:
        f (callable): Terme source f(x)
        N (int): Nombre de volumes (cellules)
        U0 (float): Condition limite u(0) = U0
        U1 (float): Condition limite u(1) = U1
        tracer_graphe (bool): Affichage graphique optionnel
    
    Retourne:
        tuple: (U, x) où
            U (ndarray): Solution aux centres des cellules + limites
            x (ndarray): Points de discrétisation (centres + limites)
    
    Raises:
        ValueError: Si N <= 1
        RuntimeError: Si le système linéaire est singulier
    """
    
    if N <= 1:
        raise ValueError("N doit être supérieur à 1 pour les volumes finis")
    
    # Discrétisation du domaine
    h = 1.0 / N  # Taille de chaque volume
    
    # Points des interfaces (faces des volumes)
    x_faces = np.linspace(0, 1, N + 1)  # N+1 faces pour N volumes
    
    # Centres des volumes (points de calcul)
    x_centres = np.array([(x_faces[i] + x_faces[i+1])/2 for i in range(N)])
    
    # Gestion du cas N=1 (volume unique)
    if N == 1:
        # Un seul volume [0,1], centre en x=0.5
        x_centre = 0.5
        f_centre = f(np.array([x_centre]))[0]
        
        # Équation: flux_sortant - flux_entrant = source_intégrée
        # -(U1 - U_centre)/h - (-(U_centre - U0)/h) = f_centre * h
        # -U1/h + U_centre/h + U_centre/h - U0/h = f_centre * h
        # (2/h) * U_centre = f_centre * h + (U0 + U1)/h
        # U_centre = h * (f_centre * h + (U0 + U1)/h) / 2
        # U_centre = (h² * f_centre + U0 + U1) / 2
        
        U_centre = (h**2 * f_centre + U0 + U1) / 2
        
        # Construction de la solution complète
        x_solution = np.array([0, x_centre, 1])
        U_solution = np.array([U0, U_centre, U1])
        
    else:
        # Cas général: N > 1 volumes
        
        # Matrice du système (N équations, N inconnues)
        A = np.zeros((N, N))
        b = np.zeros(N)
        
        # Calcul du terme source intégré sur chaque volume
        f_centres = f(x_centres)
        source_integree = f_centres * h  # ∫ f(x) dx ≈ f(x_centre) * h
        
        for i in range(N):
            # Équation de conservation pour le volume i
            # Flux sortant - Flux entrant = Source intégrée
            
            # Coefficient diagonal (toujours présent)
            A[i, i] = 2.0 / h  # Contribution des deux faces
            
            # Terme source
            b[i] = source_integree[i]
            
            # Flux à la face gauche (x_{i-1/2})
            if i == 0:
                # Volume à gauche du domaine: flux = -(U_centre - U0)/h
                b[i] += U0 / h
            else:
                # Volume interne: flux = -(U_i - U_{i-1})/h
                A[i, i-1] = -1.0 / h
            
            # Flux à la face droite (x_{i+1/2})  
            if i == N-1:
                # Volume à droite du domaine: flux = -(U1 - U_centre)/h
                b[i] += U1 / h
            else:
                # Volume interne: flux = -(U_{i+1} - U_i)/h
                A[i, i+1] = -1.0 / h
        
        try:
            # Résolution du système linéaire
            U_centres = np.linalg.solve(A, b)
        except np.linalg.LinAlgError as e:
            raise RuntimeError(f"Impossible de résoudre le système Volumes Finis: {e}")
        
        # Construction de la solution complète avec limites
        x_solution = np.concatenate([[0], x_centres, [1]])
        U_solution = np.concatenate([[U0], U_centres, [U1]])
    
    # Affichage graphique optionnel
    if tracer_graphe:
        plt.figure(figsize=(12, 8))
        
        plt.subplot(2, 1, 1)
        plt.plot(x_solution, U_solution, 'ro-', linewidth=2, markersize=6, 
                label=f'Solution VF (N={N})')
        plt.grid(True, alpha=0.3)
        plt.xlabel('x')
        plt.ylabel('u(x)')
        plt.title(f'Solution par Volumes Finis - N={N} volumes')
        plt.legend()
        
        plt.subplot(2, 1, 2)
        # Affichage des volumes
        for i in range(N):
            plt.axvspan(x_faces[i], x_faces[i+1], alpha=0.3, 
                       color=f'C{i%10}', label=f'Volume {i+1}' if i < 3 else '')
            plt.plot(x_centres[i] if N > 1 else 0.5, 
                    U_centres[i] if N > 1 else U_solution[1], 
                    'ko', markersize=8)
        
        plt.grid(True, alpha=0.3)
        plt.xlabel('x')
        plt.ylabel('Volumes')
        plt.title('Discrétisation en Volumes Finis')
        if N <= 3:
            plt.legend()
        
        plt.tight_layout()
        plt.show()
    
    return U_solution, x_solution


def erreur_Linfini_vf(u_numerique, u_exacte_func, x):
    """
    Calcule l'erreur L∞ entre solution VF et solution exacte
    
    Paramètres:
        u_numerique (ndarray): Solution numérique VF
        u_exacte_func (callable): Fonction solution exacte
        x (ndarray): Points de discrétisation
    
    Retourne:
        float: Erreur maximale ||u_num - u_exact||_∞
    """
    u_exacte = u_exacte_func(x)
    return np.max(np.abs(u_numerique - u_exacte))


def calculer_ordre_convergence_vf(N_values, erreurs):
    """
    Calcule l'ordre de convergence numérique pour Volumes Finis
    
    Paramètres:
        N_values (list): Valeurs de N testées
        erreurs (list): Erreurs correspondantes
    
    Retourne:
        tuple: (ordres_individuels, ordre_moyen)
    """
    if len(N_values) < 2:
        return [], 0.0
    
    log_N = np.log(np.array(N_values))
    log_erreurs = np.log(np.array(erreurs))
    
    ordres = []
    for i in range(1, len(N_values)):
        if erreurs[i] > 1e-15 and erreurs[i-1] > 1e-15:
            ordre = -(log_erreurs[i] - log_erreurs[i-1]) / (log_N[i] - log_N[i-1])
            ordres.append(ordre)
    
    ordre_moyen = np.mean(ordres) if ordres else 0.0
    return ordres, ordre_moyen


def analyser_convergence_vf(solution_exacte_func, terme_source_func, u0, u1, 
                           N_values, nom_cas, dossier_figures):
    """
    Analyse complète de convergence pour méthode Volumes Finis
    
    Paramètres:
        solution_exacte_func (callable): u(x) exacte
        terme_source_func (callable): f(x) terme source
        u0, u1 (float): Conditions aux limites
        N_values (list): Valeurs de N à tester
        nom_cas (str): Nom du cas pour les fichiers
        dossier_figures (str): Répertoire des figures
    
    Retourne:
        tuple: (erreurs, ordres, ordre_moyen)
    """
    os.makedirs(dossier_figures, exist_ok=True)
    
    erreurs = []
    
    # Calcul des erreurs pour chaque N
    for N in N_values:
        u_num, x = resoudre_equation_diff_vf(terme_source_func, N, u0, u1)
        erreur = erreur_Linfini_vf(u_num, solution_exacte_func, x)
        erreurs.append(erreur)
        
        # Tracés pour quelques valeurs de N
        if N in [N_values[0], N_values[len(N_values)//2], N_values[-1]]:
            x_exact = np.linspace(0, 1, 1000)
            u_exact = solution_exacte_func(x_exact)
            
            plt.figure(figsize=(12, 8))
            
            plt.subplot(2, 1, 1)
            plt.plot(x, u_num, 'ro-', markersize=6, linewidth=2, 
                    label=f'VF N={N}')
            plt.plot(x_exact, u_exact, 'b-', linewidth=2, 
                    label='Solution exacte')
            plt.grid(True, alpha=0.3)
            plt.xlabel('x')
            plt.ylabel('u(x)')
            plt.title(f'{nom_cas} - Volumes Finis N={N}')
            plt.legend()
            
            plt.subplot(2, 1, 2)
            erreur_points = np.abs(u_num - solution_exacte_func(x))
            plt.semilogy(x, erreur_points, 'go-', markersize=4, 
                        label=f'Erreur (max: {np.max(erreur_points):.2e})')
            plt.grid(True, alpha=0.3)
            plt.xlabel('x')
            plt.ylabel('Erreur absolue')
            plt.title(f'Erreur pour N={N}')
            plt.legend()
            
            plt.tight_layout()
            
            nom_fichier = f"{nom_cas.replace(' ', '_').replace('(', '').replace(')', '')}_VF_N{N}.png"
            plt.savefig(os.path.join(dossier_figures, nom_fichier), dpi=300, bbox_inches='tight')
            plt.close()
    
    # Analyse de convergence
    ordres, ordre_moyen = calculer_ordre_convergence_vf(N_values, erreurs)
    
    # Graphique de convergence
    plt.figure(figsize=(10, 8))
    plt.loglog(N_values, erreurs, 'ro-', linewidth=2, markersize=8, 
              label='Erreur VF calculée')
    
    # Ligne théorique O(h²) = O(1/N²)
    if erreurs[0] > 1e-15:
        pente_theorique = [erreurs[0] * (N_values[0] / N)**2 for N in N_values]
        plt.loglog(N_values, pente_theorique, 'b--', linewidth=2, 
                  label='O(h²) théorique')
    
    plt.grid(True, alpha=0.3)
    plt.xlabel('Nombre de volumes N')
    plt.ylabel('Erreur L∞')
    plt.title(f'Convergence Volumes Finis - {nom_cas}')
    plt.legend()
    
    # Annotation de l'ordre
    if ordre_moyen > 0:
        plt.text(0.05, 0.95, f'Ordre moyen: {ordre_moyen:.3f}', 
                transform=plt.gca().transAxes, fontsize=12,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
    
    plt.tight_layout()
    
    nom_fichier = f"{nom_cas.replace(' ', '_').replace('(', '').replace(')', '')}_VF_convergence.png"
    plt.savefig(os.path.join(dossier_figures, nom_fichier), dpi=300, bbox_inches='tight')
    plt.close()
    
    return erreurs, ordres, ordre_moyen


# ============================================================================
# SOLUTIONS EXACTES ET TERMES SOURCES POUR VALIDATION
# ============================================================================

def solution_exacte_sin_vf(x):
    """Solution exacte u(x) = sin(πx)"""
    return np.sin(np.pi * x)


def terme_source_sin_vf(x):
    """Terme source f(x) pour u(x) = sin(πx)"""
    return np.pi**2 * np.sin(np.pi * x)


def solution_exacte_cubique_vf(x):
    """Solution exacte u(x) = x³"""
    return x**3


def terme_source_cubique_vf(x):
    """Terme source f(x) pour u(x) = x³"""
    return -6.0 * x


def solution_exacte_quadratique_vf(x):
    """Solution exacte u(x) = x²"""
    return x**2


def terme_source_quadratique_vf(x):
    """Terme source f(x) pour u(x) = x²"""
    return -2.0 * np.ones_like(x)


def solution_exacte_lineaire_vf(x):
    """Solution exacte pour f(x) = 2x + 1 avec u(0)=0, u(1)=0"""
    return -x**3/3 - x**2/2 + (5/6)*x


def terme_source_lineaire_vf(x):
    """Terme source f(x) = 2x + 1"""
    return 2*x + 1


# ============================================================================
# CAS DE TEST PRÉDÉFINIS
# ============================================================================

def cas_sin_vf():
    """Cas test: u(x) = sin(πx) avec conditions homogènes"""
    return (solution_exacte_sin_vf, terme_source_sin_vf, 0.0, 0.0, "u(x) = sin(πx)")


def cas_cubique_vf():
    """Cas test: u(x) = x³"""
    return (solution_exacte_cubique_vf, terme_source_cubique_vf, 0.0, 1.0, "u(x) = x³")


def cas_quadratique_vf():
    """Cas test: u(x) = x²"""
    return (solution_exacte_quadratique_vf, terme_source_quadratique_vf, 0.0, 1.0, "u(x) = x²")


def cas_lineaire_vf():
    """Cas test: source linéaire f(x) = 2x + 1"""
    return (solution_exacte_lineaire_vf, terme_source_lineaire_vf, 0.0, 0.0, "f(x) = 2x + 1")


if __name__ == "__main__":
    """
    Tests de démonstration du solveur Volumes Finis
    """
    print("🔬 DÉMONSTRATION SOLVEUR VOLUMES FINIS 1D")
    print("=" * 60)
    
    # Test cas sin(πx)
    print("\n📊 Test 1: u(x) = sin(πx)")
    sol_func, src_func, u0, u1, nom = cas_sin_vf()
    
    for N in [10, 20, 40]:
        u_num, x = resoudre_equation_diff_vf(src_func, N, u0, u1)
        erreur = erreur_Linfini_vf(u_num, sol_func, x)
        print(f"   N={N:2d}: Erreur = {erreur:.2e}")
    
    # Test de convergence
    print(f"\n📈 Analyse de convergence...")
    N_values = [10, 20, 40, 80]
    erreurs, ordres, ordre_moyen = analyser_convergence_vf(
        sol_func, src_func, u0, u1, N_values, nom, "test_figures"
    )
    
    print(f"   Ordre de convergence moyen: {ordre_moyen:.3f}")
    print(f"   Ordre théorique attendu: 2.000")
    
    if abs(ordre_moyen - 2.0) < 0.3:
        print("   ✅ Convergence O(h²) validée !")
    else:
        print("   ⚠️ Convergence à vérifier...")
    
    print("\n🎯 Solveur Volumes Finis prêt pour validation complète !")