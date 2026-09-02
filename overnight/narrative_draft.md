# Draft narrative for RESULTS.md (to be finalized with the last runs)

## What was run (overnight, Apple M4, MPS)
- 80k training games per condition (≈1.6M states), 3k held-out test games (≈60k states) from the same experts, fresh seed.
- Imitator: 6.3M-param decoder (8 layers, 256 d), blind play on move tokens, 1600 steps × batch 512 (≈10 epochs), one seed
  (second seeds for the core conditions if time allowed). Exact rewards from Pons' solver for every state and move.
- Evaluation from logits (no sampling noise) at τ ∈ {0.001, 0.1, 0.3, 0.5, 0.75, 1.0, 1.5}, plus 150-game matches vs the expert.

## Findings

1. **Denoising works and scales with error diversity (H1, H3).** At fixed error rate, the τ→0 gain over the expert falls
   monotonically with the shared fraction π: +0.040 (π=0), +0.017 (π=0.5), −0.017 (π=1) in E[r]. Sign flips as predicted.
   Magnitudes are ~¼ of the theoretical ceiling because the imitator never reaches the argmax of the mixture on unseen
   states (its τ=1 accuracy is *below* the expert in every condition: the learned distribution is a flatter copy of the data).

2. **A learnable shared error is reproduced exactly and cannot be denoised (H2).** In the `rule` condition (all experts
   play the leftmost legal column on plies divisible by 3) the model's accuracy on rule plies equals the expert's to three
   decimals in every phase and at every checkpoint from step 200. The same holds for the opening-blindness control:
   P(centre | empty board) = 0.0001 at τ=1, 0 at τ→0. No discovery.

3. **An unlearnable shared error is denoised on unseen states — a finite-data effect outside the per-state theory.** In
   the hash-defined π=1 condition, accuracy on bias states at τ→0 is 0.007 in the opening (seen states: Theorem 2 holds)
   but 0.41 / 0.56 in mid/late game (unseen states: the model generalizes the majority, optimal behaviour). The relevant
   notion of "shared" for a finite imitator is *shared across experts and representable as a function of the state*.

4. **Skill selection has a threshold where predicted.** With fully shared errors outside expertise and routing strength α,
   the τ→0 gain vs the best expert is −0.104 (α=0), −0.043 (α=0.2), +0.126 (α=0.45), +0.169 (α=1), bracketing α*=1/3.
   Below the threshold low temperature *hurts* (it commits to the shared error). At τ=1 the routed mixture already beats
   the best expert for every α>0: selection transcendence does not need low temperature, denoising does.

5. **Head-to-head matches agree in sign** with the state-level analysis except in the π=1 case, where the model beats the
   expert (0.61) despite no state-level transcendence: the match is played on the model's own state distribution, which is
   mostly unseen states where the hash bias gets generalized away (finding 3).

## Caveats
- One seed per condition for most cells (std over seeds available only for the core cells). Effects of ±0.02 in E[r] are
  at the edge of what one seed supports; the sign pattern across conditions is the robust result.
- The model is undertrained relative to the theory's assumption (τ=1 below the mixture). More data/steps should move the
  π=0 gain toward the ceiling; whether it does is itself informative.
- ρ applies only to states where a worse move exists (~52% of states), so realized error rates (~0.15) are half the nominal.
