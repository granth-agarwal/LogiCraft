import type { Config } from "tailwindcss";
export default {darkMode:["class"],content:["./app/**/*.{ts,tsx}","./components/**/*.{ts,tsx}"],theme:{extend:{colors:{background:"hsl(var(--background))",foreground:"hsl(var(--foreground))",card:"hsl(var(--card))",border:"hsl(var(--border))",accent:"hsl(var(--accent))"},borderRadius:{xl:"14px"},boxShadow:{panel:"0 18px 55px rgb(0 0 0 / .28)"}}},plugins:[]} satisfies Config;

