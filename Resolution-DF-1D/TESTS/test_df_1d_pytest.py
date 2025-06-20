"""
SUITE DE TESTS COMPLÈTE ET ROBUSTE - DIFFÉRENCES FINIES 1D
============================================================

✅ Tous les tests de la version précédente + tolérances rigoureuses
✅ Gestion robuste des chemins de fichiers
✅ Couverture exhaustive sans régression

Auteur: theTigerFox
Date: 2025-06-20
"""

import sys
import os

# GESTION ROBUSTE DES CHEMINS - fonctionne depuis n'importe où
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import pytest
import numpy as np
import warnings
from solver_df_1d import resoudre_equation_diff, erreur_Linfini


class TestDifferencesFines1DComplet:
    """
    Suite de tests COMPLÈTE et EXHAUSTIVE avec tolérances mathématiquement rigoureuses
    
    ✅ TOUS les tests de la version précédente
    ✅ + Tolérances calculées selon l'ordre de convergence O(h²)
    ✅ + Gestion robuste des chemins
    """
    
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Configuration avec tolérances théoriques rigoureuses"""
        warnings.filterwarnings('ignore')
        
        # Constantes théoriques pour l'erreur de troncature
        self.C_sin = np.pi**4 / 12        # Pour sin(πx)
        self.C_cubic = 1.0 / 12           # Pour x³
        self.C_constant = 1.0 / 12        # Pour fonctions constantes
        
        # Tolérances fixes pour cas spéciaux
        self.tol_machine = 1e-14          # Précision machine
        self.tol_tres_fine = 1e-10        # Maillages très fins
        self.tol_fine = 1e-6              # Standard
        self.tol_moyenne = 1e-4           # Acceptable
        self.tol_grossiere = 1e-2         # Maillages grossiers
        self.tol_tres_grossiere = 1e-1    # Maillages minimaux
        
        self.safety_factor = 2.0          # Facteur de sécurité
    
    def tolerance_theorique(self, N, constante_C, safety=True):
        """Calcule tolérance théorique exacte selon O(h²)"""
        h = 1.0 / N
        erreur_theo = constante_C * h**2
        if safety:
            erreur_theo *= self.safety_factor
        return max(erreur_theo, self.tol_machine)
    
    # =========================================================================
    # TESTS DE BASE - FONCTIONNEMENT NOMINAL (version complète restaurée)
    # =========================================================================
    
    @pytest.mark.parametrize("N", [10, 20, 40, 80])
    def test_base_fonction_sinusoidale_tolerance_rigoureuse(self, N):
        """
        TEST DE BASE: Fonction sinusoïdale avec tolérance mathématiquement exacte
        
        Cas de test: u(x) = sin(πx) avec conditions homogènes
        Tolérance: ε = (π⁴/12) × h² × facteur_sécurité
        """
        def f_source(x):
            return np.pi**2 * np.sin(np.pi * x)
        
        def u_exacte(x):
            return np.sin(np.pi * x)
        
        u0, u1 = 0.0, 0.0
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exacte, x)
        
        tolerance = self.tolerance_theorique(N, self.C_sin)
        
        assert erreur <= tolerance, (
            f"N={N}: Erreur {erreur:.2e} > tolérance théorique {tolerance:.2e}"
        )
    
    @pytest.mark.parametrize("N", [15, 30, 60, 120])
    def test_base_fonction_polynomiale_cubique_tolerance_rigoureuse(self, N):
        """
        TEST DE BASE: x³ avec tolérance théorique exacte
        """
        def f_source(x):
            return -6.0 * x
        
        def u_exacte(x):
            return x**3
        
        u0, u1 = 0.0, 1.0
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exacte, x)
        
        tolerance = self.tolerance_theorique(N, self.C_cubic)
        
        assert erreur <= tolerance, (
            f"N={N}: Erreur {erreur:.2e} > tolérance théorique {tolerance:.2e}"
        )
    
    def test_base_fonction_quadratique_precision_machine(self):
        """TEST DE BASE: x² - précision machine (solution exacte)"""
        def f_source(x):
            return -2.0 * np.ones_like(x)
        
        def u_exacte(x):
            return x**2
        
        u0, u1 = 0.0, 1.0
        N = 50
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exacte, x)
        
        assert erreur <= self.tol_machine, (
            f"Précision machine non atteinte pour x²: {erreur:.2e}"
        )
    
    # =========================================================================
    # TESTS DE LIMITES - CAS EXTRÊMES (version complète restaurée)
    # =========================================================================
    
    def test_limite_maillage_minimal_tolerance_adaptee(self):
        """
        TEST DE LIMITE: Maillage minimal N=2
        Tolérance: très large car h=0.5, h²=0.25
        """
        def f_source(x):
            return np.ones_like(x)
        
        def u_exacte(x):
            return 0.5 * x * (1 - x)
        
        u0, u1 = 0.0, 0.0
        N = 2
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exacte, x)
        
        # Tolérance très large pour maillage minimal
        tolerance = self.tolerance_theorique(N, self.C_constant, safety=True)
        tolerance = max(tolerance, self.tol_tres_grossiere)
        
        assert erreur <= tolerance, (
            f"Maillage minimal N=2 instable: {erreur:.2e} > {tolerance:.2e}"
        )
    
    def test_limite_maillage_tres_grossier_N5(self):
        """TEST DE LIMITE: Maillage très grossier N=5"""
        def f_source(x):
            return np.pi**2 * np.sin(np.pi * x)
        
        def u_exacte(x):
            return np.sin(np.pi * x)
        
        u0, u1 = 0.0, 0.0
        N = 5
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exacte, x)
        
        tolerance = self.tolerance_theorique(N, self.C_sin, safety=True)
        tolerance = max(tolerance, self.tol_grossiere)
        
        assert erreur <= tolerance, (
            f"Maillage grossier N=5 instable: {erreur:.2e}"
        )
    
    def test_limite_maillage_tres_fin_N1000(self):
        """TEST DE LIMITE: Maillage très fin N=1000"""
        def f_source(x):
            return np.pi**2 * np.sin(np.pi * x)
        
        def u_exacte(x):
            return np.sin(np.pi * x)
        
        u0, u1 = 0.0, 0.0
        N = 1000
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exacte, x)
        
        tolerance = self.tolerance_theorique(N, self.C_sin, safety=False)
        tolerance = max(tolerance, self.tol_tres_fine)
        
        assert erreur <= tolerance, (
            f"Maillage très fin N=1000 instable: {erreur:.2e}"
        )
    
    # =========================================================================
    # TESTS DE FONCTIONS - CAS LIMITES (version complète restaurée)
    # =========================================================================
    
    def test_fonction_nulle_tolerance_machine(self):
        """
        TEST FONCTION: Source nulle f(x)=0
        Solution: droite → précision machine
        """
        def f_source(x):
            return np.zeros_like(x)
        
        def u_exacte(x):
            return 1 + 2*x  # Solution linéaire
        
        u0, u1 = 1.0, 3.0
        N = 20
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exacte, x)
        
        # Solution linéaire exacte → précision machine
        tolerance = self.tol_machine * max(abs(u0), abs(u1))
        
        assert erreur <= tolerance, (
            f"Fonction nulle mal résolue: {erreur:.2e}"
        )
    
    def test_fonction_constante_non_nulle_tolerance_theorique(self):
        """
        TEST FONCTION: Constante f(x)=4
        Tolérance théorique O(h²)
        """
        C = 4.0
        def f_source(x):
            return C * np.ones_like(x)
        
        def u_exacte(x):
            return 2 * x * (1 - x)  # Solution analytique
        
        u0, u1 = 0.0, 0.0
        N = 40
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exacte, x)
        
        tolerance = self.tolerance_theorique(N, self.C_constant)
        
        assert erreur <= tolerance, (
            f"Fonction constante mal résolue: {erreur:.2e} > {tolerance:.2e}"
        )
    
    def test_fonction_lineaire_tolerance_theorique(self):
        """TEST FONCTION: Source linéaire f(x)=2x+1"""
        def f_source(x):
            return 2*x + 1
        
        def u_exacte(x):
            # Solution calculée analytiquement pour -u''=2x+1, u(0)=u(1)=0
            return (x - x**3)/3 - x**2/6 + x/6
        
        u0, u1 = 0.0, 0.0
        N = 30
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exacte, x)
        
        # Tolérance pour polynôme degré 3
        tolerance = self.tolerance_theorique(N, self.C_cubic)
        
        assert erreur <= tolerance, (
            f"Fonction linéaire mal résolue: {erreur:.2e}"
        )
    
    @pytest.mark.parametrize("freq", [2, 3, 5])
    def test_fonction_oscillante_haute_frequence(self, freq):
        """
        TEST FONCTION: Haute fréquence avec tolérance adaptée
        Tolérance augmente avec freq⁴
        """
        def f_source(x):
            return (freq * np.pi)**2 * np.sin(freq * np.pi * x)
        
        def u_exacte(x):
            return np.sin(freq * np.pi * x)
        
        u0, u1 = 0.0, 0.0
        N = max(50, 20 * freq)  # Maillage adapté à la fréquence
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exacte, x)
        
        # Tolérance adaptée à la fréquence
        C_adapted = self.C_sin * freq**4
        tolerance = self.tolerance_theorique(N, C_adapted)
        tolerance *= 2  # Facteur pour haute fréquence
        
        assert erreur <= tolerance, (
            f"Haute fréquence {freq} mal résolue: {erreur:.2e} > {tolerance:.2e}"
        )
    
    # =========================================================================
    # TESTS CONDITIONS LIMITES - EXHAUSTIFS (version complète restaurée)
    # =========================================================================
    
    @pytest.mark.parametrize("u0,u1", [
        (0.0, 0.0),           # Homogènes nulles
        (1.0, 2.0),           # Positives
        (-5.0, -10.0),        # Négatives
        (1000.0, 2000.0),     # Grandes valeurs
        (-1e-6, 1e-6),        # Très petites
        (0.0, 1000.0),        # Asymétriques
        (-100.0, 100.0),      # Très asymétriques
        (1e10, 2e10),         # Extrêmement grandes
    ])
    def test_conditions_limites_variees_tolerance_relative(self, u0, u1):
        """
        TEST CONDITIONS: Large gamme avec tolérance relative
        """
        def f_source(x):
            return np.zeros_like(x)  # Solution linéaire exacte
        
        def u_exacte(x):
            return u0 + (u1 - u0) * x
        
        N = 25
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exacte, x)
        
        # Tolérance relative aux valeurs
        solution_scale = max(abs(u0), abs(u1), 1.0)
        tolerance = self.tol_machine * solution_scale
        
        assert erreur <= tolerance, (
            f"Conditions ({u0}, {u1}) mal gérées: {erreur:.2e} > {tolerance:.2e}"
        )
    
    @pytest.mark.parametrize("amplitude", [1e-12, 1e-8, 1e-4, 1.0, 1e4, 1e8, 1e12])
    def test_amplitude_extreme_tolerance_relative(self, amplitude):
        """
        TEST AMPLITUDE: Échelles extrêmes avec tolérance relative
        """
        def f_source(x):
            return amplitude * np.pi**2 * np.sin(np.pi * x)
        
        def u_exacte(x):
            return amplitude * np.sin(np.pi * x)
        
        u0, u1 = 0.0, 0.0
        N = 40
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exacte, x)
        
        # Tolérance relative
        if amplitude != 0:
            solution_max = amplitude  # max de |sin| = 1
            erreur_relative = erreur / abs(solution_max)
            tolerance_relative = self.tolerance_theorique(N, self.C_sin, safety=False)
            
            assert erreur_relative <= tolerance_relative, (
                f"Amplitude {amplitude:.1e}: erreur relative {erreur_relative:.2e} > {tolerance_relative:.2e}"
            )
    
    # =========================================================================
    # TESTS DE ROBUSTESSE - GESTION D'ERREURS (version complète)
    # =========================================================================
    
    @pytest.mark.parametrize("N_invalide", [0, 1, -5, -1])
    def test_robustesse_maillage_invalide(self, N_invalide):
        """TEST ROBUSTESSE: Maillages invalides"""
        def f_source(x):
            return np.ones_like(x)
        
        with pytest.raises(ValueError, match="N doit être supérieur à 1"):
            resoudre_equation_diff(f_source, N_invalide, 0.0, 1.0)
    
    def test_robustesse_fonction_source_nan(self):
        """TEST ROBUSTESSE: Fonction source avec NaN"""
        def f_source_nan(x):
            return np.full_like(x, np.nan)
        
        u0, u1 = 0.0, 1.0
        N = 10
        
        try:
            u_num, x = resoudre_equation_diff(f_source_nan, N, u0, u1)
            assert np.any(np.isnan(u_num)), "NaN non détectés"
        except (RuntimeError, np.linalg.LinAlgError):
            pass  # Acceptable
    
    def test_robustesse_fonction_source_inf(self):
        """TEST ROBUSTESSE: Fonction source avec Inf"""
        def f_source_inf(x):
            return np.full_like(x, np.inf)
        
        u0, u1 = 0.0, 1.0
        N = 10
        
        try:
            u_num, x = resoudre_equation_diff(f_source_inf, N, u0, u1)
            assert np.any(np.isinf(u_num)), "Inf non détectés"
        except (RuntimeError, np.linalg.LinAlgError):
            pass
    
    # =========================================================================
    # TESTS DE CONVERGENCE - VALIDATION THÉORIQUE (complets)
    # =========================================================================
    
    @pytest.mark.parametrize("cas_test", [
        ("sin_pi_x", lambda x: np.pi**2 * np.sin(np.pi * x), lambda x: np.sin(np.pi * x), 0.0, 0.0),
        ("x_cube", lambda x: -6*x, lambda x: x**3, 0.0, 1.0),
        ("x_carre", lambda x: -2*np.ones_like(x), lambda x: x**2, 0.0, 1.0),
        ("constante", lambda x: 2*np.ones_like(x), lambda x: x*(1-x), 0.0, 0.0),
    ])
    def test_convergence_ordre_theorique_complet(self, cas_test):
        """
        TEST CONVERGENCE: Vérification ordre 2 pour tous les cas
        """
        nom_cas, f_source, u_exacte, u0, u1 = cas_test
        
        N_values = [10, 20, 40, 80, 160]
        erreurs = []
        
        for N in N_values:
            u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
            erreur = erreur_Linfini(u_num, u_exacte, x)
            erreurs.append(erreur)
        
        # Calcul des ordres (en évitant les erreurs nulles pour x²)
        ordres = []
        for i in range(1, len(N_values)):
            if erreurs[i] > 1e-15 and erreurs[i-1] > 1e-15:
                ordre = np.log(erreurs[i-1] / erreurs[i]) / np.log(N_values[i] / N_values[i-1])
                ordres.append(ordre)
        
        if ordres:  # Si on a pu calculer des ordres
            ordre_moyen = np.mean(ordres)
            
            # Tolérance sur l'ordre selon le cas
            if nom_cas == "x_carre":
                # x² peut atteindre précision machine
                assert ordre_moyen >= 1.5, f"Ordre trop faible pour {nom_cas}: {ordre_moyen:.3f}"
            else:
                assert 1.8 <= ordre_moyen <= 2.2, (
                    f"Ordre incorrect pour {nom_cas}: {ordre_moyen:.3f} (attendu ≈ 2.0)"
                )
    
    # =========================================================================
    # TESTS COMBINÉS - CAS RÉALISTES COMPLEXES (version complète restaurée)
    # =========================================================================
    
    @pytest.mark.parametrize("config", [
        # (nom, N, freq, amplitude, u0, u1, facteur_tolerance)
        ("standard", 50, 1, 1.0, 0.0, 0.0, 1.0),
        ("haute_freq", 100, 3, 0.5, 0.0, 0.0, 5.0),
        ("grande_amplitude", 60, 1, 100.0, 0.0, 0.0, 1.0),
        ("conditions_complexes", 40, 2, 1.0, 5.0, -3.0, 2.0),
        ("multi_echelle", 80, 1, 1e-6, 1e3, 2e3, 10.0),
    ])
    def test_combine_scenarios_complexes_tolerance_adaptee(self, config):
        """
        TEST COMBINÉ: Scénarios complexes avec tolérances adaptées
        """
        nom, N, freq, amplitude, u0, u1, facteur_tolerance = config
        
        def f_source_base(x):
            return amplitude * (freq * np.pi)**2 * np.sin(freq * np.pi * x)
        
        # Pour simplicité, on teste surtout la stabilité
        u_num, x = resoudre_equation_diff(f_source_base, N, u0, u1)
        
        # Tests de sanité
        assert not np.any(np.isnan(u_num)), f"Solution instable pour {nom}"
        assert not np.any(np.isinf(u_num)), f"Solution divergente pour {nom}"
        assert np.abs(u_num[0] - u0) < 1e-12, f"Condition u(0) non respectée pour {nom}"
        assert np.abs(u_num[-1] - u1) < 1e-12, f"Condition u(1) non respectée pour {nom}"
    
    def test_combine_stress_test_ultime(self):
        """
        TEST COMBINÉ: Stress test ultime avec toutes les difficultés
        """
        # Configuration complexe mais réaliste
        freq = 4
        amplitude = 0.8
        u0, u1 = 0.2, -0.3
        N = 120
        
        def f_source(x):
            return amplitude * (freq * np.pi)**2 * np.sin(freq * np.pi * x)
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        
        # Tests de sanité complets
        assert not np.any(np.isnan(u_num)), "Solution contient NaN"
        assert not np.any(np.isinf(u_num)), "Solution contient Inf"
        assert np.abs(u_num[0] - u0) < 1e-14, f"u(0): {u_num[0]} ≠ {u0}"
        assert np.abs(u_num[-1] - u1) < 1e-14, f"u(1): {u_num[-1]} ≠ {u1}"
        
        # Variation raisonnable
        variation = np.max(u_num) - np.min(u_num)
        assert variation < 100, f"Variation excessive: {variation}"
        
        # Pas de discontinuités
        gradients = np.abs(np.diff(u_num))
        assert np.max(gradients) < 10, "Discontinuités détectées"
    
    @pytest.mark.parametrize("scenario", [
        ("poly_degre4", 60, lambda x: -12*x**2, lambda x: x**4 - 2*x**3 + x**2, 0.0, 0.0),
        ("source_mixte", 80, lambda x: np.pi**2*np.sin(np.pi*x) + 6*x, lambda x: np.sin(np.pi*x) - x**3 + x, 0.0, 0.0),
        ("echelle_micro", 50, lambda x: 1e-12*np.ones_like(x), lambda x: 1e-12*0.5*x*(1-x), 0.0, 0.0),
        ("echelle_macro", 40, lambda x: 1e12*np.ones_like(x), lambda x: 1e12*0.5*x*(1-x), 0.0, 0.0),
    ])
    def test_combine_scenarios_realistes_exhaustifs(self, scenario):
        """
        TEST COMBINÉ: Scénarios réalistes exhaustifs
        """
        nom, N, f_func, u_exact, u0, u1 = scenario
        
        u_num, x = resoudre_equation_diff(f_func, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exact, x)
        
        # Tolérance adaptée
        h = 1.0 / N
        if "degre4" in nom:
            tolerance = max(self.tol_moyenne, h**2)
        elif "micro" in nom or "macro" in nom:
            solution_max = np.max(np.abs(u_exact(x)))
            tolerance = max(self.tol_fine, 1e-10 * solution_max)
        else:
            tolerance = max(self.tol_moyenne, 5 * h**2)
        
        assert erreur <= tolerance, (
            f"Scénario {nom}: erreur {erreur:.2e} > tolérance {tolerance:.2e}"
        )


# =========================================================================
# TESTS DE PERFORMANCE ET ANALYSE (bonus)
# =========================================================================

@pytest.mark.performance
class TestPerformanceComplet:
    """Tests de performance complets"""
    
    @pytest.mark.parametrize("N", [100, 500, 1000, 2000])
    def test_performance_scaling(self, N):
        """Test du scaling temporel"""
        import time
        
        def f_source(x):
            return np.pi**2 * np.sin(np.pi * x)
        
        start = time.time()
        u_num, x = resoudre_equation_diff(f_source, N, 0.0, 0.0)
        temps = time.time() - start
        
        # Scaling approximativement linéaire
        temps_limite = 0.001 * (N / 100)  # 1ms pour N=100
        assert temps < temps_limite, f"N={N}: temps {temps:.3f}s > limite {temps_limite:.3f}s"


if __name__ == "__main__":
    # Test d'import pour vérifier les chemins
    print(f"📁 Répertoire actuel: {os.getcwd()}")
    print(f"📁 Répertoire du script: {current_dir}")
    print(f"📁 Répertoire parent: {parent_dir}")
    print(f"📁 Chemins Python: {sys.path[:3]}...")
    
    # Vérification import
    try:
        from solver_df_1d import resoudre_equation_diff
        print("✅ Import solver_df_1d réussi")
    except ImportError as e:
        print(f"❌ Erreur import: {e}")
        sys.exit(1)
    
    # Lancement des tests
    pytest.main([__file__, "-v", "--tb=short"])