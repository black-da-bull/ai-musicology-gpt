import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

@dataclass
class Message:
    type: str
    content: str


def load_conversation(path: str) -> Any:
    """Load a JSON conversation log from ``path``."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_messages(conversation: Any) -> List[Message]:
    """Parse a conversation object into ``Message`` instances."""
    # conversation may be {"messages": [...]} or just a list of messages
    if isinstance(conversation, dict):
        messages = conversation.get("messages", [])
    else:
        messages = conversation

    parsed: List[Message] = []
    for msg in messages:
        role = msg.get("role")
        content = msg.get("content")
        if role not in {"system", "user", "assistant"}:
            raise ValueError(f"Unknown role: {role}")
        parsed.append(Message(type=role, content=content))
    return parsed


def normalize_conversation(path: str) -> Dict[str, List[Dict[str, str]]]:
    """Load, parse and return a normalized dictionary for the conversation."""
    conv = load_conversation(path)
    messages = parse_messages(conv)
    return {"conversation": [asdict(m) for m in messages]}
