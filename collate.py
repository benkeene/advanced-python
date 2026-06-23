import json

import pandas as pd

RUNS_PATH = "runs.csv"
OUTPUT_PATH = "collated.csv"

# Columns from runs.csv that describe a run and belong on every sample row.
RUN_META = [
    "run_id",
    "condition_idx",
    "repeat_idx",
    "seed",
    "task",
    "llm",
    "runtime_s",
    "build_git_commit",
    "run_git_commit",
]

# Front-of-table sample columns, when present. Anything else trails after.
SAMPLE_FRONT = ["question", "answer", "response", "prediction", "correct"]


def load_samples(results_path):
    with open(results_path) as f:
        return [json.loads(line) for line in f]


def explode_json_column(df, column, prefix):
    """
    Parse a column of JSON strings into one real column per key.
    Mirrors explode_task_args in build_experiment.py
    """
    parsed = df[column].apply(json.loads)
    exploded = pd.json_normalize(parsed.tolist()).add_prefix(prefix)
    exploded.index = df.index
    return pd.concat([df.drop(columns=[column]), exploded], axis=1)


def order_columns(df):
    front = [c for c in SAMPLE_FRONT if c in df.columns]
    rest = [c for c in df.columns if c not in front]
    return df[front + rest]


def collate(runs_path=RUNS_PATH):
    """Load every run's samples into one tidy per-sample dataframe."""
    runs = pd.read_csv(runs_path)

    frames = []
    for _, run in runs.iterrows():
        samples = pd.DataFrame(load_samples(run["results_path"]))
        for col in RUN_META:
            samples[col] = run[col]
        samples["task_args"] = run["task_args"]
        samples["llm_args"] = run["llm_args"]
        frames.append(samples)

    df = pd.concat(frames, ignore_index=True)
    df = explode_json_column(df, "task_args", "arg_")
    df = explode_json_column(df, "llm_args", "llm_")
    df["correct"] = df["prediction"] == df["answer"]
    return order_columns(df)


def main():
    df = collate()
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Wrote {len(df)} samples to {OUTPUT_PATH}")
    print(f"Tasks: {sorted(df['task'].unique())}")
    print(f"Columns: {list(df.columns)}")
    print()
    print("Accuracy by condition:")
    print(df.groupby(["task", "arg_condition"])["correct"].mean().round(3))


if __name__ == "__main__":
    main()
