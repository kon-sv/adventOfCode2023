from typing import List, Tuple

SchematicList = List[List[str]]
Pos = Tuple[int, int]

schematic_2d: SchematicList = []

with open('input.txt') as f:
    for y, line in enumerate(f.readlines()):
        # print(len(line))
        schematic_2d.append([])
        for x, character in enumerate(line.strip()):
            schematic_2d[y].append(character)

def clamp(number):
    return max(0, min(number, 139))


class Digiloc:
    locating_digit: bool
    digits: List
    start_pos: Pos
    found: bool

    def __init__(self) -> None:
        self.digits = []
        self.start_pos = (0,0)
        self.end_pos = (0,0)

        self.locating_digit = False

    def input(self, char: str, pos: Pos) -> bool:
        if char.isdigit():
            if not self.locating_digit:
                self.locating_digit = True
                self.start_pos = pos
            self.digits.append(char)
        else:
            if self.locating_digit:
                # new number found
                self.found = True
                self.end_pos = pos
                return True
            self.locating_digit = False
        return False

    def flush(self) -> Tuple[int, Pos]:
        if self.found:
            number = int("".join(self.digits))
            pos = self.start_pos
            end_pos = self.end_pos

            self.start_pos = (0,0)
            self.end_pos = (0,0)
            self.digits = []
            self.found = False
            self.locating_digit = False
            return (number, pos, end_pos)


class Schematic:
    numbers: List[Tuple[Pos, Pos, int]]
    schematic_2d: SchematicList
    symbols: List
    gears: List[Tuple[Pos, int]]
    gear_pos: dict
    def __init__(self, schematic_2d: SchematicList) -> None:
        self.schematic_2d = schematic_2d
        self.numbers = []
        self.symbols = []
        self.gears = []
        self.gear_pos = {}

        self.save_numbers()

    def print(self):
        for y in self.schematic_2d:
            for x in y:
                print(x, end='')
            print('')

    def save_numbers(self):
        digiLoc = Digiloc()
        for y, y_list in enumerate(self.schematic_2d):
            for x, character in enumerate(y_list):
                pos = (x, y)
                if digiLoc.input(character, pos):
                    (number, start_pos, end_pos) = digiLoc.flush()
                    self.numbers.append((start_pos, end_pos, number))
                else:
                    if not character.isalnum() and character != '.':
                        self.symbols.append(character)
                
                if character == '*':
                    self.gears.append((pos, character))
                    self.gear_pos[pos] = []

        self.symbols = set(self.symbols)

    def check_adjacency(self, idx):
        # print(self.symbols)
        (pos, end_pos, number) = self.numbers[idx]
        digits = len(str(number))
        # print(pos, number)
        
        # (left, top), (right, bottom)
        box = (
            (clamp(pos[0] - 1), clamp(pos[1] - 1)),
            (clamp(pos[0] + digits), clamp(pos[1] + 1))
        )

        y = box[0][1]
        end_x = box[1][0]
        end_y = box[1][1]
        has_special_symbol = False
        has_gear = False
        while y <= end_y:
            
            x = box[0][0]
            while x <= end_x:
                character = self.schematic_2d[y][x]
                # print(character, end='')

                if not has_special_symbol and character in self.symbols:
                    # print("special!")
                    has_special_symbol = True

                if not has_gear and character == "*":
                    has_gear = True
                    self.gear_pos[(x, y)].append(number)

                x = x+1
            # print('')
            y = y+1
        # print(box)
        return {
            "has_special_symbol": has_special_symbol,
            "has_gear": has_gear
        }

    def print_adjacency(self, idx, type='numbers'):
        if type  == 'numbers':
            (pos, number) = self.numbers[idx]
        elif type == 'gears':
            (pos, number) = self.gears[idx]
        else:
            return
        
        print(pos, number)

        digits = len(str(number))

        # (left, top), (right, bottom)
        box = (
            (clamp(pos[0] - 1), clamp(pos[1] - 1)),
            (clamp(pos[0] + digits), clamp(pos[1] + 1))
        )

        y = box[0][1]
        end_x = box[1][0]
        end_y = box[1][1]
        while y <= end_y:
            
            x = box[0][0]
            while x <= end_x:
                character = self.schematic_2d[y][x]
                print(character, end='')
                x = x+1
            print('')
            y = y+1


schematic = Schematic(schematic_2d)

def test_1(schematic: Schematic):
    s = 0
    for i, number in enumerate(schematic.numbers):
        if schematic.check_adjacency(i):
            print(number)
            s = sum([s, number[1]])
    print(s)

test_1(schematic)

def test_2(schematic: Schematic):
    s = 0
    i = 0
    # checks = schematic.check_adjacency(i)
    # print(checks["has_gear"])
    schematic.print_adjacency(0,'gears')

    for i, number in enumerate(schematic.numbers):
        schematic.check_adjacency(i)
            

    for k, v in schematic.gear_pos.items():
        if len(v) == 2:
            print(k, v, end='')
            val = v[0] * v[1]
            print('', val)

            s = sum([s, val])
    print(s)


    
test_2(schematic)


            

