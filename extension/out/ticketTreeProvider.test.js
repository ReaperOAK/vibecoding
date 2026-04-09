"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
const fs = __importStar(require("fs"));
const os = __importStar(require("os"));
const path = __importStar(require("path"));
const ticketTreeProvider_1 = require("./ticketTreeProvider");
function createTempWorkspace() {
    return fs.mkdtempSync(path.join(os.tmpdir(), 'vibecoding-tree-'));
}
function writeTicket(rootPath, stage, ticketId, title) {
    const stagePath = path.join(rootPath, 'ticket-state', stage);
    fs.mkdirSync(stagePath, { recursive: true });
    fs.writeFileSync(path.join(stagePath, `${ticketId}.json`), JSON.stringify({ ticket_id: ticketId, title }, null, 2), 'utf-8');
}
function getStage(nodes, stage) {
    const found = nodes.find((node) => node.kind === 'stage' && node.group === stage);
    expect(found).toBeDefined();
    return found;
}
describe('TicketTreeProvider', () => {
    test('TreeProvider instantiation creates READY, IN_PROGRESS, and DONE groups', () => {
        const rootPath = createTempWorkspace();
        const provider = new ticketTreeProvider_1.TicketTreeProvider(rootPath);
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
        const groups = (0, ticketTreeProvider_1.loadTicketGroups)(rootPath);
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
        const provider = new ticketTreeProvider_1.TicketTreeProvider(rootPath);
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
        const provider = new ticketTreeProvider_1.TicketTreeProvider(rootPath);
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
        const groups = (0, ticketTreeProvider_1.loadTicketGroups)(rootPath);
        expect(groups.READY).toHaveLength(0);
        expect(groups.IN_PROGRESS).toHaveLength(0);
        expect(groups.DONE).toHaveLength(0);
    });
    test('Provider without workspace root creates non-collapsible empty groups', () => {
        const provider = new ticketTreeProvider_1.TicketTreeProvider(undefined);
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
        const provider = new ticketTreeProvider_1.TicketTreeProvider(rootPath);
        const rootNodes = provider.getChildren();
        const ready = getStage(rootNodes, 'READY');
        const ticket = provider.getChildren(ready)[0];
        expect(ticket.kind).toBe('ticket');
        expect(provider.getChildren(ticket)).toHaveLength(0);
        expect(provider.getTreeItem(ticket)).toBe(ticket);
    });
});
//# sourceMappingURL=ticketTreeProvider.test.js.map