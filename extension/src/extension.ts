import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

export function activate(context: vscode.ExtensionContext): void {
    const config = vscode.workspace.getConfiguration('vibecoding');

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
}

export function deactivate(): void {
    // No cleanup needed
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
