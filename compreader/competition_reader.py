import camelot
import pandas as pd

from competition import Competition, Pilot, Task, Participant 

PAGES = "all" # "all"

class CompetitionFile:

    def __init__(self, name, path):
        self.name = name
        self.path = path
    
    def read(self):
        tables = camelot.read_pdf(self.path, pages=PAGES)

        for t in tables:
            print(t)
            print(t.parsing_report)
            df = t.df
            print(df)

    def read_competition(self):
        tables = camelot.read_pdf(self.path, pages=PAGES)       
        
        # read task table
        df_tasks = tables[1].df
        #df_tasks.columns = df_tasks.iloc[0]
        df_tasks.columns = ['Task', 'Date', 'Distance', 'Validity', 'Type']
        df_tasks = df_tasks[1:]
        df_tasks.reset_index(inplace=True, drop=True)
        n_tasks = len(df_tasks)

        # append additional tables:                
        results = [tables[i].df[1:] for i in range(2, len(tables))]
        result = pd.concat(results)
        result.columns = tables[2].df.iloc[0]
        result.reset_index(inplace=True, drop=True)

        # convert data types
        for i in range(n_tasks):
            result.isetitem(7+i, pd.to_numeric(result.iloc[:, 7+i]))
        
        # create competition:
        competition = Competition(self.name)

        # create pilots:
        pilots = [competition.addPilot(row['Name']) for _,row in result.iterrows()]

        # create tasks:
        task_names = [result.iloc[:, 7+i].name for i in range(n_tasks)]
        task_validities = [int(result.iloc[:, 7+i].max())/1000. for i in range(n_tasks)]
        tasks = [competition.addTask(n, v) for n, v in zip(task_names, task_validities)]

        # register participants:
        for i,t in enumerate(tasks):
            for p,(_,row) in zip(pilots, result.iterrows()):
                t.addParticipation(p, row[t.name])

        # Quick Change to Display Differences
        result.iloc[:, 7].info()
        result.iloc[:, 7] = pd.to_numeric(result.iloc[:, 7])
        result.iloc[:, 8] = pd.to_numeric(result.iloc[:, 8])
        result.iloc[:, 9] = pd.to_numeric(result.iloc[:, 9])
        result.iloc[:, 7].info()
        result.info()

        result.iloc[:, 7] = result.iloc[:, 7].max()-result.iloc[:, 7]
        result.iloc[:, 8] = result.iloc[:, 8].max()-result.iloc[:, 8]
        result.iloc[:, 9] = result.iloc[:, 9].max()-result.iloc[:, 9]
        result.iloc[:, 10] = result.iloc[:, 7]+result.iloc[:, 8]+result.iloc[:, 9]

        result['total_diff'] = result.iloc[:, 10] - result.iloc[:, 10].min()

        print(result)

class TaskFile:

    def __init__(self, path):
        self.path = path
    
    def read(self):
        tables = camelot.read_pdf(self.path, pages=PAGES)
        for t in tables:
            print(t)
            print(t.parsing_report)
            df = t.df
            print(df)



if __name__ == "__main__":
    
    # run tutorial
    # read verbier meta info
    #path = "files/swiss-open-verbier/E1-SportsClass-V1.pdf"
    #path = "files/swiss-open-verbier/E1-SportsClass-V2-2.pdf"
    path = "files/swiss-open-verbier/E1-Overall-V2.pdf"    
    file = CompetitionFile("Swiss-Open-Verbier", path)
    #file.read()
    file.read_competition()


    


