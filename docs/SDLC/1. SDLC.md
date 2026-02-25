# **The 6 Phases of Production-Grade Software Development (Detailed Artifact Edition)**

This document outlines the formal, structured phases of a professional software development life cycle (SDLC). It integrates the core process with the specific technical and planning artifacts (like SRS, UML, ERD, etc.) used at each stage.

While "vibecoding" optimizes for solo speed, this process optimizes for **long-term reliability, scalability, and maintainability** by a team. Every phase is a "gate" designed to manage and reduce a specific type of risk.

## **Pre-Phase: Business Strategy**

Before the SDLC for a specific project begins, the business must decide *which* projects to pursue.

* **Key Activity: Project Selection**  
  * This is a high-level business decision that answers "What problem should we solve?" It's based on analyzing cost, market opportunity, risk, and strategic alignment with company goals.

## **1\. Planning & Discovery**

This phase is about defining **what** the selected project is and **why** it's needed. It aligns the business, product, and engineering teams on a common goal.

* **Goal:** To validate an idea and define its functional and non-functional requirements.  
* **Risk Reduced:** Building the wrong product or a feature nobody needs.  
* **Primary Roles:** Product Managers (PMs), Business Analysts, UX Researchers, Tech Leads.  
* **Key Activities:**  
  * **Problem Analysis:** The primary activity of the discovery phase. It involves deep research into the business needs and user pain points.  
  * Analyzing business requirements and market research.  
  * Conducting user interviews and gathering feedback.  
  * Defining scope, success metrics, and potential trade-offs.  
  * Creating high-level User Stories (e.g., in Jira or Notion).  
* **Key Artifacts (Deliverables):**  
  * **SRS (Software Requirements Specification) / PRD (Product Requirements Document):** These are formal "source of truth" documents. An SRS is often more exhaustive and technical, but both define the feature's purpose, scope, and user-facing behavior.  
  * **User Stories:** A prioritized backlog of features (e.g., "As a user, I can reset my password...").  
  * **Project Plan (High-Level):** The initial roadmap, timeline, and resource plan created by the Product Manager and Tech Lead.

## **2\. Architecture & Design**

This phase is about defining **how** to build the feature, both visually and technically. This is where the majority of formal engineering diagrams are created.

* **Goal:** To create a precise technical and visual blueprint before writing code.  
* **Risk Reduced:** Building a fragile, unscalable, insecure, or hard-to-maintain system.  
* **Primary Roles:** Senior/Staff Engineers, Tech Leads, UI/UX Designers.  
* **Key Activities & Their Artifacts:**  
  * **UI/UX Design:** Creating wireframes, high-fidelity mockups, and the interactive **Project Prototype** (e.g., in Figma). This is the *visual* specification.  
  * **System & Logic Modeling:** Whiteboarding the technical architecture. This uses several diagram types to create the **Technical Design Doc (TDD)**:  
    * **Use Case Diagram (UML):** Visually maps User Stories from Phase 1 to "actors" (users) to show *who* can do *what*.  
    * **Activity Diagram (UML):** Models complex business logic or user flows (e.g., the step-by-step logic of a "password reset" feature).  
    * **Data Flow Diagram (DFD):** Shows how data moves *through* the different parts of the system.  
    * **Class Diagram (UML):** For Object-Oriented design, this models the static structure of the code (classes, attributes, methods, and relationships).  
  * **Data Modeling:** Defining the database schema.  
    * **Entity Relationship Diagram (ERD):** The primary blueprint for the database, showing all the tables (Entities) and their Relationships.  
    * **Data Dictionary:** A detailed specification for every piece of data (e.g., users.email: string, max\_length: 255, "Must be unique, indexed").  
  * **API Contract Definition:** Explicitly defining the API endpoints.  
    * **Sequence Diagram (UML):** The perfect tool for designing this. It shows how components (e.g., Frontend, Backend, Email Service) interact *in order* to complete a task.  
* **Key Artifacts (Deliverables):**  
  * **Figma Prototypes** (The Project Prototype).  
  * **Technical Design Doc (TDD):** A document containing the diagrams above (ERD, DFD, UML), data dictionary, and system boundaries.  
  * **API Contract:** A file (like swagger.json) that both front and back-end teams build against.

## **3\. Implementation (Build)**

This is the phase where engineers write the code, guided *strictly* by the artifacts from Phase 2\.

