from compreader.ftv import SumStrategy, PerformanceSumStrategy, FixedTotalValidityStrategy

### Construct PWC Example
def construct_pwc_example():
    competition = Competition('PWCExample')
    p1 = competition.addPilot('Pilot 1')
    p2 = competition.addPilot('Pilot 2')
    p3 = competition.addPilot('Pilot 3')
    p4 = competition.addPilot('Pilot 4')
    p5 = competition.addPilot('Pilot 5')
    t1 = competition.addTask('Task 1', 0.98)
    t2 = competition.addTask('Task 2', 1.0)
    t3 = competition.addTask('Task 3', 0.75)
    t4 = competition.addTask('Task 4', 0.42)
    t5 = competition.addTask('Task 5', 1.0)
    t1.addParticipation(p1, 300)
    t1.addParticipation(p2, 900)
    t1.addParticipation(p3, 500)
    t1.addParticipation(p4, 800)
    t1.addParticipation(p5, 950)

    t2.addParticipation(p1, 305)
    t2.addParticipation(p2, 600)
    t2.addParticipation(p3, 500)
    t2.addParticipation(p4, 1000)
    t2.addParticipation(p5, 800)

    t3.addParticipation(p1, 750)
    t3.addParticipation(p2, 200)
    t3.addParticipation(p3, 500)
    t3.addParticipation(p4, 300)
    t3.addParticipation(p5, 600)

    t4.addParticipation(p1, 250)
    t4.addParticipation(p2, 100)
    t4.addParticipation(p3, 400)
    t4.addParticipation(p4, 350)
    t4.addParticipation(p5, 200)

    t5.addParticipation(p1, 1000)
    t5.addParticipation(p2, 400)
    t5.addParticipation(p3, 500)
    t5.addParticipation(p4, 700)
    t5.addParticipation(p5, 800)
    return competition

def construct_verbier_sport(dq3):
    competition = Competition('Verbier (Sport)')
    
    p1 = competition.addPilot('Romain')
    p2 = competition.addPilot('Andre')
    p3 = competition.addPilot('Gin')
    p4 = competition.addPilot('Benjamin')
    p5 = competition.addPilot('Chrisitian B')
    p6 = competition.addPilot('Chrisitian Z')
    
    t1 = competition.addTask('Task 1', 0.9986)
    t2 = competition.addTask('Task 2', 1.0)
    t3 = competition.addTask('Task 3', 0.9993*dq3)    

    t1.addParticipation(p1, 961)
    t1.addParticipation(p2, 991)
    t1.addParticipation(p3, 961)
    t1.addParticipation(p4, 974)
    t1.addParticipation(p5, 999)
    t1.addParticipation(p6, 971)

    t2.addParticipation(p1, 972)
    t2.addParticipation(p2, 993)
    t2.addParticipation(p3, 989)
    t2.addParticipation(p4, 989)
    t2.addParticipation(p5, 907)
    t2.addParticipation(p6, 994)

    t3.addParticipation(p1, 1000*dq3-999+999)
    t3.addParticipation(p2, 1000*dq3-999+943)
    t3.addParticipation(p3, 1000*dq3-999+973)
    t3.addParticipation(p4, 1000*dq3-999+954)
    t3.addParticipation(p5, 1000*dq3-999+955)
    t3.addParticipation(p6, 1000*dq3-999+875)
    
    return competition

def construct_sample(dq2):
    competition = Competition('Example')

    p1 = competition.addPilot('Pilot 1')
    p2 = competition.addPilot('Pilot 2')
    p3 = competition.addPilot('Pilot 3')
    #v1, v2, v3 = (0.5, dq2, 0.5)
    v1, v2, v3 = (1.0, dq2, 1.0)
    t1 = competition.addTask('Task 1', v1)
    t2 = competition.addTask('Task 2', v2)
    #t3 = competition.addTask('Task 3', v3)

    t1.addParticipation(p1, round(v1*1000))
    t1.addParticipation(p2, round(v1*1000-50))
    t1.addParticipation(p3, round(v1*1000-100))

    t2.addParticipation(p1, round(v2*1000))
    t2.addParticipation(p2, max(0, round(v2*1000-100)))
    t2.addParticipation(p3, max(0, round(v2*1000-50)))

    #t3.addParticipation(p1, round(v3*1000))
    #t3.addParticipation(p2, round(v3*1000-300))
    #t3.addParticipation(p3, round(v3*1000-300))

    return competition

