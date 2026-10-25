const pptxgen = require('pptxgenjs');
const path = require('path');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'Song Xinyue';
pptx.subject = 'CISC3010 Project 8';
pptx.title = 'Spark Caching and Distributed Execution';
pptx.company = 'CISC3010';
pptx.lang = 'en-US';
pptx.theme = {
  headFontFace: 'Arial',
  bodyFontFace: 'Arial',
  lang: 'en-US'
};
pptx.defineSlideMaster({
  title: 'MASTER',
  background: { color: 'F8FAFC' },
  objects: [
    { rect: { x: 0, y: 0, w: 13.333, h: 0.12, fill: { color: '2563EB' }, line: { color: '2563EB' } } },
    { text: { text: 'CISC3010 | Project 8', options: { x: 0.55, y: 7.08, w: 4.0, h: 0.18, fontFace: 'Arial', fontSize: 8, color: '64748B', margin: 0 } } },
    { text: { text: 'Spark Caching and Distributed Execution', options: { x: 8.0, y: 7.08, w: 4.8, h: 0.18, fontFace: 'Arial', fontSize: 8, color: '64748B', align: 'right', margin: 0 } } }
  ],
  slideNumber: { x: 12.9, y: 7.08, color: '64748B', fontFace: 'Arial', fontSize: 8 }
});

const C = { ink: '111827', muted: '475569', blue: '2563EB', lightBlue: 'DBEAFE', green: '16A34A', lightGreen: 'DCFCE7', amber: 'D97706', lightAmber: 'FEF3C7', gray: 'E5E7EB', rose: 'DB2777', lightRose: 'FCE7F3', white: 'FFFFFF' };
const W = 13.333;
const H = 7.5;
const root = path.resolve(__dirname, '..');

function title(slide, text, kicker = '') {
  if (kicker) slide.addText(kicker.toUpperCase(), { x: 0.62, y: 0.45, w: 3.0, h: 0.22, fontFace: 'Arial', fontSize: 9, bold: true, color: C.blue, charSpacing: 1.2, margin: 0 });
  slide.addText(text, { x: 0.62, y: kicker ? 0.72 : 0.48, w: 11.8, h: 0.48, fontFace: 'Arial', fontSize: 26, bold: true, color: C.ink, margin: 0, breakLine: false, fit: 'shrink' });
}

function text(slide, str, x, y, w, h, opts = {}) {
  slide.addText(str, { x, y, w, h, fontFace: 'Arial', fontSize: opts.fontSize || 16, color: opts.color || C.ink, bold: opts.bold || false, italic: opts.italic || false, margin: opts.margin === undefined ? 0.03 : opts.margin, breakLine: false, fit: 'shrink', valign: opts.valign || 'mid', align: opts.align || 'left', bullet: opts.bullet, paraSpaceAfterPt: opts.paraSpaceAfterPt || 0, breakLine: false });
}

function box(slide, x, y, w, h, label, fill, opts = {}) {
  slide.addShape(pptx.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.06, fill: { color: fill }, line: { color: opts.line || C.ink, width: 1.1 } });
  text(slide, label, x + 0.08, y + 0.06, w - 0.16, h - 0.12, { fontSize: opts.fontSize || 15, bold: true, align: 'center', color: opts.color || C.ink });
}

function arrow(slide, x1, y1, x2, y2, color = C.muted) {
  slide.addShape(pptx.ShapeType.line, { x: x1, y: y1, w: x2 - x1, h: y2 - y1, line: { color, width: 1.5, beginArrowType: 'none', endArrowType: 'triangle' } });
}

function chip(slide, x, y, w, label, fill, color = C.ink) {
  slide.addShape(pptx.ShapeType.roundRect, { x, y, w, h: 0.34, rectRadius: 0.05, fill: { color: fill }, line: { color: fill } });
  text(slide, label, x, y + 0.02, w, 0.26, { fontSize: 10, bold: true, color, align: 'center' });
}

function addNotes(slide, lines) {
  if (slide.addNotes) slide.addNotes(lines.join('\n'));
}

