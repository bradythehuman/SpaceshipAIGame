class Mood:
    def __init__(self):
        self.crew_damage = []
        self.hull = []
        self.deaths = []
        self.win = []
        self.ai_mistakes = 0  # Acions that reduce crews trust in the ai.

        self.fear = self.calculate_fear()
        self.distrust = self.calculate_distrust()


    def fight_end_update(self, crew, ship, victory=True):
        if victory:
            self.win.append(True)
        else:
            self.win.append(False)
        damage = 0
        for member in crew:
            damage += member.stats["max_health"] - member.health
        self.crew_damage.append(damage)
        self.hull.append(ship.hull - ship.hull_dmg)
        self.

    def calculate_fear(self):
        fear = 0
        weighting =
        return fear

    def calculate_distrust(self):
        distrust = 0
        return distrust

def diminishing_effect(list, weight, division_factor=2):
    result = 0
    for i in range(1, len(list)+1):
        if list[-i]:
            result += weight
        weight /= division_factor
        if not weight:
            break
    return result