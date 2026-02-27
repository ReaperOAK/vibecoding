import type { NextRequest } from 'next/server';
import { auth } from '@/lib/auth';
import { db } from './db';

export async function createContext(opts: { req: NextRequest }) {
  const session = await auth();
  return {
    db,
    session,
    userId: session?.user?.id ?? null,
    tenantId: (session?.user as any)?.tenantId ?? null,
  };
}

export type Context = Awaited<ReturnType<typeof createContext>>;