// 1
{
  const s = pptx.addSlide('MASTER');
  s.background = { color: 'F8FAFC' };
  s.addShape(pptx.ShapeType.rect, { x: 8.65, y: 0.12, w: 4.68, h: 6.75, fill: { color: 'E0ECFF' }, line: { color: 'E0ECFF' } });
  s.addShape(pptx.ShapeType.arc, { x: 8.98, y: 1.18, w: 3.85, h: 3.85, adjustPoint: 0.25, line: { color: '2563EB', width: 3, transparency: 10 }, fill: { color: 'FFFFFF', transparency: 100 } });
  s.addShape(pptx.ShapeType.arc, { x: 9.55, y: 1.75, w: 2.7, h: 2.7, adjustPoint: 0.25, line: { color: '16A34A', width: 3, transparency: 15 }, fill: { color: 'FFFFFF', transparency: 100 } });
  text(s, 'PROJECT 8', 0.72, 1.0, 3, 0.28, { fontSize: 12, bold: true, color: C.blue });
  text(s, 'Spark caching\nis a tradeoff', 0.72, 1.45, 7.2, 1.35, { fontSize: 38, bold: true, color: C.ink });
  text(s, 'A distributed PageRank experiment on two local Spark workers', 0.74, 3.15, 6.4, 0.56, { fontSize: 20, color: C.muted });
  text(s, 'Research question', 0.74, 4.38, 2.0, 0.28, { fontSize: 12, bold: true, color: C.blue });
  text(s, 'When repeated work reuses the same RDD, when does caching repay its materialization cost?', 0.74, 4.73, 6.5, 0.82, { fontSize: 20, bold: true, color: '1E3A8A' });
  chip(s, 0.74, 6.1, 1.3, '2 workers', C.lightBlue, C.blue);
  chip(s, 2.18, 6.1, 1.55, '6 iterations', C.lightGreen, C.green);
  chip(s, 3.88, 6.1, 1.55, '12 runs', C.lightAmber, C.amber);
  addNotes(s, ['Introduce the project as an experiment, not as a claim that caching always improves total runtime.', 'The key question is what happens after the first materialization when the same links RDD is reused.']);
}

// 2
{
  const s = pptx.addSlide('MASTER'); title(s, 'The project targets four observable requirements', 'Scope');
  const items = [
    ['01', 'Distributed execution', 'One driver plus two local Spark workers in local-cluster mode.', C.lightBlue, C.blue],
    ['02', 'Iterative workload', 'PageRank reuses the same adjacency-list RDD across six iterations.', C.lightGreen, C.green],
    ['03', 'Controlled comparison', 'Same graph, partitions, workers and iteration count with cache on or off.', C.lightAmber, C.amber],
    ['04', 'Evidence', 'Logs, Spark UI stages, raw timings, checksum and sequential reference.', C.lightRose, C.rose]
  ];
  items.forEach((it, i) => {
    const y = 1.45 + i * 1.25;
    s.addShape(pptx.ShapeType.roundRect, { x: 0.75, y, w: 11.8, h: 0.92, rectRadius: 0.06, fill: { color: C.white }, line: { color: 'CBD5E1', width: 1 } });
    s.addShape(pptx.ShapeType.roundRect, { x: 0.92, y: y + 0.16, w: 0.72, h: 0.58, rectRadius: 0.06, fill: { color: it[3] }, line: { color: it[3] } });
    text(s, it[0], 0.92, y + 0.24, 0.72, 0.28, { fontSize: 13, bold: true, color: it[4], align: 'center' });
    text(s, it[1], 1.92, y + 0.14, 3.2, 0.3, { fontSize: 18, bold: true });
    text(s, it[2], 1.92, y + 0.48, 9.7, 0.25, { fontSize: 13, color: C.muted });
  });
  text(s, 'The experiment is intentionally small enough to run on one laptop, but still exposes Spark stages, partitions and persistence.', 0.78, 6.63, 11.5, 0.32, { fontSize: 15, color: C.muted, italic: true });
  addNotes(s, ['Walk through the four things the teacher will look for: actual distributed components, an iterative workload, a fair cache comparison, and observable correctness/performance evidence.']);
}

