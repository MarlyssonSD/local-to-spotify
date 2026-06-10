def jaccard_sim(a, b):
    '''Calcula a similaridade de Jaccard entre duas strings.
    A similaridade de Jaccard é definida como o tamanho da interseção dividido pelo tamanho da união dos conjuntos de palavras.
    '''
    a_set = set(a.lower().split())
    b_set = set(b.lower().split())
    intersec = a_set.intersection(b_set)
    union = a_set.union(b_set)
    return len(intersec) / len(union) if union else 0
