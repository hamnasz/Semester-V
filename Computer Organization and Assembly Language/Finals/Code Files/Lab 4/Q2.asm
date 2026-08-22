ORG 100h           ; Origin at 100h

MOV AX, 0100h      ; Load first operand into AX
MOV BX, 3F00h      ; Load second operand into BX

ADD AX, BX         ; Add BX to AX
                   ; Logic: 0100h + 3F00h = 4000h

MOV AH, 4Ch        ; Prepare to exit
INT 21h            ; Return control to DOS