// 3
{
  const s = pptx.addSlide('MASTER'); title(s, 'One shared RDD feeds repeated stages', 'Architecture');
  box(s, 0.75, 2.35, 2.05, 0.72, 'Deterministic\nedge list', C.gray, { fontSize: 16 });
  box(s, 4.1, 2.35, 2.25, 0.72, 'Spark driver', C.lightBlue, { fontSize: 18, line: C.blue });
  box(s, 8.15, 2.15, 2.05, 0.7, 'Worker 1\nExecutor', C.lightGreen, { fontSize: 15, line: C.green });
  box(s, 8.15, 3.45, 2.05, 0.7, 'Worker 2\nExecutor', C.lightGreen, { fontSize: 15, line: C.green });
  box(s, 4.1, 4.65, 2.25, 0.72, 'links RDD\nMEMORY_ONLY', C.lightAmber, { fontSize: 16, line: C.amber });
  box(s, 8.15, 4.65, 2.05, 0.72, 'Metrics +\nrank output', C.lightRose, { fontSize: 15, line: C.rose });
  arrow(s, 2.8, 2.7, 4.1, 2.7); arrow(s, 6.35, 2.45, 8.15, 2.5); arrow(s, 6.35, 2.82, 8.15, 3.8); arrow(s, 5.22, 3.1, 5.22, 4.65); arrow(s, 6.35, 5.0, 8.15, 5.0);
  chip(s, 0.8, 5.95, 2.2, 'same input each run', C.gray);
  chip(s, 3.55, 5.95, 2.65, 'cache toggle', C.lightAmber, C.amber);
  chip(s, 6.85, 5.95, 2.65, 'same resources', C.lightBlue, C.blue);
  text(s, 'The driver repeats join -> contribution -> reduce. Only the links RDD is intentionally persisted.', 0.78, 6.55, 10.8, 0.28, { fontSize: 14, color: C.muted });
  addNotes(s, ['Point out that the worker processes are real local Spark workers, while all components still share one physical laptop.', 'The links RDD is the reusable part. The rank vector changes every iteration.']);
}

// 4
{
  const s = pptx.addSlide('MASTER'); title(s, 'Caching changes the cost of the second and later iterations', 'Mechanism');
  text(s, 'Without persistence', 0.9, 1.35, 4.2, 0.3, { fontSize: 19, bold: true, color: C.muted });
  text(s, 'Each iteration can recompute the shared links lineage.', 0.9, 1.72, 4.8, 0.35, { fontSize: 14, color: C.muted });
  box(s, 0.9, 2.35, 1.75, 0.65, 'Read + group', C.gray, { fontSize: 14 });
  box(s, 3.1, 2.35, 1.65, 0.65, 'Join', C.gray, { fontSize: 14 });
  box(s, 5.2, 2.35, 1.65, 0.65, 'Reduce', C.gray, { fontSize: 14 });
  arrow(s, 2.65, 2.68, 3.1, 2.68); arrow(s, 4.75, 2.68, 5.2, 2.68);
  text(s, 'With MEMORY_ONLY', 7.15, 1.35, 4.2, 0.3, { fontSize: 19, bold: true, color: C.blue });
  text(s, 'Materialize once, then reuse cached partitions.', 7.15, 1.72, 4.9, 0.35, { fontSize: 14, color: C.muted });
  box(s, 7.15, 2.35, 1.7, 0.65, 'Read + group', C.lightAmber, { fontSize: 14, line: C.amber });
  box(s, 9.3, 2.35, 1.7, 0.65, 'Cached links', C.lightAmber, { fontSize: 14, line: C.amber });
  box(s, 11.4, 2.35, 1.2, 0.65, 'Join', C.lightBlue, { fontSize: 14, line: C.blue });
  arrow(s, 8.85, 2.68, 9.3, 2.68); arrow(s, 11.0, 2.68, 11.4, 2.68);
  s.addShape(pptx.ShapeType.line, { x: 9.8, y: 3.35, w: 0, h: 1.0, line: { color: C.amber, width: 2, dash: 'dash' } });
  text(s, 'RDD lineage still exists for recovery. Cache changes reuse, not correctness.', 2.2, 4.95, 8.8, 0.45, { fontSize: 21, bold: true, color: '1E3A8A', align: 'center' });
  text(s, 'The expected benefit appears in subsequent iterations. Total runtime also includes materialization and Spark startup.', 2.0, 5.65, 9.3, 0.45, { fontSize: 15, color: C.muted, align: 'center' });
  addNotes(s, ['This is the core design idea from the RDD paper: persistence stores partitions for reuse, while lineage remains available for recomputation.', 'Make clear that caching does not change the PageRank answer. It changes when work is paid.']);
}

