import Sidebar from "@/components/Sidebar";
import Topbar from "@/components/Topbar";
import ExpertAssistant from "@/components/ExpertAssistant";
import { ToastNotificationsProvider } from "@/components/ToastNotifications";
import { KeyboardShortcutHint } from "@/components/KeyboardShortcutHint";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <ToastNotificationsProvider>
      <div className="flex min-h-screen">
        <Sidebar />
        <div className="flex-1 flex flex-col min-w-0">
          <Topbar />
          <main className="flex-1 p-4 md:p-6 bg-slate-50">{children}</main>
        </div>
        <ExpertAssistant />
        {/* ToastNotifications stack is rendered by the provider above */}
      </div>
      <KeyboardShortcutHint />
    </ToastNotificationsProvider>
  );
}
