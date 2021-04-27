from firebase import db


def firestoreQueryResultsToDictArray(firestoreQueryResults):
    array = []

    for data in firestoreQueryResults:
        array.append(data.to_dict())

    return array


def getNewId(collection):
    result = firestoreQueryResultsToDictArray(
        db.collection(collection).stream())
    return str(len(result) + 1)
