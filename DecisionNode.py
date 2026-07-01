
class DecisionNode:
    
    def __init__(self, condition=None, yes=None, no=None, result=None):
        self.condition = condition
        self.yes = yes
        self.no = no
        self.result = result