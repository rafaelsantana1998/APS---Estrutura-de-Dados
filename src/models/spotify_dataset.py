import pandas as pd
import random

class SpotifyDatasetModel:
    def __init__(self, csv_filepath):
        # Carrega o CSV baixado do Kaggle
        self.df = pd.read_csv(csv_filepath)

    def get_sample(self, size, column_name='popularity'):
        """
        Extrai uma amostra de tamanho N a partir de uma coluna especifica.
        """
        # Garante que a amostra nao excede o tamanho total
        sample_df = self.df.sample(n=min(size, len(self.df)), random_state=42)
        return sample_df[column_name].tolist()

    def generate_scenarios(self, base_list):
        """
        Cria os 3 cenarios exigidos pelo trabalho:
        1. Aleatorio
        2. Ordenado (Melhor Caso para alguns algoritmos)
        3. Inversamente Ordenado (Pior Caso)
        """
        random_case = list(base_list)
        
        # Dados em ordem crescente (Melhor Caso)
        sorted_case = sorted(base_list)
        
        # Dados em ordem decrescente (Pior Caso)
        reversed_case = sorted(base_list, reverse=True)
        
        return {
            'aleatorio': random_case,
            'ordenado': sorted_case,
            'inverso': reversed_case
        }
