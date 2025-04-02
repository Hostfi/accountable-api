-- Migration: Initial schema setup
-- Description: Creates the initial database schema for users and organizations
-- Tables:
--   - users: Stores user profiles linked to Clerk authentication
--   - organizations: Stores organization/company information
--   - organization_members: Junction table for user-organization relationships (single admin per org)
-- Author: AI Assistant
-- Date: 2024-03-24

-- Enable UUID extension for generating UUIDs
create extension if not exists "uuid-ossp";

-- Users table (linked to Clerk)
create table users (
    id uuid primary key default uuid_generate_v4(),
    clerk_id text not null unique,
    email text not null unique,
    first_name text,
    last_name text,
    avatar_url text,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

comment on table users is 'User profiles linked to Clerk authentication';

-- Organizations table
create table organizations (
    id uuid primary key default uuid_generate_v4(),
    name text not null,
    slug text not null unique,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

comment on table organizations is 'Organizations/companies that users can belong to';

-- Organization members (admin only)
create table organization_members (
    id uuid primary key default uuid_generate_v4(),
    organization_id uuid not null references organizations(id) on delete cascade,
    user_id uuid not null references users(id) on delete cascade,
    created_at timestamptz default now(),
    updated_at timestamptz default now(),
    -- Ensure only one member per organization
    unique (organization_id)
);

comment on table organization_members is 'Single admin user for each organization';

-- Create indexes for faster lookups
create index idx_users_clerk_id on users(clerk_id);
create index idx_organizations_slug on organizations(slug);
create index idx_org_members_user_id on organization_members(user_id);

-- Create trigger function to update updated_at column
create or replace function update_updated_at_column()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language 'plpgsql';

-- Apply trigger to all tables
create trigger update_users_updated_at
    before update on users
    for each row
    execute procedure update_updated_at_column();

create trigger update_organizations_updated_at
    before update on organizations
    for each row
    execute procedure update_updated_at_column();

create trigger update_organization_members_updated_at
    before update on organization_members
    for each row
    execute procedure update_updated_at_column();

-- Create stored procedures
create or replace function get_user_organizations(user_id_param uuid)
returns table (
    id uuid,
    name text,
    slug text,
    created_at timestamptz,
    updated_at timestamptz
) as $$
begin
    return query
    select 
        o.id,
        o.name,
        o.slug,
        o.created_at,
        o.updated_at
    from 
        organizations o
    join 
        organization_members om on o.id = om.organization_id
    where 
        om.user_id = user_id_param;
end;
$$ language plpgsql security definer;

comment on function get_user_organizations is 'Get all organizations a user administers';

-- Enable Row Level Security
alter table users enable row level security;
alter table organizations enable row level security;
alter table organization_members enable row level security;

-- RLS Policies for users table
create policy "Users can read their own profile"
    on users for select
    using (clerk_id = auth.uid());

create policy "Users can update their own profile"
    on users for update
    using (clerk_id = auth.uid());

-- RLS Policies for organizations table
create policy "Users can view organizations they administer"
    on organizations for select
    using (
        id in (
            select organization_id 
            from organization_members 
            where user_id in (select id from users where clerk_id = auth.uid())
        )
    );

create policy "Users can update organizations they administer"
    on organizations for update
    using (
        id in (
            select organization_id 
            from organization_members 
            where user_id in (select id from users where clerk_id = auth.uid())
        )
    );

-- RLS Policies for organization_members table
create policy "Users can view their organization memberships"
    on organization_members for select
    using (
        user_id in (select id from users where clerk_id = auth.uid())
    ); 
