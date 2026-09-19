# Overnight notes (running log of findings, in order)

## 00:21 — iid π=0, 800 steps (archived as *_steps800)
- expert acc 0.845 / E[r] 0.461. Model τ=1: acc 0.745, E[r] 0.380 (below the mixture: underfit, val loss still falling).
- Model τ→0: acc 0.869, E[r] 0.483 → **transcends** (+0.021). Match vs expert at τ→0: 0.667 (10/150 illegal losses).
- By phase (open/mid/late): model E[r] 0.547/0.442/0.442 vs expert 0.450/0.462/0.490 → transcendence is concentrated in the
  opening (dense data); in later, mostly unseen states the 800-step model is still below the expert.
- Decision: 800 steps is undertrained (τ=1 acc 0.745 < expert 0.845). Switched to 1600 steps for all runs.

## 01:21 — iid π=1, 1600 steps
- expert acc 0.867. Model τ=1 acc 0.806; τ→0 acc 0.845, E[r] 0.454 vs best expert 0.472 → **no transcendence on the expert
  state distribution** (−0.017), as predicted. Yet head-to-head match at τ→0: 0.613 (15 illegal losses).
- acc on bias states at τ→0: 0.284 overall, **by phase 0.007 / 0.409 / 0.563**. Non-bias: 0.998 / 0.903 / 0.849.
- Interpretation: on *seen* states (opening) the shared error is reproduced exactly (Theorem 2: argmax of the mixture is the
  error). On *unseen* states the hash-defined bias is unpredictable, so the model generalizes the majority behaviour
  (optimal) → partial "denoising" of a shared error that is shared across experts but random across states. This is a
  finite-data / generalization effect outside the per-state theory, and it explains the positive match score: the match is
  played on the model's own state distribution where most states are new.
- Consequence for the design: a shared bias only survives low temperature if it is *learnable* (a function of the state
  the model can represent). Added the `rule` condition (all experts play the leftmost legal column on plies divisible by 3)
  as the proper H2 test; the opening-blindness condition is the other learnable shared bias.

## 01:57 — selection α=0 (uniform routing, fully shared errors outside expertise), 1600 steps
- Best single expert acc 0.452 / E[r] 0.332. Mixture puts 0.25 on the optimal move and 0.75 on the shared wrong move.
- Model τ=1: acc 0.475, E[r] 0.314 (≈ mixture). Model τ→0: acc 0.366, E[r] 0.228 → **−0.104 vs best expert: low
  temperature makes it worse**, exactly as Theorem 2 predicts when the argmax of the mixture is the shared error.
- acc on states with a wrong move available: 0.132 at τ→0 (the model commits the shared error); states with no wrong
  move: 1.000. Match vs expert bot: 0.197 at τ→0 vs 0.480 at τ=1 — head-to-head confirms that low temperature hurts here.
- This is the anti-transcendence corner of the α sweep; α=1 should be the opposite corner.

## 02:28 — selection α=1 (perfect routing), 1600 steps
- Best single expert acc 0.737 / E[r] 0.336 (each expert is optimal only in its region). Mixture with perfect routing is optimal.
- Model τ=1: acc 0.944, E[r] 0.477 (already far above the best expert: routing alone gives transcendence, no temperature needed).
  Model τ→0: acc 0.976, E[r] 0.504 → **+0.169 vs best expert**. acc on states with a wrong move 0.931, others 1.000.
- Together with α=0 (−0.104) the two corners of the α sweep bracket the predicted threshold α*=1/3. Intermediate α pending.

## 02:58 — iid π=0, 1600 steps (replaces the 800-step run)
- expert acc 0.845 / E[r] 0.461. Model τ=1: acc 0.763, E[r] 0.395 (still flatter than the mixture). Model τ→0: acc 0.890,
  E[r] 0.501 → **+0.040 vs expert** (800 steps gave +0.021: the gain grows with training). Theory ceiling acc 1.0.
- Head-to-head vs expert: τ→0 wins, τ=1 loses (0.187) — at τ=1 the imitator is a *noisier* copy of a noisy expert.
- Reading: the imitator has not fit the mixture (τ=1 acc 0.763 < 0.845); low temperature removes both the experts' noise
  and the model's own residual entropy. The gap to the theoretical ceiling (1.0) is a measurement of how far a 6M model
  trained on 80k games is from the argmax of the mixture on unseen states.

## 03:26 — rule condition (learnable shared bias: leftmost legal column on plies divisible by 3, plus ρ=0.3 iid noise), 1600 steps
- Realized error rates on the test set: shared 0.169, random 0.100 (total 0.269). Expert acc 0.729 / E[r] 0.404.
- Model τ=1: acc 0.672, E[r] 0.356. Model τ→0: acc 0.750, E[r] 0.423 → **+0.019 vs expert**. Theory (rule reproduced
  exactly, random errors denoised): acc 0.831. Observed: non-bias states 0.875 (theory 1.0), rule plies 0.511 (theory 0.287).
