import luigi

class UpdateDB(luigi.contrib.postgres.CopyToTable):
    host = "localhost"
    database = "mldb"
    user = "pandae"
    password = "9248868612"
    table = "pods"

    columns = [("runid", "ab34"),
               ("pod_url", "okay1")
               ("pod_port", 5001 )
               ("experiment_id", 1)]


    def requires(self):
        return []


class Runner(luigi.Task):
    def requires(self):
        return [UpdateDB()]

    def run(self):

        with self.output().open('w') as file:
            file.write('Deployment task completed\n')

    def output(self):
        return luigi.LocalTarget('states/test.txt')


if __name__ == '__main__':
    luigi.run()
                        

