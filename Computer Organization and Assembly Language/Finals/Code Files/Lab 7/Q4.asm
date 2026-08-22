ORG 100h

MOV AH, 04h        ; Load 04h into AH
MOV CL, 3          ; Set shift count to 3

SHR AH, CL         ; Shift 04h Right 3 times.
                   ; 04h (0000 0100) -> Shift 3 -> 00h

JZ  ResultIsZero   ; Jump if Zero Flag (ZF) is set

JMP Exit_Prog

ResultIsZero:
MOV BL, 0AAh       ; Marker: Load AAh to indicate result became zero

Exit_Prog:
MOV AH, 4Ch
INT 21h
RET          
