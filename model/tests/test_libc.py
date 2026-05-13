import pytest

from carsf.libc import human_labour_equivalent, output_per_fte_benchmark


def test_opfte_benchmark() -> None:
    assert output_per_fte_benchmark(9000, 10) == 900


def test_hle_uses_sector_output_unit() -> None:
    assert human_labour_equivalent(4500, 900) == 5


def test_opfte_rejects_zero_qlc() -> None:
    with pytest.raises(ValueError):
        output_per_fte_benchmark(9000, 0)
