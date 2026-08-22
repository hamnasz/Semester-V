; Name: Humna Imran
; Roll Number: 2023-BS-AI-017
; Lab 4 - Question 3
; Task: Subtract 0050h from 00A0h, result in BX

ORG 100h           ; Standard COM file start

MOV BX, 00A0h      ; Load the Minuend (Total) into BX
MOV CX, 0050h      ; Load the Subtrahend (Amount to remove) into CX

SUB BX, CX         ; Subtract CX from BX
                   ; Logic: BX = 00A0h - 0050h = 0050h

MOV AH, 4Ch        ; Function to terminate
INT 21h            ; Execute interrupt
