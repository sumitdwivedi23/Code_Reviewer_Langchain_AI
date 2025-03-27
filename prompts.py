# Analyze code for style, bugs, and optimization
ANALYZE_PROMPT = """
You are an expert code reviewer. Here’s the code from {filename} to analyze for style, bugs, and optimization:
Provide a detailed breakdown in markdown:
1. Style issues (e.g., naming, readability)
2. Potential bugs or errors
3. Optimization suggestions
"""

# Suggest specific improvements
IMPROVE_PROMPT = """
Based on this analysis:
{analysis}
Suggest specific improvements for the code snippet:" \
"Provide:
1. Rewritten code snippets where applicable
2. Explanations for each change
Return your suggestions in markdown format.
"""

# Generate a professional review report
REPORT_PROMPT = """
Compile a professional peer review report based on:
- Original code:" \
"- Analysis:
{analysis}
- Improvements:
{improvements}
Format the report in markdown with sections:
1. Summary
2. Detailed Feedback
3. Revised Code
4. Conclusion
"""