; Name: Humna Imran
; Roll Number: 2023-BS-AI-017
; Lab 4 - Question 9
; Task: Divide 1Ah (26) by 05h (5)

ORG 100h           ; Program start

MOV AX, 001Ah      ; Load 26 decimal (1Ah) into AX
MOV DX, 0000h      ; Clear high-word register DX
MOV BX, 0005h      ; Load 5 decimal (05h) into BX

DIV BX             ; Perform Division
                   ; 26 / 5 = 5 with remainder 1
                   ; AX (Quotient) = 0005h
                   ; DX (Remainder) = 0001h

MOV AH, 4Ch        ; Exit setup
INT 21h            ; Execute exit     
