# Aesthetic Strategy for Boutique Handcrafted Scarves E-Commerce

## Executive Summary

This document defines the visual identity, design system, and aesthetic principles for the boutique scarf shop e-commerce platform. The strategy balances luxury positioning with accessibility, artisan authenticity with modern usability.

---

## 1. Brand Positioning

### Target Audience
- **Primary:** Affluent consumers (30-55 years) who value craftsmanship and unique design
- **Secondary:** Gift buyers seeking meaningful, high-quality items
- **Tertiary:** Conscious consumers prioritising handmade/ethical fashion

### Brand Personality
- **Elegant** yet approachable
- **Artisan** but not rustic
- **Premium** without being ostentatious
- **Modern** with timeless appeal

---

## 2. Colour Palette

### Primary Colours

#### Luxury Purple Gradient
- **Primary 1:** `#667eea` (Soft Periwinkle)
  - Usage: Headers, primary CTAs, brand accents
  - Psychology: Creativity, luxury, artisan craftsmanship
  
- **Primary 2:** `#764ba2` (Royal Purple)
  - Usage: Gradients, hover states, premium features
  - Psychology: Sophistication, exclusivity

**Rationale:** Purple has historically signified royalty and luxury. The gradient creates movement and visual interest whilst maintaining elegance.

### Neutral Foundation

#### Greys (Primary)
- **Dark:** `#1f2937` (Charcoal)
  - Usage: Primary text, footer, navigation
  - Contrast Ratio: 15.3:1 (WCAG AAA)

- **Medium:** `#6b7280` (Slate Grey)
  - Usage: Secondary text, descriptions, metadata
  - Contrast Ratio: 7.1:1 (WCAG AAA)

- **Light:** `#9ca3af` (Silver)
  - Usage: Placeholders, disabled states, hints
  - Contrast Ratio: 4.6:1 (WCAG AA)

- **Ultra-Light:** `#e5e7eb` (Platinum)
  - Usage: Borders, dividers, subtle backgrounds
  
- **Background:** `#f5f5f5` (Whisper)
  - Usage: Page background, card containers

#### Whites
- **Pure White:** `#ffffff`
  - Usage: Card backgrounds, modals, content areas

### Accent Colours

#### Success/Positive (Stock Available)
- **Primary:** `#059669` (Emerald)
  - Usage: In stock indicators, success messages
  
- **Light:** `#4ade80` (Mint)
  - Usage: Connected states, confirmations

#### Alert/Error
- **Danger:** `#dc2626` (Ruby)
  - Usage: Error messages, out of stock, critical alerts
  
- **Warning:** `#f59e0b` (Amber)
  - Usage: Low stock, pending actions

#### Information
- **Info:** `#3b82f6` (Azure)
  - Usage: Information badges, tooltips

### Metallic Accents (Future Enhancement)
- **Gold:** `#d4af37` - for premium/featured products
- **Rose Gold:** `#b76e79` - limited editions
- **Silver:** `#c0c0c0` - standard products

**Implementation Note:** Metallic gradients to be CSS-based for performance, not images.

---

## 3. Typography

### Font Stack

#### Primary (Body & UI)
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 
             'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 
             'Droid Sans', 'Helvetica Neue', sans-serif;
```
**Rationale:** System fonts ensure instant loading, native feel, and optimal readability across platforms.

#### Display/Headers (Optional Enhancement)
**Recommendation:** Add `'Playfair Display'` or `'Cormorant Garamond'` for luxury serif accents
```css
font-family: 'Playfair Display', Georgia, serif;
```
**Usage:** Hero headlines, product names, special announcements

#### Monospace (Code/Technical)
```css
font-family: 'Courier New', Consolas, Monaco, monospace;
```
**Usage:** Order numbers, API codes, technical information

### Type Scale

| Element | Size | Weight | Line Height | Usage |
|---------|------|--------|-------------|-------|
| H1 | 2.5rem (40px) | 700 | 1.2 | Hero headlines |
| H2 | 2rem (32px) | 600 | 1.3 | Section headers |
| H3 | 1.5rem (24px) | 600 | 1.4 | Subsections |
| H4 | 1.25rem (20px) | 600 | 1.4 | Card titles |
| Body Large | 1.125rem (18px) | 400 | 1.6 | Intro paragraphs |
| Body | 1rem (16px) | 400 | 1.6 | Standard text |
| Small | 0.875rem (14px) | 400 | 1.5 | Metadata, captions |
| Tiny | 0.75rem (12px) | 400 | 1.4 | Labels, legal |

### Responsive Adjustments
```css
@media (max-width: 768px) {
  H1: 1.8rem (28.8px)
  H2: 1.5rem (24px)
}
```

---

## 4. Spacing System

### Base Unit: 0.25rem (4px)

| Token | Value | Usage |
|-------|-------|-------|
| xs | 0.25rem (4px) | Tight spacing, icon padding |
| sm | 0.5rem (8px) | Element padding, small gaps |
| md | 1rem (16px) | Standard spacing |
| lg | 1.5rem (24px) | Section padding |
| xl | 2rem (32px) | Large section gaps |
| 2xl | 3rem (48px) | Hero sections |
| 3xl | 4rem (64px) | Major page divisions |

### Grid System
- **Max Content Width:** 1200px (prevents ultra-wide layouts)
- **Gutter:** 2rem (32px)
- **Columns:** 12-column flexible grid

---

## 5. Visual Elements

### Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| sm | 4px | Buttons, badges, small elements |
| md | 8px | Cards, inputs, standard UI |
| lg | 12px | Large cards, modals, images |
| xl | 16px | Hero sections, feature cards |
| full | 9999px | Pills, tags, circular elements |

**Brand Standard:** 12px for primary UI elements creates soft, approachable feel.

### Shadows

#### Elevation Scale
```css
/* Subtle (cards at rest) */
shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.06);

