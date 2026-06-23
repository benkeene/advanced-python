import itertools
import json
import subprocess
from pathlib import Path

import pandas as pd

TASK_REGISTRY = {
    "arithmetic": None,
    # "coin_flips": None,
}

LLM_REGISTRY = {
    "qwen2.5-7b": None,
}


TASK_SWEEPS = {
    "arithmetic": {
        "condition": ["standard", "zs_cot"],
        "n_samples": [10],
    },
    # "coin_flips": {
    # "condition": ["standard", "zs_cot"],
    # "n_samples": [10],
    # },
}

LLM_SWEEP = {
    "llm": ["qwen2.5-7b"],
    "temperature": [0.0],
    "top_k": [3],
}

REPEATS = 3
SEED_START = 1000
SEED_STRIDE = 100

OUTPUT_PATH = Path("experiment.csv")


def _git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def get_git_state():
    commit = _git("rev-parse", "HEAD")
    dirty = bool(_git("status", "--porcelain"))
    return commit, dirty


def validate_keys():
    for task in TASK_SWEEPS:
        if task not in TASK_REGISTRY:
            raise KeyError(f"task {task!r} not in TASK_REGISTRY {list(TASK_REGISTRY)}")
    for llm in LLM_SWEEP["llm"]:
        if llm not in LLM_REGISTRY:
            raise KeyError(f"llm {llm!r} not in LLM_REGISTRY {list(LLM_REGISTRY)}")


def build():
    validate_keys()
    git_commit, git_dirty = get_git_state()

    llm_keys = list(LLM_SWEEP.keys())
    llm_combos = list(itertools.product(*(LLM_SWEEP[k] for k in llm_keys)))

    rows = []
    idx = 0

    for task, task_sweep in TASK_SWEEPS.items():
        task_keys = list(task_sweep.keys())
        task_combos = list(itertools.product(*(task_sweep[k] for k in task_keys)))

        for task_combo in task_combos:
            task_cfg = dict(zip(task_keys, task_combo))
            for llm_combo in llm_combos:
                llm_cfg = dict(zip(llm_keys, llm_combo))

                rows.append(
                    {
                        "idx": idx,
                        "task": task,
                        "llm": llm_cfg["llm"],
                        "task_args": json.dumps(task_cfg, sort_keys=True),
                        "llm_args": json.dumps(
                            {k: v for k, v in llm_cfg.items() if k != "llm"},
                            sort_keys=True,
                        ),
                        "repeats": REPEATS,
                        "base_seed": SEED_START + idx * SEED_STRIDE,
                        "git_commit": git_commit,
                        "git_dirty": git_dirty,
                    }
                )
                idx += 1

    df = pd.DataFrame(rows)
    df = df[
        [
            "idx",
            "task",
            "llm",
            "task_args",
            "llm_args",
            "repeats",
            "base_seed",
            "git_commit",
            "git_dirty",
        ]
    ]
    return df


def explode_task_args(df):
    """Return a copy of df with task_args parsed into one column per key."""
    parsed = df["task_args"].apply(json.loads)
    args_df = pd.json_normalize(parsed.tolist()).add_prefix("arg_")
    args_df.index = df.index
    return pd.concat([df.drop(columns=["task_args"]), args_df], axis=1)


def main():
    df = build()
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Wrote {len(df)} conditions to {OUTPUT_PATH.resolve()}")
    print(
        f"Total executions planned: {int(df['repeats'].sum())} "
        f"({len(df)} conditions × {REPEATS} repeats)"
    )
    commit = df["git_commit"].iloc[0]
    dirty = df["git_dirty"].iloc[0]
    print(
        f"Build git: {commit[:12]} "
        f"({'DIRTY — uncommitted changes!' if dirty else 'clean'})"
    )
    print()
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
