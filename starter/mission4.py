"""BONUS — Breathing Styles Tournament (+10).   Run: python mission4.py"""
import matplotlib.pyplot as plt
from matchers import (naive_match, rabin_karp_match, kmp_match,
                      compute_transition_function, fa_match)
from utils import Timer

T = "a" * 100_000
P = "a" * 99 + "b"
ARENA = (T, P)

rows = []   

with Timer() as t:
    shifts, comps = naive_match(T, P)
rows.append(("Naive", len(shifts), comps, t.seconds))

with Timer() as t:
    shifts, comps, _ = rabin_karp_match(T, P)
rows.append(("Rabin-Karp", len(shifts), comps, t.seconds))

with Timer() as t:
    shifts, comps = kmp_match(T, P)
rows.append(("KMP", len(shifts), comps, t.seconds))

with Timer() as t:
    delta = compute_transition_function(P, "ab")     
    shifts, steps = fa_match(T, delta, len(P))
rows.append(("Automaton", len(shifts), steps, t.seconds))

print(f"{'Technique':<12}{'Matches':>8}{'Comparisons':>14}{'Time (s)':>12}")
for name, matches, comps, secs in rows:
    print(f"{name:<12}{matches:>8}{comps:>14,}{secs:>12.4f}")

names = [r[0] for r in rows]
comps = [r[2] for r in rows]
times = [r[3] for r in rows]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

b1 = ax1.bar(names, comps, color="#c0392b")
ax1.set_yscale("symlog", linthresh=1)      
ax1.set_ylim(0, 3e7)
ax1.set_title("Comparisons (log scale)")
ax1.bar_label(b1, labels=[f"{c:,}" for c in comps], padding=2, fontsize=8)

b2 = ax2.bar(names, times, color="#2980b9")
ax2.set_title("Time (seconds)")
ax2.bar_label(b2, labels=[f"{t:.3f}" for t in times], padding=2, fontsize=8)

for ax in (ax1, ax2):
    ax.tick_params(axis="x", rotation=20)
fig.suptitle("Breathing Styles Tournament: T = a×100,000, P = a×99 + b")
plt.tight_layout()
plt.savefig("tournament.png", dpi=150)
plt.show()