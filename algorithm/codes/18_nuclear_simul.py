import sys

sys.stdin = open('input.txt')

class Atom:
    def __init__(self, x: int, y:int, dir:int, energy:int ):
        self.x= x
        self.y =y
        self.dir =dir
        self.energy = energy

    dx = [0, 0, -1, 1]
    dy = [1, -1, 0, 0]
    def is_collapse(self,another:Atom):
        

T = int(input())


for tc in range(1, T+1):
    N = int(input())

