05 REM Fibonacci numbers 
10 LET MAX = 5000
20 LET X = 1
25 LET Y = 1
30 IF (X > MAX) THEN GOTO 100
40 PRINT X
50 LET X = X + Y
60 IF (Y > MAX) THEN GOTO 100
70 PRINT Y
80 LET Y = X + Y
90 GOTO 30
100 END