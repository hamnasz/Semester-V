.model small
.stack 100h
.data
    msg db 'HELLO', 0Ah, 0Dh, '$' ; 0Ah is New Line, 0Dh is Carriage Return

.code
main proc
    mov ax, @data
    mov ds, ax

    mov cx, 5      ; Set loop counter to 5

print_hello:
    lea dx, msg    ; Load address of "HELLO"
    mov ah, 09h    ; Print string function
    int 21h
    
    loop print_hello ; Repeat 5 times

    mov ah, 4ch    ; Exit
    int 21h
main endp
end main
