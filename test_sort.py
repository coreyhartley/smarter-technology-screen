import pytest
from sort import sort, Package

def test_standard_package():
    """Small and light packages should be STANDARD."""
    assert sort(10, 10, 10, 10) == Package.STANDARD.upper()
    # Testing near but below thresholds
    assert sort(149, 149, 40, 19) == Package.STANDARD.upper()

def test_special_bulky_by_dimension():
    """One dimension > 150 should be SPECIAL."""
    assert sort(151, 10, 10, 10) == Package.SPECIAL.upper()
    assert sort(10, 151, 10, 10) == Package.SPECIAL.upper()
    assert sort(10, 10, 151, 10) == Package.SPECIAL.upper()

def test_special_bulky_by_volume():
    """Volume >= 1,000,000 should be SPECIAL."""
    assert sort(100, 100, 100, 10) == Package.SPECIAL.upper()

def test_special_heavy():
    """Mass >= 20 should be SPECIAL."""
    assert sort(10, 10, 10, 20) == Package.SPECIAL.upper()
    assert sort(10, 10, 10, 50) == Package.SPECIAL.upper()

def test_rejected_bulky_and_heavy():
    """Both bulky and heavy should be REJECTED."""
    # Bulky by dimension and heavy
    assert sort(151, 10, 10, 20) == Package.REJECTED.upper()
    # Bulky by volume and heavy
    assert sort(100, 100, 100, 20) == Package.REJECTED.upper()

def test_invalid_inputs():
    """Ensure ValueError is raised for non-positive values."""
    with pytest.raises(ValueError, match="All dimensions must be positive"):
        sort(0, 10, 10, 10)
    with pytest.raises(ValueError, match="All dimensions must be positive"):
        sort(-5, 10, 10, 10)
    with pytest.raises(ValueError, match="Mass must be positive"):
        sort(10, 10, 10, 0)
    with pytest.raises(ValueError, match="Mass must be positive"):
        sort(10, 10, 10, -1)

@pytest.mark.parametrize("w, h, l, m, expected", [
    (150, 150, 44, 19, Package.STANDARD.upper()),     # Exactly at dimension threshold
    (100, 100, 99.9, 10, Package.STANDARD.upper()),   # Just below volume threshold
    (20, 20, 20, 19.9, Package.STANDARD.upper()),     # Just below mass threshold
])
def test_boundary_conditions(w, h, l, m, expected):
    """Verify behavior exactly at or near threshold boundaries."""
    assert sort(w, h, l, m) == expected
