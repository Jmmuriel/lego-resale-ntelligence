// Keep in sync with getApiUrl() in src/lib/api.ts.
const LOCAL_API_URL = "http://127.0.0.1:8000";
const PUBLIC_API_URL = "https://lego-resale-ntelligence-production.up.railway.app";

const isDev = process.env.NODE_ENV === "development";

// Origins the browser may call from client components (analyze, set lookup, ...).
// NEXT_PUBLIC_API_URL is read at build time, like the client bundle does.
function apiOrigins() {
  if (process.env.NEXT_PUBLIC_API_URL) {
    return [new URL(process.env.NEXT_PUBLIC_API_URL).origin];
  }
  if (process.env.VERCEL === "1") {
    return [PUBLIC_API_URL];
  }
  return [PUBLIC_API_URL, LOCAL_API_URL];
}

const contentSecurityPolicy = [
  "default-src 'self'",
  // 'unsafe-inline' is required because Next.js injects inline bootstrap and
  // RSC payload scripts, and /analyze and /sets are prerendered as static HTML,
  // so a per-request nonce is not possible there. 'unsafe-eval' is only added
  // for `next dev` (React's dev tooling needs it).
  `script-src 'self' 'unsafe-inline'${isDev ? " 'unsafe-eval'" : ""}`,
  // Inline style attributes (React style props, recharts) + Google Fonts CSS.
  "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
  "font-src 'self' https://fonts.gstatic.com",
  "img-src 'self' data: blob:",
  `connect-src 'self' ${apiOrigins().join(" ")}${isDev ? " ws: wss:" : ""}`,
  "object-src 'none'",
  "base-uri 'self'",
  "form-action 'self'",
  "frame-ancestors 'none'"
].join("; ");

const securityHeaders = [
  { key: "Content-Security-Policy", value: contentSecurityPolicy },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" }
];

/** @type {import('next').NextConfig} */
const nextConfig = {
  poweredByHeader: false,
  typedRoutes: true,
  async headers() {
    return [{ source: "/:path*", headers: securityHeaders }];
  }
};

export default nextConfig;
