"""
Exécuteur de tests pour Volumes Finis 1D
Identique au DF-1D mais adapté pour VF
"""

import sys
import os
import subprocess
import datetime

# Gestion robuste des chemins
script_dir = os.path.dirname(os.path.abspath(__file__))
tests_dir = script_dir
resolution_dir = os.path.dirname(script_dir)


def main():
    """Exécute les tests VF avec affichage simple en temps réel"""
    
    print("=" * 80)
    print("🧪 EXÉCUTION DES TESTS - VOLUMES FINIS 1D")
    print("=" * 80)
    print(f"📅 Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👤 Utilisateur: theTigerFox")
    print(f"🔬 Méthode: Volumes Finis")
    print("=" * 80)
    
    # Changement vers le répertoire des tests
    original_dir = os.getcwd()
    os.chdir(tests_dir)
    
    try:
        # Vérification fichier de test
        test_file = "test_vf_1d_pytest.py"
        if not os.path.exists(test_file):
            print(f"❌ Fichier de test non trouvé: {test_file}")
            print(f"📁 Contenu: {os.listdir('.')}")
            return 1
        
        # Arguments pytest pour développement
        pytest_args = [
            sys.executable, "-m", "pytest",
            test_file,
            "-v",                       # Verbose
            "--tb=short",              # Traceback court
            "--color=yes",             # Couleurs
            "-x",                      # Arrêt au premier échec
            "--disable-warnings",      # Pas de warnings
        ]
        
        print("🚀 Lancement des tests Volumes Finis...")
        print("-" * 40)
        
        # Exécution avec affichage direct
        result = subprocess.run(pytest_args)
        exit_code = result.returncode
        
        # Résumé simple
        print("\n" + "=" * 80)
        if exit_code == 0:
            print("✅ TOUS LES TESTS VF RÉUSSIS !")
            print("🎯 Solveur Volumes Finis validé")
        else:
            print("❌ DES TESTS VF ONT ÉCHOUÉ")
            print("🔧 Vérifier les erreurs ci-dessus")
        print("=" * 80)
        
        return exit_code
        
    finally:
        os.chdir(original_dir)


if __name__ == "__main__":
    sys.exit(main())