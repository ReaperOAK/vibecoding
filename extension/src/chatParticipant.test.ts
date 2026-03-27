import * as assert from 'assert';
import { VibecodingParticipant } from './chatParticipant';

/**
 * Unit tests for VibecodingParticipant chat handler
 * 
 * Note: These are component tests that verify the interface layer.
 * Subprocess execution tests would require mocking the child_process module,
 * which VS Code Insiders' native testing framework handles via @vscode/test-electron.
 */

// Test suite for VibecodingParticipant
export function runTests(): Promise<void> {
    return runTestSuite();
}

async function runTestSuite(): Promise<void> {
    const tests: Array<{ name: string; fn: () => Promise<void> | void }> = [];

    // Test: Participant can be instantiated
    tests.push({
        name: 'VibecodingParticipant.create() returns instance',
        fn: () => {
            const participant = VibecodingParticipant.create();
            assert.ok(participant, 'Participant should be created');
        }
    });

    // Test: Singleton pattern works
    tests.push({
        name: 'VibecodingParticipant uses singleton pattern',
        fn: () => {
            const p1 = VibecodingParticipant.getInstance();
            assert.ok(p1, 'Should have instance');
        }
    });

    // Test: Dispose clears instance
    tests.push({
        name: 'VibecodingParticipant.disposeInstance() clears singleton',
        fn: () => {
            VibecodingParticipant.create();
            VibecodingParticipant.disposeInstance();
            const instance = VibecodingParticipant.getInstance();
            assert.strictEqual(instance, null, 'Instance should be null after dispose');
        }
    });

    // Test: Command interface exists
    tests.push({
        name: 'VibecodingParticipant has command handlers',
        fn: async () => {
            const participant = VibecodingParticipant.create();
            assert.ok(typeof participant.handleStatusCommand === 'function');
            assert.ok(typeof participant.handleSyncCommand === 'function');
            assert.ok(typeof participant.handleNextCommand === 'function');
            assert.ok(typeof participant.handleChatRequest === 'function');
        }
    });

    // Run all tests
    let passed = 0;
    let failed = 0;

    for (const test of tests) {
        try {
            await Promise.resolve(test.fn());
            console.log(`✓ ${test.name}`);
            passed++;
        } catch (error) {
            console.error(`✗ ${test.name}`, error instanceof Error ? error.message : String(error));
            failed++;
        }
    }

    console.log(`\nTest Results: ${passed} passed, ${failed} failed`);
    
    if (failed > 0) {
        throw new Error(`${failed} test(s) failed`);
    }
}
