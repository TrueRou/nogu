import { useUserStore } from "@/stores/user_information";
import type { AxiosInstance } from "axios";

export interface IExceptionNode {
    message: string;
    i18n_node: string;
    details?: [IExceptionNode];
}

export interface IBackendArgs {
    limit?: number;
    offset?: number;
}

export abstract class BackendObject<T> {
    axios: AxiosInstance;

    constructor() {
        this.axios = useUserStore().requests()
    }

    abstract fetchOne(id: number): Promise<T> | Promise<null>;

    abstract fetchAll(params: IBackendArgs): Promise<T[]> | Promise<null>;
}