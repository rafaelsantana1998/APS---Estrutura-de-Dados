import time

class SortingController:
    
    @staticmethod
    def bubble_sort(arr):
        """Implementação do Bubble Sort com contadores de métricas."""
        a = arr.copy()
        comparisons = 0
        swaps = 0
        n = len(a)
        
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                comparisons += 1
                if a[j] > a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
                    swaps += 1
                    swapped = True
            if not swapped:
                break
        return a, comparisons, swaps

    @staticmethod
    def selection_sort(arr):
        """Implementação do Selection Sort com contadores de métricas."""
        a = arr.copy()
        comparisons = 0
        swaps = 0
        n = len(a)
        
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                comparisons += 1
                if a[j] < a[min_idx]:
                    min_idx = j
            if min_idx != i:
                a[i], a[min_idx] = a[min_idx], a[i]
                swaps += 1
        return a, comparisons, swaps

    @staticmethod
    def insertion_sort(arr):
        """Implementação do Insertion Sort com contadores de métricas."""
        a = arr.copy()
        comparisons = 0
        swaps = 0  # Conta as deslocações/movimentações de elementos
        
        for i in range(1, len(a)):
            key = a[i]
            j = i - 1
            while j >= 0:
                comparisons += 1
                if a[j] > key:
                    a[j + 1] = a[j]
                    swaps += 1
                    j -= 1
                else:
                    break
            a[j + 1] = key
        return a, comparisons, swaps

    @staticmethod
    def merge_sort(arr):
        """Implementação do Merge Sort com contadores de métricas."""
        comparisons = 0
        swaps = 0  # Representa as escritas/recombinações no array

        def merge(left, right):
            nonlocal comparisons, swaps
            merged = []
            i = j = 0
            while i < len(left) and j < len(right):
                comparisons += 1
                if left[i] <= right[j]:
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    j += 1
                    swaps += 1
            merged.extend(left[i:])
            merged.extend(right[j:])
            return merged

        def sort(sub_arr):
            if len(sub_arr) <= 1:
                return sub_arr
            mid = len(sub_arr) // 2
            left = sort(sub_arr[:mid])
            right = sort(sub_arr[mid:])
            return merge(left, right)

        sorted_arr = sort(arr.copy())
        return sorted_arr, comparisons, swaps

    def execute_benchmark(self, data, algorithm_name):
        """Mede o tempo de execução (em ms) de um algoritmo específico."""
        start_time = time.time()
        
        if algorithm_name == 'Bubble Sort':
            _, comps, swaps = self.bubble_sort(data)
        elif algorithm_name == 'Selection Sort':
            _, comps, swaps = self.selection_sort(data)
        elif algorithm_name == 'Insertion Sort':
            _, comps, swaps = self.insertion_sort(data)
        elif algorithm_name == 'Merge Sort':
            _, comps, swaps = self.merge_sort(data)
        else:
            raise ValueError("Algoritmo desconhecido.")
            
        execution_time = (time.time() - start_time) * 1000  # Conversão para milissegundos
        
        return {
            'tempo_ms': round(execution_time, 4),
            'comparacoes': comps,
            'trocas': swaps
        }
