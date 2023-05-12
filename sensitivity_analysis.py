from itertools import combinations
'''
configure weights and scores here at the start
no need to change anything else given:
max 4 scores/weights are changed at a time by either decreasing or increasing by 1
'''
criteria_dict = {'mass': 4,
            'cost' : 5,
            'reliability': 5,
            'expected dev effort': 2,
            'sustainability': 3,
            'operabiltiy': 4}


sw_scores =  {'mass': 2,
            'cost' : 2,
            'reliability': 1,
            'expected dev effort': 3,
            'sustainability': 1,
            'operabiltiy': 4}

rwgg_scores =  {'mass': 4,
            'cost' : 3,
            'reliability': 5,
            'expected dev effort': 5,
            'sustainability': 3,
            'operabiltiy': 3}

rwfg_scores = {'mass': 4,
            'cost' : 4,
            'reliability': 4,
            'expected dev effort': 3,
            'sustainability': 4,
            'operabiltiy': 4}

concept_dicts = {'sw':sw_scores, 'rwgg': rwgg_scores, 'rwfg' : rwfg_scores}


class criterion():
    def __init__(self, name, weight) -> None:
        self.name = name
        self.weight = weight
        self.archive_weight = weight
    
    def change_weight(self, sign) -> None:
        if sign < 0:
            self.weight -= 1
        elif sign > 0:
            self.weight += 1
        return None
    
    def reset(self):
        self.weight = self.archive_weight

criteria = [criterion(c, criteria_dict[c]) for c in criteria_dict]

class concept():
    def __init__(self, name, scores) -> None:
        self.name = name
        self.scores = scores
        self.archive = scores.copy()

    def change_score(self, criterion_):
        def change2(sign, criterion_ = criterion_, concept_ = self):
            if sign < 0:
                concept_.scores[criterion_] -= 1
            elif sign > 0:
                concept_.scores[criterion_] += 1

        return change2
    
    def print_scores(self):
        [print(self.scores[s]) for s in self.scores]
    
    def reset(self):
        self.scores = self.archive.copy()

    def score(self, criteria_ = criteria):
        return sum([self.scores[c.name] * c.weight for c in criteria_])

concepts = [concept(c, concept_dicts[c].copy()) for c in concept_dicts]

def reset_all(criteria_ = criteria, concepts = concepts):
    [c.reset() for c in concepts]
    [c.reset() for c in criteria_]


def assess_winner(concepts = concepts):
    scores = [c.score() for c in concepts]
    indices = [i for i, x in enumerate(scores) if x == max(scores)]
    if len(indices) > 1:
        return None
    else:
        return concepts[indices[0]].name
    

# the lists conctain functions that can be called with the signs later and result
master_list = [c.change_weight for c in criteria]

lst2 = [[con.change_score(c.name) for c in criteria] for con in concepts]

for lst in lst2:
    master_list += lst

wins = dict()
for con in concepts:
    wins[con.name] = 0

# [print(con.score()) for con in concepts]
# print(assess_winner())

sign_set = (0, 1,-1)
k = 0
for sign1 in sign_set:
    for sign2 in sign_set:
        for sign3 in sign_set:
            for sign4 in sign_set:
                k += 1
                signs = (sign1, sign2, sign3, sign4)
                for combo in combinations(master_list, 4):
                    for k in range(4):
                        combo[k](signs[k])
                    try:
                        wins[assess_winner()] += 1
                    except:
                        pass      
                    # print(wins)
                    # print('start')
                    # [print(con.score()) for con in concepts]         
                    reset_all()
                    # [print(con.score()) for con in concepts]
                    # print('end')
                    k += 1
print('results')
[print(f'{win} -- {wins[win]}') for win in wins]
