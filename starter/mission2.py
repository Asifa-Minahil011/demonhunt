"""Mission 2 — Tamayo's Blood Lab (finite automaton).   Run: python mission2.py"""
import os
from matchers import compute_transition_function, fa_match
from utils import read_text

FOLDER = "../data/blood_samples"
DEMON_MARKER = "GATTACAGATTC"
ALPHABET = "ACGT"


def reverse_complement(s):
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(complement.get(base, base) for base in reversed(s))


def print_delta_table(delta, alphabet):
    """Print delta with one row per state and one column per letter."""
    print("state " + "".join(f"{a:>4}" for a in alphabet))
    for state, row in enumerate(delta):
        print(f"{state:>5} " + "".join(f"{row[a]:>4}" for a in alphabet))


def main():
    delta_fwd = compute_transition_function(DEMON_MARKER, ALPHABET)
    print(f"=== Delta table for the marker {DEMON_MARKER} ===")
    print_delta_table(delta_fwd, ALPHABET)

    rev_marker = reverse_complement(DEMON_MARKER)
    delta_rev = compute_transition_function(rev_marker, ALPHABET)
    print(f"\nReverse complement of the marker: {rev_marker}")

    print("\n=== Blood Sample Analysis ===")
    hidden_demon_sample = None

    if os.path.exists(FOLDER):
        for filename in sorted(os.listdir(FOLDER)):
            file_path = os.path.join(FOLDER, filename)
            if os.path.isfile(file_path):
                text = read_text(file_path)
                fwd_matches, _ = fa_match(text, delta_fwd, len(DEMON_MARKER))
                rev_matches, _ = fa_match(text, delta_rev, len(rev_marker))

                print(f"{filename} | Forward strand: {len(fwd_matches)} | "
                      f"Reverse strand: {len(rev_matches)}")

                if len(fwd_matches) > 0 or len(rev_matches) > 0:
                    hidden_demon_sample = filename
    else:
        print(f"Directory {FOLDER} not found. Check your path structure.")

    if hidden_demon_sample:
        print(f"\n[!] The sample belonging to the hidden demon is: {hidden_demon_sample}")
    else:
        print("\n[!] No demon sample identified")
if __name__ == "__main__":
    main()