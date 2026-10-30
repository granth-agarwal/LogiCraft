import { supabase, usesSupabase } from "./supabase";
export const apiBase = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";
export class ApiError extends Error {
  constructor(public status: number, public details: unknown) {
    super(typeof details === "string" ? details : JSON.stringify(details));
  }
}
export function csrfToken() {
  return typeof document === "undefined" ? "" : document.cookie.split("; ").find(x => x.startsWith("csrftoken="))?.split("=")[1] ?? "";
}
export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  const session = usesSupabase ? (await supabase().auth.getSession()).data.session : null;
  const response = await fetch(`${apiBase}${path}`, {
    ...init, credentials: "include", headers: {
      "Content-Type": "application/json", "X-CSRFToken": csrfToken(),
      ...(session ? { Authorization: `Bearer ${session.access_token}` } : {}), ...init.headers,
    },
  });
  if (!response.ok) throw new ApiError(response.status, await response.json().catch(() => "Request failed"));
  return response.status === 204 ? undefined as T : response.json() as Promise<T>;
}
