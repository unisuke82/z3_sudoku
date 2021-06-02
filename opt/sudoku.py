from z3 import *
import math
import time

startTime = time.time()
solver = Solver()

problem = [
    [0,0,6,0,0,0,4,0,0],
    [0,0,0,1,0,8,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,4,0,0,0,0],
    [0,0,0,7,6,0,0,0,2],
    [8,0,9,0,0,0,0,1,0],
    [0,0,0,0,7,0,6,0,0],
    [3,0,2,0,0,0,0,0,0],
    [1,0,0,3,0,0,0,0,0]]
sudoku_size = len(problem)

X = [ [[Bool("P_%s_%s_%s" % (ri, cj, k+1))
        for k in range(sudoku_size)]
       for cj in range(sudoku_size)]
      for ri in range(sudoku_size)
      ]

init = []
for ri,row in enumerate(problem):
    for cj,num in enumerate(row):
        if num!=0:
            init.append(X[ri][cj][num-1])

solver.add(And(init))

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
