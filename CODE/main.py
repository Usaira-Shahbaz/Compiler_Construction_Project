import tkinter as tk
from tkinter import scrolledtext, messagebox
from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from code_generator import CodeGenerator
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
import os
import time

# Global variable to keep track of saved code history
CODE_HISTORY_FILE = "code_history.txt"

def run_code():
    """Handles the code execution and displays output or errors."""
    code = code_editor.get("1.0", tk.END).strip()
    
    # Enhanced input validation
    if not code:
        messagebox.showwarning("No Code Entered", "Please enter some code to run.")
        return
    
    # Add more checks to ensure valid code (e.g., basic syntax check)
    if not any(char.isalpha() for char in code):  # Simple check: code should have alphabets
        messagebox.showwarning("Invalid Code", "The code should contain some valid expressions or identifiers.")
        return

    try:
        # Lexical Analysis
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        lexer_output.config(state=tk.NORMAL)
        lexer_output.delete("1.0", tk.END)

        for token in tokens:
            # Apply blue color for keywords
            if token[0] in ["ADD", "SUB", "MUL", "DIV", "MOD", "POW", "LOG", "SIN", "COS", "TAN", "VAR", "PRINT"]:
                lexer_output.insert(tk.END, str(token) + "\n", "keyword")
            else:
                lexer_output.insert(tk.END, str(token) + "\n")
        lexer_output.config(state=tk.DISABLED)

        # Syntax Analysis
        parser = Parser(tokens)
        ast = parser.parse()
        parser_output.config(state=tk.NORMAL)
        parser_output.delete("1.0", tk.END)
        parser_output.insert(tk.END, str(ast))
        parser_output.config(state=tk.DISABLED)

        # Generate Parse Tree
        dot_tree = parser.generate_dot_tree(ast)
        dot_tree.attr(bgcolor="lightblue", style="filled")
        dot_tree.attr('node', style='filled', color='lightgoldenrodyellow')
        dot_tree.render("parse_tree", format="png", cleanup=True)
        display_parse_tree()

        # Semantic Analysis
        semantic_analyzer = SemanticAnalyzer(ast)
        semantic_analyzer.analyze()
        semantic_output.config(state=tk.NORMAL)
        semantic_output.delete("1.0", tk.END)
        semantic_output.insert(tk.END, "Semantic analysis passed successfully!")
        semantic_output.config(state=tk.DISABLED)

        # Code Generation
        generator = CodeGenerator()
        result = generator.execute(ast)
        tac_output = generator.get_tac()
        assembly_output = generator.get_assembly()

        # Display TAC and Assembly Code
        codegen_output.config(state=tk.NORMAL)
        codegen_output.delete("1.0", tk.END)
        codegen_output.insert(tk.END, f"Three-Address Code:\n{tac_output}\n\nAssembly Code:\n{assembly_output}")
        codegen_output.config(state=tk.DISABLED)

        # Display final output in the output section
        output_section.config(state=tk.NORMAL)
        output_section.delete("1.0", tk.END)
        output_section.insert(tk.END, f"Output:\n{result}")
        output_section.config(state=tk.DISABLED)

        # Save the code to history after each run
        save_code_to_history(code)

    except Exception as e:
        error_message = f"Error: {str(e)}"
        
        lexer_output.config(state=tk.NORMAL)
        lexer_output.insert(tk.END, error_message, "error")
        lexer_output.config(state=tk.DISABLED)

def save_code_to_history(code):
    """Saves the code to a history file."""
    if not os.path.exists(CODE_HISTORY_FILE):
        with open(CODE_HISTORY_FILE, "w") as history_file:
            history_file.write("Code History\n")
    with open(CODE_HISTORY_FILE, "a") as history_file:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        history_file.write(f"--- {timestamp} ---\n")
        history_file.write(code + "\n\n")

def display_parse_tree():
    """Displays the generated parse tree in the GUI."""
    tree_window = tk.Toplevel(app)
    tree_window.title("Parse Tree Visualization")
    tree_canvas = tk.Canvas(tree_window, bg="white", width=800, height=600)
    tree_canvas.pack(fill=tk.BOTH, expand=True)

    tree_img = tk.PhotoImage(file="parse_tree.png")
    tree_canvas.image = tree_img  # Keep a reference to avoid garbage collection
    tree_canvas.create_image(10, 10, anchor=tk.NW, image=tree_img)

