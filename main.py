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
    if request.method == "POST":
        text = request.json["text"]
        
        fitness = classifier.predict_text(text)
        print("Text - ", text, " result - " + fitness)

    return json.jsonify({ "text": text, "fitness": fitness, "message": message })

@app.route("/getTodayComments", methods=["POST", "GET"])
def getTodayComments():
    try:
        data = dbManager.getTodayComments()
    except Exception as ex:
        print("A sql query executueting throws an error in getTodayComments")
        print(ex)
        return abort(500) 
    
    print("getTodayComments")
    estimatedComments = [{ 
        "text": i[0], 
        "id": i[1], 
        "fitness": classifier.predict_text(i[0]) 
    } for i in data]

    return json.jsonify(estimatedComments)

if __name__ == "__main__":
    '''
    app.run(debug=True)
    '''
    from waitress import serve
    serve(app, port=5006, url_scheme='https')
