class Connection():
    def __init__(self, origin, target):
        self.origin = origin
        self.target = target
        self.weight = None
        self.enabled = True