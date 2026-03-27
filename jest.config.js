/** @type {import('jest').Config} */
module.exports = {
  rootDir: '.',
  roots: ['<rootDir>/extension/src'],
  testMatch: ['**/*.test.ts'],
  transform: {
    '^.+\\.ts$': [
      '<rootDir>/extension/node_modules/ts-jest/dist/index.js',
      {
        tsconfig: '<rootDir>/extension/tsconfig.json',
        diagnostics: false,
        isolatedModules: true
      }
    ]
  },
  testEnvironment: 'node',
  collectCoverage: true,
  collectCoverageFrom: [
    'extension/src/chatParticipant.ts',
    'extension/src/ticketTreeProvider.ts'
  ],
  coverageDirectory: 'coverage',
  coverageThreshold: {
    '**/ticketTreeProvider.ts': {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    },
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  }
};
