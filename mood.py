class Mood:
    def __init__(self):
        self.crew_damage = []
        self.hull = []
        self.deaths = []
        self.lose = []
        self.ai_mistakes = 0  # Acions that reduce crews trust in the ai.

        self.fear = self.calculate_fear()  # Range 0 - 100
        self.trust = self.calculate_trust()  # Bool
        self.state = self.calculate_state()  # String

    def fight_end_update(self, crew, ship, victory=True):
        if victory:
            self.lose.append(False)
        else:
            self.lose.append(True)
        damage = 0
        self.deaths.append(0)
        for member in crew:
            if member.health:
                damage += member.stats["max_health"] - member.health
            else:
                self.deaths[-1] += 1
        self.crew_damage.append(damage)
        self.hull.append(ship.hull - ship.hull_dmg)

    def calculate_fear(self):
        fear = sum([self.crew_damage[-x] / x for x in range(1, len(self.crew_damage))])
        fear += diminishing_effect(self.hull, 8)
        fear += diminishing_effect(self.deaths, 8)
        fear += diminishing_effect(self.lose, 8)
        return fear

    def calculate_trust(self):
        if self.ai_mistakes + int(self.fear / 5) >= 40:
            return False
        else:
            return True

    # Possible states include
    def calculate_state(self):
        if self.trust:
            if self.fear < 15:
                return "confident"
            elif self.fear < 40:
                return "neutral"
            elif self.fear < 70:
                return "afraid"
            else:
                return "terrified"
        else:
            if self.fear < 30:
                return "rebellious"
            elif self.fear < 60:
                return "afraid"
            else:
                return "terrified"


def diminishing_effect(stat_list, weight, division_factor=2):
    result = 0
    for i in range(1, len(stat_list)+1):
        if stat_list[-i]:
            result += weight
        weight /= division_factor
        if not weight:
            break
    return result
