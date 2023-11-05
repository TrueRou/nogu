export interface Account {
    user_id: number;
    server_id: number;
    server_user_id: number;
    server_user_name: string;
    checked_at: Date;
}


export interface User {
    id: number;
    username: string;
    email: string;
    country: string;
    privileges: number;
    created_at: Date;
    updated_at: Date;
    accounts: Account[];
}

export interface UserSimple {
    id: number;
    username: string;
    country: string;
    privileges: number;
}

export interface Stage {
    name: string;
    mode: number;
    formula: number;
    pool_id: number;
    team_id: number;
    id: number;
    created_at: Date;
    updated_at: Date;
}

export interface TeamMember {
    member: UserSimple;
    member_position: number;
}

export interface Team {
    name: string;
    privacy: number;
    achieved: boolean;
    finish_at: Date;
    active_stage_id: number;
    id: number;
    create_at: Date;
    active_stage: Stage;
    member: TeamMember[];
}