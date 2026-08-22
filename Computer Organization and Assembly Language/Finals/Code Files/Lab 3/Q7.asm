.model small
.stack 100h
.data
.code
main proc
    mov cx, 13     ; There are 13 even letters in 26 alphabets
    mov dl, 'B'    ; Start from 'B' (the first even letter)

even_loop:
    mov ah, 02h    ; Print char
    int 21h

    add dl, 2      ; Add 2 to skip the odd letter (B -> D)
    loop even_loop

    mov ah, 4ch    ; Exit
    int 21h
main endp
end main
