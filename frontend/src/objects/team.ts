import { BackendObject, type IBackendArgs as IBackendParams } from "./backend";
import type { IStage } from "./stage";
import type { IUserSimple } from "./user";
import { MemberPosition } from "@/enums";
import { type ITranslateable } from "@/translatable";

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

export interface ITeamParams extends IBackendParams {
    privacy_limit: number;
    active_only: boolean;
}

export class Team extends BackendObject<ITeam> {
    public async fetchAll(params: ITeamParams): Promise<ITeam[]> {
        const teams: ITeam[] = await this.axios.get('/teams', { params: params })
        return teams
    }

    public async fetchOne(id: number): Promise<ITeam> {
        const team: ITeam = await this.axios.get(`/teams/${id}`)
        return team
    }

    public getLeader(member: ITeamMember[]): ITeamMember | undefined {
        return member.find(member => member.member_position == MemberPosition.OWNER)
    }
}
