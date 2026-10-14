import {NextResponse} from "next/server";
import {createServerClient,type CookieOptions} from "@supabase/ssr";
import {cookies} from "next/headers";
export async function GET(request:Request){const url=new URL(request.url);const code=url.searchParams.get("code");const store=await cookies();if(code){const client=createServerClient(process.env.NEXT_PUBLIC_SUPABASE_URL!,process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,{cookies:{getAll:()=>store.getAll(),setAll:(items:{name:string;value:string;options:CookieOptions}[])=>items.forEach(({name,value,options})=>store.set(name,value,options))}});await client.auth.exchangeCodeForSession(code)}return NextResponse.redirect(new URL("/",url.origin))}
