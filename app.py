from flask import Flask, jsonify, send_file
from functions.auto_compatibility import DataLabeling, Compare
from functions.scouting_api import return_scoutingapi, return_tba
from flask_cors import cross_origin
  
app = Flask(__name__)

@app.route("/scoutingapi", methods=['GET'])
@cross_origin()
def get_scoutingapi():
    return jsonify(return_scoutingapi()), 200

@app.route("/tba", methods=['GET'])
@cross_origin()
def get_tba():
    return jsonify(return_tba()), 200

@app.route("/auto/graph/<event>/<team>", methods=['GET'])
@cross_origin()
def get_graph(event, team):
    title = "/graph/" + event + "/" + team
    dl = DataLabeling(event, team)
    return send_file(dl.return_graph(title), mimetype='image/png'), 200

@app.route("/auto/data/<event>/<team>", methods=['GET'])
@cross_origin()
def get_data(event, team):
    dl = DataLabeling(event, team)
    return jsonify(dl.return_data()), 200

@app.route("/auto/compare/graph/<event>/<team1>/<team2>", methods=['GET'])
@cross_origin()
def get_compare_graph2(event, team1, team2):
    teams = [team1, team2]
    title = "/auto/compare/graph/"+event+"/"+team1+"/"+team2
    compare = Compare(event, teams)
    return send_file(compare.return_compare_graph(title), mimetype='image/png'), 200

@app.route("/auto/compare/graph/<event>/<team1>/<team2>/<team3>", methods=['GET'])
@cross_origin()
def get_compare_graph3(event, team1, team2, team3):
    teams = [team1, team2, team3]
    title = "/auto/compare/graph/" + event + "/" + team1 + "/" + team2 +"/" + team3
    compare = Compare(event, teams)
    return send_file(compare.return_compare_graph(title), mimetype='image/png'), 200

@app.route("/auto/compare/data/<event>/<team1>/<team2>", methods=['GET'])
@cross_origin()
def get_compare_data2(event, team1, team2):
    teams = [team1, team2]
    compare = Compare(event, teams)
    return jsonify(compare.return_compare_data()), 200

@app.route("/auto/compare/data/<event>/<team1>/<team2>/<team3>", methods=['GET'])
@cross_origin()
def get_compare_data3(event, team1, team2, team3):
    teams = [team1, team2, team3]
    compare = Compare(event, teams)
    return jsonify(compare.return_compare_data()), 200
  
if __name__ == "__main__": 
    app.run(debug=True)