/* Standard (cards, dropdowns) */
shadow-md: 0 2px 8px rgba(0, 0, 0, 0.1);

/* Elevated (modals, hover states) */
shadow-lg: 0 4px 12px rgba(0, 0, 0, 0.15);

/* Dramatic (hero images, featured products) */
shadow-xl: 0 8px 24px rgba(0, 0, 0, 0.2);
```

**Hover Enhancement:**
```css
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.18);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Gradients

#### Primary Gradient (Brand)
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

#### Subtle Overlay (Hero Images)
```css
background: linear-gradient(
  to bottom, 
  rgba(102, 126, 234, 0.1) 0%, 
  rgba(118, 75, 162, 0.2) 100%
);
```

#### Shimmer Effect (Loading States)
```css
background: linear-gradient(
  90deg,
  rgba(255, 255, 255, 0) 0%,
  rgba(255, 255, 255, 0.6) 50%,
  rgba(255, 255, 255, 0) 100%
);
```

---

## 6. Component Aesthetics

### Product Cards

#### Structure
```
┌─────────────────────┐
│                     │
│   [Product Image]   │  ← 200px height, object-fit: cover
│                     │
├─────────────────────┤
│ Product Name        │  ← H4, 1rem padding
│ Brief description   │  ← Body Small, grey
├─────────────────────┤
│ £125.00  | In Stock │  ← Price (large, purple) | Status
└─────────────────────┘
```

#### Design Specs
- **Background:** Pure white (`#ffffff`)
- **Border Radius:** 12px
- **Shadow:** 0 2px 8px rgba(0, 0, 0, 0.1)
- **Hover:** Transform Y(-4px), enhanced shadow
- **Transition:** 0.3s ease-out
- **Image Aspect Ratio:** 4:3 (consistent across products)

### Buttons

#### Primary (Call-to-Action)
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
color: #ffffff;
padding: 0.75rem 2rem;
border-radius: 8px;
font-weight: 600;
box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
transition: all 0.2s ease;

&:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}
```

#### Secondary (Outline)
```css
background: transparent;
color: #667eea;
border: 2px solid #667eea;
padding: 0.75rem 2rem;
border-radius: 8px;

&:hover {
  background: rgba(102, 126, 234, 0.1);
}
```

#### Ghost/Tertiary
```css
background: transparent;
color: #6b7280;
padding: 0.75rem 1.5rem;

&:hover {
  color: #667eea;
  background: rgba(102, 126, 234, 0.05);
}
```

### Forms & Inputs

```css
input, textarea, select {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  transition: border-color 0.2s;
  
  &:focus {
    border-color: #667eea;
    outline: none;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
  
  &:disabled {
    background: #f5f5f5;
    color: #9ca3af;
    cursor: not-allowed;
  }
}
```

### Navigation

#### Header
- **Background:** White with subtle shadow
- **Height:** 80px
- **Sticky:** Yes (position: sticky, top: 0, z-index: 50)
- **Logo:** Left-aligned, 40px height
- **Cart Icon:** Badge with count (purple circle)

#### Mobile Menu
- **Activation:** Hamburger icon (3 lines, 20px width)
- **Transition:** Slide from right
- **Overlay:** rgba(0, 0, 0, 0.5)

---

## 7. Photography & Imagery

### Product Photography Guidelines

#### Technical Specs
- **Resolution:** Minimum 1200x900px (retina-ready)
- **Format:** WebP (primary), JPEG (fallback)
- **Aspect Ratio:** 4:3 (consistent across site)
- **Background:** Pure white (#ffffff) or lifestyle context
- **Lighting:** Soft, diffused, natural-looking

#### Style Guide
- **Angles:** 3/4 view showing texture and drape
- **Context:** Styled on mannequin or model (not flat lay)
- **Detail Shots:** Close-ups showing fabric texture, stitching, patterns
- **Lifestyle:** Worn in natural settings (30% of images)

#### Image Treatment
```css
.product-image {
  object-fit: cover;
  filter: brightness(1.05) contrast(1.02) saturate(1.1);
  transition: transform 0.3s;
}

.product-card:hover .product-image {
  transform: scale(1.05);
}
```

### Hero Images
- **Size:** 1920x800px (2.4:1 ratio)
- **Overlay:** Linear gradient (subtle purple tint)
- **Text:** Large, white, left-aligned with ample padding
- **CTA:** Prominent button (primary style)

### Icons
- **Style:** Outline (not filled) for clean, modern look
- **Stroke Width:** 2px
- **Source:** [Heroicons](https://heroicons.com/) or [Feather Icons](https://feathericons.com/)
- **Size:** 20px (standard), 24px (larger contexts)
- **Colour:** Inherit from context or purple brand colour

---

## 8. Animation & Micro-interactions

### Timing Functions

```css
/* Standard easing */
--ease-out: cubic-bezier(0.4, 0, 0.2, 1);

/* Bounce effect */
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);