def save_code():
    """Saves the code from the editor to a file."""
    code = code_editor.get("1.0", tk.END).strip()
    if not code:
        messagebox.showwarning("No Code", "There is no code to save.")
        return

    file_path = asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(code)
        messagebox.showinfo("Success", f"Code saved to {file_path}")

def load_code():
    """Loads code from an external file."""
    file_path = askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            code = file.read()
        code_editor.delete("1.0", tk.END)
        code_editor.insert(tk.END, code)
        messagebox.showinfo("Success", f"Code loaded from {file_path}")

def reset_code():
    """Resets the editor and output sections."""
    code_editor.delete("1.0", tk.END)
    lexer_output.config(state=tk.NORMAL)
    lexer_output.delete("1.0", tk.END)
    lexer_output.config(state=tk.DISABLED)
    parser_output.config(state=tk.NORMAL)
    parser_output.delete("1.0", tk.END)
    parser_output.config(state=tk.DISABLED)
    semantic_output.config(state=tk.NORMAL)
    semantic_output.delete("1.0", tk.END)
    semantic_output.config(state=tk.DISABLED)
    codegen_output.config(state=tk.NORMAL)
    codegen_output.delete("1.0", tk.END)
    codegen_output.config(state=tk.DISABLED)
    output_section.config(state=tk.NORMAL)
    output_section.delete("1.0", tk.END)
    output_section.config(state=tk.DISABLED)

# GUI setup
app = tk.Tk()
app.title("Custom Language IDE")
app.geometry("1000x800")

# Set dark theme colors
bg_color = "#1e1e1e"
fg_color = "#d4d4d4"
highlight_color = "#007acc"

app.configure(bg=bg_color)

# Add a canvas and scrollbar to enable scrolling
canvas = tk.Canvas(app, bg=bg_color, highlightthickness=0)
scrollbar = ttk.Scrollbar(app, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg=bg_color)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Code Editor
code_editor_label = tk.Label(scrollable_frame, text="Code Editor:", font=("Consolas", 12, "bold"), fg=fg_color, bg=bg_color)
code_editor_label.pack(anchor=tk.W, padx=10, pady=(10, 0))

code_editor = scrolledtext.ScrolledText(scrollable_frame, wrap=tk.WORD, font=("Consolas", 12), bg="#252526", fg=fg_color, insertbackground="white")
code_editor.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

# Controls Section
controls_frame = tk.Frame(scrollable_frame, bg=bg_color)
controls_frame.pack(pady=5)

# Run Button
run_button = tk.Button(controls_frame, text="Run Code", command=run_code, bg="red", fg="white", font=("Arial", 12, "bold"), relief=tk.FLAT)
run_button.grid(row=0, column=0, padx=10)

# Save Button
save_button = tk.Button(controls_frame, text="Save Code", command=save_code, bg="green", fg="white", font=("Arial", 12, "bold"), relief=tk.FLAT)
save_button.grid(row=0, column=1, padx=10)

# Load Button
load_button = tk.Button(controls_frame, text="Load Code", command=load_code, bg="blue", fg="white", font=("Arial", 12, "bold"), relief=tk.FLAT)
load_button.grid(row=0, column=2, padx=10)

# Reset Button
reset_button = tk.Button(controls_frame, text="Reset Code", command=reset_code, bg="orange", fg="white", font=("Arial", 12, "bold"), relief=tk.FLAT)
reset_button.grid(row=0, column=3, padx=10)


