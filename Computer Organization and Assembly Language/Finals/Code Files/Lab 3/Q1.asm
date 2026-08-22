.model small
.stack 100h
.data
    ; Define the string variable ending with '$'
    name_msg db 'Humna Imran$' 

.code
main proc
    ; Initialize the Data Segment
    mov ax, @data
    mov ds, ax

    ; Print the string
    lea dx, name_msg    ; Load the address of the message into DX
    mov ah, 09h         ; Function 09h: Print string ending in '$'
    int 21h             ; Call DOS interrupt

    ; Exit Program
    mov ah, 4ch         ; Function 4Ch: Terminate program
    int 21h
main endp
end main