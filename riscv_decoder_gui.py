import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from riscv_classifier import decode_instruction, read_hex_file
from pipeline_analyzer import PipelineAnalyzer
from translations import TRANSLATIONS
import os

class RiscVDecoderGUI:
    def __init__(self, root):
        self.root = root
        self.current_language = 'pt_BR'  # Idioma padrão
        self.translations = TRANSLATIONS
        self.setup_ui()

    def setup_ui(self):
        self.root.title(self.get_text('title'))
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        # Menu de idiomas
        self.create_language_menu()
        
        # Estilo
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Helvetica", 16, "bold"), padding=10)
        style.configure("Header.TLabel", font=("Helvetica", 12, "bold"), padding=5)
        style.configure("Grid.TFrame", background="white")
        
        # Título
        self.title_label = ttk.Label(
            self.root,
            text=self.get_text('title'),
            style="Title.TLabel"
        )
        self.title_label.pack(pady=10)
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Frame para entrada
        input_frame = ttk.LabelFrame(main_frame, text=self.get_text('input_frame'))
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
        self.notebook.add(decode_frame, text=self.get_text('decode_tab'))
        
        self.decode_text = scrolledtext.ScrolledText(
            decode_frame,
            height=10,
            width=50,
            font=("Courier", 10)
        )
        self.decode_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Aba de análise de pipeline
        pipeline_frame = ttk.Frame(self.notebook)
        self.notebook.add(pipeline_frame, text=self.get_text('pipeline_tab'))
        
        # Frame para grid de resultados
        grid_frame = ttk.Frame(pipeline_frame)
        grid_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Criar grid de resultados
        self.create_results_grid(grid_frame)
        
        # Barra de status
        self.status_var = tk.StringVar()
        self.status_var.set(self.get_text('ready'))
        self.status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief="sunken",
            padding=5
        )
        self.status_bar.pack(side="bottom", fill="x")
        
        # Armazenar resultados da análise
        self.analysis_results = {}

    def create_language_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        language_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Language / Idioma", menu=language_menu)
        
        language_menu.add_command(label="Português (BR)", 
                                command=lambda: self.change_language('pt_BR'))
        language_menu.add_command(label="English (US)", 
                                command=lambda: self.change_language('en_US'))

    def change_language(self, lang):
        self.current_language = lang
        self.update_ui_texts()

    def update_ui_texts(self):
        self.root.title(self.get_text('title'))
        self.title_label.config(text=self.get_text('title'))

        def update_buttons_recursive(widget):
            for child in widget.winfo_children():
                if isinstance(child, ttk.Button):
                    current_text = child.cget('text')
                    if current_text in [self.get_text('load_file', 'pt_BR'), self.get_text('load_file', 'en_US')]:
                        child.config(text=self.get_text('load_file'))
                    elif current_text in [self.get_text('decode', 'pt_BR'), self.get_text('decode', 'en_US')]:
                        child.config(text=self.get_text('decode'))
                    elif current_text in [self.get_text('analyze', 'pt_BR'), self.get_text('analyze', 'en_US')]:
                        child.config(text=self.get_text('analyze'))
                    elif current_text in [self.get_text('clear', 'pt_BR'), self.get_text('clear', 'en_US')]:
                        child.config(text=self.get_text('clear'))
                    elif current_text in [self.get_text('view', 'pt_BR'), self.get_text('view', 'en_US')]:
                        child.config(text=self.get_text('view'))
                    elif current_text in [self.get_text('save', 'pt_BR'), self.get_text('save', 'en_US')]:
                        child.config(text=self.get_text('save'))
                update_buttons_recursive(child)

        update_buttons_recursive(self.root)

        # Atualizar textos das abas
        self.notebook.tab(0, text=self.get_text('decode_tab'))
        self.notebook.tab(1, text=self.get_text('pipeline_tab'))
        
        # Atualizar cabeçalhos da grid
        grid_frame = self.notebook.winfo_children()[1].winfo_children()[0]
        headers = self.get_text('grid_headers')
        for i, header in enumerate(headers):
            for widget in grid_frame.winfo_children():
                if isinstance(widget, ttk.Label) and widget.grid_info()["row"] == 0 and widget.grid_info()["column"] == i:
                    widget.config(text=header)
        
        # Atualizar nomes das técnicas
        techniques = [
            self.get_text('techniques')['1'],
            self.get_text('techniques')['2'],
            self.get_text('techniques')['3'],
            self.get_text('techniques')['4'],
            self.get_text('techniques')['5'],
            self.get_text('techniques')['6'],
            self.get_text('techniques')['7'],
            self.get_text('techniques')['8'],
            self.get_text('techniques')['9']
        ]
        
        for i, technique in enumerate(techniques, 1):
            for widget in grid_frame.winfo_children():
                if isinstance(widget, ttk.Label) and widget.grid_info()["row"] == i and widget.grid_info()["column"] == 0:
                    widget.config(text=technique)
        
        # Atualizar status
        self.status_var.set(self.get_text('ready'))

    def get_text(self, key, lang=None):
        if lang is None:
            lang = self.current_language
        return self.translations[lang][key]

    def create_buttons(self, parent):
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill="x", pady=5)
        
        ttk.Button(
            btn_frame,
            text=self.get_text('load_file'),
            command=self.load_file
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame,
            text=self.get_text('decode'),
            command=self.decode
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame,
            text=self.get_text('analyze'),
            command=self.analyze_pipeline
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame,
            text=self.get_text('clear'),
            command=self.clear
        ).pack(side="left", padx=5)

    def create_results_grid(self, parent):
        # Cabeçalhos
        headers = self.get_text('grid_headers')
        for i, header in enumerate(headers):
            ttk.Label(
                parent,
                text=header,
                style="Header.TLabel"
            ).grid(row=0, column=i, padx=5, pady=5, sticky="w")
        
        # Linhas para cada técnica
        techniques = [
            self.get_text('techniques')['1'],
            self.get_text('techniques')['2'],
            self.get_text('techniques')['3'],
            self.get_text('techniques')['4'],
            self.get_text('techniques')['5'],
            self.get_text('techniques')['6'],
            self.get_text('techniques')['7'],
            self.get_text('techniques')['8'],
            self.get_text('techniques')['9']
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
            text=self.get_text('view'),
            command=lambda: self.view_technique(row-1)
        ).pack(side="left", padx=2)
        
        ttk.Button(
            frame,
            text=self.get_text('save'),
            command=lambda: self.save_technique(row-1)
        ).pack(side="left", padx=2)

    def load_file(self):
        filename = filedialog.askopenfilename(
            title=self.get_text('load_file'),
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            instructions = read_hex_file(filename)
            if instructions:
                self.input_text.delete(1.0, tk.END)
                for instruction in instructions:
                    self.input_text.insert(tk.END, f"{instruction:08X}\n")
                self.status_var.set(self.get_text('file_loaded').format(filename))
            else:
                self.status_var.set(self.get_text('file_error'))

    def decode(self):
        try:
            self.decode_text.delete(1.0, tk.END)
            input_text = self.input_text.get(1.0, tk.END).strip()
            
            if not input_text:
                self.status_var.set(self.get_text('empty_input'))
                return
            
            instructions = []
            for line in input_text.split('\n'):
                if line.strip():
                    instruction = int(line.strip(), 16)
                    instructions.append(instruction)
            
            self.decode_text.insert(tk.END, f"{self.get_text('decode_tab')}:\n")
            self.decode_text.insert(tk.END, "=" * 70 + "\n")
            
            for i, instruction in enumerate(instructions):
                info = decode_instruction(instruction)
                formatted_info = self.format_instruction_info(info)
                self.decode_text.insert(
                    tk.END,
                    f"Instrução {i+1}: 0x{instruction:08X} ->\n{formatted_info}\n\n"
                )
            
            self.status_var.set(self.get_text('decode_success'))
            
        except ValueError as e:
            self.status_var.set(self.get_text('invalid_hex'))
        except Exception as e:
            self.status_var.set(self.get_text('decode_error').format(str(e)))

    def analyze_pipeline(self):
        try:
            input_text = self.input_text.get(1.0, tk.END).strip()
            
            if not input_text:
                self.status_var.set(self.get_text('analysis_empty'))
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
                overhead_label.config(text=f"{overhead} {self.get_text('instructions')}")
            
            self.status_var.set(self.get_text('analysis_success'))
            
        except Exception as e:
            self.status_var.set(self.get_text('analysis_error').format(str(e)))

    def get_grid_label(self, row, col):
        # Encontra o widget na posição específica do grid
        for widget in self.notebook.winfo_children()[1].winfo_children()[0].winfo_children():
            if isinstance(widget, ttk.Label) and widget.grid_info()["row"] == row + 1 and widget.grid_info()["column"] == col:
                return widget
        return None

    def view_technique(self, index):
        if not self.analysis_results:
            messagebox.showwarning(
                self.get_text('warning'),
                self.get_text('run_analysis_first')
            )
            return
        
        technique = list(self.analysis_results.keys())[index]
        instructions, overhead = self.analysis_results[technique]
        
        # Cria uma nova janela para visualização
        view_window = tk.Toplevel(self.root)
        view_window.title(f"{self.get_text('view')} - {technique}")
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
        text_area.insert(tk.END, f"{self.get_text('technique')}: {technique}\n")
        text_area.insert(tk.END, f"{self.get_text('overhead')}: {overhead} {self.get_text('instructions')}\n")
        text_area.insert(tk.END, "=" * 50 + "\n\n")
        
        for i, inst in enumerate(instructions):
            text_area.insert(tk.END, f"{i+1}: 0x{inst:08X}\n")
        
        text_area.config(state="disabled")

    def save_technique(self, index):
        if not self.analysis_results:
            messagebox.showwarning(
                self.get_text('warning'),
                self.get_text('run_analysis_first')
            )
            return
        
        technique = list(self.analysis_results.keys())[index]
        instructions, overhead = self.analysis_results[technique]
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[(self.get_text('text_files'), "*.txt")],
            title=f"{self.get_text('save_result')} - {technique}"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(f"{self.get_text('technique')}: {technique}\n")
                    f.write(f"{self.get_text('overhead')}: {overhead} {self.get_text('instructions')}\n")
                    f.write("=" * 50 + "\n\n")
                    for i, inst in enumerate(instructions):
                        f.write(f"{i+1}: 0x{inst:08X}\n")
                self.status_var.set(self.get_text('file_saved').format(filename))
            except Exception as e:
                messagebox.showerror(
                    self.get_text('error'),
                    self.get_text('save_error').format(str(e))
                )

    def format_instruction_info(self, info):
        """Formata a informação da instrução para exibição"""
        base = self.get_text('instruction_format').format(info['tipo'].lower())
        
        if 'rd' in info:
            base += f", {self.get_text('register_dest').format(info['rd'])}"
        if 'funct3' in info:
            base += f", {self.get_text('function3').format(info['funct3'])}"
        if 'rs1' in info:
            base += f", {self.get_text('register_src1').format(info['rs1'])}"
        if 'rs2' in info:
            base += f", {self.get_text('register_src2').format(info['rs2'])}"
        if 'imm' in info:
            base += f", {self.get_text('immediate').format(info['imm'])}"
        if 'funct7' in info:
            base += f", {self.get_text('function7').format(info['funct7'])}"
        
        return base

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
        
        self.status_var.set(self.get_text('areas_cleared'))

def main():
    root = tk.Tk()
    app = RiscVDecoderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 