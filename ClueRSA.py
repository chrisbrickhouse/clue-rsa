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
        
    def _update_probs(self,card):
        if card.isupper():
            p = self.p_prob_dict[card]
            self.p_prob_dict[card] = 0.0
            n = [x for x in self.p_prob_dict if self.p_prob_dict[x] > 0.0]
            diff = p/len(n)
            for c in n:
                self.p_prob_dict[c] += diff
        elif card.islower():
            p = self.w_prob_dict[card]
            self.w_prob_dict[card] = 0.0
            n = [x for x in self.w_prob_dict if self.w_prob_dict[x] > 0.0]
            diff = p/len(n)
            for c in n:
                self.w_prob_dict[c] += diff
        else:
            p = self.r_prob_dict[card]
            self.r_prob_dict[card] = 0.0
            n = [x for x in self.r_prob_dict if self.r_prob_dict[x] > 0.0]
            diff = p/len(n)
            for c in n:
                self.r_prob_dict[c] += diff
            
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
        
    def reason(self,guess,player,factor=.333,t=0.0):
        possible_cards = guess.difference(self.holding)
        if len(possible_cards) == 1:
            card = possible_cards.pop()
            p_dict = self._get_p_dict(card)
            p = p_dict[card]
            p_dict[card] = 0.0
            n = [x for x in p_dict if p_dict[x] > t]
            diff = p/len(n)
            for i in n:
                if i == card:
                    continue
                p_dict[i] += diff
            return()
        elif player not in self.shown_by:
            return()
        universe = self.shown.union(self.unknown)
        known_not_held_by_player = self.shown - self.shown_by[player]
        universe = universe - known_not_held_by_player
        likely_shown = guess & self.shown_by[player]
        unlikely_shown = universe - likely_shown
        pos = likely_shown | unlikely_shown
        print(len(likely_shown),len(unlikely_shown))
        num = len(likely_shown)+len(unlikely_shown)
        for c in pos:
            if c in likely_shown:
                dist_prob = float(len(likely_shown)) / len(universe)
            else:
                dist_prob = float(len(unlikely_shown)) / len(universe)
            pd = self._get_p_dict(c)
            old = pd[c]
            pd[c] = pd[c]*dist_prob
            print(old-pd[c])
        if len(likely_shown) == 1 and len(unlikely_shown) == 0:
            print('Watson!......................................')
        '''
        for part in possible_cards:
            if part.isupper():
                n = [x for x in self.p_prob_dict if self.p_prob_dict[x] > t]
                if len(n) == 1 or self.p_prob_dict[part] == 0.0:
                    continue
                p = self.p_prob_dict[part]
                q = 1.0-p
                n_p = p*factor
                n_q = 1.0 - n_p
                not_part_p = n_q / len(n)
                for i in n:
                    if i == part:
                        self.p_prob_dict[part] = n_p
                    else:
                        self.p_prob_dict[i] = not_part_p
            elif part.islower():
                n = [x for x in self.w_prob_dict if self.w_prob_dict[x] > t]
                if len(n) == 1 or self.w_prob_dict[part] == 0.0:
                    continue
                p = self.w_prob_dict[part]
                q = 1.0-p
                n_p = p*factor
                n_q = 1.0 - n_p
                not_part_p = n_q / len(n)
                for i in n:
                    if i == part:
                        self.w_prob_dict[part] = n_p
                    else:
                        self.w_prob_dict[i] = not_part_p
            else:
                n = [x for x in self.r_prob_dict if self.r_prob_dict[x] > t]
                if len(n) == 1 or self.r_prob_dict[part] == 0.0:
                    continue
                p = self.r_prob_dict[part]
                q = 1.0-p
                n_p = p*factor
                n_q = 1.0 - n_p
                not_part_p = n_q / len(n)
                for i in n:
                    if i == part:
                        self.r_prob_dict[part] = n_p
                    else:
                        self.r_prob_dict[i] = not_part_p
            '''

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

def main(n=3):
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
    count = 0

    while solved != True:
        print('Round %s' % str(round_))
        i=0
        for i in range(n):
            count +=1
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
                        players[k].reason(guess,j)
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
    return(round_,i,count,guess_probs)
    
rounds = []
winner = []
counts = []
ns = []
guess_probs = []
for _ in range(1000):
    n = random.randint(2,6)
    dat = main(n)
    rounds.append(dat[0])
    winner.append(dat[1])
    counts.append(dat[2])
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
