from translations import TRANSLATIONS

def get_opcode(instruction):
    """Extrai o opcode (bits 0-6) da instrução"""
    return instruction & 0x7F

def get_rd(instruction):
    """Extrai o registrador de destino (bits 7-11)"""
    return (instruction >> 7) & 0x1F

def get_funct3(instruction):
    """Extrai o funct3 (bits 12-14)"""
    return (instruction >> 12) & 0x7

def get_rs1(instruction):
    """Extrai o registrador fonte 1 (bits 15-19)"""
    return (instruction >> 15) & 0x1F

def get_rs2(instruction):
    """Extrai o registrador fonte 2 (bits 20-24)"""
    return (instruction >> 20) & 0x1F

def get_funct7(instruction):
    """Extrai o funct7 (bits 25-31)"""
    return (instruction >> 25) & 0x7F

def get_imm_i(instruction):
    """Extrai o imediato do formato I"""
    return (instruction >> 20) & 0xFFF

def get_imm_s(instruction):
    """Extrai o imediato do formato S"""
    imm_11_5 = (instruction >> 25) & 0x7F
    imm_4_0 = (instruction >> 7) & 0x1F
    return (imm_11_5 << 5) | imm_4_0

def get_imm_b(instruction):
    """Extrai o imediato do formato B"""
    imm_12 = (instruction >> 31) & 0x1
    imm_11 = (instruction >> 7) & 0x1
    imm_10_5 = (instruction >> 25) & 0x3F
    imm_4_1 = (instruction >> 8) & 0xF
    return (imm_12 << 12) | (imm_11 << 11) | (imm_10_5 << 5) | (imm_4_1 << 1)

def get_imm_u(instruction):
    """Extrai o imediato do formato U"""
    return (instruction >> 12) & 0xFFFFF

def get_imm_j(instruction):
    """Extrai o imediato do formato J"""
    imm_20 = (instruction >> 31) & 0x1
    imm_10_1 = (instruction >> 21) & 0x3FF
    imm_11 = (instruction >> 20) & 0x1
    imm_19_12 = (instruction >> 12) & 0xFF
    return (imm_20 << 20) | (imm_19_12 << 12) | (imm_11 << 11) | (imm_10_1 << 1)

def decode_instruction(instruction, lang='pt_BR'):
    """Decodifica todos os campos da instrução baseado no tipo"""
    opcode = get_opcode(instruction)
    
    # Mapeamento dos opcodes para os tipos de instrução
    opcode_types = {
        0x33: "R",  # Operações aritméticas e lógicas
        0x13: "I",  # Operações imediatas
        0x03: "I",  # Load
        0x23: "S",  # Store
        0x63: "B",  # Branch
        0x37: "U",  # LUI
        0x17: "U",  # AUIPC
        0x6F: "J",  # JAL
        0x67: "I",  # JALR
    }
    
    tipo = opcode_types.get(opcode, "Desconhecido")
    result = {
        "tipo": tipo,
        "opcode": opcode,
        "rd": get_rd(instruction),
        "funct3": get_funct3(instruction),
        "rs1": get_rs1(instruction)
    }
    
    if tipo == "R":
        result.update({
            "rs2": get_rs2(instruction),
            "funct7": get_funct7(instruction)
        })
    elif tipo == "I":
        result["imm"] = get_imm_i(instruction)
    elif tipo == "S":
        result.update({
            "rs2": get_rs2(instruction),
            "imm": get_imm_s(instruction)
        })
    elif tipo == "B":
        result.update({
            "rs2": get_rs2(instruction),
            "imm": get_imm_b(instruction)
        })
    elif tipo == "U":
        result["imm"] = get_imm_u(instruction)
    elif tipo == "J":
        result["imm"] = get_imm_j(instruction)
    
    return result

def format_instruction_info(info, lang='pt_BR'):
    """Formata a informação da instrução para exibição"""
    base = TRANSLATIONS[lang]['instruction_format'].format(info['tipo'].lower())
    
    if 'rd' in info:
        base += f", {TRANSLATIONS[lang]['register_dest'].format(info['rd'])}"
    if 'funct3' in info:
        base += f", {TRANSLATIONS[lang]['function3'].format(info['funct3'])}"
    if 'rs1' in info:
        base += f", {TRANSLATIONS[lang]['register_src1'].format(info['rs1'])}"
    if 'rs2' in info:
        base += f", {TRANSLATIONS[lang]['register_src2'].format(info['rs2'])}"
    if 'imm' in info:
        base += f", {TRANSLATIONS[lang]['immediate'].format(info['imm'])}"
    if 'funct7' in info:
        base += f", {TRANSLATIONS[lang]['function7'].format(info['funct7'])}"
    
    return base

def read_hex_file(filename):
    """Lê um arquivo de instruções em hexadecimal"""
    instructions = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                hex_str = line.strip()
                if hex_str:
                    instruction = int(hex_str, 16)
                    instructions.append(instruction)
    except FileNotFoundError:
        print(f"Erro: Arquivo {filename} não encontrado")
        return None
    return instructions

def main():
    filename = input("Digite o nome do arquivo de instruções: ")
    instructions = read_hex_file(filename)
    
    if instructions:
        print("\nDecodificação das instruções:")
        print("=" * 70)
        for i, instruction in enumerate(instructions):
            info = decode_instruction(instruction)
            formatted_info = format_instruction_info(info)
            print(f"Instrução {i+1}: 0x{instruction:08X} -> {formatted_info}")

if __name__ == "__main__":
    main() 