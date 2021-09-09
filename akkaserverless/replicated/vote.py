from akkaserverless.replicated.data import ReplicatedData
from akkaserverless.akkaserverless.component.replicatedentity.replicated_entity_pb2 import (
    VoteDelta,
    ReplicatedEntityDelta
)


class ReplicatedVote(ReplicatedData):

    def __init__(self):
        self.current_value = False
        self.voters = 1
        self.votes_for = 0
        self.vote_changed = False

    def vote(self, new_vote: bool):
        if type(new_vote) != bool:
            raise Exception("vote() requires a bool")

        if self.current_value == new_vote:
            return

        if self.vote_changed == True:
            self.vote_changed = False
        else: 
            self.vote_changed = True

        self.current_value = new_vote
        self.voters += 1
        if self.vote_changed == True:
            self.votes_for += 1
        else:
            self.votes_for -= 1

    def get_current_value(self):
        return self.current_value

    def get_votes(self):
        return self.voters

    def get_votes_for(self):
        return self.votes_for

    def has_delta(self):
        self.vote_changed

    def delta(self):
        VoteDelta
        if self.vote_changed:
            ReplicatedEntityDelta(self_vote=VoteDelta(change=self.current_value, votes_for= self.votes_for, total_voters= self.voters))
        else:
            return None

    def apply_delta(self, delta):
        self.current_value = delta.self_vote
        self.votes_for = delta.votes_for
        self.votes = delta.total_voters




#d = ReplicatedVote()
#d.vote(True)
#d.vote(False)
#d.vote(True)
#d.vote(True)
#d.vote(False)
#print(d.get_votes_for())
#print(d.get_votes())
#delta = d.delta()
#print(delta)
#d.apply_delta(delta)
#print(d.current_value)
#print(d.delta)
