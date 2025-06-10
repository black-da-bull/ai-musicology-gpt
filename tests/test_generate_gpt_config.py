import json
import os
import subprocess
import sys
test_data = {
    "prompt_template": {"name": "Test", "template": "Hello {name}"},
    "agent_persona": {"name": "Assistant", "description": "Helpful"},
    "workflow_map": {"steps": ["step1", "step2"]},
    "correction_loop": {"max_iterations": 2, "criteria": "accuracy"},
    "guardrail": {"rules": ["rule1", "rule2"]},
}


def run_script(tmpdir):
    session_path = os.path.join(tmpdir, "session.json")
    with open(session_path, "w") as f:
        json.dump(test_data, f)

    subprocess.check_call([
        sys.executable,
        os.path.join(os.path.dirname(__file__), os.pardir, "generate_gpt_config.py"),
        session_path,
        tmpdir,
    ])
    return session_path


def test_files_created(tmp_path):
    run_script(tmp_path)
    expected_files = [
        "prompt_template.json",
        "agent_persona.json",
        "workflow_map.json",
        "correction_loop.json",
        "guardrail.json",
        "custom_gpt_config.json",
        "workspace_project.md",
    ]
    for fname in expected_files:
        assert (tmp_path / fname).exists(), f"{fname} not created"

    with open(tmp_path / "custom_gpt_config.json") as f:
        data = json.load(f)
    assert data["prompt_template"]["name"] == "Test"
