from flask import Flask, jsonify, send_file
from functions.cluster_labeling import DataLabeling, Compare
from functions.scouting_api import return_scoutingapi
from flask_cors import cross_origin
  
app = Flask(__name__)

@app.route("/scoutingapi", methods=['GET'])
@cross_origin()
def get_scoutingapi():
    return jsonify(return_scoutingapi()), 200

@app.route("/graph/<event>/<team>", methods=['GET'])
@cross_origin()
def get_graph(event, team):
    title = "/graph/" + event + "/" + team
    dl = DataLabeling(event, team)
    return send_file(dl.return_graph(title), mimetype='image/png'), 200

@app.route("/data/<event>/<team>", methods=['GET'])
@cross_origin()
def get_data(event, team):
    dl = DataLabeling(event, team)
    return jsonify(dl.return_data()), 200

@app.route("/compare/graph/<event>/<team1>/<team2>", methods=['GET'])
@cross_origin()
def get_compare_graph2(event, team1, team2):
    teams = [team1, team2]
    title = "/compare/graph/"+event+"/"+team1+"/"+team2
    compare = Compare(event, teams)
    return send_file(compare.return_compare_graph(title), mimetype='image/png'), 200

@app.route("/compare/graph/<event>/<team1>/<team2>/<team3>", methods=['GET'])
@cross_origin()
def get_compare_graph3(event, team1, team2, team3):
    teams = [team1, team2, team3]
    title = "/compare/graph/" + event + "/" + team1 + "/" + team2 +"/" + team3
    compare = Compare(event, teams)
    return send_file(compare.return_compare_graph(title), mimetype='image/png'), 200
  
if __name__ == "__main__": 
    app.run(debug=True)