.org 0
.org 0x8000

.equ OUT_PORT, 0x6000

start:
ldx 0
loop:
lda msg, x
cmp 0
beq done
sta OUT_PORT
inx
jmp loop

done:
jmp start

msg: .ascii "Hello world!\n"

.org 0xfffc
.word start
