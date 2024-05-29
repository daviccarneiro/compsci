import cv2
import pytesseract
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os

# Definir o caminho para o executável do Tesseract (ajuste conforme necessário)
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'  # Ajuste conforme necessário

# Verificar se a variável TESSDATA_PREFIX está configurada corretamente
os.environ['TESSDATA_PREFIX'] = '/opt/homebrew/Cellar/tesseract/5.3.4_1/share/tessdata'

# Função para realizar OCR e verificar checkboxes
def extract_data_from_image(image_path):
    # Carregar a imagem
    image = cv2.imread(image_path)

    # Pré-processamento da imagem
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Aplicar OCR para extrair texto
    data = pytesseract.image_to_string(thresh, lang='por')

    # Analisar os dados extraídos
    extracted_data = {
        "Escova de dentes própria": "Sim" if "Escova de dentes própria\nSim" in data else "Não",
        "Uso de pasta de dentes com fluor": "Sim" if "Uso de pasta de dentes com fluor\nSim" in data else "Não",
        "Frequência da escovação": "Sim" if "Frequência da escovação\nSim" in data else "Não",
        "Consumo de bebida alcoolica": "Sim" if "Consumo de bebida alcoolica\nSim" in data else "Não",
        "Uso de tabaco": "Sim" if "Uso de tabaco\nSim" in data else "Não",
        "Prática de alguma religião": "Sim" if "Prática de alguma religião\nSim" in data else "Não",
        "Frequência do consumo (diário)": "Diário" if "Frequência do consumo\nDiário" in data else "",
        "Frequência do consumo (semanal)": "Semanal" if "Frequência do consumo\nSemanal" in data else "",
        "Frequência do consumo (mensal)": "Mensal" if "Frequência do consumo\nMensal" in data else "",
        "Frequência do consumo (eventos sociais)": "Eventos sociais" if "Frequência do consumo\nEventos sociais" in data else "",
        "Frequência do consumo (nunca)": "Nunca" if "Frequência do consumo\nNunca" in data else "",
        "Frequência (nunca)": "Nunca" if "Frequência\nNunca" in data else "",
        "Frequência (anualmente)": "Anualmente" if "Frequência\nAnualmente" in data else "",
        "Frequência (mensalmente)": "Mensalmente" if "Frequência\nMensalmente" in data else "",
        "Frequência (semanalmente)": "Semanalmente" if "Frequência\nSemanalmente" in data else ""
    }

    return extracted_data

# Função para exibir e salvar os dados em um arquivo Excel
def save_data_to_excel(data, output_path):
    # Criar um DataFrame
    df = pd.DataFrame([data])

    # Exibir os dados extraídos
    print(df)

    # Salvar em um arquivo Excel
    df.to_excel(output_path, index=False)

# Função para selecionar o arquivo e processar a imagem
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        data = extract_data_from_image(file_path)
        save_data_to_excel(data, "dados_extraidos.xlsx")
        messagebox.showinfo("Concluído", "Os dados foram extraídos e salvos em 'dados_extraidos.xlsx'")
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
