# Design Requirements: Mindfulness Podcast Website

**Created:** 2025-11-03  
**Purpose:** Design system foundation based on mindfulness/wellness research

---

## Colour Palette

### Primary Colours (Mindfulness-Inspired)
- **Calming Teal:** `#20948B` - Primary brand colour (balance, healing, nature)
- **Soft Blue:** `#51d0de` - Secondary accent (trust, tranquillity, calm)
- **Light Sage Green:** `#6AB187` - Tertiary accent (vitality, balance, growth)

### Supporting Colours
- **Periwinkle Blue:** `#7acfd6` - UI accents, hover states (serenity, mindfulness)
- **Soft Lavender:** `#bf4aa8` (lightened to #e0c4da) - Gentle highlights (spirituality, wellness)
- **Warm Neutral:** `#f1f0ee` - Background, cards (clean, spacious)
- **Deep Slate:** `#3a4660` - Text, headers (grounding, readability)

### Rationale
Research shows blue-green palettes (teal, seafoam, periwinkle) are consistently used by successful meditation apps (Calm, Headspace) and wellness platforms. These colours:
- Reduce visual noise and cognitive load
- Evoke nature, healing, and tranquillity
- Create immersive, calming experiences
- Work well for mindfulness-focused audiences

---

## Typography

### Font Families
- **Headings:** Inter or Outfit (modern, clean, approachable)
- **Body Text:** Inter or System UI (readable, accessible)
- **Accent/Quotes:** Georgia or serif (warmth, wisdom)

### Type Scale
- H1: 2.5rem (40px) - Page titles
- H2: 2rem (32px) - Section headers
- H3: 1.5rem (24px) - Episode titles
- Body: 1rem (16px) - Standard text
- Small: 0.875rem (14px) - Metadata, captions

---

## Layout Patterns

### Homepage
- **Hero Section:** Latest episode featured prominently
- **Layout:** Clean, spacious with generous white space
- **Audio Player:** Embedded HTML5 player with custom styled controls
- **CTA:** Clear "Subscribe" button using teal primary colour

### Episode Listing
- **Grid Layout:** 2-3 columns on desktop, 1 column on mobile
- **Card Design:** Each episode in shadcn/ui Card component
  - Cover image (square aspect ratio)
  - Title and brief description
  - Play button overlay
  - Episode metadata (date, duration)
- **Pagination:** 20 episodes per page with clear navigation

### Design Principles
1. **Minimalism:** Reduce visual clutter, focus on content
2. **Spaciousness:** Generous padding and margins (calming effect)
3. **Consistency:** Unified colour application across all pages
4. **Accessibility:** High contrast text, clear focus states
5. **Responsive:** Mobile-first approach with fluid layouts

---

## Visual Elements

### Component Styling
- **Border Radius:** Soft rounded corners (8px-12px) for warmth
- **Shadows:** Subtle shadows for depth without harshness
- **Buttons:** Rounded, with smooth hover transitions
- **Cards:** Elevated appearance with soft shadows

### Imagery
- High-quality episode cover art
- Calming nature-inspired imagery where appropriate
- Consistent image treatment (soft overlays, uniform aspect ratios)

---

## Best Practices (From Research)

### Podcast Website Essentials
1. **Clear Navigation:** Simple menu structure
2. **Platform Icons:** Links to Spotify, Apple Podcasts, etc.
3. **Latest Episodes Prominent:** Featured on homepage
4. **Embedded Audio:** Direct playback without leaving site
5. **About/Contact Pages:** Clear information architecture
6. **SEO Optimisation:** Episode descriptions with keywords

### Wellness Design Principles
1. **Calming Colour Psychology:** Blues/greens reduce anxiety
2. **Visual Hierarchy:** Clear content prioritisation
3. **Microinteractions:** Smooth, delightful animations
4. **Emotional Design:** Create sense of peace and welcome
5. **Trust Signals:** Professional, cohesive aesthetic

---

## Component Requirements (shadcn/ui)

### Phase 1 (Core Features)
- Card (episode display)
- Button (CTAs, controls)
- Badge (episode metadata)

### Phase 2 (Email System)
- Form (email signup)
- Input (email field)
- Toast (notifications)

### Phase 3 (Admin Panel)
- Table (episode/subscriber lists)
- Dialog (confirmations)
- Form components (episode management)

---

## References
- Meditation apps: Calm (blue gradients), Headspace (calming colours, friendly design)
- Colour research: Teal/blue-green for healing and balance
- Podcast layouts: Grid displays, clear episode cards, embedded players
- 2025 trends: Soft palettes, emotional design, minimalist aesthetics


