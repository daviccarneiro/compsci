import cv2
import pytesseract
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os

# Configurar a variável de ambiente TESSDATA_PREFIX
os.environ['TESSDATA_PREFIX'] = '/opt/homebrew/Cellar/tesseract/5.3.4_1/share/tessdata'

# Definir o caminho para o executável do Tesseract (ajuste conforme necessário)
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    cropped_image = image[1100:1700, 100:1400]  # Ajuste os valores conforme necessário para focar na área específica
    gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    return thresh, cropped_image

def detect_checkboxes(thresh, cropped_image):
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    checkbox_positions = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if 15 < w < 50 and 15 < h < 50:
            checkbox_positions.append((x, y, w, h))

    checkbox_positions = sorted(checkbox_positions, key=lambda pos: (pos[1], pos[0]))

    # Mapeamento das posições de checkboxes para as variáveis de interesse
    extracted_data = {
        "Escova_Propria": 1 if any(40 < x < 70 and 40 < y < 70 for x, y, w, h in checkbox_positions) else 2,
        "Pasta_Com_Fluor": 1 if any(250 < x < 280 and 40 < y < 70 for x, y, w, h in checkbox_positions) else 2,
        "Frequencia_Escovacao": 1 if any(470 < x < 500 and 40 < y < 70 for x, y, w, h in checkbox_positions) else 2,
        "Uso_Alcool": 1 if any(40 < x < 70 and 170 < y < 200 for x, y, w, h in checkbox_positions) else 2,
        "Freq_Alcool": 0 if any(40 < x < 70 and 350 < y < 380 for x, y, w, h in checkbox_positions) else 1 if any(40 < x < 70 and 230 < y < 260 for x, y, w, h in checkbox_positions) else 2 if any(40 < x < 70 and 260 < y < 290 for x, y, w, h in checkbox_positions) else 3 if any(40 < x < 70 and 290 < y < 320 for x, y, w, h in checkbox_positions) else 4,
        "Uso_Tabaco": 1 if any(250 < x < 280 and 170 < y < 200 for x, y, w, h in checkbox_positions) else 2,
        "Freq_Tabaco": 0 if any(250 < x < 280 and 350 < y < 380 for x, y, w, h in checkbox_positions) else 1 if any(250 < x < 280 and 230 < y < 260 for x, y, w, h in checkbox_positions) else 2 if any(250 < x < 280 and 260 < y < 290 for x, y, w, h in checkbox_positions) else 3 if any(250 < x < 280 and 290 < y < 320 for x, y, w, h in checkbox_positions) else 4,
        "Religiao": 1 if any(470 < x < 500 and 170 < y < 200 for x, y, w, h in checkbox_positions) else 2,
        "Freq_Religiao": 0 if any(470 < x < 500 and 350 < y < 380 for x, y, w, h in checkbox_positions) else 1 if any(470 < x < 500 and 230 < y < 260 for x, y, w, h in checkbox_positions) else 2 if any(470 < x < 500 and 260 < y < 290 for x, y, w, h in checkbox_positions) else 3
    }

    return extracted_data

# Função para exibir e salvar os dados em um arquivo Excel
def save_data_to_excel(data, output_path):
    # Criar um DataFrame
    df = pd.DataFrame([data])

    # Verificar se o arquivo existe
    if os.path.isfile(output_path):
        # Se o arquivo existe, abra-o e adicione os novos dados
        with pd.ExcelWriter(output_path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
    else:
        # Se o arquivo não existe, crie um novo arquivo e adicione os dados
        with pd.ExcelWriter(output_path, mode='w', engine='openpyxl') as writer:
            df.to_excel(writer, index=False)

# Função para exibir os dados e permitir edição
def show_data_for_editing(data):
    edit_window = tk.Toplevel(root)
    edit_window.title("Editar Dados Coletados")
    
    entries = {}
    
    for i, (key, value) in enumerate(data.items()):
        tk.Label(edit_window, text=key).grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(edit_window)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entry.insert(0, value)
        entries[key] = entry
    
    def save_edited_data():
        edited_data = {key: int(entry.get()) for key, entry in entries.items()}
        save_data_to_excel(edited_data, "dados_extraidos.xlsx")
        messagebox.showinfo("Concluído", "Os dados foram salvos em 'dados_extraidos.xlsx'")
        edit_window.destroy()
    
    tk.Button(edit_window, text="Salvar", command=save_edited_data).grid(row=len(data), columnspan=2, pady=10)

# Função para selecionar o arquivo e processar a imagem
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        thresh, cropped_image = preprocess_image(file_path)
        data = detect_checkboxes(thresh, cropped_image)
        show_data_for_editing(data)
    else:
        messagebox.showwarning("Aviso", "Nenhum arquivo selecionado.")

# Criar a interface gráfica
root = tk.Tk()
root.title("Análise de Fichas")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="Selecione a imagem da ficha para análise:")
label.pack(pady=5)

button = tk.Button(frame, text="Selecionar arquivo", command=select_file)
button.pack(pady=5)

root.mainloop()
