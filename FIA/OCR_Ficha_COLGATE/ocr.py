import cv2
import pytesseract
import pandas as pd
import streamlit as st
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

def save_data_to_csv(data, output_path):
    # Criar um DataFrame
    df = pd.DataFrame([data])

    # Verificar se o arquivo existe
    if os.path.isfile(output_path):
        # Se o arquivo existe, adicione os novos dados ao arquivo existente
        df.to_csv(output_path, mode='a', header=False, index=False)
    else:
        # Se o arquivo não existe, crie um novo arquivo e adicione os dados
        df.to_csv(output_path, mode='w', header=True, index=False)

# Interface Streamlit
st.title("Análise de Fichas")

uploaded_file = st.file_uploader("Selecione a imagem da ficha para análise", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    with open("temp_image.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    thresh, cropped_image = preprocess_image("temp_image.jpg")
    data = detect_checkboxes(thresh, cropped_image)
    
    st.write("Dados Extraídos:")
    
    # Formulário para corrigir os dados extraídos
    with st.form(key='data_form'):
        escova_propria = st.selectbox('Escova Própria', [1, 2], index=0 if data['Escova_Propria'] == 1 else 1)
        pasta_com_fluor = st.selectbox('Pasta Com Flúor', [1, 2], index=0 if data['Pasta_Com_Fluor'] == 1 else 1)
        frequencia_escovacao = st.selectbox('Frequência de Escovação', [1, 2], index=0 if data['Frequencia_Escovacao'] == 1 else 1)
        uso_alcool = st.selectbox('Uso de Álcool', [1, 2], index=0 if data['Uso_Alcool'] == 1 else 1)
        freq_alcool = st.selectbox('Frequência de Uso de Álcool', [0, 1, 2, 3, 4], index=data['Freq_Alcool'])
        uso_tabaco = st.selectbox('Uso de Tabaco', [1, 2], index=0 if data['Uso_Tabaco'] == 1 else 1)
        freq_tabaco = st.selectbox('Frequência de Uso de Tabaco', [0, 1, 2, 3, 4], index=data['Freq_Tabaco'])
        religiao = st.selectbox('Prática de Alguma Religião', [1, 2], index=0 if data['Religiao'] == 1 else 1)
        freq_religiao = st.selectbox('Frequência da Prática Religiosa', [0, 1, 2, 3], index=data['Freq_Religiao'])

        submit_button = st.form_submit_button(label='Salvar Dados')

    if submit_button:
        # Atualizar os dados com os valores do formulário
        data = {
            "Escova_Propria": escova_propria,
            "Pasta_Com_Fluor": pasta_com_fluor,
            "Frequencia_Escovacao": frequencia_escovacao,
            "Uso_Alcool": uso_alcool,
            "Freq_Alcool": freq_alcool,
            "Uso_Tabaco": uso_tabaco,
            "Freq_Tabaco": freq_tabaco,
            "Religiao": religiao,
            "Freq_Religiao": freq_religiao
        }
        save_data_to_csv(data, "dados_extraidos.csv")
        st.success("Dados salvos com sucesso em 'dados_extraidos.csv'")
        
        # Botão para visualizar a ficha atualizada
        if st.button("Visualizar Ficha Atualizada"):
            df = pd.read_csv("dados_extraidos.csv")
            st.write(df)
        
        # Botão para exportar a planilha atual
        with open("dados_extraidos.csv", "rb") as file:
            st.download_button(
                label="Download Planilha",
                data=file,
                file_name="dados_extraidos.csv",
                mime="text/csv"
            )
