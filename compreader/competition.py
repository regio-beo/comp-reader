import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from tqdm import tqdm

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

    def simulateMinMaxScores(self, n, day_quality, strategy):
        self.applyScoring(strategy) # compute current scores
        for p in self.pilots:
            p.current_score = p.total_points
        
        for _ in range(n):
            self.addVirtualTask(day_quality, 0)        
        self.applyScoring(strategy) # compute minimum scores
        for p in self.pilots:
            p.min_score = p.total_points
        # compute improvement performance:
        for p in self.pilots:
            p.min_improvement_performance = 1.0            
            for score in p.ftv_scores:                
                if p.min_improvement_performance == 1.0 and score.usage_ftv_int < 100:
                    p.min_improvement_performance = score.performance
            p.min_improvement_performance = int (p.min_improvement_performance * day_quality * 1000) # convert to day quality                   
        
        self.tasks = self.tasks[:-n] # remove min scoring task
        for _ in range(n):
            self.addVirtualTask(day_quality, day_quality*1000)
        self.applyScoring(strategy) # compute max scores
        for p in self.pilots:
            p.max_score = p.total_points        
        
        # compute positions:
        max_scores = np.array([p.max_score for p in self.pilots])
        for p in self.pilots:
            p.min_position = (max_scores > p.min_score).sum() # +1 not required as yourself are included in the better pilots
        # missing points to reach:
        
        min_scores = np.array(sorted([p.min_score for p in self.pilots], reverse=True))
        for p in self.pilots:
            p.max_position = (min_scores > p.max_score).sum()+1 # +1 as you are lower than yourself
        for p in self.pilots:
            p.max_position_difference = int(day_quality*1000 + min_scores[p.max_position-1] - p.max_score) # compute missing points to achieve max position

        self.printMinMaxScores()

        self.tasks = self.tasks[:-n] # remove max scoring task (cleanup)
    
    def monteCarloSimulation(self, n, n_tasks, day_quality, method, strategy, order_as_initial=True, limit_plot=50):

        # recreate current situation:
        self.applyScoring(strategy) # might be important
        if order_as_initial: # shows the ranking with the information available at the time
            self.pilots = sorted(self.pilots, key=lambda p: p.total_points, reverse=True)
        n_flown_task = len(self.tasks)
        
        # run simulation
        n_pilots = len(self.pilots)
        counter = np.zeros((n_pilots, n_pilots))
        for i in range(n_pilots):
            self.pilots[i].counter_id = i # helper to find counting row
        
        # compute mu and std of pilot performances:
        for p in self.pilots:
            performances = []
            for score in p.ftv_scores:
                if score.performance_int > 0:
                    performances.append(score.performance)
            if len(performances) > 0:
                p.performance_mu = np.mean(performances)
                p.performance_sigma = np.std(performances)
            else:
                # defaults?! average of population?
                p.performance_mu = 0.1
                p.performance_sigma = 0.01
            #print(f'{p.name:>20}: {p.performance_mu:.2f}, +-{p.performance_sigma:.2f}')

        # use result to capture winning condition
        winner_pilot_points = []
        winner_condition = lambda pos: pos == 0
        winner_name = 'Sommerfeld'
        competitor_names = ['Karpfinger', 'Brodbeck', 'Fankhauser']        
        competitor_pilot_points = dict()
        for name in competitor_names:
            competitor_pilot_points[name] = []

        prev_counter = None
        for i in tqdm(range(n)):
            for _ in range(n_tasks):
                t_monte = self.addTask('MonteCarlo', day_quality)
                for p in self.pilots:                   
                    # uniform points:
                    if method == 'uniform':
                        points = np.random.randint(0, int(day_quality*1000))
                    
                    # random selected (previous) performance:
                    if method == 'copy_task':
                        task_like = np.random.randint(0, n_flown_task)
                        max_points = int(p.ftv_scores[task_like].performance*day_quality*1000)
                        points = np.random.randint(0, max_points+1)

                    #pilots do not exceed their max performance:
                    if method == 'uniform_max_pb':
                        points = np.random.randint(0, int(p.ftv_scores[0].performance*day_quality*1000)+1)

                    # skill based mu sigma performance:
                    if method == 'gaussian_pilot':
                        performance = np.random.normal(loc=p.performance_mu, scale=p.performance_sigma)
                        performance = min(1.0, performance)
                        performance = max(0.0, performance)
                        points = int(performance*day_quality*1000)

                    t_monte.addParticipation(p, points)

            self.applyScoring(strategy)
            monte_pilots = sorted(self.pilots, key=lambda p: p.total_points, reverse=True)
            for pos,pilot in enumerate(monte_pilots):
                counter[pilot.counter_id, pos] += 1

                if winner_name in pilot.name and winner_condition(pos):                    
                    # collect points for each appended task (and sum them up):
                    winner_points = 0
                    for i in range(n_tasks):
                        winner_points += self.tasks[-(i+1)].participantByName(winner_name).points
                    winner_pilot_points.append(winner_points)
                    
                    for name in competitor_names:
                        competition_points = 0
                        for i in range(n_tasks):
                            competition_points += self.tasks[-(i+1)].participantByName(name).points
                        competitor_pilot_points[name].append(competition_points)


            self.tasks = self.tasks[:-n_tasks] # remove monte task

            if i % 100 == 0:        
                counter_normalized = counter.copy()/(i+1)         
                if prev_counter is not None:
                    change = np.mean((prev_counter-counter_normalized)**2)
                    #print('change:', change)
                    EARLY_STOP = True
                    if EARLY_STOP and change < 1e-7:
                        n = i # fix early stopping
                        break
                prev_counter = counter_normalized

            #    print(counter/(i+1))
        
        print('~~~ Final Simulation ~~~')
        #for p in self.pilots:
        #    mx = np.argmax(counter[p.counter_id]) + 1
        #    print(f'{p.name}: {counter[p.counter_id]}, Expected Rank: {mx}')
        
        # normalize per row:
        mxs = np.max(counter, 1)
        counter_normalized = (counter.T/mxs).T
        counter_probs = counter/n
        #print(counter_normalized)
        # as probabilities:
        #counter_normalized = counter/n

        limit_plot = min(n_pilots, limit_plot)

        names = [p.name for p in self.pilots][:limit_plot]

        mpl.rcParams['figure.dpi'] = 125

        # Beni vs Jakob Plot:
        fig, ax = plt.subplots()
        for name in competitor_names:

            # filter max values per line:
            max_values_x = np.array([0]*1000*n_tasks)
            for x,y in zip(competitor_pilot_points[name], winner_pilot_points):
                max_values_x[y-1] = max(max_values_x[y-1], x)
            ax.scatter(max_values_x[max_values_x>0], np.arange(1, 1001)[max_values_x>0], alpha=0.3, s=50, label=name, linewidth=0)

            #ax.scatter(competitor_pilot_points[name], winner_pilot_points, alpha=0.3, s=10, label=name, linewidth=0)        
        
        ax.set_xlim(0, 1000*n_tasks)
        ax.set_ylim(0, 1000*n_tasks)
        ax.set_xticks(np.linspace(0, 1000*n_tasks, 21))
        ax.set_yticks(np.linspace(0, 1000*n_tasks, 21))
        ax.set_xlabel(', '.join(competitor_names))
        ax.set_ylabel(winner_name)
        ax.set_aspect('equal')
        ax.legend()
        ax.set_title(f'{winner_name} 1st')
        plt.grid()

        # Monte Carlo Plot:
        fig, ax = plt.subplots()
        im = ax.imshow(counter_normalized[:limit_plot, :limit_plot])
        ax.plot([0, limit_plot-1], [0, limit_plot-1], linestyle='dashed', color='r', alpha=0.6)

        # set labels
        ax.set_xticks(np.arange(limit_plot), labels=np.arange(limit_plot)+1) # start rank at 1
        ax.set_yticks(np.arange(limit_plot), labels=names)

        # print normalized values:
        for i in range(limit_plot):
            for j in range(limit_plot):
                text = ax.text(j, i, f'{counter_probs[i, j]:.2f}', ha='center', va='center', color='w', size=6)

        ax.set_title(f'Monte Carlo Simulation of {n} different Task outcomes')
        #fig.tight_layout
        plt.show()        

        #print(counter/(i+1))

    
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
        for p in pilots[:5]:
            p.print_ftv_scores()
    
    def printMinMaxScores(self):
        print(f'Extrema Scores of {self.name}:')
        print('                     Name | current    | min              | max ')
        pilots = sorted(self.pilots, key=lambda p: p.current_score, reverse=True)
        for p in pilots:
            p.print_min_max_scores()
        