/* Smooth */
--ease-smooth: cubic-bezier(0.25, 0.46, 0.45, 0.94);
```

### Key Animations

#### Hover States
```css
/* Card lift */
transform: translateY(-4px);
transition: transform 0.3s var(--ease-out);

/* Button press */
transform: scale(0.98);
transition: transform 0.1s;
```

#### Loading States
```css
@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.loading {
  background: linear-gradient(90deg, 
    rgba(255,255,255,0) 0%, 
    rgba(255,255,255,0.6) 50%, 
    rgba(255,255,255,0) 100%);
  animation: shimmer 1.5s infinite;
}
```

#### Page Transitions
```css
.fade-in {
  animation: fadeIn 0.4s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
```

#### Cart Badge Bounce
```css
.cart-badge-update {
  animation: bounce 0.5s var(--ease-bounce);
}

@keyframes bounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.3); }
}
```

---

## 9. Accessibility Standards

### Contrast Ratios (WCAG 2.1 AA Minimum)

| Combination | Ratio | Standard | Usage |
|-------------|-------|----------|-------|
| #1f2937 on #ffffff | 15.3:1 | AAA | Body text |
| #6b7280 on #ffffff | 7.1:1 | AAA | Secondary text |
| #ffffff on #667eea | 4.6:1 | AA | Button text |
| #667eea on #ffffff | 4.9:1 | AA | Links |

### Focus States
```css
*:focus-visible {
  outline: 3px solid #667eea;
  outline-offset: 2px;
}
```

### Screen Reader Support
- Semantic HTML5 elements
- ARIA labels on interactive elements
- Alt text for all images (descriptive, not decorative)
- Skip-to-content link

### Keyboard Navigation
- Tab order follows logical flow
- All interactive elements keyboard-accessible
- Escape key closes modals/dropdowns

---

## 10. Responsive Breakpoints

```css
/* Mobile First Approach */
--mobile: 320px;      /* Minimum support */
--mobile-lg: 480px;   /* Large phones */
--tablet: 768px;      /* Tablets */
--desktop: 1024px;    /* Small desktops */
--desktop-lg: 1280px; /* Standard desktops */
--desktop-xl: 1536px; /* Large screens */
```

### Layout Adjustments

#### Mobile (<768px)
- Single column product grid
- Stacked navigation (hamburger menu)
- Full-width cards
- Reduced padding (1rem vs 2rem)
- Font sizes reduced by 10-20%

#### Tablet (768px-1024px)
- 2-column product grid
- Horizontal navigation (if space permits)
- Reduced hero image height

#### Desktop (>1024px)
- 3-4 column product grid
- Full horizontal navigation
- Larger hero images
- Sidebar filters (if applicable)

---

## 11. Performance Considerations

### Image Optimisation
```html
<picture>
  <source srcset="product.webp" type="image/webp">
  <source srcset="product.jpg" type="image/jpeg">
  <img src="product.jpg" alt="Handcrafted silk scarf" loading="lazy">
