# Does error *diversity* (not error rate) enable transcendence?

A controlled Connect-4 replication of **Zhang et al. 2024, "Transcendence: Generative Models Can
Outperform The Experts That Train Them"** ([arXiv 2406.11741](https://arxiv.org/abs/2406.11741)),
designed to test the one claim that paper could not manipulate directly: that low-temperature
sampling transcends the experts *because* their errors are diverse (uncorrelated), and fails when
they are not.

## 1. Background: what the paper proves and what it only correlates

The paper trains an autoregressive transformer on chess games of players rated ≤1000 and shows it
plays at ~1500 when sampled at temperature τ→0. Its theory (Section 3):

* **Thm 1** – at τ=1 the imitator is the *mixture* of experts; a linear reward of a mixture never
  beats the best mixture component. No transcendence.
* **Thm 2** – transcendence via low temperature is possible **iff** the argmax of the mixture beats
  the best expert.
* **Thm 3/4** – sufficient conditions: a single expert with i.i.d. random errors (denoising), or several
  experts each optimal on a different region and random elsewhere (complementary). In both cases the
  argmax of the mixture is the optimal move.

The mechanism is implicit **majority voting**. It only works when the wrong moves don't agree with
each other. The paper *hypothesises* this is why ChessFormer-1500 fails (less move entropy in the
data) but cannot manipulate error correlation in human games.

## 2. Hypotheses tested here

Connect 4 is exactly solved (Pons' solver + opening book), so the reward of every move at every
state is known exactly and the experts can be synthetic with **controllable error structure**.

Let the experts have a total error rate ρ per state, of which a fraction **π is shared**:

* on *bias states* (a deterministic hash of the position, measure β = π·ρ) **every expert plays the
  same wrong move**;
* elsewhere each expert independently errs with prob. (ρ−β)/(1−β), picking a uniformly random
  non-optimal move.

The imitator is trained identically on each dataset and evaluated at several temperatures against
the solver. Predictions (all falsifiable from the logits, no sampling noise):

| | τ = 1 | τ → 0 |
|---|---|---|
| **H1** π = 0 (all errors idiosyncratic, Thm 3) | ≈ expert accuracy 1−ρ | transcends: accuracy → 1 |
| **H2** π = 1 (all errors shared) | ≈ 1−ρ | **no transcendence**: reproduces the shared error, accuracy ≈ 1−ρ |
| **H3** 0 < π < 1 | ≈ 1−ρ | accuracy ≈ 1 − π·ρ, i.e. **gain declines linearly with π** at fixed ρ |
| **H4** complementary experts (Thm 4) | ≈ mixture | beats *every* expert |
| **H5** on bias states specifically | ≈ expert | accuracy ≈ 0 (the bias survives), while non-bias states → 1 |

(In practice ρ applies only to states where a worse move exists; the theory lines in the plots use
the *realized* random/shared error rates recorded by the generator.)

A positive H1 + negative H2 with **the same error rate** is the causal evidence that diversity, not
noise level, is what gets denoised. H3 gives a dose–response curve. H5 shows the mechanism state by
state. We also record the paper's "favor" distribution (per-state ΔE[r] between τ and τ=1) exactly.

### The original "blindness" idea is a special case

A dataset where every expert never plays the centre in the opening is a *shared* bias (π=1
concentrated in the first plies). Thm 2 predicts low temperature cannot recover the centre, so that
setup is included only as a control (`--mode blind`), not as a test of discovery.

## 3. Setup

```
third_party/connect4/   Pons' exact solver (AGPL) + 7x6.book (downloaded by scripts/setup.sh)
c4/game.py              7x6 board, move-sequence tokens (BOS, 7 columns, 3 results, PAD)
c4/solver.py            persistent solver subprocess (weak mode: win/draw/loss) + cache
c4/experts.py           synthetic experts: modes iid (ρ, π) / complementary (K) / selection (K, α) / rule / blind
c4/generate.py          multiprocess dataset generation -> data/<tag>.npz + .meta.json
c4/model.py             nanoGPT-style decoder (default 8L/8H/256d ≈ 6.4M params)
c4/train.py             next-token training; logs argmax accuracy & E[r] on val states every N steps
c4/evaluate.py          `states`: logit-based E[r], P(optimal), bias/non-bias split, favor, per τ
                        `match`: head-to-head games vs expert / perfect bot (5 retries on illegal move)
c4/plots.py             fig1 reward vs τ · fig2 gain vs π (+theory) · fig6 selection gain vs α (+threshold) · fig3 bias vs non-bias · fig4 favor · fig5 training
c4/report.py            RESULTS.md = NARRATIVE.md + auto-generated tables
scripts/setup.sh        build solver, download book, `uv sync`
scripts/smoke.sh        toy end-to-end run (minutes, CPU/MPS)
scripts/run_grid.sh     full grid (5 π values × 3 seeds + complementary + blind)
scripts/overnight_*.sh  the two queues (CPU data generation / MPS training+eval) used for the overnight run
```

The imitator plays **blind**: it only ever sees the move sequence, like PGN in the paper. Every game
ends with a result token (as the PGN result), training loss covers moves and result.

## 3b. Results

See **`RESULTS.md`** (narrative + auto-generated tables + figures) and `overnight/notes.md` (chronological log with the
decisions taken during the overnight run). Settings actually used: 80k games/condition, 1600 steps × batch 512, one seed
per condition plus second seeds for the core cells.

## 4. Running

```bash
./scripts/setup.sh                       # once
N=4000 STEPS=400 ./scripts/smoke.sh      # ~5 min sanity check, writes results/figs_smoke/
./scripts/run_grid.sh                    # full grid; env vars: N_GAMES SEEDS EPOCHS RHO PIS EXTRA
uv run python -m c4.plots                # regenerate figures from results/ and runs/
```

Cost model (measured on an M4 laptop): data generation is CPU-bound in the solver, ~1.9 ms per
state ≈ 40 ms per game per core (games average 21 plies). 300k games ≈ 3.3 core-hours per dataset,
so 7 datasets ≈ 23 core-hours (parallelises perfectly). Training a 6.4M-param model for 3 epochs on
300k games (~40M tokens) is a few minutes on any modern GPU. Evaluation is seconds.

## 5. Reading the results

`results/<tag>/seed<k>/states.json` has, per τ: `er` (expected reward), `acc` (P(optimal)),
`acc_bias` / `acc_nonbias`, `gain_vs_best_expert`, plus `expert` baselines, `realized` error rates
and the `theory` prediction. `results/figs/fig2_gain_vs_pi.png` is the headline figure: measured
τ→0 accuracy gain vs π, against the dotted theory line (= realized random-error rate).

Success criteria: H1 gain > 0 and H2 gain ≈ 0 with matched error rate; H3 monotone decreasing and
close to theory; H5 bias-state accuracy near 0 at τ→0 while non-bias accuracy near 1.

Things that would be informative if they *fail*: a finite-capacity model may not reach the argmax
of the mixture (the theory assumes the exact mixture is learned), so the gain at π=0 may saturate
below the theory line; how far below is a measurement of how well imitation learns the mode.
