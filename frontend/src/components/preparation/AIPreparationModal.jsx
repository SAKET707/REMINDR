import { useEffect, useState } from "react";
import { X, Plus, Check, LoaderCircle } from "lucide-react";

export default function AIPreparationModal({
  open,
  onClose,
  reminderId,
  suggestions,
  onAdd,
}) {
  const [items, setItems] = useState([]);
  const [addingIndex, setAddingIndex] = useState(null);

  useEffect(() => {
    setItems(
      suggestions.map((text) => ({
        text,
        added: false,
      })),
    );
  }, [suggestions]);

  if (!open) return null;

  async function handleAdd(index) {
    if (items[index].added) return;

    try {
      setAddingIndex(index);

      await onAdd(items[index].text);

      setItems((prev) =>
        prev.map((item, i) =>
          i === index
            ? {
                ...item,
                added: true,
              }
            : item,
        ),
      );
    } finally {
      setAddingIndex(null);
    }
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4"
      onClick={onClose}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="max-h-[80vh] w-full max-w-2xl overflow-y-auto rounded-2xl bg-white p-6 shadow-xl"
      >
        <div className="flex items-start justify-between">
          <div>
            <h2 className="font-heading text-2xl font-bold text-primary-dark">
              AI Preparation Suggestions
            </h2>

            <p className="mt-2 text-sm text-text-secondary">
              Review, edit and add only the tasks you need.
            </p>
          </div>

          <button
            onClick={onClose}
            className="rounded-lg p-2 transition hover:bg-background-soft"
          >
            <X size={20} />
          </button>
        </div>

        <div className="mt-8 space-y-4">
          {items.map((item, index) => (
            <div
              key={index}
              className="flex items-center gap-4 rounded-xl border border-border p-3"
            >
              <input
                value={item.text}
                disabled={item.added}
                onChange={(e) => {
                  const value = e.target.value;

                  setItems((prev) =>
                    prev.map((task, i) =>
                      i === index
                        ? {
                            ...task,
                            text: value,
                          }
                        : task,
                    ),
                  );
                }}
                className={`flex-1 bg-transparent outline-none ${
                  item.added
                    ? "line-through text-text-secondary opacity-50"
                    : "text-primary-dark"
                }`}
              />

              <button
                disabled={item.added || addingIndex === index}
                onClick={() => handleAdd(index)}
                className={`flex min-w-[95px] items-center justify-center gap-2 rounded-xl px-4 py-2 text-sm font-medium transition ${
                  item.added
                    ? "cursor-default bg-green-600 text-white"
                    : "bg-primary text-white hover:opacity-90"
                }`}
              >
                {addingIndex === index ? (
                  <>
                    <LoaderCircle className="animate-spin" size={16} />
                  </>
                ) : item.added ? (
                  <>
                    <Check size={16} />
                    Added
                  </>
                ) : (
                  <>
                    <Plus size={16} />
                    Add
                  </>
                )}
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
