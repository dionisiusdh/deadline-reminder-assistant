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
keywords_task = ["Kuis", "Ujian", "Tucil", "Tubes",
                 "Praktikum", "Tugas", "Ulangan"]

# Debug mode
DEBUG = False


def case_add_task(x):
    """
    Mereturn true jika string x merupakan command untuk
    Menambah sebuah task baru
    return : boolean
    """
    x = x.lower()                                   # lower case x agar seragam

    res = {
        "taskId": "",
        "tanggal": "",
        "kodeMatkul": "",
        "jenis": "",
        "topik": ""
    }

    # Keywords
    main_keywords_1 = ["tambahkan", "tambah", "add", "tmbah", "ada", "baru"]
    preposition_keywords = ["pada", "ketika", "@"]

    listTanggal = get_date(x)
    listMatkul = get_matkul(x)
    listJenis = get_all_same_pattern(keywords_task, x)
    # Masih asumsi hanya ada satu preposisi
    listPreposition = get_all_same_pattern(preposition_keywords, x)
    listMain = get_all_same_pattern(main_keywords_1, x)

    if (len(listTanggal) == 1 and len(listMatkul) == 1 and len(listJenis) == 1 and len(listPreposition) > 0 and len(listMain) > 0):

        res["tanggal"] = listTanggal[0].strip(" ")
        res["kodeMatkul"] = listMatkul[0].strip(" ").upper()
        res["jenis"] = listJenis[0].strip(" ").capitalize()

        # Get Index Of Important Keywords
        # Asumsikan bahwa topik selalu diapit oleh <Kode Kuliah> dan <preposition_keywords>
        startIndex = int(KMP(res["kodeMatkul"], x, False)[0]) + 6
        endIndex = -1
        increment = 0

        endIndexFound = False

        for preposition in listPreposition:
            for index in KMP(preposition, x, False):
                if(index > startIndex):
                    endIndex = index
                    endIndexFound = True
                    break
            if(endIndexFound):
                break

        if(endIndex == -1):
            return False

        taskId = getNewId(TASK_FIRESTORE_COLLECTIONS)

        res["topik"] = x[startIndex:endIndex].strip(" ").capitalize()
        res["taskId"] = taskId

        taskData = {
            "taskId": taskId,
            "tanggal": res["tanggal"],
            "mataKuliah": res["kodeMatkul"],
            "jenis": res["jenis"],
            "topik": res["topik"]
        }

        taskRef = db.collection(TASK_FIRESTORE_COLLECTIONS).document(taskId)
        taskRef.set(taskData)

        res["message"] = "[TASK BERHASIL DICATAT]\n"
        res["message"] += f"(ID: {taskId}) {res['tanggal']} - {res['kodeMatkul']} - {res['jenis']} - {res['topik']}"

        return res

    return False


def case_mark_task_done(x, allTask):
    """
    Mereturn true jika string x merupakan command untuk
    Menandai sebuah task done
    return : boolean
    """

    # lower case x agar seragam
    x = x.lower()

    res = {
        "message": ""
    }

    # TaskId db panjang. Asumsi posisi id Task: <keywords_task> <taskId>
    listTaskId = get_number(x)

    done_keywords = ["udah", "sudah", "udh", "selesai", "usai",
                     "tuntas", "tamat", "kelar", "klr", "lewat", "sls"]

    listDone = get_all_same_pattern(done_keywords, x)
    listTask = get_all_same_pattern(keywords_task, x)

    if (len(listDone) > 0 and len(listTask) == 1 and len(listTaskId) > 0):
        taskIdFound = False
        realTaskIndex = ""
        realTaskId = ""
        typeIndex = int(KMP(listTask[0], x, False)[0])

        listIndex = []

        for taskId in listTaskId:
            for index in KMP(taskId, x, False):
                listIndex.append(index)

        listIndex.sort()

        for index in listIndex:
            if(index > typeIndex):
                realTaskIndex = index
                break

        for taskId in listTaskId:
            for index in KMP(taskId, x, False):
                if (index == realTaskIndex):
                    realTaskId = taskId
                    break

        # Mencari apakah task dengan Id yang diinput tersedia
        idFound = False
        for task in allTask:
            if(task['taskId'] == realTaskId):
                idFound = True
                break

        # Handle kondisi ketika ditemukan id maupun tidak ditemukan
        if(idFound):
            res["message"] = f"Berhasil menandai task {realTaskId} menjadi selesai"
            tasks = db.collection(
                TASK_FIRESTORE_COLLECTIONS).document(realTaskId)
            tasks.delete()
            return res
        else:
            res["message"] = "Task dengan Id tersebut tidak dapat ditemukan"
            return res

    return False


