import { Pencil, Trash2 } from "lucide-react";
export default function ReminderCard({
  reminder,
  editable = false,
  onEdit,
  onDelete,
}) {
  return (
    <div className="rounded-2xl border border-border bg-white p-4 shadow-sm transition-shadow duration-300 hover:shadow-md sm:p-5 lg:p-6">
      <h3 className="font-heading text-base font-semibold leading-snug text-primary-dark sm:text-lg lg:text-xl">
        {reminder.email.subject}
      </h3>

      <p className="mt-2 text-sm leading-6 text-text-secondary sm:text-[15px] lg:text-base">
        {reminder.email.summary}
      </p>

      <p className="mt-4 text-sm font-medium text-primary sm:text-[15px] lg:text-base">
        {new Date(reminder.scheduled_for).toLocaleString()}
      </p>

      {editable && (
        <div className="mt-5 flex flex-wrap gap-3">
          <button
            onClick={() => onEdit(reminder)}
            className="flex items-center gap-1 rounded-xl border border-border px-3 py-1.5 text-sm font-medium text-primary transition hover:bg-background-soft"
          >
            <Pencil size={16} />
            <span>Edit</span>
          </button>

          <button
            onClick={() => onDelete(reminder)}
            className="flex items-center gap-1 rounded-xl border border-red-300 px-3 py-1.5 text-sm font-medium text-red-600 transition hover:bg-red-50"
          >
            <Trash2 size={16} />
            <span>Delete</span>
          </button>
        </div>
      )}
    </div>
  );
}
