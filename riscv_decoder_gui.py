import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from riscv_classifier import decode_instruction, read_hex_file
from pipeline_analyzer import PipelineAnalyzer
import os

class RiscVDecoderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Decodificador e Analisador RISC-V")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        # Estilo
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Helvetica", 16, "bold"), padding=10)
        style.configure("Header.TLabel", font=("Helvetica", 12, "bold"), padding=5)
        style.configure("Grid.TFrame", background="white")
        
        # Título
        title = ttk.Label(
            root,
            text="Decodificador e Analisador de Pipeline RISC-V",
            style="Title.TLabel"
        )
        title.pack(pady=10)
        
        # Frame principal
        main_frame = ttk.Frame(root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Frame para entrada
        input_frame = ttk.LabelFrame(main_frame, text="Entrada (Instruções em Hexadecimal)")
        input_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Botões
        self.create_buttons(input_frame)
        
        # Área de texto para entrada manual
        self.input_text = scrolledtext.ScrolledText(
            input_frame,
            height=5,
            width=50,
            font=("Courier", 10)
        )
        self.input_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Notebook para diferentes visualizações
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Aba de decodificação
        decode_frame = ttk.Frame(self.notebook)
        self.notebook.add(decode_frame, text="Decodificação")
        
        self.decode_text = scrolledtext.ScrolledText(
            decode_frame,
            height=10,
            width=50,
            font=("Courier", 10)
        )
        self.decode_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Aba de análise de pipeline
        pipeline_frame = ttk.Frame(self.notebook)
        self.notebook.add(pipeline_frame, text="Análise de Pipeline")
        
        # Frame para grid de resultados
        grid_frame = ttk.Frame(pipeline_frame)
        grid_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Criar grid de resultados
        self.create_results_grid(grid_frame)
        
        # Barra de status
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto para decodificar instruções")
        self.status_bar = ttk.Label(
            root,
            textvariable=self.status_var,
            relief="sunken",
            padding=5
        )
        self.status_bar.pack(side="bottom", fill="x")
        
        # Armazenar resultados da análise
        self.analysis_results = {}

    def create_buttons(self, parent):
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill="x", pady=5)
        
        ttk.Button(
            btn_frame,
            text="Carregar Arquivo",
            command=self.load_file
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame,
            text="Decodificar",
            command=self.decode
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame,
            text="Analisar Pipeline",
            command=self.analyze_pipeline
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame,
            text="Limpar",
            command=self.clear
        ).pack(side="left", padx=5)

    def create_results_grid(self, parent):
        # Cabeçalhos
        headers = ["Técnica", "Conflitos", "Sobrecusto", "Ações"]
        for i, header in enumerate(headers):
            ttk.Label(
                parent,
                text=header,
                style="Header.TLabel"
            ).grid(row=0, column=i, padx=5, pady=5, sticky="w")
        
        # Linhas para cada técnica
        techniques = [
            "1. Sem forwarding (detectar)",
            "2. Com forwarding (detectar)",
            "3. Sem forwarding (NOPs)",
            "4. Com forwarding (NOPs)",
            "5. Sem forwarding (reordenar)",
            "6. Com forwarding (reordenar)",
            "7. NOPs para controle",
            "8. Delayed branch",
            "9. Combinação 4+6"
        ]
        
        for i, technique in enumerate(techniques, 1):
            # Nome da técnica
            ttk.Label(
                parent,
                text=technique
            ).grid(row=i, column=0, padx=5, pady=2, sticky="w")
            
            # Conflitos
            self.create_conflicts_label(parent, i, 1)
            
            # Sobrecusto
            self.create_overhead_label(parent, i, 2)
            
            # Botões de ação
            self.create_action_buttons(parent, i, 3)

    def create_conflicts_label(self, parent, row, col):
        label = ttk.Label(parent, text="")
        label.grid(row=row, column=col, padx=5, pady=2, sticky="w")
        return label

    def create_overhead_label(self, parent, row, col):
        label = ttk.Label(parent, text="")
        label.grid(row=row, column=col, padx=5, pady=2, sticky="w")
        return label

    def create_action_buttons(self, parent, row, col):
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=col, padx=5, pady=2, sticky="w")
        
        ttk.Button(
            frame,
            text="Ver",
            command=lambda: self.view_technique(row-1)
        ).pack(side="left", padx=2)
        
        ttk.Button(
            frame,
            text="Salvar",
            command=lambda: self.save_technique(row-1)
        ).pack(side="left", padx=2)

    def load_file(self):
        filename = filedialog.askopenfilename(
            title="Selecione o arquivo de instruções",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        if filename:
            instructions = read_hex_file(filename)
            if instructions:
                self.input_text.delete(1.0, tk.END)
                for instruction in instructions:
                    self.input_text.insert(tk.END, f"{instruction:08X}\n")
                self.status_var.set(f"Arquivo carregado: {filename}")
            else:
                self.status_var.set("Erro ao carregar o arquivo")

    def decode(self):
        try:
            self.decode_text.delete(1.0, tk.END)
            input_text = self.input_text.get(1.0, tk.END).strip()
            
            if not input_text:
                self.status_var.set("Por favor, insira algumas instruções para decodificar")
                return
            
            instructions = []
            for line in input_text.split('\n'):
                if line.strip():
                    instruction = int(line.strip(), 16)
                    instructions.append(instruction)
            
            self.decode_text.insert(tk.END, "Decodificação das instruções:\n")
            self.decode_text.insert(tk.END, "=" * 70 + "\n")
            
            for i, instruction in enumerate(instructions):
                info = decode_instruction(instruction)
                formatted_info = self.format_instruction_info(info)
                self.decode_text.insert(
                    tk.END,
                    f"Instrução {i+1}: 0x{instruction:08X} ->\n{formatted_info}\n\n"
                )
            
            self.status_var.set("Decodificação concluída com sucesso")
            
        except ValueError as e:
            self.status_var.set("Erro: Formato hexadecimal inválido")
        except Exception as e:
            self.status_var.set(f"Erro durante a decodificação: {str(e)}")

    def analyze_pipeline(self):
        try:
            input_text = self.input_text.get(1.0, tk.END).strip()
            
            if not input_text:
                self.status_var.set("Por favor, insira algumas instruções para analisar")
                return
            
            instructions = []
            for line in input_text.split('\n'):
                if line.strip():
                    instruction = int(line.strip(), 16)
                    instructions.append(instruction)
            
            analyzer = PipelineAnalyzer(instructions)
            self.analysis_results = analyzer.analyze_all_techniques()
            
            # Atualiza o grid com os resultados
            for i, (technique, (modified_instructions, overhead)) in enumerate(self.analysis_results.items()):
                # Atualiza labels de conflitos e sobrecusto
                conflicts_label = self.get_grid_label(i, 1)
                overhead_label = self.get_grid_label(i, 2)
                
                conflicts_label.config(text=str(len(modified_instructions) - len(instructions)))
                overhead_label.config(text=f"{overhead} instruções")
            
            self.status_var.set("Análise de pipeline concluída com sucesso")
            
        except Exception as e:
            self.status_var.set(f"Erro durante a análise: {str(e)}")

    def get_grid_label(self, row, col):
        # Encontra o widget na posição específica do grid
        for widget in self.notebook.winfo_children()[1].winfo_children()[0].winfo_children():
            if isinstance(widget, ttk.Label) and widget.grid_info()["row"] == row + 1 and widget.grid_info()["column"] == col:
                return widget
        return None

    def view_technique(self, index):
        if not self.analysis_results:
            messagebox.showwarning("Aviso", "Execute a análise primeiro")
            return
        
        technique = list(self.analysis_results.keys())[index]
        instructions, overhead = self.analysis_results[technique]
        
        # Cria uma nova janela para visualização
        view_window = tk.Toplevel(self.root)
        view_window.title(f"Visualização - {technique}")
        view_window.geometry("600x400")
        
        # Área de texto para mostrar as instruções
        text_area = scrolledtext.ScrolledText(
            view_window,
            width=70,
            height=20,
            font=("Courier", 10)
        )
        text_area.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Insere as instruções
        text_area.insert(tk.END, f"Técnica: {technique}\n")
        text_area.insert(tk.END, f"Sobrecusto: {overhead} instruções\n")
        text_area.insert(tk.END, "=" * 50 + "\n\n")
        
        for i, inst in enumerate(instructions):
            text_area.insert(tk.END, f"{i+1}: 0x{inst:08X}\n")
        
        text_area.config(state="disabled")

    def save_technique(self, index):
        if not self.analysis_results:
            messagebox.showwarning("Aviso", "Execute a análise primeiro")
            return
        
        technique = list(self.analysis_results.keys())[index]
        instructions, overhead = self.analysis_results[technique]
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de texto", "*.txt")],
            title=f"Salvar resultado - {technique}"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(f"Técnica: {technique}\n")
                    f.write(f"Sobrecusto: {overhead} instruções\n")
                    f.write("=" * 50 + "\n\n")
                    for i, inst in enumerate(instructions):
                        f.write(f"{i+1}: 0x{inst:08X}\n")
                self.status_var.set(f"Arquivo salvo: {filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar arquivo: {str(e)}")

    def format_instruction_info(self, info):
        lines = [
            f"  Tipo: {info['tipo']}",
            f"  Opcode: 0x{info['opcode']:02X}",
        ]
        
        if 'rd' in info:
            lines.append(f"  Registrador Destino (rd): x{info['rd']}")
        if 'funct3' in info:
            lines.append(f"  Funct3: {info['funct3']}")
        if 'rs1' in info:
            lines.append(f"  Registrador Fonte 1 (rs1): x{info['rs1']}")
        if 'rs2' in info:
            lines.append(f"  Registrador Fonte 2 (rs2): x{info['rs2']}")
        if 'imm' in info:
            lines.append(f"  Imediato: {info['imm']}")
        if 'funct7' in info:
            lines.append(f"  Funct7: {info['funct7']}")
        
        return "\n".join(lines)

    def clear(self):
        self.input_text.delete(1.0, tk.END)
        self.decode_text.delete(1.0, tk.END)
        self.analysis_results = {}
        
        # Limpa os labels do grid
        for i in range(9):
            conflicts_label = self.get_grid_label(i, 1)
            overhead_label = self.get_grid_label(i, 2)
            if conflicts_label:
                conflicts_label.config(text="")
            if overhead_label:
                overhead_label.config(text="")
        
        self.status_var.set("Áreas de texto limpas")

def main():
    root = tk.Tk()
    app = RiscVDecoderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 