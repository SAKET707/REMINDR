import { FcGoogle } from "react-icons/fc";
import { FiSend } from "react-icons/fi";
import AppLayout from "../layouts/AppLayout";
import { useAuth } from "../context/useAuth";
import { connectTelegram } from "../services/telegram";
import { notify } from "../utils/toast";
import { deleteAccount } from "../services/user";

export default function Profile() {
  const { user, loading, refreshUser, logout } = useAuth();

  const handleDeleteAccount = async () => {
    const confirmed = window.confirm(
      "This will permanently delete your REMINDR account.\n\nThis action cannot be undone.",
    );

    if (!confirmed) return;

    try {
      await deleteAccount();

      notify.success("Account deleted successfully.");

      logout();
    } catch (error) {
      notify.error("Unable to delete account.");
    }
  };

  const handleRefreshTelegram = async () => {
    try {
      await refreshUser();

      notify.success("Profile updated.");
    } catch (error) {
      notify.error("Unable to refresh profile.");
    }
  };

  const handleTelegramConnect = async () => {
    try {
      const { token } = await connectTelegram();

      window.open(`https://t.me/REMINDR0_bot?start=${token}`, "_blank");

      notify.success("Telegram opened. Complete the connection there.");
    } catch (error) {
      console.error(error);
      notify.error("Unable to connect Telegram.");
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background-soft">
        <h1 className="font-heading text-4xl font-bold text-primary-dark">
          Loading...
        </h1>
      </div>
    );
  }

  return (
    <AppLayout>
      <h1 className="font-heading text-8xl font-bold text-primary-dark">
        Profile
      </h1>

      <p className="mt-3 text-3xl text-text-secondary">
        Manage your connected accounts.
      </p>

      <div className="mt-12 max-w-5xl rounded-3xl bg-white p-10 shadow-md">
        {/* User */}

        <div className="flex flex-col items-center">
          {user?.profile_picture ? (
            <img
              src={user.profile_picture}
              alt={user.name}
              className="h-36 w-36 rounded-full object-cover"
            />
          ) : (
            <div className="flex h-36 w-36 items-center justify-center rounded-full bg-primary-dark text-5xl font-bold text-white">
              {user?.name?.charAt(0)}
            </div>
          )}

          <h2 className="mt-6 font-heading text-4xl font-bold text-primary-dark">
            {user?.name}
          </h2>

          <p className="mt-3 text-2xl text-text-secondary">{user?.email}</p>
        </div>

        <hr className="my-10 border-border" />

        {/* Google */}

        <div className="flex items-center justify-between">
          <div className="flex items-center gap-5">
            <FcGoogle className="text-5xl" />

            <div>
              <h3 className="font-heading text-3xl font-semibold text-primary-dark">
                Google Account
              </h3>

              <p className="mt-1 text-xl text-text-secondary">Connected</p>
            </div>
          </div>

          <span className="rounded-full bg-green-100 px-6 py-3 text-lg font-semibold text-green-700">
            Connected
          </span>
        </div>

        <hr className="my-10 border-border" />

        {/* Telegram */}

        {/* Telegram */}

        <div className="flex items-center justify-between">
          <div className="flex items-center gap-5">
            <FiSend className="text-4xl text-primary-dark" />

            <div>
              <h3 className="font-heading text-3xl font-semibold text-primary-dark">
                Telegram
              </h3>

              <p className="mt-1 text-xl text-text-secondary">
                {user?.telegram_chat_id ? "Connected" : "Not Connected"}
              </p>
            </div>
          </div>

          {user?.telegram_chat_id ? (
            <span className="rounded-full bg-green-100 px-6 py-3 text-lg font-semibold text-green-700">
              Connected
            </span>
          ) : (
            <div className="flex flex-col items-end gap-4">
              <button
                onClick={handleTelegramConnect}
                className="rounded-xl bg-primary-dark px-8 py-4 text-lg font-semibold text-white transition hover:opacity-90"
              >
                Connect Telegram
              </button>

              <button
                onClick={handleRefreshTelegram}
                className="text-base font-medium text-primary-dark underline underline-offset-4 transition hover:opacity-70"
              >
                I've Connected
              </button>
            </div>
          )}
        </div>

        <hr className="my-10 border-border" />
        <div className="rounded-2xl border border-red-200 bg-red-50 p-8">
          <h3 className="font-heading text-3xl font-bold text-red-700">
            Danger Zone
          </h3>

          <p className="mt-3 text-xl text-red-600">
            Permanently delete your REMINDR account. This removes your
            reminders, processed emails, disconnects Gmail notifications and
            cannot be undone.
          </p>

          <button
            onClick={handleDeleteAccount}
            className="mt-8 rounded-xl bg-red-600 px-8 py-4 text-lg font-semibold text-white transition hover:bg-red-700"
          >
            Delete Account
          </button>
        </div>
      </div>
    </AppLayout>
  );
}