</picture>
```

### CSS Strategy
- Critical CSS inlined (above-the-fold)
- Non-critical CSS loaded async
- CSS variables for theming (faster than JS)

### Font Loading
```css
@font-face {
  font-family: 'Playfair Display';
  font-display: swap; /* Prevents FOIT */
  src: url('/fonts/playfair.woff2') format('woff2');
}
```

---

## 12. Dark Mode Considerations

### Strategy
**Phase 1:** Not implemented (luxury brands typically favour light backgrounds)  
**Phase 2 (Future):** Optional dark theme for accessibility

### If Implemented:
```css
@media (prefers-color-scheme: dark) {
  --bg-primary: #1a1a1a;
  --text-primary: #e5e5e5;
  --card-bg: #2d2d2d;
  
  /* Adjust purple for dark backgrounds */
  --brand-primary: #8b9aef; /* Lighter purple */
}
```

**Rationale:** Dark mode can make luxury products appear less premium. Consider user toggle rather than auto-detection.

---

## 13. Implementation Phases

### Phase 1: Foundation (Current)
- ✅ Colour system implemented
- ✅ Typography system
- ✅ Basic component styling
- ✅ Responsive grid

### Phase 2: Enhancement (Next)
- Add custom serif font for luxury feel
- Implement advanced hover effects
- Add product image zoom
- Implement skeleton loading states
- Add micro-animations (cart badge, etc.)

### Phase 3: Advanced (Future)
- Product image galleries (multiple angles)
- 360° product views
- Video content integration
- Personalisation (saved colour preferences)
- Advanced filtering with smooth transitions

---

## 14. Recommended React UI Library Integration

### Top Choice: **Chakra UI**

#### Why Chakra UI?
1. **Style-through-props** - Rapid customisation
2. **Accessible by default** - WCAG compliant
3. **Built-in dark mode** - For future phases
4. **Themeable** - Easy to apply brand colours
5. **Composable** - Build complex UIs from primitives

#### Migration Strategy
```bash
npm install @chakra-ui/react @emotion/react @emotion/styled framer-motion
```

```jsx
import { ChakraProvider, extendTheme } from '@chakra-ui/react';

const theme = extendTheme({
  colors: {
    brand: {
      50: '#f5f3ff',
      100: '#ede9fe',
      200: '#ddd6fe',
      300: '#c4b5fd',
      400: '#a78bfa',
      500: '#667eea',  // Primary
      600: '#764ba2',  // Secondary
      700: '#6d28d9',
      800: '#5b21b6',
      900: '#4c1d95',
    },
  },
  fonts: {
    heading: `'Playfair Display', Georgia, serif`,
    body: `-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`,
  },
  components: {
    Button: {
      baseStyle: {
        fontWeight: '600',
        borderRadius: '8px',
      },
      variants: {
        solid: {
          bg: 'linear-gradient(135deg, brand.500 0%, brand.600 100%)',
          color: 'white',
          _hover: {
            transform: 'translateY(-2px)',
            boxShadow: 'lg',
          },
        },
      },
    },
  },
});
```

### Alternative: **ShadCN UI**
- More minimal
- Tailwind-based
- Copy components directly (not npm package)
- Better for full design control

---

## 15. Tools & Resources

### Design Tools
- **Figma:** For mockups and prototypes
- **Adobe Color:** Colour palette testing
- **Coolors:** Gradient generators
- **Contrast Checker:** WCAG compliance

### Development Tools
- **Chrome DevTools:** Responsive testing
- **Lighthouse:** Performance audits
- **axe DevTools:** Accessibility scanning
- **React DevTools:** Component inspection

### Cloudinary for Image Management
```javascript
// Automatic optimisation
const imageUrl = cloudinary.url('scarf-01.jpg', {
  width: 400,
  height: 300,
  crop: 'fill',
  quality: 'auto',
  fetch_format: 'auto', // WebP if supported
});
```

---

## 16. Brand Touch points

### Consistency Across Channels

| Touchpoint | Application |
|------------|-------------|
| Website | Primary implementation of all guidelines |
| Email | Purple header, white cards, same typography |
| Social Media | Purple brand colours, professional product photos |
| Packaging | Consider physical materials that echo digital elegance |
| Business Cards | Purple gradient accent, clean typography |

---

## 17. Success Metrics

### Aesthetic KPIs
- **Bounce Rate:** <40% (engaging design retains visitors)
- **Time on Site:** >2 minutes
- **Product Page Views:** >3 pages per session
- **Add to Cart Rate:** >5%
- **Lighthouse Performance Score:** >90
- **Lighthouse Accessibility Score:** 100

### A/B Testing Opportunities
- Button colour (purple vs. emerald for CTAs)
- Product card shadow depth
- Hero image style (lifestyle vs. product-focused)
- Typography (system fonts vs. custom serif)

---

## 18. Maintenance & Evolution

### Quarterly Reviews
- Analyse user feedback on design
- Review analytics (heatmaps, scroll depth)
- Test new design trends (cautiously)
- Audit accessibility compliance
- Performance benchmarking

### Design System Documentation
- Component library (Storybook recommended)
- Living style guide
- Version control for design tokens
- Designer-developer handoff process

---

## Conclusion

This aesthetic strategy positions the boutique scarf shop as a **premium, modern, and accessible** e-commerce platform. The purple-based colour system communicates luxury and creativity, whilst the clean typography and generous spacing ensure usability. All design decisions prioritise **user experience, accessibility, and brand consistency**.

**Next Steps:**
1. Review and approve colour palette
2. Select and implement typography (add custom serif)
3. Build component library (Chakra UI recommended)
4. Create high-quality product photography guidelines
5. Implement Phase 2 enhancements

---

**Document Version:** 1.0  
**Last Updated:** November 2, 2025  
**Project DNA:** ATGCATGC


## Executive Summary

This document defines the visual identity, design system, and aesthetic principles for the boutique scarf shop e-commerce platform. The strategy balances luxury positioning with accessibility, artisan authenticity with modern usability.

---

## 1. Brand Positioning

### Target Audience
- **Primary:** Affluent consumers (30-55 years) who value craftsmanship and unique design
- **Secondary:** Gift buyers seeking meaningful, high-quality items
- **Tertiary:** Conscious consumers prioritising handmade/ethical fashion

### Brand Personality
- **Elegant** yet approachable
- **Artisan** but not rustic
- **Premium** without being ostentatious
- **Modern** with timeless appeal

---

## 2. Colour Palette

### Primary Colours

#### Luxury Purple Gradient
- **Primary 1:** `#667eea` (Soft Periwinkle)
  - Usage: Headers, primary CTAs, brand accents
  - Psychology: Creativity, luxury, artisan craftsmanship
  
