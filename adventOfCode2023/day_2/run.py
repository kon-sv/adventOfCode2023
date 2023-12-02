import re
from typing import List, TypedDict

CubeDict = TypedDict('CubeDict', {
    "red": int,
    "green": int,
    "blue": int
})

class Pull:
    cubes: CubeDict

    def __init__(self, cubes) -> None:
        self.cubes = {
            "red": cubes["red"],
            "green": cubes["green"],
            "blue": cubes["blue"]
        }

class Game:
    id: int
    pulls: List[Pull]

    

    def __init__(self, id, pulls):
        self.id = id
        self.pulls = pulls

    def pull_sum(self):
        sum = {
            "red": 0,
            "green": 0,
            "blue": 0
        }
        for p in self.pulls:
            for c, v in p.cubes.items():
                sum[c] = sum[c] + v
        return sum
        
    def within_limit(self, red, green, blue):
        for p in self.pulls:
            if p.cubes["red"] > red or p.cubes["green"] > green or p.cubes["blue"] > blue:
                return False
        return True

    def minimum_setup(self) -> CubeDict:
        setup: CubeDict = {
            "red": 0,
            "green": 0,
            "blue": 0
        }
        for p in self.pulls:
            for color in ['red', 'green', 'blue']:
                if p.cubes[color] > setup[color]:
                    setup[color] = p.cubes[color]

        return setup
    
    def power(self):
        setup = self.minimum_setup()
        return setup["red"] * setup["green"] * setup["blue"]

    def print(self):
        print(f'Game {self.id}')
        print('    Pulls:')
        for i, pull in enumerate(self.pulls):
            print('   ', i)
            for color, amount in pull.cubes.items():
                print(f'        {color}: {amount}', )
        

def parse_line(line: str) -> Game:
    cubes_dict = {
        "red": 0,
        "green": 0,
        "blue": 0
    }

    match = re.match(r'Game\ (\d+)\: (.*)', line)
    id = match.group(1)
    pulls_str = match.group(2)

    pulls_list = []
    for pull in pulls_str.split(';'):
        pull = pull.strip()
        cubes = pull.split(',')
        cubes_dict = {
            "red": 0,
            "green": 0,
            "blue": 0
        }
        for cube in cubes:
            cube_color = cube.strip().split(' ')
            color = cube_color[1]
            amount = cube_color[0]
            cubes_dict[color] = int(amount)
            
        pulls_list.append(Pull(cubes_dict))


    return Game(id, pulls_list)

def game_list() -> List[Game]:
    games = []
    with open("input.txt") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            # print(line.strip())
            game = parse_line(line)
            games.append(game)
            #game.print()
            # pretty_print(game)
            # print(line)
    return games

games = game_list()

def test_1(games: List[Game]):
    limit = {
        "red": 12,
        "green": 13,
        "blue": 14
    }

    s = 0
    for game in games:
        if game.within_limit(**limit):
            s = sum([s, int(game.id)])
    print(s)

test_1(games)

def test_2(games: List[Game]):
    s = 0
    for game in games:
        power = game.power()
        s = sum([s, power])
    print(s)

test_2(games)


def debug(games: List[Game]):
    test_game = 2
    game = games[test_game]
    game.print()
    print(game.pull_sum())
    print(game.minimum_setup())
    print(game.power())

# debug(games)



# test(limit)

# gg = "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"

# m = re.search('Game (\d): (.*)', gg)
# print(m.group(1))
# print(m.group(2))



