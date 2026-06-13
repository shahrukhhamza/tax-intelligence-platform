import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import KnowledgeGraph from "../components/KnowledgeGraph";

function KnowledgeGraphPage() {

  const { id } = useParams();

  const entityId = id || "ENT001";

  const [graphData, setGraphData] = useState({
    nodes: [],
    edges: [],
  });

  useEffect(() => {

    fetch(
      `http://127.0.0.1:8000/api/graph/${entityId}`
    )
      .then((res) => res.json())
      .then((data) => {

        console.log(
          "GRAPH RESPONSE:",
          data
        );

        setGraphData({
          nodes: data.nodes || [],
          edges: data.edges || [],
        });

      })
      .catch((err) =>
        console.error(err)
      );

  }, [entityId]);

  return (
    <div style={{ padding: "20px" }}>

      <h1>
        Entity Investigation Graph
      </h1>

      <p>
        Entity ID: {entityId}
      </p>

      <KnowledgeGraph
        nodes={graphData.nodes}
        edges={graphData.edges}
      />

    </div>
  );
}

export default KnowledgeGraphPage;