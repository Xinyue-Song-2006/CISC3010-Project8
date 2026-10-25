"""Compare Spark PageRank output with a sequential reference implementation."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def read_graph(path: str) -> tuple[list[int], dict[int, list[int]]]:
    links: dict[int, list[int]] = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        source, target = map(int, line.split())
        links.setdefault(source, []).append(target)
    nodes = sorted(links)
    return nodes, links


def reference(nodes: list[int], links: dict[int, list[int]], iterations: int) -> dict[int, float]:
    ranks = {node: 1.0 / len(nodes) for node in nodes}
    for _ in range(iterations):
        next_ranks = {node: 0.15 / len(nodes) for node in nodes}
        for source, targets in links.items():
            share = 0.85 * ranks[source] / len(targets)
            for target in targets:
                next_ranks[target] = next_ranks.get(target, 0.15 / len(nodes)) + share
        ranks = next_ranks
    return ranks


def read_spark_ranks(spark_json: str) -> dict[int, float]:
    ranks_path = Path(spark_json).with_name(Path(spark_json).stem + "_ranks.csv")
    with ranks_path.open(newline="", encoding="utf-8") as handle:
        return {int(row["node"]): float(row["rank"]) for row in csv.DictReader(handle)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--spark-results", required=True)
    parser.add_argument("--iterations", type=int, required=True)
    parser.add_argument("--tolerance", type=float, default=1e-8)
    parser.add_argument("--output")
    args = parser.parse_args()
    nodes, links = read_graph(args.input)
    expected = reference(nodes, links, args.iterations)
    actual = read_spark_ranks(args.spark_results)
    missing = sorted(set(expected) - set(actual))
    if missing:
        raise SystemExit(f"FAIL: missing nodes in Spark output: {missing[:5]}")
    max_error = max(abs(expected[node] - actual[node]) for node in expected)
    passed = max_error <= args.tolerance
    result = {"passed": passed, "nodes": len(nodes), "iterations": args.iterations, "max_abs_error": max_error, "tolerance": args.tolerance}
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
