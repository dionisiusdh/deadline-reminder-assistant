import json
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from firebase import db
from constants import TASK_FIRESTORE_COLLECTIONS
from utils import firestoreQueryResultsToDictArray, getNewId
import parser


app = Flask(__name__)
CORS(app)


# Routes

# get all task
@app.route("/task", methods=["GET"])
def getAllTask():
    try:
        filterParamNames = ["mataKuliah", "jenis", "topik"]

        # get all data from collection
        tasksResult = db.collection(TASK_FIRESTORE_COLLECTIONS)

        # filter
        for filterParamName in filterParamNames:
            filterParamValue = request.args.get(filterParamName)

            if filterParamValue is not None:
                tasksResult = tasksResult.where(
                    filterParamName, "==", filterParamValue)

        tasks = firestoreQueryResultsToDictArray(tasksResult.stream())

        res = {
            "message": "Success getting all task data",
            "data": {
                "tasks": tasks
            }
        }

    except:
        res = {
            "message": "Error occured on querying all task data"
        }

    finally:
        return jsonify(res)


# add task
@app.route("/task", methods=["POST"])
def addTask():
    try:
        requestBody = request.get_json()

        tanggal = requestBody["tanggal"]
        mataKuliah = requestBody["mataKuliah"]
        jenis = requestBody["jenis"]
        topik = requestBody["topik"]
        taskId = getNewId(TASK_FIRESTORE_COLLECTIONS)

        taskData = {
            "taskId": taskId,
            "tanggal": tanggal,
            "mataKuliah": mataKuliah,
            "jenis": jenis,
            "topik": topik
        }

        taskRef = db.collection(TASK_FIRESTORE_COLLECTIONS).document(taskId)
        taskRef.set(taskData)

        res = {
            "message": "post endpoint success",
            "data": {
                "task": taskData
            }
        }

    except KeyError:
        res = {
            "message": "Data incomplete on request body"
        }

    except:
        res = {
            "message": "Error occured on saving data"
        }

    finally:
        return jsonify(res)

# bot


@app.route("/bot", methods=["POST"])
def getChatbotReply():

    requestBody = request.get_json()
    message = requestBody["msg"]

    return jsonify(parser.parse(message))


PORT = 5000
if __name__ == "__main__":
    app.run(host="localhost", port=PORT, debug=True)
