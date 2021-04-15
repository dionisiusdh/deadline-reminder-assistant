"""
Modul Pemrosesan Regex
"""

import re

# params x : string message dari pengguna

def get_date(x):
    """
    Mengambil tanggal yang ada dari x
    Asumsikan tanggal selalu valid
    Dapat berformat DD/MM/YYYY atau D/MM/YYYY atau D/M/YYYY
    Dapat menggunakan / atau - atau spasi
    return : list of tanggal
    """
    res = re.findall(r"\b\d{1,2}[-/ ]\d{1,2}[-/ ]\d{4}\b", x)
    return res

def get_matkul(x):
    """
    Mengambil kode mata kuliah yang ada dari x
    Asumsikan tanggal selalu valid berformat XXYYYY seperti IF1212
    return : list of kode mata kuliah
    """
    res = re.findall(r"^[a-zA-Z]{2}\d{4}", x)
    return res

print(get_date("9/100/2002 dan 10/12/2011 dan 9/12/20000 dan 1 12 2000 dan 20-1-2000"))
print(get_matkul("IF2211 dan IF22131 dan IFA2102 dan IF210"))