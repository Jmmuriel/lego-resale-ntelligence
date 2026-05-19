"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { Route } from "next";

const MarketIcon = () => (
  <svg className="nav-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
    <polyline points="1,11 5,7 8,9 11,5 15,3" />
  </svg>
);

const AnalyzeIcon = () => (
  <svg className="nav-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
    <circle cx="6.5" cy="6.5" r="4.5" />
    <line x1="10" y1="10" x2="14" y2="14" />
  </svg>
);

const WatchlistIcon = () => (
  <svg className="nav-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
    <path d="M3 2h10a1 1 0 0 1 1 1v12l-6-3-6 3V3a1 1 0 0 1 1-1z" />
  </svg>
);

const SetsIcon = () => (
  <svg className="nav-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
    <rect x="1" y="1" width="6" height="6" rx="1" />
    <rect x="9" y="1" width="6" height="6" rx="1" />
    <rect x="1" y="9" width="6" height="6" rx="1" />
    <rect x="9" y="9" width="6" height="6" rx="1" />
  </svg>
);

const ResearchIcon = () => (
  <svg className="nav-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
    <path d="M8 1v6l3 1.5" />
    <circle cx="8" cy="10" r="5" />
  </svg>
);

const PortfolioIcon = () => (
  <svg className="nav-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
    <rect x="1" y="5" width="14" height="10" rx="1" />
    <path d="M5 5V4a3 3 0 0 1 6 0v1" />
    <line x1="8" y1="9" x2="8" y2="11" />
  </svg>
);

const BriefingsIcon = () => (
  <svg className="nav-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
    <rect x="2" y="1" width="12" height="14" rx="1" />
    <line x1="5" y1="5" x2="11" y2="5" />
    <line x1="5" y1="8" x2="11" y2="8" />
    <line x1="5" y1="11" x2="8" y2="11" />
  </svg>
);

const items: Array<{ href: Route; label: string; icon: React.ReactNode }> = [
  { href: "/",           label: "Market",     icon: <MarketIcon /> },
  { href: "/analyze",    label: "Analyze",    icon: <AnalyzeIcon /> },
  { href: "/watchlist",  label: "Watchlist",  icon: <WatchlistIcon /> },
  { href: "/sets",       label: "Sets",       icon: <SetsIcon /> },
  { href: "/research",   label: "Research",   icon: <ResearchIcon /> },
  { href: "/portfolio",  label: "Portfolio",  icon: <PortfolioIcon /> },
  { href: "/briefings",  label: "Briefings",  icon: <BriefingsIcon /> }
];

export default function SidebarNav() {
  const pathname = usePathname();

  return (
    <nav className="nav-list" aria-label="Primary navigation">
      {items.map((item) => (
        <li key={item.href} style={{ listStyle: "none" }}>
          <Link
            aria-current={pathname === item.href ? "page" : undefined}
            className={pathname === item.href ? "active" : undefined}
            href={item.href}
          >
            {item.icon}
            {item.label}
          </Link>
        </li>
      ))}
    </nav>
  );
}
