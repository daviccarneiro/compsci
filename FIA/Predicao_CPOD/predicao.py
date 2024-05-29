import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pickle
import os

# Defina o caminho para o arquivo CSV
csv_path = 'MOCK_DATA.csv'

# Verifique se o arquivo CSV está no diretório
if not os.path.isfile(csv_path):
    st.error(f"Arquivo {csv_path} não encontrado.")
    st.stop()

# Load dataset
data = pd.read_csv(csv_path)

# Preprocess the data
le_gender = LabelEncoder()
data['gender'] = le_gender.fit_transform(data['gender'])
data['Capital'] = data['Capital'].astype(int)

# Define features and target
X = data[['gender', 'Capital', 'EscovacoesPorDia']]
y = data['CPOD']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train or load model
model_path = 'rf_model.pkl'
try:
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)

# Streamlit app
st.title('Previsão de Índice CPOD')

gender = st.selectbox('Gênero', ['Female', 'Male'])
capital = st.selectbox('Mora na capital?', ['Sim', 'Não'])
escovacoes = st.slider('Escovações por dia', 1, 10, 1)

if st.button('Prever CPOD'):
    gender_num = le_gender.transform([gender])[0]
    capital_num = 1 if capital == 'Sim' else 0
    input_data = pd.DataFrame([[gender_num, capital_num, escovacoes]], columns=['gender', 'Capital', 'EscovacoesPorDia'])
    prediction = model.predict(input_data)[0]
    st.write(f'Índice CPOD previsto: {prediction:.2f}')

if st.button('Re-treinar modelo'):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)
    st.write('Modelo re-treinado com sucesso!')
