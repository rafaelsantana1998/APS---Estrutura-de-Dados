import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

from src.models.spotify_dataset import SpotifyDatasetModel
from src.controllers.sorting import SortingController

# Configuração da página do Streamlit
st.set_page_config(page_title="Algoritmos de Ordenação - Spotify", layout="wide")

st.title("🎵 Análise de Algoritmos de Ordenação com Dados do Spotify")
st.markdown("Trabalho prático focado na avaliação teórica (Big-O) e empírica de algoritmos de ordenação.")

# Caminho para o dataset
csv_path = os.path.join('data', 'dataset.csv')

if not os.path.exists(csv_path):
    st.error(f"O ficheiro '{csv_path}' não foi encontrado na pasta 'data/'. Por favor, verifica o upload.")
else:
    @st.cache_resource
    def load_data():
        return SpotifyDatasetModel(csv_path)

    model = load_data()
    controller = SortingController()

    # Barra lateral (Sidebar) para controlos do utilizador
    st.sidebar.header("Parâmetros do Teste")
    size = st.sidebar.selectbox(    "Tamanho da Amostra (n):",    [500, 2500, 25000, 50000, 115000], 
    index=2
)
    column = st.sidebar.selectbox("Métrica de Ordenação:", ["popularity", "duration_ms", "tempo"])
    
    if st.sidebar.button("Executar Testes"):
        with st.spinner("A executar os algoritmos e a calcular métricas..."):
            raw_data = model.get_sample(size, column_name=column)
            scenarios = model.generate_scenarios(raw_data)
            
            results = []
            for scenario_name, data_list in scenarios.items():
                for algo in ['Bubble Sort', 'Selection Sort', 'Insertion Sort', 'Merge Sort']:
                    metrics = controller.execute_benchmark(data_list, algo)
                    results.append({
                        'Cenário': scenario_name.capitalize(),
                        'Algoritmo': algo,
                        'Tempo (ms)': metrics['tempo_ms'],
                        'Comparações': metrics['comparacoes'],
                        'Trocas': metrics['trocas']
                    })
            
            df_results = pd.DataFrame(results)
            
            # Exibir resultados por cenário
            for scenario_name in ['Aleatorio', 'Ordenado', 'Inverso']:
                st.subheader(f"Cenário: {scenario_name}")
                subset = df_results[df_results['Cenário'] == scenario_name]
                st.dataframe(subset, use_container_width=True)
            
            # Gráfico Comparativo de Desempenho (Tempo)
            st.subheader("📊 Comparativo Gráfico de Desempenho (Tempo em ms)")
            fig, ax = plt.subplots(figsize=(10, 5))
            
            for algo in ['Bubble Sort', 'Selection Sort', 'Insertion Sort', 'Merge Sort']:
                algo_data = df_results[df_results['Algoritmo'] == algo]
                ax.plot(algo_data['Cenário'], algo_data['Tempo (ms)'], marker='o', label=algo)
            
            ax.set_ylabel("Tempo (ms)")
            ax.set_xlabel("Cenário de Entrada")
            ax.legend()
            ax.grid(True)
            
            st.pyplot(fig)
