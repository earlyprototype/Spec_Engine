/**
 * Gemini AI Service for Define Stage
 * Handles AI synthesis for problem framing, HMW statements, and stakeholder analysis
 */

interface HMWStatement {
  id: string;
  statement: string;
  priority: 'high' | 'medium' | 'low';
}

interface Stakeholder {
  id: string;
  name: string;
  role: string;
  influence: 'high' | 'medium' | 'low';
  interest: 'high' | 'medium' | 'low';
  needs: string;
}

export interface DefineData {
  hmwStatements: HMWStatement[];
  stakeholders: Stakeholder[];
  constraints: string;
  opportunities: string;
  problemContext: string;
}

export interface DefineSynthesisResult {
  refinedProblemStatement: string;
  alternativeFramings: string[];
  prioritizedHMWs: string[];
  stakeholderInsights: string[];
  keyConstraints: string[];
  opportunities: string[];
  recommendations: string[];
}

/**
 * Generates AI synthesis of Define stage data using Gemini API
 */
export async function generateDefineSynthesis(data: DefineData): Promise<DefineSynthesisResult> {
  const apiKey = import.meta.env.VITE_GEMINI_API_KEY;
  
  if (!apiKey) {
    throw new Error('Gemini API key not configured. Please add VITE_GEMINI_API_KEY to your .env file.');
  }

  // Build comprehensive prompt from define data
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
 * Builds a comprehensive prompt for Gemini based on Define stage data
 */
function buildSynthesisPrompt(data: DefineData): string {
  let prompt = `You are an expert innovation consultant helping to synthesise problem framing and stakeholder analysis for a Design Thinking project in the Define stage.

Your task is to analyse the problem framing work and provide insights to help the team move forward with a clear, well-defined problem statement.

## PROBLEM CONTEXT

${data.problemContext || 'No problem context provided yet.'}

## HOW MIGHT WE (HMW) STATEMENTS (${data.hmwStatements.length} total)

`;

  if (data.hmwStatements.length > 0) {
    data.hmwStatements.forEach((hmw, index) => {
      prompt += `${index + 1}. ${hmw.statement} [Priority: ${hmw.priority}]\n`;
    });
  } else {
    prompt += 'No HMW statements created yet.\n';
  }

  prompt += `\n## STAKEHOLDER ANALYSIS (${data.stakeholders.length} total)

`;

  if (data.stakeholders.length > 0) {
    data.stakeholders.forEach((stakeholder, index) => {
      prompt += `
Stakeholder ${index + 1}: ${stakeholder.name}
- Role: ${stakeholder.role || 'Not specified'}
- Influence: ${stakeholder.influence}
- Interest: ${stakeholder.interest}
- Key Needs: ${stakeholder.needs || 'Not specified'}
`;
    });
  } else {
    prompt += 'No stakeholders identified yet.\n';
  }

  prompt += `\n## CONSTRAINTS & LIMITATIONS

${data.constraints || 'No constraints documented yet.'}

## OPPORTUNITIES & ASSETS

${data.opportunities || 'No opportunities documented yet.'}

---

Please provide a comprehensive synthesis in the following structured format:

## REFINED PROBLEM STATEMENT
[Provide a clear, concise problem statement (2-3 sentences) that synthesises the context, HMW statements, and stakeholder insights into a focused innovation challenge]

## ALTERNATIVE PROBLEM FRAMINGS
[List 3-4 alternative ways to frame this problem that might open up different solution spaces]

## PRIORITIZED HMW STATEMENTS
[List the 3-5 most impactful HMW statements from those provided, explaining why they're most valuable]

## STAKEHOLDER INSIGHTS
[List 3-5 key insights about stakeholder needs, power dynamics, or alignment opportunities]

## KEY CONSTRAINTS
[List 3-4 most critical constraints that must be addressed in the solution]

## KEY OPPORTUNITIES
[List 3-4 most promising opportunities or assets to leverage]

## RECOMMENDATIONS FOR IDEATION
[Provide 3-5 specific recommendations for the upcoming Ideate stage based on this problem framing]

Be specific, actionable, and grounded in the data provided. If data is limited, acknowledge this and provide recommendations to strengthen the problem definition. Focus on clarity and actionability.`;

  return prompt;
}

/**
 * Parses Gemini's response into structured format
 */
function parseGeminiResponse(text: string): DefineSynthesisResult {
  // Extract sections using regex patterns
  const problemStatementMatch = text.match(/##\s*REFINED PROBLEM STATEMENT\s*([\s\S]*?)(?=##|$)/i);
  const alternativeFramingsMatch = text.match(/##\s*ALTERNATIVE PROBLEM FRAMINGS\s*([\s\S]*?)(?=##|$)/i);
  const prioritizedHMWsMatch = text.match(/##\s*PRIORITIZED HMW STATEMENTS\s*([\s\S]*?)(?=##|$)/i);
  const stakeholderInsightsMatch = text.match(/##\s*STAKEHOLDER INSIGHTS\s*([\s\S]*?)(?=##|$)/i);
  const constraintsMatch = text.match(/##\s*KEY CONSTRAINTS\s*([\s\S]*?)(?=##|$)/i);
  const opportunitiesMatch = text.match(/##\s*KEY OPPORTUNITIES\s*([\s\S]*?)(?=##|$)/i);
  const recommendationsMatch = text.match(/##\s*RECOMMENDATIONS FOR IDEATION\s*([\s\S]*?)(?=##|$)/i);

  // Helper to extract bullet points from text
  const extractBulletPoints = (text: string): string[] => {
    const lines = text.split('\n')
      .map(line => line.trim())
      .filter(line => line.length > 0)
      .filter(line => line.match(/^[-*•\d.]/));
    
    return lines.map(line => line.replace(/^[-*•\d.]\s*/, '').trim());
  };

  // Helper to extract paragraph text (non-bullet points)
  const extractParagraph = (text: string): string => {
    return text.split('\n')
      .map(line => line.trim())
      .filter(line => line.length > 0 && !line.match(/^[-*•\d.]/))
      .join(' ')
      .trim();
  };

  return {
    refinedProblemStatement: problemStatementMatch ? extractParagraph(problemStatementMatch[1]) : 'Problem statement not available',
    alternativeFramings: alternativeFramingsMatch ? extractBulletPoints(alternativeFramingsMatch[1]) : [],
    prioritizedHMWs: prioritizedHMWsMatch ? extractBulletPoints(prioritizedHMWsMatch[1]) : [],
    stakeholderInsights: stakeholderInsightsMatch ? extractBulletPoints(stakeholderInsightsMatch[1]) : [],
    keyConstraints: constraintsMatch ? extractBulletPoints(constraintsMatch[1]) : [],
    opportunities: opportunitiesMatch ? extractBulletPoints(opportunitiesMatch[1]) : [],
    recommendations: recommendationsMatch ? extractBulletPoints(recommendationsMatch[1]) : [],
  };
}


