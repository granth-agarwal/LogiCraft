from django.db import migrations

TABLES = [
    "accounts_profile", "fleet_driver", "fleet_vehicle", "fleet_trip", "fleet_maintenancerecord",
    "warehouse_warehouse", "warehouse_inventoryitem", "warehouse_stockmovement",
    "shipments_shipment", "shipments_shipmentevent", "scheduling_route", "scheduling_schedule",
    "scheduling_booking", "notifications_notification",
]

PROFILE_ID = "(SELECT id FROM accounts_profile WHERE supabase_user_id = auth.uid())"
ROLE = "COALESCE((auth.jwt() -> 'app_metadata' ->> 'role'), (auth.jwt() ->> 'role'))"

def enable_rls(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql": return
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("SELECT to_regprocedure('auth.uid()') IS NOT NULL")
        if not cursor.fetchone()[0]: return
        for table in TABLES:
            cursor.execute(f'ALTER TABLE "{table}" ENABLE ROW LEVEL SECURITY')
        policies = {
            "accounts_profile": f"supabase_user_id = auth.uid() OR {ROLE} = 'admin'",
            "shipments_shipment": f"created_by_id = {PROFILE_ID} OR {ROLE} IN ('admin','fleet_manager','warehouse_staff')",
            "shipments_shipmentevent": f"EXISTS (SELECT 1 FROM shipments_shipment s WHERE s.id = shipment_id AND (s.created_by_id = {PROFILE_ID} OR {ROLE} IN ('admin','fleet_manager','warehouse_staff')))",
            "scheduling_booking": f"customer_id = {PROFILE_ID} OR {ROLE} IN ('admin','fleet_manager')",
            "notifications_notification": f"recipient_id = {PROFILE_ID} OR {ROLE} = 'admin'",
        }
        operations = f"{ROLE} IN ('admin','fleet_manager','warehouse_staff')"
        fleet = f"{ROLE} IN ('admin','fleet_manager')"
        warehouse = f"{ROLE} IN ('admin','warehouse_staff')"
        scheduling = f"{ROLE} IN ('admin','fleet_manager')"
        for table in TABLES:
            if table.startswith("fleet_"): condition = fleet
            elif table.startswith("warehouse_"): condition = warehouse
            elif table.startswith("scheduling_"): condition = policies.get(table, scheduling)
            else: condition = policies.get(table, operations)
            cursor.execute(f'DROP POLICY IF EXISTS logicraft_access ON "{table}"')
            cursor.execute(f'CREATE POLICY logicraft_access ON "{table}" FOR ALL TO authenticated USING ({condition}) WITH CHECK ({condition})')

def disable_rls(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql": return
    with schema_editor.connection.cursor() as cursor:
        for table in TABLES:
            cursor.execute(f'DROP POLICY IF EXISTS logicraft_access ON "{table}"')
            cursor.execute(f'ALTER TABLE "{table}" DISABLE ROW LEVEL SECURITY')

class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_initial"), ("fleet", "0001_initial"), ("warehouse", "0001_initial"),
        ("shipments", "0001_initial"), ("scheduling", "0001_initial"), ("notifications", "0001_initial"),
    ]
    operations = [migrations.RunPython(enable_rls, disable_rls)]
