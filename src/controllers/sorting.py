import time
from models.spotify_dataset import SpotifyDatasetModel
from controllers.sorting_algorithms import bubble_sort, merge_sort # As tuas implementacoes manuais

model = SpotifyDatasetModel('data/dataset.csv')
sizes = [100, 500, 1000, 5000, 10000, 50000]

for size in sizes:
    raw_data = model.get_sample(size, column_name='duration_ms')
    scenarios = model.generate_scenarios(raw_data)
    
    for scenario_name, data in scenarios.items():
        # Exemplo para medir tempo do Merge Sort
        data_to_sort = data.copy()
        start_time = time.time()
        
        # Chamada da funcao com contadores
        sorted_data, comparisons, swaps = merge_sort(data_to_sort)
        
        execution_time = (time.time() - start_time) * 1000 # Tempo em milissegundos
        print(f"Tamanho: {size} | Cenario: {scenario_name} | Tempo: {execution_time:.2f}ms")
