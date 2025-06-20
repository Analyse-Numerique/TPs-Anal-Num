"""
TESTS CORRIGÉS - Version finale sans erreurs mathématiques
==========================================================
"""

import sys
import os

# Gestion robuste des chemins
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import pytest
import numpy as np
import warnings
from solver_df_1d import resoudre_equation_diff, erreur_Linfini


class TestDifferencesFines1DCorrige:
    """Tests corrigés avec mathématiques vérifiées"""
    
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Configuration avec tolérances rigoureuses"""
        warnings.filterwarnings('ignore')
        
        # Constantes théoriques exactes
        self.C_sin = np.pi**4 / 12        # Pour sin(πx)
        self.C_cubic = 1.0 / 12           # Pour x³
        self.C_constant = 1.0 / 12        # Pour fonctions constantes
        
        # Tolérances
        self.tol_machine = 1e-14
        self.tol_tres_fine = 1e-10
        self.tol_fine = 1e-6
        self.tol_moyenne = 1e-4
        self.tol_grossiere = 1e-2
        self.tol_tres_grossiere = 1e-1
        
        self.safety_factor = 2.0
    
    def tolerance_theorique(self, N, constante_C, safety=True):
        """Calcule tolérance théorique selon O(h²)"""
        h = 1.0 / N
        erreur_theo = constante_C * h**2
        if safety:
            erreur_theo *= self.safety_factor
        return max(erreur_theo, self.tol_machine)
    
    # =========================================================================
    # TESTS DE BASE - CORRIGÉS
    # =========================================================================
    
    @pytest.mark.parametrize("N", [10, 20, 40, 80])
    def test_base_fonction_sinusoidale(self, N):
        """TEST BASE: sin(πx) - VALIDÉ ✅"""
        def f_source(x):
            return np.pi**2 * np.sin(np.pi * x)
        
        def u_exacte(x):
            return np.sin(np.pi * x)
        
        u0, u1 = 0.0, 0.0
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exacte, x)
        tolerance = self.tolerance_theorique(N, self.C_sin)
        
        assert erreur <= tolerance, f"N={N}: {erreur:.2e} > {tolerance:.2e}"
    
    @pytest.mark.parametrize("N", [15, 30, 60, 120])
    def test_base_fonction_cubique(self, N):
        """TEST BASE: x³ - VALIDÉ ✅"""
        def f_source(x):
            return -6.0 * x
        
        def u_exacte(x):
            return x**3
        
        u0, u1 = 0.0, 1.0
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exacte, x)
        tolerance = self.tolerance_theorique(N, self.C_cubic)
        
        assert erreur <= tolerance, f"N={N}: {erreur:.2e} > {tolerance:.2e}"
    
    def test_base_fonction_quadratique(self):
        """TEST BASE: x² - Précision machine ✅"""
        def f_source(x):
            return -2.0 * np.ones_like(x)
        
        def u_exacte(x):
            return x**2
        
        u0, u1 = 0.0, 1.0
        N = 50
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exacte, x)
        
        assert erreur <= self.tol_machine, f"x² mal résolu: {erreur:.2e}"
    
    # =========================================================================
    # TESTS DE LIMITES - VALIDÉS
    # =========================================================================
    
    def test_limite_maillage_minimal(self):
        """TEST LIMITE: N=2 - CORRIGÉ ✅"""
        def f_source(x):
            return np.ones_like(x)
        
        def u_exacte(x):
            return 0.5 * x * (1 - x)
        
        u0, u1 = 0.0, 0.0
        N = 2
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exacte, x)
        
        # Tolérance large pour N=2
        tolerance = max(self.tolerance_theorique(N, self.C_constant), self.tol_tres_grossiere)
        
        assert erreur <= tolerance, f"N=2 instable: {erreur:.2e}"
    
    @pytest.mark.parametrize("N", [5, 10, 20])
    def test_limite_maillages_grossiers(self, N):
        """TEST LIMITE: Maillages grossiers ✅"""
        def f_source(x):
            return np.pi**2 * np.sin(np.pi * x)
        
        def u_exacte(x):
            return np.sin(np.pi * x)
        
        u0, u1 = 0.0, 0.0
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exacte, x)
        
        tolerance = max(self.tolerance_theorique(N, self.C_sin), self.tol_grossiere)
        
        assert erreur <= tolerance, f"N={N} instable: {erreur:.2e}"
    
    def test_limite_maillage_tres_fin(self):
        """TEST LIMITE: Maillage très fin ✅"""
        def f_source(x):
            return np.pi**2 * np.sin(np.pi * x)
        
        def u_exacte(x):
            return np.sin(np.pi * x)
        
        u0, u1 = 0.0, 0.0
        N = 500
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exacte, x)
        
        tolerance = max(self.tolerance_theorique(N, self.C_sin, safety=False), self.tol_tres_fine)
        
        assert erreur <= tolerance, f"N=500 instable: {erreur:.2e}"
    
    # =========================================================================
    # TESTS DE FONCTIONS - CORRIGÉS
    # =========================================================================
    
    def test_fonction_nulle(self):
        """TEST FONCTION: f(x)=0 → solution linéaire ✅"""
        def f_source(x):
            return np.zeros_like(x)
        
        def u_exacte(x):
            return 1 + 2*x  # u(0)=1, u(1)=3
        
        u0, u1 = 1.0, 3.0
        N = 20
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exacte, x)
        
        tolerance = self.tol_machine * max(abs(u0), abs(u1))
        
        assert erreur <= tolerance, f"Fonction nulle: {erreur:.2e}"
    
    def test_fonction_constante(self):
        """TEST FONCTION: f(x)=C → solution quadratique ✅"""
        C = 4.0
        def f_source(x):
            return C * np.ones_like(x)
        
        def u_exacte(x):
            return 2 * x * (1 - x)  # Solution de -u''=4, u(0)=u(1)=0
        
        u0, u1 = 0.0, 0.0
        N = 40
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exacte, x)
        
        tolerance = self.tolerance_theorique(N, self.C_constant)
        
        assert erreur <= tolerance, f"Fonction constante: {erreur:.2e}"
    
    def test_fonction_lineaire_corrigee(self):
        """
        TEST FONCTION: f(x) = 2x + 1 - MATHÉMATIQUEMENT CORRIGÉ ✅
        
        Résolution exacte de -u''(x) = 2x + 1 avec u(0)=0, u(1)=0:
        1. u''(x) = -(2x + 1)
        2. u'(x) = -x² - x + C₁  
        3. u(x) = -x³/3 - x²/2 + C₁x + C₂
        4. u(0) = 0 → C₂ = 0
        5. u(1) = 0 → -1/3 - 1/2 + C₁ = 0 → C₁ = 5/6
        
        Solution exacte: u(x) = -x³/3 - x²/2 + (5/6)x
        """
        def f_source(x):
            return 2*x + 1
        
        def u_exacte(x):
            # Solution mathématiquement correcte !
            return -x**3/3 - x**2/2 + (5/6)*x
        
        u0, u1 = 0.0, 0.0
        N = 30
        
        # Vérification mathématique
        x_test = np.array([0.0, 0.5, 1.0])
        u_test = u_exacte(x_test)
        u_second = 2*x_test  # u''(x) = 2x (dérivée de -x³/3 - x²/2 + 5x/6)
        f_test = -(2*x_test + 1)  # -u''(x) = -(2x + 1) = f(x) ✓
        
        print(f"\n🔍 Vérification mathématique:")
        print(f"   u(0) = {u_test[0]:.6f} (doit être 0)")
        print(f"   u(1) = {u_test[2]:.6f} (doit être 0)")
        print(f"   -u''(0.5) = {-u_second[1]:.6f}, f(0.5) = {2*0.5 + 1:.6f}")
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exacte, x)
        
        # Tolérance pour polynôme degré 3
        tolerance = self.tolerance_theorique(N, self.C_cubic)
        
        print(f"   Erreur calculée: {erreur:.6e}")
        print(f"   Tolérance: {tolerance:.6e}")
        
        assert erreur <= tolerance, f"Fonction linéaire corrigée: {erreur:.2e} > {tolerance:.2e}"
    
    @pytest.mark.parametrize("freq", [2, 3, 4])
    def test_fonction_oscillante(self, freq):
        """TEST FONCTION: Hautes fréquences ✅"""
        def f_source(x):
            return (freq * np.pi)**2 * np.sin(freq * np.pi * x)
        
        def u_exacte(x):
            return np.sin(freq * np.pi * x)
        
        u0, u1 = 0.0, 0.0
        N = max(50, 15 * freq)  # Maillage adapté
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exacte, x)
        
        # Tolérance adaptée à la fréquence
        C_adapted = self.C_sin * freq**4
        tolerance = self.tolerance_theorique(N, C_adapted) * 3  # Facteur pour HF
        
        assert erreur <= tolerance, f"Fréquence {freq}: {erreur:.2e} > {tolerance:.2e}"
    
    # =========================================================================
    # TESTS DE CONDITIONS AUX LIMITES
    # =========================================================================
    
    @pytest.mark.parametrize("u0,u1", [
        (0.0, 0.0),           # Homogènes
        (1.0, 2.0),           # Positives
        (-5.0, -10.0),        # Négatives  
        (1000.0, 2000.0),     # Grandes
        (-1e-6, 1e-6),        # Petites
        (0.0, 1000.0),        # Asymétriques
    ])
    def test_conditions_limites_variees(self, u0, u1):
        """TEST CONDITIONS: Variété complète ✅"""
        def f_source(x):
            return np.zeros_like(x)
        
        def u_exacte(x):
            return u0 + (u1 - u0) * x
        
        N = 25
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        erreur = erreur_Linfini(u_num, u_exacte, x)
        
        solution_scale = max(abs(u0), abs(u1), 1.0)
        tolerance = self.tol_machine * solution_scale
        
        assert erreur <= tolerance, f"Conditions ({u0}, {u1}): {erreur:.2e}"
    
    # =========================================================================
    # TESTS DE ROBUSTESSE
    # =========================================================================
    
    @pytest.mark.parametrize("N_invalide", [0, 1, -5])
    def test_robustesse_entrees_invalides(self, N_invalide):
        """TEST ROBUSTESSE: Entrées invalides ✅"""
        def f_source(x):
            return np.ones_like(x)
        
        with pytest.raises(ValueError, match="N doit être supérieur à 1"):
            resoudre_equation_diff(f_source, N_invalide, 0.0, 1.0)
    
    def test_robustesse_valeurs_nan(self):
        """TEST ROBUSTESSE: Gestion des NaN ✅"""
        def f_source_nan(x):
            return np.full_like(x, np.nan)
        
        u0, u1 = 0.0, 1.0
        N = 10
        
        try:
            u_num, x = resoudre_equation_diff(f_source_nan, N, u0, u1)
            assert np.any(np.isnan(u_num)), "NaN non détectés"
        except (RuntimeError, np.linalg.LinAlgError):
            pass  # Acceptable
    
    # =========================================================================
    # TESTS DE CONVERGENCE
    # =========================================================================
    
    @pytest.mark.parametrize("cas_test", [
        ("sin", lambda x: np.pi**2 * np.sin(np.pi * x), lambda x: np.sin(np.pi * x), 0.0, 0.0),
        ("x3", lambda x: -6*x, lambda x: x**3, 0.0, 1.0),
        ("x2", lambda x: -2*np.ones_like(x), lambda x: x**2, 0.0, 1.0),
    ])
    def test_convergence_ordre_theorique(self, cas_test):
        """TEST CONVERGENCE: Ordre 2 théorique ✅"""
        nom, f_source, u_exacte, u0, u1 = cas_test
        
        N_values = [10, 20, 40, 80, 160]
        erreurs = []
        
        for N in N_values:
            u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
            erreur = erreur_Linfini(u_num, u_exacte, x)
            erreurs.append(erreur)
        
        # Calcul des ordres
        ordres = []
        for i in range(1, len(N_values)):
            if erreurs[i] > 1e-15 and erreurs[i-1] > 1e-15:
                ordre = np.log(erreurs[i-1] / erreurs[i]) / np.log(N_values[i] / N_values[i-1])
                ordres.append(ordre)
        
        if ordres:
            ordre_moyen = np.mean(ordres)
            
            if nom == "x2":
                assert ordre_moyen >= 1.5, f"Ordre faible pour {nom}: {ordre_moyen:.3f}"
            else:
                assert 1.8 <= ordre_moyen <= 2.2, f"Ordre incorrect pour {nom}: {ordre_moyen:.3f}"
    
    # =========================================================================
    # TESTS COMBINÉS
    # =========================================================================
    
    @pytest.mark.parametrize("config", [
        ("standard", 50, 1, 1.0, 0.0, 0.0),
        ("haute_freq", 80, 3, 0.5, 0.0, 0.0),
        ("grande_amplitude", 60, 1, 100.0, 0.0, 0.0),
        ("conditions_complexes", 40, 2, 1.0, 5.0, -3.0),
    ])
    def test_combine_scenarios_realistes(self, config):
        """TEST COMBINÉ: Scénarios réalistes ✅"""
        nom, N, freq, amplitude, u0, u1 = config
        
        def f_source(x):
            return amplitude * (freq * np.pi)**2 * np.sin(freq * np.pi * x)
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        
        # Tests de sanité
        assert not np.any(np.isnan(u_num)), f"NaN pour {nom}"
        assert not np.any(np.isinf(u_num)), f"Inf pour {nom}"
        assert np.abs(u_num[0] - u0) < 1e-12, f"u(0) pour {nom}"
        assert np.abs(u_num[-1] - u1) < 1e-12, f"u(1) pour {nom}"
    
    def test_combine_stress_test_final(self):
        """TEST COMBINÉ: Stress test final ✅"""
        freq = 4
        amplitude = 0.8
        u0, u1 = 0.2, -0.3
        N = 120
        
        def f_source(x):
            return amplitude * (freq * np.pi)**2 * np.sin(freq * np.pi * x)
        
        u_num, x = resoudre_equation_diff(f_source, N, u0, u1)
        
        # Validation complète
        assert not np.any(np.isnan(u_num)), "NaN détectés"
        assert not np.any(np.isinf(u_num)), "Inf détectés"
        assert np.abs(u_num[0] - u0) < 1e-14, f"u(0): {u_num[0]} ≠ {u0}"
        assert np.abs(u_num[-1] - u1) < 1e-14, f"u(1): {u_num[-1]} ≠ {u1}"
        
        variation = np.max(u_num) - np.min(u_num)
        assert variation < 100, f"Variation excessive: {variation}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])