from sentiment_classifier import SentimentClassifier
from dbManager import dbManager
from flask import Flask, request, json, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
classifier = SentimentClassifier()
dbManager = dbManager()

#@app.route("/", methods=["GET", "POST"])
@cross_origin()

@app.route("/", methods=["GET"])
def index_page():	
    return render_template('index.html')


@app.route("/checkSubject", methods=["POST"])
def checkSubject():
    text = request.get_json(force=True)["text"]
    return json.jsonify({ "text": text, "class": classifier.predict_text(text),"confidence": classifier.predict_proba(text)})

@app.route("/getTodayComments", methods=["POST", "GET"])
def getTodayComments():
    try:
        data = dbManager.getTodayComments()
    except Exception as ex:
        print("A sql query executueting throws an error in getTodayComments")
        print(ex)
        return abort(500) 

    estimatedComments = [{ 
        "text": i[0], 
        "id": i[1], 
        "class": classifier.predict_text(i[0]),
        "confidence": classifier.predict_proba(i[0]),
        "text_len": len(i[0]) 
    } for i in data if i[0] is not None]

    return json.jsonify(estimatedComments)

@app.route("/getWorseThen", methods=["POST", "GET"])
def getWorseThen():
    estimatedComments = []
    skip = 0
    take = 200
    while len(estimatedComments) < 200:
        try:
            print("try getWorseThen")
            data = dbManager.getPageOfComments(skip, take)
        except Exception as ex:
            print("A sql query executueting throws an error in getWorseThen")
            print(ex)
            return abort(500) 

        temp = [{ 
            "text": i[0], 
            "id": i[1], 
            "class": classifier.predict_text(i[0]),
            "confidence": classifier.predict_proba(i[0]),
            "text_len": len(i[0]) 
        } for i in data if i[0] is not None 
        and 
        classifier.predict_proba(i[0]) > 0.75 
        and 
        classifier.predict_text(i[0]) == -1]

        estimatedComments += temp

        print(skip, take, len(estimatedComments))
        skip += take

    return json.jsonify(estimatedComments)

if __name__ == "__main__":
    '''
    app.run(port=5006, debug=True)
    '''
    from waitress import serve
    serve(app, port=5006)
