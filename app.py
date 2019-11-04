import os
import sys
from flask import Flask, request, jsonify, redirect
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
def check_runs():
    runid = input("enter runid: ") #takes Runid from user
    try:
        if Pod.query.filter_by(runid=runid).first():
            pod=Pod.query.filter_by(runid=runid).first()
            print(pod.pod_url, pod.pod_port, pod.experiment_id)
            #return jsonify(pod.serialize())  #if we want to get results on the web page
        else:
            add_runs(runid)
            pod=Pod.query.filter_by(runid=runid).first()
            print(pod.pod_url, pod.pod_port, pod.experiment_id)
            #return jsonify(pod.serialize()) #results on web page   
    except Exception as e:
	    return(str(e))

def add_runs(runid):
    #runid = input("enter runid: ") #takes Runid from user
    # pod_url=request.args.get('pod_url')
    # pod_port=request.args.get('pod_port')
    # experiment_id=request.args.get('experiment_id')


    """ enter code for deployment of POD with the help of helpers file """

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