// 5
{
  const s = pptx.addSlide('MASTER'); title(s, 'PageRank makes repeated reuse visible', 'Workload');
  s.addShape(pptx.ShapeType.roundRect, { x: 0.82, y: 1.35, w: 6.0, h: 4.9, rectRadius: 0.06, fill: { color: 'FFFFFF' }, line: { color: 'CBD5E1', width: 1 } });
  text(s, 'Per-iteration computation', 1.12, 1.7, 4.5, 0.3, { fontSize: 19, bold: true });
  const steps = [['1', 'Join links with current ranks'], ['2', 'Split rank across outgoing edges'], ['3', 'Reduce contributions by node'], ['4', 'Materialize new ranks']];
  steps.forEach((st, i) => { const y = 2.28 + i * 0.75; s.addShape(pptx.ShapeType.ellipse, { x: 1.15, y, w: 0.42, h: 0.42, fill: { color: C.lightBlue }, line: { color: C.blue } }); text(s, st[0], 1.15, y + 0.07, 0.42, 0.22, { fontSize: 11, bold: true, color: C.blue, align: 'center' }); text(s, st[1], 1.8, y + 0.06, 4.25, 0.28, { fontSize: 16 }); });
  s.addShape(pptx.ShapeType.roundRect, { x: 7.35, y: 1.35, w: 5.1, h: 2.0, rectRadius: 0.06, fill: { color: C.lightAmber }, line: { color: C.amber, width: 1 } });
  text(s, 'Rank recurrence', 7.75, 1.72, 2.3, 0.3, { fontSize: 18, bold: true, color: C.amber });
  text(s, 'rank_new(v) = 0.15 / N\n+ 0.85 * sum(rank(u) / out_degree(u))', 7.75, 2.18, 4.35, 0.75, { fontSize: 20, bold: true, color: C.ink, valign: 'mid' });
  s.addShape(pptx.ShapeType.roundRect, { x: 7.35, y: 3.8, w: 5.1, h: 2.45, rectRadius: 0.06, fill: { color: C.lightGreen }, line: { color: C.green, width: 1 } });
  text(s, 'Why cache helps', 7.75, 4.15, 2.8, 0.3, { fontSize: 18, bold: true, color: C.green });
  text(s, 'The graph structure stays fixed.\nThe rank vector changes.\nCaching only the reusable side isolates the mechanism.', 7.75, 4.65, 4.0, 1.1, { fontSize: 17, color: C.ink });
  addNotes(s, ['The graph is fixed across iterations, so links is the natural target for persistence.', 'The rank vector changes each time, so caching the final result would not answer the same question.']);
}

// 6
{
  const s = pptx.addSlide('MASTER'); title(s, 'The comparison holds the resource budget fixed', 'Experiment');
  const cols = [0.85, 3.3, 6.0, 8.6, 11.0];
  const headers = ['Factor', 'Small', 'Medium', 'Large', 'Control'];
  headers.forEach((h, i) => { s.addShape(pptx.ShapeType.rect, { x: cols[i], y: 1.45, w: i === 0 ? 2.0 : 2.0, h: 0.58, fill: { color: C.lightBlue }, line: { color: 'CBD5E1' } }); text(s, h, cols[i] + 0.08, 1.62, 1.84, 0.2, { fontSize: 14, bold: true, color: '1E3A8A', align: 'center' }); });
  const rows = [
    ['Edges', '2,000', '10,000', '30,000', 'same seed'],
    ['Cache', 'off / on', 'off / on', 'off / on', 'only toggle'],
    ['Iterations', '6', '6', '6', 'same'],
    ['Partitions', '4', '4', '4', 'same'],
    ['Workers', '2', '2', '2', 'same'],
    ['Repeats', '2', '2', '2', 'variation']
  ];
  rows.forEach((row, r) => row.forEach((cell, c) => { const x = cols[c]; const y = 2.03 + r * 0.58; s.addShape(pptx.ShapeType.rect, { x, y, w: 2.0, h: 0.58, fill: { color: r % 2 ? 'FFFFFF' : 'F8FAFC' }, line: { color: 'CBD5E1' } }); text(s, cell, x + 0.08, y + 0.15, 1.84, 0.2, { fontSize: 14, bold: c === 0, color: c === 0 ? C.ink : C.muted, align: c === 0 ? 'left' : 'center' }); }));
  s.addShape(pptx.ShapeType.roundRect, { x: 1.0, y: 6.0, w: 11.25, h: 0.55, rectRadius: 0.06, fill: { color: 'EFF6FF' }, line: { color: 'BFDBFE' } });
  text(s, 'Initial materialization is measured separately from the five later iterations.', 1.25, 6.16, 10.75, 0.2, { fontSize: 16, bold: true, color: '1E3A8A', align: 'center' });
  addNotes(s, ['Stress that cached and uncached runs have the same input, same partitions, same two-worker budget, and same six iterations.', 'The separation between first materialization and later iterations is required by the assignment and is essential for interpretation.']);
}

