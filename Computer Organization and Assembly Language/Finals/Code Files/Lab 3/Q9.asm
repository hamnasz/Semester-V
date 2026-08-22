.model small
.stack 100h
.data
.code
main proc
    mov cx, 5       ; Print 5 stars
    
star_loop:
    push cx         ; Save the main loop counter (because we use CX for delay)

    ; Print one star
    mov dl, '*'
    mov ah, 02h
    int 21h

    ; --- DELAY LOGIC START ---
    ; A simple empty loop to waste time
    mov cx, 0FFFFh  ; Set a large number
delay:
    nop             ; Do nothing
    nop
    loop delay      ; Repeat until CX becomes 0
    ; --- DELAY LOGIC END ---

    pop cx          ; Restore main loop counter
    loop star_loop  ; Repeat star printing

    mov ah, 4ch     ; Exit
    int 21h
main endp
end main
