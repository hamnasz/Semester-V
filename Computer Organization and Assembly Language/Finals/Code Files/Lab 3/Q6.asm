.model small
.stack 100h
.data
.code
main proc
    ; Push characters onto the stack
    mov ax, 'A'
    push ax        ; Stack: A
    mov ax, 'B'
    push ax        ; Stack: B, A
    mov ax, 'C'
    push ax        ; Stack: C, B, A (Top is C)

    ; Pop and print
    ; 1st Pop
    pop dx         ; dx becomes 'C'
    mov ah, 02h    ; Print char
    int 21h

    ; 2nd Pop
    pop dx         ; dx becomes 'B'
    mov ah, 02h
    int 21h

    ; 3rd Pop
    pop dx         ; dx becomes 'A'
    mov ah, 02h
    int 21h

    mov ah, 4ch    ; Exit
    int 21h
main endp
end main