// 7
{
  const s = pptx.addSlide('MASTER'); title(s, 'Caching helps later iterations most on the largest input', 'Result');
  s.addImage({ path: path.join(root, 'results', 'cache_speedup.png'), x: 0.8, y: 1.35, w: 7.1, h: 4.0 });
  s.addShape(pptx.ShapeType.roundRect, { x: 8.45, y: 1.55, w: 3.9, h: 3.35, rectRadius: 0.06, fill: { color: C.lightBlue }, line: { color: 'BFDBFE' } });
  text(s, 'Subsequent iterations', 8.85, 1.92, 3.0, 0.3, { fontSize: 18, bold: true, color: C.blue });
  text(s, '2,000 edges\n0.984x\n\n10,000 edges\n1.005x\n\n30,000 edges\n1.056x', 8.85, 2.45, 2.5, 1.9, { fontSize: 17, bold: true, color: C.ink });
  text(s, 'Cached time is lower when the repeated work is large enough to repay persistence.', 0.82, 5.8, 11.0, 0.4, { fontSize: 18, bold: true, color: '1E3A8A', align: 'center' });
  addNotes(s, ['Read the result as a mechanism result: caching lowers later iteration time on the large workload.', 'The small workload is a useful counterexample. It prevents an overclaim that caching always helps.']);
}

// 8
{
  const s = pptx.addSlide('MASTER'); title(s, 'Materialization cost explains the small-data slowdown', 'Result');
  s.addImage({ path: path.join(root, 'results', 'iteration_timing.png'), x: 0.7, y: 1.25, w: 7.3, h: 4.2 });
  const bullets = [
    ['Small', 'Cached total runtime is higher because the first materialization dominates.', C.amber],
    ['Medium', 'Later iteration times are almost identical.', C.muted],
    ['Large', 'Cached later iterations are faster and total time is slightly lower.', C.green]
  ];
  bullets.forEach((b, i) => { const y = 1.65 + i * 1.25; s.addShape(pptx.ShapeType.ellipse, { x: 8.55, y: y + 0.04, w: 0.28, h: 0.28, fill: { color: b[2] }, line: { color: b[2] } }); text(s, b[0], 9.05, y, 2.7, 0.28, { fontSize: 18, bold: true, color: b[2] }); text(s, b[1], 9.05, y + 0.35, 3.1, 0.58, { fontSize: 14, color: C.muted }); });
  text(s, 'A slowdown is a valid distributed-systems result when the mechanism cost is visible and explained.', 1.0, 6.0, 11.1, 0.35, { fontSize: 17, bold: true, color: C.ink, align: 'center' });
  addNotes(s, ['This slide answers the “why did caching not always win?” question.', 'The teacher explicitly allows a carefully explained slowdown as a valid result.']);
}

// 9
{
  const s = pptx.addSlide('MASTER'); title(s, 'Correctness and observability are part of the result', 'Evidence');
  const cards = [
    ['Correctness', 'Sequential reference\nmax error: 4.99e-13\nchecksum: 1.0', C.lightGreen, C.green],
    ['Runtime evidence', 'Per-iteration timings\nmaterialization separated\nmean +/- standard deviation', C.lightBlue, C.blue],
    ['Distributed evidence', 'Spark UI URL\npartitions and stages\nMEMORY_ONLY storage level', C.lightAmber, C.amber]
  ];
  cards.forEach((c, i) => { const x = 0.85 + i * 4.15; s.addShape(pptx.ShapeType.roundRect, { x, y: 1.55, w: 3.55, h: 3.25, rectRadius: 0.06, fill: { color: c[2] }, line: { color: c[3], width: 1.1 } }); text(s, c[0], x + 0.28, 1.95, 2.95, 0.35, { fontSize: 20, bold: true, color: c[3], align: 'center' }); text(s, c[1], x + 0.32, 2.65, 2.9, 1.25, { fontSize: 17, color: C.ink, align: 'center' }); });
  text(s, 'Every figure is traceable to raw JSON and raw_runs.csv.', 1.1, 5.65, 11.1, 0.4, { fontSize: 22, bold: true, color: '1E3A8A', align: 'center' });
  text(s, 'The code also keeps the local-cluster setting explicit so the single-laptop limitation is not hidden.', 1.3, 6.25, 10.7, 0.3, { fontSize: 14, color: C.muted, align: 'center' });
  addNotes(s, ['Correctness is independent of caching: both configurations agree with the same sequential reference.', 'The logs and raw results prove what was measured and make the figures reproducible.']);
}

