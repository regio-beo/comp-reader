import camelot

PAGES = "1" # "all"

class CompetitionFile:

    def __init__(self, path):
        self.path = path

    def read(self):
        tables = camelot.read_pdf(self.path, pages=PAGES)
        for t in tables:
            print(t)
            print(t.parsing_report)
            df = t.df
            print(df)

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
    file = CompetitionFile(path)
    file.read()


    

