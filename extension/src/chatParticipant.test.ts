import { EventEmitter } from 'events';
import { VibecodingParticipant } from './chatParticipant';

const mockCreateChatParticipant = jest.fn(() => ({
    dispose: jest.fn(),
    iconPath: undefined,
    slashCommandProvider: undefined
}));

jest.mock('vscode', () => ({
    workspace: { workspaceFolders: [{ uri: { fsPath: '/workspace' } }] },
    ThemeIcon: function ThemeIcon(id: string): { id: string } {
        return { id };
    },
    chat: {
        createChatParticipant: (...args: unknown[]) => mockCreateChatParticipant.apply(null, args as never[])
    }
}), { virtual: true });

const mockSpawn = jest.fn();
jest.mock('child_process', () => ({
    spawn: (...args: unknown[]) => mockSpawn(...args)
}));

const mockExistsSync = jest.fn();
const mockReaddirSync = jest.fn();
const mockReadFileSync = jest.fn();

jest.mock('fs', () => ({
    existsSync: (...args: unknown[]) => mockExistsSync(...args),
    readdirSync: (...args: unknown[]) => mockReaddirSync(...args),
    readFileSync: (...args: unknown[]) => mockReadFileSync(...args)
}));

type SpawnMockProcess = EventEmitter & {
    stdout: EventEmitter;
    stderr: EventEmitter;
};

function createSpawnProcess(exitCode: number, stdout = '', stderr = ''): SpawnMockProcess {
    const processEmitter = new EventEmitter() as SpawnMockProcess;
    processEmitter.stdout = new EventEmitter();
    processEmitter.stderr = new EventEmitter();

    setImmediate(() => {
        if (stdout) {
            processEmitter.stdout.emit('data', Buffer.from(stdout));
        }
        if (stderr) {
            processEmitter.stderr.emit('data', Buffer.from(stderr));
        }
        processEmitter.emit('close', exitCode);
    });

    return processEmitter;
}

describe('VibecodingParticipant', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        VibecodingParticipant.disposeInstance();
    });

    it('formats status dashboard from valid JSON output', async () => {
        mockSpawn.mockReturnValue(
            createSpawnProcess(0, JSON.stringify({ summary: { READY: 2, BACKEND: 1 } }))
        );

        const participant = VibecodingParticipant.create();
        const response = await participant.handleStatusCommand();

        expect(response).toContain('Ticket Dashboard');
        expect(response).toContain('| READY | 2 |');
        expect(response).toContain('| BACKEND | 1 |');
    });

    it('returns fallback when status output is empty', async () => {
        mockSpawn.mockReturnValue(createSpawnProcess(0, ''));

        const participant = VibecodingParticipant.create();
        const response = await participant.handleStatusCommand();

        expect(response).toBe('Unable to retrieve status.');
    });

    it('returns error text when status JSON is invalid', async () => {
        mockSpawn.mockReturnValue(createSpawnProcess(0, '{bad json'));

        const participant = VibecodingParticipant.create();
        const response = await participant.handleStatusCommand();

        expect(response).toContain('Error retrieving status');
    });

    it('formats sync output in fenced markdown block', async () => {
        mockSpawn.mockReturnValue(createSpawnProcess(0, 'Moved TASK-1 to READY'));

        const participant = VibecodingParticipant.create();
        const response = await participant.handleSyncCommand();

        expect(response).toContain('Sync Complete');
        expect(response).toContain('```');
        expect(response).toContain('Moved TASK-1 to READY');
    });

    it('returns fallback when sync output is empty', async () => {
        mockSpawn.mockReturnValue(createSpawnProcess(0, ''));

        const participant = VibecodingParticipant.create();
        const response = await participant.handleSyncCommand();

        expect(response).toBe('Sync completed but no output returned.');
    });

    it('returns sync error on subprocess failure', async () => {
        mockSpawn.mockReturnValue(createSpawnProcess(1, '', 'boom'));

        const participant = VibecodingParticipant.create();
        const response = await participant.handleSyncCommand();

        expect(response).toContain('Error running sync');
    });

    it('returns no ready ticket when READY directory is missing', async () => {
        mockExistsSync.mockReturnValue(false);

        const participant = VibecodingParticipant.create();
        const response = await participant.handleNextCommand();

        expect(response).toBe('No READY tickets found');
    });

    it('returns no ready ticket when READY directory has no ticket files', async () => {
        mockExistsSync.mockReturnValue(true);
        mockReaddirSync.mockReturnValue([]);

        const participant = VibecodingParticipant.create();
        const response = await participant.handleNextCommand();

        expect(response).toBe('No READY tickets found');
    });

    it('formats next ticket details and acceptance criteria', async () => {
        mockExistsSync.mockReturnValue(true);
        mockReaddirSync.mockReturnValue(['TASK-VIB-011.json']);
        mockReadFileSync.mockReturnValue(
            JSON.stringify({
                ticket_id: 'TASK-VIB-011',
                title: 'Sample ticket',
                type: 'backend',
                priority: 'high',
                acceptance_criteria: ['first', 'second']
            })
        );

        const participant = VibecodingParticipant.create();
        const response = await participant.handleNextCommand();

        expect(response).toContain('Next Ticket');
        expect(response).toContain('TASK-VIB-011');
        expect(response).toContain('1. first');
        expect(response).toContain('2. second');
    });

    it('returns no ready ticket when parsed file has no ticket_id', async () => {
        mockExistsSync.mockReturnValue(true);
        mockReaddirSync.mockReturnValue(['bad.json']);
        mockReadFileSync.mockReturnValue(JSON.stringify({ title: 'Missing id', type: 'backend' }));

        const participant = VibecodingParticipant.create();
        const response = await participant.handleNextCommand();

        expect(response).toBe('No READY tickets found');
    });

    it('returns error when ticket file read throws', async () => {
        mockExistsSync.mockReturnValue(true);
        mockReaddirSync.mockReturnValue(['TASK-VIB-011.json']);
        mockReadFileSync.mockImplementation(() => {
            throw new Error('read failed');
        });

        const participant = VibecodingParticipant.create();
        const response = await participant.handleNextCommand();

        expect(response).toContain('Error retrieving next ticket');
    });

    it('returns help text for unknown chat command', async () => {
        const participant = VibecodingParticipant.create();
        const markdown = jest.fn();

        await participant.handleChatRequest(
            {
                prompt: '/unknown',
                command: undefined
            } as never,
            {} as never,
            { markdown } as never,
            {} as never
        );

        expect(markdown).toHaveBeenCalledWith('Available commands: `/status`, `/sync`, `/next`');
    });

    it('handles slash command via request.command field', async () => {
        mockSpawn.mockReturnValue(
            createSpawnProcess(0, JSON.stringify({ summary: { READY: 1 } }))
        );

        const participant = VibecodingParticipant.create();
        const markdown = jest.fn();

        await participant.handleChatRequest(
            {
                prompt: 'show me status',
                command: 'status'
            } as never,
            {} as never,
            { markdown } as never,
            {} as never
        );

        expect(markdown).toHaveBeenCalledWith(expect.stringContaining('Ticket Dashboard'));
    });
});

