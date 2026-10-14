import { supabase } from "./supabase";
const base = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";
export class ApiError extends Error { constructor(public status:number, public details:unknown){super("API request failed")} }
export async function api<T>(path:string, init:RequestInit={}):Promise<T>{
  const {data:{session}}=await supabase().auth.getSession();
  const response=await fetch(`${base}${path}`,{...init,headers:{"Content-Type":"application/json",...(session?{Authorization:`Bearer ${session.access_token}`}:{ }),...init.headers}});
  if(!response.ok) throw new ApiError(response.status,await response.json().catch(()=>null));
  return response.status===204 ? undefined as T : response.json() as Promise<T>;
}

