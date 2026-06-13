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

  const getNodeStyle = (type) => {

    switch (type) {

      case "target":
      case "citizen":
        return {
          background: "#ef4444",
          color: "#fff",
          border: "2px solid #b91c1c",
          width: 200,
          fontWeight: "bold",
        };

      case "vehicle_summary":
        return {
          background: "#2563eb",
          color: "#fff",
          border: "2px solid #1d4ed8",
          width: 180,
        };

      case "luxury":
        return {
          background: "#1e40af",
          color: "#fff",
          border: "2px solid #1e3a8a",
          width: 180,
        };

      case "utility":
        return {
          background: "#f59e0b",
          color: "#fff",
          border: "2px solid #d97706",
          width: 180,
        };

      case "income":
        return {
          background: "#10b981",
          color: "#fff",
          border: "2px solid #059669",
          width: 180,
        };

      case "tax":
        return {
          background: "#8b5cf6",
          color: "#fff",
          border: "2px solid #7c3aed",
          width: 180,
        };

      case "status":
        return {
          background: "#eab308",
          color: "#000",
          border: "2px solid #ca8a04",
          width: 180,
        };

      case "risk":
        return {
          background: "#991b1b",
          color: "#fff",
          border: "2px solid #7f1d1d",
          width: 180,
        };

      case "compliance":
        return {
          background: "#dc2626",
          color: "#fff",
          border: "2px solid #991b1b",
          width: 220,
          fontWeight: "bold",
        };

      case "property":
        return {
          background: "#14b8a6",
          color: "#fff",
          border: "2px solid #0f766e",
          width: 180,
        };

      default:
        return {
          background: "#ffffff",
          color: "#000000",
          border: "1px solid #d1d5db",
          width: 180,
        };
    }
  };

  const citizenNode = nodes.find(
    (n) =>
      n.type === "target" ||
      n.type === "citizen"
  );

  const flowNodes = [];

  if (citizenNode) {

    flowNodes.push({

      id: String(citizenNode.id),

      data: {
        label: citizenNode.label,
      },

      position: {
        x: 600,
        y: 400,
      },

      style: getNodeStyle(
        citizenNode.type
      ),
    });

    nodes.forEach((node) => {

      if (
        node.id === citizenNode.id
      ) {
        return;
      }

      let position = {
        x: 100,
        y: 100,
      };

      switch (node.type) {

        case "compliance":
          position = {
            x: 600,
            y: 50,
          };
          break;

        case "risk":
          position = {
            x: 950,
            y: 50,
          };
          break;

        case "status":
          position = {
            x: 150,
            y: 250,
          };
          break;

        case "vehicle_summary":
          position = {
            x: 1050,
            y: 250,
          };
          break;

        case "luxury":
          position = {
            x: 1050,
            y: 100,
          };
          break;

        case "tax":
          position = {
            x: 150,
            y: 550,
          };
          break;

        case "income":
          position = {
            x: 1050,
            y: 550,
          };
          break;

        case "property":
          position = {
            x: 150,
            y: 750,
          };
          break;

        case "utility":
          position = {
            x: 600,
            y: 800,
          };
          break;

        default:
          position = {
            x: 300,
            y: 300,
          };
      }

      flowNodes.push({

        id: String(node.id),

        data: {
          label: node.label,
        },

        position,

        style: getNodeStyle(
          node.type
        ),
      });

    });

  }

  const flowEdges = edges.map(
    (edge, index) => ({

      id: `e${index}`,

      source: String(edge.source),

      target: String(edge.target),

      label: edge.label,

      animated: true,

      style: {
        strokeWidth: 2,
      },
    })
  );

  return (
    <div
      style={{
        width: "100%",
        height: "90vh",
      }}
    >
      <ReactFlow
        nodes={flowNodes}
        edges={flowEdges}
        fitView
      >
        <ReactFlow
  nodes={flowNodes}
  edges={flowEdges}
  fitView
>
  <Controls
  style={{
    background: "#111827",
    border: "1px solid #243244",
    borderRadius: "12px",
    overflow: "hidden",
  }}
/>

  <Background
    color="#334155"
    gap={20}
  />
</ReactFlow>
      </ReactFlow>
    </div>
  );
}

export default KnowledgeGraph;