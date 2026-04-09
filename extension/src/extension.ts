import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { VibecodingParticipant } from './chatParticipant';
import { TicketTreeProvider } from './ticketTreeProvider';

/**
 * Activates the extension and registers commands, views, and MCP providers.
 */
export function activate(context: vscode.ExtensionContext): void {
    const config = vscode.workspace.getConfiguration('vibecoding');
    const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;

    registerTicketMcpServerProvider(context, workspaceRoot);

    const provider = new TicketTreeProvider(workspaceRoot);
    const ticketTreeView = vscode.window.createTreeView('vibecoding.tickets', {
        treeDataProvider: provider
    });

    context.subscriptions.push(
        ticketTreeView,
        vscode.commands.registerCommand('vibecoding.refreshTickets', () => provider.refresh())
    );

    // Auto-scaffold on first activation
    if (config.get<boolean>('autoScaffold', true)) {
        scaffoldIfNeeded(context);
    }

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('vibecoding.scaffold', () => scaffold(context)),
        vscode.commands.registerCommand('vibecoding.refreshAgents', () => refreshAgents(context)),
        vscode.commands.registerCommand('vibecoding.syncTickets', () => syncTickets())
    );

    // Create and register the vibecoding chat participant
    const participant = VibecodingParticipant.create();
    context.subscriptions.push({
        dispose: () => VibecodingParticipant.disposeInstance()
    });
}

export function deactivate(): void {
    // Clean up chat participant
    VibecodingParticipant.disposeInstance();
}

async function scaffoldIfNeeded(context: vscode.ExtensionContext): Promise<void> {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        return;
    }

    const githubDir = path.join(workspaceFolder.uri.fsPath, '.github');
    if (!fs.existsSync(path.join(githubDir, 'agents'))) {
        const answer = await vscode.window.showInformationMessage(
            'Vibecoding agent infrastructure not found. Scaffold now?',
            'Yes', 'No'
        );
        if (answer === 'Yes') {
            await scaffold(context);
        }
    }
}

async function scaffold(context: vscode.ExtensionContext): Promise<void> {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('No workspace folder open.');
        return;
    }

    const root = workspaceFolder.uri.fsPath;
    const dirs = [
        '.github/agents', '.github/instructions', '.github/skills',
        '.github/hooks/scripts', '.github/prompts', '.github/guardian',
        '.github/memory-bank', '.github/mcp-servers/ticket-server',
        '.github/vibecoding', 'ticket-state/READY', 'ticket-state/DONE',
        'tickets', 'agent-output', '.vscode'
    ];

    for (const dir of dirs) {
        const fullPath = path.join(root, dir);
        if (!fs.existsSync(fullPath)) {
            fs.mkdirSync(fullPath, { recursive: true });
        }
    }

    // Create guardian stop file
    const stopFile = path.join(root, '.github/guardian/STOP_ALL');
    if (!fs.existsSync(stopFile)) {
        fs.writeFileSync(stopFile, 'RUN');
    }

    vscode.window.showInformationMessage('Vibecoding infrastructure scaffolded.');
}

async function refreshAgents(context: vscode.ExtensionContext): Promise<void> {
    vscode.window.showInformationMessage('Agent templates refreshed (no-op in scaffold mode).');
}

async function syncTickets(): Promise<void> {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        return;
    }

    const terminal = vscode.window.createTerminal('Vibecoding');
    terminal.sendText('python3 tickets.py --sync');
    terminal.show();
}

/**
 * Registers the ticket server as an MCP app provider for the current workspace.
 */
function registerTicketMcpServerProvider(
    context: vscode.ExtensionContext,
    workspaceRoot: string | undefined
): void {
    if (!workspaceRoot) {
        return;
    }

    const providerId = 'vibecoding.ticket-server';
    const serverScriptPath = path.join(workspaceRoot, '.github', 'mcp-servers', 'ticket-server', 'server.py');

    const registration = vscode.lm.registerMcpServerDefinitionProvider(providerId, {
        provideMcpServerDefinitions: () => {
            const server = new vscode.McpStdioServerDefinition(
                'Vibecoding Ticket Server',
                'python3',
                [serverScriptPath],
                {
                    VIBECODING_WORKSPACE_ROOT: workspaceRoot,
                    PYTHONUNBUFFERED: '1'
                }
            );

            // The MCP server process should execute from the workspace root.
            server.cwd = vscode.Uri.file(workspaceRoot);

            return [server];
        }
    });

    context.subscriptions.push(registration);
}
