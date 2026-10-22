// The public demo is read-only unless writes are explicitly enabled at build time.
// The backend must enforce this too: hiding controls is not access control.
export const DEMO_ALLOW_WRITES = process.env.NEXT_PUBLIC_DEMO_ALLOW_WRITES === "1";

export const READ_ONLY_NOTE = "Read-only public demo: saving and editing are disabled.";
