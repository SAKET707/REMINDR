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
        <h1 className="font-heading text-3xl font-bold text-primary-dark sm:text-4xl">
          Loading...
        </h1>
      </div>
    );
  }

  return (
    <AppLayout>
      {/* Header */}

      <section>
        <h1 className="font-heading text-4xl font-bold text-primary-dark sm:text-5xl lg:text-6xl">
          Profile
        </h1>

        <p className="mt-3 text-base text-text-secondary sm:text-lg lg:text-xl">
          Manage your connected accounts.
        </p>
      </section>

      {/* Card */}

      <div className="mt-10 max-w-5xl rounded-3xl bg-white p-5 shadow-sm sm:p-6 lg:p-8">
        {/* User */}

        <div className="flex flex-col items-center text-center">
          {user?.profile_picture ? (
            <img
              src={user.profile_picture}
              alt={user.name}
              className="h-24 w-24 rounded-full object-cover sm:h-28 sm:w-28 lg:h-32 lg:w-32"
            />
          ) : (
            <div className="flex h-24 w-24 items-center justify-center rounded-full bg-primary-dark text-3xl font-bold text-white sm:h-28 sm:w-28 sm:text-4xl lg:h-32 lg:w-32 lg:text-5xl">
              {user?.name?.charAt(0)}
            </div>
          )}

          <h2 className="mt-5 font-heading text-2xl font-bold text-primary-dark sm:text-3xl">
            {user?.name}
          </h2>

          <p className="mt-2 break-all text-sm text-text-secondary sm:text-base">
            {user?.email}
          </p>
        </div>

        <hr className="my-7 border-border" />

        {/* Google */}

        <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-4">
            <FcGoogle className="text-4xl sm:text-5xl" />

            <div>
              <h3 className="font-heading text-xl font-semibold text-primary-dark sm:text-2xl">
                Google Account
              </h3>

              <p className="mt-1 text-sm text-text-secondary sm:text-base">
                Connected
              </p>
            </div>
          </div>

          <span className="self-start rounded-full bg-green-100 px-4 py-2 text-sm font-semibold text-green-700 sm:self-auto sm:px-5 sm:py-2.5">
            Connected
          </span>
        </div>

        <hr className="my-7 border-border" />

        {/* Telegram */}

        <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
          <div className="flex items-center gap-4">
            <FiSend className="text-3xl text-primary-dark sm:text-4xl" />

            <div>
              <h3 className="font-heading text-xl font-semibold text-primary-dark sm:text-2xl">
                Telegram
              </h3>

              <p className="mt-1 text-sm text-text-secondary sm:text-base">
                {user?.telegram_chat_id ? "Connected" : "Not Connected"}
              </p>
            </div>
          </div>

          {user?.telegram_chat_id ? (
            <span className="self-start rounded-full bg-green-100 px-4 py-2 text-sm font-semibold text-green-700 sm:self-auto sm:px-5 sm:py-2.5">
              Connected
            </span>
          ) : (
            <div className="flex w-full flex-col gap-3 lg:w-auto lg:items-end">
              <button
                onClick={handleTelegramConnect}
                className="w-full rounded-xl bg-primary-dark px-6 py-3 text-base font-semibold text-white transition hover:opacity-90 lg:w-auto lg:px-7 lg:py-3"
              >
                Connect Telegram
              </button>

              <button
                onClick={handleRefreshTelegram}
                className="text-sm font-medium text-primary-dark underline underline-offset-4 transition hover:opacity-70 sm:text-base"
              >
                I've Connected
              </button>
            </div>
          )}
        </div>

        <hr className="my-7 border-border" />

        {/* Danger Zone */}

        <div className="rounded-2xl border border-red-200 bg-red-50 p-5 sm:p-6">
          <h3 className="font-heading text-xl font-bold text-red-700 sm:text-2xl">
            Danger Zone
          </h3>

          <p className="mt-3 text-sm leading-6 text-red-600 sm:text-base">
            Permanently delete your REMINDR account. This removes your
            reminders, processed emails, disconnects Gmail notifications and
            cannot be undone.
          </p>

          <button
            onClick={handleDeleteAccount}
            className="mt-5 w-full rounded-xl bg-red-600 px-6 py-3 text-base font-semibold text-white transition hover:bg-red-700 sm:w-auto sm:px-7 sm:py-3"
          >
            Delete Account
          </button>
        </div>
      </div>
    </AppLayout>
  );
}
