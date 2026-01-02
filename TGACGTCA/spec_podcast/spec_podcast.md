# Spec: Podcast Website

**Version:** 1.0  
**Last Updated:** 2025-11-03  
**Purpose:** Human-readable specification for deploying a production podcast website

---

## Goal
Deploy a production-ready podcast website featuring latest episode display, paginated episode listings, audio playback functionality, email subscription system, and administrative content management panel.

---

## Software Stack & Architecture

### Deployment Type
- [x] Web Application (browser-based)

### Technology Stack
- **Language:** JavaScript/TypeScript
- **Framework:** Next.js (React-based) or similar modern framework
- **Backend:** Insforge BaaS (provides database, authentication, file storage, email service)
- **Database:** Provided by Insforge (PostgreSQL/similar)
- **UI Library:** shadcn/ui components (Radix UI primitives + Tailwind CSS)
- **Component System:** shadcn/ui with MCP server integration for component discovery
- **Styling:** Tailwind CSS utility classes with CSS variables for theming
- **Packaging:** Static site generation + API routes deployed to Vercel/Netlify

### User Interface Requirements
- **Primary users:** Podcast listeners (non-technical users seeking mindfulness content), Podcast administrators (content managers)
- **Interaction method:** Web browser with point-and-click navigation
- **Technical skill level:** None (listeners), Basic (administrators using CMS-style interface)
- **Accessibility requirements:** Responsive design (mobile/tablet/desktop), intuitive navigation, calming mindfulness-inspired colour palette, clear audio controls

### Deployment Requirements
- **Target environment:** Web (any modern browser: Chrome, Firefox, Safari, Edge)
- **Installation method:** Open URL in browser (no installation required)
- **Configuration needed:** Domain name, Insforge API keys, email service credentials (configured during deployment)
- **Startup process:** Navigate to website URL

---

## Definition of Complete

What must exist and be verified:

### Functional Completeness
- [x] Homepage displays latest episode with title, description, and play button
- [x] Episode listings page shows episodes with 20-per-page pagination
- [x] Audio player functions correctly (play, pause, seek, volume control)
- [x] Email signup form captures subscriber emails and sends confirmation
- [x] Admin panel allows authenticated users to add, edit, delete episodes
- [x] Admin panel displays subscriber list

### Deployment Completeness
- [x] Website deployed to production hosting platform (Vercel/Netlify/similar)
- [x] Custom domain configured with SSL certificate
- [x] Insforge backend connected to production frontend
- [x] Audio files hosted and accessible via CDN or Insforge storage

### User Acceptance
- [x] Non-technical user can browse episodes without instruction
- [x] Audio playback works on mobile, tablet, and desktop devices
- [x] Admin can add new episode with audio file upload without developer assistance
- [x] Email subscriptions deliver successfully to subscriber inboxes

### Production Readiness
- [x] Insforge backend configured for production (not test mode)
- [x] Email service configured with production API keys
- [x] Error handling implemented for failed API calls
- [x] Performance tested with 50+ episodes

### Verification Method
1. Manual testing: Browse homepage, play episode, navigate pagination
2. Device testing: Test on mobile phone, tablet, desktop browser
3. Admin testing: Add/edit/delete test episode via admin panel
4. Email testing: Submit test subscription, verify confirmation email received
5. Load testing: Verify pagination works with 25+ episodes (simulating 2+ pages)

---

## Definitions
- **goal:** Deploy a complete, production-ready podcast website with listener and admin functionality
- **task[n]:** Discrete objectives that collectively build and deploy the website
- **step[m]:** Concrete actions within each task
- **backup[p]:** Alternative approaches if primary method fails
- **critical_flag:** Boolean indicating whether step failure blocks goal achievement
- **mode:** Execution mode (silent/collaborative/dynamic)
- **progress.json:** Execution log tracking all steps, retries, and outcomes

## Components
- Frontend web application (Next.js/React)
- Insforge BaaS backend (database, auth, storage, email)
- Audio player component
- Admin panel interface
- Email subscription system
- Production deployment (Vercel/Netlify + Insforge)

## Constraints
- Audio playback must work across Chrome, Firefox, Safari, Edge
- Admin panel must be usable by non-technical content managers
- Website must be responsive (mobile, tablet, desktop)
- Mindfulness-inspired design must be consistent across all pages
- Pagination must handle 100+ episodes gracefully
- Email deliverability rate ≥95%

---

## User Stories

