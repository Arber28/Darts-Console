'use strict';

const Scoring = (() => {
  const clock = 'Around the Clock';
  const x01 = ['301', '501', '701'];
  const cricketTargets = [15, 16, 17, 18, 19, 20, 25];
  const halveTargets = [20, 19, 18, 17, 16, 15, 25];
  const checkouts = ['Straight Out', 'Double Out', 'Master Out'];
  const minimum = mode => ['Cricket', 'Killer', 'Gotcha!', 'Knockout', 'Tic-Tac-Toe'].includes(mode) ? 2 : 1;
  const valid = (n, m) => (n === 0 && m === 0) ||
    (Number.isInteger(n) && ((n >= 1 && n <= 20 && [1, 2, 3].includes(m)) ||
      (n === 25 && [1, 2].includes(m))));

  function label(n, m) {
    if (n === 0) return 'Miss';
    if (n === 25) return m === 2 ? 'Inner bull' : 'Outer bull';
    return ['','S','D','T'][m] + n;
  }

  function start(mode, players, options = {}) {
    if (players.length < minimum(mode) || players.length > 20) throw Error('Invalid player count');
    return {mode, players: [...players], options: {...options}, events: [], started: Date.now()};
  }

  function replay(match) {
    const {mode, options, events} = match;
    const countdown = x01.includes(mode);
    const rounds = {'High Score': options.rounds ?? 10, Shanghai: 7, Baseball: 9, 'Halve-It': 7,
      'Bermuda Triangle': options.sequence?.length};
    const players = match.players.map((name, i) => ({
      name, score: countdown ? Number(mode) : 0, lives: 3, marks: {}, target: 1,
      number: options.numbers?.[i] ?? i + 1, active: true, last: null
    }));
    const state = {players, current: 0, round: 1, darts: [], winners: null, notice: '', history: [],
      skipped: 0, turns: []};
    const grid = options.grid ?? [];
    const owners = Array(grid.length).fill(null);
    state.owners = owners;
    let initial = players[0].score;
    let hits = 0;

    function finishTurn(bust) {
      const p = players[state.current];
      const total = state.darts.reduce((sum, dart) => sum + dart.n * dart.m, 0);
      if (bust) p.score = initial;
      else if (mode === 'Gotcha!') {
        for (const other of players) {
          if (other !== p && other.score === p.score) other.score = 0;
        }
      }
      if (mode === 'Knockout') {
        const previous = [...state.turns].reverse().find(turn =>
          turn.player !== state.current && players[turn.player].active);
        if (previous && total <= previous.total && --p.lives === 0) p.active = false;
        p.last = total;
      }
      if (['Halve-It', 'Bermuda Triangle'].includes(mode) && hits === 0) p.score = Math.floor(p.score / 2);
      state.turns.push({player: state.current, total});
      state.notice = bust ? p.name + ' busted' : '';
      const remaining = players.map((p, i) => p.active ? i : -1).filter(i => i >= 0);
      if (['Knockout', 'Killer'].includes(mode) && remaining.length === 1) {
        state.winners = remaining;
        return;
      }
      const next = remaining.find(i => i > state.current);
      if (next === undefined) {
        if (state.round === rounds[mode]) {
          const best = Math.max(...players.map(p => p.score));
          state.winners = players.flatMap((p, i) => p.score === best ? [i] : []);
          return;
        }
        state.round++;
      }
      state.current = next ?? remaining[0];
      state.darts = [];
      initial = players[state.current].score;
      hits = 0;
    }

    function throwDart(n, m) {
      const p = players[state.current];
      const points = n * m;
      const win = () => { state.winners = [state.current]; };
      const mark = (limit = Infinity) => {
        const before = p.marks[n] ?? 0;
        p.marks[n] = Math.min(limit, before + m);
        return before;
      };
      if (countdown) {
        const out = options.out ?? 'Double Out';
        const left = p.score - points;
        const legal = out === 'Straight Out' || m === 2 || (out === 'Master Out' && m === 3);
        p.score = left;
        if (left < 0 || (left === 1 && out !== 'Straight Out') || (left === 0 && !legal)) return true;
        if (left === 0) win();
        return false;
      }
      switch (mode) {
        case 'Cricket':
          if (cricketTargets.includes(n)) {
            const before = mark(3);
            if (players.some(other => other !== p && (other.marks[n] ?? 0) < 3)) {
              p.score += Math.max(0, before + m - 3) * n;
            }
            if (cricketTargets.every(target => p.marks[target] === 3) &&
                players.every(other => p.score >= other.score)) win();
          }
          break;
        case clock: {
          const target = p.target === 21 ? 25 : p.target;
          if (n === target && ++p.target > (options.bull ? 21 : 20)) win();
          break;
        }
        case 'Killer':
          if ((p.marks[p.number] ?? 0) < 3) {
            if (n === p.number) mark(3);
            break;
          }
          if (n === p.number && options.selfHit !== 'Lose lives') break;
          for (const other of players) {
            if (other.active && other.number === n) {
              other.lives = Math.max(0, other.lives - m);
              other.active = other.lives > 0;
              if (!p.active || players.filter(player => player.active).length === 1) finishTurn(false);
              break;
            }
          }
          break;
        case 'Shanghai':
          if (n === state.round) {
            p.score += points;
            if (new Set(state.darts.filter(d => d.n === n).map(d => d.m)).size === 3) win();
          }
          break;
        case 'Baseball':
          if (n === state.round) p.score += m;
          break;
        case 'High Score':
          p.score += points;
          break;
        case 'Gotcha!':
          p.score += points;
          if (p.score > 301) return true;
          if (p.score === 301) win();
          break;
        case 'Halve-It':
        case 'Bermuda Triangle': {
          const target = mode === 'Halve-It' ? {n: halveTargets[state.round - 1]} : options.sequence[state.round - 1];
          if ((target.n === undefined || n === target.n) && (!target.m || m === target.m) && points > 0) {
            p.score += points;
            hits++;
          }
          break;
        }
        case 'Tic-Tac-Toe': {
          const square = grid.indexOf(n);
          if (square === -1 || owners[square] !== null) break;
          if (mark(3) + m < 3) break;
          owners[square] = state.current;
          p.score++;
          const lines = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
          if (lines.some(line => line.every(i => owners[i] === state.current))) win();
          else if (owners.every(owner => owner !== null)) state.winners = [];
          break;
        }
      }
      return false;
    }

    events.forEach((event, index) => {
      if (state.winners || event.round !== state.round || event.player !== state.current ||
          (event.type === 'throw' && event.slot !== state.darts.length)) {
        state.skipped++;
        return;
      }
      if (event.type === 'next') {
        finishTurn(false);
        return;
      }
      const {n, m} = event;
      state.notice = '';
      state.darts.push({n, m});
      state.history.push({index, n, m, player: state.current, round: state.round});
      const bust = throwDart(n, m);
      if (!state.winners && (bust || state.darts.length === 3)) finishTurn(bust);
    });
    return state;
  }

  function record(match, n, m) {
    if (!valid(n, m)) throw Error('Invalid segment');
    const {current, round, darts, winners} = replay(match);
    if (!winners) match.events.push({type: 'throw', player: current, round, slot: darts.length, n, m});
  }

  function next(match) {
    const {current, round, winners} = replay(match);
    if (!winners) match.events.push({type: 'next', player: current, round});
  }

  function correct(match, index, n, m) {
    if (!valid(n, m) || match.events[index]?.type !== 'throw') throw Error('Invalid correction');
    Object.assign(match.events[index], {n, m});
  }

  function undo(match) {
    const history = replay(match).history;
    if (history.length) match.events.splice(history.at(-1).index);
  }

  return {start, replay, record, next, correct, undo, label, minimum, checkouts};
})();

if (typeof module !== 'undefined') module.exports = Scoring;
