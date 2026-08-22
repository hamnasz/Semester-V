.model small
.stack 100h
.data
    msg_eq  db 'EQUAL$'
    msg_neq db 'NOT EQUAL$'

.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, 5      ; First number (Change this to test)
    mov bx, 5      ; Second number (Change this to test)

    cmp ax, bx     ; Compare AX and BX
    je  is_equal   ; Jump if Equal (JE) to label 'is_equal'

    ; If we are here, they are NOT equal
    lea dx, msg_neq
    mov ah, 09h
    int 21h
    jmp exit_prog  ; Skip the equal part

is_equal:
    ; This part runs only if the jump happened
    lea dx, msg_eq
    mov ah, 09h
    int 21h

exit_prog:
    mov ah, 4ch
    int 21h
main endp
end main
