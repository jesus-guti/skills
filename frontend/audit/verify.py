"""Checks del instalador sobre proyectos temporales, sin tocar instalaciones activas."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

def run(project, *args):
    return subprocess.run([sys.executable, str(ROOT / 'frontctl'), 'install',
                           '--project', str(project), *args], capture_output=True, text=True)

class Installation(unittest.TestCase):
    def test_plan_is_read_only(self):
        with tempfile.TemporaryDirectory() as d:
            project = Path(d)
            result = run(project)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(list(project.iterdir()), [])

    def test_core_is_portable_and_contains_references(self):
        with tempfile.TemporaryDirectory() as d:
            project = Path(d)
            result = run(project, '--apply')
            self.assertEqual(result.returncode, 0, result.stderr)
            target = project / '.agents/skills'
            self.assertEqual(sorted(p.name for p in target.iterdir()),
                             sorted(json.loads((ROOT / 'profile.json').read_text())['core']))
            self.assertTrue((target / 'frontend-motion/references/animate/RECIPES.md').is_file())
            self.assertFalse(list(target.glob('*/references/**/SKILL.md')))
            self.assertTrue((target / 'impeccable/scripts/impeccable').is_file())
            again = run(project, '--apply')
            self.assertEqual(again.returncode, 0, again.stderr)
            self.assertIn('Creadas 0 skills', again.stdout)

    def test_collision_blocks_entire_batch(self):
        with tempfile.TemporaryDirectory() as d:
            project = Path(d)
            original = project / '.agents/skills/impeccable/SKILL.md'
            original.parent.mkdir(parents=True)
            original.write_text('existing user content')
            result = run(project, '--apply')
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(original.read_text(), 'existing user content')
            self.assertEqual([p.name for p in original.parent.parent.iterdir()], ['impeccable'])

    def test_symlink_outside_project_is_rejected(self):
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as outside:
            project = Path(d)
            (project / '.agents').symlink_to(outside)
            result = run(project, '--apply')
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(list(Path(outside).iterdir()), [])

    def test_optional_selection_uses_requested_harness(self):
        with tempfile.TemporaryDirectory() as d:
            project = Path(d)
            result = run(project, '--harness', 'claude', '--skills', 'variant', '--apply')
            self.assertEqual(result.returncode, 0, result.stderr)
            target = project / '.claude/skills'
            self.assertEqual(sorted(p.name for p in target.iterdir()), ['frontend-review', 'variant'])
            self.assertIn('disable-model-invocation: true', (target / 'variant/SKILL.md').read_text())
            self.assertFalse((project / '.agents').exists())

    def test_unknown_skill_creates_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            project = Path(d)
            result = run(project, '--skills', '../../other', '--apply')
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(list(project.iterdir()), [])

if __name__ == '__main__':
    unittest.main()
