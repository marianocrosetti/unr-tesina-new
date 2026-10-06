# Experiment 1 — design draft (review task for applicants)

## About this document

This is the current design draft of the first experiment of my undergraduate thesis (Licenciatura en Ciencias de la Computación, Universidad Nacional de Rosario). It is a work in progress, not a finished design.

The thesis extends the study of *transcendence* (a model trained by imitation outperforming the experts that generated its data) in a solved game, Connect Four. The two reference papers are:

- [1] Zhang et al. (2024). *Transcendence: Generative Models Can Outperform The Experts That Train Them*. NeurIPS 2024. https://arxiv.org/abs/2406.11741
- [2] Abreu et al. (2025). *A Taxonomy of Transcendence*. COLM 2025. https://arxiv.org/abs/2508.17669

### The task

Please read the design below and send me a **critique** (about one page, bullet points are fine). For example:

- Flaws in the design: confounds, missing controls, metrics that don't measure what they claim, wrong derivations.
- Decisions you would change (model, data size, training, evaluation) and why.
- Whether the experiment tests something interesting and not already shown in [1] or [2].
- What you would run first to reduce the biggest risk.

I'm not looking for a "correct" answer. I want to see how you reason about an experimental design. The draft has open points, and probably errors I haven't found yet.

---

## Elements common to all experiments

### Terminology

The design of each experiment trains and evaluates the model in different **configurations**.
The results of each **configuration** will be shown in comparison tables. Each configuration is one cell of a table.
In the design section of each experiment we define the constants and variables that make up each configuration.
**Variables** are values that change between configurations; **constants** keep the same value in all configurations.

### Chosen domain

As a solved, two-player, perfect-information game we chose Connect Four:

* 2D grid, 6 rows by 7 columns.
* 2 players.
* On each turn a player chooses a column `c ∈ [1,7]` and "drops" a piece: it lands at `(h, c)`, where `h` is the lowest empty cell of column `c`.
* A full column cannot be played.
* A player who makes a vertical, horizontal or diagonal line of 4 consecutive pieces wins.
* If the board is full, the game is a draw.

### Solver

