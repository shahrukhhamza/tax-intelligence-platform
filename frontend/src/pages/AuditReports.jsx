import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function AuditReports() {
  const { id } = useParams();

  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) {
      setLoading(false);
      return;
    }

    fetch(`http://127.0.0.1:8000/api/audit/${id}`)
      .then((res) => res.json())
      .then((data) => {
        setReport(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [id]);

  if (!id) {
    return (
      <div style={{ padding: "32px" }}>
        <h1>AI Audit Center</h1>
        <p style={{ marginTop: "10px", color: "#94A3B8" }}>
          Open a citizen profile and click
          "Generate AI Audit Report".
        </p>
      </div>
    );
  }

  if (loading) {
    return (
      <div style={{ padding: "32px" }}>
        <h2>Loading Audit Report...</h2>
      </div>
    );
  }

  if (!report) {
    return (
      <div style={{ padding: "32px" }}>
        <h2>Report Not Found</h2>
      </div>
    );
  }

  const riskColor =
    report.risk_score >= 80
      ? "#EF4444"
      : report.risk_score >= 60
      ? "#F97316"
      : report.risk_score >= 35
      ? "#EAB308"
      : "#22C55E";

  return (
    <div style={{ padding: "32px" }}>
      <h1>AI Tax Audit Report</h1>

      <p
        style={{
          color: "#94A3B8",
          marginTop: "8px",
        }}
      >
        Entity ID: {report.entity_id}
      </p>

      {/* Score Card */}

      <div
        className="card"
        style={{
          padding: "24px",
          marginTop: "24px",
          marginBottom: "24px",
        }}
      >
        <h3>Tax Compliance Deviation Score</h3>

        <h1
          style={{
            color: riskColor,
            marginTop: "10px",
          }}
        >
          {report.tax_compliance_deviation_score}/100
        </h1>

        <p style={{ color: riskColor }}>
          {report.risk_level} Risk
        </p>

        <p style={{ marginTop: "10px" }}>
          Audit Confidence: {report.audit_confidence}%
        </p>
      </div>

      {/* Financial Profile */}

      <div
        className="card"
        style={{
          padding: "24px",
          marginBottom: "24px",
        }}
      >
        <h2>Financial Profile</h2>

        <p>
          Declared Income: PKR{" "}
          {report.declared_income?.toLocaleString()}
        </p>

        <p>
          Tax Paid: PKR{" "}
          {report.tax_paid?.toLocaleString()}
        </p>

        <p>
          Filer Status: {report.filer_status}
        </p>

        <p>
          Vehicles: {report.vehicle_count}
        </p>

        <p>
          Properties: {report.property_count}
        </p>

        <p>
          Luxury Vehicles:{" "}
          {report.luxury_vehicle_count}
        </p>

        <p>
          Utility Bill: PKR{" "}
          {report.max_utility_bill?.toLocaleString()}
        </p>
      </div>

      {/* Findings */}

      <div
        className="card"
        style={{
          padding: "24px",
          marginBottom: "24px",
        }}
      >
        <h2>AI Findings</h2>

        <ul style={{ marginTop: "15px" }}>
          {report.findings?.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </div>

      {/* Summary */}

      <div
        className="card"
        style={{
          padding: "24px",
          marginBottom: "24px",
        }}
      >
        <h2>Executive Summary</h2>

        <p style={{ marginTop: "15px" }}>
          {report.summary}
        </p>
      </div>

      {/* Leakage */}

      <div
        className="card"
        style={{
          padding: "24px",
          marginBottom: "24px",
        }}
      >
        <h2>Estimated Tax Leakage</h2>

        <h1
          style={{
            color: "#EF4444",
            marginTop: "12px",
          }}
        >
          PKR{" "}
          {report.estimated_leakage?.toLocaleString()}
        </h1>
      </div>

      {/* Recommendation */}

      <div
        className="card"
        style={{
          padding: "24px",
          marginBottom: "24px",
        }}
      >
        <h2>Recommendation</h2>

        <h3
          style={{
            color: "#F97316",
            marginTop: "12px",
          }}
        >
          {report.recommendation}
        </h3>
      </div>

      {/* Audit Trail */}

      <div
        className="card"
        style={{
          padding: "24px",
          marginBottom: "24px",
        }}
      >
        <h2>Audit Trail</h2>

        <div style={{ marginTop: "16px" }}>
          {report.audit_trail?.map((step) => (
            <div
              key={step.step}
              style={{
                padding: "12px",
                marginBottom: "12px",
                borderLeft: "4px solid #3B82F6",
                background: "rgba(255,255,255,0.03)",
              }}
            >
              <strong>
                Step {step.step}
              </strong>

              <p>{step.action}</p>

              <p
                style={{
                  color: "#94A3B8",
                }}
              >
                {step.result}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Aliases */}

      <div
        className="card"
        style={{
          padding: "24px",
        }}
      >
        <h2>Known Identity Variations</h2>

        <ul style={{ marginTop: "15px" }}>
          {report.aliases?.map(
            (alias, index) => (
              <li key={index}>{alias}</li>
            )
          )}
        </ul>
      </div>
    </div>
  );
}

export default AuditReports;