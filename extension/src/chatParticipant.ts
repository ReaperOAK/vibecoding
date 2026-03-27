import * as vscode from 'vscode';
import { spawn } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Represents the structure of ticket status summary
 */
interface TicketStatusSummary {
    summary?: Record<string, number>;
    tickets?: TicketInfo[];
}

/**
 * Represents a single ticket's information
 */
interface TicketInfo {
    ticket_id: string;
    title: string;
    type: string;
    priority?: string;
    acceptance_criteria?: string[];
}

/**
 * VibecodingParticipant implements VS Code chat participant for managing tickets
 * Provides three slash commands: /status, /sync, /next
 */
export class VibecodingParticipant {
    private participant: vscode.ChatParticipant | null = null;
    private workspaceRoot: string;

    private static instance: VibecodingParticipant | null = null;

    constructor() {
        const workspace = vscode.workspace.workspaceFolders?.[0];
        this.workspaceRoot = workspace?.uri.fsPath || process.cwd();
    }

    /**
     * Create the chat participant and register handlers
     */
    static create(): VibecodingParticipant {
        const instance = new VibecodingParticipant();
        instance.initializeParticipant();
        VibecodingParticipant.instance = instance;
        return instance;
    }

    /**
     * Initialize the VS Code chat participant
     */
    private initializeParticipant(): void {
        this.participant = vscode.chat.createChatParticipant('vibecoding', this.handleChatRequest.bind(this));
        
        // Configure participant
        if (this.participant) {
            this.participant.iconPath = new vscode.ThemeIcon('sync-spinning');
            this.participant.slashCommandProvider = {
                provideSlashCommands: (_token) => [
                    { command: 'status', description: 'Show ticket dashboard with stage counts' },
                    { command: 'sync', description: 'Run ticket sync and report moved tickets' },
                    { command: 'next', description: 'Display highest-priority READY ticket' }
                ]
            };
        }
    }

    /**
     * Handle incoming chat requests
     */
    public async handleChatRequest(request: vscode.ChatRequest, _context: vscode.ChatContext, _token: vscode.CancellationToken): Promise<void> {
        const prompt = request.prompt.toLowerCase().trim();

        let response: string = '';

        if (prompt.includes('/status')) {
            response = await this.handleStatusCommand();
        } else if (prompt.includes('/sync')) {
            response = await this.handleSyncCommand();
        } else if (prompt.includes('/next')) {
            response = await this.handleNextCommand();
        } else {
            response = 'Available commands: `/status`, `/sync`, `/next\'';
        }

        // Send response to chat
        const chatResponse = vscode.LanguageModelChatMessage.User(response);
        await request.stream.markdown(response);
    }

    /**
     * Handle /status command - show ticket dashboard
     */
    public async handleStatusCommand(): Promise<string> {
        try {
            const output = await this.executeCommand('tickets.py', ['--status', '--json']);
            
            if (!output) {
                return 'Unable to retrieve status.';
            }

            const parsed = JSON.parse(output) as TicketStatusSummary;
            return this.formatStatusOutput(parsed);
        } catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error);
            return `Error retrieving status: ${errorMsg}`;
        }
    }

    /**
     * Handle /sync command - run sync and report changes
     */
    public async handleSyncCommand(): Promise<string> {
        try {
            const output = await this.executeCommand('tickets.py', ['--sync']);
            
            if (!output) {
                return 'Sync completed but no output returned.';
            }

            return this.formatSyncOutput(output);
        } catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error);
            return `Error running sync: ${errorMsg}`;
        }
    }

    /**
     * Handle /next command - show next ready ticket
     */
    public async handleNextCommand(): Promise<string> {
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
        } catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error);
            return `Error retrieving next ticket: ${errorMsg}`;
        }
    }

    /**
     * Execute a command in subprocess and return output
     */
    private async executeCommand(command: string, args: string[]): Promise<string> {
        return new Promise((resolve, reject) => {
            const process = spawn('python3', [command, ...args], { cwd: this.workspaceRoot });

            let stdout = '';
            let stderr = '';

            process.stdout.on('data', (data: Buffer) => {
                stdout += data.toString();
            });

            process.stderr.on('data', (data: Buffer) => {
                stderr += data.toString();
            });

            process.on('close', (code: number) => {
                if (code === 0) {
                    resolve(stdout);
                } else {
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
    private formatStatusOutput(parsed: TicketStatusSummary): string {
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
    private formatSyncOutput(output: string): string {
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
    private formatNextTicketOutput(ticket: any): string {
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
            ticket.acceptance_criteria.forEach((criterion: string, idx: number) => {
                markdown += `${idx + 1}. ${criterion}\n`;
            });
        }

        return markdown;
    }

    /**
     * Dispose the participant
     */
    public dispose(): void {
        if (this.participant) {
            this.participant.dispose();
            this.participant = null;
        }
    }

    /**
     * Get the singleton instance
     */
    static getInstance(): VibecodingParticipant | null {
        return VibecodingParticipant.instance;
    }

    /**
     * Dispose the singleton instance
     */
    static disposeInstance(): void {
        if (VibecodingParticipant.instance) {
            VibecodingParticipant.instance.dispose();
            VibecodingParticipant.instance = null;
        }
    }
}
