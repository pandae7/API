import yaml
from kubernetes import config, client
import luigi
import kubernetes.client
from datetime import datetime

config.load_kube_config()
configuration = kubernetes.client.Configuration()
print("okay4")

class CreateYAML(luigi.Task):
    run_id = luigi.Parameter()
    exp_id = luigi.Parameter()

    def run(self):
        with open('templates/deployment.yaml') as stream:
            docs = list(yaml.safe_load_all(stream))
        docs[0]['metadata']['name'] = self.run_id
        docs[0]['spec']['template']['app'] = self.run_id
        docs[0]['spec']['template']['metadata']['labels']['app'] = self.run_id
        docs[0]['spec']['selector']['matchLabels']['app'] = self.run_id
        docs[0]['spec']['template']['spec']['containers'][0]['args'] = ["-c", "mlflow models serve -m s3://mlflowtrackingserver/" +
                                                                        str(self.exp_id)+"/"+str(self.run_id) +
                                                                        "/artifacts/model --host 0.0.0.0 --port 5001"]
        docs[0]['spec']['template']['spec']['containers'][0]['name'] = self.run_id

        docs[1]['metadata']['name'] = "pod-" + str(self.run_id)
        docs[1]['metadata']['labels']['app'] = self.run_id
        docs[1]['spec']['selector']['app'] = self.run_id

        with self.output().open('w') as stream:
            yaml.dump_all(
                docs,
                stream,
                default_flow_style=False
            )

    def output(self):
        return luigi.LocalTarget('deployments/' + str(self.run_id) + '_dep.yaml')


class Deploy(luigi.Task):
    run_id = luigi.Parameter()
    exp_id = luigi.Parameter()

    def requires(self):
        return CreateYAML(self.run_id, self.exp_id)

    def run(self):
        with open('deployments/' + str(self.run_id) + '_dep.yaml') as stream:
            docs = list(yaml.safe_load_all(stream))

            k8s_apps_v1 = client.AppsV1Api(kubernetes.client.ApiClient(configuration))
            resp = k8s_apps_v1.create_namespaced_deployment(
                body=docs[0], namespace='default')
            print("okay5")
            k8s_apps_v2 = client.CoreV1Api(kubernetes.client.ApiClient(configuration))
            resp2 = k8s_apps_v2.create_namespaced_service(
                body=docs[1], namespace='default')
            print("okay6")
            # return resp
            

        print("Deployment created.")
        with self.output().open('w') as file:
            file.write(datetime.now().strftime('Deployment task completed on %H %M %d %m %Y\n'))

    def output(self):
        return luigi.LocalTarget('states/' + str(self.run_id) + '_dep.txt')


class UpdateDB(luigi.Task):
    run_id = luigi.Parameter()
    exp_id = luigi.Parameter()

    def requires(self):
        return Deploy(self.run_id, self.exp_id)

    def run(self):

        with self.output().open('w') as file:
            file.write(datetime.now().strftime('DB update task completed on %H %M %d %m %Y\n'))

    def output(self):
        return luigi.LocalTarget('states/' + str(self.run_id) + '_db.txt')

if __name__ == '__main__':
    luigi.run()

