.global _start

_start:
    # Tipo I - Carregar imediato
    addi x8, x0, 5      # x8 = 5 (0x00500413)
    
    # Tipo R - Soma de registradores
    add x9, x8, x8      # x9 = x8 + x8 (0x008404B3)
    
    # Tipo S - Store
    sw x9, 12(x8)       # Memoria[x8 + 12] = x9 (0x00942623)
    
    # Tipo B - Branch
    beq x8, x9, pula    # if (x8 == x9) goto pula (0x00940463)
    
    # Tipo U - Load Upper Immediate
    lui x10, 0x12345    # x10 = 0x12345000 (0x12345537)
    
pula:
    # Tipo J - Jump and Link
    jal x1, fim         # x1 = pc + 4; goto fim (0x008000EF)
    
fim:
    # Encerrar programa
    addi x17, x0, 93    # Syscall exit (93) no RARS
    ecall               # Chamada do sistema 