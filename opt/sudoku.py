from z3 import *
import itertools
import math

solver = Solver()
sudoku_size = 4

X = [ [[Bool("P_%s_%s_%s" % (i, j, k+1))
        for k in range(sudoku_size)]
        for j in range(sudoku_size)]
        for i in range(sudoku_size)
    ]

print(X)
print(type(X))

def have_value():
    have = And([ Or([And(X[i][j][a], Not(X[i][j][b]), Not(X[i][j][c]), Not(X[i][j][d]))
                     for a,b,c,d in itertools.permutations(range(sudoku_size))])
                 for j in range(sudoku_size)
                 for i in range(sudoku_size)
                 ])
    solver.add(have)
    print(have)

def column_unique():
    cells_c = And([Or([And(X[0][j][a], X[1][j][b], X[2][j][c], X[3][j][d])
                    for a,b,c,d in itertools.permutations(range(sudoku_size))])
                    for j in range(sudoku_size)
               ])
    solver.add(cells_c)
    print(cells_c)

def row_unique():
    row_c = And([ Or([And(X[i][0][a], X[i][1][b], X[i][2][c], X[i][3][d])
                        for a,b,c,d in itertools.permutations(range(sudoku_size))])
                    for i in range(sudoku_size)
                    ])
    solver.add(row_c)
    print(row_c)

def square_unique():
    square_c = And([ Or([And(X[i*2][j*2][a], X[i*2+1][j*2][b], X[i*2][j*2+1][c], X[i*2+1][j*2+1][d])
                         for a,b,c,d in itertools.permutations(range(sudoku_size))])
                     for i in range(int(math.sqrt(sudoku_size)))
                     for j in range(int(math.sqrt(sudoku_size)))
                     ])
    solver.add(square_c)
    print('square_c')
    print(square_c)

have_value()
column_unique()
row_unique()
square_unique()

print(solver.check())
print(solver.model())


r = [ [ [ solver.model().evaluate(X[i][j][k]) for k in range(sudoku_size) ]
      for j in range(sudoku_size) ]
      for i in range(sudoku_size)
      ]

print_matrix(r)

r = [ [ [ solver.model().evaluate(X[i][j][k]) for k in range(sudoku_size) ].index(True)
        for j in range(sudoku_size) ]
      for i in range(sudoku_size)
      ]
print_matrix(r)