.model small
.stack 100h
.data
    msg_one db 'ONE$'
    msg_not db 'NOT ONE$'

.code
main proc
    mov ax, @data
    mov ds, ax

    mov ax, 1      ; Set AX to 1 (Change this to 2 to test "NOT ONE")

    cmp ax, 1      ; Compare AX with 1
    je  print_one  ; Jump if Equal

    ; If not equal:
    lea dx, msg_not
    mov ah, 09h
    int 21h
    jmp quit       ; Skip the "ONE" part

print_one:
    lea dx, msg_one
    mov ah, 09h
    int 21h

quit:
    mov ah, 4ch    ; Exit
    int 21h
main endp
end main
