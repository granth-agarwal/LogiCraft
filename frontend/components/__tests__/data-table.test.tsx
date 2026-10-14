import {fireEvent,render,screen} from "@testing-library/react";
import {describe,expect,it} from "vitest";
import {DataTable} from "../data-table";
const rows=[{id:1,name:"Zulu"},{id:2,name:"Alpha"}];
describe("DataTable",()=>{it("filters records",()=>{render(<DataTable rows={rows} columns={[{key:"name",label:"Name"}]}/>);fireEvent.change(screen.getByLabelText("Search"),{target:{value:"Alpha"}});expect(screen.getByText("Alpha")).toBeInTheDocument();expect(screen.queryByText("Zulu")).not.toBeInTheDocument()});it("sorts records",()=>{render(<DataTable rows={rows} columns={[{key:"name",label:"Name"}]}/>);fireEvent.click(screen.getByRole("button",{name:/Name/}));expect(screen.getAllByRole("row")[1]).toHaveTextContent("Zulu")})});
