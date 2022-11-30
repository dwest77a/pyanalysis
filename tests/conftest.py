import pytest
import numpy as np

@pytest.fixture
def dataset1d():
    return np.array([10, 12, 12, 10, 12, 10, 10, 12])

@pytest.fixture
def tsigma():
    return 1

@pytest.fixture
def tvariance():
    return 1