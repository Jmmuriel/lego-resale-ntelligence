import type { Metadata } from "next";
import SidebarNav from "@/components/SidebarNav";
import "./globals.css";

export const metadata: Metadata = {
  title: "LEGO Resale Intelligence V2",
  description: "Collector-grade market intelligence for retired LEGO sets."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <div className="app-shell">
          <aside className="sidebar">
            <div className="brand-lockup">
              <span className="brand-mark">LR</span>
              <div>
                <strong>LEGO Resale</strong>
                <small>Collector Terminal</small>
              </div>
            </div>
            <SidebarNav />
            <div className="sidebar-footer">V2 · alpha · local</div>
          </aside>
          <main className="main-stage">{children}</main>
        </div>
      </body>
    </html>
  );
}
