"use client";
import {FormEvent, ReactNode, useCallback, useEffect, useState} from "react";
import {Loader2, Plus} from "lucide-react";
import {toast} from "sonner";
import {ApiError, api} from "@/lib/api";
import type {Page} from "@/lib/types";
import {DataTable, type Column} from "./data-table";
import {SlideOver} from "./slide-over";
export interface Field { name:string; label:string; type?:"text"|"number"|"date"|"datetime-local"|"select"|"json"; required?:boolean; options?:{label:string;value:string}[] }
export function ResourcePage<T extends {id:number}>({title, description, endpoint, columns, fields, editable=true, creatable=true, details}: {
  title:string; description:string; endpoint:string; columns:Column<T>[]; fields:Field[];
  editable?:boolean; creatable?:boolean; details?:(row:T)=>ReactNode;
}) {
  const [rows,setRows]=useState<T[]>([]);
  const [loading,setLoading]=useState(true);
  const [saving,setSaving]=useState(false);
  const [error,setError]=useState("");
  const [open,setOpen]=useState(false);
  const [editing,setEditing]=useState<T|null>(null);
  const load=useCallback(()=>{
    setLoading(true);
    (async()=>{
      const records:T[]=[];
      let page=1;
      let result:Page<T>;
      do {
        result=await api<Page<T>>(page===1?endpoint:`${endpoint}${endpoint.includes("?")?"&":"?"}page=${page}`);
        records.push(...result.results);page++;
      } while(result.next);
      return records;
    })().then(setRows).catch(()=>toast.error(`Could not load ${title.toLowerCase()}`)).finally(()=>setLoading(false));
  },[endpoint,title]);
  useEffect(()=>{load();window.addEventListener("logicraft:updated",load);return ()=>window.removeEventListener("logicraft:updated",load)},[load]);
  async function submit(e:FormEvent<HTMLFormElement>) {
    e.preventDefault();setSaving(true);setError("");
    const raw=Object.fromEntries(new FormData(e.currentTarget));
    const values:Record<string,unknown>={...raw};
    for(const field of fields) {
      const value=raw[field.name];
      if(value===""&&!field.required){delete values[field.name];continue}
      if(field.type==="number"&&value!=="")values[field.name]=Number(value);
      if(field.type==="datetime-local"&&typeof value==="string"&&value)values[field.name]=new Date(value).toISOString();
      if(field.type==="json"&&typeof value==="string")try{values[field.name]=JSON.parse(value)}catch{setError(`${field.label} must be valid JSON.`);setSaving(false);return}
    }
    try {
      await api<T>(editing?`${endpoint}${editing.id}/`:endpoint,{method:editing?"PATCH":"POST",body:JSON.stringify(values)});
      toast.success(`${title} saved`);setOpen(false);setEditing(null);load();
    } catch(cause) {setError(cause instanceof ApiError?cause.message:"Could not save this record.");toast.error("Save failed")}
    finally {setSaving(false)}
  }
  async function remove() {
    if(!editing||!window.confirm("Delete this record?"))return;
    setSaving(true);
    try {await api(`${endpoint}${editing.id}/`,{method:"DELETE"});setOpen(false);setEditing(null);load()}
    catch(cause) {setError(cause instanceof ApiError?cause.message:"Could not delete this record.")}
    finally {setSaving(false)}
  }
  function initialValue(field:Field) {
    if(!editing)return "";
    const value=editing[field.name as keyof T];
    if(field.type==="json")return JSON.stringify(value);
    if(field.type==="datetime-local"&&value){const date=new Date(String(value));return new Date(date.getTime()-date.getTimezoneOffset()*60000).toISOString().slice(0,16)}
    return String(value??"");
  }
  return <>
    <header className="mb-6 flex items-end justify-between"><div><h2 className="text-2xl font-semibold tracking-tight">{title}</h2><p className="mt-1 text-sm text-zinc-500">{description}</p></div>{creatable?<button onClick={()=>{setEditing(null);setError("");setOpen(true)}} className="flex items-center gap-2 rounded-lg bg-violet-600 px-3 py-2 text-sm font-medium text-white"><Plus size={16}/>Add</button>:null}</header>
    <DataTable rows={rows} columns={[{key:"id",label:"ID"},...columns]} loading={loading} onRow={editable||details?row=>{setEditing(row);setError("");setOpen(true)}:undefined}/>
    <SlideOver open={open} title={`${editing?editable?"Edit":"View":"Create"} ${title}`} onClose={()=>setOpen(false)}>
      {editing&&details?details(editing):null}
      {editable||!editing?<form onSubmit={submit} className="space-y-4">{fields.map(f=><label key={f.name} className="block text-sm">{f.label}{f.type==="select"?<select name={f.name} required={f.required} defaultValue={initialValue(f)} className="mt-2 w-full rounded-lg border bg-background px-3 py-2"><option value="">Select…</option>{f.options?.map(o=><option key={o.value} value={o.value}>{o.label}</option>)}</select>:<input name={f.name} type={f.type==="json"?"text":f.type??"text"} step={f.type==="number"?"any":undefined} required={f.required} defaultValue={initialValue(f)} className="mt-2 w-full rounded-lg border bg-transparent px-3 py-2"/>}</label>)}{error?<p role="alert" className="rounded-lg bg-rose-500/10 px-3 py-2 text-sm text-rose-400">{error}</p>:null}<button disabled={saving} className="flex w-full justify-center rounded-lg bg-violet-600 py-2.5 text-white disabled:opacity-60">{saving?<Loader2 className="animate-spin"/>:"Save changes"}</button>{editing?<button type="button" disabled={saving} onClick={remove} className="w-full rounded-lg border border-rose-500 py-2 text-rose-500">Delete record</button>:null}</form>:null}
    </SlideOver>
  </>;
}
