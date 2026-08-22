.model small
.stack 100h
.data
.code
main proc
    mov cx, 26     ; There are 26 letters in the alphabet
    mov dl, 'A'    ; Start with letter 'A'

print_loop:
    mov ah, 02h    ; Function 02h: Print single character in DL
    int 21h

    inc dl         ; Increment DL to get the next character (A -> B)
    loop print_loop; Decrement CX. If CX is not 0, jump to print_loop

    mov ah, 4ch    ; Exit
    int 21h
main endp
end main
