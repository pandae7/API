import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from model import Pod

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/add")
def add_runs():
    runid=request.args.get('runid')
    pod_url=request.args.get('pod_url')
    pod_port=request.args.get('pod_port')
    experiment_id=request.args.get('experiment_id')
    try:
        pod=Pod(
            runid=runid,
            pod_url=pod_url,
            pod_port=pod_port,
            experiment_id=experiment_id
        )
        db.session.add(pod)
        db.session.commit()
        return "pod_info added. for  runid={}".format(pod.runid)
    except Exception as e:
	    return(str(e))

@app.route("/getall")
def get_all():
    try:
        pods=Pod.query.all()
        return  jsonify([e.serialize() for e in pods])
    except Exception as e:
	    return(str(e))

@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        pod=Pod.query.filter_by(id=id_).first()
        return jsonify(pod.serialize())
    except Exception as e:
	    return(str(e))

if __name__ == '__main__':
    app.run(port=5001)