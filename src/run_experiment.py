"""Run repeatable cached/uncached experiments and aggregate raw measurements."""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
os.environ.setdefault("PYSPARK_PYTHON", "python")
os.environ.setdefault("PYSPARK_DRIVER_PYTHON", "python")


def spark_submit() -> str:
    import pyspark

    spark_bin = Path(pyspark.__file__).resolve().parent / "bin" / "spark-submit.cmd"
    if spark_bin.exists():
        return str(spark_bin)
    raise FileNotFoundError(f"spark-submit.cmd not found below {spark_bin.parent}")


def run_one(input_path: Path, output_path: Path, cache: bool, iterations: int, partitions: int, master: str, ui_port: int) -> dict:
    command = [
        spark_submit(),
        "--master", master,
        str(ROOT / "src" / "run_pagerank.py"),
        "--input", str(input_path),
        "--output", str(output_path),
        "--iterations", str(iterations),
        "--partitions", str(partitions),
        "--ui-port", str(ui_port),
        "--app-name", f"Project8-{'cached' if cache else 'uncached'}",
    ]
    if cache:
        command.append("--cache")
    completed = subprocess.run(command, cwd=ROOT, check=True, text=True, capture_output=True)
    result = json.loads(output_path.read_text(encoding="utf-8"))
    result.update({"cache": cache, "stdout_tail": completed.stdout[-1000:]})
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=2)
    parser.add_argument("--iterations", type=int, default=6)
    parser.add_argument("--partitions", type=int, default=4)
    parser.add_argument("--master", default="local-cluster[2,1,1024]")
    parser.add_argument("--out-dir", default=str(ROOT / "results"))
    args = parser.parse_args()
    out_dir = Path(args.out_dir)
    data_dir = ROOT / "data" / "generated"
    out_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    workloads = [(500, 2000, "small"), (2000, 10000, "medium"), (5000, 30000, "large")]
    all_results: list[dict] = []
    for nodes, edges, label in workloads:
        input_path = data_dir / f"{label}.txt"
        subprocess.run([PYTHON, str(ROOT / "data" / "generate_data.py"), "--nodes", str(nodes), "--edges", str(edges), "--seed", "3010", "--out", str(input_path)], check=True)
        for cache in (False, True):
            for repeat in range(1, args.repeats + 1):
                output_path = out_dir / f"experiment_{label}_{'cached' if cache else 'uncached'}_{repeat}.json"
                print(f"Running {label} cache={cache} repeat={repeat}", flush=True)
                result = run_one(input_path, output_path, cache, args.iterations, args.partitions, args.master, 4040 + repeat)
                result.update({"workload": label, "nodes_requested": nodes, "edges_requested": edges, "repeat": repeat})
                all_results.append(result)

    raw_path = out_dir / "raw_runs.csv"
    fields = ["workload", "nodes_requested", "edges_requested", "repeat", "cache", "iterations", "partitions", "materialization_s", "subsequent_mean_s", "total_runtime_s", "checksum", "storage_level", "default_parallelism"]
    with raw_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for result in all_results:
            writer.writerow({field: result.get(field) for field in fields})
    print(json.dumps({"runs": len(all_results), "raw_csv": str(raw_path)}, indent=2))


if __name__ == "__main__":
    main()
