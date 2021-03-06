from datetime import datetime


def date_to_str(date):
    """
    Mereturn string berformat DD/MM/YYYY dari sebuah datetime
    """
    if (date.month < 10):
        return f"{date.day}/0{date.month}/{date.year}"
    return f"{date.day}/{date.month}/{date.year}"


def str_to_date(x):
    """
    Mereturn sebuah objek date dari string x
    x dapat berformat DD/MM/YYYY atau DD-MM-YYYY atau DD MM YYYY
    """
    if ("/" in x):
        x = x.split("/")
    elif ("-" in x):
        x = x.split("-")
    elif (" " in x):
        x = x.split(" ")

    return datetime(int(x[2]), int(x[1]), int(x[0])).date()


def str_to_datetime(x):
    """
    Mereturn sebuah objek date dari string x
    x dapat berformat DD/MM/YYYY atau DD-MM-YYYY atau DD MM YYYY
    """
    if ("/" in x):
        x = x.split("/")
    elif ("-" in x):
        x = x.split("-")
    elif (" " in x):
        x = x.split(" ")

    return datetime(int(x[2]), int(x[1]), int(x[0]))

# print(str_to_date("28/08/2012"))
