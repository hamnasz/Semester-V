ORG 100h

MOV AL, 85h        ; Load 85h (Binary: 1000 0101)
                   ; MSB is 1, so Shift Left will set Carry.

SHL AL, 1          ; Shift Left.
                   ; New AL = 0Ah (0000 1010), Carry Flag = 1

JNC SkipSub        ; Jump if No Carry (Skip subtraction)

; Logic: If we are here, Carry is 1
SUB AL, 01h        ; Subtract 1 from AL (0Ah - 01h = 09h)

SkipSub:
MOV AH, 4Ch
INT 21h
RET    
