-- Run in the Supabase SQL editor. New users receive a safe customer role claim.
create or replace function public.handle_new_user_role()
returns trigger
language plpgsql
security definer set search_path = ''
as $$
begin
  update auth.users
  -- Never trust user_metadata for authorization; privileged role changes belong
  -- in an admin-only Edge Function or server-side Supabase Admin API call.
  set raw_app_meta_data = coalesce(raw_app_meta_data, '{}'::jsonb) ||
      jsonb_build_object('role', 'customer')
  where id = new.id;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created_set_role on auth.users;
create trigger on_auth_user_created_set_role
after insert on auth.users
for each row execute procedure public.handle_new_user_role();