// 10
{
  const s = pptx.addSlide('MASTER'); title(s, 'The result connects directly to RDD persistence and lineage', 'Reading');
  s.addShape(pptx.ShapeType.roundRect, { x: 0.85, y: 1.55, w: 5.35, h: 3.9, rectRadius: 0.06, fill: { color: C.lightBlue }, line: { color: 'BFDBFE' } });
  text(s, 'From the paper', 1.25, 1.95, 2.5, 0.32, { fontSize: 21, bold: true, color: C.blue });
  text(s, 'RDDs expose a fault-tolerant abstraction for in-memory cluster computing. Persistence can reuse computed partitions. Lineage provides a path for recomputation when a partition is lost.', 1.25, 2.55, 4.45, 1.55, { fontSize: 18, color: C.ink });
  s.addShape(pptx.ShapeType.roundRect, { x: 7.1, y: 1.55, w: 5.35, h: 3.9, rectRadius: 0.06, fill: { color: C.lightGreen }, line: { color: 'BBF7D0' } });
  text(s, 'In this project', 7.5, 1.95, 2.7, 0.32, { fontSize: 21, bold: true, color: C.green });
  text(s, 'links.persist(MEMORY_ONLY) stores the shared graph partitions. The local two-worker deployment measures reuse and makes the lineage-based recovery assumption explicit, without claiming multi-machine scale.', 7.5, 2.55, 4.45, 1.55, { fontSize: 18, color: C.ink });
  text(s, 'Reading: Zaharia et al., NSDI 2012 | Current API: Apache Spark RDD Programming Guide', 1.1, 6.05, 11.1, 0.35, { fontSize: 15, color: C.muted, align: 'center' });
  addNotes(s, ['The project does not reproduce the entire paper. It implements one idea accurately and states its simplifications.', 'The key connection is persistence for reuse plus lineage for recovery.']);
}

// 11
{
  const s = pptx.addSlide('MASTER'); title(s, 'The repository is ready for the demo and final submission', 'Close');
  const left = ['README with setup and commands', 'Spark code and local-cluster launcher', 'Correctness checker and sample input', 'Raw JSON / CSV results and scripts'];
  const right = ['3-4 page report with references', 'Presentation demo and speaker notes', 'AI-use and external-code disclosure', 'After 26 Oct: add feedback changes'];
  text(s, 'Included', 0.95, 1.45, 2.2, 0.35, { fontSize: 22, bold: true, color: C.blue });
  text(s, 'Still required after presenting', 7.0, 1.45, 4.4, 0.35, { fontSize: 22, bold: true, color: C.amber });
  left.forEach((v, i) => { const y = 2.1 + i * 0.75; s.addShape(pptx.ShapeType.ellipse, { x: 1.0, y: y + 0.03, w: 0.22, h: 0.22, fill: { color: C.green }, line: { color: C.green } }); text(s, v, 1.42, y, 4.85, 0.32, { fontSize: 17 }); });
  right.forEach((v, i) => { const y = 2.1 + i * 0.75; s.addShape(pptx.ShapeType.ellipse, { x: 7.05, y: y + 0.03, w: 0.22, h: 0.22, fill: { color: C.amber }, line: { color: C.amber } }); text(s, v, 7.47, y, 4.85, 0.32, { fontSize: 17 }); });
  s.addShape(pptx.ShapeType.roundRect, { x: 1.0, y: 5.55, w: 11.15, h: 0.72, rectRadius: 0.06, fill: { color: 'EFF6FF' }, line: { color: 'BFDBFE' } });
  text(s, 'Main takeaway: caching pays when repeated reuse is large enough to amortize materialization.', 1.25, 5.78, 10.65, 0.25, { fontSize: 20, bold: true, color: '1E3A8A', align: 'center' });
  addNotes(s, ['Close with the main takeaway and show the demo if time allows.', 'The only intentionally pending item is the actual feedback after the scheduled presentation. It must be filled before the final 5 November submission.']);
}

pptx.writeFile({ fileName: path.join(__dirname, 'project8_spark_presentation.pptx') });
