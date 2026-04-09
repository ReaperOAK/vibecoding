import * as fs from 'fs';
import * as path from 'path';

type TicketGroup = 'READY' | 'IN_PROGRESS' | 'DONE';
type ActiveStage = 'RESEARCH' | 'PM' | 'ARCHITECT' | 'DEVOPS' | 'BACKEND' | 'UIDESIGNER' | 'FRONTEND' | 'QA' | 'SECURITY' | 'CI' | 'DOCS' | 'VALIDATION';
type TicketStage = 'READY' | ActiveStage | 'DONE';

const ACTIVE_STAGES: readonly ActiveStage[] = [
    'RESEARCH',
    'PM',
    'ARCHITECT',
    'DEVOPS',
    'BACKEND',
    'UIDESIGNER',
    'FRONTEND',
    'QA',
    'SECURITY',
    'CI',
    'DOCS',
    'VALIDATION'
];

interface TicketRecord {
    id: string;
    title: string;
    stage: TicketStage;
}

interface StageNode {
    kind: 'stage';
    label: string;
    group: TicketGroup;
    collapsibleState: number;
    description: string;
    contextValue: 'vibecoding.stage';
    iconId: string;
}

interface TicketNode {
    kind: 'ticket';
    label: string;
    ticketId: string;
    stage: TicketStage;
    collapsibleState: number;
    description: string;
    tooltip: string;
    contextValue: 'vibecoding.ticket';
    iconId: string;
}

export type TicketTreeNode = StageNode | TicketNode;

type Disposable = { dispose(): void };
type EventListener<T> = (event: T | undefined) => unknown;
type Event<T> = (listener: EventListener<T>) => Disposable;

class SimpleEmitter<T> {
    private readonly listeners = new Set<EventListener<T>>();

    public readonly event: Event<T> = (listener: EventListener<T>): Disposable => {
        this.listeners.add(listener);
        return {
            dispose: () => {
                this.listeners.delete(listener);
            }
        };
    };

    public fire(data?: T): void {
        for (const listener of this.listeners) {
            listener(data);
        }
    }
}

function readTicketFile(ticketPath: string, stage: TicketStage): TicketRecord {
    const raw = fs.readFileSync(ticketPath, 'utf-8');
    const parsed = JSON.parse(raw) as Partial<{ ticket_id: string; title: string }>;
    const fallbackId = path.basename(ticketPath, '.json');
    return {
        id: parsed.ticket_id ?? fallbackId,
        title: parsed.title ?? 'Untitled ticket',
        stage
    };
}

function readTicketStage(rootPath: string, stage: TicketStage): TicketRecord[] {
    const stagePath = path.join(rootPath, 'ticket-state', stage);
    if (!fs.existsSync(stagePath)) {
        return [];
    }

    const tickets = fs.readdirSync(stagePath)
        .filter((name) => name.endsWith('.json'))
        .map((name) => readTicketFile(path.join(stagePath, name), stage));

    tickets.sort((a, b) => a.id.localeCompare(b.id));
    return tickets;
}

function sortTickets(tickets: TicketRecord[]): TicketRecord[] {
    tickets.sort((a, b) => a.id.localeCompare(b.id));
    return tickets;
}

export function loadTicketGroups(rootPath: string): Record<TicketGroup, TicketRecord[]> {
    const inProgress = ACTIVE_STAGES.flatMap((stage) => readTicketStage(rootPath, stage));
    return {
        READY: readTicketStage(rootPath, 'READY'),
        IN_PROGRESS: sortTickets(inProgress),
        DONE: readTicketStage(rootPath, 'DONE')
    };
}

export class TicketTreeProvider {
    private readonly emitter = new SimpleEmitter<TicketTreeNode>();
    private groups: Record<TicketGroup, TicketRecord[]>;

    public readonly onDidChangeTreeData: Event<TicketTreeNode> = this.emitter.event;

    public constructor(private readonly rootPath: string | undefined) {
        this.groups = this.load();
    }

    public getTreeItem(element: TicketTreeNode): TicketTreeNode {
        return element;
    }

    public getChildren(element?: TicketTreeNode): TicketTreeNode[] {
        if (!element) {
            return this.createStageNodes();
        }

        if (element.kind === 'stage') {
            return this.groups[element.group].map((ticket) => this.toTicketNode(ticket));
        }

        return [];
    }

    public refresh(): void {
        this.groups = this.load();
        this.emitter.fire(undefined);
    }

    private load(): Record<TicketGroup, TicketRecord[]> {
        if (!this.rootPath) {
            return { READY: [], IN_PROGRESS: [], DONE: [] };
        }
        return loadTicketGroups(this.rootPath);
    }

    private createStageNodes(): StageNode[] {
        return [
            this.toStageNode('READY'),
            this.toStageNode('IN_PROGRESS'),
            this.toStageNode('DONE')
        ];
    }

    private toStageNode(group: TicketGroup): StageNode {
        const count = this.groups[group].length;
        return {
            kind: 'stage',
            label: group,
            group,
            collapsibleState: count > 0 ? 1 : 0,
            description: `${count}`,
            contextValue: 'vibecoding.stage',
            iconId: group === 'DONE' ? 'check' : group === 'IN_PROGRESS' ? 'sync' : 'clock'
        };
    }

    private toTicketNode(ticket: TicketRecord): TicketNode {
        return {
            kind: 'ticket',
            label: ticket.id,
            ticketId: ticket.id,
            stage: ticket.stage,
            collapsibleState: 0,
            description: ticket.title,
            tooltip: `${ticket.id}: ${ticket.title}`,
            contextValue: 'vibecoding.ticket',
            iconId: ticket.stage === 'DONE' ? 'pass' : ticket.stage === 'READY' ? 'circle-large-outline' : 'play-circle'
        };
    }
}