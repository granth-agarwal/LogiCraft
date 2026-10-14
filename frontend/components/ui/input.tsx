import * as React from "react";
import {cn} from "@/lib/utils";
export function Input({className,...props}:React.InputHTMLAttributes<HTMLInputElement>){return <input className={cn("focus-ring h-10 w-full rounded-lg border bg-transparent px-3 text-sm",className)} {...props}/>}

