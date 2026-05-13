from carsf import QLCWeights, Worker, qualified_labour_contribution_worker


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
