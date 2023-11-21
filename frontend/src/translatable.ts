export interface ITranslateableList extends ITranslateable {
    details?: [ITranslateable];
}

export interface ITranslateable {
    message: string;
    i18n_node: string;
}

// translate
export function t(translateable: string): string {
    return translateable // TODO: Implement translation
}

// translate with typedef
export function tt(translateable: ITranslateable): string {
    return translateable.message // TODO: Implement translation
}

// translate with typedef list
export function ttl(translateableList: ITranslateableList): string {
    let message = tt(translateableList)
    if (translateableList.details != null) {
        message += ': \n'
        for (const detail of translateableList.details) {
            message += tt(detail) + '\n'
        }
    }
    return message
}