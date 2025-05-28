from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum

class ConflictType(Enum):
    RAW = "RAW"  # Read After Write
    WAR = "WAR"  # Write After Read
    WAW = "WAW"  # Write After Write
    CONTROL = "CONTROL"  # Conflito de controle (branch/jump)

@dataclass
class Instruction:
    hex_code: int
    type: str
    rd: int = None
    rs1: int = None
    rs2: int = None
    imm: int = None
    is_branch: bool = False
    is_jump: bool = False

class PipelineAnalyzer:
    def __init__(self, instructions: List[int]):
        self.original_instructions = instructions
        self.decoded_instructions = self._decode_instructions()
        self.conflicts = []
        self.solutions = {}

    def _decode_instructions(self) -> List[Instruction]:
        """Decodifica as instruções hexadecimais em objetos Instruction"""
        decoded = []
        for hex_code in self.original_instructions:
            opcode = hex_code & 0x7F
            rd = (hex_code >> 7) & 0x1F
            funct3 = (hex_code >> 12) & 0x7
            rs1 = (hex_code >> 15) & 0x1F
            rs2 = (hex_code >> 20) & 0x1F
            
            # Determina o tipo da instrução
            if opcode == 0x33:  # Tipo R
                inst_type = "R"
                is_branch = False
                is_jump = False
            elif opcode in [0x13, 0x03, 0x67]:  # Tipo I
                inst_type = "I"
                is_branch = False
                is_jump = (opcode == 0x67)
            elif opcode == 0x23:  # Tipo S
                inst_type = "S"
                is_branch = False
                is_jump = False
            elif opcode == 0x63:  # Tipo B
                inst_type = "B"
                is_branch = True
                is_jump = False
            elif opcode in [0x37, 0x17]:  # Tipo U
                inst_type = "U"
                is_branch = False
                is_jump = False
            elif opcode == 0x6F:  # Tipo J
                inst_type = "J"
                is_branch = False
                is_jump = True
            else:
                inst_type = "UNKNOWN"
                is_branch = False
                is_jump = False

            decoded.append(Instruction(
                hex_code=hex_code,
                type=inst_type,
                rd=rd if inst_type in ["R", "I", "U"] else None,
                rs1=rs1 if inst_type in ["R", "I", "S", "B"] else None,
                rs2=rs2 if inst_type in ["R", "S", "B"] else None,
                is_branch=is_branch,
                is_jump=is_jump
            ))
        return decoded

    def detect_data_conflicts(self, with_forwarding: bool = False) -> List[Tuple[int, int, ConflictType]]:
        """Detecta conflitos de dados entre instruções"""
        conflicts = []
        for i in range(len(self.decoded_instructions)):
            for j in range(i + 1, min(i + 4, len(self.decoded_instructions))):
                inst1 = self.decoded_instructions[i]
                inst2 = self.decoded_instructions[j]
                
                # RAW (Read After Write)
                if inst1.rd is not None and inst2.rs1 is not None and inst1.rd == inst2.rs1:
                    if not with_forwarding or j - i > 1:
                        conflicts.append((i, j, ConflictType.RAW))
                if inst1.rd is not None and inst2.rs2 is not None and inst1.rd == inst2.rs2:
                    if not with_forwarding or j - i > 1:
                        conflicts.append((i, j, ConflictType.RAW))
                
                # WAW (Write After Write)
                if inst1.rd is not None and inst2.rd is not None and inst1.rd == inst2.rd:
                    conflicts.append((i, j, ConflictType.WAW))
                
                # WAR (Write After Read)
                if inst1.rs1 is not None and inst2.rd is not None and inst1.rs1 == inst2.rd:
                    conflicts.append((i, j, ConflictType.WAR))
                if inst1.rs2 is not None and inst2.rd is not None and inst1.rs2 == inst2.rd:
                    conflicts.append((i, j, ConflictType.WAR))
        
        return conflicts

    def detect_control_conflicts(self) -> List[Tuple[int, int]]:
        """Detecta conflitos de controle (branches e jumps)"""
        conflicts = []
        for i, inst in enumerate(self.decoded_instructions):
            if inst.is_branch or inst.is_jump:
                # Adiciona conflito para as próximas 2 instruções
                for j in range(i + 1, min(i + 3, len(self.decoded_instructions))):
                    conflicts.append((i, j))
        return conflicts

    def insert_nops(self, conflicts: List[Tuple[int, int, ConflictType]], 
                   with_forwarding: bool = False) -> List[int]:
        """Insere NOPs para resolver conflitos"""
        nop = 0x00000013  # addi x0, x0, 0
        result = self.original_instructions.copy()
        offset = 0
        
        for i, j, conflict_type in conflicts:
            if conflict_type == ConflictType.RAW:
                if not with_forwarding:
                    # Insere NOPs entre as instruções
                    for _ in range(j - i - 1):
                        result.insert(i + 1 + offset, nop)
                        offset += 1
            elif conflict_type == ConflictType.CONTROL:
                # Insere NOPs após branch/jump
                result.insert(i + 1 + offset, nop)
                result.insert(i + 1 + offset, nop)
                offset += 2
        
        return result

    def reorder_instructions(self, conflicts: List[Tuple[int, int, ConflictType]], 
                           with_forwarding: bool = False) -> List[int]:
        """Reordena instruções para reduzir conflitos"""
        result = self.original_instructions.copy()
        # Implementação básica - pode ser melhorada
        for i, j, conflict_type in conflicts:
            if conflict_type == ConflictType.RAW and not with_forwarding:
                # Tenta mover instruções independentes para frente
                for k in range(i + 1, j):
                    if not self._has_dependency(self.decoded_instructions[k], 
                                             self.decoded_instructions[i]):
                        result[i], result[k] = result[k], result[i]
                        break
        return result

    def _has_dependency(self, inst1: Instruction, inst2: Instruction) -> bool:
        """Verifica se há dependência entre duas instruções"""
        if inst1.rd is not None:
            if inst2.rs1 is not None and inst1.rd == inst2.rs1:
                return True
            if inst2.rs2 is not None and inst1.rd == inst2.rs2:
                return True
        if inst2.rd is not None:
            if inst1.rs1 is not None and inst2.rd == inst1.rs1:
                return True
            if inst1.rs2 is not None and inst2.rd == inst1.rs2:
                return True
        return False

    def apply_delayed_branch(self) -> List[int]:
        """Aplica a técnica de delayed branch"""
        result = []
        i = 0
        while i < len(self.original_instructions):
            inst = self.decoded_instructions[i]
            if inst.is_branch or inst.is_jump:
                # Adiciona a instrução de branch/jump
                result.append(self.original_instructions[i])
                # Tenta mover a próxima instrução útil para o slot de delay
                if i + 1 < len(self.original_instructions):
                    next_inst = self.decoded_instructions[i + 1]
                    if not self._has_dependency(next_inst, inst):
                        result.append(self.original_instructions[i + 1])
                        i += 1
                    else:
                        # Insere NOP se não for possível mover instrução útil
                        result.append(0x00000013)  # NOP
                else:
                    result.append(0x00000013)  # NOP
            else:
                result.append(self.original_instructions[i])
            i += 1
        return result

    def analyze_all_techniques(self) -> Dict[str, Tuple[List[int], int]]:
        """Analisa e aplica todas as técnicas solicitadas"""
        results = {}
        
        # 1. Sem forwarding, detectar conflitos
        data_conflicts = self.detect_data_conflicts(with_forwarding=False)
        results["1_sem_forwarding_detect"] = (self.original_instructions, len(data_conflicts))
        
        # 2. Com forwarding, detectar conflitos
        data_conflicts_fw = self.detect_data_conflicts(with_forwarding=True)
        results["2_com_forwarding_detect"] = (self.original_instructions, len(data_conflicts_fw))
        
        # 3. Sem forwarding, inserir NOPs
        nop_solution = self.insert_nops(data_conflicts, with_forwarding=False)
        results["3_sem_forwarding_nops"] = (nop_solution, len(nop_solution) - len(self.original_instructions))
        
        # 4. Com forwarding, inserir NOPs
        nop_solution_fw = self.insert_nops(data_conflicts_fw, with_forwarding=True)
        results["4_com_forwarding_nops"] = (nop_solution_fw, len(nop_solution_fw) - len(self.original_instructions))
        
        # 5. Sem forwarding, reordenar
        reordered = self.reorder_instructions(data_conflicts, with_forwarding=False)
        results["5_sem_forwarding_reorder"] = (reordered, len(reordered) - len(self.original_instructions))
        
        # 6. Com forwarding, reordenar
        reordered_fw = self.reorder_instructions(data_conflicts_fw, with_forwarding=True)
        results["6_com_forwarding_reorder"] = (reordered_fw, len(reordered_fw) - len(self.original_instructions))
        
        # 7. NOPs para conflitos de controle
        control_conflicts = self.detect_control_conflicts()
        control_nops = self.insert_nops([(i, j, ConflictType.CONTROL) for i, j in control_conflicts])
        results["7_control_nops"] = (control_nops, len(control_nops) - len(self.original_instructions))
        
        # 8. Delayed branch
        delayed = self.apply_delayed_branch()
        results["8_delayed_branch"] = (delayed, len(delayed) - len(self.original_instructions))
        
        # 9. Combinação de 4 e 6
        combined = self.insert_nops(data_conflicts_fw, with_forwarding=True)
        combined = self.reorder_instructions(data_conflicts_fw, with_forwarding=True)
        results["9_combined"] = (combined, len(combined) - len(self.original_instructions))
        
        return results 