org 100h

MOV AL, 03h      ; Load 03h into AL
MOV CL, 2        ; Set shift count to 2 (Shifting left by 2 multiplies by 4)

SHL AL, CL       ; Multiply: 03h * 4 = 0Ch (12 decimal)

ADD AL, 02h      ; Add 02h: 0Ch + 02h = 0Eh (14 decimal)

MOV AH, 4Ch      ; Return control to OS
INT 21h 