def case_show_all_task(x, allTask):
    """
    Mereturn true jika string x merupakan command untuk
    Menampilkan seluruh task
    return : boolean
    """
    x = x.lower()           # lower case x agar seragam

    res = {"message": ""}   # result

    # Proses taskType, bisa berupa kuis, tubes, dll atau all
    task_type = get_all_same_pattern(keywords_task, x)
    if (len(task_type) != 0):
        task_type = task_type[0]
    else:
        task_type = "tugas"

    # Keywords
    main_keywords_1 = ["lihat", "liat", "apa saja",
                       "apa aja", "apa aj", "apa sj",
                       "apa", "buat", "daftar", "list"]
    main_keywords_2 = ["deadline", "tugas", "task", "dilakukan", "ada"]

    if (isPatternExistKMP(main_keywords_1, x, False) and (isPatternExistKMP(main_keywords_2, x, False) or task_type != "tugas")):
        today = datetime.now().date()

        # kasus A : Periode tanggal, ambil tanggal jika ada
        date = get_date(x)
        # kasus B : N Minggu ke depan
        keywords_B = ["minggu", "mnggu", "mng"]
        # kasus C : N Hari ke depan
        keywords_C = ["hari", "hri", "hr"]
        # kasus D : Hari ini
        keywords_D = ["hari ini", "hri ini", "hr ini",
                      "sekarang", "skrng"]

        if (len(date) == 2):
            # kasus A: period
            for i in range(len(allTask)):
                if (task_type.lower() == "tugas" or (task_type.lower() == allTask[i]["jenis"].lower())):
                    tanggal = allTask[i]["tanggal"]
                    if (str_to_date(date[0]) <= str_to_date(tanggal) <= str_to_date(date[1])):
                        matkul = allTask[i]["mataKuliah"]
                        topik = allTask[i]["topik"].capitalize()
                        jenis = allTask[i]["jenis"].capitalize()
                        res["message"] += f"(ID: {i + 1}). {tanggal} - {matkul} - {jenis} - {topik} \n"
        elif (isPatternExistKMP(keywords_B, x) and len(get_number(x)) != 0):
            # kasus B : N Minggu ke depan
            for i in range(len(allTask)):
                if (task_type.lower() == "tugas" or (task_type.lower() == allTask[i]["jenis"].lower())):
                    tanggal = allTask[i]["tanggal"]
                    if (today <= str_to_date(tanggal) <= today + timedelta(days=int(get_number(x)[0])*7)):
                        matkul = allTask[i]["mataKuliah"]
                        topik = allTask[i]["topik"].capitalize()
                        jenis = allTask[i]["jenis"].capitalize()
                        res["message"] += f"(ID: {i + 1}). {tanggal} - {matkul} - {jenis} - {topik} \n"
        elif (isPatternExistKMP(keywords_C, x) and len(get_number(x)) != 0):
            # kasus C : N Hari ke depan
            for i in range(len(allTask)):
                if (task_type.lower() == "tugas" or (task_type.lower() == allTask[i]["jenis"].lower())):
                    tanggal = allTask[i]["tanggal"]
                    if (today <= str_to_date(tanggal) <= today + timedelta(days=int(get_number(x)[0]))):
                        matkul = allTask[i]["mataKuliah"]
                        topik = allTask[i]["topik"].capitalize()
                        jenis = allTask[i]["jenis"].capitalize()
                        res["message"] += f"(ID: {i + 1}). {tanggal} - {matkul} - {jenis} - {topik} \n"
        elif (isPatternExistKMP(keywords_D, x)):
            # kasus D : Hari ini
            for i in range(len(allTask)):
                if (task_type.lower() == "tugas" or (task_type.lower() == allTask[i]["jenis"].lower())):
                    tanggal = allTask[i]["tanggal"]
                    if (tanggal == date_to_str(today)):
                        matkul = allTask[i]["mataKuliah"]
                        topik = allTask[i]["topik"].capitalize()
                        jenis = allTask[i]["jenis"].capitalize()
                        res["message"] += f"(ID: {i + 1}). {tanggal} - {matkul} - {jenis} - {topik} \n"
        else:
            # all
            for i in range(len(allTask)):
                if (task_type.lower() == "tugas" or (task_type.lower() == allTask[i]["jenis"].lower())):
                    tanggal = allTask[i]["tanggal"]
                    if (str_to_date(tanggal) >= today):
                        tanggal = allTask[i]["tanggal"]
                        matkul = allTask[i]["mataKuliah"]
                        topik = allTask[i]["topik"].capitalize()
                        jenis = allTask[i]["jenis"].capitalize()
                        res["message"] += f"(ID: {i + 1}). {tanggal} - {matkul} - {jenis} - {topik} \n"

        if (res["message"] == ""):
            return {"message": "Kamu tidak punya tugas terkait dijangka waktu ini"}

        return res

    return False


