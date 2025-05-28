# Decodificador e Analisador de Pipeline RISC-V / RISC-V Decoder and Pipeline Analyzer

---

## Português (BR)

Este programa decodifica instruções RISC-V e analisa conflitos no pipeline, oferecendo diferentes técnicas para otimização. Agora, a interface é totalmente bilíngue (Português e Inglês), podendo ser alternada pelo menu "Language / Idioma".

### Funcionalidades
- **Decodificação de instruções**: Identifica o tipo e os campos de cada instrução RISC-V.
- **Análise de pipeline**: Detecta e trata conflitos de dados e controle, simulando diferentes técnicas de otimização.
- **Interface gráfica amigável**: Permite entrada manual ou por arquivo, visualização e exportação dos resultados.
- **Suporte bilíngue**: Todos os textos, botões e mensagens podem ser alternados entre português e inglês.

### Como usar
1. Execute o programa:
   ```
   python riscv_decoder_gui.py
   ```
2. Escolha o idioma no menu "Language / Idioma".
3. Insira instruções em hexadecimal manualmente ou carregue um arquivo `.txt`.
4. Use as abas para alternar entre:
   - **Decodificação**: Mostra o detalhamento de cada instrução.
   - **Análise de Pipeline**: Mostra os resultados das técnicas de otimização.
5. Clique em "Decodificar" para ver a decodificação.
6. Clique em "Analisar Pipeline" para ver os resultados das análises.
7. Use "Limpar" para resetar as áreas de texto.

### Decodificação
- Identifica o tipo da instrução (R, I, S, B, U, J)
- Extrai campos: opcode, rd, rs1, rs2, funct3, funct7, imediato
- Exibe os campos de forma legível

### Análise de Pipeline
O programa implementa as seguintes técnicas:
1. Detecção de conflitos sem forwarding
2. Detecção de conflitos com forwarding
3. Inserção de NOPs sem forwarding
4. Inserção de NOPs com forwarding
5. Reordenação de instruções sem forwarding
6. Reordenação de instruções com forwarding
7. NOPs para conflitos de controle
8. Delayed branch
9. Combinação de técnicas 4 e 6

Cada técnica mostra o número de conflitos/sobrecusto e permite visualizar ou exportar o resultado.

### Requisitos
- Python 3.x
- tkinter (incluso no Python padrão)

### Formato do arquivo de entrada
Uma instrução hexadecimal por linha, exemplo:
```
00500413
00100093
```

### Campos decodificados por tipo de instrução

#### Tipo R
- opcode (bits 0-6)
- rd (bits 7-11)
- funct3 (bits 12-14)
- rs1 (bits 15-19)
- rs2 (bits 20-24)
- funct7 (bits 25-31)

#### Tipo I
- opcode (bits 0-6)
- rd (bits 7-11)
- funct3 (bits 12-14)
- rs1 (bits 15-19)
- imediato (bits 20-31)

#### Tipo S
- opcode (bits 0-6)
- imediato[4:0] (bits 7-11)
- funct3 (bits 12-14)
- rs1 (bits 15-19)
- rs2 (bits 20-24)
- imediato[11:5] (bits 25-31)

#### Tipo B
- opcode (bits 0-6)
- imediato[11,4:1] (bits 7-11)
- funct3 (bits 12-14)
- rs1 (bits 15-19)
- rs2 (bits 20-24)
- imediato[12,10:5] (bits 25-31)

#### Tipo U
- opcode (bits 0-6)
- rd (bits 7-11)
- imediato[31:12] (bits 12-31)

#### Tipo J
- opcode (bits 0-6)
- rd (bits 7-11)
- imediato[20,10:1,11,19:12] (bits 12-31)

---

## English (US)

This program decodes RISC-V instructions and analyzes pipeline hazards, offering several optimization techniques. The interface is fully bilingual (Portuguese and English), and you can switch languages via the "Language / Idioma" menu.

### Features
- **Instruction decoding**: Identifies the type and fields of each RISC-V instruction.
- **Pipeline analysis**: Detects and handles data/control hazards, simulating various optimization techniques.
- **User-friendly GUI**: Allows manual or file input, result visualization, and export.
- **Bilingual support**: All texts, buttons, and messages can be switched between Portuguese and English.

### How to use
1. Run the program:
   ```
   python riscv_decoder_gui.py
   ```
2. Choose the language in the "Language / Idioma" menu.
3. Enter hexadecimal instructions manually or load a `.txt` file.
4. Use the tabs to switch between:
   - **Decoding**: Shows detailed information for each instruction.
   - **Pipeline Analysis**: Shows the results of optimization techniques.
5. Click "Decode" to see the decoding.
6. Click "Analyze Pipeline" to see the analysis results.
7. Use "Clear" to reset the text areas.

### Decoding
- Identifies the instruction type (R, I, S, B, U, J)
- Extracts fields: opcode, rd, rs1, rs2, funct3, funct7, immediate
- Displays fields in a readable format

### Pipeline Analysis
The program implements the following techniques:
1. Hazard detection without forwarding
2. Hazard detection with forwarding
3. NOP insertion without forwarding
4. NOP insertion with forwarding
5. Instruction reordering without forwarding
6. Instruction reordering with forwarding
7. NOPs for control hazards
8. Delayed branch
9. Combination of techniques 4 and 6

Each technique shows the number of hazards/overhead and allows you to view or export the result.

### Requirements
- Python 3.x
- tkinter (included in standard Python)

### Input file format
One hexadecimal instruction per line, e.g.:
```
00500413
00100093
```

### Decoded fields by instruction type

#### R Type
- opcode (bits 0-6)
- rd (bits 7-11)
- funct3 (bits 12-14)
- rs1 (bits 15-19)
- rs2 (bits 20-24)
- funct7 (bits 25-31)

#### I Type
- opcode (bits 0-6)
- rd (bits 7-11)
- funct3 (bits 12-14)
- rs1 (bits 15-19)
- immediate (bits 20-31)

#### S Type
- opcode (bits 0-6)
- immediate[4:0] (bits 7-11)
- funct3 (bits 12-14)
- rs1 (bits 15-19)
- rs2 (bits 20-24)
- immediate[11:5] (bits 25-31)

#### B Type
- opcode (bits 0-6)
- immediate[11,4:1] (bits 7-11)
- funct3 (bits 12-14)
- rs1 (bits 15-19)
- rs2 (bits 20-24)
- immediate[12,10:5] (bits 25-31)

#### U Type
- opcode (bits 0-6)
- rd (bits 7-11)
- immediate[31:12] (bits 12-31)

#### J Type
- opcode (bits 0-6)
- rd (bits 7-11)
- immediate[20,10:1,11,19:12] (bits 12-31) 