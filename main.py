import os
from src.models.spotify_dataset import SpotifyDatasetModel
from src.controllers.sorting import SortingController

def main():
    # Caminho para o dataset do Spotify na pasta data/
    csv_path = os.path.join('data', 'dataset.csv')
    
    if not os.path.exists(csv_path):
        print(f"Erro: O ficheiro '{csv_path}' não foi encontrado.")
        print("Certifica-te de que o 'dataset.csv' está dentro da pasta 'data/' no teu repositório.")
        return

    print("A carregar o dataset do Spotify...")
    model = SpotifyDatasetModel(csv_path)
    controller = SortingController()

    # Tamanhos de entrada especificados no enunciado do trabalho
    # (Podes ajustar para valores maiores como 10000 ou 50000 se o computador aguentar)
    sizes = [100, 500, 1000, 50000, 10000, 50000]
    algorithms = ['Bubble Sort', 'Selection Sort', 'Insertion Sort', 'Merge Sort']

    print("\n" + "="*70)
    print(" INÍCIO DOS TESTES DE DESEMPENHO DOS ALGORITMOS DE ORDENAÇÃO ")
    print("="*70)

    for size in sizes:
        try:
            # Extrai uma amostra do dataset (ex: usando a coluna 'popularity' ou 'duration_ms')
            raw_data = model.get_sample(size, column_name='popularity')
        except Exception as e:
            print(f"Erro ao extrair amostra de tamanho {size}: {e}")
            continue

        # Gera os 3 cenários obrigatórios: aleatório, ordenado (melhor caso) e inverso (pior caso)
        scenarios = model.generate_scenarios(raw_data)

        for scenario_name, data_list in scenarios.items():
            print(f"\n-> Tamanho: {size} elementos | Cenário: {scenario_name.upper()}")
            print("-" * 65)
            print(f"{'Algoritmo':<16} | {'Tempo (ms)':<12} | {'Comparações':<14} | {'Trocas/Mov.':<12}")
            print("-" * 65)

            for algo in algorithms:
                # Executa o algoritmo e mede as métricas
                metrics = controller.execute_benchmark(data_list, algo)
                print(f"{algo:<16} | {metrics['tempo_ms']:<12.4f} | {metrics['comparacoes']:<14} | {metrics['trocas']:<12}")
            
            print("-" * 65)

    print("\n[SUCESSO] Todos os testes foram executados com sucesso!")

if __name__ == "__main__":
    main()
