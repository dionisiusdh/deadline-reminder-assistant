"""
Modul Utama Parser
@params x : string message dari pengguna
"""
from random import randrange
from datetime import datetime, timedelta
from firebase import db
from constants import *
from algorithm import *
from regex import *
from date import *
from utils import *

# ===== KEYWORDS =====
keywords_task = ["Kuis", "Ujian", "Tucil",
                 "Tubes", "Praktikum", "Tugas", "PR", "Ulangan"]


def case_add_task(x):
    """
    Mereturn true jika string x merupakan command untuk
    Menambah sebuah task baru
    return : boolean
    """
    x = x.lower()                                   # lower case x agar seragam

    res = {
        "type": "add",
        "tanggal": "",
        "kodeMatkul": "",
        "jenis": "",
        "topik": ""
    }

    # Keywords
    preposition_keywords = ["pada", "ketika"]

    listTanggal = get_date(x)
    listMatkul = get_matkul(x)
    listJenis = get_all_same_pattern(keywords_task, x)
    # Masih asumsi hanya ada satu preposisi
    listPreposition = get_all_same_pattern(preposition_keywords, x)

    if (len(listTanggal) == 1 and len(listMatkul) == 1 and len(listJenis) == 1 and len(listPreposition) == 1):

        res["tanggal"] = listTanggal[0].strip(" ")
        res["kodeMatkul"] = listMatkul[0].strip(" ")
        res["jenis"] = listJenis[0].strip(" ")

        # Get Index Of Important Keywords
        # Asumsikan bahwa topik selalu diapit oleh <Kode Kuliah> dan <preposition_keywords>
        startIndex = int(KMP(res["kodeMatkul"], x, False)[0]) + 6
        wordFound = False
        endIndex = int(KMP(listPreposition[0], x, False)[0])

        res["topik"] = x[startIndex:endIndex].strip(" ")

        return res

    return False


def case_mark_task_done(x):
    """
    Mereturn true jika string x merupakan command untuk
    Menandai sebuah task done
    return : boolean
    """

    x = x.lower()                                   # lower case x agar seragam

    res = {
        "type": "delete",
        "taskId": "",
    }

    # taskId db panjang
    taskId = "DUMMY"

    done_keywords = ["udah", "sudah", "udh", "selesai", "usai",
                     "tuntas", "tamat", "kelar", "klr", "lewat", "sls"]

    listDone = get_all_same_pattern(done_keywords, x)
    listTask = get_all_same_pattern(keywords_task, x)

    if (len(listDone) > 0 and len(listTask) > 0):
        res["taskId"] = taskId
        return res
    return False


def case_show_all_task(x):
    """
    Mereturn true jika string x merupakan command untuk
    Menampilkan seluruh task
    return : boolean
    """
    x = x.lower()                                   # lower case x agar seragam

    res = {
        "type": "show",
        "showType": "all",
        "taskType": "all",
        "startDate": "",
        "endDate": ""
    }                                               # default type (all task)

    # Proses taskType, bisa berupa kuis, tubes, dll atau all
    task_type = get_all_same_pattern(keywords_task, x)
    if (len(task_type) != 0):
        res["taskType"] = task_type[0]

    # Keywords
    main_keywords_1 = ["lihat", "liat", "apa saja",
                       "apa aja", "apa aj", "apa sj", "buat"]
    main_keywords_2 = ["deadline", "tugas", "dilakukan", "ada"]

    if (isPatternExistKMP(main_keywords_1, x, False) and isPatternExistKMP(main_keywords_2, x, False)):
        today = datetime.now()

        # kasus A : Periode tanggal, ambil tanggal jika ada
        date = get_date(x)
        # kasus B : N Minggu ke depan
        keywords_B = ["minggu", "mnggu", "mng"]
        # kasus C : N Hari ke depan
        keywords_C = ["hari", "hri", "hr"]
        keywords_D = ["hari ini", "hri ini", "hr ini",
                      "sekarang", "skrng"]     # kasus D : Hari ini

        if (len(date) == 2):
            # kasus A: period
            res["showType"] = "custom"
            res["startDate"] = date[0]
            res["endDate"] = date[1]
        elif (isPatternExistKMP(keywords_B, x) and len(get_number(x)) != 0):
            # kasus B : N Minggu ke depan
            nweek = int(get_number(x)[0])
            res["showType"] = "week"
            res["startDate"] = date_to_str(today)
            res["endDate"] = date_to_str(today + timedelta(days=nweek*7))
        elif (isPatternExistKMP(keywords_C, x) and len(get_number(x)) != 0):
            # kasus C : N Hari ke depan
            nday = int(get_number(x)[0])
            res["showType"] = "day"
            res["startDate"] = date_to_str(today)
            res["endDate"] = date_to_str(today + timedelta(days=nday))
        elif (isPatternExistKMP(keywords_D, x)):
            # kasus D : Hari ini
            res["showType"] = "today"
            res["startDate"] = date_to_str(today)
            res["endDate"] = res["startDate"]

        return res

    return False