- **Primary 2:** `#764ba2` (Royal Purple)
  - Usage: Gradients, hover states, premium features
  - Psychology: Sophistication, exclusivity

**Rationale:** Purple has historically signified royalty and luxury. The gradient creates movement and visual interest whilst maintaining elegance.

### Neutral Foundation

#### Greys (Primary)
- **Dark:** `#1f2937` (Charcoal)
  - Usage: Primary text, footer, navigation
  - Contrast Ratio: 15.3:1 (WCAG AAA)

- **Medium:** `#6b7280` (Slate Grey)
  - Usage: Secondary text, descriptions, metadata
  - Contrast Ratio: 7.1:1 (WCAG AAA)

- **Light:** `#9ca3af` (Silver)
  - Usage: Placeholders, disabled states, hints
  - Contrast Ratio: 4.6:1 (WCAG AA)

- **Ultra-Light:** `#e5e7eb` (Platinum)
  - Usage: Borders, dividers, subtle backgrounds
  
- **Background:** `#f5f5f5` (Whisper)
  - Usage: Page background, card containers

#### Whites
- **Pure White:** `#ffffff`
  - Usage: Card backgrounds, modals, content areas

### Accent Colours

#### Success/Positive (Stock Available)
- **Primary:** `#059669` (Emerald)
  - Usage: In stock indicators, success messages
  
- **Light:** `#4ade80` (Mint)
  - Usage: Connected states, confirmations

#### Alert/Error
- **Danger:** `#dc2626` (Ruby)
  - Usage: Error messages, out of stock, critical alerts
  
- **Warning:** `#f59e0b` (Amber)
  - Usage: Low stock, pending actions

#### Information
- **Info:** `#3b82f6` (Azure)
  - Usage: Information badges, tooltips

### Metallic Accents (Future Enhancement)
- **Gold:** `#d4af37` - for premium/featured products
- **Rose Gold:** `#b76e79` - limited editions
- **Silver:** `#c0c0c0` - standard products

**Implementation Note:** Metallic gradients to be CSS-based for performance, not images.

---

## 3. Typography

### Font Stack

#### Primary (Body & UI)
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 
             'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 
             'Droid Sans', 'Helvetica Neue', sans-serif;
```
**Rationale:** System fonts ensure instant loading, native feel, and optimal readability across platforms.

#### Display/Headers (Optional Enhancement)
**Recommendation:** Add `'Playfair Display'` or `'Cormorant Garamond'` for luxury serif accents
```css
font-family: 'Playfair Display', Georgia, serif;
```
**Usage:** Hero headlines, product names, special announcements

#### Monospace (Code/Technical)
```css
font-family: 'Courier New', Consolas, Monaco, monospace;
```
**Usage:** Order numbers, API codes, technical information

### Type Scale

| Element | Size | Weight | Line Height | Usage |
|---------|------|--------|-------------|-------|
| H1 | 2.5rem (40px) | 700 | 1.2 | Hero headlines |
| H2 | 2rem (32px) | 600 | 1.3 | Section headers |
| H3 | 1.5rem (24px) | 600 | 1.4 | Subsections |
| H4 | 1.25rem (20px) | 600 | 1.4 | Card titles |
| Body Large | 1.125rem (18px) | 400 | 1.6 | Intro paragraphs |
| Body | 1rem (16px) | 400 | 1.6 | Standard text |
| Small | 0.875rem (14px) | 400 | 1.5 | Metadata, captions |
| Tiny | 0.75rem (12px) | 400 | 1.4 | Labels, legal |

### Responsive Adjustments
```css
@media (max-width: 768px) {
  H1: 1.8rem (28.8px)
  H2: 1.5rem (24px)
}
```

---

## 4. Spacing System

### Base Unit: 0.25rem (4px)

| Token | Value | Usage |
|-------|-------|-------|
| xs | 0.25rem (4px) | Tight spacing, icon padding |
| sm | 0.5rem (8px) | Element padding, small gaps |
| md | 1rem (16px) | Standard spacing |
| lg | 1.5rem (24px) | Section padding |
| xl | 2rem (32px) | Large section gaps |
| 2xl | 3rem (48px) | Hero sections |
| 3xl | 4rem (64px) | Major page divisions |

### Grid System
- **Max Content Width:** 1200px (prevents ultra-wide layouts)
- **Gutter:** 2rem (32px)
- **Columns:** 12-column flexible grid

---

## 5. Visual Elements

### Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| sm | 4px | Buttons, badges, small elements |
| md | 8px | Cards, inputs, standard UI |
| lg | 12px | Large cards, modals, images |
| xl | 16px | Hero sections, feature cards |
| full | 9999px | Pills, tags, circular elements |

**Brand Standard:** 12px for primary UI elements creates soft, approachable feel.

### Shadows

#### Elevation Scale
```css
/* Subtle (cards at rest) */
shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.06);

