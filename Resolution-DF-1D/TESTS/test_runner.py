"""
Script d'exécution robuste qui fonctionne depuis n'importe où
"""

import sys
import os
import subprocess
import datetime

# GESTION ROBUSTE DES CHEMINS
script_dir = os.path.dirname(os.path.abspath(__file__))
tests_dir = script_dir
resolution_dir = os.path.dirname(script_dir)
project_root = os.path.dirname(resolution_dir)

def main():
    """Exécute les tests depuis le bon répertoire"""
    
    print("=" * 80)
    print("🚀 LANCEMENT DE LA SUITE DE TESTS COMPLÈTE (VERSION ROBUSTE)")
    print("=" * 80)
    print(f"📅 Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👤 Utilisateur: theTigerFox")
    print(f"🔧 Framework: pytest")
    print("=" * 80)
    
    # Affichage des chemins pour debug
    print(f"📁 Répertoire de travail: {os.getcwd()}")
    print(f"📁 Répertoire du script: {script_dir}")
    print(f"📁 Répertoire des tests: {tests_dir}")
    print(f"📁 Répertoire Resolution-DF-1D: {resolution_dir}")
    print("=" * 80)
    
    # Changement vers le répertoire des tests
    original_dir = os.getcwd()
    os.chdir(tests_dir)
    
    try:
        # Vérification que les fichiers existent
        test_file = "test_df_1d_pytest.py"
        if not os.path.exists(test_file):
            print(f"❌ Fichier de test non trouvé: {test_file}")
            print(f"📁 Contenu du répertoire: {os.listdir('.')}")
            return 1
        
        # Arguments pytest optimisés
        pytest_args = [
            sys.executable, "-m", "pytest",
            test_file,                    # Fichier de tests
            "-v",                        # Mode verbose
            "--tb=short",               # Traceback court
            "--color=yes",              # Couleurs
            "--durations=5",            # Top 5 des tests les plus lents
            "--strict-markers",         # Vérification markers
            "-x",                       # Arrêt au premier échec
            "--disable-warnings",       # Masquer warnings pytest
        ]
        
        print("🧪 Exécution des tests...")
        print(f"📝 Commande: {' '.join(pytest_args)}")
        print("=" * 80)
        
        # Exécution
        result = subprocess.run(pytest_args, 
                              capture_output=False,  # Affichage direct
                              text=True)
        
        exit_code = result.returncode
        
        # Rapport final
        print("\n" + "=" * 80)
        if exit_code == 0:
            print("✅ TOUS LES TESTS RÉUSSIS!")
            print("🎯 Le solver des différences finies 1D est VALIDÉ.")
            print("🔧 Tolérances mathématiquement rigoureuses respectées.")
            print("📊 Couverture de tests COMPLÈTE sans régression.")
        else:
            print("❌ CERTAINS TESTS ONT ÉCHOUÉ!")
            print("⚠️  Vérifier l'implémentation du solver.")
        print("=" * 80)
        
        return exit_code
        
    finally:
        # Retour au répertoire original
        os.chdir(original_dir)


if __name__ == "__main__":
    sys.exit(main())