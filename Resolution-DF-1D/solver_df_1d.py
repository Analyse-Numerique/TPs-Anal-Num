"""
Solveur corrigé pour les différences finies 1D
CORRECTION du bug pour N=2 (maillage minimal)
"""

import numpy as np
import matplotlib.pyplot as plt
import os


def resoudre_equation_diff(f, N, U0, U1, tracer_graphe=False):
    """
    Résout l'équation différentielle -U''(x) = f(x) avec les conditions aux limites
    U(0) = U0 et U(1) = U1 par la méthode des différences finies.
    
    CORRECTION: Gestion correcte du cas N=2 (1 seul point intérieur)
    """
    if N <= 1:
        raise ValueError("N doit être supérieur à 1")

    h = 1 / N
    x_interieur = np.linspace(0, 1, N + 1)[1:-1]  # Points intérieurs
    n_interior = len(x_interieur)  # N-1 points intérieurs

    # Gestion spéciale pour N=2 (1 seul point intérieur)
    if n_interior == 1:
        # Cas simple: 1 équation, 1 inconnue
        A = np.array([[2.0]])
        b = np.array([h**2 * f(x_interieur[0]) + U0 + U1])
        U_interieur = np.linalg.solve(A, b)
    else:
        # Cas général: N-1 équations, N-1 inconnues
        A = np.zeros((n_interior, n_interior))
        b = np.zeros(n_interior)

        for i in range(n_interior):
            # Diagonale principale
            A[i, i] = 2.0
            
            # Super-diagonale (seulement si elle existe)
            if i < n_interior - 1:
                A[i, i + 1] = -1.0
                
            # Sous-diagonale (seulement si elle existe)
            if i > 0:
                A[i, i - 1] = -1.0
                
            # Second membre
            b[i] = h**2 * f(x_interieur[i])
            
            # Conditions aux limites
            if i == 0:
                b[i] += U0
            if i == n_interior - 1:
                b[i] += U1

        try:
            U_interieur = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            raise RuntimeError("Impossible de résoudre le système linéaire.")

    # Construction de la solution complète
    x = np.linspace(0, 1, N + 1)
    U = np.zeros(N + 1)
    U[0] = U0
    U[1:-1] = U_interieur
    U[-1] = U1
    
    if tracer_graphe:
        plt.figure(figsize=(10, 6))
        plt.plot(x, U, 'b-', linewidth=2)
        plt.grid(True)
        plt.xlabel('x')
        plt.ylabel('U(x)')
        plt.title('Solution de l\'équation -U\'\'(x) = f(x)')
        plt.show()

    return U, x


# ... (garde toutes les autres fonctions de l'ancien solver_df_1d.py)

def solution_exacte_sin(x):
    """Solution exacte u(x) = sin(πx)"""
    return np.sin(np.pi * x)


def solution_exacte_cube(x):
    """Solution exacte u(x) = x³"""
    return x ** 3


def terme_source_sin(x):
    """Terme source f(x) pour u(x) = sin(πx) dans -u''(x) = f(x)"""
    return np.pi ** 2 * np.sin(np.pi * x)


def terme_source_cube(x):
    """Terme source f(x) pour u(x) = x³ dans -u''(x) = f(x)"""
    return -6 * x  # SIGNE CORRECT


def erreur_Linfini(u_numerique, u_exacte, x):
    """Calcule l'erreur en norme L∞ entre la solution numérique et la solution exacte"""
    return np.max(np.abs(u_numerique - u_exacte(x)))


def calculer_ordre_convergence(N_values, erreurs):
    """Calcule l'ordre numérique de convergence à partir des erreurs pour différentes tailles de maillage"""
    log_N = np.log(np.array(N_values))
    log_erreurs = np.log(np.array(erreurs))

    ordres = []
    for i in range(1, len(N_values)):
        ordre = -(log_erreurs[i] - log_erreurs[i - 1]) / (log_N[i] - log_N[i - 1])
        ordres.append(ordre)

    ordre_moyen = np.mean(ordres)
    return ordres, ordre_moyen


