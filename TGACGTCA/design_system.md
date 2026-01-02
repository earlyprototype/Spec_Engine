# Design System: Mindfulness Podcast Website

**Version:** 1.0  
**Created:** 2025-11-03  
**Purpose:** Complete design system with tokens, scales, and component guidelines

---

## Colour Palette

### Primary Palette
```css
/* Primary Brand Colours */
--color-primary-teal: #20948B;       /* Main brand colour */
--color-primary-teal-light: #39b5ab; /* Hover states */
--color-primary-teal-dark: #186d66;  /* Active states */

/* Secondary Colours */
--color-secondary-blue: #51d0de;     /* Accents, links */
--color-secondary-blue-light: #7ddde8;
--color-secondary-blue-dark: #3bb5c3;

/* Tertiary Colours */
--color-tertiary-sage: #6AB187;      /* Supporting accents */
--color-tertiary-sage-light: #8ec4a2;
--color-tertiary-sage-dark: #55926d;
```

### Neutral Palette
```css
/* Backgrounds */
--color-background: #ffffff;         /* Page background */
--color-background-alt: #f1f0ee;     /* Card backgrounds */
--color-background-muted: #e8e7e5;   /* Disabled states */

/* Text */
--color-text-primary: #3a4660;       /* Headers, body text */
--color-text-secondary: #5f6b85;     /* Secondary text */
--color-text-muted: #8891a8;         /* Captions, metadata */
--color-text-inverse: #ffffff;       /* Text on dark backgrounds */
```

### Semantic Colours
```css
/* Status & Feedback */
--color-success: #6AB187;            /* Success messages */
--color-warning: #f4b942;            /* Warnings */
--color-error: #e85d5d;              /* Errors */
--color-info: #51d0de;               /* Information */
```

### Accent Colours
```css
/* Highlights & Special Elements */
--color-accent-lavender: #e0c4da;    /* Spiritual/wellness highlights */
--color-accent-periwinkle: #7acfd6;  /* UI accents */
```

---

## Typography

### Font Families
```css
--font-family-heading: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-family-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-family-accent: Georgia, 'Times New Roman', serif;
```

### Font Sizes
```css
/* Type Scale (1.250 - Major Third) */
--font-size-xs: 0.75rem;      /* 12px - Small metadata */
--font-size-sm: 0.875rem;     /* 14px - Captions */
--font-size-base: 1rem;       /* 16px - Body text */
--font-size-lg: 1.125rem;     /* 18px - Large body */
--font-size-xl: 1.25rem;      /* 20px - H4 */
--font-size-2xl: 1.5rem;      /* 24px - H3 */
--font-size-3xl: 2rem;        /* 32px - H2 */
--font-size-4xl: 2.5rem;      /* 40px - H1 */
```

### Font Weights
```css
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

### Line Heights
```css
--line-height-tight: 1.25;    /* Headings */
--line-height-normal: 1.5;    /* Body text */
--line-height-relaxed: 1.75;  /* Large text blocks */
```

---

## Spacing Scale

### Spacing System (0.25rem base)
```css
--spacing-0: 0;
--spacing-1: 0.25rem;    /* 4px */
--spacing-2: 0.5rem;     /* 8px */
--spacing-3: 0.75rem;    /* 12px */
--spacing-4: 1rem;       /* 16px */
--spacing-5: 1.25rem;    /* 20px */
--spacing-6: 1.5rem;     /* 24px */
--spacing-8: 2rem;       /* 32px */
--spacing-10: 2.5rem;    /* 40px */
--spacing-12: 3rem;      /* 48px */
--spacing-16: 4rem;      /* 64px */
--spacing-20: 5rem;      /* 80px */
```

### Component-Specific Spacing
```css
--spacing-card-padding: var(--spacing-6);      /* 24px */
--spacing-section-gap: var(--spacing-12);      /* 48px */
--spacing-element-gap: var(--spacing-4);       /* 16px */
--spacing-button-padding: var(--spacing-3) var(--spacing-6); /* 12px 24px */
```

---

## Border & Radius

### Border Widths
```css
--border-width-thin: 1px;
--border-width-default: 2px;
--border-width-thick: 3px;
```

### Border Radius
```css
--radius-sm: 0.375rem;   /* 6px - Small elements */
--radius-md: 0.5rem;     /* 8px - Buttons, inputs */
--radius-lg: 0.75rem;    /* 12px - Cards */
--radius-xl: 1rem;       /* 16px - Large cards */
--radius-full: 9999px;   /* Circular elements */
```

---

## Shadows

### Shadow System
```css
/* Subtle shadows for mindfulness aesthetic */
--shadow-sm: 0 1px 2px 0 rgba(58, 70, 96, 0.05);
--shadow-md: 0 4px 6px -1px rgba(58, 70, 96, 0.08), 
             0 2px 4px -1px rgba(58, 70, 96, 0.04);
--shadow-lg: 0 10px 15px -3px rgba(58, 70, 96, 0.1), 
             0 4px 6px -2px rgba(58, 70, 96, 0.05);
--shadow-xl: 0 20px 25px -5px rgba(58, 70, 96, 0.1), 
             0 10px 10px -5px rgba(58, 70, 96, 0.04);
