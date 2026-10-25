"""Run an iterative PageRank workload with optional RDD caching."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

from pyspark import SparkConf, SparkContext, StorageLevel


def parse_edges(line: str) -> tuple[int, int]:
    source, target = line.split()
    return int(source), int(target)


def build_links(sc: SparkContext, input_path: str, partitions: int):
    edges = sc.textFile(input_path, minPartitions=partitions).map(parse_edges)
    return edges.groupByKey(numPartitions=partitions).mapValues(lambda values: tuple(values))


def run(args: argparse.Namespace) -> dict:
    python_exec = os.environ.get("PYSPARK_PYTHON", "python")
    conf = (
        SparkConf()
        .setAppName(args.app_name)
        .setMaster(args.master)
        .set("spark.executor.instances", "2")
        .set("spark.executor.cores", "1")
        .set("spark.cores.max", "2")
        .set("spark.pyspark.python", python_exec)
        .set("spark.pyspark.driver.python", python_exec)
        .set("spark.executorEnv.PYSPARK_PYTHON", python_exec)
        .set("spark.executorEnv.PYSPARK_DRIVER_PYTHON", python_exec)
        .set("spark.python.worker.faulthandler.enabled", "true")
        .set("spark.python.worker.reuse", "true")
        .set("spark.default.parallelism", str(args.partitions))
        .set("spark.ui.enabled", "true")
        .set("spark.ui.port", str(args.ui_port))
        .set("spark.eventLog.enabled", "false")
    )
    sc = SparkContext(conf=conf)
    sc.setLogLevel("WARN")
    start = time.perf_counter()
    links = build_links(sc, args.input, args.partitions)
    if args.cache:
        links = links.persist(StorageLevel.MEMORY_ONLY)
    materialization_start = time.perf_counter()
    source_count = links.count()
    materialization_s = time.perf_counter() - materialization_start

    nodes = links.keys().distinct(args.partitions)
    node_count = nodes.count()
    initial_rank = 1.0 / node_count
    ranks = nodes.map(lambda node: (node, initial_rank)).partitionBy(args.partitions)
    iteration_times: list[float] = []
    rank_counts: list[int] = []
    for iteration in range(1, args.iterations + 1):
        iteration_start = time.perf_counter()
        contributions = (
            links.join(ranks, numPartitions=args.partitions)
            .flatMap(lambda item: ((target, item[1][1] / len(item[1][0])) for target in item[1][0]))
            .reduceByKey(lambda left, right: left + right, numPartitions=args.partitions)
        )
        ranks = contributions.mapValues(lambda value: 0.15 / node_count + 0.85 * value)
        rank_count = ranks.count()
        elapsed = time.perf_counter() - iteration_start
        iteration_times.append(elapsed)
        rank_counts.append(rank_count)
        print(f"ITERATION {iteration}: seconds={elapsed:.6f} ranks={rank_count} cache={args.cache}", flush=True)

    final_ranks = ranks.collect()
    final_ranks.sort(key=lambda item: item[1], reverse=True)
    total_runtime_s = time.perf_counter() - start
    storage_level = str(links.getStorageLevel())
    result = {
        "input": str(Path(args.input).resolve()),
        "cache_enabled": bool(args.cache),
        "master": args.master,
        "partitions": args.partitions,
        "iterations": args.iterations,
        "source_keys": source_count,
        "nodes": node_count,
        "materialization_s": materialization_s,
        "iteration_s": iteration_times,
        "subsequent_mean_s": sum(iteration_times[1:]) / max(1, len(iteration_times[1:])),
        "total_runtime_s": total_runtime_s,
        "rank_count_per_iteration": rank_counts,
        "storage_level": storage_level,
        "spark_ui": sc.uiWebUrl,
        "default_parallelism": sc.defaultParallelism,
        "top5": [[int(node), float(score)] for node, score in final_ranks[:5]],
        "checksum": float(sum(score for _, score in final_ranks)),
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    if args.write_ranks:
        ranks_path = output.with_name(output.stem + "_ranks.csv")
        ranks_path.write_text("node,rank\n" + "\n".join(f"{node},{score:.12f}" for node, score in final_ranks) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)
    sc.stop()
    return result


def main() -> None:
    os.environ.setdefault("PYSPARK_PYTHON", "python")
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--iterations", type=int, default=6)
    parser.add_argument("--partitions", type=int, default=4)
    parser.add_argument("--master", default="local-cluster[2,1,1024]")
    parser.add_argument("--cache", action="store_true")
    parser.add_argument("--write-ranks", action="store_true")
    parser.add_argument("--ui-port", type=int, default=4040)
    parser.add_argument("--app-name", default="Project8-PageRank")
    args = parser.parse_args()
    if args.iterations < 2:
        raise ValueError("Use at least two iterations so materialization and reuse can be compared")
    run(args)


if __name__ == "__main__":
    main()