* **Goal:** To write clean, maintainable, and *tested* code that meets the specification.  
* **Risk Reduced:** Introducing bugs, regressions, or "technical debt" (messy code).  
* **Primary Roles:** Developers (Frontend, Backend, Full-stack).  
* **Key Activities:**  
  * Creating a new git branch for the feature.  
  * **Test-Driven Development (TDD):** Writing failing **Unit Test Cases** (as executable code) *before* writing the feature code.  
  * Writing the application code, following the tech spec (ERD, Class Diagrams) and API contract (Sequence Diagrams).  
  * **Code Review (CR):** A *non-negotiable* step where at least one other engineer must review the code for logic, style, security, and correctness before it can be merged.  
* **Key Artifacts (Deliverables):**  
  * A **Pull Request (PR)** with a clear description of changes.  
  * Merged code with a full suite of passing **Unit Test Cases**.

## **4\. Verification & QA (Quality Assurance)**

This phase is about verifying that the newly built feature works as intended *within the larger system* and didn't break anything else.

* **Goal:** To find and fix bugs before they reach the user.  
* **Risk Reduced:** Shipping a broken or buggy product to customers.  
* **Primary Roles:** QA (Quality Assurance) Engineers, SDETs (Software Devs in Test).  
* **Key Activities:**  
  * Defining the high-level test strategy in a **Unit Test Plan** and **E2E Test Plan**.  
  * **Continuous Integration (CI):** An automated system (like GitHub Actions) that builds the app and runs the *entire* test suite on every new commit.  
  * **Staging Deployment:** The CI pipeline automatically deploys the "QA-ready" build to a **Staging Environment** (a private clone of production).  
  * **Automated E2E Testing:** Running scripts (e.g., Cypress, Playwright) that execute the **E2E Test Cases** (which are based on the original **Use Case Diagrams** and **User Stories**).  
  * **Manual QA:** A QA engineer manually clicks through the new feature, trying to break it with edge cases.  
* **Key Artifacts (Deliverables):**  
  * A "QA Approved" build.  
  * A list of "Pass/Fail" automated test results.  
  * New bug tickets for any issues found.

## **5\. Release & Deployment**

This is the controlled process of shipping the code to real users.

* **Goal:** To release the new feature to production users safely, with zero downtime.  
* **Risk Reduced:** A chaotic or failed release that takes the entire application offline.  
* **Primary Roles:** DevOps Engineers, SREs (Site Reliability Engineers), or a fully automated pipeline.  
* **Key Activities:**  
  * **Continuous Deployment (CD):** An automated pipeline that takes the QA-approved build and deploys it to the production servers.  
  * **Phased Rollouts / Canary Releases:** The feature is released to 1% of users first. The team monitors for errors. If all is well, it's rolled out to 5%, then 20%, then 100%.  
  * **Feature Flags (Toggles):** The new code is deployed to 100% of users but is "turned off" by default. A Product Manager can log into a dashboard and "turn on" the feature for users, independent of a code deployment.  
* **Key Artifacts (Deliverables):**  
  * The feature is 100% live in production.  
  * Updated documentation for the new feature.

## **6\. Operation & Maintenance**

The "vibecoding" process often ends at deployment. The professional process is just beginning. The feature must be supported for its entire lifetime.

* **Goal:** To ensure the feature *stays* fast, available, and correct in the real world.  
* **Risk Reduced:** The app being slow, buggy, or down without the team knowing ("silent failures").  
* **Primary Roles:** SREs, DevOps, On-call Engineers.  
* **Key Activities:**  
  * **Monitoring & Observability:** Watching dashboards (e.g., in Datadog, Grafana) that track error rates, application performance (latency), and server health.  
  * **Logging:** Collecting and analyzing logs from production servers to trace user issues (e.g., in Splunk, LogRocket).  
  * **Incident Response:** An automated alert fires (e.g., "Login error rate is over 5%\!"). An "on-call" engineer is paged to investigate and fix the issue immediately.  
  * **Bug Triage & Feedback Loop:** A user reports a bug. This creates a new ticket, which goes back to **Phase 1 (Planning)** to be prioritized, starting the entire cycle over again.  
* **Key Artifacts (Deliverables):**  
  * A stable, healthy application.  
  * Dashboards and alerts.  
  * A prioritized backlog of bugs and improvements.