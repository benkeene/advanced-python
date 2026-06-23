import json
import random
import re
from pathlib import Path

DATASET_PATH = "data/arithmetic.jsonl"

CONDITIONS = {
    "standard": " Answer with only a number.",
    "zs_cot": " Let's think step by step.",
}


def _load_dataset():
    with open(DATASET_PATH) as f:
        return [json.loads(line) for line in f]


def _parse_answer(response):
    numbers = re.findall(r"-?\d+", response)
    return int(numbers[-1]) if numbers else None


def _score(results, labels):
    correct = sum(
        r["prediction"] == l
        for r, l in zip(results, labels)
        if r["prediction"] is not None
    )
    parseable = sum(1 for r in results if r["prediction"] is not None)
    unparseable = len(results) - parseable
    accuracy = correct / parseable if parseable else 0.0
    return correct, parseable, unparseable, accuracy


def run(model, args, seed, results_path):
    """Execute one run of the arithmetic task.

    args:
        condition: "standard" | "zs_cot"
        n_samples: int
    """
    condition = args["condition"]
    n_samples = args["n_samples"]
    suffix = CONDITIONS[condition]

    dataset = _load_dataset()
    rng = random.Random(seed)
    sample = rng.sample(dataset, min(n_samples, len(dataset)))
    labels = [item["answer"] for item in sample]

    questions = [item["question"] + suffix for item in sample]
    responses = model.chat(questions)

    results = []
    for item, response in zip(sample, responses):
        prediction = _parse_answer(response)
        results.append({**item, "response": response, "prediction": prediction})

    Path(results_path).parent.mkdir(parents=True, exist_ok=True)
    with open(results_path, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    correct, parseable, unparseable, accuracy = _score(results, labels)
    return {
        "n_correct": correct,
        "n_parseable": parseable,
        "n_unparseable": unparseable,
        "n_total": len(results),
        "accuracy": accuracy,
    }
