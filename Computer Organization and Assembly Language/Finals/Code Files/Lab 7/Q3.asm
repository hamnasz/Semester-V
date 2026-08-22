org 100h

MOV DL, 80h       ; Load 80h (Binary: 1000 0000) into DL.
                  ; We choose 80h because the leftmost bit (MSB) is 1.

SHL DL, 1         ; Shift Left by 1.
                  ; The MSB (1) is shifted out into the Carry Flag.
                  ; CF becomes 1. DL becomes 00h.

JC Carry_Set      ; Jump if Carry (JC) is set (CF=1).

JMP Exit          ; Skip if no carry.

Carry_Set:
MOV AX, 1111h     ; Marker: Load 1111h into AX to show we jumped.

Exit:
MOV AH, 4Ch       ; Exit Program
INT 21h             
