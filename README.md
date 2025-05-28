# Decodificador e Analisador de Pipeline RISC-V

Este programa decodifica instruções RISC-V e analisa conflitos no pipeline, oferecendo diferentes técnicas para otimização. O programa suporta os seguintes tipos de instrução:
- Tipo R (operações entre registradores)
- Tipo I (operações imediatas e loads)
- Tipo S (stores)
- Tipo B (branches)
- Tipo U (upper immediate)
- Tipo J (jumps)

## Versões do Programa

### Interface Gráfica (GUI)
Execute `riscv_decoder_gui.py` para usar a versão com interface gráfica. Esta versão oferece:
- Interface amigável e intuitiva
- Carregamento de arquivos através de diálogo
- Entrada manual de instruções
- Visualização formatada dos resultados
- Barra de status com feedback
- Botões para carregar arquivo, decodificar e limpar

### Linha de Comando (CLI)
Execute `riscv_classifier.py` para usar a versão em linha de comando.

## Funcionalidades

### Decodificação
- Identifica o tipo da instrução baseado no opcode
- Extrai todos os campos relevantes para cada tipo de instrução:
  - rd (registrador destino)
  - rs1, rs2 (registradores fonte)
  - funct3, funct7 (campos de função)
  - imediato (valor imediato, formatado de acordo com o tipo da instrução)

### Análise de Pipeline
O programa implementa as seguintes técnicas de otimização:

1. Detecção de conflitos sem forwarding
2. Detecção de conflitos com forwarding
3. Inserção de NOPs sem forwarding
4. Inserção de NOPs com forwarding
5. Reordenação de instruções sem forwarding
6. Reordenação de instruções com forwarding
7. NOPs para conflitos de controle
8. Delayed branch
9. Combinação de técnicas 4 e 6

## Requisitos
- Python 3.x
- tkinter (incluído na instalação padrão do Python)

## Como usar a Interface Gráfica
1. Execute o programa:
   ```
   python riscv_decoder_gui.py
   ```
2. Use uma das opções:
   - Clique em "Carregar Arquivo" para selecionar um arquivo de instruções
   - Digite as instruções hexadecimais diretamente na área de texto
3. Use as abas para alternar entre:
   - Decodificação: mostra a decodificação detalhada das instruções
   - Análise de Pipeline: mostra os resultados das diferentes técnicas de otimização
4. Clique em "Decodificar" para ver a decodificação
5. Clique em "Analisar Pipeline" para ver as análises de conflitos e otimizações
6. Use "Limpar" para resetar as áreas de texto

## Como usar a Versão CLI
1. Prepare um arquivo de texto contendo as instruções em hexadecimal (uma por linha)
2. Execute o programa:
   ```
   python riscv_classifier.py
   ```
3. Digite o nome do arquivo quando solicitado

## Formato do arquivo de entrada
O arquivo de entrada deve conter uma instrução hexadecimal por linha, por exemplo:
```
00500413
00100093
```

## Exemplo de saída da análise de pipeline
```
Análise de Pipeline:
======================================================================

Técnica: 1_sem_forwarding_detect
Sobrecusto: 0 instruções
Instruções modificadas:
  1: 0x00500413
  2: 0x00100093
...

Técnica: 2_com_forwarding_detect
Sobrecusto: 0 instruções
Instruções modificadas:
  1: 0x00500413
  2: 0x00100093
...

--------------------------------------------------
```

## Campos decodificados por tipo de instrução

### Tipo R
- opcode (bits 0-6)
- rd (bits 7-11)
- funct3 (bits 12-14)
- rs1 (bits 15-19)
- rs2 (bits 20-24)
- funct7 (bits 25-31)

### Tipo I
- opcode (bits 0-6)
- rd (bits 7-11)
- funct3 (bits 12-14)
- rs1 (bits 15-19)
- imediato (bits 20-31)

### Tipo S
- opcode (bits 0-6)
- imediato[4:0] (bits 7-11)
- funct3 (bits 12-14)
- rs1 (bits 15-19)
- rs2 (bits 20-24)
- imediato[11:5] (bits 25-31)

### Tipo B
- opcode (bits 0-6)
- imediato[11,4:1] (bits 7-11)
- funct3 (bits 12-14)
- rs1 (bits 15-19)
- rs2 (bits 20-24)
- imediato[12,10:5] (bits 25-31)

### Tipo U
- opcode (bits 0-6)
- rd (bits 7-11)
- imediato[31:12] (bits 12-31)

### Tipo J
- opcode (bits 0-6)
- rd (bits 7-11)
- imediato[20,10:1,11,19:12] (bits 12-31) 