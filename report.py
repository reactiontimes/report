from statistics import mean,median

def spread(results):
    if not results:
        return 0
    mean = sum(results)/len(results)
    spreads = [(result-mean)**2 for result in results]
    return (sum(spreads)/len(spreads))**(1/2)
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
        self.spread = spread(self.goes)
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

print('{:20} {:>10} {:>15} {:>15} {:>15} {:>15} {:>15}'.format('Group Name','People','Personal Spread','Average','Std dev of Avg','Median','Std dev of Median'))
for report in reports:
    keeps = [person for person in people if report.check(person)]
    avgs = [person.average for person in keeps]
    medians = [person.median for person in keeps]
    spreads = [person.spread for person in keeps]
    try:
        average = sum(avgs)/len(avgs)
        the_median = sum(medians)/len(medians)
        the_spread = sum(spreads)/len(spreads)
    except ZeroDivisionError:
        average = 0
        the_median =0
        the_spread = 0
    #print(keeps)
    print('{:20} {:10} {:15.3f} {:15.3f} {:15.3f} {:15.3f} {:15.3f}'.format(report.name,len(keeps),the_spread,average,spread(avgs),the_median,spread(medians)))
