import AppLayout from "../layouts/AppLayout";
import ReminderCard from "../components/dashboard/ReminderCard";
import { useReminder } from "../context/useReminder";
import { deleteReminder } from "../services/reminder";
import { notify } from "../utils/toast";
import { useState } from "react";
import { updateReminder } from "../services/reminder";
import ConfirmationModal from "../components/common/ConfirmationModal";

export default function ManageReminders() {
  const { reminders, loading, removeReminder, replaceReminder } = useReminder();
  const [editingReminder, setEditingReminder] = useState(null);
  const [scheduledFor, setScheduledFor] = useState("");
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [reminderToDelete, setReminderToDelete] = useState(null);
  const [deletingReminder, setDeletingReminder] = useState(false);

  const [minDateTime] = useState(() => {
    return new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
      .toISOString()
      .slice(0, 16);
  });

  function handleEdit(reminder) {
    setEditingReminder(reminder);

    setScheduledFor(
      new Date(reminder.scheduled_for).toISOString().slice(0, 16),
    );
  }

  async function handleSave() {
    try {
      console.log("scheduledFor:", scheduledFor);
      console.log("ISO:", new Date(scheduledFor).toISOString());
      const updatedReminder = await updateReminder(
        editingReminder.id,
        new Date(scheduledFor).toISOString(),
      );

      replaceReminder(updatedReminder);

      notify.success("Reminder updated successfully.");

      setEditingReminder(null);
      setScheduledFor("");
    } catch (error) {
      console.error(error);
      notify.error("Failed to update reminder.");
    }
  }

  async function handleDelete() {
    if (!reminderToDelete) return;

    try {
      setDeletingReminder(true);

      await deleteReminder(reminderToDelete.id);

      removeReminder(reminderToDelete.id);

      notify.success("Reminder deleted successfully.");

      setShowDeleteModal(false);
      setReminderToDelete(null);
    } catch (error) {
      console.error(error);
      notify.error("Failed to delete reminder.");
    } finally {
      setDeletingReminder(false);
    }
  }

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background-soft">
        <h1 className="font-heading text-3xl font-bold text-primary-dark">
          Loading...
        </h1>
      </div>
    );
  }

  return (
    <AppLayout>
      <section>
        <h1 className="font-heading text-4xl font-bold text-primary-dark sm:text-5xl lg:text-6xl">
          Manage Reminders
        </h1>

        <p className="mt-3 text-base text-text-secondary sm:text-lg lg:text-xl">
          Edit or delete your scheduled reminders.
        </p>
      </section>

      <section className="mt-10 space-y-5">
        {reminders.length === 0 ? (
          <div className="rounded-2xl border border-border bg-card p-8 text-center shadow-sm">
            <p className="text-text-secondary">No reminders available.</p>
          </div>
        ) : (
          reminders.map((reminder) => (
            <ReminderCard
              key={reminder.id}
              reminder={reminder}
              editable
              onEdit={handleEdit}
              onDelete={(reminder) => {
                setReminderToDelete(reminder);
                setShowDeleteModal(true);
              }}
            />
          ))
        )}
      </section>

      {editingReminder && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
          <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl">
            <h2 className="font-heading text-2xl font-semibold text-primary-dark">
              Edit Reminder
            </h2>

            <p className="mt-2 text-sm text-text-secondary">
              Select a new reminder time.
            </p>

            <input
              type="datetime-local"
              value={scheduledFor}
              min={minDateTime}
              onChange={(e) => setScheduledFor(e.target.value)}
              className="mt-6 w-full rounded-xl border border-border p-3 outline-none focus:border-primary"
            />

            <div className="mt-8 flex justify-end gap-3">
              <button
                onClick={() => {
                  setEditingReminder(null);
                  setScheduledFor("");
                }}
                className="rounded-xl border border-border px-5 py-2"
              >
                Cancel
              </button>

              <button
                onClick={handleSave}
                className="rounded-xl bg-primary px-5 py-2 text-white hover:opacity-90"
              >
                Save Changes
              </button>
            </div>
          </div>
        </div>
      )}

      <ConfirmationModal
        open={showDeleteModal}
        title="Delete Reminder"
        message="Are you sure you want to delete this reminder?"
        description="This reminder will be permanently removed. This action cannot be undone."
        confirmText="Delete"
        cancelText="Cancel"
        loading={deletingReminder}
        onCancel={() => {
          if (!deletingReminder) {
            setShowDeleteModal(false);
            setReminderToDelete(null);
          }
        }}
        onConfirm={handleDelete}
      />
    </AppLayout>
  );
}
