import json
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from firebase import db


app = Flask(__name__)
CORS(app)


# Routes

# get all task
@app.route("/task", methods=["GET"])
def getAllTask():

    print("Get Request received")

    res = {
        "message": "get endpoint success"
    }

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
        taskId = uuid.uuid4()

        print(requestBody)

        res = {
            "message": "post endpoint success"
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


PORT = 5000
if __name__ == "__main__":
    app.run(host="localhost", port=PORT, debug=True)
