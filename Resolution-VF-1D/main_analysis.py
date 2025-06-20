"""
Analyse complète des volumes finis 1D - VERSION FINALE
SAUVEGARDE DANS LE BON DOSSIER : Resolution-VF-1D/FIGURES/
"""

import os
import numpy as np
from datetime import datetime
import csv
from solver_vf_1d import (
    resoudre_equation_vf, analyser_convergence_vf, erreur_Linfini,
    cas_sin_pi_x, cas_cube_corrige, cas_quadratique, verification_mathematique
)


def main():
    """Analyse complète avec sauvegarde dans les BONS dossiers"""
    print("=" * 80)
    print("ANALYSE COMPLÈTE - VOLUMES FINIS 1D")
    print("=" * 80)
    
    # Vérification mathématique d'abord
    verification_mathematique()
    
    # Création du dossier FIGURES avec timestamp dans le BON endroit
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dossier_figures = os.path.join("FIGURES", f"run_{timestamp}")
    os.makedirs(dossier_figures, exist_ok=True)
    print(f"\n📁 Dossier figures: {dossier_figures}")
    
    # Valeurs de N pour l'étude de convergence
    N_values = [10, 20, 40, 80, 160, 320]
    
    # Liste pour stocker tous les résultats
    tous_resultats = []
    
    # ===== CAS 1: u(x) = sin(πx) =====
    print("\n" + "=" * 60)
    print("CAS 1: u(x) = sin(πx)")
    print("=" * 60)
    
    solution_exacte, terme_source, u0, u1, nom_cas = cas_sin_pi_x()
    erreurs_sin, ordres_sin, ordre_moyen_sin = analyser_convergence_vf(
        solution_exacte, terme_source, u0, u1, N_values, nom_cas, dossier_figures
    )
    
    tous_resultats.append({
        'nom': nom_cas,
        'N_values': N_values,
        'erreurs': erreurs_sin,
        'ordres': ordres_sin,
        'ordre_moyen': ordre_moyen_sin
    })
    
    # ===== CAS 2: u(x) = x³ =====
    print("\n" + "=" * 60)
    print("CAS 2: u(x) = x³ (CORRIGÉ)")
    print("=" * 60)
    
    solution_exacte, terme_source, u0, u1, nom_cas = cas_cube_corrige()
    erreurs_cube, ordres_cube, ordre_moyen_cube = analyser_convergence_vf(
        solution_exacte, terme_source, u0, u1, N_values, nom_cas, dossier_figures
    )
    
    tous_resultats.append({
        'nom': nom_cas,
        'N_values': N_values,
        'erreurs': erreurs_cube,
        'ordres': ordres_cube,
        'ordre_moyen': ordre_moyen_cube
    })
    
    # ===== CAS 3: u(x) = x² =====
    print("\n" + "=" * 60)
    print("CAS 3: u(x) = x² (CAS SIMPLE)")
    print("=" * 60)
    
    solution_exacte, terme_source, u0, u1, nom_cas = cas_quadratique()
    erreurs_quad, ordres_quad, ordre_moyen_quad = analyser_convergence_vf(
        solution_exacte, terme_source, u0, u1, N_values, nom_cas, dossier_figures
    )
    
    tous_resultats.append({
        'nom': nom_cas,
        'N_values': N_values,
        'erreurs': erreurs_quad,
        'ordres': ordres_quad,
        'ordre_moyen': ordre_moyen_quad
    })
    
    # ===== AFFICHAGE DES RÉSULTATS =====
    print("\n" + "=" * 80)
    print("RÉSUMÉ DES RÉSULTATS")
    print("=" * 80)
    
    for i, resultats in enumerate(tous_resultats, 1):
        print(f"\nCas {i}: {resultats['nom']}")
        print("-" * 60)
        print(f"{'N':<8} {'Erreur L-infini':<20} {'Ordre de conv.':<15}")
        print("-" * 60)
        for j, N in enumerate(resultats['N_values']):
            ordre_str = f"{resultats['ordres'][j - 1]:.4f}" if j > 0 else "N/A"
            print(f"{N:<8} {resultats['erreurs'][j]:<20.10e} {ordre_str:<15}")
        print("-" * 60)
        print(f"Ordre moyen de convergence: {resultats['ordre_moyen']:.4f}")
        
        # Évaluation qualitative
        if abs(resultats['ordre_moyen'] - 2.0) < 0.1:
            print("✅ Convergence EXCELLENTE (ordre ~2)")
        elif abs(resultats['ordre_moyen'] - 2.0) < 0.3:
            print("✅ Convergence BONNE")
        else:
            print("⚠️  Convergence à vérifier")
    
    # ===== SAUVEGARDE DES RÉSULTATS =====
    # Fichier CSV dans le bon dossier
    fichier_resultats = f"resultats_convergence_VF1D_{timestamp}.csv"
    with open(fichier_resultats, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Cas', 'N', 'h', 'Erreur_L_infini', 'Ordre_convergence'])
        
        for resultats in tous_resultats:
            nom = resultats['nom']
            N_values = resultats['N_values']
            erreurs = resultats['erreurs']
            ordres = resultats['ordres']
            
            for j, N in enumerate(N_values):
                ordre = ordres[j - 1] if j > 0 else None
                writer.writerow([
                    nom, N, 1.0/N, erreurs[j], ordre
                ])
            
            # Ligne avec ordre moyen
            writer.writerow([nom, 'Ordre_moyen', '', '', resultats['ordre_moyen']])
            writer.writerow([])  # Ligne vide
    
    # Fichier texte formaté dans le bon dossier
    fichier_txt = f"rapport_convergence_VF1D_{timestamp}.txt"
    with open(fichier_txt, 'w', encoding='utf-8') as f:
        f.write("=" * 120 + "\n")
        f.write("RAPPORT D'ANALYSE - VOLUMES FINIS 1D\n")
        f.write("=" * 120 + "\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Utilisateur: theTigerFox\n")
        f.write(f"Équation résolue: -u''(x) = f(x) sur [0,1]\n")
        f.write(f"Méthode: Volumes finis centrés d'ordre 2\n")
        f.write(f"Tailles de maillage testées: {N_values}\n\n")
        
        for i, resultats in enumerate(tous_resultats, 1):
            nom = resultats['nom']
            N_values = resultats['N_values']
            erreurs = resultats['erreurs']
            ordres = resultats['ordres']
            ordre_moyen = resultats['ordre_moyen']
            
            f.write(f"CAS {i}: {nom}\n")
            f.write("-" * 100 + "\n")
            f.write(f"{'N':<8} {'h':<12} {'Erreur L-infini':<20} {'Ordre conv.':<15}\n")
            f.write("-" * 100 + "\n")
            
            for j, N in enumerate(N_values):
                ordre_str = f"{ordres[j - 1]:.4f}" if j > 0 else "N/A"
                f.write(f"{N:<8} {1.0/N:<12.6f} {erreurs[j]:<20.10e} {ordre_str:<15}\n")
            
            f.write("-" * 100 + "\n")
            f.write(f"Ordre moyen de convergence: {ordre_moyen:.4f}\n")
            f.write(f"Écart à la théorie (ordre 2): {abs(ordre_moyen - 2.0):.4f}\n")
            
            # Analyse qualitative détaillée
            if abs(ordre_moyen - 2.0) < 0.05:
                f.write("✅ EXCELLENT: Convergence parfaite d'ordre 2\n")
            elif abs(ordre_moyen - 2.0) < 0.1:
                f.write("✅ TRÈS BON: Convergence proche de l'ordre théorique\n")
            elif abs(ordre_moyen - 2.0) < 0.3:
                f.write("✅ BON: Convergence acceptable\n")
            else:
                f.write("⚠️  À VÉRIFIER: Convergence éloignée de la théorie\n")
            
            f.write("\n")
        
        f.write("\n" + "=" * 120 + "\n")
        f.write("CONCLUSIONS GÉNÉRALES\n")
        f.write("=" * 120 + "\n")
        f.write("La méthode des volumes finis centrés d'ordre 2 présente:\n")
        f.write("• Une convergence théorique d'ordre 2 pour les solutions régulières\n")
        f.write("• Une stabilité numérique satisfaisante\n")
        f.write("• Une précision adaptée aux problèmes étudiés\n")
        f.write("• Une approche conservative naturelle\n\n")
        
        ordres_moyens = [r['ordre_moyen'] for r in tous_resultats]
        ordre_global = np.mean(ordres_moyens)
        f.write(f"Ordre de convergence global: {ordre_global:.4f}\n")
        
        f.write(f"\nRapport généré le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print("\n" + "=" * 80)
    print("📁 FICHIERS GÉNÉRÉS")
    print("=" * 80)
    print(f"📊 Figures: {dossier_figures}/")
    print(f"📋 Données CSV: {fichier_resultats}")
    print(f"📄 Rapport détaillé: {fichier_txt}")
    
    print(f"\n🎯 ORDRE DE CONVERGENCE GLOBAL: {np.mean([r['ordre_moyen'] for r in tous_resultats]):.4f}")
    print("\n✅ ANALYSE TERMINÉE AVEC SUCCÈS !")


if __name__ == "__main__":
    main() 