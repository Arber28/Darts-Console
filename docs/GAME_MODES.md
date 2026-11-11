# Game rules

These are the rules planned for the console. They're written down here so the scoring logic has a clear reference. Game modes are not playable in the current interface demo.

Each player gets up to three darts per turn. Every game will need a way to correct a missed or incorrectly detected hit, including corrections to earlier turns.

## X01: 301, 501 and 701

- Each player starts with the selected score.
- Dart points are subtracted after each hit.
- The player must reach exactly zero to win.
- Checkout options: Straight Out (any scoring segment), Double Out (a double or inner bull) and Master Out (double or triple).
- A bust ends the turn and restores the score from before that turn. A bust occurs when the player goes below zero or cannot finish legally with the remaining score.

## Cricket

Targets: 15, 16, 17, 18, 19, 20 and bull.

- A target closes after three marks: single = 1, double = 2, triple = 3.
- Outer bull counts as one mark; inner bull counts as two.
- Marks beyond the third score points if at least one opponent still has that target open.
- Extra marks score the target value each (25 for each bull mark).
- When everyone has closed a target, it no longer scores.
- To win, close every target and have at least as many points as every opponent.

## Around the Clock

- Hit 1 through 20 in order.
- Any single, double or triple of the current number counts as one successful target.
- After a hit, move to the next number immediately, even within the same turn.
- Optional final target: bull.
- First player to finish wins.

## Killer

House rules for the console:

- Assign each player a unique number from 1 to 20.
- Everyone starts with three lives.
- Hit your own number for three marks to become a killer: single = 1, double = 2, triple = 3 marks.
- Once active, hit an opponent's number to remove one, two or three lives respectively.
- A player is out at zero lives. Last player remaining wins.

Still to decide: random or manual number assignment, hits on your own number after activation, and how to handle eliminated targets.

## Shanghai

Seven rounds, one target per round: 1 in round one, 2 in round two, through 7 in round seven.

- Only hits on the round's number score.
- Single, double and triple award their normal dart points.
- Hit a single, double and triple of the current number within one turn to win immediately (Shanghai).
- Otherwise, the highest total after round seven wins.
- Tie-break rules still need to be decided.

## High Score

- Ten rounds by default, three darts per player per round.
- All hits count their normal points; misses score zero.
- Highest total after the final round wins.
- Round count can be made configurable.

## Baseball

- Nine innings, one target number per inning: 1 through 9.
- Only the current inning's number counts.
- Single = one run, double = two, triple = three.
- Most runs after nine innings wins.

## Gotcha!

The console uses the following house rules:

- Everyone starts at zero and aims for exactly 301.
- Dart points are added to the score.
- Going above 301 is a bust; restore the score from the start of the turn.
- If your score at the end of your turn exactly matches an opponent's score, reset that opponent to zero. If several opponents match, reset all of them.
- Reaching exactly 301 wins immediately.

## Knockout

Simplified house rules:

- Everyone starts with three lives.
- Add up the three darts in each turn.
- From the second turn of the match onward, compare the current turn's points with the preceding active player's last turn. You must score strictly more or lose one life.
- Skip eliminated players in the comparison.
- The last remaining player wins.

## Halve-It

Targets: 20, 19, 18, 17, 16, 15, bull.

- Each round uses only its target.
- Matching hits score their normal points, including 25/50 for bull.
- If none of a player's three darts hits the target, halve that player's running total, rounded down.
- Highest score after the final target wins.

## Bermuda Triangle

A later addition based on changing targets and specific double/triple rounds. A turn with no valid hit halves the player's total. The exact round sequence still needs to be chosen before implementation.

## Tic-Tac-Toe Darts

For two players or two teams.

- Map nine dartboard numbers to a 3×3 grid.
- Claim a square by scoring three marks on its number (single = 1, double = 2, triple = 3).
- A claimed square cannot be taken by the opponent.
- Three squares in a row, column or diagonal wins.

The nine target numbers still need to be fixed.

## Shared game features

- Saved players: Emre, Arber, Adnan, Atakan, Amir and Ali; guests can be added.
- Random player order at the beginning of a match.
- Each game has its own scoring view.
- Undo and manual correction must work across busts, eliminations and game-ending throws.

## Games to build first

Start with 301/501/701, High Score and Around the Clock. Add Cricket, Shanghai and the remaining modes once throw history and corrections work.