def case_update_task(x, allTask):
    x = x.lower()                                   # lower case x agar seragam

    # taskId db panjang
    taskId = get_number(x)
    changeDate = get_date(x)

    # Keywords
    main_keywords_1 = ["undur", "mundur", "maju", "mju", "ganti", "gnti"]
    main_keywords_2 = [
        "deadline", "tenggat", "tanggal", "kumpul", "ngumpul",
        "tugas", "tgas", "tgs", "kuis", "ujian", "tucil",
        "tubes", "praktikum", "pr", "task"
    ]

    lenAllTask = len(allTask)

    if (isPatternExistKMP(main_keywords_1, x, False) and isPatternExistKMP(main_keywords_2, x, False) and len(changeDate) != 0 and len(taskId) != 0):
        if (int(taskId[0]) > lenAllTask):
            return {"message": f"Tidak dapat melakukan pengubahan deadline. Coba cek ID task kamu!"}
        else:
            tasks = db.collection(
                TASK_FIRESTORE_COLLECTIONS).document(taskId[0])
            update_data = {"tanggal": changeDate[0]}
            # tasks.update(update_data)
            return {"message": f"Berhasil mengubah deadline task {taskId[0]} menjadi {changeDate[0]}"}

    return False


def case_error():
    """
    Generate random error message
    """

    error_messages = [
        "Pesan tidak dimengerti",
        "Maaf aku gak ngerti maksud kamu",
        "Aku nggak ngerti :(",
        "Aku gangerti, mungkin kamu butuh bantuan dengan 'help'",
        "Hmm... pesan kamu tidak aku mengerti"
    ]

    random = randrange(0, len(error_messages)-1)

    return {"message": error_messages[random]}


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

    keywordTugas = ["tucil", "task", "tubes", "tugas"]
    isTugasExist = isPatternExistKMP(keywordTugas, x, False)

    main_keywords_1 = ["deadline", "tenggat"]
    main_keywords_2 = ["kapan"]
    isMainKeyWordsExist = isPatternExistKMP(
        main_keywords_1, x, False) and isPatternExistKMP(main_keywords_2, x, False)

    matkulNames = get_matkul(x)
    matkulNames = [matkul.strip() for matkul in matkulNames]
    isMatkulExist = len(matkulNames) > 0

    if isMainKeyWordsExist and isTugasExist and isMatkulExist:
        # get the data with the same matkul name and the same jenis
        tasks = []

        # since we are only able to use 'in' query once only, getting the data based on the jenis are done manually
        tasksResult = db.collection(TASK_FIRESTORE_COLLECTIONS).where(
            "mataKuliah", "in", matkulNames)
        for keyword in keywordTugas:
            if (isPatternExistKMP([keyword], x, False)):
                taskQueryResult = tasksResult.where("jenis", "==", keyword)
                tasks += firestoreQueryResultsToDictArray(
                    taskQueryResult.stream())

        # filter the date to only include that the date is more than today's date
        tasksTemp = tasks
        tasks = []
        dateToday = datetime.now()
        for task in tasksTemp:
            dateTask = str_to_datetime(task["tanggal"])

            if dateTask >= dateToday:
                tasks.append(task)

        if (len(tasks) == 0):
            return {"message": f"Tidak ditemukan deadline"}
        else:
            messageResponse = "[DEADLINE]\n"

            for i in range(len(tasks)):
                task = tasks[i]

                if (i != 0):
                    messageResponse += "\n"

                messageResponse += f'Deadline {task["jenis"]} {task["mataKuliah"]} itu di tanggal {task["tanggal"]}. Semangat :)'

            return {"message": messageResponse}

    else:
        return False


