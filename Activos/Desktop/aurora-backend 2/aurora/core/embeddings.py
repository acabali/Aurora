from typing import List
import numpy as np
def embed_texts(texts: List[str]) -> List[List[float]]:
    return [list(np.random.default_rng(abs(hash(t)) % 2**32).random(384)) for t in texts]
