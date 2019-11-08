import luigi
from luigi.contrib.postgres import CopyToTable 


class UpdateDB(CopyToTable):
    
    
    
    host = "localhost"
    database = "harshdb"
    user = "pandae"
    password = "db123"
    table = "pods"
    port = "5432"

    columns = [("run_id", "TEXT"),
            ("pod_url","TEXT"),
            ("pod_port","TEXT"),
            ("exp_id","TEXT")]

    def rows(self):
        with open("states/test.txt",'r') as fobj:
            for line in fobj:
                print(line)
                yield line.split(',')

    def requires(self):
        return [Runner()]


class Runner(luigi.Task):
    def requires(self):
        return []

    def run(self):
        arr = ["2345fr","101515", "5001", "1"]
        
        with self.output().open('w') as file:
            for a in arr:
                file.write("{},".format(a))

            
    def output(self):
        return luigi.LocalTarget('states/test.txt')


if __name__ == '__main__':
    luigi.run()
                        

