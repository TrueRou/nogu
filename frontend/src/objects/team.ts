import { BackendObject, type IBackendArgs as IBackendParams } from "./object";
import type { IStage } from "./stage";
import type { IUserSimple } from "./user";
import { MemberPosition } from "@/constants";

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

export interface ITeamArgs extends IBackendParams {
    privacy_limit: number;
    active_only: boolean;
}

export class Team extends BackendObject<ITeam> {
    public async fetchAll(params: ITeamArgs): Promise<ITeam[]> {
        const teams: ITeam[] = await this.axios.get('/teams', { params: params })
        return teams
    }

    public async fetchOne(id: number): Promise<ITeam> {
        const team: ITeam = await this.axios.get(`/teams/${id}`)
        return team
    }

    public getLeader(team: ITeam): ITeamMember | undefined {
        return team.member.find(member => member.member_position == MemberPosition.OWNER)
    }

    public getLeaderUsername(team: ITeam) {
        return this.getLeader(team)?.member.username || ''
    }
}
