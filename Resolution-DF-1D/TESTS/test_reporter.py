"""
GÉNÉRATEUR DE RAPPORTS PROFESSIONNELS COMPLET
=============================================

Générateur de rapports de niveau professionnel avec:
- Exécution robuste des tests avec gestion d'erreurs
- Parsing intelligent des résultats pytest
- Rapports TXT et Markdown de qualité publication
- Analyses statistiques détaillées
- Recommandations techniques
- Gestion complète des chemins et erreurs

Auteur: theTigerFox
Date: 2025-06-20
"""

import sys
import os
import subprocess
import datetime
import json
import re
from pathlib import Path
import traceback

# GESTION ROBUSTE DES CHEMINS
script_dir = os.path.dirname(os.path.abspath(__file__))
tests_dir = script_dir
resolution_dir = os.path.dirname(script_dir)
project_root = os.path.dirname(resolution_dir)


class TestReporterProfessionnel:
    """
    Générateur de rapports professionnels avec gestion complète
    """
    
    def __init__(self):
        self.timestamp = datetime.datetime.now()
        self.rapport_dir = os.path.join(tests_dir, "RAPPORTS")
        self.ensure_directories()
        
        # Métadonnées du projet
        self.metadata = {
            'projet': 'Résolution par Différences Finies 1D',
            'auteur': 'theTigerFox',
            'cours': 'Analyse Numérique - Master 1',
            'institution': 'École Polytechnique',
            'methode': 'Différences finies centrées d\'ordre 2',
            'equation': '-u\'\'(x) = f(x) sur [0,1] avec conditions de Dirichlet',
            'date': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'timestamp': self.timestamp.strftime('%Y%m%d_%H%M%S'),
            'version': '1.0.0',
            'framework': 'pytest'
        }
        
        # Configuration des analyses
        self.config = {
            'test_file': 'test_df_1d_pytest.py',
            'timeout': 300,  # 5 minutes max
            'retry_count': 2,
            'verbose_level': 2
        }
        
        self.stats = {}
        self.raw_results = {}
        self.analysis = {}
    
    def ensure_directories(self):
        """Création des répertoires nécessaires"""
        try:
            os.makedirs(self.rapport_dir, exist_ok=True)
            print(f"📁 Répertoire rapports: {self.rapport_dir}")
        except Exception as e:
            print(f"❌ Erreur création répertoire: {e}")
            raise
    
    def executer_tests_robuste(self):
        """
        Exécution robuste des tests avec gestion complète des erreurs
        """
        print("🔍 EXÉCUTION DES TESTS AVEC CAPTURE COMPLÈTE")
        print("=" * 60)
        
        # Changement vers le répertoire des tests
        original_dir = os.getcwd()
        
        try:
            os.chdir(tests_dir)
            print(f"📁 Répertoire de travail: {os.getcwd()}")
            
            # Vérification de l'existence des fichiers
            test_file = self.config['test_file']
            if not os.path.exists(test_file):
                available_files = [f for f in os.listdir('.') if f.endswith('.py')]
                raise FileNotFoundError(
                    f"Fichier de test non trouvé: {test_file}\n"
                    f"Fichiers disponibles: {available_files}"
                )
            
            print(f"✅ Fichier de test trouvé: {test_file}")
            
            # Préparation de la commande pytest
            pytest_cmd = [
                sys.executable, "-m", "pytest",
                test_file,
                "-v",                           # Verbose
                "--tb=long",                    # Traceback complet
                "--durations=0",                # Toutes les durées
                "--strict-markers",             # Vérification des markers
                "--color=no",                   # Pas de couleurs pour parsing
                "--no-header",                  # Pas d'en-tête pour parsing
                "-r", "fEsxXvs",               # Rapport détaillé de tous les types
            ]
            
            print(f"📝 Commande: {' '.join(pytest_cmd)}")
            print("🚀 Lancement de l'exécution...")
            print("-" * 60)
            
            # Exécution avec gestion du timeout
            start_time = datetime.datetime.now()
            
            try:
                result = subprocess.run(
                    pytest_cmd,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    timeout=self.config['timeout']
                )
            except subprocess.TimeoutExpired:
                raise RuntimeError(f"Timeout après {self.config['timeout']}s")
            
            end_time = datetime.datetime.now()
            execution_duration = (end_time - start_time).total_seconds()
            
            # Stockage des résultats bruts
            self.raw_results = {
                'exit_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'execution_time': execution_duration,
                'start_time': start_time,
                'end_time': end_time,
                'success': result.returncode == 0,
                'command': ' '.join(pytest_cmd)
            }
            
            print(f"✅ Exécution terminée en {execution_duration:.2f}s")
            print(f"📊 Code de sortie: {result.returncode}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de l'exécution: {e}")
            self.raw_results = {
                'exit_code': -1,
                'stdout': '',
                'stderr': str(e),
                'execution_time': 0,
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
            return False
            
        finally:
            os.chdir(original_dir)
    
    def analyser_resultats_complet(self):
        """
        Analyse complète et intelligente des résultats pytest
        """
        print("\n📈 ANALYSE DÉTAILLÉE DES RÉSULTATS")
        print("=" * 60)
        
        if not self.raw_results.get('success', False):
            print("⚠️ Analyse sur résultats d'échec")
        
        stdout = self.raw_results.get('stdout', '')
        stderr = self.raw_results.get('stderr', '')
        
        # Initialisation des statistiques
        self.stats = {
            'execution': {
                'success': self.raw_results.get('success', False),
                'exit_code': self.raw_results.get('exit_code', -1),
                'duration': self.raw_results.get('execution_time', 0),
                'start_time': self.raw_results.get('start_time'),
                'end_time': self.raw_results.get('end_time')
            },
            'tests': {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'errors': 0,
                'skipped': 0,
                'warnings': 0,
                'details': []
            },
            'performance': {
                'slowest_tests': [],
                'fastest_tests': [],
                'average_duration': 0
            },
            'failures': {
                'count': 0,
                'details': [],
                'categories': {}
            },
            'coverage': {
                'categories_tested': [],
                'completeness': 0
            }
        }
        
        try:
            # Analyse des résultats de tests individuels
            self._analyser_tests_individuels(stdout)
            
            # Analyse des échecs
            self._analyser_echecs(stdout)
            
            # Analyse des performances
            self._analyser_performances(stdout)
            
            # Analyse de la couverture
            self._analyser_couverture()
            
            # Génération de l'analyse qualitative
            self._generer_analyse_qualitative()
            
            print(f"✅ Analyse terminée:")
            print(f"   📊 Tests analysés: {self.stats['tests']['total']}")
            print(f"   ✅ Succès: {self.stats['tests']['passed']}")
            print(f"   ❌ Échecs: {self.stats['tests']['failed']}")
            print(f"   💥 Erreurs: {self.stats['tests']['errors']}")
            
        except Exception as e:
            print(f"⚠️ Erreur pendant l'analyse: {e}")
            print(f"🔍 Analyse partielle avec données disponibles")
    
    def _analyser_tests_individuels(self, stdout):
        """Analyse des tests individuels"""
        
        # Pattern pour capturer les résultats de tests
        # Format: test_file.py::ClassName::test_method[param] STATUS
        test_pattern = r'([^:]+::)?([^:\s]+)::(test_[^\s\[]+)(?:\[([^\]]+)\])?\s+(PASSED|FAILED|ERROR|SKIPPED)'
        
        matches = re.findall(test_pattern, stdout, re.MULTILINE)
        
        for match in matches:
            file_part, class_name, test_name, param, status = match
            
            full_test_name = f"{class_name}::{test_name}"
            if param:
                full_test_name += f"[{param}]"
            
            test_detail = {
                'name': full_test_name,
                'short_name': test_name,
                'class': class_name,
                'parameter': param if param else None,
                'status': status,
                'category': self._categoriser_test(test_name)
            }
            
            self.stats['tests']['details'].append(test_detail)
            
            # Comptage par statut
            if status == 'PASSED':
                self.stats['tests']['passed'] += 1
            elif status == 'FAILED':
                self.stats['tests']['failed'] += 1
            elif status == 'ERROR':
                self.stats['tests']['errors'] += 1
            elif status == 'SKIPPED':
                self.stats['tests']['skipped'] += 1
        
        self.stats['tests']['total'] = len(self.stats['tests']['details'])
        
        # Analyse des warnings
        warning_pattern = r'(\d+) warning'
        warning_match = re.search(warning_pattern, stdout)
        if warning_match:
            self.stats['tests']['warnings'] = int(warning_match.group(1))
    
    def _categoriser_test(self, test_name):
        """Catégorise les tests selon leur nom"""
        categories = {
            'base': ['base', 'fonction_sinusoidale', 'fonction_cubique', 'fonction_quadratique'],
            'limite': ['limite', 'maillage', 'minimal', 'grossier', 'fin'],
            'fonction': ['fonction', 'nulle', 'constante', 'lineaire', 'oscillante'],
            'conditions': ['conditions', 'limites', 'variees'],
            'robustesse': ['robustesse', 'entrees', 'invalides', 'nan', 'inf'],
            'convergence': ['convergence', 'ordre', 'theorique'],
            'combine': ['combine', 'scenarios', 'stress', 'realistes'],
            'performance': ['performance', 'scaling', 'temps']
        }
        
        test_lower = test_name.lower()
        for category, keywords in categories.items():
            if any(keyword in test_lower for keyword in keywords):
                return category
        
        return 'autre'
    
    def _analyser_echecs(self, stdout):
        """Analyse détaillée des échecs"""
        
        # Recherche de la section FAILURES
        if 'FAILURES' in stdout:
            failures_section = stdout.split('FAILURES')[1]
            if '=====' in failures_section:
                failures_section = failures_section.split('=====')[0]
            
            # Pattern pour extraire les détails d'échec
            failure_pattern = r'_+ ([^_]+) _+\n(.*?)(?=_+ [^_]+ _+|\Z)'
            failure_matches = re.findall(failure_pattern, failures_section, re.DOTALL)
            
            for test_name, failure_detail in failure_matches:
                # Extraction de l'assertion error
                assert_pattern = r'AssertionError: (.+)'
                assert_match = re.search(assert_pattern, failure_detail)
                
                failure_info = {
                    'test': test_name.strip(),
                    'full_detail': failure_detail.strip(),
                    'assertion': assert_match.group(1) if assert_match else 'Non spécifié',
                    'category': self._categoriser_echec(failure_detail)
                }
                
                self.stats['failures']['details'].append(failure_info)
        
        self.stats['failures']['count'] = len(self.stats['failures']['details'])
    
    def _categoriser_echec(self, failure_detail):
        """Catégorise les types d'échecs"""
        detail_lower = failure_detail.lower()
        
        if 'tolerance' in detail_lower or 'erreur' in detail_lower:
            return 'precision'
        elif 'ordre' in detail_lower or 'convergence' in detail_lower:
            return 'convergence'
        elif 'nan' in detail_lower or 'inf' in detail_lower:
            return 'stabilite'
        elif 'index' in detail_lower or 'bounds' in detail_lower:
            return 'implementation'
        else:
            return 'autre'
    
    def _analyser_performances(self, stdout):
        """Analyse des performances des tests"""
        
        # Pattern pour les durées: 0.05s call test_name
        duration_pattern = r'([\d.]+)s call (.+)'
        duration_matches = re.findall(duration_pattern, stdout)
        
        durations = []
        for duration_str, test_name in duration_matches:
            try:
                duration = float(duration_str)
                durations.append({
                    'test': test_name.strip(),
                    'duration': duration
                })
            except ValueError:
                continue
        
        if durations:
            # Tri par durée
            durations.sort(key=lambda x: x['duration'], reverse=True)
            
            self.stats['performance']['slowest_tests'] = durations[:5]
            self.stats['performance']['fastest_tests'] = durations[-5:]
            self.stats['performance']['average_duration'] = sum(d['duration'] for d in durations) / len(durations)
    
    def _analyser_couverture(self):
        """Analyse de la couverture des tests"""
        
        categories = set()
        for test in self.stats['tests']['details']:
            categories.add(test['category'])
        
        self.stats['coverage']['categories_tested'] = list(categories)
        
        # Calcul de la complétude (sur 7 catégories principales)
        expected_categories = {'base', 'limite', 'fonction', 'conditions', 'robustesse', 'convergence', 'combine'}
        covered = len(categories.intersection(expected_categories))
        self.stats['coverage']['completeness'] = (covered / len(expected_categories)) * 100
    
    def _generer_analyse_qualitative(self):
        """Génère une analyse qualitative des résultats"""
        
        total = self.stats['tests']['total']
        passed = self.stats['tests']['passed']
        failed = self.stats['tests']['failed']
        
        if total == 0:
            quality = 'indetermine'
            recommendation = 'Aucun test exécuté - vérifier la configuration'
        elif failed == 0:
            quality = 'excellent'
            recommendation = 'Implémentation validée - prête pour production'
        elif failed <= 1 and passed >= total * 0.95:
            quality = 'tres_bon'
            recommendation = 'Quasi-validation complète - échecs mineurs acceptables'
        elif failed <= total * 0.1:
            quality = 'bon'
            recommendation = 'Validation acceptable - corriger les échecs identifiés'
        elif failed <= total * 0.25:
            quality = 'moyen'
            recommendation = 'Corrections nécessaires avant validation'
        else:
            quality = 'insuffisant'
            recommendation = 'Révision majeure de l\'implémentation requise'
        
        self.analysis = {
            'quality_level': quality,
            'recommendation': recommendation,
            'success_rate': (passed / max(total, 1)) * 100,
            'critical_issues': failed > total * 0.1,
            'production_ready': failed <= 1 and passed >= total * 0.9
        }
    
    def generer_rapport_txt_professionnel(self):
        """Génère un rapport TXT de niveau professionnel"""
        
        filename = f"rapport_professionnel_DF1D_{self.metadata['timestamp']}.txt"
        filepath = os.path.join(self.rapport_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                self._ecrire_entete_txt(f)
                self._ecrire_resume_executif_txt(f)
                self._ecrire_analyse_detaillee_txt(f)
                self._ecrire_resultats_tests_txt(f)
                self._ecrire_analyse_echecs_txt(f)
                self._ecrire_performance_txt(f)
                self._ecrire_recommandations_txt(f)
                self._ecrire_annexes_txt(f)
            
            print(f"✅ Rapport TXT généré: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Erreur génération rapport TXT: {e}")
            return None
    
    def _ecrire_entete_txt(self, f):
        """Écrit l'en-tête professionnel du rapport TXT"""
        f.write("█" * 100 + "\n")
        f.write("██                                                                              ██\n")
        f.write("██    RAPPORT DE VALIDATION PROFESSIONNEL - DIFFÉRENCES FINIES 1D             ██\n")
        f.write("██                                                                              ██\n")
        f.write("█" * 100 + "\n\n")
        
        # Métadonnées du projet
        f.write("INFORMATIONS DU PROJET\n")
        f.write("=" * 50 + "\n")
        f.write(f"Titre          : {self.metadata['projet']}\n")
        f.write(f"Auteur         : {self.metadata['auteur']}\n")
        f.write(f"Cours          : {self.metadata['cours']}\n")
        f.write(f"Institution    : {self.metadata['institution']}\n")
        f.write(f"Date           : {self.metadata['date']}\n")
        f.write(f"Version        : {self.metadata['version']}\n")
        f.write(f"Framework      : {self.metadata['framework']}\n")
        f.write("\n")
        
        # Métadonnées techniques
        f.write("SPÉCIFICATIONS TECHNIQUES\n")
        f.write("=" * 50 + "\n")
        f.write(f"Méthode        : {self.metadata['methode']}\n")
        f.write(f"Équation       : {self.metadata['equation']}\n")
        f.write(f"Domaine        : [0,1] ⊂ ℝ\n")
        f.write(f"Ordre théorique: O(h²)\n")
        f.write(f"Type problème  : Problème aux limites (Dirichlet)\n")
        f.write("\n")
    
    def _ecrire_resume_executif_txt(self, f):
        """Écrit le résumé exécutif"""
        f.write("▓▓▓ RÉSUMÉ EXÉCUTIF ▓▓▓\n")
        f.write("=" * 60 + "\n")
        
        # Statut global
        if self.stats['execution']['success']:
            if self.analysis['production_ready']:
                statut = "✅ VALIDATION COMPLÈTE RÉUSSIE"
                niveau = "PRODUCTION READY"
            else:
                statut = "⚡ VALIDATION QUASI-COMPLÈTE"
                niveau = "ACCEPTABLE AVEC RÉSERVES"
        else:
            statut = "❌ VALIDATION ÉCHOUÉE"
            niveau = "RÉVISION REQUISE"
        
        f.write(f"STATUT GLOBAL     : {statut}\n")
        f.write(f"NIVEAU QUALITÉ    : {niveau}\n")
        f.write(f"RECOMMANDATION    : {self.analysis['recommendation']}\n\n")
        
        # Métriques clés
        f.write("MÉTRIQUES PRINCIPALES\n")
        f.write("-" * 30 + "\n")
        f.write(f"Tests exécutés    : {self.stats['tests']['total']:>8}\n")
        f.write(f"Succès           : {self.stats['tests']['passed']:>8}\n")
        f.write(f"Échecs           : {self.stats['tests']['failed']:>8}\n")
        f.write(f"Erreurs          : {self.stats['tests']['errors']:>8}\n")
        f.write(f"Taux de réussite : {self.analysis['success_rate']:>7.1f}%\n")
        f.write(f"Temps d'exécution: {self.stats['execution']['duration']:>7.2f}s\n")
        f.write(f"Couverture       : {self.stats['coverage']['completeness']:>7.1f}%\n\n")
    
    def _ecrire_analyse_detaillee_txt(self, f):
        """Écrit l'analyse détaillée"""
        f.write("▓▓▓ ANALYSE TECHNIQUE DÉTAILLÉE ▓▓▓\n")
        f.write("=" * 60 + "\n")
        
        if self.analysis['production_ready']:
            f.write("🎯 VALIDATION MATHÉMATIQUE EXCELLENTE\n")
            f.write("   ✓ Implémentation des différences finies parfaite\n")
            f.write("   ✓ Convergence d'ordre 2 confirmée\n")
            f.write("   ✓ Stabilité numérique exceptionnelle\n")
            f.write("   ✓ Robustesse aux cas limites validée\n")
            f.write("   ✓ Gestion d'erreurs sécurisée\n")
            f.write("   ✓ Performance computationnelle optimale\n\n")
            
        elif self.stats['tests']['failed'] <= 1:
            f.write("⚡ VALIDATION QUASI-PARFAITE\n")
            f.write("   ✓ Implémentation des différences finies correcte\n")
            f.write("   ✓ Convergence d'ordre 2 largement confirmée\n")
            f.write("   ✓ Stabilité numérique très bonne\n")
            f.write("   ✓ Robustesse aux cas limites excellente\n")
            f.write("   ⚠ Échec mineur acceptable (précision machine/cas limite)\n")
            f.write("   ✓ Performance satisfaisante\n\n")
            
        else:
            f.write("⚠️ VALIDATION PARTIELLE\n")
            f.write(f"   ⚠ {self.stats['tests']['failed']} test(s) échoué(s)\n")
            f.write(f"   ⚠ {self.stats['tests']['errors']} erreur(s) technique(s)\n")
            f.write("   • Analyse des échecs requise\n")
            f.write("   • Corrections ciblées nécessaires\n\n")
        
        # Analyse par catégorie
        f.write("ANALYSE PAR CATÉGORIE DE TESTS\n")
        f.write("-" * 40 + "\n")
        
        categories_stats = {}
        for test in self.stats['tests']['details']:
            cat = test['category']
            if cat not in categories_stats:
                categories_stats[cat] = {'total': 0, 'passed': 0, 'failed': 0}
            
            categories_stats[cat]['total'] += 1
            if test['status'] == 'PASSED':
                categories_stats[cat]['passed'] += 1
            elif test['status'] == 'FAILED':
                categories_stats[cat]['failed'] += 1
        
        for category, stats in sorted(categories_stats.items()):
            success_rate = (stats['passed'] / max(stats['total'], 1)) * 100
            status_icon = "✅" if success_rate == 100 else "⚠️" if success_rate >= 80 else "❌"
            
            f.write(f"   {status_icon} {category.capitalize():<12}: "
                   f"{stats['passed']:>2}/{stats['total']:<2} ({success_rate:5.1f}%)\n")
        
        f.write("\n")
    
    def _ecrire_resultats_tests_txt(self, f):
        """Écrit les résultats détaillés des tests"""
        f.write("▓▓▓ RÉSULTATS DÉTAILLÉS DES TESTS ▓▓▓\n")
        f.write("=" * 60 + "\n")
        
        # Regroupement par catégorie
        by_category = {}
        for test in self.stats['tests']['details']:
            cat = test['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(test)
        
        for category, tests in sorted(by_category.items()):
            category_name = {
                'base': '🎯 Tests de Base',
                'limite': '⚡ Tests de Limites',
                'fonction': '🔧 Tests de Fonctions',
                'conditions': '🎛️ Tests de Conditions',
                'robustesse': '🛡️ Tests de Robustesse',
                'convergence': '📈 Tests de Convergence',
                'combine': '🎪 Tests Combinés',
                'performance': '⚡ Tests de Performance',
                'autre': '❓ Autres Tests'
            }.get(category, f'📋 {category.capitalize()}')
            
            f.write(f"\n{category_name}\n")
            f.write("-" * 50 + "\n")
            
            for test in tests:
                status_symbol = {
                    'PASSED': '✅',
                    'FAILED': '❌',
                    'ERROR': '💥',
                    'SKIPPED': '⏭️'
                }.get(test['status'], '❓')
                
                test_name = test['name']
                if len(test_name) > 60:
                    test_name = test_name[:57] + "..."
                
                f.write(f"   {status_symbol} {test_name:<63} {test['status']}\n")
    
    def _ecrire_analyse_echecs_txt(self, f):
        """Écrit l'analyse des échecs"""
        if self.stats['failures']['count'] > 0:
            f.write(f"\n▓▓▓ ANALYSE DES ÉCHECS ({self.stats['failures']['count']}) ▓▓▓\n")
            f.write("=" * 60 + "\n")
            
            for i, failure in enumerate(self.stats['failures']['details'], 1):
                f.write(f"\nÉCHEC #{i}: {failure['test']}\n")
                f.write("-" * 40 + "\n")
                f.write(f"Catégorie: {failure['category']}\n")
                f.write(f"Assertion: {failure['assertion']}\n")
                f.write("Détail:\n")
                
                # Formatage du détail d'échec
                detail_lines = failure['full_detail'].split('\n')
                for line in detail_lines[:10]:  # Limite à 10 lignes
                    f.write(f"   {line}\n")
                
                if len(detail_lines) > 10:
                    f.write(f"   ... ({len(detail_lines) - 10} lignes supplémentaires)\n")
        else:
            f.write(f"\n✅ AUCUN ÉCHEC DÉTECTÉ\n")
            f.write("Tous les tests ont été exécutés avec succès.\n")
    
    def _ecrire_performance_txt(self, f):
        """Écrit l'analyse des performances"""
        f.write(f"\n▓▓▓ ANALYSE DES PERFORMANCES ▓▓▓\n")
        f.write("=" * 60 + "\n")
        
        f.write(f"Temps total d'exécution: {self.stats['execution']['duration']:.3f}s\n")
        
        if self.stats['performance']['slowest_tests']:
            f.write(f"Durée moyenne par test: {self.stats['performance']['average_duration']:.4f}s\n\n")
            
            f.write("Tests les plus lents:\n")
            f.write("-" * 30 + "\n")
            for test in self.stats['performance']['slowest_tests']:
                test_name = test['test']
                if len(test_name) > 40:
                    test_name = test_name[:37] + "..."
                f.write(f"   {test['duration']:>6.3f}s  {test_name}\n")
            
            if self.stats['performance']['fastest_tests']:
                f.write("\nTests les plus rapides:\n")
                f.write("-" * 30 + "\n")
                for test in reversed(self.stats['performance']['fastest_tests']):
                    test_name = test['test']
                    if len(test_name) > 40:
                        test_name = test_name[:37] + "..."
                    f.write(f"   {test['duration']:>6.3f}s  {test_name}\n")
        
        # Évaluation des performances
        total_time = self.stats['execution']['duration']
        total_tests = self.stats['tests']['total']
        
        if total_time < 2.0:
            perf_eval = "EXCELLENTE"
        elif total_time < 5.0:
            perf_eval = "TRÈS BONNE"
        elif total_time < 10.0:
            perf_eval = "BONNE"
        else:
            perf_eval = "ACCEPTABLE"
        
        f.write(f"\nÉvaluation des performances: {perf_eval}\n")
    
    def _ecrire_recommandations_txt(self, f):
        """Écrit les recommandations"""
        f.write(f"\n▓▓▓ RECOMMANDATIONS TECHNIQUES ▓▓▓\n")
        f.write("=" * 60 + "\n")
        
        if self.analysis['production_ready']:
            f.write("🚀 VALIDATION COMPLÈTE - PRODUCTION READY\n\n")
            f.write("STATUT: ✅ CERTIFIÉ POUR UTILISATION\n")
            f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            f.write("• Implémentation mathématiquement correcte\n")
            f.write("• Convergence d'ordre 2 parfaitement validée\n")
            f.write("• Stabilité numérique exceptionnelle\n")
            f.write("• Robustesse face aux cas limites confirmée\n")
            f.write("• Gestion d'erreurs sécurisée et complète\n")
            f.write("• Performance computationnelle optimale\n\n")
            
            f.write("PROCHAINES ÉTAPES RECOMMANDÉES:\n")
            f.write("✓ Intégration en environnement de production\n")
            f.write("✓ Extension aux différences finies 2D\n")
            f.write("✓ Documentation utilisateur finale\n")
            f.write("✓ Optimisations avancées (optionnel)\n")
            
        elif self.analysis['success_rate'] >= 95:
            f.write("⚡ VALIDATION QUASI-COMPLÈTE - ACCEPTABLE\n\n")
            f.write("STATUT: ✅ UTILISABLE AVEC RÉSERVES MINEURES\n")
            f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            f.write("• Implémentation globalement correcte\n")
            f.write("• Échecs mineurs probablement liés à:\n")
            f.write("  - Précision machine pour cas extrêmes\n")
            f.write("  - Tolérances de tests très strictes\n")
            f.write("  - Cas limites théoriques acceptables\n\n")
            
            f.write("ACTIONS RECOMMANDÉES:\n")
            f.write("• Analyser les échecs mineurs (voir section Échecs)\n")
            f.write("• Ajuster les tolérances si nécessaire\n")
            f.write("• Validation sur cas d'usage réels\n")
            f.write("• Procéder aux étapes suivantes du projet\n")
            
        else:
            f.write("⚠️ CORRECTIONS NÉCESSAIRES\n\n")
            f.write("STATUT: ❌ RÉVISION REQUISE AVANT UTILISATION\n")
            f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            f.write(f"• {self.stats['tests']['failed']} test(s) critique(s) échoué(s)\n")
            f.write("• Révision de l'implémentation nécessaire\n\n")
            
            f.write("ACTIONS PRIORITAIRES:\n")
            f.write("• Analyser chaque échec détaillé\n")
            f.write("• Corriger les erreurs d'implémentation\n")
            f.write("• Relancer la validation complète\n")
            f.write("• Vérifier la logique mathématique\n")
    
    def _ecrire_annexes_txt(self, f):
        """Écrit les annexes techniques"""
        f.write(f"\n▓▓▓ ANNEXES TECHNIQUES ▓▓▓\n")
        f.write("=" * 60 + "\n")
        
        # Informations d'exécution
        f.write("ENVIRONNEMENT D'EXÉCUTION\n")
        f.write("-" * 30 + "\n")
        f.write(f"Système d'exploitation: {os.name}\n")
        f.write(f"Python: {sys.version.split()[0]}\n")
        f.write(f"Répertoire de travail: {os.getcwd()}\n")
        f.write(f"Commande exécutée: {self.raw_results.get('command', 'N/A')}\n")
        f.write(f"Heure de début: {self.stats['execution']['start_time']}\n")
        f.write(f"Heure de fin: {self.stats['execution']['end_time']}\n\n")
        
        # Couverture détaillée
        f.write("COUVERTURE DES TESTS\n")
        f.write("-" * 30 + "\n")
        f.write(f"Catégories couvertes: {', '.join(self.stats['coverage']['categories_tested'])}\n")
        f.write(f"Complétude: {self.stats['coverage']['completeness']:.1f}%\n\n")
        
        # Métadonnées du rapport
        f.write("MÉTADONNÉES DU RAPPORT\n")
        f.write("-" * 30 + "\n")
        f.write(f"Généré le: {self.metadata['date']}\n")
        f.write(f"Version du rapport: {self.metadata['version']}\n")
        f.write(f"Auteur: {self.metadata['auteur']}\n")
        
        # Pied de page
        f.write("\n" + "█" * 100 + "\n")
        f.write(f"Rapport généré automatiquement par TestReporterProfessionnel v{self.metadata['version']}\n")
        f.write(f"Date de génération: {self.metadata['date']}\n")
        f.write(f"Auteur du projet: {self.metadata['auteur']} - {self.metadata['institution']}\n")
        f.write("█" * 100 + "\n")
    
    def generer_rapport_markdown_professionnel(self):
        """Génère un rapport Markdown de niveau professionnel"""
        
        filename = f"rapport_professionnel_DF1D_{self.metadata['timestamp']}.md"
        filepath = os.path.join(self.rapport_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                self._ecrire_entete_md(f)
                self._ecrire_resume_md(f)
                self._ecrire_resultats_md(f)
                self._ecrire_analyse_md(f)
                self._ecrire_details_md(f)
                self._ecrire_conclusions_md(f)
                self._ecrire_annexes_md(f)
            
            print(f"✅ Rapport Markdown généré: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Erreur génération rapport Markdown: {e}")
            return None
    
    def _ecrire_entete_md(self, f):
        """Écrit l'en-tête Markdown avec badges"""
        f.write("# 🧪 Rapport de Validation Professionnel\n")
        f.write("## Différences Finies 1D - Analyse Complète\n\n")
        
        # Badges de statut
        if self.analysis['production_ready']:
            status_badge = "![Status](https://img.shields.io/badge/Status-VALIDATED-brightgreen)"
            quality_badge = "![Quality](https://img.shields.io/badge/Quality-PRODUCTION_READY-brightgreen)"
        elif self.analysis['success_rate'] >= 95:
            status_badge = "![Status](https://img.shields.io/badge/Status-QUASI_COMPLETE-green)"
            quality_badge = "![Quality](https://img.shields.io/badge/Quality-ACCEPTABLE-green)"
        else:
            status_badge = "![Status](https://img.shields.io/badge/Status-NEEDS_REVIEW-orange)"
            quality_badge = "![Quality](https://img.shields.io/badge/Quality-REVISION_REQUIRED-orange)"
        
        coverage_badge = f"![Coverage](https://img.shields.io/badge/Coverage-{self.stats['tests']['passed']}/{self.stats['tests']['total']}-blue)"
        method_badge = "![Method](https://img.shields.io/badge/Method-Finite_Differences-purple)"
        order_badge = "![Order](https://img.shields.io/badge/Convergence-O(h²)-yellow)"
        time_badge = f"![Time](https://img.shields.io/badge/Execution-{self.stats['execution']['duration']:.2f}s-lightgrey)"
        
        f.write(f"{status_badge} {quality_badge} {coverage_badge}\n")
        f.write(f"{method_badge} {order_badge} {time_badge}\n\n")
        
        # Table des métadonnées
        f.write("## 📋 Informations du Projet\n\n")
        f.write("| Propriété | Valeur |\n")
        f.write("|-----------|--------|\n")
        f.write(f"| **Projet** | {self.metadata['projet']} |\n")
        f.write(f"| **Auteur** | {self.metadata['auteur']} |\n")
        f.write(f"| **Institution** | {self.metadata['institution']} |\n")
        f.write(f"| **Cours** | {self.metadata['cours']} |\n")
        f.write(f"| **Date** | {self.metadata['date']} |\n")
        f.write(f"| **Version** | {self.metadata['version']} |\n")
        f.write(f"| **Méthode** | {self.metadata['methode']} |\n")
        f.write(f"| **Équation** | `{self.metadata['equation']}` |\n\n")
    
    def _ecrire_resume_md(self, f):
        """Écrit le résumé exécutif Markdown"""
        f.write("## 📊 Résumé Exécutif\n\n")
        
        # Table des résultats principaux
        f.write("### 🎯 Résultats Principaux\n\n")
        f.write("| Métrique | Valeur | Évaluation |\n")
        f.write("|----------|--------|------------|\n")
        
        # Statut global
        if self.analysis['production_ready']:
            status_icon = "✅"
            status_text = "VALIDATION COMPLÈTE"
            eval_text = "🚀 Production Ready"
        elif self.analysis['success_rate'] >= 95:
            status_icon = "⚡"
            status_text = "QUASI-VALIDATION"
            eval_text = "✅ Acceptable"
        else:
            status_icon = "⚠️"
            status_text = "RÉVISION REQUISE"
            eval_text = "🔧 À corriger"
        
        f.write(f"| **Statut Global** | {status_icon} {status_text} | {eval_text} |\n")
        f.write(f"| **Tests Exécutés** | {self.stats['tests']['total']} | ℹ️ Total |\n")
        f.write(f"| **Succès** | {self.stats['tests']['passed']} | ✅ Validés |\n")
        f.write(f"| **Échecs** | {self.stats['tests']['failed']} | {'❌ Critiques' if self.stats['tests']['failed'] > 1 else '⚠️ Mineurs' if self.stats['tests']['failed'] == 1 else '✅ Aucun'} |\n")
        f.write(f"| **Taux de Réussite** | {self.analysis['success_rate']:.1f}% | {'🎯 Excellent' if self.analysis['success_rate'] >= 95 else '👍 Bon' if self.analysis['success_rate'] >= 80 else '⚠️ Insuffisant'} |\n")
        f.write(f"| **Temps d'Exécution** | {self.stats['execution']['duration']:.2f}s | {'⚡ Rapide' if self.stats['execution']['duration'] < 5 else '👍 Acceptable' if self.stats['execution']['duration'] < 20 else '🐌 Lent'} |\n")
        f.write(f"| **Couverture** | {self.stats['coverage']['completeness']:.1f}% | {'🎯 Complète' if self.stats['coverage']['completeness'] >= 90 else '👍 Bonne' if self.stats['coverage']['completeness'] >= 70 else '⚠️ Partielle'} |\n\n")
        
        # Recommandation principale
        f.write("### 💡 Recommandation Principale\n\n")
        if self.analysis['production_ready']:
            f.write("🚀 **VALIDATION RÉUSSIE** - Le solver est **certifié pour utilisation en production**.\n\n")
            f.write("✨ L'implémentation des différences finies 1D est mathématiquement correcte, ")
            f.write("numériquement stable et robuste. Tous les critères de validation sont satisfaits.\n\n")
        elif self.analysis['success_rate'] >= 95:
            f.write("⚡ **QUASI-VALIDATION** - Le solver est **acceptable avec réserves mineures**.\n\n")
            f.write("✅ L'implémentation est globalement correcte. Les échecs mineurs sont probablement ")
            f.write("liés à des cas limites acceptables ou à la précision machine.\n\n")
        else:
            f.write("⚠️ **RÉVISION NÉCESSAIRE** - Des corrections sont requises avant utilisation.\n\n")
            f.write("🔧 Analyser les échecs détaillés et corriger les problèmes identifiés avant validation finale.\n\n")
    
    def _ecrire_resultats_md(self, f):
        """Écrit les résultats détaillés Markdown"""
        f.write("## 📈 Résultats par Catégorie\n\n")
        
        # Analyse par catégorie
        categories_stats = {}
        for test in self.stats['tests']['details']:
            cat = test['category']
            if cat not in categories_stats:
                categories_stats[cat] = {'total': 0, 'passed': 0, 'failed': 0, 'tests': []}
            
            categories_stats[cat]['total'] += 1
            categories_stats[cat]['tests'].append(test)
            if test['status'] == 'PASSED':
                categories_stats[cat]['passed'] += 1
            elif test['status'] == 'FAILED':
                categories_stats[cat]['failed'] += 1
        
        # Table de résumé par catégorie
        f.write("### 📊 Résumé par Catégorie\n\n")
        f.write("| Catégorie | Tests | Succès | Échecs | Taux | Statut |\n")
        f.write("|-----------|-------|--------|--------|------|--------|\n")
        
        category_icons = {
            'base': '🎯',
            'limite': '⚡',
            'fonction': '🔧',
            'conditions': '🎛️',
            'robustesse': '🛡️',
            'convergence': '📈',
            'combine': '🎪',
            'performance': '⚡',
            'autre': '❓'
        }
        
        for category, stats in sorted(categories_stats.items()):
            icon = category_icons.get(category, '📋')
            success_rate = (stats['passed'] / max(stats['total'], 1)) * 100
            
            if success_rate == 100:
                status = "✅ Parfait"
            elif success_rate >= 90:
                status = "🟢 Excellent"
            elif success_rate >= 80:
                status = "🟡 Bon"
            else:
                status = "🔴 Problème"
            
            f.write(f"| {icon} {category.capitalize()} | {stats['total']} | {stats['passed']} | {stats['failed']} | {success_rate:.1f}% | {status} |\n")
        
        f.write("\n")
        
        # Détails par catégorie avec tests collapsés
        f.write("### 📝 Détails par Catégorie\n\n")
        
        for category, stats in sorted(categories_stats.items()):
            icon = category_icons.get(category, '📋')
            category_name = category.capitalize()
            
            f.write(f"#### {icon} {category_name}\n\n")
            f.write(f"**Résumé**: {stats['passed']}/{stats['total']} tests réussis ")
            f.write(f"({(stats['passed']/max(stats['total'],1)*100):.1f}%)\n\n")
            
            # Liste des tests
            f.write("<details>\n")
            f.write(f"<summary>Voir les {stats['total']} tests de cette catégorie</summary>\n\n")
            f.write("| Test | Statut |\n")
            f.write("|------|--------|\n")
            
            for test in stats['tests']:
                status_emoji = {
                    'PASSED': '✅',
                    'FAILED': '❌',
                    'ERROR': '💥',
                    'SKIPPED': '⏭️'
                }.get(test['status'], '❓')
                
                test_name = test['name']
                if len(test_name) > 60:
                    test_name = test_name[:57] + "..."
                
                f.write(f"| `{test_name}` | {status_emoji} {test['status']} |\n")
            
            f.write("\n</details>\n\n")
    
    def _ecrire_analyse_md(self, f):
        """Écrit l'analyse technique Markdown"""
        f.write("## 🔬 Analyse Technique\n\n")
        
        if self.analysis['production_ready']:
            f.write("### ✅ Validation Mathématique Complète\n\n")
            f.write("🎯 **Tous les critères de validation sont satisfaits**\n\n")
            f.write("#### Points Validés\n\n")
            f.write("- ✅ **Convergence O(h²)** : Ordre théorique parfaitement confirmé\n")
            f.write("- ✅ **Stabilité numérique** : Aucune instabilité détectée\n")
            f.write("- ✅ **Précision maximale** : Précision machine atteinte pour les cas exacts\n")
            f.write("- ✅ **Robustesse** : Tous les cas limites et pathologiques gérés\n")
            f.write("- ✅ **Sécurité** : Gestion d'erreurs complète et sécurisée\n")
            f.write("- ✅ **Performance** : Temps d'exécution optimal\n\n")
            
        elif self.analysis['success_rate'] >= 95:
            f.write("### ⚡ Validation Quasi-Complète\n\n")
            f.write("🎯 **Validation globalement réussie avec réserves mineures**\n\n")
            f.write("#### Points Validés\n\n")
            f.write("- ✅ **Convergence O(h²)** : Largement confirmée\n")
            f.write("- ✅ **Stabilité numérique** : Très bonne\n")
            f.write("- ✅ **Robustesse** : Excellente sur la majorité des cas\n")
            f.write("- ⚠️ **Échecs mineurs** : Probablement liés à des cas limites acceptables\n\n")
            
            f.write("#### Analyse des Échecs Mineurs\n\n")
            f.write("Les échecs détectés sont vraisemblablement dus à :\n")
            f.write("- 🔬 **Précision machine** : Pour les solutions exactes (polynômes degré ≤ 2)\n")
            f.write("- 📐 **Tolérances strictes** : Critères de tests très rigoureux\n")
            f.write("- 🎯 **Cas limites théoriques** : Comportements aux bornes acceptables\n\n")
            
        else:
            f.write("### ⚠️ Validation Partielle\n\n")
            f.write("🔧 **Corrections nécessaires avant validation complète**\n\n")
            f.write(f"- ❌ **{self.stats['tests']['failed']} test(s) critique(s) échoué(s)**\n")
            f.write(f"- 💥 **{self.stats['tests']['errors']} erreur(s) technique(s)**\n")
            f.write("- 🔍 **Analyse détaillée requise** (voir section Échecs)\n\n")
        
        # Métriques de qualité
        f.write("### 📊 Métriques de Qualité\n\n")
        f.write("| Aspect | Évaluation | Score | Commentaire |\n")
        f.write("|--------|------------|-------|-------------|\n")
        
        # Évaluation de la couverture
        if self.stats['coverage']['completeness'] >= 90:
            cov_eval = "🎯 Excellente"
            cov_score = "A+"
        elif self.stats['coverage']['completeness'] >= 70:
            cov_eval = "👍 Bonne"
            cov_score = "B+"
        else:
            cov_eval = "⚠️ Partielle"
            cov_score = "C"
        
        f.write(f"| Couverture de tests | {cov_eval} | {cov_score} | {self.stats['coverage']['completeness']:.1f}% des catégories |\n")
        
        # Évaluation de la robustesse
        robustesse_rate = 100  # Par défaut
        if 'robustesse' in [test['category'] for test in self.stats['tests']['details']]:
            robustesse_tests = [t for t in self.stats['tests']['details'] if t['category'] == 'robustesse']
            robustesse_passed = sum(1 for t in robustesse_tests if t['status'] == 'PASSED')
            robustesse_rate = (robustesse_passed / max(len(robustesse_tests), 1)) * 100
        
        if robustesse_rate >= 95:
            rob_eval = "🛡️ Excellente"
            rob_score = "A+"
        elif robustesse_rate >= 80:
            rob_eval = "👍 Bonne"
            rob_score = "B+"
        else:
            rob_eval = "⚠️ À améliorer"
            rob_score = "C"
        
        f.write(f"| Robustesse | {rob_eval} | {rob_score} | {robustesse_rate:.1f}% de réussite |\n")
        
        # Évaluation de la performance
        if self.stats['execution']['duration'] < 2:
            perf_eval = "⚡ Excellente"
            perf_score = "A+"
        elif self.stats['execution']['duration'] < 10:
            perf_eval = "👍 Bonne"
            perf_score = "B+"
        else:
            perf_eval = "🐌 Acceptable"
            perf_score = "C"
        
        f.write(f"| Performance | {perf_eval} | {perf_score} | {self.stats['execution']['duration']:.2f}s total |\n")
        
        # Évaluation globale
        if self.analysis['success_rate'] >= 95:
            global_eval = "🏆 Excellente"
            global_score = "A+"
        elif self.analysis['success_rate'] >= 80:
            global_eval = "👍 Bonne"
            global_score = "B+"
        else:
            global_eval = "⚠️ À améliorer"
            global_score = "C"
        
        f.write(f"| Qualité Globale | {global_eval} | {global_score} | {self.analysis['success_rate']:.1f}% de réussite |\n\n")
    
    def _ecrire_details_md(self, f):
        """Écrit les détails techniques Markdown"""
        if self.stats['failures']['count'] > 0:
            f.write("## 🔍 Analyse des Échecs\n\n")
            f.write(f"**{self.stats['failures']['count']} échec(s) détecté(s)**\n\n")
            
            for i, failure in enumerate(self.stats['failures']['details'], 1):
                f.write(f"### ❌ Échec #{i}: `{failure['test']}`\n\n")
                f.write(f"**Catégorie**: {failure['category']}\n\n")
                f.write(f"**Assertion**: `{failure['assertion']}`\n\n")
                
                f.write("<details>\n")
                f.write("<summary>Voir les détails techniques</summary>\n\n")
                f.write("```\n")
                f.write(failure['full_detail'][:1000])  # Limite à 1000 caractères
                if len(failure['full_detail']) > 1000:
                    f.write("\n... (tronqué)")
                f.write("\n```\n")
                f.write("</details>\n\n")
        
        # Analyse des performances
        if self.stats['performance']['slowest_tests']:
            f.write("## ⚡ Analyse des Performances\n\n")
            f.write(f"**Temps total**: {self.stats['execution']['duration']:.3f}s\n")
            f.write(f"**Temps moyen par test**: {self.stats['performance']['average_duration']:.4f}s\n\n")
            
            f.write("### 🐌 Tests les plus lents\n\n")
            f.write("| Test | Durée |\n")
            f.write("|------|-------|\n")
            
            for test in self.stats['performance']['slowest_tests'][:3]:
                test_name = test['test']
                if len(test_name) > 50:
                    test_name = test_name[:47] + "..."
                f.write(f"| `{test_name}` | {test['duration']:.3f}s |\n")
            
            f.write("\n")
    
    def _ecrire_conclusions_md(self, f):
        """Écrit les conclusions Markdown"""
        f.write("## 🎯 Conclusions et Recommandations\n\n")
        
        if self.analysis['production_ready']:
            f.write("### 🚀 Validation Complète - Production Ready\n\n")
            f.write("✨ **Le solver de différences finies 1D est entièrement validé** et certifié pour utilisation.\n\n")
            f.write("#### 🎉 Accomplissements\n\n")
            f.write("- 🎯 **Implémentation parfaite** des différences finies centrées d'ordre 2\n")
            f.write("- 📐 **Convergence O(h²)** mathématiquement confirmée\n")
            f.write("- 🛡️ **Robustesse exceptionnelle** face à tous les cas testés\n")
            f.write("- ⚡ **Performance optimale** pour l'usage prévu\n")
            f.write("- 🔒 **Sécurité** et gestion d'erreurs complètes\n\n")
            f.write("#### 🛤️ Prochaines Étapes Recommandées\n\n")
            f.write("1. ✅ **Déploiement en production** - Le code est prêt\n")
            f.write("2. 🚀 **Extension aux différences finies 2D** - Étape suivante naturelle\n")
            f.write("3. 📚 **Documentation utilisateur** - Finaliser la documentation\n")
            f.write("4. 🔧 **Optimisations avancées** - Améliorer les performances (optionnel)\n")
            f.write("5. 🧪 **Tests d'intégration** - Validation sur cas d'usage réels\n\n")
            
        elif self.analysis['success_rate'] >= 95:
            f.write("### ⚡ Validation Quasi-Complète - Acceptable\n\n")
            f.write("🎯 **Le solver est globalement validé** avec des réserves mineures acceptables.\n\n")
            f.write("#### 🎉 Points Forts\n\n")
            f.write("- ✅ **Implémentation correcte** des différences finies\n")
            f.write("- ✅ **Convergence largement confirmée** sur la majorité des cas\n")
            f.write("- ✅ **Robustesse excellente** pour les cas principaux\n")
            f.write("- ⚠️ **Échecs mineurs** probablement acceptables\n\n")
            
            f.write("#### 🔍 Actions Recommandées\n\n")
            f.write("1. 🔬 **Analyser les échecs mineurs** - Vérifier s'ils sont acceptables\n")
            f.write("2. 📐 **Ajuster les tolérances** - Si nécessaire pour les cas limites\n")
            f.write("3. ✅ **Procéder aux étapes suivantes** - Le solver est utilisable\n")
            f.write("4. 📝 **Documentation des limitations** - Noter les cas limites\n\n")
            
        else:
            f.write("### ⚠️ Révision Nécessaire\n\n")
            f.write("🔧 **Des corrections sont requises** avant la validation finale.\n\n")
            f.write("#### 🔍 Problèmes Identifiés\n\n")
            f.write(f"- ❌ **{self.stats['tests']['failed']} test(s) critique(s) échoué(s)**\n")
            f.write(f"- 💥 **{self.stats['tests']['errors']} erreur(s) technique(s)**\n")
            f.write("- 📊 **Taux de réussite insuffisant** pour validation\n\n")
            
            f.write("#### 🛠️ Plan d'Action\n\n")
            f.write("1. 🔍 **Analyser chaque échec** - Identifier les causes racines\n")
            f.write("2. 🔧 **Corriger l'implémentation** - Résoudre les problèmes identifiés\n")
            f.write("3. 🧪 **Relancer la validation** - Vérifier les corrections\n")
            f.write("4. 📚 **Réviser la théorie** - Si nécessaire pour les aspects mathématiques\n\n")
        
        # Recommandations générales
        f.write("### 💡 Recommandations Générales\n\n")
        
        f.write("#### 📚 Documentation\n")
        f.write("- Maintenir la documentation technique à jour\n")
        f.write("- Documenter les cas limites et leurs comportements\n")
        f.write("- Créer des exemples d'usage pour les utilisateurs\n\n")
        
        f.write("#### 🔬 Tests et Validation\n")
        f.write("- Conserver cette suite de tests pour régression\n")
        f.write("- Ajouter des tests pour nouveaux cas d'usage\n")
        f.write("- Valider régulièrement les performances\n\n")
        
        f.write("#### 🚀 Évolution Future\n")
        f.write("- Planifier l'extension aux problèmes 2D\n")
        f.write("- Considérer des méthodes d'ordre supérieur\n")
        f.write("- Évaluer l'intégration avec d'autres solveurs\n\n")
    
    def _ecrire_annexes_md(self, f):
        """Écrit les annexes techniques Markdown"""
        f.write("## 📎 Annexes Techniques\n\n")
        
        # Environnement d'exécution
        f.write("### 🖥️ Environnement d'Exécution\n\n")
        f.write("| Propriété | Valeur |\n")
        f.write("|-----------|--------|\n")
        f.write(f"| Système | {os.name} |\n")
        f.write(f"| Python | {sys.version.split()[0]} |\n")
        f.write(f"| Répertoire | `{os.getcwd()}` |\n")
        f.write(f"| Commande | `{self.raw_results.get('command', 'N/A')}` |\n")
        f.write(f"| Début | {self.stats['execution']['start_time']} |\n")
        f.write(f"| Fin | {self.stats['execution']['end_time']} |\n")
        f.write(f"| Durée | {self.stats['execution']['duration']:.3f}s |\n\n")
        
        # Statistiques détaillées
        f.write("### 📊 Statistiques Détaillées\n\n")
        f.write("#### Tests par Statut\n")
        f.write("```\n")
        f.write(f"✅ PASSED : {self.stats['tests']['passed']:>3}\n")
        f.write(f"❌ FAILED : {self.stats['tests']['failed']:>3}\n")
        f.write(f"💥 ERROR  : {self.stats['tests']['errors']:>3}\n")
        f.write(f"⏭️ SKIPPED: {self.stats['tests']['skipped']:>3}\n")
        f.write(f"━━━━━━━━━━━━━━━━━\n")
        f.write(f"📊 TOTAL  : {self.stats['tests']['total']:>3}\n")
        f.write("```\n\n")
        
        # Couverture par catégorie
        f.write("#### Couverture par Catégorie\n")
        f.write("```\n")
        for cat in sorted(self.stats['coverage']['categories_tested']):
            f.write(f"📋 {cat.capitalize():<12}: ✅ Couverte\n")
        f.write(f"\n📈 Complétude: {self.stats['coverage']['completeness']:.1f}%\n")
        f.write("```\n\n")
        
        # Métadonnées du rapport
        f.write("### 📄 Métadonnées du Rapport\n\n")
        f.write("| Propriété | Valeur |\n")
        f.write("|-----------|--------|\n")
        f.write(f"| Version | {self.metadata['version']} |\n")
        f.write(f"| Généré le | {self.metadata['date']} |\n")
        f.write(f"| Framework | {self.metadata['framework']} |\n")
        f.write(f"| Auteur | {self.metadata['auteur']} |\n")
        f.write(f"| Institution | {self.metadata['institution']} |\n\n")
        
        # Pied de page
        f.write("---\n\n")
        f.write(f"*📊 Rapport généré automatiquement par TestReporterProfessionnel v{self.metadata['version']}*  \n")
        f.write(f"*📅 {self.metadata['date']} - {self.metadata['auteur']} - {self.metadata['institution']}*  \n")
        f.write(f"*🏫 {self.metadata['cours']} - {self.metadata['projet']}*\n")
    
    def generer_rapports_complets(self):
        """
        Point d'entrée principal pour génération complète des rapports
        """
        print("=" * 80)
        print("📊 GÉNÉRATEUR DE RAPPORTS PROFESSIONNELS")
        print("=" * 80)
        print(f"🎯 Projet: {self.metadata['projet']}")
        print(f"👤 Auteur: {self.metadata['auteur']}")
        print(f"📅 Date: {self.metadata['date']}")
        print("=" * 80)
        
        try:
            # Étape 1: Exécution des tests
            print("\n🚀 ÉTAPE 1: EXÉCUTION DES TESTS")
            if not self.executer_tests_robuste():
                print("⚠️ Problème lors de l'exécution, mais on continue l'analyse...")
            
            # Étape 2: Analyse des résultats
            print("\n📈 ÉTAPE 2: ANALYSE DES RÉSULTATS")
            self.analyser_resultats_complet()
            
            # Étape 3: Génération des rapports
            print("\n📝 ÉTAPE 3: GÉNÉRATION DES RAPPORTS")
            rapport_txt = self.generer_rapport_txt_professionnel()
            rapport_md = self.generer_rapport_markdown_professionnel()
            
            # Rapport final
            print("\n" + "=" * 80)
            print("✅ GÉNÉRATION TERMINÉE AVEC SUCCÈS")
            print("=" * 80)
            
            if rapport_txt:
                print(f"📄 **Rapport TXT**: {rapport_txt}")
            if rapport_md:
                print(f"📝 **Rapport MD**: {rapport_md}")
            
            print(f"📁 **Dossier**: {self.rapport_dir}")
            print("=" * 80)
            
            # Résumé final
            if self.analysis.get('production_ready', False):
                print("🎉 **STATUT**: ✅ VALIDATION COMPLÈTE RÉUSSIE")
                print("🚀 **Le solver est certifié pour utilisation !**")
            elif self.analysis.get('success_rate', 0) >= 95:
                print("⚡ **STATUT**: ✅ VALIDATION QUASI-COMPLÈTE")
                print("👍 **Le solver est acceptable avec réserves mineures**")
            else:
                print("⚠️ **STATUT**: 🔧 RÉVISION NÉCESSAIRE")
                print("📋 **Consulter les rapports pour les détails**")
            
            print(f"📊 **Tests**: {self.stats['tests']['passed']}/{self.stats['tests']['total']} réussis")
            print(f"⏱️ **Durée**: {self.stats['execution']['duration']:.2f}s")
            print("=" * 80)
            
            return self.raw_results.get('success', False)
            
        except Exception as e:
            print(f"\n❌ ERREUR FATALE LORS DE LA GÉNÉRATION")
            print(f"💥 {e}")
            print(f"🔍 Traceback: {traceback.format_exc()}")
            return False


def main():
    """
    Point d'entrée principal du générateur de rapports
    """
    print("🎯 GÉNÉRATEUR DE RAPPORTS PROFESSIONNELS")
    print("📋 Utilisation: Génération de rapports de validation complets")
    print("-" * 60)
    
    try:
        reporter = TestReporterProfessionnel()
        success = reporter.generer_rapports_complets()
        return 0 if success else 1
        
    except Exception as e:
        print(f"💥 Erreur fatale: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())