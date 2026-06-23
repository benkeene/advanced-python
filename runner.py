import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd

from llm import Qwen
import tasks.arithmetic as arithmetic_task
import tasks.coin_flips as coin_flips_task

TASK_REGISTRY = {
    "arithmetic": arithmetic_task.run,
    "coin_flips": coin_flips_task.run,
}

LLM_REGISTRY = {
    "qwen2.5-7b": Qwen,
}

PLAN_PATH = Path("experiment.csv")
RUNS_PATH = Path("runs.csv")
RESULTS_DIR = Path("results")


def _git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def get_git_state():
    commit = _git("rev-parse", "HEAD")
    dirty = bool(_git("status", "--porcelain"))
    return commit, dirty


def build_skeleton(plan):
    rows = []
    for _, cond in plan.iterrows():
        for repeat_idx in range(int(cond["repeats"])):
            run_id = f"run{int(cond['idx']):02d}_rep{repeat_idx:01d}"
            rows.append(
                {
                    "run_id": run_id,
                    "condition_idx": int(cond["idx"]),
                    "repeat_idx": repeat_idx,
                    "seed": int(cond["base_seed"]) + repeat_idx,
                    "task": cond["task"],
                    "llm": cond["llm"],
                    "task_args": cond["task_args"],
                    "llm_args": cond["llm_args"],
                    "build_git_commit": cond["git_commit"],
                    "build_git_dirty": cond["git_dirty"],
                    "run_git_commit": None,
                    "started_at": None,
                    "finished_at": None,
                    "runtime_s": None,
                    "n_correct": None,
                    "n_parseable": None,
                    "n_unparseable": None,
                    "n_total": None,
                    "accuracy": None,
                    "results_path": None,
                }
            )
    return pd.DataFrame(rows)


def run_all(plan_path):
    plan = pd.read_csv(plan_path)
    runs = build_skeleton(plan)

    run_git_commit, _ = get_git_state()
    RESULTS_DIR.mkdir(exist_ok=True)

    n_total = len(runs)
    print(f"Running {n_total} runs ({len(plan)} conditions x repeats)\n")

    for i, run in runs.iterrows():
        task_fn = TASK_REGISTRY[run["task"]]
        task_args = json.loads(run["task_args"])
        llm_args = json.loads(run["llm_args"])

        model = LLM_REGISTRY[run["llm"]](
            max_tokens=256,
            temperature=llm_args.get("temperature", 0.0),
            top_k=llm_args.get("top_k", -1),
        )

        results_path = str(RESULTS_DIR / f"{run['run_id']}.jsonl")

        print(
            f"[{i + 1}/{n_total}] {run['task']}  " f"{run['run_id']}  {task_args}",
        )

        started_at = datetime.now()
        t0 = time.perf_counter()
        metrics = task_fn(
            model=model,
            args=task_args,
            seed=int(run["seed"]),
            results_path=results_path,
        )
        runtime = time.perf_counter() - t0

        runs.at[i, "run_git_commit"] = run_git_commit
        runs.at[i, "started_at"] = started_at.isoformat()
        runs.at[i, "finished_at"] = datetime.now().isoformat()
        runs.at[i, "runtime_s"] = round(runtime, 2)
        runs.at[i, "results_path"] = results_path
        for k, v in metrics.items():
            runs.at[i, k] = v

        print(
            f"    accuracy={metrics['accuracy']:.1%}  "
            f"({metrics['n_correct']}/{metrics['n_parseable']})  "
            f"{runtime:.1f}s",
        )

    runs.to_csv(RUNS_PATH, index=False)
    print(f"\nWrote {len(runs)} runs to {RUNS_PATH.resolve()}")
    return runs


if __name__ == "__main__":
    plan = sys.argv[1] if len(sys.argv) > 1 else PLAN_PATH
    run_all(plan)
