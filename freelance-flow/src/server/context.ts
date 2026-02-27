import type { NextRequest } from 'next/server';
import { db } from './db';

export async function createContext(opts: { req: NextRequest }) {
  return {
    db,
    session: null, // Will be populated by auth middleware
    tenantId: null, // Will be populated by tenant middleware
  };
}

export type Context = Awaited<ReturnType<typeof createContext>>;
