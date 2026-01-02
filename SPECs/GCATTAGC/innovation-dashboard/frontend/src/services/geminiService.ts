/**
 * Gemini AI Service
 * Handles AI synthesis for Discovery stage data using Google Gemini 2.5 Pro
 */

interface DiscoveryData {
  userResearch: {
    interviews: Array<{
      participantName: string;
      date: string;
      notes: string;
    }>;
    surveys: Array<{
      title: string;
      responses: string;
      insights: string;
    }>;
    demographics: string;
  };
  observations: {
    fieldNotes: Array<{
      date: string;
      context: string;
      observation: string;
    }>;
    contextualFindings: string;
  };
  insights: {
    patterns: string[];
    themes: string[];
    opportunities: string[];
    challenges: string[];
  };
}

export interface SynthesisResult {
  summary: string;
  keyInsights: string[];
  userNeeds: string[];
  recommendations: string[];
  problemAreas: string[];
}

/**
 * Generates AI synthesis of discovery data using Gemini API
 */
export async function generateDiscoverySynthesis(data: DiscoveryData): Promise<SynthesisResult> {
  const apiKey = import.meta.env.VITE_GEMINI_API_KEY;
  
  if (!apiKey) {
    throw new Error('Gemini API key not configured. Please add VITE_GEMINI_API_KEY to your .env file.');
  }

  // Build comprehensive prompt from discovery data
  const prompt = buildSynthesisPrompt(data);

  try {
    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=${apiKey}`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          contents: [
            {
              parts: [
                {
                  text: prompt,
                },
              ],
            },
          ],
          generationConfig: {
            temperature: 0.7,
            topK: 40,
            topP: 0.95,
            maxOutputTokens: 2048,
          },
        }),
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Gemini API error:', errorData);
      throw new Error(`Gemini API error: ${response.status} ${response.statusText}`);
    }

    const result = await response.json();
    const generatedText = result.candidates?.[0]?.content?.parts?.[0]?.text;

    if (!generatedText) {
      throw new Error('No content generated from Gemini API');
    }

    // Parse the structured response
    return parseGeminiResponse(generatedText);
  } catch (error) {
    console.error('Error calling Gemini API:', error);
    throw error;
  }
}

/**
 * Builds a comprehensive prompt for Gemini based on discovery data
 */
function buildSynthesisPrompt(data: DiscoveryData): string {
  let prompt = `You are an expert innovation consultant helping to synthesise discovery research for a Design Thinking project.

Please analyse the following discovery data and provide a comprehensive synthesis:

## USER RESEARCH

### Interviews (${data.userResearch.interviews.length} total):
`;

  if (data.userResearch.interviews.length > 0) {
    data.userResearch.interviews.forEach((interview, index) => {
      prompt += `
Interview ${index + 1}:
- Participant: ${interview.participantName || 'Anonymous'}
- Date: ${interview.date}
- Notes: ${interview.notes || 'No notes provided'}
`;
    });
  } else {
    prompt += '\nNo interviews conducted yet.\n';
  }

  prompt += `\n### Surveys (${data.userResearch.surveys.length} total):
`;

  if (data.userResearch.surveys.length > 0) {
    data.userResearch.surveys.forEach((survey, index) => {
      prompt += `
Survey ${index + 1}: ${survey.title || 'Untitled'}
- Responses: ${survey.responses || 'No responses provided'}
- Insights: ${survey.insights || 'No insights provided'}
`;
    });
  } else {
    prompt += '\nNo surveys conducted yet.\n';
  }

  prompt += `\n### User Demographics:
${data.userResearch.demographics || 'No demographic information provided'}

## OBSERVATIONS

### Field Notes (${data.observations.fieldNotes.length} total):
`;

  if (data.observations.fieldNotes.length > 0) {
    data.observations.fieldNotes.forEach((note, index) => {
      prompt += `
Note ${index + 1}:
- Date: ${note.date}
- Context: ${note.context || 'Not specified'}
- Observation: ${note.observation || 'No observation provided'}
`;
    });
  } else {
    prompt += '\nNo field notes recorded yet.\n';
  }

  prompt += `\n### Contextual Findings:
${data.observations.contextualFindings || 'No contextual findings provided'}

## INITIAL INSIGHTS

### Patterns Identified:
${data.insights.patterns.length > 0 ? data.insights.patterns.map((p, i) => `${i + 1}. ${p}`).join('\n') : 'No patterns identified yet'}

### Themes:
${data.insights.themes.length > 0 ? data.insights.themes.map((t, i) => `${i + 1}. ${t}`).join('\n') : 'No themes identified yet'}

### Opportunities:
${data.insights.opportunities.length > 0 ? data.insights.opportunities.map((o, i) => `${i + 1}. ${o}`).join('\n') : 'No opportunities identified yet'}

### Challenges:
${data.insights.challenges.length > 0 ? data.insights.challenges.map((c, i) => `${i + 1}. ${c}`).join('\n') : 'No challenges identified yet'}

---

Please provide a synthesis in the following structured format:

## EXECUTIVE SUMMARY
[2-3 paragraph summary of key findings]

## KEY INSIGHTS
[List 5-7 most important insights discovered, each as a separate bullet point]

## USER NEEDS
[List 4-6 core user needs identified from the research]

## RECOMMENDATIONS
[List 3-5 actionable recommendations for the Define stage]

## PROBLEM AREAS TO EXPLORE
[List 3-4 specific problem areas that should be addressed in the Define stage]

Please be specific, actionable, and grounded in the data provided. If data is limited, acknowledge this and provide recommendations based on what is available.`;

  return prompt;
}

/**
 * Parses Gemini's response into structured format
 */
function parseGeminiResponse(text: string): SynthesisResult {
  // Extract sections using regex patterns
  const summaryMatch = text.match(/##\s*EXECUTIVE SUMMARY\s*([\s\S]*?)(?=##|$)/i);
  const insightsMatch = text.match(/##\s*KEY INSIGHTS\s*([\s\S]*?)(?=##|$)/i);
  const needsMatch = text.match(/##\s*USER NEEDS\s*([\s\S]*?)(?=##|$)/i);
  const recommendationsMatch = text.match(/##\s*RECOMMENDATIONS\s*([\s\S]*?)(?=##|$)/i);
  const problemAreasMatch = text.match(/##\s*PROBLEM AREAS TO EXPLORE\s*([\s\S]*?)(?=##|$)/i);

  // Helper to extract bullet points from text
  const extractBulletPoints = (text: string): string[] => {
    const lines = text.split('\n')
      .map(line => line.trim())
      .filter(line => line.length > 0)
      .filter(line => line.match(/^[-*•\d.]/));
    
    return lines.map(line => line.replace(/^[-*•\d.]\s*/, '').trim());
  };

  return {
    summary: summaryMatch?.[1]?.trim() || 'Summary not available',
    keyInsights: insightsMatch ? extractBulletPoints(insightsMatch[1]) : [],
    userNeeds: needsMatch ? extractBulletPoints(needsMatch[1]) : [],
    recommendations: recommendationsMatch ? extractBulletPoints(recommendationsMatch[1]) : [],
    problemAreas: problemAreasMatch ? extractBulletPoints(problemAreasMatch[1]) : [],
  };
}