- As a podcast listener, I want to see the latest episode on the homepage so I can quickly start listening to new content
- As a podcast listener, I want to browse previous episodes with pagination so I can find older content
- As a podcast listener, I want to play episodes directly on the website so I don't need external apps
- As a podcast listener, I want to subscribe for email updates so I'm notified about new episodes
- As a podcast administrator, I want to upload new episodes via admin panel so I can publish content without developer help
- As a podcast administrator, I want to edit episode descriptions so I can correct mistakes or update information
- As a podcast administrator, I want to view subscriber list so I can track audience growth

---

## Task [1]: Design and Setup Foundation
**TOML Reference:** `tasks[id=1]` in parameters_podcast.toml  
**Research Enabled:** true (current design trends for mindfulness/meditation websites)

### Step [1]: Research mindfulness web design patterns and colour schemes
- **Primary method:** Search for current mindfulness/meditation website design trends, colour psychology for calming interfaces, and modern podcast website layouts
- **Backup [1]:** If comprehensive research unavailable, analyse popular mindfulness apps (Calm, Headspace) and podcast platforms (Spotify, Apple Podcasts) for design patterns
- **Expected output:** Design requirements document specifying colour palette (hex codes), typography choices, layout patterns, and mindfulness-inspired visual elements
- **Critical:** true
- **Mode:** silent

### Step [2]: Create design system and visual identity
- **Primary method:** Define colour palette with 4-6 mindfulness-inspired colours (calming blues, greens, neutrals), typography scale, spacing system, and component design tokens
- **Backup [1]:** If custom design system too complex, adapt existing design system (Material UI, Chakra UI) with mindfulness colour overrides
- **Expected output:** Design system documentation with colour palette (hex codes), font families, spacing scale, and sample component mockups
- **Critical:** true
- **Mode:** silent

### Step [3]: Initialize project with Next.js, shadcn/ui, and Insforge backend
- **Primary method:** Create Next.js project with TypeScript, initialize shadcn/ui using `npx shadcn init` (selecting base color and style matching mindfulness palette), configure Insforge SDK, set up database schema (episodes, subscribers), and configure authentication
- **Backup [1]:** If Insforge integration issues arise, use Supabase as alternative BaaS
- **Backup [2]:** If BaaS approach blocked, set up custom Express.js backend with PostgreSQL and JWT authentication
- **Expected output:** Initialized project repository with working development server, shadcn/ui configured with components.json, Insforge connection verified, database schema created, Tailwind CSS and CSS variables configured
- **Critical:** true
- **Mode:** silent
- **Note:** MCP server integration available for autonomous component discovery and installation

### Step [4]: Configure development environment and tooling
- **Primary method:** Set up ESLint, Prettier, Git repository, environment variable management, and local development workflow
- **Expected output:** Development environment configured with linting rules, code formatting, version control initialized, and README with setup instructions
- **Critical:** false
- **Mode:** silent

**Verification:** Development server runs locally, Insforge connection authenticated, design system documented  
**Logging:** Append structured entry to progress_podcast.json for each step

---

## Task [2]: Implement Core Podcast Features
**TOML Reference:** `tasks[id=2]` in parameters_podcast.toml

### Step [1]: Build homepage with featured latest episode using shadcn/ui components
- **Primary method:** Create homepage component fetching latest episode from Insforge database, display title, description, cover image, and embedded audio player. Use shadcn/ui Card component for episode layout, add required components via `npx shadcn add card`
- **Backup [1]:** If dynamic fetching fails, implement static generation with revalidation
- **Expected output:** Homepage displays latest episode with all metadata, styled using shadcn/ui Card component with mindfulness theme, responsive across devices
- **Critical:** true
- **Mode:** silent
- **Note:** MCP tools available for component discovery: search for appropriate shadcn components for layout

### Step [2]: Create episode listing page with pagination using shadcn/ui components
- **Primary method:** Build episode archive page with grid/list layout using shadcn/ui Card components for episodes, implement pagination showing 20 episodes per page using shadcn/ui Pagination component (`npx shadcn add pagination`), add navigation controls
- **Backup [1]:** If server-side pagination complex, implement client-side pagination with all episodes loaded
- **Expected output:** Episode listing page with working pagination using shadcn/ui Pagination component, showing 20 episodes per page in Card layouts, navigation controls functional
- **Critical:** true
- **Mode:** silent

