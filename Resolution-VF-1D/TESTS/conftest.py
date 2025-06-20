"""
Configuration pytest pour les tests Volumes Finis 1D
"""

import sys
import os

# Ajout du répertoire parent au path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import pytest
import numpy as np

# Configuration globale pour les tests
pytest_plugins = []

# Fixtures globales
@pytest.fixture(scope="session")
def tolerance_config():
    """Configuration des tolérances pour tous les tests"""
    return {
        'machine': 1e-14,
        'tres_fine': 1e-10,
        'fine': 1e-6,
        'moyenne': 1e-4,
        'grossiere': 1e-2,
        'tres_grossiere': 1e-1
    }

@pytest.fixture(scope="session")
def test_cases():
    """Cas de tests standardisés"""
    return {
        'sin_pi_x': {
            'f_source': lambda x: np.pi**2 * np.sin(np.pi * x),
            'u_exacte': lambda x: np.sin(np.pi * x),
            'u0': 0.0,
            'u1': 0.0,
            'C_theo': np.pi**4 / 12
        },
        'x_cube': {
            'f_source': lambda x: -6.0 * x,
            'u_exacte': lambda x: x**3,
            'u0': 0.0,
            'u1': 1.0,
            'C_theo': 1.0 / 12
        },
        'x_square': {
            'f_source': lambda x: -2.0 * np.ones_like(x),
            'u_exacte': lambda x: x**2,
            'u0': 0.0,
            'u1': 1.0,
            'C_theo': 1.0 / 12
        }
    }

@pytest.fixture(scope="session")
def mesh_sizes():
    """Tailles de maillage standardisées"""
    return {
        'coarse': [5, 10, 20],
        'medium': [10, 20, 40, 80],
        'fine': [50, 100, 200],
        'very_fine': [100, 200, 400, 800]
    } 