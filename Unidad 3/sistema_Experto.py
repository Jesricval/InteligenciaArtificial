import tkinter as tk
from tkinter import ttk, messagebox
from pyswip import Prolog

# --- Definición de Síntomas en la interfaz ---
symptoms_config = [
    {'id': 'fiebre', 'label': 'Fiebre:', 'options': ['ausente', 'baja', 'alta']},
    {'id': 'tos', 'label': 'Tos:', 'options': ['ausente', 'seca', 'productiva']},
    {'id': 'tipo_flema', 'label': 'Tipo de Flema (si tos productiva):', 'options': ['ninguna','clara', 'amarilla', 'verdosa', 'herrumbrosa']},
    {'id': 'dolor_garganta', 'label': 'Dolor de Garganta:', 'options': ['si', 'no_presente']},
    {'id': 'congestion_nasal', 'label': 'Congestión Nasal:', 'options': ['si', 'no_presente']},
    {'id': 'secrecion_nasal', 'label': 'Secreción Nasal:', 'options': ['si', 'no_presente']},
    {'id': 'tipo_secrecion', 'label': 'Tipo de Secreción Nasal (si hay):', 'options': ['ninguna','acuosa', 'espesa']},
    {'id': 'dolor_cabeza', 'label': 'Dolor de Cabeza:', 'options': ['si', 'no_presente']},
    {'id': 'dolores_musculares', 'label': 'Dolores Musculares:', 'options': ['no_presente', 'si', 'intensos']},
    {'id': 'fatiga', 'label': 'Fatiga:', 'options': ['no_presente', 'si', 'intensa']},
    {'id': 'dificultad_respirar', 'label': 'Dificultad para Respirar:', 'options': ['si', 'no_presente']},
    {'id': 'sibilancias', 'label': 'Sibilancias (silbidos al respirar):', 'options': ['si', 'no_presente']},
    {'id': 'dolor_pecho', 'label': 'Dolor de Pecho:', 'options': ['si', 'no_presente']},
    {'id': 'estornudos', 'label': 'Estornudos:', 'options': ['no_presente','si', 'frecuentes']},
    {'id': 'picazon_ojos_nariz', 'label': 'Picazón en Ojos/Nariz:', 'options': ['si', 'no_presente']},
    {'id': 'duracion_sintomas', 'label': 'Duración de los Síntomas:', 'options': [
        'ninguna', '< 3 dias', '> 5 dias', '< 10 dias', '< 3 semanas', 'semanas/meses',
        '5d_a_3sem', 
    ]},
    {'id': 'contacto_enfermo', 'label': 'Contacto con Enfermo (Gripe, COVID):', 'options': ['ninguno','si', 'no', 'desconocido']},
    {'id': 'historial_alergias', 'label': 'Historial de Alergias Conocidas:', 'options': ['si', 'no_presente']},
    {'id': 'historial_asma', 'label': 'Historial de Asma:', 'options': ['si', 'no_presente']},
    {'id': 'exposicion_polvo_tierra', 'label': 'Exposición a Polvo/Tierra (reciente):', 'options': ['si', 'no_presente']},
    {'id': 'epoca_año', 'label': 'Época del Año Predominante para Síntomas:', 'options': ['cualquiera','primavera', 'verano', 'otoño', 'invierno']},
    {'id': 'perdida_olfato_gusto', 'label': 'Pérdida de Olfato o Gusto:', 'options': ['si', 'no_presente']}
]


class AppDiagnostico:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Experto: Diagnóstico Respiratorio (Culiacán)")
        self.prolog = Prolog()
        try:
            self.prolog.consult("diag_res.pl")
        except Exception as e:
            messagebox.showerror("Error de Prolog", f"No se pudo cargar 'diagnosticador_respiratorio.pl': {e}\nAsegúrate que SWI-Prolog esté instalado y en el PATH, y que el archivo .pl exista.")
            self.root.destroy()
            return

        self.symptom_vars = {}

        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        canvas = tk.Canvas(main_frame)
        canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.symptoms_frame = ttk.Frame(canvas, padding="10")
        canvas.create_window((0, 0), window=self.symptoms_frame, anchor="nw")
        
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        row_num = 0
        for symptom_def in symptoms_config:
            label = ttk.Label(self.symptoms_frame, text=symptom_def['label'])
            label.grid(row=row_num, column=0, sticky="w", pady=2)
            
            var = tk.StringVar(value="default_selection") 
            self.symptom_vars[symptom_def['id']] = var
            
            options_frame = ttk.Frame(self.symptoms_frame)
            options_frame.grid(row=row_num, column=1, sticky="w")

            rb_default = ttk.Radiobutton(options_frame, text="No seleccionado", variable=var, value="default_selection")
            rb_default.pack(side=tk.LEFT, padx=2)

            for option_val in symptom_def['options']:
                val_to_assert = option_val
                if option_val == "no_presente": 
                     val_to_assert = "default_selection" 

                rb = ttk.Radiobutton(options_frame, text=option_val.replace("_", " ").capitalize(), variable=var, value=val_to_assert if option_val != "no_presente" else "default_selection_for_no")
                if option_val == "no_presente":
                     rb.configure(value="default_selection") 
                else:
                     rb.configure(value=option_val)
                rb.pack(side=tk.LEFT, padx=2)
            row_num += 1

        controls_frame = ttk.Frame(root, padding="10")
        controls_frame.grid(row=1, column=0, sticky="ew")

        self.diagnose_button = ttk.Button(controls_frame, text="Obtener Diagnóstico", command=self.diagnose)
        self.diagnose_button.pack(pady=10)

        self.result_label = ttk.Label(controls_frame, text="Diagnóstico(s) Posible(s):", font=("Arial", 12, "bold"))
        self.result_label.pack(pady=5)
        self.result_text = tk.Text(controls_frame, height=5, width=70, wrap=tk.WORD, state=tk.DISABLED)
        self.result_text.pack(pady=5, fill="x", expand=True)

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

    def diagnose(self):
        list(self.prolog.query("limpiar_sintomas."))

        for symptom_id, var in self.symptom_vars.items():
            value = var.get()
            if value not in ["default_selection", "default_selection_for_no", "ninguna", "cualquiera"]: 
                if symptom_id == 'duracion_sintomas' and value == '5d_a_3sem':
                    self.prolog.assertz(f"sintoma(duracion_sintomas, '> 5 dias')")
                    self.prolog.assertz(f"sintoma(duracion_sintomas, '< 3 semanas')")
                else:
                    self.prolog.assertz(f"sintoma('{symptom_id}', '{value}')")
        
        solutions = list(self.prolog.query("encontrar_diagnosticos(D)."))
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        if solutions and solutions[0]['D']:
            diagnoses_str = "\n".join([f"- {d.decode('utf-8') if isinstance(d, bytes) else str(d)}" for d in solutions[0]['D']])
            self.result_text.insert(tk.END, diagnoses_str)
        else:
            self.result_text.insert(tk.END, "No se pudo determinar un diagnóstico con los síntomas proporcionados.")
        self.result_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppDiagnostico(root)
    root.mainloop()