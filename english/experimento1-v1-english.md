# Experiment 1

## Elements common to all experiments

## Terminology

The design of each experiment proposes training and evaluating the model in different **configurations**.&nbsp;  
Then, the results of each **configuration** will be presented in the comparison tables included in the results. Each configuration will correspond to one cell of the table.&nbsp;  
In the design section of each experiment we define the constants and variables that we will use to define each configuration that makes it up.&nbsp;  
We will call **variables** the values that change depending on the configuration and **constants** those that keep the same value in all configurations.

## Chosen domain

As a solved, two-player, complete-information game we have chosen Connect4:

* 2D grid, 6 rows high by 7 columns wide.  
* 2 players.  
* On each turn, they choose a column `c ∈ [1,7]` in which a piece is "dropped": its position will be `(h, c),` where `h` is the height of the first empty cell, from bottom to top, of column `c`.  
* A full column cannot be played.  
* If a player forms a vertical, horizontal or diagonal line of 4 consecutive pieces, they win.  
* If the board is full, the game is a draw.

## Solver

Solver used: [https://github.com/PascalPons/connect4](https://github.com/PascalPons/connect4).&nbsp;  
It tells us whether a position is a win, a loss or a draw (for the player who has to move at that moment).

## Notation and Terminology

* We will use `state` to record the board configuration at a specific turn.  
* We will use `column` to indicate the choice of the column in which to drop the piece on each turn; we will also call it a "**move**".  
* **Legal moves**: for a state, the set of columns that are not full (and in which we can therefore play):  
  `legal(state) ⊆ [1,7]`  
* **The value** of a position is `value(state) ∈ {1, ½, 0},` depending on whether `state` is a win, a draw or a loss, respectively.&nbsp;  
  Note: another convention such as `{1, 0, -1}` could have been used. What matters is being consistent. Using the chosen values is a deliberate decision, in line with \[1\], which uses the probability of winning (a number between 0 and 1\) provided by Stockfish.  
* **reward** of a move `column` in a state `state`: `reward(state, column) ∈ {1, ½, 0}` depending on whether it leads the opponent to a winning, drawn or losing state:

`reward(state, column) = 1 - value(state')`

Where `state’` is the state obtained by playing `column,` when in `state`.

* **Optimal moves**: those with maximum `reward` among the available legal ones.  
* **Error**: the act of making a legal but non-optimal move.  
* **Trivial state**: the `state` in which all moves are optimal.&nbsp;  
  We will be mainly interested in *non-trivial states*, which is equivalent to saying:  
  * States in which there is at least one move whose reward is lower than that of the optimal move.  
  * States in which it is feasible to make a mistake.&nbsp;

Close to half of the states are trivial. This is very relevant for our experiment, since we will speak of ρ as the "error proportion" or "probability of making a mistake". For us the probability will apply only to non-trivial states. That is, “of all the moves in a game where it was possible to make a mistake (non-trivial states), what fraction are errors”.&nbsp;  
Without this caveat, the theoretical predictions would not match the experimental results.  
Note that “the probability of making a mistake on a random move” will be a smaller number: adjusted by the fraction that non-trivial states represent of all states.&nbsp;

> ### Dataset

* Our datasets will be composed of sequences. Each sequence will represent one game.

* The **vocabulary** of the sequences will be the **12 tokens**: `{BOS, PAD, 1-0, 0-1, 1/2-1/2} ∪ [1,7]` (vs. the 32 characters of the PGN notation used by \[1\]):

  * `BOS` is the beginning-of-sequence token  
  * `1-0`, `0-1` and `1/2-1/2` are the end-of-sequence tokens that also indicate the result of the game. The PGN used in \[1\] also includes the results, which is why we include them.  
  * `PAD`: padding token for batching (see the batching section)  
* **Data**: Each game is represented as a sequence of the aforementioned tokens. As in \[1\], the model sees only the sequence: neither the board nor the identity of the expert.

* **Batching:** unlike \[1\], which builds batches by concatenating games, we propose to use padding because:

  * Padding only wastes compute, but does not matter at the scale we work at.  
  * If we have multiple games per row, the model can attend to previous games (unless we solve it at the masking level: although possible, it would require complicated masking that depends on each row of the batch)  
  * Main reason: in our representation, the position along the sequence dimension corresponds to the move number, so we estimate that it is easier for the positional embedding to encode "we are at move t".&nbsp;  
    In our shared-error design we will use patterns such as "every 3 moves", which we estimate are *more easily learnable* by the model with this batching choice.

### Model and training

* Model:  decoder-only, nanoGPT base (same as \[1\]).  
* Hyperparameters that we kept from \[1\]:  
  * AdamW optimizer, β \= (0.9, 0.95)  
  * Cosine schedule with warmup 200  
  * Weight decay 0.1  
  * Gradient clip 1.0  
  * Dropout 0  
  * Precision bfloat16  
  * Learning rate (respective maximum and minimum of the cosine schedule used): 3e-4, 3e-5  
* Hyperparameters that we scaled to our domain:  
  * (Layers, heads, width): (8, 8, 256\) respectively (6.3 M parameters).  
    \[1\] Uses (16, 8, 512\) (50M parameters); we shrank it because our domain is dramatically smaller.&nbsp;  
* Batch size: 512 rows (remember that for us 1 row : 1 game), approximately 22K tokens&nbsp;  
  Note: \[1\] quantifies the batch size in tokens since it trains by concatenating games; they use batches of 125K tokens each (\~300 games per batch). Our batch is between 6 and 10 times smaller than \[1\], in line with a model 8 times smaller.  
* Epochs: To be determined  
  * The preliminary experiments used 10 epochs of 80K games each. Because of that we had to adopt *early stopping*: evaluating the checkpoint with the best val loss, not the one at the end.  
  * \[1\] Trains for less than one epoch; therefore it presents no memorization risk.  
  * A control study with 320K shows even better results than with 80K games, which indicates that we should have generated more data to reduce the number of epochs.  
  * Technically, we could generate enough data so as not to have to repeat any game. It is not clear to what extent generating data makes sense. Chinchilla Laws for this model size gives 5.5M  
* Training repetitions: as in \[1\], we will not repeat the training runs. Doing so with several seeds may make sense in a context where the choice of training/test sets can change the results, but not in deep learning with the amount of data we handle and with the way we generate the development and test sets (randomly, read the last section of this document).

### Evaluation. (I recommend reading the more formal definition of the experiment first since we use variables in the metrics that are defined there)

Only non-trivial states are taken into account for the evaluation.

The temperature policy is defined as in \[1\]:&nbsp;

`p_τ(c | e) = softmax(logits / τ)`

We will define three metrics and each one induces a different notion of transcendence:&nbsp;

* Accuracy: the probability that the model, at temperature τ, plays an optimal move.  
* Expected reward: matches the theoretical definition of transcendence in \[1\]  
* Rating against experts

#### **Accuracy**

`acc_τ(e) = Σ p_τ(c | e)` over the optimal moves `c` in `e`

`acc_τ    = average of acc_τ(e)` over the non-trivial test states

It is deduced analytically that for the population of experts it holds that:&nbsp;  
`acc(expert) = 1 − ρ`&nbsp;

We define *"transcendence in accuracy"* if `acc_τ(model) > acc(expert)`

#### **Expected reward**

`E[r]_τ(e) = Σ_c p_τ(c | e) · r(e, c)`

`E[r]_τ    =` average over the non-trivial test states

Unlike `acc`, this metric weights each error by its cost: throwing a win away into a draw costs ½; into a loss, 1\.  
Analogously, we define “*transcendence in reward"* if `E[r]_τ > E[expert]_τ`&nbsp;

#### **Rating against experts**

This is a parallel to what \[1\] does to present its main result: that the rating of the trained model is higher than that of the experts, by actually making the trained model play against experts instead of doing the state-by-state analysis.&nbsp;  
In our case, we will compute it by playing 300 complete games (the same number as \[1\]) against a bot that follows the policy of the trained population:

* in 150 it will play as the first player&nbsp;  
* in 150 it will play as the second player

To "play with the model", in each state a column is sampled from p\_τ&nbsp;  
As in \[1\], upon an illegal output we sample up to 5 times and then the game is considered lost.&nbsp;  
Then the score obtained is defined as:&nbsp;

`score = (wins + ½ draws) / 300`

There is transcendence if `score > 0.5` (that is: the expected results of the model are better than if the expert had played against itself)

### Temperature sweep

In each configuration of the experiment one model will be trained. (later, in the experiment design, we define the variables swept across configurations)  
Then, for each trained model, different evaluations will be made at different τ (note that all metrics depend on τ).  
For each configuration, we will report the metrics for τ ∈ {0.001, 0.01, 0.1, 0.3, 0.5, 0.75, 1, 1.5}.&nbsp;  
In the analysis we will place special emphasis on:&nbsp;

* τ=1 (the model imitates the distribution of the data; \[1\] predicts that it cannot transcend  
* τ→0 (argmax; where voting operates).&nbsp;

(The rest of the sweep is to draw the curve)

## Experiment 1 proper

## Objective

To quantify how the proportion of errors shared among experts affects transcendence.

## Proposed design

### Conceptual description

The experiment I plan to do now, as a first step, consists of using the proposed Connect4 game and training a model with synthetic games.&nbsp;  
Those synthetic games are generated by several experts.&nbsp;  
Those experts have a probability of making mistakes.&nbsp;  
Making a mistake is making a non-optimal move (one that worsens the position)&nbsp;  
When they make a mistake, they have probability `P` of making a shared error and probability `(1-P)` of making an independent, random error.&nbsp;  
The idea is to vary `P` and see how the quality of play of the trained model improves.

### More formal definition

* We will define the set of biased states (denoted `B`) as a subset of the non-trivial states. In this subset all experts will play the same erroneous move `w(e)`. They are "the states in which all experts make a mistake in the same way", "the shared-error states". Below we will define how we will construct `B` for each configuration; first, we need to introduce some additional concepts.  
* `ρ` is the expert's error rate in non-trivial states. It is a constant fixed at 0.3 for all configurations (it has to be less than 0.5, otherwise the conditions for the majority vote to be better than each expert do not hold, so there would be no transcendence even when there are no shared errors)  
* `P` fraction of the errors of `ρ` that are shared  
  It is the variable to be swept across configurations: `P ∈ {0, 0.25, 0.5, 0.75, 1}`

  Example: if `P=0.2` then the experts, when they are in non-trivial states, have probability:  
  * `0.06` of making shared errors.  
  * `0.24` of making independent errors.

The total probability of erring in a non-trivial state remains at `0.3`  
&nbsp;The probability of erring given that one is not only in a non-trivial state, but in `B`, is `0.24/0.94 = 0.255` (we will define it as `q` later)

* `β = P·ρ` is the probability that, in a non-trivial state, a shared error occurs.&nbsp;  
  Intuitively, `β` is the fraction of the visited non-trivial states that fall in `B`.  
* `q = (ρ − β)/(1 − β)` is the probability of erring (while in a non-trivial state) given that you are outside `B`  
* Construction of `B` and `w(e)`:  
  * A state is in `B` if the move number `t` belongs to `S` `⊂ {1, …, 42}`.  
    Colloquially: `S` is the index of the moves that are in `B`  
    The 42 arises because no game has a length greater than 42 (6x7)  
    How do we define `S`? We want:  
    * `S` to be spread evenly across opening, middlegame and endgame, so that the shared error is not concentrated in one phase of the game.  
    * Letting `nontrivial(t)` be the fraction of non-trivial states that occur at `t,` we want:  
      &nbsp;`sum of nontrivial(t) = β` for `t ∈ S`  
  * We will define `w(e)` as the leftmost legal column that is not optimal.&nbsp;

**Note:** in the preliminary experiments, `B` was defined by means of a hash of the state. A hash is hard to learn (the model does not receive the state as input to begin with, so it would have to reconstruct it and learn to compute the hash). Therefore, in new states the model cannot know that it is in `B`; it does what similar states do.  
The rule `t ∈ S` is learnable, so the shared error should be reproduced even in states of `B` not seen during training.  
We propose to run a comparison of the same experiment, defining `B` by means of a hash of the state and comparing how the representability of `B` affects the results.

Then the experts will play:&nbsp;

* If `e` is trivial, play a random legal move.&nbsp;  
* If `e` is non-trivial:&nbsp;  
  * If `t \in S` play `w(e)`&nbsp;  
  * Otherwise:  
    * With probability `q` play a random erroneous move .  
    * With probability `1−q` play a random optimal move.

**Important note:** the rule `t ∈ S`, although we believe it will be easily representable for the model, does not indicate whether the state is trivial nor how many times it is seen during training, so the fraction of non-trivial states that fall in `B` is not `|S|/42`, but the sum, over `t ∈ S`, of the fraction of non-trivial states visited at move `t`. That is why `S` is calibrated with a pilot dataset so that this sum gives `β`, and the effective `β` is reported by measuring on the test set what fraction of the non-trivial states actually fell in `B`.

### Training, validation and test sets

All three are generated with the same generator and the same expert configuration

(ρ, P, S) fixed, differing only in the random seed used to generate them

### Correlation of errors between experts

Pending


 no let's not use string and period for reading ; there is no need for parity
  there must be parity of field names
  and the write values must be \subset_equal read values
  but we can read things that we cannot write
