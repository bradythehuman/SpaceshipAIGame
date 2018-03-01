import positional


class Crew:
    base_stats = {"max_health": 5,  # Basic stats
                  "defense": 0,
                  "attack": 1,
                  "delusional": False,  # Personality
                  "aggressive": False,
                  "recklessness": False,
                  "over-confident": False,
                  "selfish": False,
                  "turret_operator": 0,  # Skills
                  "pilot": 0,
                  "mechanic": 0,
                  "medic": 0,
                  "combat": 0}

    def __init__(self, game):
        # Abstract stats
        self.game = game
        self.stats = self.base_stats
        self.health = self.stats["max_health"]
        self.role = ''  # Key determinate in the get_target method
        self.state = "calm"
        # Spacial stats
        self.pos = [0, 0]
        self.target = []
        self.shortest_path_tree = {}

    def update(self, game):
        self.pos = game.my_ship.map["bed"][game.crew.index(self)]  # Should only be done between rounds
        self.update_state(game.mood)
        self.get_target()
        self.update_path_tree()

    def update_path_tree(self):
        floor = self.game.get_empty_floor() + [self.pos]
        # Assemble graph from ship floor tiles list. key = node, value = list of adjacent nodes
        graph = {}
        for tile in floor:
            adjacency_list = []
            for transform in [positional.transform_up, positional.transform_down, positional.transform_left,
                              positional.transform_right]:
                test_pos = transform(list(tile))
                if test_pos in floor:
                    adjacency_list.append(tuple(test_pos))
            graph[tuple(tile)] = adjacency_list
        # Rough imlimentation of breadth first search algorithm to find the shortest path from the crew members position
        # to the end value taken as a parameter. Returns empty list is path is impossible. CANNOT CURRENTLY HANDLE
        # OBSTICALS/OTHER CREW MEMBERS!
        initial = tuple(self.pos)
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
        self.shortest_path_tree = shortest_path_tree

    def update_state(self, mood):
        if self.stats["delusional"] and self.stats["aggressive"] and mood.state == "terrified":
            self.state = "frenzied"
        else:
            self.state = "calm"

    # Determines target based on assigned role and other stats
    def get_target(self):
        if self.state == "frenzied":
            # Attack the nearest person
            pass

    def get_path(self, target_pos):
        if tuple(target_pos) in self.shortest_path_tree:
            return self.shortest_path_tree[tuple(target_pos)]
        else:
            return []

    def move_unit(self, target_pos):
        self.pos = target_pos
        self.update_path_tree()

    def display_stats(self):
        pass




