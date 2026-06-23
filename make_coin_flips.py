import json
import random
from names_dataset import NameDataset

nd = NameDataset()
names = (
    nd.get_top_names(n=1000, country_alpha2="US")["US"]["M"]
    + nd.get_top_names(n=1000, country_alpha2="US")["US"]["F"]
)


def generate_coin_flip(n_flips=4, seed=None):
    if seed is not None:
        random.seed(seed)

    selected = random.sample(names, n_flips)
    actions = [random.choice([True, False]) for _ in range(n_flips)]  # True = flips

    parts = []
    for name, flips in zip(selected, actions):
        verb = "flips" if flips else "does not flip"
        parts.append(f"{name} {verb} the coin.")

    question = "A coin is heads up. " + " ".join(parts) + " Is the coin still heads up?"

    # Ground truth: count actual flips
    n_actual_flips = sum(actions)
    answer = "yes" if n_actual_flips % 2 == 0 else "no"

    return {"question": question, "answer": answer, "n_flips": n_actual_flips}


if __name__ == "__main__":
    dataset = [generate_coin_flip(n_flips=4, seed=i) for i in range(100)]
    with open("data/coin_flips.jsonl", "w") as f:
        for item in dataset:
            f.write(json.dumps(item) + "\n")
