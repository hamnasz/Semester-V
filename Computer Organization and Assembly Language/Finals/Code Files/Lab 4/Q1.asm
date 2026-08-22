ORG 100h           ; Origin of the program (COM file standard)

MOV AX, 1000h      ; Initialize AX with the first value 1000h
MOV BX, 2000h      ; Initialize BX with the second value 2000h

ADD AX, BX         ; Add the value of BX to AX
                   ; Logic: AX = 1000h + 2000h = 3000h

MOV AH, 4Ch        ; DOS function to exit program
INT 21h            ; Call DOS interrupt to terminate
