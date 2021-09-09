from akkaserverless.replicated.data import ReplicatedData
from akkaserverless.replicated.counter import ReplicatedCounter

class ReplicatedCounterMap(ReplicatedData):

    def __init__(self):
        self.counters = {}
        self.removed = {}
        self.cleared = False

    def get_or_create_counter(self, key):
        if key in self.counters:
            return self.counters[key]
        else:
            counter = ReplicatedCounter()
            self.counters[key] = counter
            return counter

    def get(self, key):
        entry = self.counters[key]
        return entry
        
    def increment(self, key, increment):
        self.get_or_create_counter(key).increment(increment)
    
    def decrement(self, key, decrement):
        self.get_or_create_counter(key).decrement(decrement)

    #override def hasDelta: Boolean = cleared || removed.nonEmpty || counters.values.exists(_.hasDelta)
    def has_delta(self):
        return self.cleared or bool(self.removed) or len(list(filter(lambda x: x.delta > 0, self.counters.values())))>0

    def reset_delta(self):
        for counter in self.counters.values():
            print('reset_delta')
            print(counter)
            counter.get_and_reset_delta()
        self.removed = {}

    def apply_delta(self, delta):
        if delta.counter == None:
            raise Exception(f'Cannot apply delta {delta} to ReplicatedCounter')

        self.current_value += delta.counter.change

'''
d = ReplicatedCounterMap()
#print(isinstance(d, ReplicatedData))
d.increment('d',2)
d.increment('d',3)
d.decrement('d',2)
print(d.get('d').current_value)
print(d.has_delta())
print(d.reset_delta())
print("dasdsadasdads")
print(d.has_delta())
'''