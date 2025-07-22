class InvalidMoveException(Exception):
    pass

class MoveFailedException(Exception):
    pass

class Hanoi:
    def __init__(self, towers=[[], [], []]):
        self.towers = towers
        self.towers_dict = {}
        self.move_count = 0

        for t, tower in enumerate(towers):
            for i, ring in enumerate(tower):
                self.towers_dict[ring] = (t, i)
        
    def move(self, source, dest):
        if not self.towers[source]:
            raise InvalidMoveException
        
        ring = self.towers[source][-1]
        print(f"moving {ring} from tower {source} to tower {dest}")

        if self.towers[dest] and self.towers[dest][-1] < ring:
            raise MoveFailedException()
        
        self.towers_dict[ring] = (dest, len(self.towers[dest]))
        self.towers[dest].append(self.towers[source].pop(-1))
        
        print(self)
        self.move_count += 1
    
    def __str__(self):
        return f'{self.towers}'