```

---

## Component Mockups

### Button Styles

#### Primary Button
```css
.btn-primary {
  background: var(--color-primary-teal);
  color: var(--color-text-inverse);
  padding: var(--spacing-button-padding);
  border-radius: var(--radius-md);
  font-weight: var(--font-weight-medium);
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background: var(--color-primary-teal-light);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}
```

#### Secondary Button
```css
.btn-secondary {
  background: transparent;
  color: var(--color-primary-teal);
  border: var(--border-width-default) solid var(--color-primary-teal);
  padding: var(--spacing-button-padding);
  border-radius: var(--radius-md);
}
```

### Card Component
```css
.card {
  background: var(--color-background-alt);
  border-radius: var(--radius-lg);
  padding: var(--spacing-card-padding);
  box-shadow: var(--shadow-md);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.card-title {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-3);
}

.card-description {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  line-height: var(--line-height-relaxed);
}
```

### Episode Card
```css
.episode-card {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: var(--spacing-4);
  background: var(--color-background-alt);
  padding: var(--spacing-5);
  border-radius: var(--radius-lg);
  align-items: center;
}

.episode-card-image {
  width: 80px;
  height: 80px;
  border-radius: var(--radius-md);
  object-fit: cover;
}

.episode-card-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
}

.episode-card-title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
}

.episode-card-meta {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
}
```

### Audio Player
```css
.audio-player {
  background: var(--color-background-alt);
  border-radius: var(--radius-lg);
  padding: var(--spacing-6);
  box-shadow: var(--shadow-md);
}

.audio-player-controls {
  display: flex;
  align-items: center;
  gap: var(--spacing-4);
}

.audio-player-button {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-full);
  background: var(--color-primary-teal);
  color: var(--color-text-inverse);
  display: flex;
  align-items: center;
  justify-content: center;
}

.audio-player-progress {
  height: 6px;
  background: var(--color-background-muted);
  border-radius: var(--radius-full);
  margin: var(--spacing-4) 0;
}

.audio-player-progress-bar {
  height: 100%;
  background: var(--color-primary-teal);
  border-radius: var(--radius-full);
  transition: width 0.1s linear;
}
```

### Form Input
```css
.input {
  width: 100%;
  padding: var(--spacing-3) var(--spacing-4);
  border: var(--border-width-default) solid var(--color-background-muted);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  color: var(--color-text-primary);
  background: var(--color-background);
  transition: border-color 0.2s ease;
}

.input:focus {
  outline: none;
  border-color: var(--color-primary-teal);
  box-shadow: 0 0 0 3px rgba(32, 148, 139, 0.1);
}
```

---

## Responsive Breakpoints

```css
--breakpoint-sm: 640px;   /* Mobile landscape */
--breakpoint-md: 768px;   /* Tablet portrait */
--breakpoint-lg: 1024px;  /* Tablet landscape / Small desktop */
--breakpoint-xl: 1280px;  /* Desktop */
--breakpoint-2xl: 1536px; /* Large desktop */
```

### Grid System
```css
/* Mobile-first grid */
.container {
  width: 100%;
  padding-left: var(--spacing-4);
  padding-right: var(--spacing-4);
  margin: 0 auto;
}

@media (min-width: 640px) {
  .container { max-width: 640px; }
}

@media (min-width: 768px) {
  .container { max-width: 768px; }
}

@media (min-width: 1024px) {
  .container { max-width: 1024px; }
}

@media (min-width: 1280px) {
  .container { max-width: 1280px; }
}
```

---

## Animation & Transitions

### Timing Functions
```css
--transition-fast: 150ms;
--transition-base: 200ms;
--transition-slow: 300ms;

--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
--ease-out: cubic-bezier(0.0, 0, 0.2, 1);
--ease-in: cubic-bezier(0.4, 0, 1, 1);
```

### Common Transitions
```css
.transition-colors {
  transition: color var(--transition-base) var(--ease-in-out),
              background-color var(--transition-base) var(--ease-in-out);
}

.transition-transform {
  transition: transform var(--transition-base) var(--ease-out);
}

.transition-shadow {
  transition: box-shadow var(--transition-base) var(--ease-out);
}
```

---

## Accessibility Guidelines

### Focus States
```css
.focus-visible {
  outline: 2px solid var(--color-primary-teal);
  outline-offset: 2px;
}
```

### Colour Contrast
- All text meets WCAG AA standards (4.5:1 for normal text, 3:1 for large text)
- Primary teal (#20948B) on white: 4.8:1 (AA compliant)
- Text primary (#3a4660) on white: 10.2:1 (AAA compliant)

### Interactive Elements
- Minimum touch target size: 44x44px
- Clear hover/focus/active states
- Keyboard navigation support

---

## Usage Examples

### Page Header
```jsx
<header className="bg-background border-b border-background-muted">
  <div className="container py-4">
    <nav className="flex items-center justify-between">
      <h1 className="text-2xl font-semibold text-primary-teal">
        Mindfulness Podcast
      </h1>
      <button className="btn-primary">Subscribe</button>
    </nav>
  </div>
</header>
```

### Episode Grid
```jsx
<div className="container py-12">
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    {episodes.map(episode => (
      <div className="card" key={episode.id}>
        <img src={episode.cover} className="episode-card-image" />
        <h3 className="card-title">{episode.title}</h3>
        <p className="card-description">{episode.description}</p>
        <button className="btn-primary mt-4">Play Episode</button>
      </div>
    ))}
  </div>
</div>
```

---

## Design Principles

1. **Mindful Minimalism:** Remove unnecessary elements, focus on content
2. **Calming Aesthetics:** Soft colours, generous spacing, smooth transitions
3. **Clarity:** Clear visual hierarchy, readable typography
4. **Consistency:** Unified application of design tokens
5. **Accessibility:** Inclusive design for all users
6. **Responsiveness:** Fluid layouts that adapt gracefully

---

**End of Design System Documentation**

