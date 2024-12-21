import os
import subprocess
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import re

class CCompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("C Compiler GUI")
        self.root.geometry("900x700")

        self.compiler_dir = os.getcwd()  # Default to current working directory
        self.selected_file = None

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Create a top frame for file selection and buttons
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=15, fill=tk.X)

        self.file_label = tk.Label(top_frame, text="No file selected", width=40, anchor='w', font=('Arial', 12))
        self.file_label.pack(side=tk.LEFT, padx=10)

        select_button = tk.Button(top_frame, text="Select C File", command=self.select_file, width=15, bg="#4CAF50", fg="white")
        select_button.pack(side=tk.LEFT, padx=10)

        compile_button = tk.Button(top_frame, text="Compile and Run", command=self.compile_and_run, width=15, bg="#2196F3", fg="white")
        compile_button.pack(side=tk.LEFT, padx=10)

        visualize_button = tk.Button(top_frame, text="Visualize", command=self.visualize, width=15, bg="#FF5722", fg="white")
        visualize_button.pack(side=tk.LEFT, padx=10)

        show_input_button = tk.Button(top_frame, text="Show Input", command=self.show_input, width=15, bg="#9C27B0", fg="white")
        show_input_button.pack(side=tk.LEFT, padx=10)

        # Tabbed interface for output areas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create the tabs
        self.input_code_tab = ttk.Frame(self.notebook)
        self.tokens_tab = ttk.Frame(self.notebook)
        self.parse_tree_tab = ttk.Frame(self.notebook)
        self.output_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.input_code_tab, text="Input Code")
        self.notebook.add(self.tokens_tab, text="Tokens")
        self.notebook.add(self.parse_tree_tab, text="Parse Tree")
        self.notebook.add(self.output_tab, text="Output")

        # Add ScrolledText widget to each tab for output display
        self.input_code_text = scrolledtext.ScrolledText(self.input_code_tab, wrap=tk.WORD, height=15, font=('Courier', 10))
        self.input_code_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.tokens_text = scrolledtext.ScrolledText(self.tokens_tab, wrap=tk.WORD, height=15, font=('Courier', 10))
        self.tokens_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.parse_tree_text = scrolledtext.ScrolledText(self.parse_tree_tab, wrap=tk.WORD, height=15, font=('Courier', 10))
        self.parse_tree_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.output_text = scrolledtext.ScrolledText(self.output_tab, wrap=tk.WORD, height=5, font=('Courier', 10))
        self.output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("C Files", "*.c")])
        if file_path:
            self.file_label.config(text=os.path.basename(file_path))
            self.selected_file = file_path

    def show_input(self):
        if not self.selected_file:
            messagebox.showerror("Error", "No C file selected.")
            return

        try:
            with open(self.selected_file, 'r') as f:
                code = f.read()
            self.input_code_text.delete(1.0, tk.END)
            self.input_code_text.insert(tk.END, code)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

    def compile_and_run(self):
        if not self.selected_file:
            messagebox.showerror("Error", "No C file selected.")
            return

        # Run the compiler
        try:
            output_file = os.path.splitext(self.selected_file)[0]  # Get output file name without extension
            result = subprocess.run(
                ["gcc", self.selected_file, "-o", output_file],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                # Run the compiled executable
                run_result = subprocess.run(
                    [output_file], capture_output=True, text=True
                )
                output = run_result.stdout
            else:
                output = result.stderr

            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, output)
        except Exception as e:
            messagebox.showerror("Error", f"Compilation or execution failed: {e}")

    def visualize(self):
        if not self.selected_file:
            messagebox.showerror("Error", "No C file selected.")
            return

        try:
            with open(self.selected_file, 'r') as f:
                code = f.read()

            # Tokenize the code
            tokens, token_types = self.tokenize_code(code)

            # Build a detailed parse tree
            parse_tree = self.build_parse_tree(tokens)

            # Clear previous content in text areas
            self.tokens_text.delete(1.0, tk.END)
            self.parse_tree_text.delete(1.0, tk.END)

            # Display tokens and token types
            token_str = "\n".join([f"{token} -> {token_type}" for token, token_type in zip(tokens, token_types)])
            self.tokens_text.insert(tk.END, token_str)

            # Display parse tree
            parse_tree_str = self.render_parse_tree(parse_tree)
            self.parse_tree_text.insert(tk.END, parse_tree_str)

        except Exception as e:
            messagebox.showerror("Error", f"Visualization failed: {e}")

    def tokenize_code(self, code):
        keywords = {'int', 'float', 'if', 'else', 'while', 'return'}
        operators = {'+', '-', '*', '/', '=', '==', '<', '>', '&&', '||', '++', '--'}
        delimiters = {';', '{', '}', '(', ')', ','}
        data_types = {'int', 'float', 'char', 'void'}

        tokens = []
        token_types = []

        token_pattern = r"\w+|[+\-*/=><!&|]+|\d+|[;{}(),]"
        matches = re.findall(token_pattern, code)

        for match in matches:
            if match in keywords:
                tokens.append(match)
                token_types.append("Keyword")
            elif match in operators:
                tokens.append(match)
                token_types.append("Operator")
            elif match in delimiters:
                tokens.append(match)
                token_types.append("Delimiter")
            elif match.isdigit():
                tokens.append(match)
                token_types.append("Literal")
            elif match in data_types:
                tokens.append(match)
                token_types.append("Data Type")
            else:
                tokens.append(match)
                token_types.append("Identifier")

        return tokens, token_types

    def build_parse_tree(self, tokens):
        parse_tree = {"Program": {"Declarations and Statements": []}}
        current_function = None

        for token in tokens:
            if token == "main":
                current_function = {"Function": "main", "Body": []}
                parse_tree["Program"]["Declarations and Statements"].append(current_function)
            elif token == "return":
                current_function["Body"].append({"Return Statement": tokens[tokens.index(token) + 1]})
            elif token == "++" or token == "--":
                variable = tokens[tokens.index(token) - 1]
                operation = "Increment" if token == "++" else "Decrement"
                current_function["Body"].append({operation: variable})
            elif token == "=":
                variable = tokens[tokens.index(token) - 1]
                value = tokens[tokens.index(token) + 1]
                current_function["Body"].append({"Assignment": {"Variable": variable, "Value": value}})

        return parse_tree

    def render_parse_tree(self, tree, level=0):
        tree_str = ""
        if isinstance(tree, list):
            for item in tree:
                tree_str += self.render_parse_tree(item, level)
        elif isinstance(tree, dict):
            for key, value in tree.items():
                tree_str += "  " * level + f"{key}:\n"
                tree_str += self.render_parse_tree(value, level + 1)
        else:
            tree_str += "  " * level + f"{tree}\n"
        return tree_str

if __name__ == "__main__":
    root = tk.Tk()
    app = CCompilerGUI(root)
    root.mainloop()
