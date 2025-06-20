"""
Configuration pytest pour les tests des différences finies
"""

import pytest
import numpy as np


def pytest_configure(config):
    """Configuration globale de pytest"""
    config.addinivalue_line(
        "markers", "performance: marque les tests de performance (lents)"
    )


@pytest.fixture(scope="session")
def tolerance_config():
    """Configuration des tolérances globales"""
    return {
        'machine': 1e-14,
        'tres_fine': 1e-10,
        'fine': 1e-6,
        'moyenne': 1e-4,
        'grossiere': 1e-2,
        'tres_grossiere': 1e-1
    }


@pytest.fixture
def solutions_exactes():
    """Banque de solutions exactes pour les tests"""
    return {
        'sin_pi': {
            'solution': lambda x: np.sin(np.pi * x),
            'source': lambda x: np.pi**2 * np.sin(np.pi * x),
            'u0': 0.0, 'u1': 0.0
        },
        'x_cube': {
            'solution': lambda x: x**3,
            'source': lambda x: -6.0 * x,
            'u0': 0.0, 'u1': 1.0
        },
        'x_carre': {
            'solution': lambda x: x**2,
            'source': lambda x: -2.0 * np.ones_like(x),
            'u0': 0.0, 'u1': 1.0
        },
        'lineaire': {
            'solution': lambda x, a=1, b=0: a*x + b,
            'source': lambda x: np.zeros_like(x),
            'u0': 0.0, 'u1': 1.0
        }
    }