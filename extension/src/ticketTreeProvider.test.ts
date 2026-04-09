import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import { TicketTreeProvider, loadTicketGroups, TicketTreeNode } from './ticketTreeProvider';

type TicketStage = 'READY' | 'DONE' | 'BACKEND' | 'QA';

function createTempWorkspace(): string {
    return fs.mkdtempSync(path.join(os.tmpdir(), 'vibecoding-tree-'));
}

function writeTicket(rootPath: string, stage: TicketStage, ticketId: string, title: string): void {
    const stagePath = path.join(rootPath, 'ticket-state', stage);
    fs.mkdirSync(stagePath, { recursive: true });
    fs.writeFileSync(
        path.join(stagePath, `${ticketId}.json`),
        JSON.stringify({ ticket_id: ticketId, title }, null, 2),
        'utf-8'
    );
}

function getStage(nodes: TicketTreeNode[], stage: 'READY' | 'IN_PROGRESS' | 'DONE'): TicketTreeNode {
    const found = nodes.find((node) => node.kind === 'stage' && node.group === stage);
    expect(found).toBeDefined();
    return found as TicketTreeNode;
}

describe('TicketTreeProvider', () => {
        test('TreeProvider instantiation creates READY, IN_PROGRESS, and DONE groups', () => {
            const rootPath = createTempWorkspace();
            const provider = new TicketTreeProvider(rootPath);
            const root = provider.getChildren();

            expect(root).toHaveLength(3);
            expect(root.some((node) => node.kind === 'stage' && node.label === 'READY')).toBe(true);
            expect(root.some((node) => node.kind === 'stage' && node.label === 'IN_PROGRESS')).toBe(true);
            expect(root.some((node) => node.kind === 'stage' && node.label === 'DONE')).toBe(true);
    });

        test('Loading tickets from filesystem returns READY, IN_PROGRESS, and DONE data', () => {
            const rootPath = createTempWorkspace();
            writeTicket(rootPath, 'READY', 'TASK-VIB-100', 'Ready ticket');
            writeTicket(rootPath, 'BACKEND', 'TASK-VIB-102', 'Active backend ticket');
            writeTicket(rootPath, 'QA', 'TASK-VIB-103', 'Active qa ticket');
            writeTicket(rootPath, 'DONE', 'TASK-VIB-101', 'Done ticket');

            const groups = loadTicketGroups(rootPath);
            expect(groups.READY).toHaveLength(1);
            expect(groups.IN_PROGRESS).toHaveLength(2);
            expect(groups.DONE).toHaveLength(1);
            expect(groups.READY[0].id).toBe('TASK-VIB-100');
            expect(groups.IN_PROGRESS[0].id).toBe('TASK-VIB-102');
            expect(groups.IN_PROGRESS[1].id).toBe('TASK-VIB-103');
            expect(groups.DONE[0].id).toBe('TASK-VIB-101');
    });

        test('Tree structure returns tickets under READY, IN_PROGRESS, and DONE groups', () => {
            const rootPath = createTempWorkspace();
            writeTicket(rootPath, 'READY', 'TASK-VIB-110', 'Ready item');
            writeTicket(rootPath, 'BACKEND', 'TASK-VIB-112', 'In progress item');
            writeTicket(rootPath, 'DONE', 'TASK-VIB-111', 'Done item');
            const provider = new TicketTreeProvider(rootPath);

            const roots = provider.getChildren();
            const readyGroup = getStage(roots, 'READY');
            const inProgressGroup = getStage(roots, 'IN_PROGRESS');
            const doneGroup = getStage(roots, 'DONE');

            const readyChildren = provider.getChildren(readyGroup);
            const inProgressChildren = provider.getChildren(inProgressGroup);
            const doneChildren = provider.getChildren(doneGroup);

            expect(readyChildren).toHaveLength(1);
            expect(inProgressChildren).toHaveLength(1);
            expect(doneChildren).toHaveLength(1);
            expect(readyChildren[0].kind).toBe('ticket');
            expect(inProgressChildren[0].kind).toBe('ticket');
            expect(doneChildren[0].kind).toBe('ticket');
            expect(readyChildren[0].label).toBe('TASK-VIB-110');
            expect(inProgressChildren[0].label).toBe('TASK-VIB-112');
            expect(doneChildren[0].label).toBe('TASK-VIB-111');
    });

    test('Refresh re-reads filesystem and emits change event', () => {
            const rootPath = createTempWorkspace();
            const provider = new TicketTreeProvider(rootPath);
            let fired = 0;

            const subscription = provider.onDidChangeTreeData(() => {
                fired += 1;
            });

            writeTicket(rootPath, 'BACKEND', 'TASK-VIB-120', 'Post-refresh ticket');
            provider.refresh();

            const roots = provider.getChildren();
            const inProgressGroup = getStage(roots, 'IN_PROGRESS');
            const inProgressChildren = provider.getChildren(inProgressGroup);

            expect(fired).toBe(1);
            expect(inProgressChildren).toHaveLength(1);
            expect(inProgressChildren[0].label).toBe('TASK-VIB-120');

            subscription.dispose();
    });

    test('loadTicketGroups returns empty arrays when stage directories are missing', () => {
            const rootPath = createTempWorkspace();
            const groups = loadTicketGroups(rootPath);

            expect(groups.READY).toHaveLength(0);
            expect(groups.IN_PROGRESS).toHaveLength(0);
            expect(groups.DONE).toHaveLength(0);
    });

        test('Provider without workspace root creates non-collapsible empty groups', () => {
            const provider = new TicketTreeProvider(undefined);
            const roots = provider.getChildren();

            const ready = getStage(roots, 'READY');
            const inProgress = getStage(roots, 'IN_PROGRESS');
            const done = getStage(roots, 'DONE');

            expect(ready.kind).toBe('stage');
            expect(inProgress.kind).toBe('stage');
            expect(done.kind).toBe('stage');
            expect(ready.collapsibleState).toBe(0);
            expect(inProgress.collapsibleState).toBe(0);
            expect(done.collapsibleState).toBe(0);
            expect(ready.description).toBe('0');
            expect(inProgress.description).toBe('0');
            expect(done.description).toBe('0');
        });

        test('Ticket node has no children and getTreeItem returns the same node', () => {
            const rootPath = createTempWorkspace();
            writeTicket(rootPath, 'READY', 'TASK-VIB-130', 'Tree item ticket');
            const provider = new TicketTreeProvider(rootPath);

            const rootNodes = provider.getChildren();
            const ready = getStage(rootNodes, 'READY');
            const ticket = provider.getChildren(ready)[0];

            expect(ticket.kind).toBe('ticket');
            expect(provider.getChildren(ticket)).toHaveLength(0);
            expect(provider.getTreeItem(ticket)).toBe(ticket);
        });
});