
class Competition:

    def __init__(self, name):
        self.name = name
        self.tasks = []
        self.pilots = []

    def addTask(self, name, quality):
        t = Task(name, quality)
        self.tasks.append(t)
        return t
    
    def addPilot(self, name):
        p = Pilot(name)
        self.pilots.append(p)
        return p
    
    def scoreAndPrint(self, strategy):
        self.applyScoring(strategy)
        self.printScores()

    def applyScoring(self, strategy):
        for p in self.pilots:
            p.total_points = 0
        strategy.apply(self)        

    def printScores(self):
        print(f'Final scores of {self.name}')
        pilots = sorted(self.pilots, key=lambda p: p.total_points, reverse=True)
        for p in pilots:
            p.print()


class Pilot:

    def __init__(self, name):
        self.name = name
        self.total_points = 0
    
    def print(self):
        print(f'{self.name}: {self.total_points}')

class Task:

    def __init__(self, name, quality):
        self.name = name
        self.quality = quality
        self.participants = []
    
    def addParticipation(self, pilot, points):
        self.participants.append(Participant(pilot, points))

    def winnerScore(self):
        scores = [p.points for p in self.participants]
        return max(scores)
    
class Participant:

    def __init__(self, pilot, points):
        self.pilot = pilot
        self.points = points
        self.points_ftv = 0
        self.performance = 0.