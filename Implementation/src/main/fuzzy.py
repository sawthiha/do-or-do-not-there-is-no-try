import numpy as np

class FuzzyTermSet:
    def __init__(self, terms, mfs):
        self.__set = dict()
        for term, mf in zip(terms, mfs):
            self.__set[term] = mf
            
    def __call__(self, value):
        return FuzzySet(self, value)
    
    def __iter__(self):
        return zip(self.__set.keys(), self.__set.values())
    
    def __getitem__(self, key):
        return FuzzyRule(key, self)

### Standard Set
# It takes terms and Membership functions
class FuzzySet:
    def __init__(self, termset : FuzzyTermSet, value = None):
        self.__set = dict()
        self.__termset = termset
        # FuzzyTermSet.__iter__
        for term, mf in termset:
            self.__set[term] = 0.0 if value == None else mf[value]
    
    def termset(self):
        return self.__termset
    
    def __getitem__(self, key):
        return self.__set[key]
    
    def __setitem__(self, key, value):
        if key not in self.__set.keys():
            raise ValueError('\'' + key + '\' is not a valid key!')
        self.__set[key] = value
    
    def __iter__(self):
        return (self.__set.keys(), self.__set.values())
    
    def iterset(self):
        return self.__set.__iter__()
    
    def __repr__(self):
        return self.__set.__repr__()
    
class FuzzyRule:
    def __init__(self, term : str, termset : FuzzyTermSet):
        self.__termsets = list()
        self.__terms = list()
        self.__operations = list()
        self.__terms.append(term)
        self.__termsets.append(termset)
    
    def __and__(self, other):
        self.__operations.append(self.f_and)
        self.concat(other)
        return self
    
    def __or__(self, other):
        self.__operations.append(self.f_or)
        self.concat(other)
        return self
    
    def terms(self):
        return self.__terms
    
    def termsets(self):
        return self.__termsets
    
    def conseq(self):
        return self.__conseq
    
    def conseqset(self):
        return self.__conseqset
    
    def opertions(self):
        return self.__operations
    
    def concat(self, other):
        self.__terms.extend(other.terms())
        self.__termsets.extend(other.termsets())
        
    def f_and(self, set1, set2, term1, term2):
        return set1[term1] & set2[term2]
    
    def f_or(self, set1, set2, term1, term2):
        return set1[term1] | set2[term2]
        
    def then(self, conseq):
        termsets = conseq.termsets()
        if len(termsets) != 1:
            raise ValueError('Consequence must be a single termset')
            
        self.__conseq = conseq.terms()[0]
        self.__conseqset = termsets[0]
        
        return self
    
    def __call__(self, fsets, result):
        if result.termset() != self.__conseqset:
            raise ValueError('Invalid Consequence!')
        n = len(self.__terms)
        value = [0.0] * n
        idx = 0
        for tm, ts in zip(self.__terms, self.__termsets):
            for fs in fsets:
                if fs.termset() == ts:
                    value[idx] = fs[tm]
            idx += 1
        value = min(value)
        result[self.__conseq] = value if value > result[self.__conseq] else result[self.__conseq]
    
class FuzzyRuleBase:
    def __init__(self, rules = None):
        self.__rules = [] if rules == None else rules
        
    def add(self, rule : FuzzyRule):
        self.__rules.append(rule)
        
    def __call__(self, antes, cons : FuzzySet):
        for rule in self.__rules:
            rule(antes, cons)
    
class FuzzyController:
    def __init__(self, mfs):
        self.__universe = mfs[0]
        self.__w_act = 0.4
        self.__w_int = 0.1
        self.__w_ext = 0.5
        
        i_low = mfs[2]['low']
        i_avg = mfs[2]['avg']
        i_exc = mfs[2]['exc']
        
        a_low = mfs[1]['low']
        a_avg = mfs[1]['avg']
        a_exc = mfs[1]['exc']
        
        e_low = mfs[3]['low']
        e_avg = mfs[3]['avg']
        e_exc = mfs[3]['exc']
        
        r_low = mfs[4]['low']
        r_avg = mfs[4]['avg']
        r_exc = mfs[4]['exc']
        
        self.__ts_activity = FuzzyTermSet(('low', 'avg', 'exc'), (a_low, a_avg, a_exc))
        self.__ts_internal = FuzzyTermSet(('low', 'avg', 'exc'), (i_low, i_avg, i_exc))
        self.__ts_external = FuzzyTermSet(('low', 'avg', 'exc'), (e_low, e_avg, e_exc))
        self.__ts_rating = FuzzyTermSet(('low', 'avg', 'exc'), (e_low, e_avg, e_exc))
        
        self.__rb = FuzzyRuleBase(rules = self.gen_rules())
        
    def gen_rules(self):
        terms = ['low', 'avg', 'exc']
        for x in [0, 1, 2]:
            for y in [0, 1, 2]:
                for z in [0, 1, 2]:
                    result = round((x * self.__w_act) + (y * self.__w_int) + (z * self.__w_ext))
                    yield (self.__ts_activity[terms[x]] & self.__ts_internal[terms[y]] & self.__ts_external[terms[z]]).then(self.__ts_rating[terms[result]])
        
    def __call__(self, activities, internal, external):
        actv = self.__ts_activity(activities)
        intr = self.__ts_internal(internal)
        extr = self.__ts_external(external)
        ratr = FuzzySet(self.__ts_rating)
        self.__rb((actv, intr, extr), ratr)
        rating = (activities * self.__w_act) + (internal * self.__w_int) + (external * self.__w_ext)
        return (max(ratr.iterset(), key= lambda key: ratr[key]), rating)

with open('mfs.pickle', 'rb') as f:
    mfs = pk.load(f)
FUZZY = FuzzyController(mfs)