// Gemini Pro 2.5 API Integration

const GEMINI_API_KEY = import.meta.env.VITE_GEMINI_API_KEY;
const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent';

export interface GeminiRequest {
  prompt: string;
  maxTokens?: number;
  temperature?: number;
}

export interface GeminiResponse {
  text: string;
  success: boolean;
  error?: string;
}

export async function generateWithGemini(request: GeminiRequest): Promise<GeminiResponse> {
  if (!GEMINI_API_KEY) {
    return {
      text: '',
      success: false,
      error: 'Gemini API key not configured. Please add VITE_GEMINI_API_KEY to your .env file.',
    };
  }

  try {
    const response = await fetch(`${GEMINI_API_URL}?key=${GEMINI_API_KEY}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        contents: [
          {
            parts: [
              {
                text: request.prompt,
              },
            ],
          },
        ],
        generationConfig: {
          temperature: request.temperature || 0.9,
          maxOutputTokens: request.maxTokens || 2048,
        },
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error?.message || 'API request failed');
    }

    const data = await response.json();
    const text = data.candidates?.[0]?.content?.parts?.[0]?.text || '';

    return {
      text,
      success: true,
    };
  } catch (error) {
    console.error('Gemini API error:', error);
    return {
      text: '',
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error occurred',
    };
  }
}

export async function generateIdeas(context: string, existingIdeas: string[]): Promise<string[]> {
  const prompt = `You are an innovation consultant helping a team brainstorm creative solutions.

Context and Problem Space:
${context}

Existing Ideas:
${existingIdeas.length > 0 ? existingIdeas.map((idea, i) => `${i + 1}. ${idea}`).join('\n') : 'None yet'}

Task: Generate 5 new, creative, and diverse ideas that:
1. Are different from the existing ideas
2. Address the problem space in innovative ways
3. Range from practical to ambitious
4. Are specific and actionable

Output format: Return ONLY the 5 ideas, one per line, without numbering or additional text.`;

  const response = await generateWithGemini({ prompt, temperature: 0.9 });

  if (!response.success) {
    throw new Error(response.error || 'Failed to generate ideas');
  }

  // Parse the response into individual ideas
  const ideas = response.text
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line.length > 0)
    .slice(0, 5); // Take first 5 ideas

  return ideas;
}

export async function clusterIdeas(ideas: string[]): Promise<{ clusters: Array<{ name: string; ideas: string[] }> }> {
  const prompt = `You are an innovation consultant analyzing brainstormed ideas to identify patterns and themes.

Ideas to cluster:
${ideas.map((idea, i) => `${i + 1}. ${idea}`).join('\n')}

Task: Group these ideas into 2-4 logical clusters based on themes, approaches, or problem areas.

Output format (JSON):
{
  "clusters": [
    {
      "name": "Cluster name describing the theme",
      "ideas": ["idea 1", "idea 2"]
    }
  ]
}

Return ONLY valid JSON, no additional text.`;

  const response = await generateWithGemini({ prompt, temperature: 0.7 });

  if (!response.success) {
    throw new Error(response.error || 'Failed to cluster ideas');
  }

  try {
    // Try to extract JSON from response
    const jsonMatch = response.text.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error('No JSON found in response');
    }
    
    const parsed = JSON.parse(jsonMatch[0]);
    return parsed;
  } catch (error) {
    console.error('Failed to parse clustering response:', error);
    throw new Error('Failed to parse AI response');
  }
}

export async function synthesizeIdeas(ideas: string[]): Promise<string> {
  const prompt = `You are an innovation consultant creating a synthesis of brainstormed ideas.

Ideas:
${ideas.map((idea, i) => `${i + 1}. ${idea}`).join('\n')}

Task: Create a concise synthesis that:
1. Identifies key themes and patterns across all ideas
2. Highlights the most promising directions
3. Suggests how ideas might be combined or refined
4. Provides actionable next steps

Keep it concise (max 200 words) and practical.`;

  const response = await generateWithGemini({ prompt, temperature: 0.7, maxTokens: 1024 });

  if (!response.success) {
    throw new Error(response.error || 'Failed to synthesize ideas');
  }

  return response.text;
}


