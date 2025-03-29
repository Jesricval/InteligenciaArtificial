import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog


class SpamClassifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clasificador de Spam")
        self.root.geometry("600x450") 

        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="Asunto:", font=('Arial', 11)).grid(row=0, column=0, sticky=tk.W, pady=(5, 2))
        self.subject_entry = tk.Entry(main_frame, width=70, font=('Arial', 10))
        self.subject_entry.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 8))
        tk.Label(main_frame, text="Correo Remitente:", font=('Arial', 11)).grid(row=2, column=0, sticky=tk.W, pady=(0, 2))
        self.sender_entry = tk.Entry(main_frame, width=70, font=('Arial', 10))
        self.sender_entry.grid(row=3, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 8))
        tk.Label(main_frame, text="Contenido del Correo:", font=('Arial', 11)).grid(row=4, column=0, sticky=tk.W, pady=(0, 2))
        self.body_text = scrolledtext.ScrolledText(main_frame, width=70, height=8, wrap=tk.WORD, font=('Arial', 10))
        self.body_text.grid(row=5, column=0, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S, pady=(0, 10))
        self.classify_button = tk.Button(main_frame, text="Clasificar Correo", font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white')
        self.classify_button.grid(row=6, column=0, columnspan=2, pady=(10, 5), ipady=5)
        self.result_label = tk.Label(main_frame, text="Resultado: Pendiente", font=('Arial', 12, 'bold'), pady=5)
        self.result_label.grid(row=7, column=0, columnspan=2)

        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=root.quit)
        menubar.add_cascade(label="Archivo", menu=filemenu)
        root.config(menu=menubar)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = SpamClassifierApp(root)
    root.mainloop()
