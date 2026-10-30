import {fireEvent, render, screen, waitFor} from "@testing-library/react";
import {beforeEach, describe, expect, it, vi} from "vitest";
import {ResourcePage} from "../resource-page";
import {RowAction} from "../row-action";
import {api} from "@/lib/api";
vi.mock("@/lib/api",()=>({api:vi.fn(),ApiError:class extends Error{}}));
type Row = {id:number;name:string};
const props = {title:"Vehicles", description:"Fleet", endpoint:"/fleet/vehicles/", columns:[{key:"name" as const,label:"Name"}],fields:[{name:"name",label:"Name",required:true}]};
const page = (results:Row[], next:string|null=null)=>({results,count:results.length,next,previous:null});
describe("Required UI operations",()=>{
  beforeEach(()=>vi.mocked(api).mockReset());
  it("deletes an existing vehicle",async()=>{
    vi.mocked(api).mockResolvedValue(page([{id:1,name:"Van"}]));
    vi.spyOn(window,"confirm").mockReturnValue(true);
    render(<ResourcePage<Row> {...props}/>);
    fireEvent.click(await screen.findByText("Van"));
    fireEvent.click(screen.getByRole("button",{name:"Delete record"}));
    await waitFor(()=>expect(api).toHaveBeenCalledWith("/fleet/vehicles/1/",{method:"DELETE"}));
    expect(window.confirm).toHaveBeenCalled();
    vi.restoreAllMocks();
  });
  it("loads records after the first API page",async()=>{
    vi.mocked(api).mockResolvedValueOnce(page([{id:1,name:"First"}],"http://localhost:8000/api/v1/fleet/vehicles/?page=2")).mockResolvedValueOnce(page([{id:2,name:"Second"}]));
    render(<ResourcePage<Row> {...props}/>);
    expect(await screen.findByText("Second")).toBeInTheDocument();
    expect(api).toHaveBeenCalledWith("/fleet/vehicles/?page=2");
  });
  it("refreshes rows after an action without opening the edit form",async()=>{
    vi.mocked(api).mockResolvedValue(page([{id:1,name:"Before"}]));
    render(<ResourcePage<Row> {...props} columns={[{key:"name",label:"Name"},{key:"id",label:"Action",render:()=> <RowAction label="Assign" title="Assign driver" endpoint="/fleet/vehicles/1/assign-driver/"/>}]}/>);
    fireEvent.click(await screen.findByRole("button",{name:"Assign"}));
    expect(screen.getAllByRole("dialog")).toHaveLength(1);
    vi.mocked(api).mockResolvedValueOnce({}).mockResolvedValue(page([{id:1,name:"After"}]));
    fireEvent.click(screen.getByRole("button",{name:"Confirm"}));
    expect(await screen.findByText("After")).toBeInTheDocument();
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });
});
