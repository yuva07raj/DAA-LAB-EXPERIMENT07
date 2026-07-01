import random


def naive_search(text, pattern):
    n = len(text)
    m = len(pattern)
    matches = []
    comparisons = 0

    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1

        if j == m:
            matches.append(i)

    return matches, comparisons


def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1

    return lps


def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    lps = compute_lps(pattern)

    matches = []
    comparisons = 0

    i = 0
    j = 0

    while i < n:
        comparisons += 1

        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            matches.append(i - j)
            j = lps[j - 1]

        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches, comparisons


def rabin_karp(text, pattern, q=101):
    n = len(text)
    m = len(pattern)
    d = 256

    h = pow(d, m - 1, q)
    p_hash = 0
    t_hash = 0

    matches = []
    comparisons = 0

    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q

    for s in range(n - m + 1):
        if p_hash == t_hash:
            for k in range(m):
                comparisons += 1
                if text[s + k] != pattern[k]:
                    break
            else:
                matches.append(s)

        if s < n - m:
            t_hash = (
                d * (t_hash - ord(text[s]) * h) + ord(text[s + m])
            ) % q

            if t_hash < 0:
                t_hash += q

    return matches, comparisons


# ---------------- MAIN PROGRAM ----------------

text = "AABAACAADAABAABA"
pattern = "AABA"

print("Text    :", text)
print("Pattern :", pattern)

naive_matches, naive_comp = naive_search(text, pattern)
kmp_matches, kmp_comp = kmp_search(text, pattern)
rk_matches, rk_comp = rabin_karp(text, pattern)

print("\nResults:")
print("Naive Search")
print("Matches     :", naive_matches)
print("Comparisons :", naive_comp)

print("\nKMP Search")
print("Matches     :", kmp_matches)
print("Comparisons :", kmp_comp)

print("\nRabin-Karp Search")
print("Matches     :", rk_matches)
print("Comparisons :", rk_comp)

# ---------------- PERFORMANCE COMPARISON ----------------

text_large = "".join(random.choices("ABCD", k=10000))
patterns = ["AB", "ABCD", "ABCDAB", "ABCDABCD"]

print("\nPerformance Comparison")
print("{:<12} {:>12} {:>12} {:>12}".format(
    "Pattern", "Naive", "KMP", "Rabin-Karp"))
print("-" * 50)

for p in patterns:
    _, c1 = naive_search(text_large, p)
    _, c2 = kmp_search(text_large, p)
    _, c3 = rabin_karp(text_large, p)

    print("{:<12} {:>12} {:>12} {:>12}".format(
        p, c1, c2, c3))
