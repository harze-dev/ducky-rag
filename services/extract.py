import json
import re
from typing import Optional, Tuple


def extract_json_response(response: str, return_response_on_failure: bool = True) -> Tuple[Optional[str], str]:
    """
    Extract JSON from LLM response and return (modified_code, explanation).

    Args:
        response: Raw LLM response containing JSON
        return_response_on_failure: If True, return raw response as explanation on parse failure

    Returns:
        Tuple of (modified_code, explanation)
    """
    try:
        # Clean the response - remove any markdown formatting
        cleaned_response = response.strip()
        if cleaned_response.startswith('```json'):
            cleaned_response = cleaned_response.replace('```json', '').replace('```', '').strip()
        elif cleaned_response.startswith('```'):
            cleaned_response = cleaned_response.replace('```', '').strip()

        # Parse JSON
        parsed = json.loads(cleaned_response)

        # Extract fields
        modified_code = parsed.get('modified_code')
        explanation = parsed.get('explanation', 'No explanation provided')

        # Convert null to None for modified_code
        if modified_code == "null" or modified_code == "" or modified_code is None:
            modified_code = None

        return modified_code, explanation

    except (json.JSONDecodeError, KeyError) as e:
        # Fallback handling
        if return_response_on_failure:
            return None, f":orange[⚠️ JSON parsing failed: {str(e)}]\n\nRaw response:\n{response}"
        else:
            return None, "Failed to parse response"


def format_code_explanation(explanation: str) -> str:
    """
    Format explanation text for display, ensuring proper markdown rendering
    """
    if explanation.startswith(':orange[⚠️'):
        return explanation  # Already formatted error

    # Convert markdown to HTML for proper rendering inside styled div
    formatted = explanation.strip()

    # Convert headers
    formatted = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', formatted, flags=re.MULTILINE)
    formatted = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', formatted, flags=re.MULTILINE)
    formatted = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', formatted, flags=re.MULTILINE)

    # Convert code blocks (```code```)
    formatted = re.sub(r'```(\w+)?\n(.*?)\n```', r'<pre><code>\2</code></pre>', formatted, flags=re.DOTALL)

    # Convert inline code (`code`)
    formatted = re.sub(r'`([^`]+)`', r'<code>\1</code>', formatted)

    # Convert bold (**text**)
    formatted = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted)

    # Convert italic (*text*)
    formatted = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', formatted)

    # Convert line breaks to <br> tags
    formatted = re.sub(r'\n\n', '<br><br>', formatted)
    formatted = re.sub(r'\n', '<br>', formatted)

    # Convert numbered lists
    def convert_numbered_list(match):
        lines = match.group(0).strip().split('\n')
        html = '<ol>'
        for line in lines:
            item = re.sub(r'^\d+\.\s+', '', line)
            html += f'<li>{item}</li>'
        html += '</ol>'
        return html

    # Match numbered lists (1. 2. 3. etc.)
    formatted = re.sub(r'(?:^\d+\.\s+.*$\n?)+', convert_numbered_list, formatted, flags=re.MULTILINE)

    # Convert bullet lists
    def convert_bullet_list(match):
        lines = match.group(0).strip().split('\n')
        html = '<ul>'
        for line in lines:
            item = re.sub(r'^[-*]\s+', '', line)
            html += f'<li>{item}</li>'
        html += '</ul>'
        return html

    # Match bullet lists (- or * bullets)
    formatted = re.sub(r'(?:^[-*]\s+.*$\n?)+', convert_bullet_list, formatted, flags=re.MULTILINE)

    return formatted
