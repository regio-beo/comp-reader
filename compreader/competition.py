
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
    
    def addVirtualTask(self, quality, points):
        tv = self.addTask('TV', quality)
        for p in self.pilots:
            tv.addParticipation(p, points)
    
    def scoreAndPrint(self, strategy):
        self.applyScoring(strategy)
        self.printScores()
    
    def scoreAndFtvPrint(self, strategy):
        self.applyScoring(strategy)
        self.printFtvScores()

    def applyScoring(self, strategy):
        for p in self.pilots:
            p.total_points = 0
        strategy.apply(self)        

    def printScores(self):
        print(f'Final scores of {self.name}')
        pilots = sorted(self.pilots, key=lambda p: p.total_points, reverse=True)
        max_score = pilots[0].total_points
        for p in pilots:
            p.print_with_diff(max_score)
            #p.print()
    
    def printFtvScores(self):
        print(f'FTV scores of {self.name}')
        pilots = sorted(self.pilots, key=lambda p: p.total_points, reverse=True)
        for p in pilots:
            p.print_ftv_scores()


class Pilot:

    def __init__(self, name):
        self.name = name
        self.total_points = 0
        self.fixed_total_validity = 0
        self.ftv_scores = []
    
    def print(self):
        print(f'{self.name}: {self.total_points}')
    
    def print_with_diff(self, max_score):
        print(f'{self.name}: {self.total_points} ({max_score-self.total_points})')

    def print_ftv_scores(self):
        # first row: name | task: points/winner (performance) | ... | total points
        # second row:   ~ |
        first_row = [f'{self.name:>20}']
        first_row += [f'{s.task.name:>5}: {s.points:>4}/{s.winner_score:>4} ({s.performance_int:>3}%)' for s in self.ftv_scores]
        first_row += [f'{self.total_points:>5}']
        second_row = [f'{"":>20}']
        second_row += [f'{s.left_out:>15}  ({s.usage_ftv_int:>3}%)' for s in self.ftv_scores] # 23
        total_left_out = self.fixed_total_validity - self.total_points
        second_row += [f'{total_left_out:>5}']
        print('|'.join(first_row))
        print('|'.join(second_row))
        print('')


class Task:

    def __init__(self, name, quality):
        self.name = name
        self.quality = quality
        self.participants = []
    
    def addParticipation(self, pilot, points):
        self.participants.append(Participant(pilot, self, points))

    def winnerScore(self):
        if self.name == 'TV':
            return (self.quality*1000) # special case
        scores = [p.points for p in self.participants]
        return max(scores)
    
class Participant:

    def __init__(self, pilot, task, points):
        self.pilot = pilot
        self.task = task
        self.points = points
        self.points_ftv = 0
        self.performance = 0.
        self.usage_ftv = 0.