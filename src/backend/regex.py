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
    list yang direturn seragam dengan format DD/MM/YYYY
    """
    res = re.findall(r"\b\d{1,2}[-/ ]\d{1,2}[-/ ]\d{4}\b", x)
    res = [date.replace("-","/").replace(" ","/") for date in res]
    return res

def get_matkul(x):
    """
    Mengambil kode mata kuliah yang ada dari x
    Asumsikan tanggal selalu valid berformat XXYYYY seperti IF1212
    return : list of kode mata kuliah
    """
    return re.findall(r"^[a-zA-Z]{2}\d{4}", x)

def get_number(x):
    """
    Mengambil angka-angka yang ada dalam x
    return : list of angka
    """
    return re.findall(r"\d+", x)

def get_all_same_pattern(listPatt, x, case_sensitive=False):
    """
    Mengambil seluruh pattern dari listPatt yang terdapat pada x
    """
    res = []
    for patt in listPatt:
        if (not case_sensitive):
            curr_res = re.findall(patt.lower(), x.lower())
        else:  
            curr_res = re.findall(patt, x)
        if (len(curr_res) != 0):
            res.append(curr_res[0])
    return res

# print(get_date("9/100/2002 dan 10/12/2011 dan 9/12/20000 dan 1 12 2000 dan 20-1-2000"))
# print(get_matkul("IF2211 dan IF22131 dan IFA2102 dan IF210"))
# print(get_number("ABC 9 sda 8 ad223"))