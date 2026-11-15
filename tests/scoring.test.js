const {test} = require('node:test');
const assert = require('node:assert/strict');
const score = require('../web/scoring');
const pair = ['Emre', 'Arber'];
const play = (match, ...darts) => darts.forEach(([n, m]) => score.record(match, n, m));
const view = score.replay;

function leave(match, n, m) {
  play(match, [20,3], [20,3], [20,3], [20,3], [n,m], [0,0]);
}

test('double-out bust restores turn score, switches player and can be undone', () => {
  const match = score.start('301', pair);
  play(match, [20,3], [20,3], [20,3]);
  score.next(match);
  play(match, [20,3], [20,3]);
  assert.equal(view(match).players[0].score, 121);
  assert.equal(view(match).current, 1);
  score.undo(match);
  assert.equal(view(match).players[0].score, 61);
  assert.equal(view(match).current, 0);
});

test('checkout multipliers and inner bull', () => {
  for (const [out, final, third] of [
    ['Straight Out', [1,1], [0,0]],
    ['Master Out', [17,3], [10,1]],
    ['Double Out', [25,2], [11,1]]
  ]) {
    const match = score.start('301', ['Emre'], {out});
    if (out === 'Straight Out') leave(match, 20, 3);
    else leave(match, ...third);
    play(match, final);
    assert.deepEqual(view(match).winners, [0], out);
    score.undo(match);
    assert.equal(view(match).winners, null);
  }
});

test('illegal exact checkout and overshoot both bust', () => {
  for (const dart of [[17,3], [20,3]]) {
    const match = score.start('301', ['Emre']);
    leave(match, 10, 1);
    play(match, dart);
    assert.equal(view(match).players[0].score, 51);
    assert.match(view(match).notice, /busted/);
  }
});

test('historical corrections preserve player identity and survive serialization', () => {
  const match = score.start('High Score', pair, {rounds:1});
  play(match, [20,3], [1,1], [1,1], [20,2], [1,1], [1,1]);
  score.correct(match, 0, 0, 0);
  const restored = JSON.parse(JSON.stringify(match));
  assert.deepEqual(view(restored).players.map(p => p.score), [2,42]);
  assert.deepEqual(view(restored).winners, [1]);
});

test('a correction that causes an early bust skips incompatible darts', () => {
  const match = score.start('301', ['Emre']);
  leave(match, 11, 1);
  play(match, [1,1], [1,1], [1,1]);
  score.correct(match, 6, 20, 3);
  assert.equal(view(match).players[0].score, 50);
  assert.equal(view(match).skipped, 2);
});

test('Cricket closes targets, scores excess marks and stops scoring closed targets', () => {
  const match = score.start('Cricket', pair);
  play(match, [20,3], [20,2], [25,2], [20,3], [20,1], [0,0], [20,3], [25,2]);
  const players = view(match).players;
  assert.equal(players[0].marks[25], 3);
  assert.equal(players[0].score, 65);
  assert.equal(players[1].score, 0);
});

test('Around the Clock advances immediately and accepts the optional bull', () => {
  const match = score.start('Around the Clock', ['Emre'], {bull:true});
  for (let n = 1; n <= 20; n++) play(match, [n,3]);
  assert.equal(view(match).players[0].target, 21);
  play(match, [25,1]);
  assert.deepEqual(view(match).winners, [0]);
});

test('Killer activates, eliminates and supports undo after a win', () => {
  const match = score.start('Killer', pair, {numbers:[4,16], selfHit:'Ignore'});
  play(match, [4,3], [16,3]);
  assert.deepEqual(view(match).winners, [0]);
  assert.equal(view(match).players[1].active, false);
  score.undo(match);
  assert.equal(view(match).players[1].lives, 3);
});

test('Shanghai requires three different multipliers in one turn', () => {
  const match = score.start('Shanghai', pair);
  play(match, [1,1], [1,3], [1,2]);
  assert.deepEqual(view(match).winners, [0]);
});

test('Baseball counts runs only for the inning target', () => {
  const match = score.start('Baseball', pair);
  play(match, [1,3], [2,3], [1,2]);
  assert.equal(view(match).players[0].score, 5);
  assert.equal(view(match).current, 1);
});

test('Gotcha resets opponents at end of turn', () => {
  const match = score.start('Gotcha!', pair);
  play(match, [20,3]);
  score.next(match);
  play(match, [20,3]);
  assert.equal(view(match).players[0].score, 60);
  score.next(match);
  assert.equal(view(match).players[0].score, 0);
});

test('Knockout loses a life on a tie and skips eliminated players', () => {
  const match = score.start('Knockout', [...pair, 'Ali']);
  for (let i = 0; i < 9; i++) {
    if (i % 3 !== 1) play(match, [i + 1,1]);
    score.next(match);
  }
  assert.equal(view(match).players[1].active, false);
  assert.equal(view(match).current, 0);
  play(match, [20,3]);
  score.next(match);
  assert.equal(view(match).current, 2);
});

test('Halve-It halves a score on a turn without a valid hit', () => {
  const match = score.start('Halve-It', ['Emre']);
  play(match, [20,3], [20,1], [0,0], [20,3], [0,0], [0,0]);
  assert.equal(view(match).players[0].score, 40);
});

test('Tic-Tac-Toe claims squares from the chosen grid', () => {
  const match = score.start('Tic-Tac-Toe', pair, {grid:[1,3,5,7,9,11,13,15,17]});
  play(match, [1,3], [3,3], [5,3]);
  assert.deepEqual(view(match).winners, [0]);
  assert.deepEqual(view(match).owners.slice(0,3), [0,0,0]);
});

test('Bermuda Triangle uses the supplied target and multiplier sequence', () => {
  const match = score.start('Bermuda Triangle', ['Emre'], {sequence:[{n:20}, {m:2}, {n:25,m:2}]});
  play(match, [20,3], [19,3], [0,0], [20,3], [12,2], [0,0], [25,1], [0,0], [0,0]);
  assert.equal(view(match).players[0].score, 42);
  assert.deepEqual(view(match).winners, [0]);
});