/* Standard (cards, dropdowns) */
shadow-md: 0 2px 8px rgba(0, 0, 0, 0.1);

/* Elevated (modals, hover states) */
shadow-lg: 0 4px 12px rgba(0, 0, 0, 0.15);

/* Dramatic (hero images, featured products) */
shadow-xl: 0 8px 24px rgba(0, 0, 0, 0.2);
```

**Hover Enhancement:**
```css
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.18);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Gradients

#### Primary Gradient (Brand)
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

#### Subtle Overlay (Hero Images)
```css
background: linear-gradient(
  to bottom, 
  rgba(102, 126, 234, 0.1) 0%, 
  rgba(118, 75, 162, 0.2) 100%
);
```

#### Shimmer Effect (Loading States)
```css
background: linear-gradient(
  90deg,
  rgba(255, 255, 255, 0) 0%,
  rgba(255, 255, 255, 0.6) 50%,
  rgba(255, 255, 255, 0) 100%
);
```

---

## 6. Component Aesthetics

### Product Cards

#### Structure
```
┌─────────────────────┐
│                     │
│   [Product Image]   │  ← 200px height, object-fit: cover
│                     │
├─────────────────────┤
│ Product Name        │  ← H4, 1rem padding
│ Brief description   │  ← Body Small, grey
├─────────────────────┤
│ £125.00  | In Stock │  ← Price (large, purple) | Status
└─────────────────────┘
```

#### Design Specs
- **Background:** Pure white (`#ffffff`)
- **Border Radius:** 12px
- **Shadow:** 0 2px 8px rgba(0, 0, 0, 0.1)
- **Hover:** Transform Y(-4px), enhanced shadow
- **Transition:** 0.3s ease-out
- **Image Aspect Ratio:** 4:3 (consistent across products)

### Buttons

#### Primary (Call-to-Action)
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
color: #ffffff;
padding: 0.75rem 2rem;
border-radius: 8px;
font-weight: 600;
box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
transition: all 0.2s ease;

&:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}
```

#### Secondary (Outline)
```css
background: transparent;
color: #667eea;
border: 2px solid #667eea;
padding: 0.75rem 2rem;
border-radius: 8px;

&:hover {
  background: rgba(102, 126, 234, 0.1);
}
```

#### Ghost/Tertiary
```css
background: transparent;
color: #6b7280;
padding: 0.75rem 1.5rem;

&:hover {
  color: #667eea;
  background: rgba(102, 126, 234, 0.05);
}
```

### Forms & Inputs

```css
input, textarea, select {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  transition: border-color 0.2s;
  
  &:focus {
    border-color: #667eea;
    outline: none;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
  
  &:disabled {
    background: #f5f5f5;
    color: #9ca3af;
    cursor: not-allowed;
  }
}
```

### Navigation

#### Header
- **Background:** White with subtle shadow
- **Height:** 80px
- **Sticky:** Yes (position: sticky, top: 0, z-index: 50)
- **Logo:** Left-aligned, 40px height
- **Cart Icon:** Badge with count (purple circle)

#### Mobile Menu
- **Activation:** Hamburger icon (3 lines, 20px width)
- **Transition:** Slide from right
- **Overlay:** rgba(0, 0, 0, 0.5)

---

## 7. Photography & Imagery

### Product Photography Guidelines

#### Technical Specs
- **Resolution:** Minimum 1200x900px (retina-ready)
- **Format:** WebP (primary), JPEG (fallback)
- **Aspect Ratio:** 4:3 (consistent across site)
- **Background:** Pure white (#ffffff) or lifestyle context
- **Lighting:** Soft, diffused, natural-looking

#### Style Guide
- **Angles:** 3/4 view showing texture and drape
- **Context:** Styled on mannequin or model (not flat lay)
- **Detail Shots:** Close-ups showing fabric texture, stitching, patterns
- **Lifestyle:** Worn in natural settings (30% of images)

#### Image Treatment
```css
.product-image {
  object-fit: cover;
  filter: brightness(1.05) contrast(1.02) saturate(1.1);
  transition: transform 0.3s;
}

.product-card:hover .product-image {
  transform: scale(1.05);
}
```

### Hero Images
- **Size:** 1920x800px (2.4:1 ratio)
- **Overlay:** Linear gradient (subtle purple tint)
- **Text:** Large, white, left-aligned with ample padding
- **CTA:** Prominent button (primary style)

### Icons
- **Style:** Outline (not filled) for clean, modern look
- **Stroke Width:** 2px
- **Source:** [Heroicons](https://heroicons.com/) or [Feather Icons](https://feathericons.com/)
- **Size:** 20px (standard), 24px (larger contexts)
- **Colour:** Inherit from context or purple brand colour

---

## 8. Animation & Micro-interactions

### Timing Functions

```css
/* Standard easing */
--ease-out: cubic-bezier(0.4, 0, 0.2, 1);

/* Bounce effect */
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);