def case_other(x):
    main_keywords_1 = ["thank you", "thanks", "thx", "makasih",
                       "makasi", "terima kasih", "trmks", "trims"]    # Thank you

    main_keywords_2 = ["halo", "hlo", "hai", "hi", "selamat"]

    if (isPatternExistKMP(main_keywords_1, x, False)):
        messages = [
            "Sama-sama",
            "Terima kasih kembali :)",
            "Yoii sama-sama",
            "Sipp"
        ]

        random = randrange(0, len(messages)-1)

        return {"message": messages[random]}
    elif (isPatternExistKMP(main_keywords_2, x, False)):
        messages = [
            "Halo!",
            "Hi!",
            "Halo juga",
            "Hai juga",
            "Senang bertemu dengan mu",
            "Sup bro"
        ]

        random = randrange(0, len(messages)-1)

        return {"message": messages[random]}

    return False


def parse(x):
    """
    Main parse
    """
    # Get all task
    allTask = firestoreQueryResultsToDictArray(
        db.collection(TASK_FIRESTORE_COLLECTIONS).stream())

    res_show_all_task = case_show_all_task(x, allTask)
    res_update_task = case_update_task(x, allTask)
    res_get_deadline_task = case_get_deadline_task(x)
    res_add = case_add_task(x)
    res_task_done = case_mark_task_done(x, allTask)
    res_help = case_help(x)
    res_other = case_other(x)

    if (res_get_deadline_task):
        print(res_get_deadline_task) if DEBUG else ""
        return res_get_deadline_task
    elif (res_show_all_task):
        print(res_show_all_task) if DEBUG else ""
        return res_show_all_task
    elif (res_add):
        print(res_add) if DEBUG else ""
        return res_add
    elif (res_update_task):
        print(res_update_task) if DEBUG else ""
        return res_update_task
    elif (res_task_done):
        print(res_task_done) if DEBUG else ""
        return res_task_done
    elif (res_help):
        print(res_help) if DEBUG else ""
        return res_help
    elif (res_other):
        print(res_other) if DEBUG else ""
        return res_other
    else:
        print(case_error()) if DEBUG else ""
        return case_error()


tests = [
    # "deadline tubes IF2200 kapan ya"
    # "hari ni ada tugas apa aja",
    # "lihat Tugas 2 minggu kedepan",
    # "lihat tucil 2 minggu kedepan",
    # "tugasnya ada apa aja ya",
    # "tubesnya ada apa aja ya",
    # "prnya ada apa aj",
    # "ganti tugas ID 100 menjadi 28/02/2022"
    # "Apa aj deadline yang dimiliki sejauh ini?",
    # "Hri ini ada apa aja",
    # "Buat beberapa hari ke depan ada kuis apa aja?",
    # "Deadline tugas IF2200 itu kapan?",
    # "Apa saja deadline antara 20/04/2021 sampai 23-05-2021?",
    # "2 Minggu ke dpan ada praktikum apa aj?",
    # "Tugas buat 2 hari kedepan",
    # "Hri ini ada tubes apa aja?",
    # "Deadline tugas ID 4 diganti ke 29/06/2022",
    # "Tugas 3 dimajuin ke 28-04-2021",
    # "Pada pada ketika Tubes pada ketika IF2211 String Matching pada ketika 14/04/2021",
    # "300 Tubes 5 300 245 346 String Matching 300 dah kelar",
]

if DEBUG:
    for test in tests:
        print(test)
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
