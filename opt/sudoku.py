from z3 import *
import itertools

solver = Solver()
sudoku_size = 4

X = [ [[Bool("P_%s_%s_%s" % (i, j, k+1))
        for k in range(sudoku_size)]
        for j in range(sudoku_size)]
        for i in range(sudoku_size)
    ]

print(X)
print(type(X))

def column_unique():

    cells_c = [Or(X[0][j][k], X[1][j][k], X[2][j][k], X[3][j][k])
               for j in range(sudoku_size)
               for k in range(sudoku_size)
               ]

    solver.add(cells_c)
    print(cells_c)

column_unique()

print(solver.check())
print(solver.model())