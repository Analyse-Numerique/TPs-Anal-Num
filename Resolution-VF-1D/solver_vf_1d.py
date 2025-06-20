"""
Solveur pour les volumes finis 1D
Méthode des volumes finis pour l'équation -u''(x) = f(x)
"""

import numpy as np
import matplotlib.pyplot as plt
import os


def resoudre_equation_vf(f, N, U0, U1, tracer_graphe=False):
    """
    Résout l'équation différentielle -U''(x) = f(x) avec les conditions aux limites
    U(0) = U0 et U(1) = U1 par la méthode des volumes finis.
    
    Pour ce problème 1D simple, la méthode des volumes finis donne
    le même système que les différences finies centrées.
    """
    if N <= 1:
        raise ValueError("N doit être supérieur à 1")

    h = 1 / N
    # Points de discrétisation (centres des volumes)
    x_centres = np.linspace(h/2, 1-h/2, N)
    # Points aux interfaces (bords des volumes)
    x_interfaces = np.linspace(0, 1, N+1)

    # Gestion spéciale pour N=2 (1 seul volume intérieur)
    if N == 2:
        # Cas simple: 1 équation, 1 inconnue
        A = np.array([[2.0]])
        b = np.array([h**2 * f(x_centres[0]) + U0 + U1])
        U_centres = np.linalg.solve(A, b)
    else:
        # Cas général: N équations, N inconnues
        A = np.zeros((N, N))
        b = np.zeros(N)

        for i in range(N):
            # Diagonale principale
            A[i, i] = 2.0
            
            # Super-diagonale (seulement si elle existe)
            if i < N - 1:
                A[i, i + 1] = -1.0
                
            # Sous-diagonale (seulement si elle existe)
            if i > 0:
                A[i, i - 1] = -1.0
                
            # Second membre (intégration sur le volume)
            b[i] = h**2 * f(x_centres[i])
            
            # Conditions aux limites
            if i == 0:
                b[i] += U0
            if i == N - 1:
                b[i] += U1

        try:
            U_centres = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            raise RuntimeError("Impossible de résoudre le système linéaire.")

    # Construction de la solution complète (centres + interfaces)
    x_complet = np.concatenate([[0], x_centres, [1]])
    U_complet = np.concatenate([[U0], U_centres, [U1]])
    
    if tracer_graphe:
        plt.figure(figsize=(10, 6))
        plt.plot(x_complet, U_complet, 'b-o', linewidth=2, markersize=6)
        plt.grid(True)
        plt.xlabel('x')
        plt.ylabel('U(x)')
        plt.title('Solution de l\'équation -U\'\'(x) = f(x) - Méthode Volumes Finis')
        plt.show()

    return U_complet, x_complet, U_centres, x_centres


def resoudre_equation_vf_correcte(f, N, U0, U1, tracer_graphe=False):
    """
    Résout l'équation différentielle -U''(x) = f(x) avec les conditions aux limites
    U(0) = U0 et U(1) = U1 par la méthode des volumes finis CORRIGÉE.
    
    Pour les volumes finis, on intègre l'équation sur chaque volume de contrôle :
    ∫_V (-u'') dx = ∫_V f(x) dx
    
    En utilisant le théorème de la divergence : -[u']_i+1/2 + [u']_i-1/2 = h * f_i
    """
    if N <= 1:
        raise ValueError("N doit être supérieur à 1")

    h = 1 / N
    # Points de discrétisation (centres des volumes)
    x_centres = np.linspace(h/2, 1-h/2, N)
    # Points aux interfaces (bords des volumes)
    x_interfaces = np.linspace(0, 1, N+1)

    # Gestion spéciale pour N=2 (1 seul volume intérieur)
    if N == 2:
        # Cas simple: 1 équation, 1 inconnue
        A = np.array([[2.0]])
        b = np.array([h * f(x_centres[0]) + U0 + U1])
        U_centres = np.linalg.solve(A, b)
    else:
        # Cas général: N équations, N inconnues
        A = np.zeros((N, N))
        b = np.zeros(N)

        for i in range(N):
            # Diagonale principale
            A[i, i] = 2.0
            
            # Super-diagonale (seulement si elle existe)
            if i < N - 1:
                A[i, i + 1] = -1.0
                
            # Sous-diagonale (seulement si elle existe)
            if i > 0:
                A[i, i - 1] = -1.0
                
            # Second membre (intégration sur le volume)
            b[i] = h * f(x_centres[i])
            
            # Conditions aux limites
            if i == 0:
                b[i] += U0
            if i == N - 1:
                b[i] += U1

        try:
            U_centres = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            raise RuntimeError("Impossible de résoudre le système linéaire.")

    # Construction de la solution complète (centres + interfaces)
    x_complet = np.concatenate([[0], x_centres, [1]])
    U_complet = np.concatenate([[U0], U_centres, [U1]])
    
    if tracer_graphe:
        plt.figure(figsize=(10, 6))
        plt.plot(x_complet, U_complet, 'b-o', linewidth=2, markersize=6)
        plt.grid(True)
        plt.xlabel('x')
        plt.ylabel('U(x)')
        plt.title('Solution de l\'équation -U\'\'(x) = f(x) - Méthode Volumes Finis')
        plt.show()

    return U_complet, x_complet, U_centres, x_centres


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
    return -6 * x


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


