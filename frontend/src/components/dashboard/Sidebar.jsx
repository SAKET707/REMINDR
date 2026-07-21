import { FiHome, FiUser, FiLogOut, FiMenu, FiBell } from "react-icons/fi";
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
      className={`relative flex min-h-screen flex-col bg-primary-dark text-white transition-all duration-300 ${
        collapsed ? "w-16 sm:w-20" : "w-64 sm:w-72 lg:w-80"
      }`}
    >
      {/* Header */}

      <div className="flex items-center justify-between border-b border-white/10 p-4 sm:p-6">
        {!collapsed && (
          <h1 className="font-heading text-2xl font-bold tracking-wide sm:text-3xl lg:text-4xl">
            REMINDR
          </h1>
        )}

        <button
          onClick={() => setCollapsed(!collapsed)}
          className="rounded-lg p-2 transition hover:bg-white/10"
        >
          <FiMenu size={22} />
        </button>
      </div>

      {/* Navigation */}

      <nav className="mt-6 flex flex-1 flex-col gap-2 px-2 sm:px-3">
        <button
          onClick={() => navigate("/dashboard")}
          className={`flex items-center rounded-2xl px-3 py-3 text-base font-medium transition sm:px-4 sm:py-4 sm:text-lg ${
            collapsed ? "justify-center" : "gap-4"
          } ${
            location.pathname === "/dashboard"
              ? "bg-primary-light text-white"
              : "hover:bg-white/10"
          }`}
        >
          <FiHome size={22} />
          {!collapsed && <span>Dashboard</span>}
        </button>

        <button
          onClick={() => navigate("/manage-reminders")}
          className={`flex items-center rounded-2xl px-3 py-3 text-base font-medium transition sm:mt-2 sm:px-4 sm:py-4 sm:text-lg ${
            collapsed ? "justify-center" : "gap-4"
          } ${
            location.pathname === "/manage-reminders"
              ? "bg-primary-light text-white"
              : "hover:bg-white/10"
          }`}
        >
          <FiBell size={22} />
          {!collapsed && <span>Manage Reminders</span>}
        </button>

        <button
          onClick={() => navigate("/profile")}
          className={`flex items-center rounded-2xl px-3 py-3 text-base font-medium transition sm:mt-2 sm:px-4 sm:py-4 sm:text-lg ${
            collapsed ? "justify-center" : "gap-4"
          } ${
            location.pathname === "/profile"
              ? "bg-primary-light text-white"
              : "hover:bg-white/10"
          }`}
        >
          <FiUser size={22} />
          {!collapsed && <span>Profile</span>}
        </button>
      </nav>

      {/* Logout */}

      <div className="mt-auto p-3 sm:p-4">
        <button
          onClick={handleLogout}
          className={`flex w-full items-center rounded-2xl bg-primary px-3 py-3 text-base font-medium transition hover:bg-red-600 sm:px-4 sm:py-4 sm:text-lg ${
            collapsed ? "justify-center" : "gap-4"
          }`}
        >
          <FiLogOut size={22} />
          {!collapsed && <span>Logout</span>}
        </button>
      </div>
    </aside>
  );
}
