import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
import tempfile

from src.session_processor import load_conversation, parse_messages, normalize_conversation, Message

sample_data = {
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
    ]
}


def test_load_and_parse():
    with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
        json.dump(sample_data, tmp)
        tmp_path = tmp.name

    conv = load_conversation(tmp_path)
    os.unlink(tmp_path)
    assert conv == sample_data

    msgs = parse_messages(conv)
    assert [m.type for m in msgs] == ["system", "user", "assistant"]
    assert msgs[1].content == "Hello"


def test_normalize_conversation(tmp_path_factory):
    path = tmp_path_factory.mktemp("data") / "conv.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sample_data, f)

    normalized = normalize_conversation(str(path))
    assert list(normalized.keys()) == ["conversation"]
    assert normalized["conversation"][0]["type"] == "system"
    assert normalized["conversation"][2]["content"] == "Hi there!"
