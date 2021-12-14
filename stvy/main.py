import random, time, numpy as np
from matplotlib import pyplot as plt

# Stvy Class
class Stvy:
    def __init__(self):
        file = open('note.txt', 'r')
        self.note = {}
        self.len = 0
        for e in file.readlines():
            temp = e.split(':')
            k, v = temp[0], temp[1]
            k = " ".join([x[0].upper() + x[1:] for x in k.split()])
            if v[-1] == '\n':
                v = v[:-1]
            self.note[k] = v[1:]
            self.len += 1
        file.close()
        self.record = 0
        file = open('point.txt', 'r')
        point_l = file.read().split()
        self.num_of_correct = int(point_l[0])
        self.num_of_total = int(point_l[1])
        self.point = str(self.num_of_correct) + '/' + str(self.num_of_total)
        file.close()
        self.freq = []

        ''' freq reset code
        with open('freq.txt', 'w') as f:
            for i in range(self.len):
                f.write('50\n')
        '''

        with open('freq.txt', 'r') as f:
            for e in f.readlines():
                temp = e[:-1]
                self.freq.append(int(temp))

    def new_def(self):
        file = open('note.txt', 'a+')
        title = input('What is the name of the definition? ')
        if self.note.get(title) is not None:
            inp = input(title + ' is already defined in the dictionary, do you want to overwrite? (y/n)')
            if inp == 'y':
                content = input('What is ' + title + '? ')
                self.note[title] = content
                file.write(title + ': ' + content + '\n')
                file.close()
            else:
                print('keep the original definition which is: ' + self.note[title])
        else:
            content = input('What is ' + title + '? ')
            self.note[title] = content
            file.write(title + ': ' + content + '\n')
            file.close()
            self.len += 1
            with open('freq.txt', 'a') as f:
                f.write('50\n')
                self.freq.append(50)


    def load_dict(self):
        print('SAVED NOTE')
        print("___________________________________________________________________________________________________")
        d = sorted(self.note.keys(), key = lambda x: x[0])
        for k in d:
            print(k, end = ': ')
            print(self.note[k])
        print("___________________________________________________________________________________________________")

    def flash_card(self):
        random.seed(time.time() % self.len)
        ans = random.choices(list(self.note.keys()), self.freq)[0]
        ques = self.note[ans]
        print('> FLASH CARD:')
        print('DESCRIPTION: ' + ques)
        inp = input('What is this? ')
        self.num_of_total += 1
        if inp == ans:
            print('Correct! good job')
            with open('record.txt', 'a') as f:
                f.write('o | ' + ans + '\n')
            self.freq[list(self.note.keys()).index(ans)] -= 1
            with open('freq.txt', 'w') as f:
                for i in range(self.len):
                    f.write(str(self.freq[i]) + '\n')
            self.num_of_correct += 1
        else:
            print('Wrong... the answer is ' + ans)
            with open('record.txt', 'a') as f:
                f.write('x | ' + ans + '\n')
        with open('point.txt', 'w') as f:
            f.write(str(self.num_of_correct) + ' ' + str(self.num_of_total))
        print('Record up to Now: ' + str(self.num_of_correct) + '/' + str(self.num_of_total))
        print('Correctness: ' + str(100*round(self.num_of_correct/self.num_of_total, 4)) + '%')
        print('---------------------------------------------------------------')


    def show_graph(self):
        print("GRAPH OPTION STRATEGY: ")
        int_rate = float(input("1-year effective annual interest rate(%)?: "))
        profit_ = np.zeros(5000)
        total_p = 0
        while True:
            response = input('Do you want to add a call(c), put option(p), or index(i) / no(n)? ')
            if response == 'n':
                break
            elif response == 'c' or response == 'p':
                s_l = input('Is it short(s) or long(l) position? ')
                strike_price = float(input("What is the strike price of the call option? ($0 - $5000): $"))
                premium = float(input("What is the premium of the option? "))
                premium *= (1 + int_rate/100)
                if response == 'c':
                    if s_l == 's':
                        profit_ += (-np.maximum(0, np.arange(5000) - strike_price) + premium)
                        total_p -= premium
                    else:
                        profit_ += (np.maximum(0, np.arange(5000) - strike_price) - premium)
                        total_p += premium
                else:
                    if s_l == 's':
                        profit_ += (-np.maximum(0, - np.arange(5000) + strike_price) + premium)
                        total_p -= premium
                    else:
                        profit_ += (np.maximum(0, - np.arange(5000) + strike_price) - premium)
                        total_p += premium

        _ = plt.plot(profit_, color='black', label='Profit Diagram')
        _ = plt.plot(np.zeros(5000), color='orange', label='Break-Even-Line')
        _ = plt.plot(0, 0, alpha=0, label='Total Premium Paid: $ ' + str(round(total_p, 2)))
        plt.grid(True)
        plt.axis('equal')
        plt.title('Call Option Profit Diagram.')
        plt.xlabel('Index Price (time = 1)')
        plt.ylabel('Profit')
        plt.legend()
        plt.show()

# MAIN
while True:
    res = input('1) Add a definition\n2) Show the dictionary\n3) Try flash card\n4) Show payoff diagram\ne) Exit \n>> ')
    obj = Stvy()
    if res == 'e':
        break
    if res == '1':
        obj.new_def()
    elif res == '2':
        obj.load_dict()
    elif res == '3':
        obj.flash_card()
    elif res == '4':
        obj.show_graph()




