import numpy as np

def monte_carlo_pi(n_samples: int, seed: int) -> int:
    rng = np.random.default_rng(seed)
    x = rng.random(n_samples)
    y = rng.random(n_samples)
    inside = np.sum(x*x + y*y <= 1.0)
    return int(inside)
