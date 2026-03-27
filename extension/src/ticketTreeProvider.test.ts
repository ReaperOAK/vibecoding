import * as assert from 'assert';
import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import { TicketTreeProvider, loadTicketGroups, TicketTreeNode } from './ticketTreeProvider';

function createTempWorkspace(): string {
    return fs.mkdtempSync(path.join(os.tmpdir(), 'vibecoding-tree-'));
}

function writeTicket(rootPath: string, stage: 'READY' | 'DONE', ticketId: string, title: string): void {
    const stagePath = path.join(rootPath, 'ticket-state', stage);
    fs.mkdirSync(stagePath, { recursive: true });
    fs.writeFileSync(
        path.join(stagePath, `${ticketId}.json`),
        JSON.stringify({ ticket_id: ticketId, title }, null, 2),
        'utf-8'
    );
}

function getStage(nodes: TicketTreeNode[], stage: 'READY' | 'DONE'): TicketTreeNode {
    const found = nodes.find((node) => node.kind === 'stage' && node.stage === stage);
    assert.ok(found, `${stage} stage should exist`);
    return found as TicketTreeNode;
}

async function runSuite(): Promise<void> {
    const tests: Array<{ name: string; fn: () => void | Promise<void> }> = [];

    tests.push({
        name: 'TreeProvider instantiation creates READY and DONE groups',
        fn: () => {
            const rootPath = createTempWorkspace();
            const provider = new TicketTreeProvider(rootPath);
            const root = provider.getChildren();

            assert.strictEqual(root.length, 2, 'Expected exactly two root groups');
            assert.ok(root.some((node) => node.kind === 'stage' && node.label === 'READY'));
            assert.ok(root.some((node) => node.kind === 'stage' && node.label === 'DONE'));
        }
    });

    tests.push({
        name: 'Loading tickets from filesystem returns READY and DONE data',
        fn: () => {
            const rootPath = createTempWorkspace();
            writeTicket(rootPath, 'READY', 'TASK-VIB-100', 'Ready ticket');
            writeTicket(rootPath, 'DONE', 'TASK-VIB-101', 'Done ticket');

            const groups = loadTicketGroups(rootPath);
            assert.strictEqual(groups.READY.length, 1);
            assert.strictEqual(groups.DONE.length, 1);
            assert.strictEqual(groups.READY[0].id, 'TASK-VIB-100');
            assert.strictEqual(groups.DONE[0].id, 'TASK-VIB-101');
        }
    });

    tests.push({
        name: 'Tree structure returns tickets under READY and DONE groups',
        fn: () => {
            const rootPath = createTempWorkspace();
            writeTicket(rootPath, 'READY', 'TASK-VIB-110', 'Ready item');
            writeTicket(rootPath, 'DONE', 'TASK-VIB-111', 'Done item');
            const provider = new TicketTreeProvider(rootPath);

            const roots = provider.getChildren();
            const readyGroup = getStage(roots, 'READY');
            const doneGroup = getStage(roots, 'DONE');

            const readyChildren = provider.getChildren(readyGroup);
            const doneChildren = provider.getChildren(doneGroup);

            assert.strictEqual(readyChildren.length, 1);
            assert.strictEqual(doneChildren.length, 1);
            assert.strictEqual(readyChildren[0].kind, 'ticket');
            assert.strictEqual(doneChildren[0].kind, 'ticket');
            assert.strictEqual(readyChildren[0].label, 'TASK-VIB-110');
            assert.strictEqual(doneChildren[0].label, 'TASK-VIB-111');
        }
    });

    tests.push({
        name: 'Refresh re-reads filesystem and emits change event',
        fn: () => {
            const rootPath = createTempWorkspace();
            const provider = new TicketTreeProvider(rootPath);
            let fired = 0;

            const subscription = provider.onDidChangeTreeData(() => {
                fired += 1;
            });

            writeTicket(rootPath, 'READY', 'TASK-VIB-120', 'Post-refresh ticket');
            provider.refresh();

            const roots = provider.getChildren();
            const readyGroup = getStage(roots, 'READY');
            const readyChildren = provider.getChildren(readyGroup);

            assert.strictEqual(fired, 1, 'Refresh should fire one event');
            assert.strictEqual(readyChildren.length, 1);
            assert.strictEqual(readyChildren[0].label, 'TASK-VIB-120');

            subscription.dispose();
        }
    });

    let passed = 0;
    let failed = 0;

    for (const test of tests) {
        try {
            await Promise.resolve(test.fn());
            process.stdout.write(`PASS ${test.name}\n`);
            passed += 1;
        } catch (error) {
            process.stderr.write(`FAIL ${test.name}: ${error instanceof Error ? error.message : String(error)}\n`);
            failed += 1;
        }
    }

    process.stdout.write(`\nResults: ${passed} passed, ${failed} failed\n`);
    if (failed > 0) {
        throw new Error(`${failed} test(s) failed`);
    }
}

export function runTests(): Promise<void> {
    return runSuite();
}

if (require.main === module) {
    runSuite().catch((error: unknown) => {
        process.stderr.write(`${error instanceof Error ? error.stack ?? error.message : String(error)}\n`);
        process.exit(1);
    });
}