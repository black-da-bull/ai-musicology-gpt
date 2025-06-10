import json
import os
import sys
from dataclasses import asdict
from prompt_modules import (
    PromptTemplate,
    AgentPersona,
    WorkflowMap,
    CorrectionLoop,
    Guardrail,
)


def load_session_data(path: str) -> dict:
    with open(path, 'r') as f:
        return json.load(f)


def write_json(obj, path: str):
    with open(path, 'w') as f:
        json.dump(obj, f, indent=2)


def generate_files(session_path: str, output_dir: str = '.'):
    data = load_session_data(session_path)

    pt = PromptTemplate(**data.get('prompt_template', {}))
    ap = AgentPersona(**data.get('agent_persona', {}))
    wm = WorkflowMap(**data.get('workflow_map', {}))
    cl = CorrectionLoop(**data.get('correction_loop', {}))
    gr = Guardrail(**data.get('guardrail', {}))

    os.makedirs(output_dir, exist_ok=True)

    write_json(asdict(pt), os.path.join(output_dir, 'prompt_template.json'))
    write_json(asdict(ap), os.path.join(output_dir, 'agent_persona.json'))
    write_json(asdict(wm), os.path.join(output_dir, 'workflow_map.json'))
    write_json(asdict(cl), os.path.join(output_dir, 'correction_loop.json'))
    write_json(asdict(gr), os.path.join(output_dir, 'guardrail.json'))

    custom = {
        'prompt_template': asdict(pt),
        'agent_persona': asdict(ap),
        'workflow_map': asdict(wm),
        'correction_loop': asdict(cl),
        'guardrail': asdict(gr),
    }
    write_json(custom, os.path.join(output_dir, 'custom_gpt_config.json'))

    md_lines = [
        '# Workspace Project',
        '',
        '## Prompt Template',
        f"Name: {pt.name}",
        '',
        '```',
        pt.template,
        '```',
        '',
        '## Agent Persona',
        f"Name: {ap.name}",
        '',
        ap.description,
        '',
        '## Workflow Map',
    ]
    md_lines.extend(f"- {step}" for step in wm.steps)
    md_lines.extend([
        '',
        '## Correction Loop',
        f"Max Iterations: {cl.max_iterations}",
        f"Criteria: {cl.criteria}",
        '',
        '## Guardrail',
    ])
    md_lines.extend(f"- {rule}" for rule in gr.rules)
    md_lines.append('')

    with open(os.path.join(output_dir, 'workspace_project.md'), 'w') as f:
        f.write('\n'.join(md_lines))


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    if not args:
        print('Usage: generate_gpt_config.py <session_data.json> [output_dir]')
        return 1
    session_path = args[0]
    output_dir = args[1] if len(args) > 1 else '.'
    generate_files(session_path, output_dir)
    return 0


if __name__ == '__main__':
    sys.exit(main())
