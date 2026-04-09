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
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
const chatParticipant_1 = require("./chatParticipant");
const ticketTreeProvider_1 = require("./ticketTreeProvider");
function activate(context) {
    const config = vscode.workspace.getConfiguration('vibecoding');
    const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    registerTicketMcpServerProvider(context, workspaceRoot);
    const provider = new ticketTreeProvider_1.TicketTreeProvider(workspaceRoot);
    const ticketTreeView = vscode.window.createTreeView('vibecoding.tickets', {
        treeDataProvider: provider
    });
    context.subscriptions.push(ticketTreeView, vscode.commands.registerCommand('vibecoding.refreshTickets', () => provider.refresh()));
    // Auto-scaffold on first activation
    if (config.get('autoScaffold', true)) {
        scaffoldIfNeeded(context);
    }
    // Register commands
    context.subscriptions.push(vscode.commands.registerCommand('vibecoding.scaffold', () => scaffold(context)), vscode.commands.registerCommand('vibecoding.refreshAgents', () => refreshAgents(context)), vscode.commands.registerCommand('vibecoding.syncTickets', () => syncTickets()));
    // Create and register the vibecoding chat participant
    const participant = chatParticipant_1.VibecodingParticipant.create();
    context.subscriptions.push({
        dispose: () => chatParticipant_1.VibecodingParticipant.disposeInstance()
    });
}
function deactivate() {
    // Clean up chat participant
    chatParticipant_1.VibecodingParticipant.disposeInstance();
}
async function scaffoldIfNeeded(context) {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        return;
    }
    const githubDir = path.join(workspaceFolder.uri.fsPath, '.github');
    if (!fs.existsSync(path.join(githubDir, 'agents'))) {
        const answer = await vscode.window.showInformationMessage('Vibecoding agent infrastructure not found. Scaffold now?', 'Yes', 'No');
        if (answer === 'Yes') {
            await scaffold(context);
        }
    }
}
async function scaffold(context) {
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
async function refreshAgents(context) {
    vscode.window.showInformationMessage('Agent templates refreshed (no-op in scaffold mode).');
}
async function syncTickets() {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        return;
    }
    const terminal = vscode.window.createTerminal('Vibecoding');
    terminal.sendText('python3 tickets.py --sync');
    terminal.show();
}
function registerTicketMcpServerProvider(context, workspaceRoot) {
    if (!workspaceRoot) {
        return;
    }
    const providerId = 'vibecoding.ticket-server';
    const serverScriptPath = path.join(workspaceRoot, '.github', 'mcp-servers', 'ticket-server', 'server.py');
    const registration = vscode.lm.registerMcpServerDefinitionProvider(providerId, {
        provideMcpServerDefinitions: () => {
            const server = new vscode.McpStdioServerDefinition('Vibecoding Ticket Server', 'python3', [serverScriptPath], {
                VIBECODING_WORKSPACE_ROOT: workspaceRoot,
                PYTHONUNBUFFERED: '1'
            });
            // The MCP server process should execute from the workspace root.
            server.cwd = vscode.Uri.file(workspaceRoot);
            return [server];
        }
    });
    context.subscriptions.push(registration);
}
//# sourceMappingURL=extension.js.map