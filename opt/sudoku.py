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

def have_value():
    have = And([ Or([And(X[i][j][a], Not(X[i][j][b]), Not(X[i][j][c]), Not(X[i][j][d]))
                     for a,b,c,d in itertools.permutations(range(sudoku_size))])
                 for j in range(sudoku_size)
                 for i in range(sudoku_size)
                 ])
    solver.add(have)

def column_unique():
    cells_c = And([Or([And(X[0][j][a], X[1][j][b], X[2][j][c], X[3][j][d])
                    for a,b,c,d in itertools.permutations(range(sudoku_size))])
                    for j in range(sudoku_size)
               ])
    solver.add(cells_c)

def row_unique():
    row_c = And([ Or([And(X[i][0][a], X[i][1][b], X[i][2][c], X[i][3][d])
                        for a,b,c,d in itertools.permutations(range(sudoku_size))])
                    for i in range(sudoku_size)
                    ])
    solver.add(row_c)

def square_unique():
    square_c = And([ Or([And(X[i*2][j*2][a], X[i*2+1][j*2][b], X[i*2][j*2+1][c], X[i*2+1][j*2+1][d])
                         for a,b,c,d in itertools.permutations(range(sudoku_size))])
                     for i in range(int(math.sqrt(sudoku_size)))
                     for j in range(int(math.sqrt(sudoku_size)))
                     ])
    solver.add(square_c)

have_value()
column_unique()
row_unique()
square_unique()

solver.add(
    And(
        X[0][0][1],
        X[0][1][0],
        X[0][2][2],
        X[3][1][3],
        X[3][2][0],
        X[3][3][1],
    )
)

solver.check()
solver.model()

if solver.check()==sat:
    r = [ [ [ solver.model().evaluate(X[i][j][k]) for k in range(sudoku_size) ].index(True)+1
            for j in range(sudoku_size) ]
          for i in range(sudoku_size)
          ]
    print(r)

else:
    print(solver.check())