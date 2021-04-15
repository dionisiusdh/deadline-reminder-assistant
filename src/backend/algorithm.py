"""
Modul Algoritma KMP dan Boyer-Moore
"""

def KMP(pat, txt):
    """
    Algoritma KMP untuk mencari pattern pat pada string txt
    return : jika pattern ditemukan, array index awal ditemukannya pattern (dimulai dari 0)
             jika pattern tidak ditemukan, maka direturn []
    """
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

print(KMP("ABC", "AAABABCBBABC"))