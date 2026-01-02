# Discovery Stage Module - User Guide

**SPEClet 1: Discovery Stage Module**  
**Status:** Completed  
**Date:** 2025-11-03

---

## Overview

The Discovery Stage Module provides comprehensive tools for innovation consultants to guide clients through the discovery phase of Design Thinking. It includes data collection, synthesis, and AI-powered insights generation.

---

## Features

### 1. User Research Collection
- **Interviews**: Record participant interviews with notes and key quotes
- **Surveys**: Document survey responses and insights
- **Demographics**: Capture target user characteristics

### 2. Observations
- **Field Notes**: Log contextual observations from user environments
- **Contextual Findings**: Document environmental and social factors

### 3. Insights Capture
- **Patterns**: Identify recurring behaviours and trends
- **Themes**: Capture overarching themes from research
- **Opportunities**: Document potential innovation opportunities
- **Challenges**: Record pain points and obstacles

### 4. AI-Powered Synthesis
- Analyses all discovery data using Gemini 2.5 Pro
- Generates executive summary
- Identifies key insights and user needs
- Provides recommendations for Define stage
- Highlights problem areas to explore

### 5. Progress Dashboard
- Real-time completion tracking
- Auto-save functionality (saves every 2 seconds)
- Suggested next actions
- Visual progress indicators

---

## Setup Requirements

### Environment Variables

Add to your `.env` file:

```env
VITE_GEMINI_API_KEY=your-gemini-api-key
```

Get your Gemini API key from: https://aistudio.google.com/app/apikey

### Dependencies

Already included in the platform:
- React 18+
- TypeScript
- Tailwind CSS
- Supabase client

---

## Usage Guide

### Getting Started

1. **Navigate to Discovery Stage**: From the project dashboard, select a project and click on the "Discovery" tab

2. **Complete Data Collection**:
   - Start with User Research tab
   - Add interviews and surveys
   - Document user demographics

3. **Record Observations**:
   - Switch to Observations tab
   - Add field notes from user contexts
   - Document contextual findings

4. **Capture Insights**:
   - Move to Insights tab
   - Identify patterns and themes
   - Note opportunities and challenges

5. **Generate AI Synthesis**:
   - Once 30%+ complete, use the Synthesis tab
   - Click "Generate AI Synthesis"
   - Review and refine the AI-generated insights

### Best Practices

**Interviews**:
- Use descriptive participant names (e.g., "User A", "Manager - Tech Company")
- Record rich, detailed notes
- Focus on behaviours, not just opinions

**Observations**:
- Include specific context (location, time, environment)
- Note what you see, not what you interpret
- Capture unexpected behaviours

**Insights**:
- Look for patterns across multiple data points
- Be specific and actionable
- Connect insights to user needs

**AI Synthesis**:
- Complete at least 30% of discovery activities for meaningful synthesis
- Review and refine AI-generated insights with your expertise
- Use synthesis to inform Define stage problem framing

---

## Data Storage

All discovery data is stored in the `stage_data` table with:
- **Project ID**: Links to specific project
- **Stage Name**: "discovery"
- **Data JSON**: Structured discovery data

Data structure:
```typescript
{
  userResearch: {
    interviews: [...],
    surveys: [...],
    demographics: "..."
  },
  observations: {
    fieldNotes: [...],
    contextualFindings: "..."
  },
  insights: {
    patterns: [...],
    themes: [...],
    opportunities: [...],
    challenges: [...]
  },
  synthesis: {
    aiGenerated: "...",
    userRefined: "...",
    timestamp: "..."
  }
}
```

---

## Keyboard Shortcuts

- **Auto-save**: Automatic every 2 seconds
- **Tab Navigation**: Use tabs to switch between sections
- **Add Items**: Click "+ Add" buttons in each section

---

## Troubleshooting

### AI Synthesis Not Working

**Issue**: "Error generating synthesis" message

**Solutions**:
1. Check that `VITE_GEMINI_API_KEY` is set in `.env` file
2. Verify your Gemini API key is valid
3. Ensure you have completed at least 30% of discovery activities
4. Check browser console for detailed error messages

### Data Not Saving

**Issue**: Changes not persisting between sessions

**Solutions**:
1. Check that Supabase is configured correctly
2. Verify Row Level Security policies are set up
3. Check browser console for API errors
4. Ensure you're logged in with valid credentials

### Progress Not Updating

**Issue**: Completion percentage stuck

**Solutions**:
1. Add substantial content (at least 50 characters in notes)
2. Complete items in multiple sections
3. Refresh the page if progress seems frozen

---

## Mobile Responsiveness

The Discovery module is fully responsive and works on:
- Desktop browsers (Chrome, Firefox, Safari, Edge)
- Tablets (iPad, Android tablets)
- Mobile phones (iOS, Android)

Forms adapt to smaller screens with stacked layouts.

---

## Next Steps

After completing discovery:
1. Review your synthesis
2. Identify 2-3 core problem areas
3. Move to the **Define stage** to frame the problem
4. Use discovery insights to inform problem definition

---

## Technical Details

### Component Location
`frontend/src/pages/DiscoveryView.tsx`

### Service Location
`frontend/src/services/geminiService.ts`

### Route
`/project/:projectId/discovery`

### API Integration
- Gemini 2.5 Pro via Google AI API
- Supabase for data persistence
- Auto-save with 2-second debounce

---

## Support

For issues or questions:
1. Check the browser console for error messages
2. Verify all environment variables are set
3. Ensure Supabase database schema is correctly configured
4. Review the `INSFORGE_SETUP.md` for backend configuration

---

**Module Status**: Production Ready  
**Last Updated**: 2025-11-03  
**SPEClet ID**: 1

