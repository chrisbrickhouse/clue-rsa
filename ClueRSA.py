import random
import matplotlib.pyplot as plt
from scipy import stats
from math import log as log
from numpy import mean as mean

class Player():
    def __init__(self):
        self.holding = set([])
        self.shown = set([])
        self.unknown = set([
                       'Y', 'P', 'G', 'B', 'R', 'W',
                       'k', 'c', 'v', 'r', 'l', 'w',
                       'Hl', 'Ln', 'Dn', 'Kt', 'Ba', 'Cn', 'Bi', 'Lb', 'St'
                       ])
        self.p_prob_dict = {
                            'Y':0.1667,
                            'P':0.1667,
                            'G':0.1667,
                            'B':0.1667,
                            'R':0.1667,
                            'W':0.1667
                            }
        self.w_prob_dict = {
                            'k':0.1667,
                            'c':0.1667,
                            'v':0.1667,
                            'r':0.1667,
                            'l':0.1667,
                            'w':0.1667
                            }
        self.r_prob_dict = {
                            'Hl':0.1111,
                            'Ln':0.1111,
                            'Dn':0.1111,
                            'Kt':0.1111,
                            'Ba':0.1111,
                            'Cn':0.1111,
                            'Bi':0.1111,
                            'Lb':0.1111,
                            'St':0.1111
                            }
        self.shown_by = {}
        self.prob_dicts = [self.p_prob_dict,self.w_prob_dict,self.r_prob_dict]

    def _receive_card(self,card):
        self.holding.add(card)
        self.unknown.discard(card)
        self._update_probs(card)

    def _update_probs(self,card,prob=0.0):
        if card.isupper():
            p = self.p_prob_dict[card]
            self.p_prob_dict[card] = prob
            s = sum([self.p_prob_dict[x] for x in self.p_prob_dict])
            for c in self.p_prob_dict:
                try:
                    self.p_prob_dict[c] /= s
                except:
                    self._reset_prior('p')
        elif card.islower():
            p = self.w_prob_dict[card]
            self.w_prob_dict[card] = prob
            s = sum([self.w_prob_dict[x] for x in self.w_prob_dict])
            for c in self.w_prob_dict:
                try:
                    self.w_prob_dict[c] /= s
                except:
                    self._reset_prior('w')
        else:
            p = self.r_prob_dict[card]
            self.r_prob_dict[card] = prob
            s = sum([self.r_prob_dict[x] for x in self.r_prob_dict])
            for c in self.r_prob_dict:
                try:
                    self.r_prob_dict[c] /= s
                except:
                    self._reset_prior('r')

    def _reset_prior(self,prob_dict):
        universe = self.unknown = set([
                       'Y', 'P', 'G', 'B', 'R', 'W',
                       'k', 'c', 'v', 'r', 'l', 'w',
                       'Hl', 'Ln', 'Dn', 'Kt', 'Ba', 'Cn', 'Bi', 'Lb', 'St'
                       ])
        impossible = self.holding | self.shown
        possible = universe - impossible
        possible = list(possible)
        if prob_dict == 'p':
            possible = [x for x in possible if x.isupper()]
            uniformPrior = 1.0 / len(possible)
            for i in self.p_prob_dict:
                if i in possible:
                    self.p_prob_dict[i] = uniformPrior
                else:
                    self.p_prob_dict[i] = 0.0
        elif prob_dict == 'w':
            possible = [x for x in possible if x.islower()]
            uniformPrior = 1.0 / len(possible)
            for i in self.w_prob_dict:
                if i in possible:
                    self.w_prob_dict[i] = uniformPrior
                else:
                    self.w_prob_dict[i] = 0.0
        elif prob_dict == 'r':
            possible = [x for x in possible if len(x) == 2]
            uniformPrior = 1.0 / len(possible)
            for i in self.r_prob_dict:
                if i in possible:
                    self.r_prob_dict[i] = uniformPrior
                else:
                    self.r_prob_dict[i] = 0.0
        print('Prior reset')

    def _get_p_dict(self,x):
        if x.isupper():
            return(self.p_prob_dict)
        elif x.islower():
            return(self.w_prob_dict)
        else:
            return(self.r_prob_dict)

    def see_card(self,card,player):
        self._update_probs(card)
        self.shown.add(card)
        if player not in self.shown_by:
            self.shown_by[player]=set()
        self.shown_by[player].add(card)
        self.unknown.discard(card)

    def guess(self):
        p = []
        for key in self.p_prob_dict:
            f = round(100 * self.p_prob_dict[key])
            p = p + [key]*int(f)
        w = []
        for key in self.w_prob_dict:
            f = round(100 * self.w_prob_dict[key])
            w = w + [key]*int(f)
        r = []
        for key in self.r_prob_dict:
            f = round(100 * self.r_prob_dict[key])
            r = r + [key]*int(f)
        a = random.sample(p,1)[0]
        b = random.sample(w,1)[0]
        c = random.sample(r,1)[0]
        x = self.p_prob_dict[a]
        y = self.w_prob_dict[b]
        z = self.r_prob_dict[c]
        joint_prob = x*y*z
        g = [a,b,c]
        return(set(g),joint_prob)

    def reason(self,guess):
        print(self.p_prob_dict)
        print(self.w_prob_dict)
        print(self.r_prob_dict)
        guess = list(guess)
        newprobs = {}
        for item in guess:
            prob_dict = self._get_p_dict(item)
            prior = prob_dict[item]
            not_prior = 1.0 - prior
            pos_test = 1.0
            neg_test = 1.0
            for other in [x for x in guess if x != item]:
                not_other = 1.0 - self._get_p_dict(other)[other]
                pos_test *= not_other
            neg_g_prior = prior * (1.0 - pos_test)
            numerator = neg_g_prior * prior
            neg_g_not_prior = not_prior * neg_test
            denominator = neg_g_not_prior * not_prior + numerator
            if denominator == 0:
                denominator = 0.00001
            new_prob = numerator / denominator
            newprobs[item]=new_prob
        for i in newprobs:
            self._update_probs(i,newprobs[i])