/* Smooth */
--ease-smooth: cubic-bezier(0.25, 0.46, 0.45, 0.94);
```

### Key Animations

#### Hover States
```css
/* Card lift */
transform: translateY(-4px);
transition: transform 0.3s var(--ease-out);

/* Button press */
transform: scale(0.98);
transition: transform 0.1s;
```

#### Loading States
```css
@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.loading {
  background: linear-gradient(90deg, 
    rgba(255,255,255,0) 0%, 
    rgba(255,255,255,0.6) 50%, 
    rgba(255,255,255,0) 100%);
  animation: shimmer 1.5s infinite;
}
```

#### Page Transitions
```css
.fade-in {
  animation: fadeIn 0.4s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
```

#### Cart Badge Bounce
```css
.cart-badge-update {
  animation: bounce 0.5s var(--ease-bounce);
}

@keyframes bounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.3); }
}
```

---

## 9. Accessibility Standards

### Contrast Ratios (WCAG 2.1 AA Minimum)

| Combination | Ratio | Standard | Usage |
|-------------|-------|----------|-------|
| #1f2937 on #ffffff | 15.3:1 | AAA | Body text |
| #6b7280 on #ffffff | 7.1:1 | AAA | Secondary text |
| #ffffff on #667eea | 4.6:1 | AA | Button text |
| #667eea on #ffffff | 4.9:1 | AA | Links |

### Focus States
```css
*:focus-visible {
  outline: 3px solid #667eea;
  outline-offset: 2px;
}
```

### Screen Reader Support
- Semantic HTML5 elements
- ARIA labels on interactive elements
- Alt text for all images (descriptive, not decorative)
- Skip-to-content link

### Keyboard Navigation
- Tab order follows logical flow
- All interactive elements keyboard-accessible
- Escape key closes modals/dropdowns

---

## 10. Responsive Breakpoints

```css
/* Mobile First Approach */
--mobile: 320px;      /* Minimum support */
--mobile-lg: 480px;   /* Large phones */
--tablet: 768px;      /* Tablets */
--desktop: 1024px;    /* Small desktops */
--desktop-lg: 1280px; /* Standard desktops */
--desktop-xl: 1536px; /* Large screens */
```

### Layout Adjustments

#### Mobile (<768px)
- Single column product grid
- Stacked navigation (hamburger menu)
- Full-width cards
- Reduced padding (1rem vs 2rem)
- Font sizes reduced by 10-20%

#### Tablet (768px-1024px)
- 2-column product grid
- Horizontal navigation (if space permits)
- Reduced hero image height

#### Desktop (>1024px)
- 3-4 column product grid
- Full horizontal navigation
- Larger hero images
- Sidebar filters (if applicable)

---

## 11. Performance Considerations

### Image Optimisation
```html
<picture>
  <source srcset="product.webp" type="image/webp">
  <source srcset="product.jpg" type="image/jpeg">
  <img src="product.jpg" alt="Handcrafted silk scarf" loading="lazy">
