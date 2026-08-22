; Name: Humna Imran
; Roll Number: 2023-BS-AI-017
; Lab 4 - Question 4
; Task: Subtract 1F00h from 2000h

ORG 100h           ; Program starts at offset 100h

MOV AX, 2000h      ; Load 2000h into AX (Minuend)
MOV BX, 1F00h      ; Load 1F00h into BX (Subtrahend)

SUB AX, BX         ; Perform Subtraction
                   ; Logic: 2000h - 1F00h = 0100h

MOV AH, 4Ch        ; DOS Exit command
INT 21h            ; Interrupt to exit
