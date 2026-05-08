import type { Prompt, Collection } from "../types";

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "/api";

async function safeJson<T>(response: Response): Promise<T | null> {
  try {
    return (await response.json()) as T;
  } catch {
    return null;
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const payload = await safeJson<{ detail?: string; message?: string }>(response);
    const message = payload?.detail || payload?.message || response.statusText;
    throw new Error(message || "Request failed");
  }
  return response.json() as Promise<T>;
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      headers: {
        "Content-Type": "application/json",
        ...(options?.headers ?? {})
      },
      ...options
    });
    return handleResponse<T>(response);
  } catch (error) {
    if (error instanceof TypeError) {
      throw new Error("Network error. Confirm the backend is running and the dev server proxy is enabled.");
    }
    throw error;
  }
}

export async function fetchHello(): Promise<{ message: string }> {
  return request("/hello");
}

export async function getPrompts(collectionId?: string, search?: string): Promise<Prompt[]> {
  const params = new URLSearchParams();
  if (collectionId) params.set("collectionId", collectionId);
  if (search) params.set("search", search);
  return request(`/prompts${params.toString() ? `?${params}` : ""}`);
}

export async function getPrompt(id: string): Promise<Prompt> {
  return request(`/prompts/${id}`);
}

export async function createPrompt(prompt: Omit<Prompt, "createdAt">): Promise<Prompt> {
  return request("/prompts", {
    method: "POST",
    body: JSON.stringify(prompt)
  });
}

export async function updatePrompt(id: string, prompt: Omit<Prompt, "createdAt">): Promise<Prompt> {
  return request(`/prompts/${id}`, {
    method: "PATCH",
    body: JSON.stringify(prompt)
  });
}

export async function deletePrompt(id: string): Promise<void> {
  await request<void>(`/prompts/${id}`, { method: "DELETE" });
}

export async function getCollections(): Promise<Collection[]> {
  return request("/collections");
}

export async function createCollection(
  collection: Omit<Collection, "promptCount">
): Promise<Collection> {
  return request("/collections", {
    method: "POST",
    body: JSON.stringify(collection)
  });
}

export async function updateCollection(
  id: string,
  collection: Omit<Collection, "promptCount">
): Promise<Collection> {
  return request(`/collections/${id}`, {
    method: "PATCH",
    body: JSON.stringify(collection)
  });
}