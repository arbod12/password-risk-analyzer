"""
analyze.py
==========
This file does the DATA ANALYSIS part of the project. It looks at a list of
common passwords, calculates some findings, and saves charts as image files
(PNG) that app.py then displays.

You run this ONCE (python3 analyze.py) to generate the chart images. You do not
need it running for the web app, app.py just shows the images it produced.

For now it analyzes the same built-in COMMON_PASSWORDS list from scorer.py so it
works with no downloads. LATER, point it at a real downloaded wordlist for a
bigger, more impressive dataset (see the note in load_passwords).
"""

import matplotlib
matplotlib.use("Agg")  # lets matplotlib save images without opening a window
import matplotlib.pyplot as plt
from collections import Counter

# We reuse the built-in list from scorer.py so everything stays consistent.
from scorer import COMMON_PASSWORDS


def load_passwords():
    """
    Returns the list of passwords to analyze.

    RIGHT NOW: uses the built-in list (works immediately).
    LATER UPGRADE: to analyze a real, large wordlist, download one (e.g. a
    top-10000 list from the public SecLists project), save it as
    'passwords.txt' in this folder, and replace the line below with:

        with open("passwords.txt", encoding="utf-8", errors="ignore") as f:
            return [line.strip() for line in f]

    A bigger dataset makes your findings and charts more impressive.
    """
    return list(COMMON_PASSWORDS)


def make_length_chart(passwords):
    """Bar chart: how many passwords are each length."""
    lengths = [len(p) for p in passwords]
    length_counts = Counter(lengths)

    # Sort by length so the bars are in order.
    x = sorted(length_counts.keys())
    y = [length_counts[length] for length in x]

    plt.figure(figsize=(8, 4))
    plt.bar(x, y, color="#2f4429")
    plt.title("Password length distribution")
    plt.xlabel("Length (characters)")
    plt.ylabel("Number of passwords")
    plt.tight_layout()
    plt.savefig("length_chart.png", dpi=120)
    plt.close()
    print("Saved length_chart.png")


def make_category_chart(passwords):
    """Bar chart: how many passwords fall into weak categories."""
    only_lower = sum(1 for p in passwords if p.isalpha() and p.islower())
    only_digits = sum(1 for p in passwords if p.isdigit())
    has_symbol = sum(1 for p in passwords if any(not c.isalnum() for c in p))

    labels = ["Only lowercase", "Only numbers", "Has a symbol"]
    values = [only_lower, only_digits, has_symbol]

    plt.figure(figsize=(8, 4))
    plt.bar(labels, values, color=["#a83d22", "#9a6a14", "#2f4429"])
    plt.title("Weak-pattern categories")
    plt.ylabel("Number of passwords")
    plt.tight_layout()
    plt.savefig("category_chart.png", dpi=120)
    plt.close()
    print("Saved category_chart.png")


def print_findings(passwords):
    """Prints the key numbers you will quote in your README and interviews."""
    total = len(passwords)
    short = sum(1 for p in passwords if len(p) <= 8)
    avg_len = sum(len(p) for p in passwords) / total

    print("\n--- KEY FINDINGS (use these in your README) ---")
    print(f"Total passwords analyzed: {total}")
    print(f"Average length: {avg_len:.1f} characters")
    print(f"Passwords 8 characters or shorter: {short} "
          f"({100 * short / total:.0f}%)")
    print("-----------------------------------------------\n")


if __name__ == "__main__":
    passwords = load_passwords()
    print_findings(passwords)
    make_length_chart(passwords)
    make_category_chart(passwords)
    print("Done. Charts saved. Now uncomment the st.image lines in app.py.")
