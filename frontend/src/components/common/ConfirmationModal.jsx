import { AlertTriangle, X } from "lucide-react";

export default function ConfirmationModal({
  open,
  title,
  message,
  description,
  confirmText = "Confirm",
  cancelText = "Cancel",
  onConfirm,
  onCancel,
  loading = false,
}) {
  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4"
      onClick={onCancel}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="w-full max-w-md rounded-2xl bg-white p-5 shadow-xl sm:p-6"
      >
        {/* Header */}
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-full bg-red-100">
              <AlertTriangle size={22} className="text-red-600" />
            </div>

            <div>
              <h2 className="font-heading text-xl font-bold text-primary-dark sm:text-2xl">
                {title}
              </h2>
            </div>
          </div>

          <button
            onClick={onCancel}
            className="rounded-lg p-2 transition hover:bg-background-soft"
          >
            <X size={20} />
          </button>
        </div>

        {/* Body */}

        <div className="mt-6 space-y-3">
          <p className="text-sm text-primary-dark sm:text-base">{message}</p>

          {description && (
            <p className="text-sm text-text-secondary sm:text-base">
              {description}
            </p>
          )}
        </div>

        {/* Buttons */}

        <div className="mt-8 flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
          <button
            onClick={onCancel}
            disabled={loading}
            className="rounded-xl border border-border px-5 py-2.5 font-medium transition hover:bg-background-soft disabled:opacity-50"
          >
            {cancelText}
          </button>

          <button
            onClick={onConfirm}
            disabled={loading}
            className="rounded-xl bg-red-600 px-5 py-2.5 font-medium text-white transition hover:bg-red-700 disabled:opacity-50"
          >
            {loading ? "Please wait..." : confirmText}
          </button>
        </div>
      </div>
    </div>
  );
}
