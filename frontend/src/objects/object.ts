import type { AxiosInstance } from "axios";

export interface IExceptionNode {
    message: string;
    i18n_node: string;
    details?: [IExceptionNode];
}

export interface IBackendArgs {
    limit: number;
    offset: number;
}

export abstract class BackendObject<T> {
    axios: AxiosInstance;

    constructor(axios_context: AxiosInstance) {
        this.axios = axios_context
    }

    abstract fetchOne(id: number): Promise<T>;

    abstract fetchAll(params: IBackendArgs): Promise<T[]>;
}