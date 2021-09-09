from akkaserverless.replicated.data import ReplicatedData
from akkaserverless.replicated.set import ReplicatedSet

class ReplicatedMultiMap(ReplicatedData):

    def __init__(self):
        self.entries = {}
        self.removed = set()
        self.cleared = False

    def get_or_create(self, key):
        if key in self.entries:
            return self.entries[key]
        else:
            set = ReplicatedSet()
            self.entries[key] = set
            return set

    def get(self, key):
        return self.entries[key].current_value if key in self.entries else None
        
    def put(self, key, item):
        self.get_or_create(key).add(item)
    
    def remove(self, key, item):
        self.get_or_create(key).remove(item)
        self.removed.add(item)

    def keys(self):
        return self.entries.keys()

    def size(self):
        return sum([len(x.current_value) for x in self.entries.current_values()])

    def is_empty(self):
        return len(self.entries) == 0

    def clear(self):
        self.entries.clear()
        self.removed.clear()
        self.cleared = True

    def delta(self):
        #deltas = set(zip(map(lambda x: x.delta if x.has_delta() else None, self.entries.current_values())))
        updated = {}
        for key in self.entries:
            current_value = self.entries[key]
            if current_value.has_delta():
                updated[key] = current_value.delta()

        return self.cleared, self.removed, updated


    #override def hasDelta: Boolean = cleared || removed.nonEmpty || counters.current_values.exists(_.hasDelta)
    def has_delta(self):
        return (not self.cleared) or len(self.removed) > 0 or len(list(filter(lambda x: x.has_delta(), self.entries.current_values()))) > 0

    def reset_delta(self):
        for entry in self.entries.current_values():
            entry.get_and_reset_delta()
        self.removed = {}
        self.cleared = False

    def apply_delta(self, delta):
        cleared, removed, updated = delta
        if cleared:
            self.entries.clear()
        
        lambda x: self.entries.remove(x), removed

        for update in updated:
            self.get_or_create(update).apply_delta(updated[update])
        #self.current_current_value += delta.counter.change


d = ReplicatedMultiMap()
d.put('reqrw', 2)
d.put('reqrwasdasd', 2)
d.put('reqrwasdasd', 3)
d.put('reqrwasdasd', 34)
print(d.get('reqrwasdasd'))
#d.remove('reqrwasdasd', 34)
#print(d.has_delta())
#delta = d.delta()
#print(delta[0])
#print(d.entries)
#d.apply_delta(delta)
#print(d.entries)
##print(d.get('reqrw'))
#print(d.size())
#d.clear()

#print(d.has_delta())
