def transform_up(pos, scalar=1):
    pos[1] -= scalar
    return pos


def transform_down(pos, scalar=1):
    pos[1] += scalar
    return pos


def transform_left(pos, scalar=1):
    pos[0] -= scalar
    return pos


def transform_right(pos, scalar=1):
    pos[0] += scalar
    return pos


class Crew:
    base_stats = {"health": 10,  # Basic stats
                  "defense": 1,
                  "attack": 1,
                  "clarity": 3,  # Personality
                  "aggression": 3,
                  "recklessness": 3,
                  "confidence": 3,
                  "selfish": False,
                  "turret_operator": 0,  # Skills
                  "pilot": 0,
                  "mechanic": 0,
                  "medic": 0,
                  "combat": 0}

    def __init__(self, pos):
        # Abstract stats
        self.stats = self.base_stats
        self.victories = 0

        # Calculated stats
        self.fear = 0
        self.frenzied = False
        self.experience_with_ai = 0

        # Spacial stats
        self.pos = pos
        self.target_pos = []

    def pathing(self, floor, end):
        # Assemble graph from ship floor tiles list. key = node, value = list of adjacent nodes
        graph = {}
        for tile in floor:
            adjacency_list = []
            test_pos = transform_up(list(tile))
            if test_pos in floor:
                adjacency_list.append(str(test_pos))
            test_pos = transform_down(list(tile))
            if test_pos in floor:
                adjacency_list.append(str(test_pos))
            test_pos = transform_left(list(tile))
            if test_pos in floor:
                adjacency_list.append(str(test_pos))
            test_pos = transform_right(list(tile))
            if test_pos in floor:
                adjacency_list.append(str(test_pos))
            graph[str(tile)] = adjacency_list

        # Rough imlimentation of breadth first search algorithm to find the shortest path from the crew members position
        # to the end value taken as a parameter. Returns empty list is path is impossible. CANNOT CURRENTLY HANDLE
        # OBSTICALS/OTHER CREW MEMBERS!
        initial = str(self.pos)
        end = str(end)
        shortest_path_tree = {initial: [initial]}
        unknown = list(graph.keys())
        unknown.remove(initial)
        queue = [initial]
        while queue:
            node = queue.pop(0)
            for adjacent in graph[node]:
                if adjacent in unknown:
                    unknown.remove(adjacent)
                    queue.append(adjacent)
                    shortest_path_tree[adjacent] = list(shortest_path_tree[node]) + [adjacent]

        if end in shortest_path_tree:
            return shortest_path_tree[end]
        else:
            return []






    # def calculate_stats(self):
    #     if self.stats["clarity"] < 2 and self.stats["aggression"] > 4:
    #         self.frenzied = True
    #     else:
    #         self.frenzied = False
    #
    #     fear = 0
    #     # Add fear if enemy damage potential is a certain degree above your own. (degree depends on confidence)
    #     # Add fear if room is on fire, out of oxygen or broken in some way
    #     # Add fear if AI is percieved as malicious
    #     self.fear = fear

    # def get_target(self):
    #     if self.frenzied:
    #         # Attack the nearest person
    #         pass

if __name__ == "__main__":
    import ship

    tim = Crew([25, 17])
    tims_ship = ship.Ship()
    print(tim.pathing(tims_ship.floor, [23, 10]))
