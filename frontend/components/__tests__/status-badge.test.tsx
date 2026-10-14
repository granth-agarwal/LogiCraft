import {render,screen} from "@testing-library/react";
import {describe,expect,it} from "vitest";
import {StatusBadge} from "../status-badge";
describe("StatusBadge",()=>{it.each([["active","text-emerald-400"],["maintenance","text-amber-400"],["failed","text-rose-400"],["in_transit","text-violet-400"],["cancelled","text-zinc-400"]] as const)("maps %s consistently",(status,color)=>{render(<StatusBadge status={status}/>);expect(screen.getByText(status.replaceAll("_"," "))).toHaveClass(color)})});

