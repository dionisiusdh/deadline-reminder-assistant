from firebase import db


def firestoreQueryResultsToDictArray(firestoreQueryResults):
    array = []

    for data in firestoreQueryResults:
        array.append(data.to_dict())

    return array


def getNewId(collection):
    result = firestoreQueryResultsToDictArray(
        db.collection(collection).stream())

    maxId = 0

    if (len(result) > 0):
        for task in result:
            taskId = int(task["taskId"])

            maxId = max(maxId, taskId)

    return str(maxId)
