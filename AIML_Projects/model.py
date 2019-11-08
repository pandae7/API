from app import db

class Pod(db.Model):
    __tablename__ = 'pods'

    run_id = db.Column(db.String, primary_key=True)
    pod_url = db.Column(db.String())
    pod_port = db.Column(db.Integer())
    exp_id = db.Column(db.Integer())

    def __init__(self, run_id, pod_url, pod_port, exp_id):
        self.run_id = run_id
        self.pod_url = pod_url
        self.pod_port = pod_port
        self.exp_id = exp_id

    def __repr__(self):
        return '<run_id {}>'.format(self.run_id)
    
    def serialize(self):
        return {
            'run_id': self.run_id, 
            'pod_url': self.pod_url,
            'pod_port': self.pod_port,
            'exp_id':self.exp_id
        }