def construct_sample_2(dq2):
    competition = Competition('Example')

    p1 = competition.addPilot('Pilot 1')
    p2 = competition.addPilot('Pilot 2')
    p3 = competition.addPilot('Pilot 3')    
    
    t1 = competition.addTask('Task 1', 1.0)
    t2 = competition.addTask('Task 2', 1.0)
    #t3 = competition.addTask('Task 3', 1.0)

    t1.addParticipation(p1, round(1000))
    t1.addParticipation(p2, round(1000-50))
    t1.addParticipation(p3, round(1000-100))

    t2.addParticipation(p1, round(dq2*1000))
    t2.addParticipation(p2, max(0, round((1000-100)*dq2)))
    t2.addParticipation(p3, max(0, round((1000-50)*dq2)))

    #t3.addParticipation(p1, round(1000))
    #t3.addParticipation(p2, round(1000-300))
    #t3.addParticipation(p3, round(1000-300))

    return competition

def plot_ftv_scores(competition):
    ftvs = np.linspace(0.0, 0.9, 100)
    print (ftvs)    
    pilots2scores = dict()
    for p in competition.pilots:
        pilots2scores[p] = []
    for ftv in ftvs:
        competition.applyScoring(FixedTotalValidityStrategy(ftv, False))
        for p in competition.pilots:
            pilots2scores[p].append(p.total_points)

    # plot pilots:
    for p in competition.pilots:
        plt.plot(ftvs, pilots2scores[p], label=p.name)
    plt.legend()    
    plt.show()

def compute_day_quality_change(day_quality, competition_constructor, ftv):   
    pilots2scores = dict()
    competition = competition_constructor(1.0)
    for p in competition.pilots:
        pilots2scores[p.name] = []
    for dq in day_quality:
        competition = competition_constructor(dq)
        competition.applyScoring(FixedTotalValidityStrategy(ftv, verbose=False, do_round=False))
        for p in competition.pilots:
            pilots2scores[p.name].append(p.total_points)
    return pilots2scores

def construct_difference_sample(days, t3_quality):
    competition = Competition('Difference Game')

    t1_quality = 1.0
    t2_quality = 0.8

    p1 = competition.addPilot('p1')
    p2 = competition.addPilot('p2')
    p3 = competition.addPilot('p3')

    # difference based participation:
    t1 = competition.addTask('t1', t1_quality)
    t1.addParticipation(p1, t1_quality*1000-0)
    t1.addParticipation(p2, t1_quality*1000-10)
    t1.addParticipation(p3, t1_quality*1000-50)    
    if days == 1:
        return competition
    
    # day two
    t2 = competition.addTask('t2', t2_quality)
    t2.addParticipation(p1, t2_quality*1000-0)
    t2.addParticipation(p2, t2_quality*1000-10)
    t2.addParticipation(p3, t2_quality*1000-50)
    if days == 2:
        return competition
    
    # day three
    t3 = competition.addTask('t3', t3_quality)
    t3.addParticipation(p1, t3_quality*1000-66)
    t3.addParticipation(p2, t3_quality*1000-0)
    t3.addParticipation(p3, t3_quality*1000-10)
    return competition

def plot_day_quality_change(competition_constructor, ftv):
    day_quality = np.linspace(0.1, 1.0, 1000)    
    pilots2scores = compute_day_quality_change(day_quality, competition_constructor, ftv)
    competition = competition_constructor(1.0)
    # plot pilots:
    for p in competition.pilots:
        plt.plot(day_quality, pilots2scores[p.name], label=p.name)
    plt.legend()    
    #plt.show()

# run naive sum strategy:
#competition = construct_verbier_sport(0.999)
#competition.scoreAndPrint(SumStrategy())
#competition.applyScoring(PerformanceSumStrategy())
#competition.scoreAndPrint(FixedTotalValidityStrategy(0.4))

#plot_day_quality_change(construct_verbier_sport, 0.4)

# Simulate day 1:
#competition = construct_difference_sample(1, 0.5)
#competition.scoreAndFtvPrint(FixedTotalValidityStrategy(0.3))

# Simulate day 2:
#competition = construct_difference_sample(2, 0.5)
#competition.scoreAndFtvPrint(FixedTotalValidityStrategy(0.3))

# Simulate day 3:
competition = construct_difference_sample(3, 0.5)
competition.scoreAndFtvPrint(FixedTotalValidityStrategy(0.3))

# Simulate day 3:
#competition = construct_difference_sample(3, 0.771)
#competition.scoreAndFtvPrint(FixedTotalValidityStrategy(0.3))

# Alternative day 3-1000er:
#competition = construct_difference_sample(3, 1.0)
#competition.scoreAndPrint(FixedTotalValidityStrategy(0.3))


#plot_ftv_scores(competition)
#plot_day_quality_change(construct_sample, 0.0)
#plot_day_quality_change(construct_sample_2, 0.0)
#plot_day_quality_change(construct_sample, 0.1)
#plot_day_quality_change(construct_sample, 0.2)
#plt.figure()
#plot_day_quality_change(construct_sample, 0.3)
#plt.figure()
#plot_day_quality_change(construct_sample_2, 0.3)
#plt.show()
#plot_day_quality_change(construct_sample, 0.4)
#plot_day_quality_change(construct_sample, 0.5)



