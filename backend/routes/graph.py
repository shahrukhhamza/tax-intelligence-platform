from fastapi import APIRouter
from services.graph_builder import GraphBuilder
import networkx as nx

router = APIRouter()


@router.get("/live-graph")
def get_live_graph():

    builder = GraphBuilder()

    graph = builder.build_graph()

    nodes = []
    edges = []

    for node, data in graph.nodes(data=True):

        nodes.append({
            "id": str(node),
            "label": data.get("label", str(node)),
            "type": data.get("type", "default")
        })

    for source, target, data in graph.edges(data=True):

        edges.append({
            "source": str(source),
            "target": str(target),
            "label": data.get("relation", "")
        })

    return {
        "nodes": nodes,
        "edges": edges
    }


@router.get("/graph/{entity_id}")
def get_entity_graph(entity_id: str):

    builder = GraphBuilder()

    graph = builder.build_graph()

    if entity_id not in graph:

        return {
            "success": False,
            "message": f"Entity {entity_id} not found",
            "nodes": [],
            "edges": []
        }

    subgraph = nx.ego_graph(
        graph,
        entity_id,
        radius=1
    )

    # ----------------------------------
    # SMART GRAPH LIMITING
    # ----------------------------------

    if len(subgraph.nodes()) > 40:

        important_nodes = [entity_id]

        vehicle_nodes = []
        other_nodes = []

        for neighbor in graph.neighbors(entity_id):

            node_type = (
                graph.nodes[neighbor]
                .get("type", "default")
            )

            if node_type == "vehicle":

                vehicle_nodes.append(
                    neighbor
                )

            else:

                other_nodes.append(
                    neighbor
                )

        # Only first 10 vehicles
        important_nodes.extend(
            vehicle_nodes[:10]
        )

        # Keep ALL important nodes
        important_nodes.extend(
            other_nodes
        )

        subgraph = graph.subgraph(
            important_nodes
        ).copy()

    nodes = []
    edges = []

    for node, data in subgraph.nodes(data=True):

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

    for source, target, data in subgraph.edges(data=True):

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