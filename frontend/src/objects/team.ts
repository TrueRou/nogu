import { BackendObject, type IBackendArgs } from "./object";
import type { IStage } from "./stage";
import type { IUserSimple } from "./user";

export interface ITeamMember {
    member: IUserSimple;
    member_position: number;
}

export interface ITeam {
    name: string;
    privacy: number;
    achieved: boolean;
    finish_at: Date;
    active_stage_id: number;
    id: number;
    create_at: Date;
    active_stage: IStage;
    member: ITeamMember[];
}

export interface ITeamArgs extends IBackendArgs {
    privacy_limit: number;
    active_only: boolean;
}

export class Team extends BackendObject<ITeam> {
    async fetchAll(params: ITeamArgs): Promise<ITeam[]> {
        const teams: ITeam[] = await this.axios.get('/teams', { params: params })
        return teams
    }

    async fetchOne(id: number): Promise<ITeam> {
        const team: ITeam = await this.axios.get(`/teams/${id}`)
        return team
    }
}