def analyser_convergence_vf(solution_exacte, terme_source, u0, u1, N_values, nom_cas, dossier_figures):
    """Analyse complète de la convergence pour un cas test donné - Méthode Volumes Finis"""
    erreurs = []

    for N in N_values:
        u_numerique, x_complet, u_centres, x_centres = resoudre_equation_vf(terme_source, N, u0, u1, tracer_graphe=False)
        # Calcul de l'erreur sur les centres des volumes
        erreur = erreur_Linfini(u_centres, solution_exacte, x_centres)
        erreurs.append(erreur)

        # Tracé pour quelques valeurs de N
        if N in [10, 40, 160]:
            x_exact = np.linspace(0, 1, 1000)
            u_exact = solution_exacte(x_exact)

            plt.figure(figsize=(12, 8))
            
            plt.subplot(2, 1, 1)
            plt.plot(x_complet, u_numerique, 'bo-', markersize=6, label=f'Solution numérique VF (N={N})')
            plt.plot(x_exact, u_exact, 'r-', linewidth=2, label='Solution exacte')
            plt.grid(True)
            plt.xlabel('x')
            plt.ylabel('u(x)')
            plt.title(f'{nom_cas} - Volumes Finis avec N = {N}')
            plt.legend()
            
            plt.subplot(2, 1, 2)
            error_points = np.abs(u_centres - solution_exacte(x_centres))
            plt.semilogy(x_centres, error_points, 'go-', markersize=4)
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
    plt.loglog(N_values, erreurs, 'bo-', linewidth=2, markersize=8, label='Erreur calculée VF')
    plt.loglog(N_values, [erreurs[0] * (N_values[0] / N) ** 2 for N in N_values], 'r--',
               linewidth=2, label='Ordre 2 théorique')
    plt.grid(True)
    plt.xlabel('N')
    plt.ylabel('Erreur L∞')
    plt.title(f'Convergence Volumes Finis pour {nom_cas}')
    plt.legend()
    plt.tight_layout()

    fichier = os.path.join(dossier_figures, f"{nom_cas.replace('(', '').replace(')', '').replace(' ', '_')}_convergence.png")
    plt.savefig(fichier, dpi=300)
    plt.close()

    return erreurs, ordres, ordre_moyen


def verification_mathematique():
    """Vérification mathématique de la méthode des volumes finis"""
    print("🔍 Vérification mathématique - Méthode Volumes Finis")
    print("=" * 60)
    
    # Test avec solution exacte u(x) = x²
    def u_exacte_test(x):
        return x**2
    
    def f_test(x):
        return -2.0 * np.ones_like(x)
    
    N_test = 10
    u_num, x_comp, u_cent, x_cent = resoudre_equation_vf(f_test, N_test, 0.0, 1.0)
    u_exacte_centres = u_exacte_test(x_cent)
    
    erreur_max = np.max(np.abs(u_cent - u_exacte_centres))
    print(f"Test avec u(x) = x², N = {N_test}")
    print(f"Erreur maximale: {erreur_max:.2e}")
    
    if erreur_max < 1e-10:
        print("✅ Vérification mathématique réussie")
    else:
        print("⚠️  Vérification mathématique à revoir")
    
    print()


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
    print("🧪 Test correction N=2 - Volumes Finis")
    def f_test(x):
        return np.ones_like(x)
    
    try:
        u_num, x_comp, u_cent, x_cent = resoudre_equation_vf(f_test, 2, 0.0, 0.0)
        print(f"✅ N=2 fonctionne: solution = {u_cent}")
    except Exception as e:
        print(f"❌ N=2 échoue encore: {e}") 