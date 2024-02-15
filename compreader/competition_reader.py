import camelot
import pandas as pd

from competition import Competition, Pilot, Task, Participant 
from ftv import FixedTotalValidityStrategy

PAGES = ["1", "1,2", "1,2,3", "all"][3]

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

        # skip 3x3 tables at the beginning:
        offset_table = 0
        if tables[0].shape == (3, 3):
            offset_table = 1               
        
        # read task table
        df_tasks = tables[offset_table].df
        #df_tasks.columns = df_tasks.iloc[0]
        df_tasks.columns = ['Task', 'Date', 'Distance', 'Validity', 'Type']
        df_tasks = df_tasks[1:]
        df_tasks.reset_index(inplace=True, drop=True)
        for idx in df_tasks.index:
            entry = df_tasks.at[idx, 'Validity']
            validity = float(entry[:-1])/100
            df_tasks.at[idx, 'Validity'] = validity
        n_tasks = len(df_tasks)

        # append additional tables:                
        results = [tables[i].df[1:] for i in range(offset_table+1, len(tables))]
        result = pd.concat(results)
        columns = list(tables[offset_table+1].df.iloc[0])
        # fix columns at Tasks:
        columns[3] = 'Sex'    
        task_names = [f'T_{i+1}' for i in range(n_tasks)]
        result.columns = columns[:7] + task_names + columns[7+n_tasks:]      
            
        result.reset_index(inplace=True, drop=True)

        # convert data types
        for idx in result.index:
            for i in range(n_tasks):
                try:
                    entry = result.at[idx, result.columns[7+i]]
                    pos = entry.index('/')                    
                    result.at[idx, result.columns[7+i]] = entry[pos+1:]
                except ValueError:
                    pass            
                
        for i in range(n_tasks):
            result.isetitem(7+i, pd.to_numeric(result.iloc[:, 7+i]))
        
        # create competition:
        competition = Competition(self.name)

        # create pilots:
        pilots = [competition.addPilot(row['Name']) for _,row in result.iterrows()]

        # create tasks:
        task_names = [result.iloc[:, 7+i].name for i in range(n_tasks)]
        #task_validities = [int(result.iloc[:, 7+i].max())/1000. for i in range(n_tasks)]        
        tasks = [competition.addTask(n, float(v)) for n, v in zip(task_names, df_tasks[['Validity']].values.flatten())]

        # register participants:
        for i,t in enumerate(tasks):
            for p,(_,row) in zip(pilots, result.iterrows()):
                t.addParticipation(p, row[t.name])
        
        return competition

    def quickthing(self):
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
    #path = "files/swiss-open-verbier/E1-Overall-V2.pdf"    
    #file = CompetitionFile("Swiss-Open-Verbier", path)
    #file.read()
    #competition = file.read_competition()
    #competition.addVirtualTask(1., 0)
    #competition.scoreAndFtvPrint(FixedTotalValidityStrategy(0.3))

    # Alpen Cup
    #path = "files/alpen-cup/AC_SportsClass_V1.pdf" # does not work of image format
    #path = "files/alpen-cup/AC_SportsClass_V4.pdf"
    #file = CompetitionFile("Alpen Cup", path)
    #ftv = 0.25

    # Swiss Cup
    #path = "files/swiss-cup/SC-SportsClass-V11.pdf"
    #path = "files/swiss-cup/SC-Overall-V11.pdf"
    #file = CompetitionFile("Swiss Cup", path)
    #ftv = 0.4 if "SportsClass" in path else 0.3    

    # OGO:
    path = "files/ogo/OGO_SportsClass_V5.pdf"
    file = CompetitionFile("OGO", path)
    ftv = 0.25

    # min max simulation
    competition = file.read_competition()
    competition.tasks = competition.tasks[:-1] # remove latest
    #competition.simulateMinMaxScores(1, 1.0, FixedTotalValidityStrategy(ftv)) # simulate outcomes
    #competition.addVirtualTask(1.0, 0)
    #competition.scoreAndFtvPrint(FixedTotalValidityStrategy(ftv))

    # run monte carlo simulation on task results:
    method = ['uniform', 'copy_task', 'uniform_max_pb', 'gaussian_pilot'][0]
    #method = ['uniform_max_pb', 'gaussian_pilot'][0]
    competition.monteCarloSimulation(50000, 1, 1.0, method, FixedTotalValidityStrategy(ftv))

    #file.read()
    #competition = file.read_competition()
    #competition.tasks = competition.tasks[:-1] # remove last one    
    #competition.scoreAndFtvPrint(FixedTotalValidityStrategy(ftv))

    #competition = file.read_competition()
    #competition.tasks = competition.tasks[:-1] # remove last one
    #competition.addVirtualTask(1.0, 0)    
    #competition.scoreAndFtvPrint(FixedTotalValidityStrategy(ftv))

    #competition = file.read_competition()
    #competition.tasks = competition.tasks[:-1] # remove last one
    #competition.addVirtualTask(1.0, 1000)    
    #competition.scoreAndFtvPrint(FixedTotalValidityStrategy(ftv))


    


