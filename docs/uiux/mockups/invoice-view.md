# Invoice View — Mockup Spec

## Overview
Detailed invoice page for clients to review and pay invoices.

## Layout
- **Header:** Invoice number, date, due date, status badge
- **Line Items Table:** Description, hours, rate, amount
- **Total:** Subtotal, tax, grand total
- **Payment Button:** Stripe integration, status
- **Payment History:** List of past payments

## Components
- **Invoice Header:** Number, status, dates
- **Line Item Row:** Description, qty, rate, amount
- **Total Card:** Tax, total
- **Payment Button:** Primary (pay), disabled (paid)
- **Payment History Item:** Date, amount, method

## States
- Paid, unpaid, overdue
- Payment failed

## Responsive
- Mobile: Table → stacked list
- Tablet: Table scrolls
- Desktop: Full table

## Accessibility
- Table ARIA roles
- Focus indicators
- Screen reader labels for amounts