class Pilot:

    def __init__(self, name):
        # clean name
        name = name.replace("\n", " ")
        name = name.replace("\r", " ")
        name = name.replace("\t", " ")        

        self.name = name
        self.total_points = 0
        self.fixed_total_validity = 0
        self.ftv_scores = []

        # compute current/min/max scores
        self.current_score = 0 # the current scores
        self.min_score = 0 # if the next run is 0 points
        self.min_position = 0 # what if all other score max points?
        self.min_improvement_performance = 0 # what to achieve in order to improve min_score (relative to )
        self.max_score = 0 # what if next run is 1000 points
        self.max_position = 0 # what if all others score 0 points?
    
    def print(self):
        print(f'{self.name}: {self.total_points}')
    
    def print_with_diff(self, max_score):
        print(f'{self.name}: {self.total_points} ({max_score-self.total_points})')

    def print_ftv_scores(self):
        # first row: name | task: points/winner (performance) | ... | total points
        # second row:   ~ |
        first_row = [f'{self.name:>25}']
        first_row += [f'{s.task.name:>5}: {s.points:>4}/{s.winner_score:>4} ({s.performance_int:>3}%)' for s in self.ftv_scores]
        first_row += [f'{self.total_points:>5}']
        second_row = [f'{"":>25}']
        second_row += [f'{s.left_out:>15}  ({s.usage_ftv_int:>3}%)' for s in self.ftv_scores] # 23
        total_left_out = self.fixed_total_validity - self.total_points
        second_row += [f'{total_left_out:>5}']
        print('|'.join(first_row))
        print('|'.join(second_row))
        print('')

    def print_min_max_scores(self):
        # compute usage score to improve on minimum:

        print(f'{self.name:>25} | {self.current_score:>10} |' \
            + f'{self.min_score:>5} ({self.min_position:>3}) >{self.min_improvement_performance:>3} |'\
            + f'{self.max_score:>5} ({self.max_position:>3}) >{self.max_position_difference:>3}')


class Task:

    def __init__(self, name, quality):
        self.name = name
        self.quality = quality
        self.participants = []
    
    def addParticipation(self, pilot, points):
        self.participants.append(Participant(pilot, self, points))

    def winnerScore(self):
        return round(self.quality*1000)
    
    def participantByName(self, name):
        for participant in self.participants:
            if name in participant.pilot.name:
                return participant
        raise ValueError('Name not found!')

    def winnerScorebyParticipant(self):
        #return int(self.quality*1000)
        #if self.name == 'TV':
        #    return int(self.quality*1000) # special case
        #scores = [p.points for p in self.participants]
        #return max(scores)
        pass # do not use this function
    
class Participant:

    def __init__(self, pilot, task, points):
        self.pilot = pilot
        self.task = task
        self.points = points
        self.points_ftv = 0
        self.performance = 0.
        self.usage_ftv = 0.