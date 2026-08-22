; Name: Humna Imran
; Roll Number: 2023-BS-AI-017
; Lab 4 - Question 10
; Task: Divide 1000h by 10h

ORG 100h           ; Origin 100h

MOV AX, 1000h      ; Load Dividend 1000h into AX
MOV DX, 0000h      ; Clear DX (Essential for accurate 16-bit division)
MOV BX, 0010h      ; Load Divisor 10h into BX

DIV BX             ; Divide DX:AX by BX
                   ; 1000h / 10h = 100h
                   ; AX (Quotient) = 0100h
                   ; DX (Remainder) = 0000h

MOV AH, 4Ch        ; Exit function
INT 21h            ; DOS Interrupt