def case_update_task(x):
    x = x.lower()                                   # lower case x agar seragam

    res = {
        "type": "update",
        "taskId": "",
        "tanggal": ""
    }                                               # default type (all task)

    # taskId db panjang
    taskId = "DUMMY"
    changeDate = get_date(x)

    # Keywords
    main_keywords_1 = ["undur", "mundur", "maju", "mju", "ganti", "gnti"]
    main_keywords_2 = [
        "deadline", "tenggat", "tanggal", "kumpul", "ngumpul",
        "tugas", "tgas", "tgs", "kuis", "ujian", "tucil",
        "tubes", "praktikum"
    ]

    if (isPatternExistKMP(main_keywords_1, x, False) and isPatternExistKMP(main_keywords_2, x, False) and len(changeDate) != 0):
        res["taskId"] = taskId
        res["tanggal"] = changeDate[0]
        return res

    return False


def case_error():
    """
    Generate random error message
    """
    res = {
        "type": "error", "message": ""
    }

    error_messages = [
        "Pesan tidak dimengerti",
        "Maaf aku gak ngerti maksud kamu",
        "Aku nggak ngerti :(",
        "Aku gangerti, mungkin kamu butuh bantuan dengan 'help'",
        "Hmm... pesan kamu tidak aku mengerti"
    ]

    random = randrange(0, len(error_messages)-1)
    res["message"] = error_messages[random]

    return res


def case_help(x):

    main_keywords_1 = ["bot", "assistant", "chatbot", "ghembot"]
    main_keywords_2 = ["lakukan", "melakukan", "dilakukan", "bisa"]
    main_keywords_3 = ["help"]

    if (isPatternExistKMP(main_keywords_1, x, False) and isPatternExistKMP(main_keywords_2, x, False)) or isPatternExistKMP(main_keywords_3, x, False):
        helpText = """
 [Fitur]
 1. Menambahkan task baru
 2. Melihat daftar task yang harus dikerjakan
 3. Menampilkan deadline dari suatu task tertentu
 4. Memperbaharui task tertentu
 5. Menandai bahwa suatu task sudah selesai dikerjakan
 6. Menampilkan opsi help yang difasilitasi oleh assistant GhemBOT

 [Daftar kata penting]"""

        for i in range(len(keywords_task)):
            keyword = keywords_task[i]
            helpText += f"\n{i + 1}. {keyword}"

        return {"message": helpText}
    else:
        return False


