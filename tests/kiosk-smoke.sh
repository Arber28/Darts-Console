#!/bin/sh
# Run on Debian as a regular user. The outer network remains untouched.
set -eu
cd "$(dirname "$0")/.."
if [ "${1:-}" != '--isolated' ]; then
    exec unshare --user --map-root-user --net sh "$0" --isolated
fi

ip link set lo up
scratch=$(mktemp -d)
trap 'if [ -n "${server:-}" ]; then kill "$server" 2>/dev/null || true; fi; rm -rf -- "$scratch"' EXIT
cp web/index.html web/scoring.js "$scratch/"
python3 - "$scratch/index.html" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
harness = """
<script>
try {
  const expect = (condition, name) => { if (!condition) throw Error(name); };
  const press = key => document.dispatchEvent(new KeyboardEvent('keydown', {key, bubbles:true}));
  expect(innerWidth === 1080 && innerHeight === 1920, '9:16 viewport '+innerWidth+'x'+innerHeight);
  expect(document.querySelector('.console').getBoundingClientRect().width === 1080, 'full-width console');
  function choose(action) {
    const count = controls().length;
    for (let i = 0; i < count; i++) {
      if (document.querySelector('.focused')?.dataset.action === action) {
        press('Enter');
        return;
      }
      press('ArrowDown');
    }
    throw Error('Could not reach ' + action);
  }
  if (location.search.includes('resume')) {
    expect(derived().history.length === 1, 'persisted history');
    expect(derived().history[0].n === 25, 'persisted corrected bull');
    press('F4');
    expect(derived().history.length === 0, 'undo after browser restart');
  } else {
    choose('mode:501');
    choose('player:Arber');
    choose('begin');
    expect(derived().players.length === 1, 'one player starting');
    choose('throw');
    choose('segment:20');
    choose('hit:20,3');
    expect(derived().players[0].score === 441, 'triple 20');
    expect(parseFloat(getComputedStyle(document.querySelector('.big-score')).fontSize) >= 200, 'distance-readable score');
    expect(document.querySelector('.score-hero').getBoundingClientRect().width >= 950, 'full scoreboard');
    expect(document.querySelector('.focused').dataset.action === 'throw', 'repeat manual scoring focus');
    press('F2');
    choose('edit:0');
    choose('segment:25');
    choose('hit:25,2');
    expect(derived().players[0].score === 451, 'bull correction');
    press('F5');
    expect(derived().round === 2, 'next turn');
  }
  parent.document.body.dataset.smoke = 'passed';
} catch (error) {
  parent.document.body.dataset.smoke = error.message;
}
</script>
"""
path.write_text(path.read_text().replace("</body>", harness + "</body>"))
PY
cat >"$scratch/smoke.html" <<'HTML'
<!doctype html><html><body style="margin:0">
<script>
const frame = document.createElement('iframe');
frame.style = 'display:block;width:1080px;height:1920px;border:0';
frame.src = '/' + location.search;
document.body.append(frame);
</script>
</body></html>
HTML
python3 -m http.server 18765 --bind 127.0.0.1 --directory "$scratch" >"$scratch/http.log" 2>&1 &
server=$!
for stage in play resume; do
    # The test process is confined to a disposable user and network namespace.
    chromium --headless --no-sandbox --disable-dev-shm-usage --no-first-run --window-size=1100,2150 \
        --user-data-dir="$scratch/profile" --dump-dom \
        "http://127.0.0.1:18765/smoke.html?kiosk&$stage" >"$scratch/dom" 2>"$scratch/browser.log" || {
            cat "$scratch/browser.log" >&2
            exit 1
        }
    if ! grep -q '<body[^>]*data-smoke="passed"' "$scratch/dom"; then
        grep -m1 '<body' "$scratch/dom" >&2
        exit 1
    fi
done
echo 'Offline Chromium smoke passed, including scoring, correction, Next, and Undo after reopening.'
