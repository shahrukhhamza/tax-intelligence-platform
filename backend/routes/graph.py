from fastapi import APIRouter
from services.graph_builder import GraphBuilder

router = APIRouter()


@router.get("/graph/{entity_id}")
def get_entity_graph(entity_id: str):

    builder = GraphBuilder()

    graph = builder.build_entity_graph(
        entity_id
    )

    if len(graph.nodes()) == 0:

        return {
            "success": False,
            "message": f"Entity {entity_id} not found",
            "nodes": [],
            "edges": []
        }

    nodes = []
    edges = []

    for node, data in graph.nodes(data=True):

        nodes.append({
            "id": str(node),
            "label": data.get(
                "label",
                str(node)
            ),
            "type": (
                "target"
                if str(node) == entity_id
                else data.get(
                    "type",
                    "default"
                )
            )
        })

    for source, target, data in graph.edges(data=True):

        edges.append({
            "source": str(source),
            "target": str(target),
            "label": data.get(
                "relation",
                ""
            )
        })

    return {
        "success": True,
        "entity_id": entity_id,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": nodes,
        "edges": edges
    }