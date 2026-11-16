"""Mission 3 — The Copycat Slayer (Rabin-Karp).   Run: python mission3.py"""
import os
from utils import read_text

MANUAL = "../data/hashira_manual.txt"
FOLDER = "../data/trainee_reports"
K = 40         
D = 256
Q = 1_000_000_007

def clean_text(t):
    """Lowercase, turn punctuation into spaces, collapse runs of spaces into one."""
    t = t.lower()
    cleaned = []
    for ch in t:
        if ch.isalnum() or ch.isspace():
            cleaned.append(ch)
        else:
            cleaned.append(' ')
    return " ".join("".join(cleaned).split())

def copy_detect(manual, report, k=K, d=D, q=Q):
    """
    1. Rolling-hash every k-character window of `manual`; store hash -> list of shifts.
    2. Roll the hash across `report`. On a hit, compare characters yourself (no == on slices).
    3. Mark every report character covered by a verified window.
    4. similarity = covered characters / len(report) * 100
    Return similarity_percent.
    """
    n_m = len(manual)
    n_r = len(report)

    if n_m < k or n_r < k:
        return 0.0

    # h = d^(k-1) mod q
    h = 1
    for _ in range(k - 1):
        h = (h * d) % q
    manual_hashes = {}
    p = 0
    for i in range(k):
        p = (d * p + ord(manual[i])) % q
    manual_hashes.setdefault(p, []).append(0)

    for s in range(n_m - k):
        p = (d * (p - ord(manual[s]) * h) + ord(manual[s + k])) % q
        manual_hashes.setdefault(p, []).append(s + 1)

    covered = [False] * n_r
    r_hash = 0
    for i in range(k):
        r_hash = (d * r_hash + ord(report[i])) % q

    for s in range(n_r - k + 1):
        if r_hash in manual_hashes:
            matched = False
            for m_shift in manual_hashes[r_hash]:
                j = 0
                verified = True
                while j < k:
                    if report[s + j] != manual[m_shift + j]:
                        verified = False
                        break
                    j += 1
                if verified:
                    matched = True
                    break
            
            if matched:
                for j in range(k):
                    covered[s + j] = True
        if s < n_r - k:
            r_hash = (d * (r_hash - ord(report[s]) * h) + ord(report[s + k])) % q
    covered_count = sum(1 for c in covered if c)
    similarity = (covered_count / n_r) * 100.0
    return similarity

def main():
    if not os.path.exists(MANUAL) or not os.path.exists(FOLDER):
        print(f"Error: Could not find {MANUAL} or {FOLDER}.")
        return
    manual_text = clean_text(read_text(MANUAL))

    results = []
    if os.path.exists(FOLDER):
        for filename in sorted(os.listdir(FOLDER)):
            file_path = os.path.join(FOLDER, filename)
            if os.path.isfile(file_path):
                report_text = clean_text(read_text(file_path))
                similarity = copy_detect(manual_text, report_text)
                results.append((filename, similarity))
    results.sort(key=lambda x: x[1], reverse=True)

    print("=== Copycat Slayer Rankings (Plagiarism Detection) ===")
    for rank, (filename, sim) in enumerate(results, 1):
        print(f"Rank {rank}: {filename} — Similarity: {sim:.2f}%")

if __name__ == "__main__":
    main()