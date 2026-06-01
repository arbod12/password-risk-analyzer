"""
scorer.py
=========
This file is the BRAIN of the app. It has one main job: take a password and
decide how risky it is.

app.py imports the score_password function from this file. That is why the
function name here (score_password) must EXACTLY match what app.py asks for.

Read the comments. You should be able to explain every section in an interview.
"""

# A small built-in list of the most common leaked passwords. This lets the app
# work right away without downloading anything. LATER, you can replace this with
# a real wordlist file (see the load_breach_list function below) for a stronger
# project. For now, this is enough to demonstrate the idea.
COMMON_PASSWORDS = {
    "123456", "password", "12345678", "qwerty", "123456789", "12345",
    "1234", "111111", "1234567", "dragon", "123123", "baseball",
    "abc123", "football", "monkey", "letmein", "shadow", "master",
    "666666", "qwertyuiop", "123321", "mustang", "1234567890",
    "michael", "654321", "superman", "1qaz2wsx", "7777777", "121212",
    "000000", "qazwsx", "123qwe", "killer", "trustno1", "jordan",
    "jennifer", "zxcvbnm", "asdfgh", "hunter", "buster", "soccer",
    "harley", "batman", "andrew", "tigger", "sunshine", "iloveyou",
    "2000", "charlie", "robert", "thomas", "hockey", "ranger",
    "daniel", "starwars", "klaster", "112233", "george", "computer",
    "michelle", "jessica", "pepper", "1111", "zxcvbn", "555555",
    "11111111", "131313", "freedom", "777777", "pass", "maggie",
    "159753", "aaaaaa", "ginger", "princess", "joshua", "cheese",
    "amanda", "summer", "love", "ashley", "nicole", "chelsea",
    "biteme", "matthew", "access", "yankees", "987654321", "dallas",
    "austin", "thunder", "taylor", "matrix", "william", "corvette",
    "admin", "welcome", "login", "passw0rd", "abc12345",
}


def load_breach_list(filename="passwords.txt"):
    """
    OPTIONAL UPGRADE (do this later for a stronger project):
    This reads a real downloaded password wordlist from a text file (one
    password per line) and returns it as a set for fast lookups.

    To use it: download a common-password list (e.g. a top-10000 list from the
    public SecLists project), save it as 'passwords.txt' in this folder, then
    in score_password below, swap COMMON_PASSWORDS for load_breach_list().

    For now app.py uses the built-in COMMON_PASSWORDS, so you do not need this
    yet. It is here to show how you would scale up.
    """
    breached = set()
    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            breached.add(line.strip())  # .strip() removes the newline at the end
    return breached


def estimate_crack_time(password):
    """
    Gives a rough, honest estimate of how hard a password is to guess by brute
    force. This is NOT real cryptography math, it is a simple educational
    estimate based on how many possible characters and how long the password is.
    In the README and interviews, say exactly that: it is an illustrative
    estimate, not a precise calculation.
    """
    # Figure out how big the "character pool" is based on what types are used.
    pool = 0
    if any(c.islower() for c in password):
        pool += 26          # lowercase letters a-z
    if any(c.isupper() for c in password):
        pool += 26          # uppercase letters A-Z
    if any(c.isdigit() for c in password):
        pool += 10          # digits 0-9
    if any(not c.isalnum() for c in password):
        pool += 32          # rough count of common symbols

    if pool == 0:
        return "instantly"

    # Total possible combinations = pool size raised to the password length.
    combinations = pool ** len(password)

    # Assume a fast attacker tries 10 billion guesses per second.
    guesses_per_second = 10_000_000_000
    seconds = combinations / guesses_per_second

    # Turn raw seconds into a human-friendly label.
    if seconds < 1:
        return "instantly"
    if seconds < 60:
        return "a few seconds"
    if seconds < 3600:
        return "minutes"
    if seconds < 86400:
        return "hours"
    if seconds < 31536000:
        return "days to months"
    if seconds < 31536000 * 100:
        return "years"
    return "centuries"


def score_password(password):
    """
    THE MAIN FUNCTION. app.py calls this.

    It takes a password (a string) and returns a dictionary with three things:
      - "score": a number from 0 (terrible) to 100 (strong)
      - "problems": a list of plain-English issues found
      - "crack_time": the rough estimate from estimate_crack_time()
    """
    score = 0
    problems = []

    # --- Check 1: length ---
    # Length matters more than anything else for password strength.
    if len(password) >= 12:
        score += 40
    elif len(password) >= 8:
        score += 25
    else:
        problems.append("Too short. Aim for at least 12 characters.")

    # --- Check 2: variety of character types ---
    if any(c.islower() for c in password):
        score += 10
    else:
        problems.append("No lowercase letters.")

    if any(c.isupper() for c in password):
        score += 15
    else:
        problems.append("No uppercase letters.")

    if any(c.isdigit() for c in password):
        score += 15
    else:
        problems.append("No numbers.")

    if any(not c.isalnum() for c in password):
        score += 20
    else:
        problems.append("No symbols (like ! or @).")

    # --- Check 3: is it a known/common breached password? ---
    # This is the most important real-world check: attackers try these first.
    if password.lower() in COMMON_PASSWORDS:
        score = 0  # automatic fail, no matter what else it has
        problems.append("This is one of the most common leaked passwords. "
                        "Attackers try these first.")

    # --- Check 4: obvious weak patterns ---
    if password.isdigit():
        problems.append("All numbers, very easy to guess.")
    if password.isalpha() and password.islower():
        problems.append("All lowercase letters, easy to guess.")

    # Make sure the score never goes below 0 or above 100.
    score = max(0, min(100, score))

    # Turn the number into a simple label for display.
    if score >= 70:
        label = "Strong"
    elif score >= 40:
        label = "Medium"
    else:
        label = "Weak"

    return {
        "score": score,
        "label": label,
        "problems": problems,
        "crack_time": estimate_crack_time(password),
    }


# This block only runs if you run THIS file directly (python3 scorer.py).
# It lets you test the logic without the web app. A nice way to check your work.
if __name__ == "__main__":
    for test in ["123456", "password", "sunshine", "Tr0ub4dor&3xK!"]:
        result = score_password(test)
        print(f"{test!r}: {result['label']} ({result['score']}/100) "
              f"- crack time: {result['crack_time']}")
        for p in result["problems"]:
            print(f"   - {p}")
        print()
    