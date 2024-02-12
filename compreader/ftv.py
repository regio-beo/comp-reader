import matplotlib.pyplot as plt
import numpy as np

from compreader.competition import Competition, Pilot, Task, Participant 


# Script to play with FTV Scores


### Scoring Strategies:
class SumStrategy:
    
    def apply(self, competition):
        for task in competition.tasks:
            for participant in task.participants:
                participant.pilot.total_points += participant.points

class PerformanceSumStrategy:

    def apply(self, competition):
        for task in competition.tasks:
            winner_score = task.winnerScore()
            for participant in task.participants:
                participant.performance = participant.points / winner_score
                participant.pilot.total_points += participant.performance

class FixedTotalValidityStrategy:

    def __init__(self, ftv, verbose=False, do_round=True):
        self.ftv = ftv
        self.verbose = verbose
        self.do_round=do_round
    
    def print(self, *args):
        if self.verbose:
            print('DEBUG:', *args)
    
    def apply(self, competition):
        # compute fixed total validity:
        total_score = sum([t.winnerScore() for t in competition.tasks])
        if self.do_round:
            fixed_total_validity = round(total_score * (1-self.ftv))
        else:
            fixed_total_validity = total_score * (1-self.ftv)
        self.print('use fixed total validity:', fixed_total_validity, 'of total score', total_score)

        # compute performances:
        pilots2scores = dict()
        for pilot in competition.pilots:
            pilot.fixed_total_validity = fixed_total_validity # helping attribute
            pilots2scores[pilot] = []
        for task in competition.tasks:
            winner_score = task.winnerScore()
            for participant in task.participants:                
                participant.points = int(participant.points)
                participant.performance = participant.points / winner_score
                participant.performance_int = int(participant.performance*100)
                participant.winner_score = int(winner_score) # helping attribute
                participant.left_out = int(winner_score - participant.points)
                pilots2scores[participant.pilot].append(participant)
        #print('pilots2scores', pilots2scores)

        # compute FTVs        
        for pilot in competition.pilots:
            ftv_left = fixed_total_validity
            scores = pilots2scores[pilot]
            scores = sorted(scores, key=lambda participant: participant.performance, reverse=True)
            self.print(f'{pilot.name}:')
            pilot.ftv_scores = scores # reference them
            for s in scores:
                if ftv_left == 0:
                    # no ftv to consider
                    s.usage_ftv_int = 0
                    continue
                if s.winner_score <= ftv_left:
                    # full ftv to consider
                    pilot.total_points += s.points
                    ftv_left -= s.winner_score
                    s.usage_ftv_int = 100
                    self.print(f'add to score: (ftv-left: {ftv_left}, task-score: {s.points}, current-score:{pilot.total_points})')
                else:
                    # partial ftv to use:
                    if self.do_round:
                        partial_score = round((ftv_left/s.winner_score)*s.points)
                    else:
                        partial_score = (ftv_left/s.winner_score)*s.points
                    s.usage_ftv_int = int(ftv_left/s.winner_score*100)
                    pilot.total_points += partial_score                    
                    self.print(f'add partial ({ftv_left}/{s.winner_score})={partial_score}, current-score:{pilot.total_points})')
                    ftv_left -= ftv_left # sounds like 0. haha
                #print(s.performance, s.points, s.winner_score)




