export type Role = "admin"|"fleet_manager"|"warehouse_staff"|"customer";
export type VehicleStatus = "active"|"maintenance"|"idle"|"retired";
export type ShipmentStatus = "pending"|"picked_up"|"in_transit"|"delivered"|"failed";
export type BookingStatus = "booked"|"cancelled"|"completed";
export interface Page<T>{count:number;next:string|null;previous:string|null;results:T[]}
export interface Profile{id:number;supabase_user_id:string;email?:string;full_name:string;role:Role;phone:string;warehouse:number|null;created_at:string}
export interface Driver{id:number;profile:number;license_number:string;license_expiry:string;status:"available"|"on_trip"|"off_duty"}
export interface Vehicle{id:number;registration_number:string;type:"truck"|"van"|"bus";capacity_kg:string;status:VehicleStatus;current_driver:number|null}
export interface Trip{id:number;vehicle:number;driver:number;start_location:string;end_location:string;start_time:string;end_time:string|null;distance_km:string;status:"scheduled"|"in_progress"|"completed"|"cancelled";route_points:{lat:number;lng:number}[]}
export interface MaintenanceRecord{id:number;vehicle:number;service_date:string;next_due_date:string;description:string;cost:string}
export interface Warehouse{id:number;name:string;address:string;capacity_units:number;manager:number}
export interface InventoryItem{id:number;sku:string;name:string;category:string;quantity:number;reorder_threshold:number;warehouse:number}
export interface StockMovement{id:number;item:number;warehouse:number;movement_type:"inbound"|"outbound";quantity:number;reason:string;created_by:number;created_at:string}
export interface ShipmentEvent{id:number;shipment:number;status:ShipmentStatus;timestamp:string;note:string}
export interface Shipment{id:number;tracking_id:string;origin:string;destination:string;vehicle:number|null;driver:number|null;status:ShipmentStatus;linked_item:number|null;quantity:number;created_by:number;created_at:string;events:ShipmentEvent[]}
export interface Route{id:number;name:string;stops:string[];estimated_duration_minutes:number}
export interface Schedule{id:number;route:number;departure_time:string;vehicle:number;capacity:number}
export interface Booking{id:number;schedule:number;customer:number;seat_number:number;status:BookingStatus;fare:string;created_at:string}
export interface Notification{id:number;recipient:number;message:string;type:"shipment_update"|"low_stock"|"booking_confirmed";is_read:boolean;created_at:string}
export interface Summary{active_vehicles:number;pending_shipments:number;low_stock_items:number;todays_bookings:number}
export interface StatusCount{status:ShipmentStatus;count:number}
export interface RevenuePoint{day:string;revenue:string}

