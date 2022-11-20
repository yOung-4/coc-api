import random

class roll():
    def roll(ranging, repeat=1, add=0, plus=1):
        result = []
        final = 0
        for i in range(0,repeat):
            result.append(random.randint(1, ranging))
        for i in result:
            final = final + i
        final += add
        final = final*plus
        return final
