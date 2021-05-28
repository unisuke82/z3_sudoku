from z3 import *
import math
import time

startTime = time.time()

solver = Solver()
sudoku_size = 9

X = [ [[Bool("P_%s_%s_%s" % (ri, cj, k+1))
        for k in range(sudoku_size)]
       for cj in range(sudoku_size)]
      for ri in range(sudoku_size)
      ]

def have_value():
    have = And([ Or([X[i][j][k] for k in range(sudoku_size)])
                 for j in range(sudoku_size)
                 for i in range(sudoku_size)
                 ])
    not_same = And([ Or(Not(X[i][j][a]), Not(X[i][j][b]))
                     for a in range(sudoku_size)
                     for b in range(a+1,sudoku_size)
                 for j in range(sudoku_size)
                 for i in range(sudoku_size)
                 ])
    solver.add(have)
    solver.add(not_same)

def column_unique():
    for j in range(sudoku_size):
        not_same_in_cells = And([ Or( Not(X[m][j][a]), Not(X[n][j][a]) )
                                  for a in range(sudoku_size)
                                  for m in range(sudoku_size)
                                  for n in range(m+1,sudoku_size)
                                  ])
        solver.add(not_same_in_cells)

def row_unique():
    for i in range(sudoku_size):
        not_same_in_rows = And([ Or( Not(X[i][m][a]), Not(X[i][n][a]) )
                                  for a in range(sudoku_size)
                                  for m in range(sudoku_size)
                                  for n in range(m+1,sudoku_size)
                                  ])
        solver.add(not_same_in_rows)

def square_unique():
    for i in range(int(math.sqrt(sudoku_size))):
        for j in range(int(math.sqrt(sudoku_size))):
            not_same_in_squares = And([ Or( Not(X[i*int(math.sqrt(sudoku_size))+m][j*int(math.sqrt(sudoku_size))+n][a]), Not(X[i*int(math.sqrt(sudoku_size))+p][j*int(math.sqrt(sudoku_size))+q][a]) )
                                        for a in range(sudoku_size)
                                        for m in range(int(math.sqrt(sudoku_size)))
                                        for n in range(int(math.sqrt(sudoku_size)))
                                        for p in range(int(math.sqrt(sudoku_size)))
                                        for q in range(n+1,int(math.sqrt(sudoku_size)))
                                        ])
            solver.add(not_same_in_squares)

have_value()
column_unique()
row_unique()
square_unique()

solver.add(
    And(
        X[0][0][7],
        X[1][2][2],
        X[1][3][5],
        X[2][1][6],
        X[2][4][8],
        X[2][6][1],
        X[3][1][4],
        X[3][5][6],
        X[4][4][3],
        X[4][5][4],
        X[4][6][6],
        X[5][3][0],
        X[5][7][2],
        X[6][2][0],
        X[6][7][5],
        X[6][8][7],
        X[7][2][7],
        X[7][3][4],
        X[7][7][0],
        X[8][1][8],
        X[8][6][3]
    )
)

solver.check()

if solver.check()==sat:
    solver.model()
    r = [ [ [ solver.model().evaluate(X[i][j][k]) for k in range(sudoku_size) ].index(True)+1
            for j in range(sudoku_size) ]
          for i in range(sudoku_size)
          ]
    for row in r:
        for num in row:
            print(num,end=' ')
        print('')

else:
    print(solver.check())

endTime = time.time()
runTime = endTime - startTime

print('run time : '+ str(runTime))
