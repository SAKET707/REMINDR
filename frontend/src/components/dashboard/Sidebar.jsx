import { FiHome, FiUser, FiLogOut, FiMenu } from "react-icons/fi";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../../context/useAuth";
import { useReminder } from "../../context/useReminder";
import { notify } from "../../utils/toast";

export default function Sidebar({ collapsed, setCollapsed }) {
  const navigate = useNavigate();
  const location = useLocation();

  const { logout } = useAuth();
  const { clearReminders } = useReminder();

  const handleLogout = () => {
    clearReminders();
    logout();
    notify.success("Signed out successfully.");
    navigate("/");
  };

  return (
    <aside
      className={`min-h-screen bg-primary-dark text-white transition-all duration-300 ${
        collapsed ? "w-20" : "w-72 lg:w-100"
      }`}
    >
      <div className="flex items-center justify-between border-b border-white/10 p-6">
        {!collapsed && (
          <h1 className="font-heading text-4xl font-bold tracking-wide">
            REMINDR
          </h1>
        )}

        <button
          onClick={() => setCollapsed(!collapsed)}
          className="rounded-lg p-2 hover:bg-white/10"
        >
          <FiMenu size={26} />
        </button>
      </div>

      <nav className="mt-8 flex flex-col gap-2 px-3">
        <button
          onClick={() => navigate("/dashboard")}
          className={`flex items-center rounded-2xl px-4 py-4 text-lg font-medium transition ${
            collapsed ? "justify-center" : "gap-5"
          } ${
            location.pathname === "/dashboard"
              ? "bg-primary-light text-white"
              : "hover:bg-white/10"
          }`}
        >
          <FiHome size={26} />
          {!collapsed && <span>Dashboard</span>}
        </button>

        <button
          onClick={() => navigate("/profile")}
          className={`mt-2 flex items-center rounded-2xl px-4 py-4 text-lg font-medium transition ${
            collapsed ? "justify-center" : "gap-5"
          } ${
            location.pathname === "/profile"
              ? "bg-primary-light text-white"
              : "hover:bg-white/10"
          }`}
        >
          <FiUser size={26} />
          {!collapsed && <span>Profile</span>}
        </button>
      </nav>

      <div className="absolute bottom-6 left-0 right-0 px-4">
        <button
          onClick={handleLogout}
          className={`flex items-center rounded-2xl bg-primary px-4 py-4 text-lg font-medium transition ${
            collapsed ? "justify-center" : "gap-5"
          } hover:bg-red-600`}
        >
          <FiLogOut size={26} />
          {!collapsed && <span>Logout</span>}
        </button>
      </div>
    </aside>
  );
}
