.model small
.stack 100h
.data
    roll_no db 'My Roll No is: 017$'

.code
main proc
    mov ax, @data
    mov ds, ax

    lea dx, roll_no ; Load address of roll number string
    mov ah, 09h     ; Print string function
    int 21h

    mov ah, 4ch     ; Exit
    int 21h
main endp
end main