- Rule plies by phase: **0.248 / 0.632 / 0.728**. In the opening (seen states) the model follows the shared rule, as Thm 2 says.
  In unseen mid/late states it increasingly plays the *optimal* move instead of the rule, even though the rule is a simple,
  learnable function of the sequence (ply index and column occupancy). Same pattern as the hash bias in π=1, weaker.
- **Resolved with the checkpoint sweep and the expert baseline:** the expert's own accuracy on rule plies is exactly
  0.248 / 0.632 / 0.728 (= how often the leftmost legal column happens to be optimal). The model matches it to three
  decimals at every checkpoint from step 200 on. So the model learned the shared rule *immediately and exactly*, in seen
  and unseen states alike; the apparent "0.73 optimal" late in the game is just the rule coinciding with the optimum.
  → **H2 confirmed cleanly**: a learnable shared error is reproduced by the τ→0 imitator and cannot be denoised
  (Theorem 2). The gain (+0.019) comes only from denoising the random part (non-bias states 0.875 vs expert ≈ 0.90·…).
- Contrast with π=1 (hash bias): expert acc on bias states 0/0/0, model 0.007 / 0.409 / 0.563. Unlearnable (state-random)
  shared errors are generalized away on unseen states; learnable ones are not. The relevant notion of "shared" for
  Theorem 2 in a finite model is therefore *shared and representable*, not just shared across experts.

## 03:55 — selection α=0.45 (above the predicted threshold 1/3), 1600 steps
- Mixture mass on optimal 0.5875 vs 0.4125 on the shared wrong move. Best expert acc 0.588 / E[r] 0.311.
- Model τ=1: acc 0.714, E[r] 0.378. Model τ→0: acc 0.778, E[r] 0.438 → **+0.126 vs best expert, transcends as predicted**.
- acc on states with a wrong move: 0.597 at τ→0 (theory 1.0 if the argmax were taken on the exact mixture). With a
  0.59/0.41 margin the finite model's argmax flips often → the threshold will look smoothed, not sharp.

## 04:25 — iid π=0.5, 1600 steps
- expert acc 0.857 / E[r] 0.468. Model τ=1 acc 0.779; τ→0 acc 0.876, E[r] 0.485 → **+0.017**. Theory ceiling acc 0.935.
- Bias (hash) states 0.430 at τ→0, non-bias 0.907.
- H3 so far: gain at τ→0 = +0.040 (π=0), +0.017 (π=0.5), −0.017 (π=1): **monotone decreasing in π at fixed error rate**,
  as predicted. Magnitudes are ~1/4 of the theoretical ceiling because the 6M model does not reach the argmax of the
  mixture on unseen states (τ=1 accuracy is below the expert in every condition: the model is a flatter copy of the data).

## 04:54 — blind condition (experts never play the centre in the first 4 plies, no other errors), 1600 steps
- The original "discovery" question, now as a control. Expert acc 0.963 / E[r] 0.500 (perfect except the opening blindness).
- Model τ→0: acc 0.917, E[r] 0.462 → −0.038 (nothing to denoise, and the model is imperfect on unseen states).
- On the blind opening states: expert acc 0.744 (how often a non-centre move is optimal), model 0.744 — identical.
- P(centre | empty board) = 0.0001 at τ=1 and 0.0000 at τ→0; after other first moves also ~0. The τ=1 distribution over the
  six remaining columns is uniform (0.163–0.170) as in the data. **No discovery at all**, as Theorem 2 and the taxonomy
  predict for a learnable, in-support, shared error with no competent expert.

## 05:23 — selection α=0.2 (below the predicted threshold 1/3), 1600 steps
- Mixture mass 0.40 optimal vs 0.60 shared wrong. Best expert acc 0.518 / E[r] 0.322.
- Model τ=1: acc 0.597, E[r] 0.348 (≈ mixture, above the best expert). Model τ→0: acc 0.501, E[r] 0.279 → **−0.043,
  no transcendence, low temperature hurts** as predicted. acc on states with a wrong move 0.223 at τ→0.
- Sign of the τ→0 gain across α so far: 0.0 → −0.104, 0.2 → −0.043, 0.45 → +0.126, 1.0 → +0.169. The flip lies between
  0.2 and 0.45, consistent with α* = 1/3. Interesting side result: at τ=1 the routed mixture already beats the best expert
  for every α > 0 tested (selection transcendence does not need low temperature; denoising does).

