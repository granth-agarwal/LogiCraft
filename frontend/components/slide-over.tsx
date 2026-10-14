"use client";
import {X} from "lucide-react";
export function SlideOver({open,title,onClose,children}:{open:boolean;title:string;onClose:()=>void;children:React.ReactNode}){if(!open)return null;return <div role="dialog" aria-modal="true" className="fixed inset-0 z-50 bg-black/60" onMouseDown={onClose}><section onMouseDown={e=>e.stopPropagation()} className="ml-auto h-full w-full max-w-md overflow-y-auto border-l bg-card p-6 shadow-panel"><header className="mb-6 flex items-center justify-between"><h2 className="text-lg font-semibold">{title}</h2><button aria-label="Close" onClick={onClose} className="rounded-lg p-2 hover:bg-zinc-500/10"><X/></button></header>{children}</section></div>}

