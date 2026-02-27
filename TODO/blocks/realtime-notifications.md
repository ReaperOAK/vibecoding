# Block: Real-Time Notifications

**Block ID:** BLOCK-BE007
**Capability Reference:** TODO-BE007
**Description:** In-app and email notifications for key events and workflow changes. Ensures users and clients are kept up to date in real time.

## Sub-Blocks

1. **BE007-1: Notification Model & DB**
   - Define DB schema for notifications, preferences
   - **Effort:** 0.5 day
   - **Owner:** Backend

2. **BE007-2: Notification API & SSE/Socket.io**
   - Implement tRPC endpoints, SSE/Socket.io for real-time delivery
   - **Effort:** 1 day
   - **Owner:** Backend

3. **BE007-3: In-App Notification UI**
   - Frontend for notification center, badges, toasts
   - **Effort:** 0.5 day
   - **Owner:** Frontend

4. **BE007-4: Email Notification Integration**
   - Send email notifications for key events
   - **Effort:** 0.5 day
   - **Owner:** Backend

5. **BE007-5: Notification Preferences**
   - User settings for notification types, channels
   - **Effort:** 0.5 day
   - **Owner:** Backend/Frontend

## Dependencies
- BLOCK-DO001 (cloud infra/CI)
- BLOCK-BE008 (auth/RBAC)
- BLOCK-BE001 (multi-tenant core)
- BLOCK-FE002 (UI design system)

---
