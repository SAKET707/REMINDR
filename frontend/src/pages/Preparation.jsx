import { useEffect, useState } from "react";
import { Pencil } from "lucide-react";
import AppLayout from "../layouts/AppLayout";
import { useReminder } from "../context/useReminder";
import AIPreparationModal from "../components/preparation/AIPreparationModal";
import { LoaderCircle } from "lucide-react";

import {
  getPreparationTasks,
  createPreparationTask,
  updatePreparationTask,
  deletePreparationTask,
  generatePreparationSuggestions,
} from "../services/preparation";
import { Trash2 } from "lucide-react";

export default function Preparation() {
  const { reminders, loading } = useReminder();

  const [tasksByReminder, setTasksByReminder] = useState({});

  const [loadingTasks, setLoadingTasks] = useState(true);
  const [addingReminderId, setAddingReminderId] = useState(null);
  const [newTaskTitle, setNewTaskTitle] = useState("");
  const [creatingTask, setCreatingTask] = useState(false);

  const [editingTaskId, setEditingTaskId] = useState(null);
  const [editingTitle, setEditingTitle] = useState("");

  const [showAiModal, setShowAiModal] = useState(false);
  const [selectedReminderId, setSelectedReminderId] = useState(null);

  const [aiSuggestions, setAiSuggestions] = useState([]);
  const [generatingAI, setGeneratingAI] = useState(false);

  useEffect(() => {
    if (loading) return;

    async function loadTasks() {
      try {
        const tasks = await getPreparationTasks();

        const taskMap = {};

        tasks.forEach((task) => {
          if (!taskMap[task.reminder_id]) {
            taskMap[task.reminder_id] = [];
          }

          taskMap[task.reminder_id].push(task);
        });

        setTasksByReminder(taskMap);
      } finally {
        setLoadingTasks(false);
      }
    }

    loadTasks();
  }, [loading, reminders]);

  async function handleCreateTask(reminderId) {
    const title = newTaskTitle.trim();

    if (!title) return;

    try {
      setCreatingTask(true);

      const task = await createPreparationTask(reminderId, title);

      setTasksByReminder((prev) => ({
        ...prev,
        [reminderId]: [...(prev[reminderId] ?? []), task],
      }));

      setNewTaskTitle("");
      setAddingReminderId(null);
    } catch (error) {
      console.error(error);
    } finally {
      setCreatingTask(false);
    }
  }

  async function handleToggleTask(taskId, completed, reminderId) {
    try {
      await updatePreparationTask(taskId, {
        completed: !completed,
      });

      setTasksByReminder((prev) => ({
        ...prev,
        [reminderId]: prev[reminderId].map((task) =>
          task.id === taskId
            ? {
                ...task,
                completed: !completed,
              }
            : task,
        ),
      }));
    } catch (error) {
      console.error(error);
    }
  }

  async function handleEditTask(task) {
    const title = editingTitle.trim();

    if (!title) {
      setEditingTaskId(null);
      setEditingTitle("");
      return;
    }

    if (title === task.title) {
      setEditingTaskId(null);
      setEditingTitle("");
      return;
    }

    try {
      await updatePreparationTask(task.id, {
        title,
      });

      setTasksByReminder((prev) => ({
        ...prev,
        [task.reminder_id]: prev[task.reminder_id].map((t) =>
          t.id === task.id
            ? {
                ...t,
                title,
              }
            : t,
        ),
      }));
    } catch (err) {
      console.error(err);
    }

    setEditingTaskId(null);
    setEditingTitle("");
  }

  async function handleDeleteTask(task) {
    const confirmed = window.confirm(
      "Are you sure you want to delete this task?",
    );

    if (!confirmed) return;

    try {
      await deletePreparationTask(task.id);

      setTasksByReminder((prev) => ({
        ...prev,
        [task.reminder_id]: prev[task.reminder_id].filter(
          (t) => t.id !== task.id,
        ),
      }));
    } catch (error) {
      console.error(error);
    }
  }

  async function handleGenerateAI(reminderId) {
    try {
      setSelectedReminderId(reminderId); // Move here
      setGeneratingAI(true);

      const suggestions = await generatePreparationSuggestions(reminderId);

      setAiSuggestions(suggestions);
      setShowAiModal(true);
    } catch (error) {
      console.error(error);
    } finally {
      setGeneratingAI(false);
    }
  }

  async function handleAddAiTask(title) {
    try {
      const task = await createPreparationTask(selectedReminderId, title);

      setTasksByReminder((prev) => ({
        ...prev,
        [selectedReminderId]: [...(prev[selectedReminderId] ?? []), task],
      }));
    } catch (error) {
      console.error(error);
      throw error;
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
          Preparation
        </h1>

        <p className="mt-3 text-base text-text-secondary sm:text-lg lg:text-xl">
          Organize everything you need before your reminders.
        </p>
      </section>

      <section className="mt-10 space-y-6">
        {reminders.map((reminder) => (
          <div
            key={reminder.id}
            className="rounded-2xl border border-border bg-card p-6 shadow-sm"
          >
            <h2 className="font-heading text-xl font-semibold text-primary-dark sm:text-2xl">
              {reminder.email.summary}
            </h2>

            <div className="mt-5">
              {tasksByReminder[reminder.id]?.length ? (
                <ul className="space-y-3">
                  {tasksByReminder[reminder.id].map((task) => (
                    <li
                      key={task.id}
                      className="flex flex-col gap-3 sm:flex-row sm:items-center"
                    >
                      <div className="flex min-w-0 flex-1 items-center gap-3">
                        <input
                          type="checkbox"
                          checked={task.completed}
                          onChange={() =>
                            handleToggleTask(
                              task.id,
                              task.completed,
                              reminder.id,
                            )
                          }
                          className="h-4 w-4 cursor-pointer accent-primary"
                        />

                        {editingTaskId === task.id ? (
                          <input
                            autoFocus
                            value={editingTitle}
                            onChange={(e) => setEditingTitle(e.target.value)}
                            onBlur={() => handleEditTask(task)}
                            onKeyDown={(e) => {
                              if (e.key === "Enter") {
                                handleEditTask(task);
                              }

                              if (e.key === "Escape") {
                                setEditingTaskId(null);
                                setEditingTitle("");
                              }
                            }}
                            className="min-w-0 flex-1 rounded-md border border-border px-2 py-1 text-sm sm:text-base outline-none focus:border-primary"
                          />
                        ) : (
                          <span
                            className={`min-w-0 flex-1 break-words text-sm sm:text-base transition-all duration-200 decoration-1 ${
                              task.completed
                                ? "line-through text-text-secondary opacity-60"
                                : "text-primary-dark"
                            }`}
                          >
                            {task.title}
                          </span>
                        )}
                      </div>

                      <div className="flex gap-2 sm:ml-auto">
                        <button
                          onClick={() => {
                            setEditingTaskId(task.id);
                            setEditingTitle(task.title);
                          }}
                          className="flex-1 sm:flex-none flex items-center justify-center gap-1 rounded-xl border border-border px-3 py-1.5 text-sm font-medium text-primary transition hover:bg-background-soft"
                        >
                          <Pencil size={16} />
                          <span>Edit</span>
                        </button>

                        <button
                          onClick={() => handleDeleteTask(task)}
                          className="flex-1 sm:flex-none flex items-center justify-center gap-1 rounded-xl border border-red-300 px-3 py-1.5 text-sm font-medium text-red-600 transition hover:bg-red-50"
                        >
                          <Trash2 size={16} />
                          <span>Delete</span>
                        </button>
                      </div>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-text-secondary">No preparation tasks yet.</p>
              )}

              <div className="mt-5">
                {addingReminderId === reminder.id ? (
                  <div className="space-y-3">
                    <input
                      type="text"
                      value={newTaskTitle}
                      onChange={(e) => setNewTaskTitle(e.target.value)}
                      placeholder="Enter task..."
                      className="w-full rounded-lg border border-border px-4 py-2 outline-none focus:border-primary"
                    />

                    <div className="flex gap-3">
                      <button
                        onClick={() => handleCreateTask(reminder.id)}
                        disabled={creatingTask}
                        className="rounded-xl bg-primary px-4 py-2 text-sm font-medium text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
                      >
                        {creatingTask ? "Saving..." : "Save"}
                      </button>

                      <button
                        onClick={() => {
                          setAddingReminderId(null);
                          setNewTaskTitle("");
                        }}
                        className="rounded-xl border border-border bg-card px-4 py-2 text-sm font-medium text-primary-dark transition hover:bg-background-soft"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="flex flex-wrap gap-3">
                    <button
                      onClick={() => setAddingReminderId(reminder.id)}
                      className="rounded-xl bg-primary px-4 py-2 text-sm font-medium text-white transition hover:opacity-90"
                    >
                      + Add Task
                    </button>

                    <button
                      onClick={() => handleGenerateAI(reminder.id)}
                      disabled={generatingAI}
                      className="rounded-xl border border-primary px-4 py-2 text-sm font-medium text-primary transition hover:bg-background-soft disabled:cursor-not-allowed disabled:opacity-50"
                    >
                      {generatingAI && selectedReminderId === reminder.id ? (
                        <span className="flex items-center gap-2">
                          <LoaderCircle size={16} className="animate-spin" />
                          Generating...
                        </span>
                      ) : (
                        <span className="flex items-center gap-2">
                          <span>Generate with AI</span>
                        </span>
                      )}
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </section>

      <AIPreparationModal
        open={showAiModal}
        reminderId={selectedReminderId}
        suggestions={aiSuggestions}
        onClose={() => {
          setShowAiModal(false);
          setAiSuggestions([]);
          setSelectedReminderId(null);
        }}
        onAdd={handleAddAiTask}
      />
    </AppLayout>
  );
}
