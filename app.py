import streamlit as st
import pandas as pd
import os
import time
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

    # Barra lateral (Sidebar) com os controlos
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
        scenario_key_map = {
            "Aleatório": "aleatorio",
            "Melhor Caso (Ordenado)": "ordenado",
            "Pior Caso (Inverso)": "inverso"
        }
        selected_key = scenario_key_map[scenario_choice]

        # Extrai os dados
        raw_data = model.get_sample(size, column_name=column)
        scenarios = model.generate_scenarios(raw_data)
        data_to_sort = scenarios[selected_key]
        
        results = []
        algorithms = ['Bubble Sort', 'Selection Sort', 'Insertion Sort', 'Merge Sort']
        
        st.subheader(f"A executar testes para: {scenario_choice} (n = {size})")
        
        progress_bars = {}
        status_texts = {}
        
        for algo in algorithms:
            col1, col2 = st.columns([2, 5])
            with col1:
                st.markdown(f"**{algo}**")
            with col2:
                status_texts[algo] = st.empty()
                status_texts[algo].text("A aguardar...")
                progress_bars[algo] = st.progress(0)

        st.write("---")

        # Executa os algoritmos individualmente
        for algo in algorithms:
            status_texts[algo].text("A processar ordenação...")
            progress_bars[algo].progress(50)
            
            metrics = controller.execute_benchmark(data_to_sort, algo)
            
            # Conversão de milissegundos para segundos (/ 1000)
            tempo_segundos = metrics['tempo_ms'] / 1000.0
            
            results.append({
                'Algoritmo': algo,
                'Tempo (s)': round(tempo_segundos, 4),  # Arredondado a 4 casas decimais para maior precisão
                'Comparações': metrics['comparacoes'],
                'Trocas': metrics['trocas']
            })
            
            progress_bars[algo].progress(100)
            status_texts[algo].text(f"Concluído em {tempo_segundos:.4f} s")
        
        df_results = pd.DataFrame(results)
        
        # Exibir tabela final de resultados
        st.subheader("📋 Tabela Comparativa de Métricas")
        st.dataframe(df_results, use_container_width=True)
        
        # Gráfico de barras comparativo (em segundos)
        st.subheader("📊 Comparativo Gráfico de Desempenho (Tempo em s)")
        fig, ax = plt.subplots(figsize=(10, 5))
        
        bars = ax.bar(df_results['Algoritmo'], df_results['Tempo (s)'], color=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
        ax.set_ylabel("Tempo (s)")
        ax.set_xlabel("Algoritmo de Ordenação")
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height}s',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)

        st.pyplot(fig)
