def firestoreQueryResultsToDictArray(firestoreQueryResults):
    array = []

    for data in firestoreQueryResults:
        array.append(data.to_dict())

    return array