def analyser_convergence(solution_exacte, terme_source, u0, u1, N_values, nom_cas, dossier_figures):
    """Analyse complète de la convergence pour un cas test donné"""
    erreurs = []

    for N in N_values:
        u_numerique, x = resoudre_equation_diff(terme_source, N, u0, u1, tracer_graphe=False)
        erreur = erreur_Linfini(u_numerique, solution_exacte, x)
        erreurs.append(erreur)

        # Tracé pour quelques valeurs de N
        if N in [10, 40, 160]:
            x_exact = np.linspace(0, 1, 1000)
            u_exact = solution_exacte(x_exact)

            plt.figure(figsize=(12, 8))
            
            plt.subplot(2, 1, 1)
            plt.plot(x, u_numerique, 'bo-', markersize=6, label=f'Solution numérique (N={N})')
            plt.plot(x_exact, u_exact, 'r-', linewidth=2, label='Solution exacte')
            plt.grid(True)
            plt.xlabel('x')
            plt.ylabel('u(x)')
            plt.title(f'{nom_cas} avec N = {N}')
            plt.legend()
            
            plt.subplot(2, 1, 2)
            error_points = np.abs(u_numerique - solution_exacte(x))
            plt.semilogy(x, error_points, 'go-', markersize=4)
            plt.grid(True)
            plt.xlabel('x')
            plt.ylabel('Erreur absolue (échelle log)')
            plt.title(f'Erreur pour N = {N}')
            
            plt.tight_layout()

            fichier = os.path.join(dossier_figures, f"{nom_cas.replace('(', '').replace(')', '').replace(' ', '_')}_N{N}.png")
            plt.savefig(fichier, dpi=300)
            plt.close()

    ordres, ordre_moyen = calculer_ordre_convergence(N_values, erreurs)

    # Graphique de convergence
    plt.figure(figsize=(10, 6))
    plt.loglog(N_values, erreurs, 'bo-', linewidth=2, markersize=8, label='Erreur calculée')
    plt.loglog(N_values, [erreurs[0] * (N_values[0] / N) ** 2 for N in N_values], 'r--',
               linewidth=2, label='Ordre 2 théorique')
    plt.grid(True)
    plt.xlabel('N')
    plt.ylabel('Erreur L∞')
    plt.title(f'Convergence pour {nom_cas}')
    plt.legend()
    plt.tight_layout()

    fichier = os.path.join(dossier_figures, f"{nom_cas.replace('(', '').replace(')', '').replace(' ', '_')}_convergence.png")
    plt.savefig(fichier, dpi=300)
    plt.close()

    return erreurs, ordres, ordre_moyen


# Définition des cas tests
def cas_sin_pi_x():
    """Cas test 1: u(x) = sin(πx)"""
    return solution_exacte_sin, terme_source_sin, 0.0, 0.0, "u(x) = sin(πx)"


def cas_cube_corrige():
    """Cas test 2: u(x) = x³"""
    return solution_exacte_cube, terme_source_cube, 0.0, 1.0, "u(x) = x³"


def cas_quadratique():
    """Cas test 3: u(x) = x²"""
    def solution_exacte_quad(x):
        return x**2
    
    def terme_source_quad(x):
        return -2.0 * np.ones_like(x)
    
    return solution_exacte_quad, terme_source_quad, 0.0, 1.0, "u(x) = x²"


if __name__ == "__main__":
    # Test du cas N=2 pour vérifier la correction
    print("🧪 Test correction N=2")
    def f_test(x):
        return np.ones_like(x)
    
    try:
        u_num, x = resoudre_equation_diff(f_test, 2, 0.0, 0.0)
        print(f"✅ N=2 fonctionne: solution = {u_num}")
    except Exception as e:
        print(f"❌ N=2 échoue encore: {e}")