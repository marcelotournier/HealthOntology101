import graphviz


def get_knowledge_graph(entities, triple_store):
    graph = graphviz.Digraph()

    node_set = list(set(entities))
    edge_set = set()

    for item in node_set:
        graph.node(item, item)
        for subject, predicate, object in triple_store:
            if subject in node_set:
                if object not in node_set:
                    node_set.append(object)
                    graph.node(object, object)
                if (subject, object) not in edge_set:
                    graph.edge(subject, object, label=predicate)
                    edge_set.add((subject, object))

    return graph
