.model small
.stack 100h
.data
.code
main proc
    mov cx, 10     ; Loop 10 times (for digits 0 to 9)
    mov dl, '0'    ; Start with character '0'

digit_loop:
    mov ah, 02h    ; Print character function
    int 21h

    inc dl         ; Go to next digit ('0' -> '1')
    loop digit_loop

    mov ah, 4ch    ; Exit
    int 21h
main endp
end main
