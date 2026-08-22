; Name: Humna Imran
; Roll Number: 2023-BS-AI-017
; Lab 4 - Question 7
; Task: Multiply 100 decimal (64h) by 4

ORG 100h           ; Standard start

MOV AX, 0064h      ; Load 100 decimal (which is 64h) into AX
MOV BX, 0004h      ; Load 4 decimal (04h) into BX

MUL BX             ; Multiply AX by BX (100 * 4 = 400)
                   ; 400 in Hex is 190h
                   ; Result: DX=0000h, AX=0190h

MOV AH, 4Ch        ; Exit code
INT 21h            ; Interrupt
