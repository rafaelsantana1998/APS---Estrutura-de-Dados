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

    # Barra lateral (Sidebar) refinada com os controlos solicitados
    st.sidebar.header("Parâmetros do Teste")
    
    size = st.sidebar.selectbox(
        "Tamanho da Amostra (n):", 
        [500, 2500, 25000, 50000, 115000], 
        index=2
    )
    
    column = st.sidebar.selectbox(
        "Métrica de Ordenação:", 
        ["popularity", "duration_ms", "tempo"]
    )
    
    scenario_choice = st.sidebar.selectbox(
        "Cenário de Entrada:", 
        ["Aleatório", "Melhor Caso (Ordenado)", "Pior Caso (Inverso)"]
    )
    
    if st.sidebar.button("Executar Teste"):
        # Mapeamento do nome amigável para a chave usada no modelo
        scenario_key_map = {
            "Aleatório": "aleatorio",
            "Melhor Caso (Ordenado)": "ordenado",
            "Pior Caso (Inverso)": "inverso"
        }
        selected_key = scenario_key_map[scenario_choice]

        with st.spinner(fating_text := f"A processar amostra de {size} elementos para o cenário '{scenario_choice}'..."):
            # Extrai apenas a amostra e gera os cenários
            raw_data = model.get_sample(size, column_name=column)
            scenarios = model.generate_scenarios(raw_data)
            
            # Seleciona apenas os dados do cenário escolhido pelo utilizador
            data_to_sort = scenarios[selected_key]
            
            results = []
            algorithms = ['Bubble Sort', 'Selection Sort', 'Insertion Sort', 'Merge Sort']
            
            for algo in algorithms:
                metrics = controller.execute_benchmark(data_to_sort, algo)
                results.append({
                    'Algoritmo': algo,
                    'Tempo (ms)': metrics['tempo_ms'],
                    'Comparações': metrics['comparacoes'],
                    'Trocas': metrics['trocas']
                })
            
            df_results = pd.DataFrame(results)
            
            # Exibir resultados
            st.subheader(f"Resultados para o Cenário: {scenario_choice} (n = {size})")
            st.dataframe(df_results, use_container_width=True)
            
            # Gráfico de barras comparativo para o cenário selecionado
            st.subheader("📊 Comparativo de Desempenho (Tempo em ms)")
            fig, ax = plt.subplots(figsize=(10, 5))
            
            bars = ax.bar(df_results['Algoritmo'], df_results['Tempo (ms)'], color=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
            ax.set_ylabel("Tempo (ms)")
            ax.set_xlabel("Algoritmo de Ordenação")
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            
            # Adicionar os valores exatos em cima das barras
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height}ms',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=9)

            st.pyplot(fig)
