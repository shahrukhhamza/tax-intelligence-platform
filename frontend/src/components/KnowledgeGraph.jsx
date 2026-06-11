import ReactFlow, {
  Background,
  Controls,
  MiniMap,
} from "reactflow";

import "reactflow/dist/style.css";

function KnowledgeGraph({
  nodes = [],
  edges = [],
}) {

  const flowNodes = nodes.map(
    (node, index) => ({
      id: String(node.id),

      data: {
        label: node.label,
      },

      position: {
        x: (index % 5) * 250,
        y: Math.floor(index / 5) * 150,
      },

      style:
        node.type === "target"
          ? {
              background: "#ef4444",
              color: "#fff",
            }
          : {},
    })
  );

  const flowEdges = edges.map(
    (edge, index) => ({
      id: `e${index}`,
      source: String(edge.source),
      target: String(edge.target),
      label: edge.label,
    })
  );

  return (
    <div
      style={{
        width: "100%",
        height: "70vh",
      }}
    >
      <ReactFlow
        nodes={flowNodes}
        edges={flowEdges}
        fitView
      >
        <MiniMap />
        <Controls />
        <Background />
      </ReactFlow>
    </div>
  );
}

export default KnowledgeGraph;