from akkaserverless.replicated.data import ReplicatedData
from akkaserverless.akkaserverless.component.replicatedentity.replicated_entity_pb2 import (
    ReplicatedCounterDelta,
    ReplicatedEntityDelta
)


class ReplicatedCounter(ReplicatedData):

    def __init__(self):
        self.current_value = 0
        self.delta = 0

    def increment(self, increment):
        #print('INCREMENTING')
        self.current_value += increment
        self.delta += increment
        return self
    
    def decrement(self, decrement):
        self.current_value -= decrement
        self.delta -= decrement
        return self

    def get_and_reset_delta(self):
        if self.delta != 0:
            current_delta = ReplicatedEntityDelta(counter=ReplicatedCounterDelta(change=self.delta))
            self.delta = 0
            return current_delta
        else:
            return None

    def apply_delta(self, delta):
        if delta.counter == None:
            raise Exception(f'Cannot apply delta {delta} to ReplicatedCounter')

        self.current_value += delta.counter.change

'''

d = ReplicatedCounter()
d.increment(3)
delta = d.get_and_reset_delta()
print(delta)
d.apply_delta(delta)
print(d.current_value)
print(d.delta)
'''