from carsf import net_labour_tax_gap


def test_nltg_cannot_be_negative() -> None:
    assert net_labour_tax_gap(hle=5, aii=0.2, qlc=10) == 0
