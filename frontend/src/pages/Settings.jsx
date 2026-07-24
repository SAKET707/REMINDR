import { FiSettings } from "react-icons/fi";
import AppLayout from "../layouts/AppLayout";
import { useAuth } from "../context/useAuth";
import { deleteAccount } from "../services/user";
import { notify } from "../utils/toast";
import ConfirmationModal from "../components/common/ConfirmationModal";
import { useState } from "react";

export default function Settings() {
  const { logout } = useAuth();
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const handleDeleteAccount = async () => {
    try {
      setDeleting(true);

      await deleteAccount();

      notify.success("Account deleted successfully.");

      logout();
    } catch (error) {
      notify.error("Unable to delete account.");
    } finally {
      setDeleting(false);
      setShowDeleteModal(false);
    }
  };

  return (
    <AppLayout>
      <section>
        <div className="flex items-center gap-3">
          <h1 className="font-heading text-4xl font-bold text-primary-dark sm:text-5xl lg:text-6xl">
            Settings
          </h1>
        </div>

        <p className="mt-3 text-base text-text-secondary sm:text-lg lg:text-xl">
          Manage your account settings.
        </p>
      </section>

      <div className="mt-10 max-w-5xl rounded-3xl bg-white p-5 shadow-sm sm:p-6 lg:p-8">
        <div className="rounded-2xl border border-red-200 bg-red-50 p-5 sm:p-6">
          <h2 className="font-heading text-xl font-bold text-red-700 sm:text-2xl">
            Danger Zone
          </h2>

          <p className="mt-3 text-sm leading-6 text-red-600 sm:text-base">
            Permanently delete your REMINDR account. This removes your
            reminders, processed emails, disconnects Gmail notifications and
            cannot be undone.
          </p>

          <button
            onClick={() => setShowDeleteModal(true)}
            className="mt-5 w-full rounded-xl bg-red-600 px-6 py-3 text-base font-semibold text-white transition hover:bg-red-700 sm:w-auto sm:px-7 sm:py-3"
          >
            Delete Account
          </button>
        </div>
      </div>
      <ConfirmationModal
        open={showDeleteModal}
        title="Delete Account"
        message="This will permanently delete your REMINDR account."
        description="All reminders, preparation tasks, processed emails and account data will be permanently deleted. This action cannot be undone."
        confirmText="Delete Account"
        cancelText="Cancel"
        loading={deleting}
        onCancel={() => {
          if (!deleting) setShowDeleteModal(false);
        }}
        onConfirm={handleDeleteAccount}
      />
    </AppLayout>
  );
}
