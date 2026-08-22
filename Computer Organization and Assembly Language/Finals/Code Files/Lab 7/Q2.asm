org 100h

MOV AL, 40h      ; Load 40h into AL
SHR AL, 1        ; Divide by 2 (Shift Right by 1): 40h / 2 = 20h

CMP AL, 15h      ; Compare result (20h) with 15h
JA ItIsGreater   ; Jump if Above (Greater) because 20h > 15h

JMP Stop         ; Skip if not greater

ItIsGreater:
MOV BL, 01h      ; Marker: Move 1 to BL to show we jumped successfully

Stop:
MOV AH, 4Ch      ; Exit program
INT 21h
