from flask import Flask, jsonify, send_file
from functions.cluster_labeling import DataLabeling
  
app = Flask(__name__) 

@app.route("/graph/<event>/<team>", methods=['GET']) 
def get_graph(event, team):
    dl = DataLabeling(event, team)
    return send_file(dl.return_graph(), mimetype='image/png'), 200

@app.route("/data/<event>/<team>", methods=['GET'])
def get_data(event, team):
    dl = DataLabeling(event, team)
    return jsonify(dl.return_data()), 200
  
if __name__ == "__main__": 
    app.run(debug=True)