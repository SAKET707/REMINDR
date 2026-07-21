import React from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import { AuthProvider } from "./context/AuthContext";
import { ReminderProvider } from "./context/ReminderContext";
import { SidebarProvider } from "./context/SidebarContext";
import { Toaster } from "react-hot-toast";

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <AuthProvider>
      <ReminderProvider>
        <SidebarProvider>
          <App />

          <Toaster
            position="top-right"
            reverseOrder={false}
            gutter={10}
            toastOptions={{
              duration: 3500,

              style: {
                background: "#E6E2DA",
                color: "#101111",
                border: "1px solid #A6824A",
                borderRadius: "14px",
                padding: "16px",
                fontSize: "15px",
                fontWeight: "500",
              },

              success: {
                iconTheme: {
                  primary: "#154230",
                  secondary: "#E6E2DA",
                },
              },

              error: {
                iconTheme: {
                  primary: "#5D1E21",
                  secondary: "#E6E2DA",
                },
              },
            }}
          />
        </SidebarProvider>
      </ReminderProvider>
    </AuthProvider>
  </React.StrictMode>,
);
