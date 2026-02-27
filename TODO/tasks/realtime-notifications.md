# Real-Time Notifications — L3 Actionable Tasks

## FF-BE007-001: Define Notification Model & DB Schema

**Status:** READY
**Priority:** P1
**Owner:** Backend
**Depends On:** FF-BE001-001
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** no
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Add notification and preferences tables to Prisma schema
2. Run DB migration and verify schema
3. Document model relationships

**File Paths:**
- prisma/schema.prisma
- prisma/migrations/
- docs/db/notification-model.md

**Acceptance Criteria:**
- [ ] Notification and preferences tables created
- [ ] Migration runs without errors
- [ ] Model relationships documented
- [ ] All code and docs committed

**Description:**
Define and implement DB models for notifications and preferences. Ensure relationships are documented and schema is migrated.

---

## FF-BE007-002: Implement Notification API & Real-Time Delivery (SSE/Socket.io)

**Status:** READY
**Priority:** P1
**Owner:** Backend
**Depends On:** FF-BE007-001
**Effort:** 2h
**SDLC Phase:** BUILD
**UI Touching:** no
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Implement tRPC endpoints for notifications
2. Integrate SSE/Socket.io for real-time delivery
3. Write unit tests for API endpoints

**File Paths:**
- app/api/notifications/
- app/utils/realtime.ts
- tests/api/notifications.test.ts

**Acceptance Criteria:**
- [ ] Notification endpoints implemented and tested
- [ ] Real-time delivery functional (SSE/Socket.io)
- [ ] Unit tests cover all endpoints
- [ ] All code and tests committed

**Description:**
Implement tRPC API endpoints and real-time delivery for notifications. Ensure robust and tested real-time experience.

---

## FF-FE007-003: Build In-App Notification UI (Center, Badges, Toasts)

**Status:** READY
**Priority:** P1
**Owner:** Frontend Engineer
**Depends On:** FF-BE007-002, FF-FE002-001
**Effort:** 2h
**SDLC Phase:** BUILD
**UI Touching:** yes
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Build notification center, badges, and toast components
2. Integrate with real-time notification API
3. Test in-app notification flows

**File Paths:**
- app/notifications/
- app/components/notifications/

**Acceptance Criteria:**
- [ ] Notification center, badges, and toasts implemented
- [ ] Integration with real-time API
- [ ] All flows tested
- [ ] All code committed

**Description:**
Build in-app notification UI, including center, badges, and toasts. Integrate with real-time backend and ensure robust experience.

---

## FF-BE007-004: Integrate Email Notification Delivery

**Status:** READY
**Priority:** P2
**Owner:** Backend
**Depends On:** FF-BE007-002
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** no
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Integrate email delivery for key notification events
2. Test email notification flows
3. Document email templates

**File Paths:**
- app/api/notifications/email.ts
- docs/notifications/email-templates.md

**Acceptance Criteria:**
- [ ] Email delivery integrated for notifications
- [ ] Email flows tested
- [ ] Email templates documented
- [ ] All code and docs committed

**Description:**
Integrate email delivery for notifications. Ensure key events trigger emails and templates are documented.

---

## FF-BE007-005: Implement Notification Preferences (User Settings)

**Status:** READY
**Priority:** P2
**Owner:** Backend, Frontend
**Depends On:** FF-BE007-002, FF-FE007-003
**Effort:** 1h
**SDLC Phase:** BUILD
**UI Touching:** yes
**Created:** 2026-02-28T00:00:00Z

**What to do:**
1. Add user settings for notification types and channels
2. Build UI for managing notification preferences
3. Test preferences flows

**File Paths:**
- app/settings/notifications.tsx
- app/api/notifications/preferences.ts

**Acceptance Criteria:**
- [ ] User settings for notification preferences implemented
- [ ] UI for managing preferences
- [ ] All flows tested
- [ ] All code committed

**Description:**
Implement user settings and UI for notification preferences. Ensure users can manage notification types and channels.

---
