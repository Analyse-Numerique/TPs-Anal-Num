"""
Exécuteur de tests pour Volumes Finis 1D
Version finale avec rapport complet
"""

import sys
import os
import subprocess
import time
from datetime import datetime

# Gestion robuste des chemins
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


def run_tests_with_pytest():
    """Exécute tous les tests avec pytest et génère un rapport détaillé"""
    
    print("=" * 80)
    print("🧪 EXÉCUTION DES TESTS - VOLUMES FINIS 1D")
    print("=" * 80)
    
    # Configuration pytest
    test_file = "test_vf_1d_pytest.py"
    output_file = f"test_results_VF1D_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    # Commande pytest avec options détaillées
    cmd = [
        sys.executable, "-m", "pytest",
        test_file,
        "-v",                    # Verbose
        "--tb=short",           # Traceback court
        "--durations=10",       # Top 10 des tests les plus lents
        "--strict-markers",     # Marqueurs stricts
        "--disable-warnings",   # Désactiver warnings
        "--color=yes",          # Couleurs
        "-q"                    # Mode quiet pour l'output
    ]
    
    print(f"\n📋 Commande: {' '.join(cmd)}")
    print(f"📄 Fichier de test: {test_file}")
    print(f"📊 Fichier de sortie: {output_file}")
    
    # Exécution avec capture de sortie
    start_time = time.time()
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=current_dir,
            timeout=300  # Timeout 5 minutes
        )
        
        execution_time = time.time() - start_time
        
        # Sauvegarde des résultats
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("RAPPORT D'EXÉCUTION DES TESTS - VOLUMES FINIS 1D\n")
            f.write("=" * 80 + "\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Temps d'exécution: {execution_time:.2f} secondes\n")
            f.write(f"Code de retour: {result.returncode}\n\n")
            
            f.write("SORTIE STANDARD:\n")
            f.write("-" * 40 + "\n")
            f.write(result.stdout)
            f.write("\n\n")
            
            f.write("SORTIE D'ERREUR:\n")
            f.write("-" * 40 + "\n")
            f.write(result.stderr)
            f.write("\n\n")
            
            # Analyse des résultats
            f.write("ANALYSE DES RÉSULTATS:\n")
            f.write("-" * 40 + "\n")
            
            if result.returncode == 0:
                f.write("✅ TOUS LES TESTS ONT RÉUSSI\n")
            else:
                f.write("❌ CERTAINS TESTS ONT ÉCHOUÉ\n")
            
            f.write(f"Temps d'exécution: {execution_time:.2f}s\n")
            
            # Comptage des tests
            lines = result.stdout.split('\n')
            passed = sum(1 for line in lines if 'PASSED' in line)
            failed = sum(1 for line in lines if 'FAILED' in line)
            errors = sum(1 for line in lines if 'ERROR' in line)
            
            f.write(f"Tests réussis: {passed}\n")
            f.write(f"Tests échoués: {failed}\n")
            f.write(f"Tests en erreur: {errors}\n")
            f.write(f"Total: {passed + failed + errors}\n")
        
        # Affichage des résultats
        print(f"\n⏱️  Temps d'exécution: {execution_time:.2f} secondes")
        print(f"📊 Code de retour: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ TOUS LES TESTS ONT RÉUSSI !")
        else:
            print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
            print("\nDétails des erreurs:")
            print(result.stderr)
        
        print(f"\n📄 Rapport complet sauvegardé dans: {output_file}")
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("⏰ TIMEOUT: Les tests ont pris trop de temps (>5 minutes)")
        return False
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        return False


def run_specific_test(test_name):
    """Exécute un test spécifique"""
    
    print(f"\n🎯 Exécution du test: {test_name}")
    
    cmd = [
        sys.executable, "-m", "pytest",
        f"test_vf_1d_pytest.py::{test_name}",
        "-v",
        "--tb=short"
    ]
    
    try:
        result = subprocess.run(cmd, cwd=current_dir, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def run_coverage_test():
    """Exécute les tests avec couverture de code"""
    
    print("\n📊 Exécution des tests avec couverture de code")
    
    cmd = [
        sys.executable, "-m", "pytest",
        "test_vf_1d_pytest.py",
        "--cov=../solver_vf_1d",
        "--cov-report=term-missing",
        "--cov-report=html",
        "-v"
    ]
    
    try:
        result = subprocess.run(cmd, cwd=current_dir, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erreur couverture: {e}")
        return False


def main():
    """Fonction principale"""
    
    print("🚀 DÉMARRAGE DE L'EXÉCUTEUR DE TESTS")
    print("=" * 50)
    
    # Vérification de l'environnement
    print("🔍 Vérification de l'environnement...")
    
    if not os.path.exists("test_vf_1d_pytest.py"):
        print("❌ Fichier de test non trouvé!")
        return False
    
    print("✅ Fichier de test trouvé")
    
    # Menu interactif
    while True:
        print("\n" + "=" * 50)
        print("MENU DES TESTS - VOLUMES FINIS 1D")
        print("=" * 50)
        print("1. 🧪 Exécuter tous les tests")
        print("2. 🎯 Exécuter un test spécifique")
        print("3. 📊 Tests avec couverture de code")
        print("4. 🚪 Quitter")
        
        choice = input("\nVotre choix (1-4): ").strip()
        
        if choice == "1":
            success = run_tests_with_pytest()
            if success:
                print("\n🎉 EXÉCUTION TERMINÉE AVEC SUCCÈS!")
            else:
                print("\n⚠️  EXÉCUTION TERMINÉE AVEC DES ÉCHECS")
                
        elif choice == "2":
            test_name = input("Nom du test (ex: TestVolumesFinis1DCorrige::test_base_fonction_sinusoidale): ").strip()
            if test_name:
                success = run_specific_test(test_name)
                if success:
                    print("✅ Test réussi!")
                else:
                    print("❌ Test échoué!")
            else:
                print("❌ Nom de test invalide")
                
        elif choice == "3":
            success = run_coverage_test()
            if success:
                print("✅ Couverture de code terminée!")
            else:
                print("❌ Erreur dans la couverture de code")
                
        elif choice == "4":
            print("👋 Au revoir!")
            break
            
        else:
            print("❌ Choix invalide")


if __name__ == "__main__":
    main() 