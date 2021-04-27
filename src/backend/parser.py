"""
Modul Utama Parser
@params x : string message dari pengguna
"""
import re
from datetime import datetime, timedelta

from algorithm import *
from regex import *
from date import *

keywords_task = ["Kuis", "Ujian", "Tucil", "Tubes", "Praktikum"]

def case_show_all_task(x):
    """
    Mereturn true jika string x merupakan command untuk
    Menampilkan seluruh task
    return : boolean
    """
    x = x.lower()                                   # lower case x agar seragam
    
    res = {
        "showType":"all", 
        "taskType":"all",
        "startDate":"",
        "endDate":""
    }                                               # default type (all task)

    # Proses taskType, bisa berupa kuis, tubes, dll atau all
    task_type = get_all_same_pattern(keywords_task, x)
    if (len(task_type) != 0):
        res["taskType"] = task_type[0]
    
    # Keywords
    main_keywords_1 = ["lihat", "liat", "apa saja", "apa aja", "apa aj", "apa sj", "buat"]
    main_keywords_2 = ["deadline", "tugas", "dilakukan", "ada"]

    if (isPatternExistKMP(main_keywords_1, x, False) and isPatternExistKMP(main_keywords_2, x, False)):
        today = datetime.now()

        date = get_date(x)                                                      # kasus A : Periode tanggal, ambil tanggal jika ada
        keywords_B = ["minggu", "mnggu", "mng"]                                 # kasus B : N Minggu ke depan
        keywords_C = ["hari", "hri", "hr"]                                      # kasus C : N Hari ke depan
        keywords_D = ["hari ini", "hri ini", "hr ini", "sekarang", "skrng"]     # kasus D : Hari ini

        if (len(date) == 2):
            # kasus A: period
            res["showType"] = "custom"
            res["startDate"] = date[0]
            res["endDate"] = date[1]
        elif (isPatternExistKMP(keywords_B, x)):
            # kasus B : N Minggu ke depan
            nweek = int(get_number(x)[0])
            res["showType"] = "week"
            res["startDate"] = date_to_str(today)
            res["endDate"] = date_to_str(today + timedelta(days = nweek*7))
        elif (isPatternExistKMP(keywords_C, x) and len(get_number(x)) != 0):
            # kasus C : N Hari ke depan
            nday = int(get_number(x)[0])
            res["showType"] = "day"
            res["startDate"] = date_to_str(today)
            res["endDate"] = date_to_str(today + timedelta(days = nday))
        elif (isPatternExistKMP(keywords_D, x)):
            # kasus D : Hari ini
            res["showType"] = "today"
            res["startDate"] = date_to_str(today)
            res["endDate"] = res["startDate"] 

        return res

    return False

tests = ["Apa aj deadline yang dimiliki sejauh ini?", "Buat beberapa hari ke depan ada kuis apa aja?",
         "Deadline tugas IF2211 itu kapan?", "Apa saja deadline antara 20/04/2021 sampai 23-05-2021?",
         "2 Minggu ke dpan ada praktikum apa aj?", "Tugas buat 2 hari kedepan", "Hri ini ada tubes apa aja?"]

for test in tests:
    res = case_show_all_task(test)
    print(f"{test} : {res}")

