# FreelanceFlow Design System

## 1. Color Palette
- **Primary:** Deep Indigo (#25316D)
- **Accent:** Vibrant Teal (#1EC6B6)
- **Semantic:**
  - Success: #27AE60
  - Warning: #F2C94C
  - Error: #EB5757
  - Info: #2D9CDB
- **Background:** #F7F9FB (light), #181A20 (dark)
- **Surface:** #FFFFFF (light), #23272F (dark)
- **Text:** #1A2233 (light), #F7F9FB (dark)

## 2. Typography
- **Font Family:** Inter, system-ui, sans-serif
- **Font Sizes:** xs (12px), sm (14px), md (16px), lg (18px), xl (24px), 2xl (32px), 3xl (40px), 4xl (56px)
- **Font Weights:** 400 (Regular), 500 (Medium), 600 (SemiBold), 700 (Bold)
- **Line Height:** 1.5

## 3. Spacing System
- **Base Unit:** 4px
- **Tokens:** 4, 8, 12, 16, 20, 24, 32, 40, 48, 56, 64px

## 4. Border Radius
- **sm:** 4px
- **md:** 8px
- **lg:** 16px
- **full:** 9999px (for pills, avatars)

## 5. Shadows (Elevation)
- **sm:** 0 1px 2px rgba(20,30,60,0.06)
- **md:** 0 2px 8px rgba(20,30,60,0.10)
- **lg:** 0 4px 16px rgba(20,30,60,0.12)
- **xl:** 0 8px 32px rgba(20,30,60,0.16)

## 6. Component Tokens
- **Button:**
  - Primary: Indigo bg, white text, teal hover
  - Secondary: White bg, indigo border, indigo text
  - Disabled: Gray bg, gray text
- **Input:**
  - Border: md radius, 1px solid #D1D5DB
  - Focus: 2px teal shadow
- **Card:**
  - Surface bg, md radius, md shadow
- **Badge:**
  - Pill shape, accent bg, white text

## 7. Dark Mode Support
- All tokens have light/dark variants
- Use CSS variables for theme switching

## 8. Motion
- **Transition Durations:** 120ms (fast), 240ms (normal), 400ms (slow)
- **Easing:** cubic-bezier(0.4,0,0.2,1)

## 9. Responsive Breakpoints
- **Mobile:** 320-768px
- **Tablet:** 768-1024px
- **Desktop:** 1024px+

## 10. Accessibility
- All colors meet WCAG 2.1 AA contrast
- Focus indicators: 2px solid accent
- Keyboard navigation: Tab order, skip links
- Screen reader labels for all controls

---

**See mockup specs for component usage and layout patterns.**