</picture>
```

### CSS Strategy
- Critical CSS inlined (above-the-fold)
- Non-critical CSS loaded async
- CSS variables for theming (faster than JS)

### Font Loading
```css
@font-face {
  font-family: 'Playfair Display';
  font-display: swap; /* Prevents FOIT */
  src: url('/fonts/playfair.woff2') format('woff2');
}
```

---

## 12. Dark Mode Considerations

### Strategy
**Phase 1:** Not implemented (luxury brands typically favour light backgrounds)  
**Phase 2 (Future):** Optional dark theme for accessibility

### If Implemented:
```css
@media (prefers-color-scheme: dark) {
  --bg-primary: #1a1a1a;
  --text-primary: #e5e5e5;
  --card-bg: #2d2d2d;
  
  /* Adjust purple for dark backgrounds */
  --brand-primary: #8b9aef; /* Lighter purple */
}
```

**Rationale:** Dark mode can make luxury products appear less premium. Consider user toggle rather than auto-detection.

---

## 13. Implementation Phases

### Phase 1: Foundation (Current)
- ✅ Colour system implemented
- ✅ Typography system
- ✅ Basic component styling
- ✅ Responsive grid

### Phase 2: Enhancement (Next)
- Add custom serif font for luxury feel
- Implement advanced hover effects
- Add product image zoom
- Implement skeleton loading states
- Add micro-animations (cart badge, etc.)

### Phase 3: Advanced (Future)
- Product image galleries (multiple angles)
- 360° product views
- Video content integration
- Personalisation (saved colour preferences)
- Advanced filtering with smooth transitions

---

## 14. Recommended React UI Library Integration

### Top Choice: **Chakra UI**

#### Why Chakra UI?
1. **Style-through-props** - Rapid customisation
2. **Accessible by default** - WCAG compliant
3. **Built-in dark mode** - For future phases
4. **Themeable** - Easy to apply brand colours
5. **Composable** - Build complex UIs from primitives

#### Migration Strategy
```bash
npm install @chakra-ui/react @emotion/react @emotion/styled framer-motion
```

```jsx
import { ChakraProvider, extendTheme } from '@chakra-ui/react';

const theme = extendTheme({
  colors: {
    brand: {
      50: '#f5f3ff',
      100: '#ede9fe',
      200: '#ddd6fe',
      300: '#c4b5fd',
      400: '#a78bfa',
      500: '#667eea',  // Primary
      600: '#764ba2',  // Secondary
      700: '#6d28d9',
      800: '#5b21b6',
      900: '#4c1d95',
    },
  },
  fonts: {
    heading: `'Playfair Display', Georgia, serif`,
    body: `-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`,
  },
  components: {
    Button: {
      baseStyle: {
        fontWeight: '600',
        borderRadius: '8px',
      },
      variants: {
        solid: {
          bg: 'linear-gradient(135deg, brand.500 0%, brand.600 100%)',
          color: 'white',
          _hover: {
            transform: 'translateY(-2px)',
            boxShadow: 'lg',
          },
        },
      },
    },
  },
});
```

### Alternative: **ShadCN UI**
- More minimal
- Tailwind-based
- Copy components directly (not npm package)
- Better for full design control

---

## 15. Tools & Resources

### Design Tools
- **Figma:** For mockups and prototypes
- **Adobe Color:** Colour palette testing
- **Coolors:** Gradient generators
- **Contrast Checker:** WCAG compliance

### Development Tools
- **Chrome DevTools:** Responsive testing
- **Lighthouse:** Performance audits
- **axe DevTools:** Accessibility scanning
- **React DevTools:** Component inspection

### Cloudinary for Image Management
```javascript
// Automatic optimisation
const imageUrl = cloudinary.url('scarf-01.jpg', {
  width: 400,
  height: 300,
  crop: 'fill',
  quality: 'auto',
  fetch_format: 'auto', // WebP if supported
});
```

---

## 16. Brand Touch points

### Consistency Across Channels

| Touchpoint | Application |
|------------|-------------|
| Website | Primary implementation of all guidelines |
| Email | Purple header, white cards, same typography |
| Social Media | Purple brand colours, professional product photos |
| Packaging | Consider physical materials that echo digital elegance |
| Business Cards | Purple gradient accent, clean typography |

---

## 17. Success Metrics

### Aesthetic KPIs
- **Bounce Rate:** <40% (engaging design retains visitors)
- **Time on Site:** >2 minutes
- **Product Page Views:** >3 pages per session
- **Add to Cart Rate:** >5%
- **Lighthouse Performance Score:** >90
- **Lighthouse Accessibility Score:** 100

### A/B Testing Opportunities
- Button colour (purple vs. emerald for CTAs)
- Product card shadow depth
- Hero image style (lifestyle vs. product-focused)
- Typography (system fonts vs. custom serif)

---

## 18. Maintenance & Evolution

### Quarterly Reviews
- Analyse user feedback on design
- Review analytics (heatmaps, scroll depth)
- Test new design trends (cautiously)
- Audit accessibility compliance
- Performance benchmarking

### Design System Documentation
- Component library (Storybook recommended)
- Living style guide
- Version control for design tokens
- Designer-developer handoff process

---

## Conclusion

This aesthetic strategy positions the boutique scarf shop as a **premium, modern, and accessible** e-commerce platform. The purple-based colour system communicates luxury and creativity, whilst the clean typography and generous spacing ensure usability. All design decisions prioritise **user experience, accessibility, and brand consistency**.

**Next Steps:**
1. Review and approve colour palette
2. Select and implement typography (add custom serif)
3. Build component library (Chakra UI recommended)
4. Create high-quality product photography guidelines
5. Implement Phase 2 enhancements

---

**Document Version:** 1.0  
**Last Updated:** November 2, 2025  
**Project DNA:** ATGCATGC





