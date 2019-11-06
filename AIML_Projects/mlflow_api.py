import os
from flask import Flask,jsonify,request
from flask_cors import CORS
import glob

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

for path in ['deployments', 'states']:
    if not os.path.exists(path):
        os.makedirs(path)


def check_db(run_id):
    # flag = True
    flag = False
    url = 'awslb.com'
    print('API with run id '+run_id+' exists.')
    return flag, url


@app.route('/deploy', methods=['POST'])
def deploy():
    # req = request.get_json(force=True)
    print("okay1")
    # run_id = req['run_id']
    run_id = request.form.get('run_id')
    exp_id = request.form.get('exp_id')
    flag, url = check_db(run_id)
    print("okay2")
    if flag:
        # output = {"url":url}
        output = url
    else:
        print("okay3")
        output = os.popen("PYTHONPATH='.' luigi --module mlflow_luigi Deploy --run-id "+
                      run_id+" --exp-id "+exp_id+" --local-scheduler").read()
    print(output)
    return output


@app.route('/delete', methods=['POST'])
def delete():
    req = request.get_json(force=True)
    run_id = req['run_id']
    files = glob.glob('states/'+run_id+'*') + glob.glob('deployments/'+run_id+'*')
    for file in files:
        os.remove(file)
    print('States Purged\n')
    return 'Done'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000)