### Step [3]: Implement responsive audio player component
- **Primary method:** Build custom HTML5 audio player with play/pause, seek bar, volume control, current time display, and responsive design
- **Backup [1]:** If custom player development blocked, integrate third-party player library (React Player, Plyr)
- **Expected output:** Functional audio player component that works across browsers (Chrome, Firefox, Safari, Edge) and devices (mobile, tablet, desktop)
- **Critical:** true
- **Mode:** silent

### Step [4]: Apply mindfulness design system consistently
- **Primary method:** Style all components with defined colour palette, typography, spacing, and ensure visual consistency across pages
- **Expected output:** All pages styled consistently with mindfulness-inspired design, colour palette applied correctly, responsive design verified on mobile/tablet/desktop
- **Critical:** false
- **Mode:** silent

**Verification:** Homepage displays latest episode, pagination works with 20+ episodes, audio player functions on all target browsers  
**Logging:** Append structured entry to progress_podcast.json for each step

---

## Task [3]: Build Email Subscription System
**TOML Reference:** `tasks[id=3]` in parameters_podcast.toml

### Step [1]: Design and implement email signup form UI using shadcn/ui components
- **Primary method:** Create signup form component using shadcn/ui Form, Input, and Button components (`npx shadcn add form input button`), implement email validation, loading state, success/error toast notifications (use shadcn/ui Toast component)
- **Expected output:** Email signup form UI implemented using shadcn/ui components, form validation functional with error states, styled consistently with mindfulness design system
- **Critical:** false
- **Mode:** silent

### Step [2]: Connect form to Insforge backend and email service
- **Primary method:** Implement backend API route to save subscriber email to Insforge database, integrate with Insforge email service (or SendGrid/Mailgun) to send confirmation emails
- **Backup [1]:** If Insforge email service unavailable, integrate directly with SendGrid or Mailgun API
- **Expected output:** Form submission saves email to database, triggers confirmation email, API handles errors gracefully (duplicate emails, invalid formats)
- **Critical:** true
- **Mode:** silent

### Step [3]: Create subscription confirmation workflow
- **Primary method:** Implement double opt-in workflow with confirmation link, create welcome email template with mindfulness-inspired design, handle confirmation link click to mark subscriber as confirmed
- **Backup [1]:** If double opt-in too complex, implement single opt-in with immediate subscription activation
- **Expected output:** Confirmation email sent with activation link, clicking link marks subscriber as confirmed, welcome message displayed
- **Critical:** false
- **Mode:** silent

### Step [4]: Test email delivery and subscriber database
- **Primary method:** Submit test subscriptions with various email providers (Gmail, Outlook, Yahoo), verify emails delivered to inbox (not spam), confirm database records created correctly
- **Expected output:** Test subscriptions successful across 3+ email providers, emails delivered to inbox within 1 minute, database records accurate
- **Critical:** true
- **Mode:** silent

**Verification:** Email signup form functional, confirmation emails delivered successfully (≥95% deliverability), subscribers saved to database  
**Logging:** Append structured entry to progress_podcast.json for each step

---

## Task [4]: Develop Admin Panel
**TOML Reference:** `tasks[id=4]` in parameters_podcast.toml

### Step [1]: Implement authentication system using Insforge
- **Primary method:** Set up Insforge authentication with email/password login, create protected admin routes, implement session management and logout functionality
- **Backup [1]:** If Insforge auth issues arise, implement NextAuth.js with email/password provider
- **Expected output:** Admin login page functional, authentication prevents unauthorized access to admin routes, session persists across page refreshes, logout works correctly
- **Critical:** true
- **Mode:** silent

### Step [2]: Build episode management CRUD interface using shadcn/ui components
- **Primary method:** Create admin dashboard using shadcn/ui Table component for episode list (`npx shadcn add table`), implement forms using shadcn/ui Form components for adding/editing episodes (title, description, audio file upload, cover image), use Dialog component for confirmation dialogs (`npx shadcn add dialog`), add Button components for actions
- **Backup [1]:** If file upload to Insforge complex, implement URL input for externally hosted audio files
- **Expected output:** Admin can add new episode with all fields using shadcn/ui form components, edit existing episodes, delete episodes with confirmation dialog, changes reflect immediately on frontend
- **Critical:** true
- **Mode:** silent

### Step [3]: Create subscriber list management view using shadcn/ui Table component
- **Primary method:** Build subscriber list page using shadcn/ui Table component showing email, subscription date, confirmation status columns, implement search using shadcn/ui Input component, add export to CSV button
- **Backup [1]:** If export functionality complex, provide read-only table view without export
- **Expected output:** Admin can view complete subscriber list in shadcn/ui Table with email addresses, subscription dates, and confirmation status badges, list paginated if >50 subscribers
- **Critical:** false
- **Mode:** silent

