from carsf import QLCWeights, Worker, qualified_labour_contribution_worker
import pytest


def test_qlc_cap_prevents_unbounded_worker_inflation() -> None:
    worker = Worker(
        annual_hours=1820,
        wage_quality=1,
        job_security=1,
        skill_development=1,
        australian_nexus=1,
    )
    weights = QLCWeights(alpha=5, beta=5, gamma=5, delta=5, qlc_max_multiplier=1.25)

    assert qualified_labour_contribution_worker(worker, weights) == 1.25


def test_fake_qlc_inflation_scores_are_clamped_and_capped() -> None:
    worker = Worker(
        annual_hours=1820,
        wage_quality=99,
        job_security=99,
        skill_development=99,
        australian_nexus=99,
    )

    assert qualified_labour_contribution_worker(worker) == 1.25


def test_qlc_zero_hours_stays_zero() -> None:
    worker = Worker(
        annual_hours=0,
        wage_quality=1,
        job_security=1,
        skill_development=1,
        australian_nexus=1,
    )

    assert qualified_labour_contribution_worker(worker) == 0


def test_qlc_rejects_negative_weights() -> None:
    worker = Worker(
        annual_hours=1820,
        wage_quality=1,
        job_security=1,
        skill_development=1,
        australian_nexus=1,
    )

    with pytest.raises(ValueError):
        qualified_labour_contribution_worker(worker, QLCWeights(alpha=-0.1))
