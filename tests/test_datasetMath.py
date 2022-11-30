import pytest

def test_sigma(dataset1d, tsigma):
    from pyanalysis.pyanalysis.datasetMath import sigma
    assert sigma(dataset1d) == tsigma


def test_variance(dataset1d, tvariance):
    from pyanalysis.pyanalysis.datasetMath import variance
    assert variance(dataset1d) == tvariance

def test_std_error():
    assert True

def test_linear_regression():
    assert True

def test_science_errors():
    assert True