import * as React from "react";
import {cva,type VariantProps} from "class-variance-authority";
import {cn} from "@/lib/utils";
const styles=cva("focus-ring inline-flex items-center justify-center gap-2 rounded-lg text-sm font-medium transition disabled:pointer-events-none disabled:opacity-50",{variants:{variant:{default:"bg-violet-600 text-white hover:bg-violet-500",outline:"border bg-transparent hover:bg-zinc-500/10",ghost:"hover:bg-zinc-500/10"},size:{default:"h-10 px-4",sm:"h-8 px-3",icon:"size-9"}},defaultVariants:{variant:"default",size:"default"}});
export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>,VariantProps<typeof styles>{}
export function Button({className,variant,size,...props}:ButtonProps){return <button className={cn(styles({variant,size}),className)} {...props}/>}

