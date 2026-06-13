import { NavLink } from "react-router-dom";

function Icon({ name, size = 18 }) {
  const common = {
    width: size,
    height: size,
    viewBox: "0 0 24 24",
    fill: "none",
    xmlns: "http://www.w3.org/2000/svg",
  };

  switch (name) {
    case "overview":
      return (
        <svg {...common}>
          <path
            d="M3 13h8V3H3v10zM3 21h8v-6H3v6zM13 21h8V11h-8v10zM13 3v6h8V3h-8z"
            fill="#94A3B8"
          />
        </svg>
      );

    case "citizens":
      return (
        <svg {...common}>
          <path
            d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
            fill="#94A3B8"
          />
        </svg>
      );

    case "graph":
      return (
        <svg {...common}>
          <path
            d="M20 8a2 2 0 11-4 0 2 2 0 014 0zM6 8a2 2 0 11-4 0 2 2 0 014 0zM12 16a2 2 0 11-4 0 2 2 0 014 0zM7 8.5l4 3.5 4-3.5"
            stroke="#94A3B8"
            strokeWidth="1.2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      );

    case "audit":
      return (
        <svg {...common}>
          <path
            d="M7 7h10v2H7V7zm0 4h7v2H7v-2z"
            fill="#94A3B8"
          />
          <rect
            x="4"
            y="3"
            width="16"
            height="18"
            rx="2"
            stroke="#94A3B8"
            strokeWidth="1"
            fill="none"
          />
        </svg>
      );

    default:
      return null;
  }
}

function Sidebar() {
  return (
    <aside className="sidebar">
      <div>

        {/* LOGO */}

        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "12px",
            marginBottom: "30px",
          }}
        >
          <div
            style={{
              width: "44px",
              height: "44px",
              borderRadius: "12px",
              background:
                "linear-gradient(135deg,#2563EB,#1D4ED8)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#fff",
              fontWeight: "800",
              fontSize: "18px",
            }}
          >
            TI
          </div>

          <div>
            <div
              style={{
                fontWeight: "800",
                fontSize: "18px",
                color: "#FFFFFF",
              }}
            >
              Tax Intelligence
            </div>

            <div
              style={{
                fontSize: "12px",
                color: "#94A3B8",
              }}
            >
              National Tax Network
            </div>
          </div>
        </div>

        {/* SECTION TITLE */}

        <div
          style={{
            fontSize: "12px",
            fontWeight: "700",
            color: "#94A3B8",
            letterSpacing: "1px",
            textTransform: "uppercase",
            marginBottom: "15px",
          }}
        >
          Intelligence
        </div>

        {/* NAVIGATION */}

        <nav
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "8px",
          }}
        >
          <NavLink
            to="/"
            className={({ isActive }) =>
              isActive ? "nav-item active" : "nav-item"
            }
          >
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "12px",
              }}
            >
              <Icon name="overview" />
              <span>Overview</span>
            </div>
          </NavLink>

          <NavLink
            to="/citizens"
            className={({ isActive }) =>
              isActive ? "nav-item active" : "nav-item"
            }
          >
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "12px",
              }}
            >
              <Icon name="citizens" />
              <span>Entity Explorer</span>
            </div>
          </NavLink>

          <NavLink
            to="/graph"
            className={({ isActive }) =>
              isActive ? "nav-item active" : "nav-item"
            }
          >
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "12px",
              }}
            >
              <Icon name="graph" />
              <span>Knowledge Graph</span>
            </div>
          </NavLink>

          <NavLink
            to="/audit"
            className={({ isActive }) =>
              isActive ? "nav-item active" : "nav-item"
            }
          >
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "12px",
              }}
            >
              <Icon name="audit" />
              <span>AI Audit Center</span>
            </div>
          </NavLink>
        </nav>
      </div>

      {/* FOOTER */}

      <div
        style={{
          marginTop: "50px",
          padding: "16px",
          background: "#111827",
          borderRadius: "12px",
          border: "1px solid #243244",
        }}
      >
        <div
          style={{
            fontSize: "12px",
            color: "#94A3B8",
          }}
        >
          System Status
        </div>

        <div
          style={{
            fontSize: "26px",
            fontWeight: "800",
            color: "#22C55E",
            marginTop: "4px",
          }}
        >
          ONLINE
        </div>

        <div
          style={{
            fontSize: "12px",
            color: "#94A3B8",
          }}
        >
          Risk Intelligence Engine
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;