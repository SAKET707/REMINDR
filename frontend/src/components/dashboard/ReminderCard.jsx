export default function ReminderCard({ reminder }) {
  return (
    <div className="rounded-2xl border border-border bg-white p-8 shadow-sm">
      <h3 className="font-heading text-2xl font-semibold text-primary-dark">
        {reminder.email.subject}
      </h3>

      <p className="mt-3 text-lg text-text-secondary">
        {reminder.email.summary}
      </p>

      <p className="mt-5 text-lg font-medium text-primary">
        {new Date(reminder.scheduled_for).toLocaleString()}
      </p>
    </div>
  );
}
