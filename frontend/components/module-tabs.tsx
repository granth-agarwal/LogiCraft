import Link from "next/link";
export function ModuleTabs({items}:{items:{label:string;href:string}[]}){return <nav className="mb-5 flex gap-1 overflow-x-auto rounded-lg border bg-card p-1">{items.map(i=><Link key={i.href} href={i.href} className="whitespace-nowrap rounded-md px-3 py-1.5 text-sm text-zinc-500 hover:bg-zinc-500/10 hover:text-foreground">{i.label}</Link>)}</nav>}

