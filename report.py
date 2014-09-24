from statistics import mean,median
class Person:
    def __init__(self,line):
        hold = line.split(',')
        self.checked= None
        self.name,self.gender,self.year = hold[:3]
        self.goes =[self.decode(go) for go in hold[3:]]
        #print(self.goes)
        if len(self.goes) !=5:
            raise ValueError('naughty '+self.name)
        self.average = mean(self.goes)
        self.median = median(self.goes)
    def __str__(self):
        return self.name
    def __repr__(self):
        return '(Person:{} {})'.format(self.name,self.average)
    
    def decode(self,value):
        def check(v):
            res=v
            digits = [(ord(r)-ord('0'))*(count+1)
                        for count,r in enumerate(res) if r != '.']
            return chr(sum(digits)%10+ord('a'))
        if '0' <= value[-1] <= '9':
            # no check digit
            if self.checked == True:
                raise ValueError('check digit missing'+self.name)
            self.checked = False
            return float(value)
        if check(value[:-1]) != value[-1]:
            raise ValueError('Bad Check digit'+self.name)
        if self.checked == False:
            raise ValueError('missing check digit'+self.name)
        self.checked == True
        return float(value[:-1])


class Report:
    def __init__(self,line):
        hold = line.split(',')
        self.name=hold[0]
        self.age_start = int(hold[1])
        self.age_end = int(hold[2])
        self.gender = hold[3].lower()
        if self.gender not in ['male','female','all']:
            raise ValueError('Gender error '+self.gender)
    def check(self,person):
        if self.gender != 'all':
            if person.gender.lower() != self.gender:
                return False
        age = 2014 - int(person.year)
        return self.age_start <= age <= self.age_end
        
with open("playtext.txt") as f:
    people = [Person(line.strip()) for line in f if not line.startswith('#')]

with open("reports.txt") as f:
    reports = [Report(line.strip()) for line in f if not line.startswith('#')]
    
#print(people)

for report in reports:
    keeps = [person for person in people if report.check(person)]
    avgs = [person.average for person in keeps]
    medians = [person.median for person in keeps]
    try:
        average = sum(avgs)/len(avgs)
        median = sum(medians)/len(medians)
    except ZeroDivisionError:
        average = 0
        median =0
    #print(keeps)
    print('Group Name: {} Average Score: {:.3f} Median:{:.3f}'.format(report.name,average,median))
