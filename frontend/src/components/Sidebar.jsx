import { NavLink } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="logo">
        TAX INTELLIGENCE
      </div>

      <nav>
        <NavLink
          to="/"
          className={({ isActive }) =>
            isActive ? "nav-item active" : "nav-item"
          }
        >
          Dashboard
        </NavLink>

        <NavLink
          to="/citizens"
          className={({ isActive }) =>
            isActive ? "nav-item active" : "nav-item"
          }
        >
          Citizens
        </NavLink>

        <NavLink
          to="/graph"
          className={({ isActive }) =>
            isActive ? "nav-item active" : "nav-item"
          }
        >
          Knowledge Graph
        </NavLink>

        <NavLink
          to="/audit"
          className={({ isActive }) =>
            isActive ? "nav-item active" : "nav-item"
          }
        >
          Audit Reports
        </NavLink>

      </nav>
    </aside>
  );
}

export default Sidebar;