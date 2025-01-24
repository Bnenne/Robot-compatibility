from flask import Flask, jsonify, send_file
from functions.auto_compatibility import DataLabeling, Compare, nyan
from functions.tele_compatibility import StrategyLabeling
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
def get_auto_graph(event, team):
    title = "/auto/graph/" + event + "/" + team
    dl = DataLabeling(event, team)
    return send_file(dl.return_graph(title), mimetype='image/png'), 200

@app.route("/auto/data/<event>/<team>", methods=['GET'])
@cross_origin()
def get_auto_data(event, team):
    dl = DataLabeling(event, team)
    return jsonify(dl.return_data()), 200

@app.route("/auto/compare/graph/<event>/<team1>/<team2>", methods=['GET'])
@cross_origin()
def get_auto_compare_graph2(event, team1, team2):
    teams = [team1, team2]
    title = "/auto/compare/graph/"+event+"/"+team1+"/"+team2
    compare = Compare(event, teams)
    return send_file(compare.return_compare_graph(title), mimetype='image/png'), 200

@app.route("/auto/compare/graph/<event>/<team1>/<team2>/<team3>", methods=['GET'])
@cross_origin()
def get_auto_compare_graph3(event, team1, team2, team3):
    teams = [team1, team2, team3]
    title = "/auto/compare/graph/" + event + "/" + team1 + "/" + team2 +"/" + team3
    compare = Compare(event, teams)
    return send_file(compare.return_compare_graph(title), mimetype='image/png'), 200

@app.route("/auto/compare/data/<event>/<team1>/<team2>", methods=['GET'])
@cross_origin()
def get_auto_compare_data2(event, team1, team2):
    teams = [team1, team2]
    compare = Compare(event, teams)
    return jsonify(compare.return_compare_data()), 200

@app.route("/auto/compare/data/<event>/<team1>/<team2>/<team3>", methods=['GET'])
@cross_origin()
def get_auto_compare_data3(event, team1, team2, team3):
    teams = [team1, team2, team3]
    compare = Compare(event, teams)
    return jsonify(compare.return_compare_data()), 200

# @app.route("/tele/graph/<event>/<team>", methods=['GET'])
# @cross_origin()
# def get_tele_graph(event, team):
#     title = "/tele/graph/" + event + "/" + team
#     dl = DataLabeling(event, team)
#     return send_file(dl.return_graph(title), mimetype='image/png'), 200
#
# @app.route("/tele/data/<event>/<team>", methods=['GET'])
# @cross_origin()
# def get_tele_data(event, team):
#     sl = StrategyLabeling(event, team)
#     return jsonify(sl.tele_actions()), 200
#
# @app.route("/gimme", methods=['GET'])
# @cross_origin()
# def gimme_meow():
#     return send_file(nyan(), mimetype='image/png'), 200

if __name__ == "__main__": 
    app.run(debug=True)