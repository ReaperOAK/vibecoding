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
exports.TicketTreeProvider = void 0;
exports.loadTicketGroups = loadTicketGroups;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const ACTIVE_STAGES = [
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
class SimpleEmitter {
    listeners = new Set();
    event = (listener) => {
        this.listeners.add(listener);
        return {
            dispose: () => {
                this.listeners.delete(listener);
            }
        };
    };
    fire(data) {
        for (const listener of this.listeners) {
            listener(data);
        }
    }
}
function readTicketFile(ticketPath, stage) {
    const raw = fs.readFileSync(ticketPath, 'utf-8');
    const parsed = JSON.parse(raw);
    const fallbackId = path.basename(ticketPath, '.json');
    return {
        id: parsed.ticket_id ?? fallbackId,
        title: parsed.title ?? 'Untitled ticket',
        stage
    };
}
function readTicketStage(rootPath, stage) {
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
function sortTickets(tickets) {
    tickets.sort((a, b) => a.id.localeCompare(b.id));
    return tickets;
}
/**
 * Loads ticket groups for the sidebar tree view.
 *
 * READY and DONE are read from their matching state directories.
 * IN_PROGRESS aggregates all active SDLC stage directories.
 */
function loadTicketGroups(rootPath) {
    const inProgress = ACTIVE_STAGES.flatMap((stage) => readTicketStage(rootPath, stage));
    return {
        READY: readTicketStage(rootPath, 'READY'),
        IN_PROGRESS: sortTickets(inProgress),
        DONE: readTicketStage(rootPath, 'DONE')
    };
}
/**
 * Tree data provider for the `vibecoding.tickets` sidebar view.
 */
class TicketTreeProvider {
    rootPath;
    emitter = new SimpleEmitter();
    groups;
    onDidChangeTreeData = this.emitter.event;
    constructor(rootPath) {
        this.rootPath = rootPath;
        this.groups = this.load();
    }
    getTreeItem(element) {
        return element;
    }
    getChildren(element) {
        if (!element) {
            return this.createStageNodes();
        }
        if (element.kind === 'stage') {
            return this.groups[element.group].map((ticket) => this.toTicketNode(ticket));
        }
        return [];
    }
    /**
     * Re-reads grouped ticket data from disk and emits a tree refresh event.
     */
    refresh() {
        this.groups = this.load();
        this.emitter.fire(undefined);
    }
    load() {
        if (!this.rootPath) {
            return { READY: [], IN_PROGRESS: [], DONE: [] };
        }
        return loadTicketGroups(this.rootPath);
    }
    createStageNodes() {
        return [
            this.toStageNode('READY'),
            this.toStageNode('IN_PROGRESS'),
            this.toStageNode('DONE')
        ];
    }
    toStageNode(group) {
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
    toTicketNode(ticket) {
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
exports.TicketTreeProvider = TicketTreeProvider;
//# sourceMappingURL=ticketTreeProvider.js.map