describe('VibecodingParticipant additional coverage', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        VibecodingParticipant.disposeInstance();
    });

    it('returns empty dashboard message when summary has no stage entries', async () => {
        mockSpawn.mockReturnValue(createSpawnProcess(0, JSON.stringify({ summary: {} })));

        const participant = VibecodingParticipant.create();
        const response = await participant.handleStatusCommand();

        expect(response).toContain('_No tickets found_');
    });

    it('returns no changes message when sync output is whitespace only', async () => {
        mockSpawn.mockReturnValue(createSpawnProcess(0, '   \n\n'));

        const participant = VibecodingParticipant.create();
        const response = await participant.handleSyncCommand();

        expect(response).toContain('No changes detected.');
    });

    it('handles subprocess error events in command execution', async () => {
        const processEmitter = new EventEmitter() as SpawnMockProcess;
        processEmitter.stdout = new EventEmitter();
        processEmitter.stderr = new EventEmitter();
        setImmediate(() => processEmitter.emit('error', new Error('spawn failed')));
        mockSpawn.mockReturnValue(processEmitter);

        const participant = VibecodingParticipant.create();
        const response = await participant.handleStatusCommand();

        expect(response).toContain('Error retrieving status: spawn failed');
    });

    it('uses default priority when next ticket has no priority field', async () => {
        mockExistsSync.mockReturnValue(true);
        mockReaddirSync.mockReturnValue(['TASK-VIB-011.json']);
        mockReadFileSync.mockReturnValue(
            JSON.stringify({
                ticket_id: 'TASK-VIB-011',
                title: 'Sample ticket',
                type: 'backend'
            })
        );

        const participant = VibecodingParticipant.create();
        const response = await participant.handleNextCommand();

        expect(response).toContain('**Priority:** Normal');
    });

    it('exposes and clears singleton instance', () => {
        VibecodingParticipant.create();
        expect(VibecodingParticipant.getInstance()).not.toBeNull();
        VibecodingParticipant.disposeInstance();
        expect(VibecodingParticipant.getInstance()).toBeNull();
    });
});
