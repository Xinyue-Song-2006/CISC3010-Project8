"""Generate a deterministic directed graph for the Spark experiments."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path


def generate_graph(nodes: int, edges: int, seed: int) -> list[tuple[int, int]]:
    if nodes < 2:
        raise ValueError("nodes must be at least 2")
    if edges < nodes:
        raise ValueError("edges must be at least nodes so every source can have an edge")

    rng = random.Random(seed)
    pairs: set[tuple[int, int]] = set()
    for source in range(nodes):
        target = (source + 1) % nodes
        pairs.add((source, target))
    while len(pairs) < edges:
        source = rng.randrange(nodes)
        target = rng.randrange(nodes)
        if source != target:
            pairs.add((source, target))
    return sorted(pairs)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nodes", type=int, default=1000)
    parser.add_argument("--edges", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=3010)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    graph = generate_graph(args.nodes, args.edges, args.seed)
    output.write_text("\n".join(f"{source} {target}" for source, target in graph) + "\n", encoding="utf-8")
    print(json.dumps({"nodes": args.nodes, "edges": len(graph), "seed": args.seed, "output": str(output)}, indent=2))


if __name__ == "__main__":
    main()
