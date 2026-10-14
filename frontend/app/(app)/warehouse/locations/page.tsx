"use client";
import {ResourcePage} from "@/components/resource-page";import {ModuleTabs} from "@/components/module-tabs";import type {Warehouse} from "@/lib/types";
const tabs=[{label:"Inventory",href:"/warehouse"},{label:"Locations",href:"/warehouse/locations"},{label:"Movements",href:"/warehouse/movements"}];
export default function Page(){return <><ModuleTabs items={tabs}/><ResourcePage<Warehouse> title="Warehouses" description="Storage locations and assigned managers." endpoint="/warehouse/warehouses/" columns={[{key:"name",label:"Name"},{key:"address",label:"Address"},{key:"capacity_units",label:"Capacity"},{key:"manager",label:"Manager"}]} fields={[{name:"name",label:"Name",required:true},{name:"address",label:"Address",required:true},{name:"capacity_units",label:"Capacity units",type:"number",required:true},{name:"manager",label:"Manager profile ID",type:"number",required:true}]}/></>}

