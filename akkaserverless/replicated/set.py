from akkaserverless.replicated.data import ReplicatedData

class ReplicatedSet(ReplicatedData):

    def __init__(self):
        self.current_value = set()
        self.added = set()
        self.removed = set()
        self.cleared = False

    def size(self):
        return len(self.current_value)

    def contains(self, item):
        return item in self.current_value
        
    def add(self, item):
        if item in self.current_value:
            return False
        else: 
            self.current_value.add(item)
            self.added.add(item) # encode - need todo
    
    def remove(self, item):
        if item not in self.current_value:
            return False
        else:
            # encode - need todo
            self.current_value.remove(item)
            self.removed.add(item) # encode - need todo

    def clear(self):
        self.current_value.clear()
        self.added.clear()
        self.removed.clear()
        self.cleared = True

    def delta(self):
        return self.cleared, self.removed, self.added
    
    def has_delta(self):
        return (not self.cleared) or len(self.removed) > 0 or len(self.added)>0

    def reset_delta(self):
        self.added.clear()
        self.removed.clear()
        self.cleared = False

    def apply_delta(self, delta):
        if delta[0] == True:
            self.current_value.clear()
        
        self.current_value -= self.removed
        self.current_value.update(self.added)


'''
d = ReplicatedSet()
#print(isinstance(d, ReplicatedData))
d.add("dd")
d.add(1)
#ßd.add(ReplicatedData())
#print(d.current_value)
d.remove("dd")
print(d.current_value)
print(d.has_delta())
print(d.delta())
#d.apply_delta(d.delta())
#print(d.current_value)
'''