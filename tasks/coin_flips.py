import json
import random
from pathlib import Path

DATASET_PATH = "data/coin_flips.jsonl"

CONDITIONS = {
    "standard": "Is the coin still heads up? Answer with only 'yes' or 'no'.",
    "zs_cot": ' Think through this step by step. Is the coin still heads up? Answer with only "yes" or "no".',
}


def _load_dataset():
    with open(DATASET_PATH) as f:
        return [json.loads(line) for line in f]


def _parse_answer(response):
    text = response.strip().lower()
    if text.startswith("yes"):
        return "yes"
    if text.startswith("no"):
        return "no"
    return None


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
    """Execute one run of the coin flips task.

    args:
        condition: "standard"
        n_samples: int
    """
    condition = args.get("condition", "standard")
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
