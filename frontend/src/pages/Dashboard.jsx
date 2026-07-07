import AppLayout from "../layouts/AppLayout";
import TelegramBanner from "../components/dashboard/TelegramBanner";
import ReminderCard from "../components/dashboard/ReminderCard";
import { useAuth } from "../context/useAuth";
import { useReminder } from "../context/useReminder";

export default function Dashboard() {
  const { user, loading: authLoading } = useAuth();
  const { reminders, loading: remindersLoading } = useReminder();

  if (authLoading || remindersLoading) {
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
        Dashboard
      </h1>

      <p className="mt-3 text-3xl text-text-secondary">
        Welcome back, <span className="font-semibold">{user?.name}</span>.
      </p>

      {!user?.telegram_chat_id && (
        <div className="mt-10">
          <TelegramBanner />
        </div>
      )}

      <div className="mt-12">
        <h2 className="mb-6 font-heading text-4xl font-semibold text-primary-dark">
          Upcoming Reminders
        </h2>

        <div className="space-y-5">
          {reminders.length === 0 ? (
            <p className="text-xl text-text-secondary">
              No upcoming reminders.
            </p>
          ) : (
            reminders.map((reminder) => (
              <ReminderCard key={reminder.id} reminder={reminder} />
            ))
          )}
        </div>
      </div>
    </AppLayout>
  );
}
