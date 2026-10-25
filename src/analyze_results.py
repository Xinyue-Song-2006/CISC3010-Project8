"""Summarize raw runs and create publication-ready experiment figures."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(args.results)
    df["cache_label"] = df["cache"].map({True: "Cached", False: "Uncached", "True": "Cached", "False": "Uncached"})
    summary = (df.groupby(["workload", "cache_label"], as_index=False)
        .agg(materialization_mean_s=("materialization_s", "mean"), materialization_std_s=("materialization_s", "std"), subsequent_mean_s=("subsequent_mean_s", "mean"), subsequent_std_s=("subsequent_mean_s", "std"), total_runtime_mean_s=("total_runtime_s", "mean"), total_runtime_std_s=("total_runtime_s", "std")))
    baseline = summary.pivot(index="workload", columns="cache_label", values="subsequent_mean_s")
    cached_speedup = (baseline["Uncached"] / baseline["Cached"]).to_dict()
    summary["cached_speedup_vs_uncached"] = summary["workload"].map(cached_speedup)
    summary.to_csv(out_dir / "summary.csv", index=False)

    plt.rcParams.update({"font.size": 11, "axes.titlesize": 13, "axes.labelsize": 11})
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    pivot = summary.pivot(index="workload", columns="cache_label", values="subsequent_mean_s")
    pivot[[column for column in ("Uncached", "Cached") if column in pivot]].plot(kind="bar", ax=ax, color=["#6B7280", "#2563EB"])
    ax.set_title("Subsequent iteration time")
    ax.set_xlabel("Workload")
    ax.set_ylabel("Seconds, mean")
    ax.legend(title="Configuration")
    fig.tight_layout()
    fig.savefig(out_dir / "cache_speedup.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    for cache_label, group in df.groupby("cache_label"):
        means = group.groupby("workload")["materialization_s"].mean()
        ax.plot(means.index, means.values, marker="o", label=f"Initial materialization: {cache_label}")
        means2 = group.groupby("workload")["subsequent_mean_s"].mean()
        ax.plot(means2.index, means2.values, marker="s", linestyle="--", label=f"Subsequent iterations: {cache_label}")
    ax.set_title("Initial materialization versus reuse")
    ax.set_xlabel("Workload")
    ax.set_ylabel("Seconds, mean")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out_dir / "iteration_timing.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    partitions = df.groupby("workload")["partitions"].first()
    ax.bar(partitions.index, partitions.values, color="#0F766E")
    ax.set_title("Fixed partition budget across workloads")
    ax.set_xlabel("Workload")
    ax.set_ylabel("Partitions")
    fig.tight_layout()
    fig.savefig(out_dir / "partition_observability.png", dpi=180)
    plt.close(fig)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