### Step [4]: Test admin workflows and usability
- **Primary method:** Conduct usability testing of admin panel workflows (add episode, edit episode, view subscribers), verify non-technical user can complete tasks without assistance
- **Expected output:** Admin workflows tested and verified usable by non-technical content manager, any UX issues documented and resolved
- **Critical:** true
- **Mode:** silent

**Verification:** Admin authentication functional, episodes can be added/edited/deleted via admin panel, subscriber list accessible  
**Logging:** Append structured entry to progress_podcast.json for each step

---

## Task [5]: Deploy and Production Verification
**TOML Reference:** `tasks[id=5]` in parameters_podcast.toml

### Step [1]: Deploy frontend to production hosting platform
- **Primary method:** Deploy Next.js application to Vercel with automatic deployments from Git, configure environment variables for production Insforge API keys
- **Backup [1]:** If Vercel deployment issues, deploy to Netlify
- **Backup [2]:** If both fail, deploy to custom VPS with PM2 process manager
- **Expected output:** Frontend deployed and accessible via production URL, Insforge backend connected successfully, environment variables configured correctly
- **Critical:** true
- **Mode:** silent

### Step [2]: Configure production domain and SSL
- **Primary method:** Configure custom domain DNS records (A/CNAME) to point to hosting platform, enable SSL certificate via Let's Encrypt (automatic with Vercel/Netlify)
- **Expected output:** Custom domain resolves to website, HTTPS enabled with valid SSL certificate, HTTP redirects to HTTPS
- **Critical:** true
- **Mode:** silent

### Step [3]: Perform end-to-end production testing
- **Primary method:** Test all user workflows in production (browse homepage, play episode, submit email subscription, test pagination), test admin workflows (login, add/edit episode), verify on multiple devices and browsers
- **Backup [1]:** If production testing reveals critical issues, create hotfix branch, deploy fix, re-test
- **Expected output:** All features functional in production, cross-browser testing passed (Chrome, Firefox, Safari, Edge), mobile/tablet/desktop responsiveness verified, no critical bugs detected
- **Critical:** true
- **Mode:** silent

### Step [4]: Document deployment and create user guides
- **Primary method:** Create deployment documentation with production configuration details, environment variable reference, write admin user guide with screenshots for episode management workflows
- **Expected output:** Deployment documentation complete with configuration steps, admin user guide created with step-by-step instructions and screenshots for adding/editing episodes
- **Critical:** false
- **Mode:** silent

**Verification:** Website deployed to production URL with custom domain and SSL, all features tested and functional, documentation complete  
**Logging:** Append structured entry to progress_podcast.json for each step

---

## Bridging: Markdown ↔ TOML Synchronisation

This spec file (spec_podcast.md) must maintain perfect alignment with its companion file (parameters_podcast.toml).

**Bridging Requirements:**
1. Each task in this file has a corresponding `[[tasks]]` entry in TOML with matching ID
2. Each step within a task has a corresponding `[[tasks.steps]]` entry with matching ID
3. Each backup method is referenced in TOML structure
4. Expected outputs in this file match `expected_output` fields in TOML
5. Critical flags match between files

**Cross-References:**
- Task [1] = `tasks[id=1]` in parameters_podcast.toml
- Task [2] = `tasks[id=2]` in parameters_podcast.toml
- Task [3] = `tasks[id=3]` in parameters_podcast.toml
- Task [4] = `tasks[id=4]` in parameters_podcast.toml
- Task [5] = `tasks[id=5]` in parameters_podcast.toml

The exe_podcast.md controller validates this synchronisation during initialisation (Section 1.8).

---

### Instructions for LLM Executor
1. Start with the **goal** (deploy production podcast website)
2. Execute **tasks [1-5]** sequentially (no parallel execution)
3. For each task, execute **steps [1-n]** in order
4. Attempt **primary method** first, use **backups** only if primary fails
5. **Log all attempts** in progress_podcast.json
6. **Read progress.json** before each step (error propagation)
7. Verify outputs match expected outputs defined above
8. Mark step critical failures appropriately and escalate per dynamic mode rules
9. For Task [1], use research tools (web search, documentation) to gather current design trends

---

**End of spec_podcast.md**

