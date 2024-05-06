export interface IToken {
    access_token: string;
    token_type: string;
}

export interface IAccount {
    user_id: number;
    server_id: number;
    su_id: number;
    su_name: string;
    su_flags: number;
    su_country: number;
    su_playtime: number;
    su_major_ruleset: number;
    checked_at: Date;
}

export interface IUser {
    id: number;
    username: string;
    email: string;
    country: string;
    privileges: number;
    created_at: Date;
    updated_at: Date;
    accounts: IAccount[];
}

export interface IUserBase {
    username: string;
    email: string;
    country: string;
}

export interface IUserSimple {
    id: number;
    username: string;
    country: string;
    privileges: number;
}