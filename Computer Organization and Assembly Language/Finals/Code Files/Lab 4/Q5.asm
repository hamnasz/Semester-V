; Name: Humna Imran
; Roll Number: 2023-BS-AI-017
; Lab 4 - Question 5
; Task: Subtract 1 from 0 (Result is -1, or FFFFh)

ORG 100h           ; Start program

MOV AX, 0000h      ; Load 0 into AX
MOV BX, 0001h      ; Load 1 into BX

SUB AX, BX         ; Subtract 1 from 0
                   ; Logic: 0 - 1 = -1
                   ; In Hex (2's complement), -1 is represented as FFFFh

MOV AH, 4Ch        ; Exit function
INT 21h            ; Call interrupt
