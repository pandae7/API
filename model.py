from app import db

class Pod(db.Model):
    __tablename__ = 'pods'

    runid = db.Column(db.Integer, primary_key=True)
    pod_url = db.Column(db.String())
    pod_port = db.Column(db.Integer())
    experiment_id = db.Column(db.Integer())

    def __init__(self, runid, pod_url, pod_port, experiment_id):
        self.runid = runid
        self.pod_url = pod_url
        self.pod_port = pod_port
        self.experiment_id = experiment_id

    def __repr__(self):
        return '<runid {}>'.format(self.runid)
    
    def serialize(self):
        return {
            'runid': self.runid, 
            'pod_url': self.pod_url,
            'pod_port': self.pod_port,
            'experiment_id':self.experiment_id
        }