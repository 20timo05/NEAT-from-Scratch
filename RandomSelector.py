import random


class RandomSelector():
    @staticmethod
    def get(list):
        total_score = sum([obj.score for obj in list])
        v = random.random() * total_score
        c = 0
        for obj in list:
            c += obj.score
            if c >= v:
                return obj
        return None