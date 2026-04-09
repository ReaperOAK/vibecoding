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
exports.VibecodingParticipant = void 0;
const vscode = __importStar(require("vscode"));
const child_process_1 = require("child_process");
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
/**
 * VibecodingParticipant implements VS Code chat participant for managing tickets
 * Provides three slash commands: /status, /sync, /next
 */
class VibecodingParticipant {
    participant = null;
    workspaceRoot;
    static instance = null;
    constructor() {
        const workspace = vscode.workspace.workspaceFolders?.[0];
        this.workspaceRoot = workspace?.uri.fsPath || process.cwd();
    }
    /**
     * Create the chat participant and register handlers
     */
    static create() {
        const instance = new VibecodingParticipant();
        instance.initializeParticipant();
        VibecodingParticipant.instance = instance;
        return instance;
    }
    /**
     * Initialize the VS Code chat participant
     */
    initializeParticipant() {
        this.participant = vscode.chat.createChatParticipant('vibecoding', this.handleChatRequest.bind(this));
        // Configure participant
        if (this.participant) {
            this.participant.iconPath = new vscode.ThemeIcon('sync-spinning');
        }
    }
    /**
     * Handle incoming chat requests
     */
    async handleChatRequest(request, _context, response, _token) {
        const prompt = request.prompt.toLowerCase().trim();
        const command = (request.command ?? '').toLowerCase();
        let responseText = '';
        if (command === 'status' || prompt.includes('/status')) {
            responseText = await this.handleStatusCommand();
        }
        else if (command === 'sync' || prompt.includes('/sync')) {
            responseText = await this.handleSyncCommand();
        }
        else if (command === 'next' || prompt.includes('/next')) {
            responseText = await this.handleNextCommand();
        }
        else {
            responseText = 'Available commands: `/status`, `/sync`, `/next`';
        }
        // Send response to chat
        response.markdown(responseText);
    }
    /**
     * Handle /status command - show ticket dashboard
     */
    async handleStatusCommand() {
        try {
            const output = await this.executeCommand('tickets.py', ['--status', '--json']);
            if (!output) {
                return 'Unable to retrieve status.';
            }
            const parsed = JSON.parse(output);
            return this.formatStatusOutput(parsed);
        }
        catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error);
            return `Error retrieving status: ${errorMsg}`;
        }
    }
    /**
     * Handle /sync command - run sync and report changes
     */
    async handleSyncCommand() {
        try {
            const output = await this.executeCommand('tickets.py', ['--sync']);
            if (!output) {
                return 'Sync completed but no output returned.';
            }
            return this.formatSyncOutput(output);
        }
        catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error);
            return `Error running sync: ${errorMsg}`;
        }
    }
    /**
     * Handle /next command - show next ready ticket
     */
    async handleNextCommand() {
        try {
            const readyDir = path.join(this.workspaceRoot, 'ticket-state', 'READY');
            if (!fs.existsSync(readyDir)) {
                return 'No READY tickets found';
            }
            const files = fs.readdirSync(readyDir).filter(f => f.endsWith('.json'));
            if (files.length === 0) {
                return 'No READY tickets found';
            }
            // Read first ticket and extract details
            const ticketPath = path.join(readyDir, files[0]);
            const ticketContent = fs.readFileSync(ticketPath, 'utf-8');
            const ticket = JSON.parse(ticketContent);
            return this.formatNextTicketOutput(ticket);
        }
        catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error);
            return `Error retrieving next ticket: ${errorMsg}`;
        }
    }
    /**
     * Execute a command in subprocess and return output
     */
    async executeCommand(command, args) {
        return new Promise((resolve, reject) => {
            const process = (0, child_process_1.spawn)('python3', [command, ...args], { cwd: this.workspaceRoot });
            let stdout = '';
            let stderr = '';
            process.stdout.on('data', (data) => {
                stdout += data.toString();
            });
            process.stderr.on('data', (data) => {
                stderr += data.toString();
            });
            process.on('close', (code) => {
                if (code === 0) {
                    resolve(stdout);
                }
                else {
                    reject(new Error(`Command failed with code ${code}: ${stderr}`));
                }
            });
            process.on('error', (error) => {
                reject(error);
            });
        });
    }
    /**
     * Format status output as markdown table
     */
    formatStatusOutput(parsed) {
        if (!parsed.summary || Object.keys(parsed.summary).length === 0) {
            return '📊 **Ticket Dashboard**\n\n_No tickets found_';
        }
        let markdown = '📊 **Ticket Dashboard**\n\n';
        markdown += '| Stage | Count |\n';
        markdown += '|-------|-------|\n';
        for (const [stage, count] of Object.entries(parsed.summary)) {
            markdown += `| ${stage} | ${count} |\n`;
        }
        return markdown;
    }
    /**
     * Format sync output
     */
    formatSyncOutput(output) {
        const lines = output.split('\n').filter(l => l.trim());
        if (lines.length === 0) {
            return '🔄 **Sync Complete**\n\nNo changes detected.';
        }
        let markdown = '🔄 **Sync Complete**\n\n';
        markdown += '```\n' + output + '\n```';
        return markdown;
    }
    /**
     * Format next ticket output
     */
    formatNextTicketOutput(ticket) {
        if (!ticket || !ticket.ticket_id) {
            return 'No READY tickets found';
        }
        let markdown = `📌 **Next Ticket**\n\n`;
        markdown += `**ID:** ${ticket.ticket_id}\n`;
        markdown += `**Title:** ${ticket.title}\n`;
        markdown += `**Type:** ${ticket.type}\n`;
        markdown += `**Priority:** ${ticket.priority || 'Normal'}\n\n`;
        if (ticket.acceptance_criteria && Array.isArray(ticket.acceptance_criteria)) {
            markdown += `**Acceptance Criteria:**\n\n`;
            ticket.acceptance_criteria.forEach((criterion, idx) => {
                markdown += `${idx + 1}. ${criterion}\n`;
            });
        }
        return markdown;
    }
    /**
     * Dispose the participant
     */
    dispose() {
        if (this.participant) {
            this.participant.dispose();
            this.participant = null;
        }
    }
    /**
     * Get the singleton instance
     */
    static getInstance() {
        return VibecodingParticipant.instance;
    }
    /**
     * Dispose the singleton instance
     */
    static disposeInstance() {
        if (VibecodingParticipant.instance) {
            VibecodingParticipant.instance.dispose();
            VibecodingParticipant.instance = null;
        }
    }
}
exports.VibecodingParticipant = VibecodingParticipant;
//# sourceMappingURL=chatParticipant.js.map