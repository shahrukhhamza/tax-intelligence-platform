from services.graph_builder import GraphBuilder

builder = GraphBuilder()

graph = builder.build_graph()

print("\nFIRST 20 NODES:\n")

for node in list(graph.nodes())[:20]:
    print(node)