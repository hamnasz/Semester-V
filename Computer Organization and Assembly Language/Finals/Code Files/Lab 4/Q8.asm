 ; Name: Humna Imran
; Roll Number: 2023-BS-AI-017
; Lab 4 - Question 8
; Task: Divide 20h by 04h

ORG 100h           ; Origin

MOV AX, 0020h      ; Load Dividend (lower 16 bits) into AX
MOV DX, 0000h      ; Clear DX (upper 16 bits) to ensure clean division
MOV BX, 0004h      ; Load Divisor into BX

DIV BX             ; Divide DX:AX by BX
                   ; Quotient (AX) = 20h / 04h = 08h
                   ; Remainder (DX) = 0000h

MOV AH, 4Ch        ; Return to DOS
INT 21h            ; Exit