Solver: [https://github.com/PascalPons/connect4](https://github.com/PascalPons/connect4).
It returns whether a position is a win, loss or draw (for the player to move).

### Notation

* `state`: the board configuration at a given turn.
* `column`: the column chosen on a turn; also called a **move**.
* **Legal moves**: for a state, the set of columns that are not full:
  `legal(state) ⊆ [1,7]`
* **Value** of a position: `value(state) ∈ {1, ½, 0}` if `state` is a win, draw or loss, respectively.
  Note: another convention such as `{1, 0, -1}` would also work; what matters is consistency. We chose these values deliberately, in line with [1], which uses the win probability (a number between 0 and 1) given by Stockfish.
* **Reward** of a move `column` in a state `state`: `reward(state, column) ∈ {1, ½, 0}`, depending on whether it leaves the opponent in a winning, drawn or losing state:

  `reward(state, column) = 1 - value(state')`

  where `state'` is the state reached by playing `column` in `state`.

* **Optimal moves**: the legal moves with maximum `reward`.
* **Error**: playing a legal but non-optimal move.
* **Trivial state**: a state in which all moves are optimal.
  We care mostly about *non-trivial states*, i.e.:
  * states with at least one move whose reward is lower than the optimal one;
  * states in which it is possible to make a mistake.

About half of the states are trivial. This matters because we talk about ρ as the "error rate" or "probability of making a mistake". For us that probability applies **only to non-trivial states**: "of all the moves in a game where a mistake was possible (non-trivial states), what fraction are errors".
Without this caveat, the theoretical predictions would not match the experimental results.
Note that "the probability of making a mistake on a random move" is a smaller number: it is scaled by the fraction of non-trivial states.

### Dataset

* Our datasets are made of sequences. Each sequence is one game.
* The **vocabulary** has **12 tokens**: `{BOS, PAD, 1-0, 0-1, 1/2-1/2} ∪ [1,7]` (vs. the 32 characters of the PGN notation used by [1]):
  * `BOS` is the beginning-of-sequence token.
  * `1-0`, `0-1` and `1/2-1/2` are end-of-sequence tokens that also give the game result. The PGN used in [1] also includes results, so we include them.
  * `PAD`: padding token for batching (see batching).
* **Data**: each game is a sequence of these tokens. As in [1], the model only sees the sequence: not the board and not the identity of the expert.
* **Batching**: unlike [1], which builds batches by concatenating games, we use padding because:
  * Padding only wastes compute, which does not matter at our scale.
  * With several games per row, the model can attend to previous games (unless we fix it with masking, which is possible but needs a complicated, per-row mask).
  * Main reason: in our representation, the position along the sequence equals the move number, so we expect it to be easier for the positional embedding to encode "we are at move t".
    Our shared-error design uses patterns such as "every 3 moves", which we expect to be *easier to learn* with this batching choice.

### Model and training

* Model: decoder-only, based on nanoGPT (same as [1]).
* Hyperparameters kept from [1]:
  * AdamW optimizer, β = (0.9, 0.95)
  * Cosine schedule with 200 warmup steps
  * Weight decay 0.1
  * Gradient clipping 1.0
  * Dropout 0
  * bfloat16 precision
  * Learning rate (max and min of the cosine schedule): 3e-4, 3e-5
* Hyperparameters scaled to our domain:
  * (layers, heads, width): (8, 8, 256), i.e. 6.3M parameters.
    [1] uses (16, 8, 512) (50M parameters); we make it smaller because our domain is dramatically smaller.
  * Batch size: 512 rows (1 row = 1 game), about 22K tokens.
    Note: [1] measures batch size in tokens because it concatenates games; it uses 125K-token batches (~300 games per batch). Our batch is 6 to 10 times smaller than [1]'s, in line with a model 8 times smaller.
* Epochs: to be decided.
  * Preliminary experiments used 10 epochs of 80K games. Because of that we had to use *early stopping*: evaluate the checkpoint with the best validation loss, not the last one.
  * [1] trains for less than one epoch, so it has no memorization risk.
  * A control run with 320K games gives even better results than 80K, which suggests we should have generated more data to reduce the number of epochs.
  * Technically we could generate enough data to never repeat a game. It is not clear how far generating more data makes sense. Chinchilla scaling laws give 5.5M for this model size.
* Training repetitions: as in [1], we will not repeat trainings. Repeating with several seeds can make sense when the choice of train/test split can change the results, but not in deep learning with our amount of data and with the way we generate the dev and test sets (randomly; see the last section).

### Evaluation

(It is easier to read the formal definition of the experiment first, since the metrics use variables defined there.)

Only non-trivial states are used for evaluation.

The temperature policy is defined as in [1]:

`p_τ(c | e) = softmax(logits / τ)`

We define three metrics; each one gives a different notion of transcendence:

* Accuracy: the probability that the model, at temperature τ, plays an optimal move.
* Expected reward: matches the theoretical definition of transcendence in [1].
* Rating against experts.

#### Accuracy

`acc_τ(e) = Σ p_τ(c | e)` over the optimal moves `c` in `e`

`acc_τ = mean of acc_τ(e)` over the non-trivial test states

Analytically, for the expert population:
`acc(expert) = 1 − ρ`

We define *"transcendence in accuracy"* as `acc_τ(model) > acc(expert)`.

#### Expected reward

`E[r]_τ(e) = Σ_c p_τ(c | e) · r(e, c)`

`E[r]_τ =` mean over the non-trivial test states

Unlike `acc`, this metric weights each error by its cost: turning a win into a draw costs ½; into a loss, 1.
Similarly, *"transcendence in reward"* is `E[r]_τ > E[expert]_τ`.

#### Rating against experts

This mirrors how [1] presents its main result: the trained model's rating is higher than the experts', obtained by actually playing games against them instead of a state-by-state analysis.
We play 300 full games (same number as [1]) against a bot that follows the policy of the training population:

* 150 as first player
* 150 as second player

To "play with the model", at each state we sample a column from `p_τ`.
As in [1], on an illegal output we resample up to 5 times; after that the game is counted as lost.
The score is:

`score = (wins + ½ draws) / 300`

There is transcendence if `score > 0.5` (i.e. the model's expected results are better than the expert playing against itself).

### Temperature sweep

One model is trained per configuration (the variables swept across configurations are defined in the experiment design below).
Each trained model is then evaluated at several τ (all metrics depend on τ).
For each configuration we report the metrics for τ ∈ {0.001, 0.01, 0.1, 0.3, 0.5, 0.75, 1, 1.5}.
The analysis focuses on:

* τ = 1 (the model imitates the data distribution; [1] predicts it cannot transcend);
* τ → 0 (argmax; where the vote operates).

(The rest of the sweep is to draw the curve.)

---

## Experiment 1

### Goal

Quantify how the fraction of errors shared between experts affects transcendence.

### Proposed design

#### Conceptual description

We use Connect Four and train a model on synthetic games.
The games are generated by several experts.
The experts can make mistakes.
A mistake is a non-optimal move (one that worsens the position).
When they make a mistake, with probability `P` it is a shared error and with probability `(1-P)` an independent, random error.
The idea is to vary `P` and see how the playing quality of the trained model changes.

#### More formal definition

* We define the set of biased states `B` as a subset of the non-trivial states. In this subset all experts play the same wrong move `w(e)`. These are "the states where all experts make the same mistake", the "shared-error states". How `B` is built for each configuration is defined below, after a few more concepts.
* `ρ` is the expert error rate in non-trivial states. It is fixed at 0.3 for all configurations (it must be below 0.5; otherwise the majority vote cannot beat each expert and there would be no transcendence even with no shared errors).
* `P` is the fraction of the `ρ` errors that are shared.
  It is the variable swept across configurations: `P ∈ {0, 0.25, 0.5, 0.75, 1}`.

  Example: if `P = 0.2`, then in non-trivial states the experts have probability:
  * `0.06` of making a shared error;
  * `0.24` of making an independent error.

  The total probability of a mistake in a non-trivial state stays at `0.3`.
  The probability of a mistake given that the state is not only non-trivial but in `B` is `0.24/0.94 = 0.255` (defined as `q` below).

* `β = P·ρ` is the probability that a shared error happens in a non-trivial state.
  Intuitively, `β` is the fraction of visited non-trivial states that fall in `B`.
* `q = (ρ − β)/(1 − β)` is the probability of a mistake (in a non-trivial state) given that the state is outside `B`.
* Construction of `B` and `w(e)`:
  * A state is in `B` if its move number `t` belongs to `S ⊂ {1, …, 42}`.
    Informally: `S` is the set of move indices that are in `B`.
    42 is the maximum game length (6×7).
    How do we choose `S`? We want:
    * `S` spread evenly across opening, middlegame and endgame, so the shared error is not concentrated in one phase of the game.
    * With `nontrivial(t)` the fraction of non-trivial states that occur at move `t`:
      `sum of nontrivial(t) = β` for `t ∈ S`.
  * `w(e)` is the leftmost legal column that is not optimal.

**Note:** in preliminary experiments, `B` was defined with a hash of the state. A hash is hard to learn (the model does not even receive the state as input, so it would have to reconstruct it and learn to compute the hash). So on new states the model cannot know it is in `B` and does what it does on similar states.
The rule `t ∈ S` is learnable, so the shared error should be reproduced even on states of `B` not seen during training.
We propose to run the same experiment with `B` defined by a state hash as a comparison, to see how the representability of `B` affects the results.

The experts then play:

* If `e` is trivial, a random legal move.
* If `e` is non-trivial:
  * If `t ∈ S`, play `w(e)`.
  * Otherwise:
    * with probability `q`, a random wrong move;
    * with probability `1−q`, a random optimal move.

**Important note:** although we believe the rule `t ∈ S` is easy for the model to represent, it does not say whether the state is trivial nor how often it is seen during training. So the fraction of non-trivial states that fall in `B` is not `|S|/42`, but the sum, over `t ∈ S`, of the fraction of visited non-trivial states at move `t`. That is why `S` is calibrated on a pilot dataset so that this sum equals `β`, and the effective `β` is reported by measuring on the test set which fraction of the non-trivial states actually fell in `B`.

### Training, validation and test sets

All three are produced by the same generator and the same expert configuration `(ρ, P, S)`; they differ only in the random seed used to generate them.

### Correlation of errors between experts

To be written.
