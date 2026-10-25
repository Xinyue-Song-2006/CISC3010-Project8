# Speaker notes

## Timing

The deck has eleven slides for a 20-minute presentation. Spend about one minute on the motivation and scope, six minutes on the architecture and mechanism, six minutes on the experiment and results, four minutes on correctness and reading connection, and three minutes on limitations and the close.

## Key messages

1. The project uses two actual local Spark worker processes, not only a sequential script.
2. PageRank is iterative and reuses the same links RDD, which makes persistence measurable.
3. Cached and uncached runs use the same workload and resource limits.
4. Caching improves later iterations on the largest workload by about 5.6%, but the small workload becomes slower overall because materialization dominates.
5. Both configurations produce the same answer, with a maximum reference error near 5e-13.
6. The RDD paper connection is persistence for reuse plus lineage for recovery.

## Demo sequence

1. Show the architecture slide and identify the driver, two workers, shared links RDD and metrics.
2. Run `scripts/run_demo.ps1`.
3. Point to the log lines for `local-cluster[2,1,1024]`, storage level, partitions, and iteration timings.
4. Run `src/verify_correctness.py` and show the maximum absolute error.
5. Open the submitted `results/cache_speedup.png` and `results/summary.csv` if the live Spark UI is not available.

## Question preparation

### Why does caching make the small input slower?

The first materialization and Spark startup cost are larger than the saving from avoiding recomputation. The assignment allows a carefully explained slowdown.

### Why do the cached and uncached answers match?

Caching changes where Spark stores intermediate partitions. It does not change the PageRank recurrence or the input data.

### What happens if a cached partition is lost?

Spark can recompute it from the RDD lineage. This project explains that assumption but does not run the optional executor-failure extension.

### Is this cluster-scale performance?

No. All workers share one laptop. The experiment demonstrates distributed execution and the caching mechanism under a fixed local resource budget.
