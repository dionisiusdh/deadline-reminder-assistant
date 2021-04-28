"""
Modul Algoritma KMP dan Boyer-Moore
"""


def KMP(pat, txt, case_sensitive=True):
    """
    Algoritma KMP untuk mencari pattern pat pada string txt
    Memiliki mode case sensitive dan tidak
    return : jika pattern ditemukan, array index awal ditemukannya pattern (dimulai dari 0)
             jika pattern tidak ditemukan, maka direturn []
    """
    if (not case_sensitive):
        pat = pat.lower()
        txt = txt.lower()

    lps = findLPS(pat)
    res = []

    j = 0

    for i in range(len(txt)):
        while j > 0 and txt[i] != pat[j]:
            j = lps[j - 1]

        if (txt[i] == pat[j]):
            j += 1

        if (j == len(pat)):
            res.append(i - (j - 1))
            j = lps[j - 1]

    return res


def findLPS(pat):
    """
    Mencari longest prefix suffix (lps) dari pattern pat
    return : array lps
    """
    lps = [0]

    for i in range(1, len(pat)):
        j = lps[i - 1]

        while j > 0 and pat[j] != pat[i]:
            j = lps[j - 1]

        if (pat[j] == pat[i]):
            lps.append(j + 1)
        else:
            lps.append(j)

    return lps


def isPatternExistKMP(listPat, txt, case_sensitive=True):
    # Mereturn true jika salah satu dari list pattern terdapat pada string txt
    for pat in listPat:
        if (KMP(pat, txt, case_sensitive) != []):
            return True
    return False


def findLevenshteinDistance(string1, string2):
    # Mereturn jarak levenshtein dari dua buah string

    string1 = string1.lower()
    string2 = string2.lower()

    rowCount = len(string1) + 1
    columnCount = len(string2) + 1
    matrix = [[0 for j in range(columnCount)] for i in range(rowCount)]

    for i in range(rowCount):

        for j in range(columnCount):

            if (min(i, j) == 0):

                matrix[i][j] = max(i, j)

            else:

                matrix[i][j] = min(
                    matrix[i - 1][j] + 1,
                    matrix[i][j - 1] + 1,
                    matrix[i - 1][j - 1] +
                    (1 if (string1[i - 1] != string2[j - 1]) else 0)
                )

    return matrix[rowCount - 1][columnCount - 1]


def countSimilarity(string1, string2):

    distance = findLevenshteinDistance(string1, string2)
    maxLength = max(len(string1), len(string2))

    return 1 - (distance / maxLength)


# string1 = "sItting"
# string2 = "kitTen"

# print(findLevenshteinDistance(string1, string2))
# print(countSimilarity(string1, string2))
# print(string1)
# print(string2)

# print(isPatternExistKMP(["AD","BD"], "AAABABCBBABC"))
