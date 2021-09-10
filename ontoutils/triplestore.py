from collections import namedtuple


triple = namedtuple('triple', ['subject', 'predicate', 'object'])

def make_triplestore(serialized_triples):
    triple_store = list(
    map(
        lambda line: triple(*line.split(" ===> ")),
        serialized_triples.split("\n")
    ))
    
    return triple_store
