import re
from langchain_core.messages import ToolMessage
from tools import scrape_url

def extract_tool_outputs(agent_result: dict) -> str:
    """
    Iterate agent_result['messages'], filter for instances of ToolMessage,
    and return their content joined by double newlines.
    Fallback to the final message content if no ToolMessage is found,
    printing the raw message structure for debugging.
    """
    messages = agent_result.get("messages", [])
    tool_contents = []
    for msg in messages:
        if isinstance(msg, ToolMessage):
            content = msg.content
            if isinstance(content, list):
                parts = []
                for part in content:
                    if isinstance(part, dict) and 'text' in part:
                        parts.append(part['text'])
                    elif isinstance(part, str):
                        parts.append(part)
                tool_contents.append("\n".join(parts))
            else:
                tool_contents.append(str(content))
            
    if tool_contents:
        return "\n\n".join(tool_contents)
        
    print("\n[DEBUG] No ToolMessage instances found in agent_result['messages'].")
    print("[DEBUG] Raw message structures:")
    for idx, msg in enumerate(messages):
        print(f"  Message {idx}: Type={type(msg).__name__}, Content length={len(str(msg.content)) if msg.content else 0}")
        print(f"  Representation: {repr(msg)[:300]}...")
        
    if messages:
        last_content = messages[-1].content
        if isinstance(last_content, list):
            parts = []
            for part in last_content:
                if isinstance(part, dict) and 'text' in part:
                    parts.append(part['text'])
                elif isinstance(part, str):
                    parts.append(part)
            return "\n".join(parts)
        return str(last_content)
    return ""

def extract_urls_from_search(search_text: str, max_urls: int = 3) -> list[str]:
    r"""
    Find URLs in the search results text using re.findall with pattern URL:\s*(\S+)
    and return the first max_urls matches.
    """
    urls = re.findall(r"URL:\s*(\S+)", search_text)
    return urls[:max_urls]

def scrape_multiple(urls: list[str]) -> str:
    """
    Iterate over the list of URLs, invoke scrape_url tool directly,
    build labeled sections, and return the joined content.
    """
    sections = []
    for idx, url in enumerate(urls, start=1):
        content = scrape_url.invoke({"url": url})
        sections.append(f"--- SOURCE {idx}: {url} ---\n{content}")
    return "\n\n".join(sections)

def parse_score(critic_text: str) -> int | None:
    r"""
    Use re.search with pattern Score:\s*(\d+) (case-insensitive) to parse
    the numerical score from critic feedback.
    """
    match = re.search(r"Score:\s*(\d+)", critic_text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None
