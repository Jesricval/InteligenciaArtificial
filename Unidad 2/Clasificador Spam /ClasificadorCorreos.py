#OSUNA RUSSELL ANA ISABEL
#RODRIGUEZ VALERIO JESUS RICARDO
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog

import pandas as pd
import numpy as np

import nltk
from nltk.corpus import stopwords

# Descomenta la siguiente línea solo la primera vez si necesitas descargar los datos
# nltk.download('stopwords', quiet=True)
nltk.data.find('corpora/stopwords')
stop_words_es = set(stopwords.words('spanish'))
stop_words_en = set(stopwords.words('english'))

stop_words = stop_words_es.union(stop_words_en)

# --- 1. Preprocesamiento 
def limpiar_texto(texto, stop_words_set):
    if not isinstance(texto, str): texto = str(texto)
    texto = texto.lower()
    texto = ''.join([c if c.isalnum() or c.isspace() else ' ' for c in texto])
    cleaned_text = ' '.join(word for word in texto.split() if word not in stop_words_set and len(word) > 2)
    return cleaned_text

# --- 2. Carga, Entrenamiento y Evaluación 
# la creación del modelo de Bayes y la evaluación del rendimiento.
from sklearn.model_selection import train_test_split 
from sklearn.feature_extraction.text import CountVectorizer  # Conteo de palabras
from sklearn.naive_bayes import MultinomialNB  # Este se utiliza para la clasificación de Bayes
from sklearn.metrics import accuracy_score, classification_report, recall_score  
from sklearn.pipeline import Pipeline 

def load_train_evaluate(csv_path):
    global stop_words  # Lista de palabras a excluir del procesamiento

    print("Cargando datos...")
    datos = pd.read_csv(csv_path) 

    # --- Limpieza y preparación de datos ---
    
    datos = datos.drop_duplicates(subset=["text"]).copy()  # Se eliminan duplicados en la columna "text"
    datos["text"] = datos["text"].str.lower() # Convertir todo el texto a minúsculas
    datos["text"] = datos["text"].str.replace(r"[^a-zA-Z\s]", " ", regex=True) #Quitar caract. raros
    datos["text"] = datos["text"].apply(lambda x: " ".join([word for word in x.split() if len(word) > 2 and word not in stop_words]))
    # División de los datos en conjuntos de entrenamiento (80%) y prueba (20%)
    entrena_x, prueba_x, entrena_y, prueba_y = train_test_split(
        datos["text"], datos["target"], test_size=0.2, random_state=42
    )
    # Convierte el texto en una matriz de conteo de palabras.
    pipeline = Pipeline([
        ('vectorizer', CountVectorizer()),
        ('classifier', MultinomialNB())])    
    print("Entrenando modelo...")
    
    # Entrenamiento del modelo con los datos de entrenamiento
    pipeline.fit(entrena_x, entrena_y)
    print("\n--- Evaluación Test ---")
    y_pred = pipeline.predict(prueba_x)

    # Cálculo de la Exactitud (P + N) / Total
    accuracy = accuracy_score(prueba_y, y_pred)
    print(f"Exactitud: {accuracy:.4f}")

    recall_spam = recall_score(prueba_y, y_pred, pos_label=1) 
    print(f"Recuperación SPAM (Recall): {recall_spam:.4f} ({recall_spam*100:.2f}%)")
    # N / (N + FP) -> De todos los que NO eran SPAM, cuántos clasificamos correctamente?
    recall_no_spam = recall_score(prueba_y, y_pred, pos_label=0)
    print(f"Recuperación NO SPAM: {recall_no_spam:.4f} ({recall_no_spam*100:.2f}%)")


    print("----------------------")
    
    # Reporte de la clasificación como precisión y recall por clase
    print("\nReporte de Clasificación Detallado:")
    print(classification_report(prueba_y, y_pred))
    return pipeline


class SpamClassifierApp:
    def __init__(self, root, initial_pipeline):
        self.root = root
        self.pipeline = initial_pipeline
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
        self.classify_button = tk.Button(main_frame, text="Clasificar Correo", command= self.classify_email, font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white')
        self.classify_button.grid(row=6, column=0, columnspan=2, pady=(10, 5), ipady=5)
        self.result_label = tk.Label(main_frame, text="Resultado: Pendiente", font=('Arial', 12, 'bold'), pady=5)
        self.result_label.grid(row=7, column=0, columnspan=2)

    def classify_email(self):
        global stop_words

        # Obtencion de ingreso de datos en interfaz
        subject = self.subject_entry.get()
        sender = self.sender_entry.get()
        body = self.body_text.get("1.0", tk.END).strip()

        if not subject and not body:
            messagebox.showwarning("Entrada Vacía", "Ingresa asunto o contenido.")
            return

        text_parts = []
        if subject:
            text_parts.append(f"Subject: {subject}") 
        if body:
            text_parts.append(body)

        text_to_classify = "\n\n".join(text_parts)

        # Limpieza y formateo de texto
        cleaned_text = limpiar_texto(text_to_classify, stop_words)
        
        if not cleaned_text:
            messagebox.showwarning("Texto Vacío", "Texto vacío después de limpieza.")
            self.result_label.config(text="Resultado: Texto vacío", fg='orange'); return

        # Prediccion con modelo
        probabilities = self.pipeline.predict_proba([cleaned_text])[0]
        prediction = np.argmax(probabilities)
        probability = probabilities[prediction]

        #Muestra al usuario
        if prediction == 1:
            result_text = f"Resultado: SPAM ({probability*100:.1f}%)"
            self.result_label.config(text=result_text, fg='red')
        else:
            result_text = f"Resultado: NO SPAM ({probability*100:.1f}%)"
            self.result_label.config(text=result_text, fg='green')

if __name__ == "__main__":

    initial_csv_path = "spam_assassin.csv"
    initial_trained_pipeline = load_train_evaluate(csv_path=initial_csv_path)

    root = tk.Tk()
    app = SpamClassifierApp(root, initial_trained_pipeline)

    if not initial_trained_pipeline:
         print(f"\nADVERTENCIA: No se pudo entrenar el modelo inicial con '{initial_csv_path}'.")

    print("\nIniciando interfaz gráfica...")
    root.mainloop()
