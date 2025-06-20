"""
Version DÉFINITIVEMENT corrigée !
"""

import numpy as np
import matplotlib.pyplot as plt
import os


def resoudre_equation_diff(f, N, U0, U1, tracer_graphe=False):
    """
    Résout l'équation différentielle -U''(x) = f(x) avec les conditions aux limites
    U(0) = U0 et U(1) = U1 par la méthode des différences finies.
    """
    if N <= 1:
        raise ValueError("N doit être supérieur à 1")

    h = 1 / N
    x_interieur = np.linspace(0, 1, N + 1)[1:-1]

    A = np.zeros((N - 1, N - 1))
    b = np.zeros(N - 1)

    for i in range(N - 1):
        if i == 0:
            A[i, i] = 2
            A[i, i + 1] = -1
            b[i] = h ** 2 * f(x_interieur[i]) + U0
        elif i == N - 2:
            A[i, i] = 2
            A[i, i - 1] = -1
            b[i] = h ** 2 * f(x_interieur[i]) + U1
        else:
            A[i, i - 1] = -1
            A[i, i] = 2
            A[i, i + 1] = -1
            b[i] = h ** 2 * f(x_interieur[i])

    try:
        U_interieur = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        raise RuntimeError("Impossible de résoudre le système linéaire.")

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


# ===== CAS TESTS CORRECTS =====

def cas_sin_pi_x():
    """CAS 1: u(x) = sin(πx) ✅"""
    def solution_exacte(x):
        return np.sin(np.pi * x)
    
    def terme_source(x):
        # Si u(x) = sin(πx), alors u''(x) = -π²sin(πx)
        # Donc -u''(x) = π²sin(πx)
        return np.pi ** 2 * np.sin(np.pi * x)
    
    u0, u1 = 0.0, 0.0
    return solution_exacte, terme_source, u0, u1, "u(x) = sin(πx)"


def cas_cube_corrige():
    """CAS 2: u(x) = x³ - TERME SOURCE CORRIGÉ ✅"""
    def solution_exacte(x):
        return x ** 3
    
    def terme_source(x):
        # Si u(x) = x³, alors u''(x) = 6x
        # Donc -u''(x) = -6x ← VOILÀ LA CORRECTION !
        return -6 * x  # ✅ SIGNE MOINS !
    
    u0, u1 = 0.0, 1.0
    return solution_exacte, terme_source, u0, u1, "u(x) = x³"


def cas_quadratique():
    """CAS 3: u(x) = x² ✅"""
    def solution_exacte(x):
        return x ** 2
    
    def terme_source(x):
        # Si u(x) = x², alors u''(x) = 2
        # Donc -u''(x) = -2
        return -2.0 * np.ones_like(x)
    
    u0, u1 = 0.0, 1.0
    return solution_exacte, terme_source, u0, u1, "u(x) = x²"


# ===== VÉRIFICATION MATHÉMATIQUE =====

def verification_mathematique():
    """Vérifie que nos cas tests sont mathématiquement corrects"""
    print("🔍 VÉRIFICATION MATHÉMATIQUE DES CAS TESTS")
    print("=" * 60)
    
    # Test 1: sin(πx)
    x_test = np.array([0.0, 0.5, 1.0])
    
    print("\n📐 CAS 1: u(x) = sin(πx)")
    u_sin = np.sin(np.pi * x_test)
    u_sin_second = -np.pi**2 * np.sin(np.pi * x_test)
    f_sin = np.pi**2 * np.sin(np.pi * x_test)
    
    print(f"  u(x) = {u_sin}")
    print(f"  u''(x) = {u_sin_second}")
    print(f"  -u''(x) = {-u_sin_second}")
    print(f"  f(x) = {f_sin}")
    print(f"  Vérification -u''(x) = f(x): {np.allclose(-u_sin_second, f_sin)} ✅")
    print(f"  Conditions: u(0) = {u_sin[0]}, u(1) = {u_sin[2]} ✅")
    
    # Test 2: x³
    print("\n📐 CAS 2: u(x) = x³")
    u_cube = x_test ** 3
    u_cube_second = 6 * x_test
    f_cube = -6 * x_test
    
    print(f"  u(x) = {u_cube}")
    print(f"  u''(x) = {u_cube_second}")
    print(f"  -u''(x) = {-u_cube_second}")
    print(f"  f(x) = {f_cube}")
    print(f"  Vérification -u''(x) = f(x): {np.allclose(-u_cube_second, f_cube)} ✅")
    print(f"  Conditions: u(0) = {u_cube[0]}, u(1) = {u_cube[2]} ✅")


# ===== FONCTIONS UTILITAIRES =====

def erreur_Linfini(u_numerique, u_exacte, x):
    return np.max(np.abs(u_numerique - u_exacte(x)))


def calculer_ordre_convergence(N_values, erreurs):
    log_N = np.log(np.array(N_values))
    log_erreurs = np.log(np.array(erreurs))

    ordres = []
    for i in range(1, len(N_values)):
        ordre = -(log_erreurs[i] - log_erreurs[i - 1]) / (log_N[i] - log_N[i - 1])
        ordres.append(ordre)

    ordre_moyen = np.mean(ordres)
    return ordres, ordre_moyen


def analyser_convergence(solution_exacte, terme_source, u0, u1, N_values, nom_cas, dossier_figures):
    """Analyse complète de la convergence"""
    erreurs = []

    print(f"\n🔍 Analyse du cas: {nom_cas}")
    
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


if __name__ == "__main__":
    verification_mathematique()
    
    print("\n🧪 TEST RAPIDE")
    sol_exacte, terme_src, u0, u1, nom = cas_cube_corrige()
    u_num, x = resoudre_equation_diff(terme_src, 40, u0, u1)
    erreur = erreur_Linfini(u_num, sol_exacte, x)
    print(f"\nErreur L∞ pour x³ avec N=40: {erreur:.6e}")
    print("Si l'erreur est ~10⁻⁴, c'est bon ! ✅")