"""Test function to collect matching peaks. Run tests both on numba compiled and
pure Python version."""
import numpy
import pytest
from matchms.similarity.spectrum_similarity_functions import collect_peak_pairs


@pytest.mark.parametrize("shift, expected_pairs",
                         [(0.0, [(2, 2, 1.0), (3, 3, 1.0)]),
                          (-5.0, [(0, 0, 0.01), (1, 1, 0.01)])])
def test_collect_peak_pairs_compiled(shift, expected_pairs):
    """Test finding expected peak matches for given tolerance."""
    spec1 = numpy.array([[100, 200, 300, 500],
                         [0.1, 0.1, 1.0, 1.0]], dtype="float").T

    spec2 = numpy.array([[105, 205.1, 300, 500.1],
                         [0.1, 0.1, 1.0, 1.0]], dtype="float").T

    matching_pairs = collect_peak_pairs(spec1, spec2, tolerance=0.2, shift=shift)
    assert len(matching_pairs) == 2, "Expected different number of matching peaks"
    assert matching_pairs == [pytest.approx(x, 1e-9) for x in expected_pairs], "Expected different pairs."


@pytest.mark.parametrize("shift, expected_pairs",
                         [(0.0, [(2, 2, 1.0), (3, 3, 1.0)]),
                          (-5.0, [(0, 0, 0.01), (1, 1, 0.01)])])
def test_collect_peak_pairs(shift, expected_pairs):
    """Test finding expected peak matches for tolerance=0.2 and given shift."""
    spec1 = numpy.array([[100, 200, 300, 500],
                         [0.1, 0.1, 1.0, 1.0]], dtype="float").T

    spec2 = numpy.array([[105, 205.1, 300, 500.1],
                         [0.1, 0.1, 1.0, 1.0]], dtype="float").T

    matching_pairs = collect_peak_pairs.py_func(spec1, spec2, tolerance=0.2, shift=shift)
    assert len(matching_pairs) == 2, "Expected different number of matching peaks"
    assert matching_pairs == [pytest.approx(x, 1e-9) for x in expected_pairs], "Expected different pairs."