## 05:53 — selection α=0.7, 1600 steps
- Mixture mass 0.775 optimal. Best expert acc 0.639 / E[r] 0.309. Model τ=1 acc 0.804 / E[r] 0.409; τ→0 acc 0.884 /
  E[r] 0.479 → **+0.170**. acc on states with a wrong move 0.759 at τ→0 (α=0.45 gave 0.597, α=1 gave 0.931: the finite
  model's argmax follows the mixture margin smoothly rather than switching at the threshold).
- Full α sweep, τ→0 gain in E[r] vs best expert: 0 → −0.104 | 0.2 → −0.043 | 0.45 → +0.126 | 0.7 → +0.170 | 1.0 → +0.169.

## 06:22 — complementary experts (Theorem 4: K=4, each optimal in its region, uniformly random elsewhere), 1600 steps
- Best single expert E[r] 0.436; the uniform mixture has acc 0.725. Model τ=1 acc 0.668 / E[r] 0.361 (flatter than the
  mixture, as everywhere). Model τ→0 acc 0.851 / E[r] 0.513 → **+0.077 vs best expert**. Theory ceiling acc 1.0.
- Same regime as iid π=0 (uncorrelated errors → majority vote works), larger gain because the experts are individually much
  worse while the mixture's argmax is still optimal everywhere.

## 06:52 — iid π=0.25, 1600 steps
- expert acc 0.846 / E[r] 0.463. Model τ→0 acc 0.878 / E[r] 0.490 → **+0.027**. Bias states 0.403, non-bias 0.897.
- π series (τ→0 gain in E[r]): 0 → +0.040 | 0.25 → +0.027 | 0.5 → +0.017 | 1.0 → −0.017. Monotone as predicted (π=0.75 pending).

## 07:23 — iid π=0.75, 1600 steps
- expert acc 0.866 / E[r] 0.472. Model τ→0 acc 0.869 / E[r] 0.476 → **+0.004**. Bias states 0.390, non-bias 0.919.
- Final π series (τ→0 gain in E[r]): 0 → +0.040 | 0.25 → +0.027 | 0.5 → +0.017 | 0.75 → +0.004 | 1.0 → −0.017.
  Monotone and close to linear in π, as the theory's ρ(1−π) shape predicts, at ~¼ of the theoretical slope.
- Seed-0 grid complete (13 conditions). Seed-1 queue for the core cells starts now.

## 07:55 — second seeds start landing (gen finished 06:36; training only now, ~1.1 s/step)
- iid π=0 seed 1: τ→0 E[r] 0.503 vs expert 0.461 → **+0.042** (seed 0: +0.040). τ=1 acc 0.761 (seed 0: 0.763). Seed
  variance in the headline number is ≈0.002, far below the between-condition differences.

## 08:06 — stopped by request (Mariano starts work). Seed-1 queue interrupted during iid π=1 seed 1 (partial run deleted).
Resume later with:  OMP_NUM_THREADS=2 SEED=1 QUEUE=configs/overnight_queue_seed1.txt ./scripts/overnight_train2.sh
(all data already generated; the script skips finished runs).

## 10:48 — RunPod pod created: id vwd3mssu0ihgsl, RTX 4090 secure ($0.74/h), image runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404, 40GB /workspace volume, SSH key injected.

## RunPod notes
- Pod vwd3mssu0ihgsl (RTX 4090 secure, 0.74 USD/h): `nproc` reports 96 but the cgroup quota is 10.2 CPUs
  (cpu.cfs_quota_us=1020000). Data generation must use ~10 workers, not 80. Training: 0.065 s/step (1600 steps ≈ 1.7 min).
- Upload Mac → pod ≈ 200 KB/s: 438 MB of datasets take ~50 min. Next time regenerate on the pod instead (deterministic given
  seed AND --workers, since chunking depends on the worker count).
- GPU queue = scripts/gpu_queue.sh (phase A: seeds 1-2 for all 13 conditions; phase B: scaling study on pi=0, pi=1, rule with
  80k vs 320k games × 1600/6400/25600 steps). Armed by scripts/arm_gpu_queue.sh.

## Day 2 — decomposition of the pi=1 model (seen / unseen / own-play), tau->0
- Expert-state distribution: seen 60% of states (99.9% of opening, 46% of midgame, 1.5% of late). gain on seen −0.004,
  on unseen −0.036 (mid −0.029, late −0.047). The hash bias is reproduced on seen states and the model is simply worse than
  the expert on unseen states. No transcendence anywhere in the expert distribution.
- Own-play vs the expert bot (300 games): match score 0.587 (0.613 earlier with 150) — yet per-move E[r] on the model's own
  states is BELOW the expert's counterfactual E[r] at the same states (all −0.013; late −0.078). So the head-to-head win is
  NOT per-move superiority on its own trajectories. It must come from the interaction / timing of errors: the expert's hash
  errors are spread over all phases (early blunders leave the opponent many moves to convert), the model's errors are
  concentrated late. Per-state expected reward and game outcome are different objects; Zhang's Glicko metric is the latter,
  the Taxonomy's query accuracy the former. Worth one sentence in the write-up, not a project.
