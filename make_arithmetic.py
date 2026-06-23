import json
import random
from names_dataset import NameDataset

nd = NameDataset()
names = (
    nd.get_top_names(n=1000, country_alpha2="US")["US"]["M"]
    + nd.get_top_names(n=1000, country_alpha2="US")["US"]["F"]
)

ITEMS = [
    "apples",
    "oranges",
    "books",
    "stickers",
    "coins",
    "marbles",
    "stamps",
    "pencils",
]

ADD_VERBS = ["receives", "buys", "finds", "picks up", "is given"]
SUB_VERBS = ["gives away", "loses", "spends", "drops", "donates"]


def generate_arithmetic(n_steps=3, seed=None):
    if seed is not None:
        random.seed(seed)

    name = random.choice(names)
    item = random.choice(ITEMS)
    total = random.randint(5, 20)

    parts = [f"{name} has {total} {item}."]
    step_log = []

    for _ in range(n_steps):
        if total > 1 and random.random() < 0.5:
            amount = random.randint(1, total - 1)
            verb = random.choice(SUB_VERBS)
            parts.append(f"{name} {verb} {amount} {item}.")
            total -= amount
            step_log.append(-amount)
        else:
            amount = random.randint(1, 10)
            verb = random.choice(ADD_VERBS)
            noun = item.rstrip("s") if amount == 1 else item
            parts.append(f"{name} {verb} {amount} more {noun}.")
            total += amount
            step_log.append(amount)

    question = " ".join(parts) + f" How many {item} does {name} have now?"

    return {
        "question": question,
        "answer": total,
        "n_steps": n_steps,
        "steps": step_log,
    }


if __name__ == "__main__":
    dataset = [
        generate_arithmetic(n_steps=n, seed=i * 7 + n)
        for n in range(2, 5)
        for i in range(34)
    ]  # ~100 samples, balanced across 2/3/4 steps

    with open("data/arithmetic.jsonl", "w") as f:
        for item in dataset:
            f.write(json.dumps(item) + "\n")

    print(f"Wrote {len(dataset)} samples to data/arithmetic.jsonl")
