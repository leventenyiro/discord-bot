export class Command {
    constructor(public id: number, public title: string, public text: string, public isCollapsed: boolean) {
        isCollapsed = false;
    }
}