def toggle_theme():
    """Switches between light and dark themes."""
    global bg_color, fg_color, highlight_color

    if bg_color == "#1e1e1e":  # Currently dark theme
        bg_color = "white"
        fg_color = "black"
        highlight_color = "blue"
    else:  # Switch to dark theme
        bg_color = "#1e1e1e"
        fg_color = "#d4d4d4"
        highlight_color = "#007acc"

    # Update the background and text colors for all widgets
    app.configure(bg=bg_color)
    canvas.configure(bg=bg_color)
    scrollable_frame.configure(bg=bg_color)

    code_editor_label.configure(fg=fg_color, bg=bg_color)
    lexer_label.configure(fg=fg_color, bg=bg_color)
    parser_label.configure(fg=fg_color, bg=bg_color)
    semantic_label.configure(fg=fg_color, bg=bg_color)
    codegen_label.configure(fg=fg_color, bg=bg_color)

    code_editor.configure(bg=bg_color, fg=fg_color, insertbackground=fg_color)
    lexer_output.configure(bg=bg_color, fg=fg_color, insertbackground=fg_color)
    parser_output.configure(bg=bg_color, fg=fg_color, insertbackground=fg_color)
    semantic_output.configure(bg=bg_color, fg=fg_color, insertbackground=fg_color)
    codegen_output.configure(bg=bg_color, fg=fg_color, insertbackground=fg_color)

    run_button.configure(bg="red", fg="white")
    save_button.configure(bg="green", fg="white")
    load_button.configure(bg="blue", fg="white")
    reset_button.configure(bg="orange", fg="white")
    theme_button.configure(bg=highlight_color, fg="white")

    scrollbar.configure(background=bg_color, troughcolor=bg_color)

# Theme Toggle Button
theme_button = tk.Button(controls_frame, text="Toggle Theme", command=toggle_theme, bg=highlight_color, fg="white", font=("Arial", 12, "bold"), relief=tk.FLAT)
theme_button.grid(row=0, column=4, padx=10)

codegen_label = tk.Label(scrollable_frame, text="Output:", font=("Consolas", 12, "bold"), fg=fg_color, bg=bg_color)
codegen_label.pack(anchor=tk.W, padx=10, pady=(10, 0))

output_section = scrolledtext.ScrolledText(scrollable_frame, wrap=tk.WORD, font=("Consolas", 12), bg=bg_color, fg=fg_color, insertbackground="white")
output_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
output_section.config(state=tk.DISABLED)


# Output Sections
lexer_label = tk.Label(scrollable_frame, text="Lexer Output:", font=("Consolas", 12, "bold"), fg=fg_color, bg=bg_color)
lexer_label.pack(anchor=tk.W, padx=10, pady=(10, 0))

lexer_output = scrolledtext.ScrolledText(scrollable_frame, wrap=tk.WORD, font=("Consolas", 12), bg=bg_color, fg=fg_color, insertbackground="white")
lexer_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
lexer_output.config(state=tk.DISABLED)

parser_label = tk.Label(scrollable_frame, text="Parser Output:", font=("Consolas", 12, "bold"), fg=fg_color, bg=bg_color)
parser_label.pack(anchor=tk.W, padx=10, pady=(10, 0))

parser_output = scrolledtext.ScrolledText(scrollable_frame, wrap=tk.WORD, font=("Consolas", 12), bg=bg_color, fg=fg_color, insertbackground="white")
parser_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
parser_output.config(state=tk.DISABLED)

semantic_label = tk.Label(scrollable_frame, text="Semantic Analysis:", font=("Consolas", 12, "bold"), fg=fg_color, bg=bg_color)
semantic_label.pack(anchor=tk.W, padx=10, pady=(10, 0))

semantic_output = scrolledtext.ScrolledText(scrollable_frame, wrap=tk.WORD, font=("Consolas", 12), bg=bg_color, fg=fg_color, insertbackground="white")
semantic_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
semantic_output.config(state=tk.DISABLED)

codegen_label = tk.Label(scrollable_frame, text="Code Generation Output:", font=("Consolas", 12, "bold"), fg=fg_color, bg=bg_color)
codegen_label.pack(anchor=tk.W, padx=10, pady=(10, 0))

codegen_output = scrolledtext.ScrolledText(scrollable_frame, wrap=tk.WORD, font=("Consolas", 12), bg=bg_color, fg=fg_color, insertbackground="white")
codegen_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
codegen_output.config(state=tk.DISABLED)



# Start the GUI event loop
app.mainloop()