def case_get_deadline_task(x):

    isTucilExist = isPatternExistKMP(["tucil"], x, False)
    isTubesExist = isPatternExistKMP(["tubes"], x, False)
    isTugasExist = isTucilExist or isTubesExist

    main_keywords_1 = ["deadline", "tenggat"]
    main_keywords_2 = ["kapan"]
    isMainKeyWordsExist = isPatternExistKMP(
        main_keywords_1, x, False) and isPatternExistKMP(main_keywords_2, x, False)

    matkulNames = get_matkul(x)
    isMatkulExist = len(matkulNames) > 0

    print(isMainKeyWordsExist)
    print(isTugasExist)
    print(isMatkulExist)
    print(matkulNames)
    print(x[:len(x)-1])

    # if isMainKeyWordsExist and isTugasExist and isMatkulExist:
    #     # get the data with the same matkul name and the same jenis
    #     tasks = []

    #     # since we are only able
    #     for matkul in matkulNames:
    #         tasksResult = db.collection(TASK_FIRESTORE_COLLECTIONS).where("mataKuliah", "in", matkulNames)

    #         if (isTucilExist):
    #             tugasKeywords.append("tucil")
    #         if (isTubesExist):
    #             tugasKeywords.append("tubes")

    #     .where("jenis", "in", tugasKeywords)

    #     tasks = firestoreQueryResultsToDictArray(tasksResult.stream())

    #     if (len(tasks) == 0):
    #         return {"message": f"Tidak ditemukan deadline untuk "}
    #     else:
    #         messageResponse = ""

    #         for i in range(len(tasks)):

    #             if (i != 0):
    #                 messageResponse += "\n"

    #             tasks = tasks[i]
    #             messageResponse += f'{i + 1}. {task["mataKuliah"]}-{task["topik"]} : {task["tanggal"]}'

    #         return {"message": messageResponse}

    # else:
    #     return False


def parse(x):
    """
    Main parse
    """
    if (case_show_all_task(x)):
        res = case_show_all_task(x)
    elif (case_update_task(x)):
        res = case_update_task(x)
    elif (case_get_deadline_task(x)):
        res = case_get_deadline_task(x)
    elif (case_help(x)):
        res = case_help(x)
    else:
        res = case_error()

    # print(f"{test} : {res}")
    return res

# tests=[
#     "Apa aj deadline yang dimiliki sejauh ini?",
#     "Buat beberapa hari ke depan ada kuis apa aja?",
#     "Deadline tugas IF2211 itu kapan?",
#     "Apa saja deadline antara 20/04/2021 sampai 23-05-2021?",
#     "2 Minggu ke dpan ada praktikum apa aj?",
#     "Tugas buat 2 hari kedepan",
#     "Hri ini ada tubes apa aja?",
#     "Deadline tugas ID 2 diganti ke 28/04/2021",
#     "Tugas 3 dimajuin ke 28-04-2021"
# ]

    # if (case_show_all_task(x)):
    #     res = case_show_all_task(x)
    # elif (case_update_task(x)):
    #     res = case_update_task(x)
    # elif (case_help(x)):
    #     res = case_help(x)
    # if (case_add_task(x)):
    #     res = case_add_task(x)
    #     print(f"{test} : {res}")
    #     return res
    # else:
    #     res = case_error()


tests = [
    "Apa aj deadline yang dimiliki sejauh ini?",
    "Buat beberapa hari ke depan ada kuis apa aja?",
    "Deadline tugas IF2211 itu kapan?",
    "Apa saja deadline antara 20/04/2021 sampai 23-05-2021?",
    "2 Minggu ke dpan ada praktikum apa aj?",
    "Tugas buat 2 hari kedepan",
    "Hri ini ada tubes apa aja?",
    "Deadline tugas ID 2 diganti ke 28/04/2021",
    "Tugas 3 dimajuin ke 28-04-2021",
    "Tubes IF2211 String Matching pada 14/04/2021",
    "Tubes IF2211 String Matching dah kelar"
]


for test in tests:
    parse(test)


# testsHelp = [
#     "apa yang bisa ghembot lakukan",
#     "Apa yang bisa assistant lakukan",
#     "bot bisa ngapain aja",
#     "help",
#     "bot ngapain ",
#     "hlp"
# ]


# for test in testsHelp:
#     print(case_help(test))