def set_up(p,w,r,players=[[],[],[]]):
    p,w,r,c=choose(p,w,r)
    to_dist = p+w+r
    random.shuffle(to_dist)
    distribute(to_dist,players)
    return(c)

def choose(p,w,r):
    random.shuffle(p)
    random.shuffle(w)
    random.shuffle(r)
    a = p.pop()
    b = w.pop()
    c = r.pop()
    conf = set([a,b,c])
    return(p,w,r,conf)

def distribute(cards,players):
    n = len(players)
    i = 0
    for card in cards:
        if i >= n:
            i = 0
        players[i]._receive_card(card)
        i+=1

def main(n=3,reason=True):
    guess_probs = []
    people = ['Y','P','G','B','R','W']
    weapons = ['k','c','v','r','l','w']
    rooms = ['Hl','Ln','Dn','Kt','Ba','Cn','Bi','Lb','St']
    common_ground = []
    players = []
    for _ in range(n):
        players.append(Player())

    confidential = set_up(people,weapons,rooms,players)

    solved = False
    round_ = 1
    ply = 0

    while solved != True:
        print('Round %s' % str(round_))
        i=0
        for i in range(n):
            ply +=1
            #print('Player %s' % str(i))
            #print(len(players[i].unknown))
            guess, j_prob = players[i].guess()
            guess_probs.append((round_,j_prob))
            loop_stop = 0
            while guess in common_ground and loop_stop < 10:
                #print('Was already guessed, trying again')
                #print(guess)
                #print(players[i].prob_dicts)
                break
                guess = players[i].guess()
                loop_stop+=1
            j = i
            shown = False
            for _ in range(n):
                j += 1
                if j >= n:
                    j = 0
                test = guess.intersection(players[j].holding)
                if bool(test):
                    players[i].see_card(random.sample(test,1)[0],j)
                    common_ground.append(guess)
                    shown = True
                    break
            if shown == True:
                for k in range(n):
                    if k == i or k == j:
                        continue
                    else:
                        if reason:
                            players[k].reason(guess)
                        else:
                            continue
            elif shown == False:
                if guess == confidential:
                    solved = True
                    print(players[i].prob_dicts)
                    break
                else:
                    print('Player accused wrong')
        round_ +=1
    print('Solved!')
    print(confidential)
    print(guess)
    return(round_,i,ply,guess_probs,reason)

rounds = []
winner = []
counts = []
ns = []
guess_probs = []
reasoning = []
for _ in range(10000):
    n = random.randint(2,6)
    reason = random.choice([True,False])
    dat = main(n,reason)
    rounds.append(dat[0])
    winner.append(dat[1])
    counts.append(dat[2])
    reasoning.append(dat[4])
    g_p = [x+(n,) for x in dat[3]]
    guess_probs = guess_probs+g_p
    ns.append(n)
#plt.hist(rounds)
#plt.show()
#plt.hist(winner)
#plt.show()
#plt.hist(ns)
#plt.show()
#plt.hist(counts)
#plt.ylabel('Frequency')
#plt.xlabel('Ply of solution')
#plt.show()
plt.figure(1)
x_dat = [x[0] for x in guess_probs]
y_dat = [log(x[1]) for x in guess_probs]
slope, intercept, r_value, p_value, std_err = stats.linregress(x_dat,y_dat)
print(0,slope,r_value**2)
for i in range(2,7):
    num = 150 + (i-1)
    plt.subplot(num)
    if i == 2:
        plt.ylabel('Log probability')
    plt.xlabel('Round')
    x_dat = [x[0] for x in guess_probs if x[2]==i]
    y_dat = [log(x[1]) for x in guess_probs if x[2]==i]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x_dat,y_dat)
    print(i,slope,r_value**2)
    plt.scatter(x_dat,y_dat)
    plt.plot([0,15],[intercept,slope*15+intercept])
    plt.xlim(0,15)
    plt.ylim(-6,0)
    plt.title('%s Players' % i)
plt.show()
print(mean(counts))
ply_v_reasoning = list(zip(counts,reasoning))
f,(tr,fr) = plt.subplots(2,1,sharex=True)
plt.xlabel("Ply of Solution")
f.text(0.04, 0.5, 'Frequency', va='center', rotation='vertical')
tr.hist([x[0] for x in ply_v_reasoning if x[1]])
tr.set_title("Bayesian")
fr.hist([x[0] for x in ply_v_reasoning if not x[1]])
fr.set_title("Non-Bayesian")
plt.show()
