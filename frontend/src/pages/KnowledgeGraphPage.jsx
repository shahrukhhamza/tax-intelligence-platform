import { useEffect, useState } from "react";
import KnowledgeGraph from "../components/KnowledgeGraph";

function KnowledgeGraphPage() {

  const [graphData, setGraphData] = useState({
    nodes: [],
    edges: [],
  });

  useEffect(() => {

    fetch(
      "http://127.0.0.1:8000/api/graph/ENT001"
    )
      .then((res) => res.json())
      .then((data) => {

        console.log("GRAPH RESPONSE:", data);

        setGraphData({
          nodes: data.nodes || [],
          edges: data.edges || [],
        });

      })
      .catch((err) =>
        console.error(err)
      );

  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>
        Entity Investigation Graph
      </h1>

      <KnowledgeGraph
        nodes={graphData.nodes}
        edges={graphData.edges}
      />
    </div>
  );
}

export default KnowledgeGraphPage;