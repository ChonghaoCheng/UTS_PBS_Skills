"""Local regression tests. No AI clients, SSH connections or PBS jobs are started."""
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/cetus-pbs'
INSTALLER = ROOT / 'scripts/install.sh'


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.project = self.base / 'project with spaces'
        self.project.mkdir()
        self.bin = self.base / 'bin'
        self.bin.mkdir()
        self.env = dict(os.environ)
        for name in ('CODEX_THREAD_ID', 'CLAUDECODE', 'PBS_JOBID',
                     'CLAUDE_CONFIG_DIR', 'DSH_HOME', 'XDG_CONFIG_HOME'):
            self.env.pop(name, None)
        self.env['PATH'] = str(self.bin) + ':/usr/bin:/bin'
        self.env['TMPDIR'] = str(self.base)
        self.command('hostname', 'echo workstation')

    def command(self, name, body):
        path = self.bin / name
        path.write_text('#!/bin/bash\nset -e\n' + body + '\n')
        path.chmod(0o755)

    def run_installer(self, *args, piped=False, personal=False):
        command = ['bash', '-s', '--'] if piped else ['bash', str(INSTALLER)]
        if not personal:
            command += ['--project', str(self.project)]
        result = subprocess.run(command + list(args), env=self.env,
                                input=INSTALLER.read_text() if piped else None,
                                text=True, capture_output=True)
        return result

    def installed(self, client):
        folder = {'codex': '.agents', 'claude': '.claude', 'dsh': '.dsh',
                  'cursor': '.cursor', 'copilot': '.github', 'gemini': '.gemini',
                  'opencode': '.opencode'}[client]
        return self.project / folder / 'skills/cetus-pbs'

    def test_detects_each_client_and_all(self):
        for client in ('codex', 'claude', 'dsh', 'cursor', 'copilot', 'gemini', 'opencode'):
            self.command(client, 'exit 99')  # Discovery must not execute the CLI.
            result = self.run_installer()
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((self.installed(client) / 'SKILL.md').read_bytes(),
                             (SKILL / 'SKILL.md').read_bytes())
        self.assertEqual(self.run_installer().returncode, 0)

    def test_active_codex_overrides_other_installed_clients(self):
        self.command('claude', 'exit 99')
        self.env['CODEX_THREAD_ID'] = 'test-session'
        result = self.run_installer()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.installed('codex').exists())
        self.assertFalse(self.installed('claude').exists())

    def test_active_claude_and_explicit_override(self):
        self.env['CLAUDECODE'] = '1'
        self.assertEqual(self.run_installer().returncode, 0)
        self.assertTrue(self.installed('claude').exists())
        self.assertEqual(self.run_installer('--client', 'dsh').returncode, 0)
        self.assertTrue(self.installed('dsh').exists())

    def test_no_client_exits_without_installing(self):
        result = self.run_installer()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('--client codex', result.stderr)
        self.assertEqual(list(self.project.iterdir()), [])

    def test_repeat_is_noop_and_changes_are_backed_up(self):
        self.assertEqual(self.run_installer('--client', 'all').returncode, 0)
        result = self.run_installer('--client', 'all')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count('Already up to date'), 7)
        self.assertEqual(list(self.project.glob('*/skill-backups/*')), [])
        installed = self.installed('codex') / 'SKILL.md'
        installed.write_text('custom old skill\n')
        result = self.run_installer('--client', 'codex')
        self.assertEqual(result.returncode, 0, result.stderr)
        backups = list(self.project.glob('.agents/skill-backups/*/cetus-pbs/SKILL.md'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), 'custom old skill\n')
        self.assertEqual(installed.read_bytes(), (SKILL / 'SKILL.md').read_bytes())

    def test_custom_personal_roots(self):
        for client, variable in (('claude', 'CLAUDE_CONFIG_DIR'), ('dsh', 'DSH_HOME')):
            config = self.base / client
            self.env[variable] = str(config)
            result = self.run_installer('--client', client, personal=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((config / 'skills/cetus-pbs/assets/job.pbs').is_file())

    def test_custom_skill_directory_without_client(self):
        skills = self.base / 'another agent' / 'skill-library'
        result = self.run_installer('--skills-dir', str(skills), personal=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((skills / 'cetus-pbs/SKILL.md').exists())
        repeated = self.run_installer('--skills-dir', str(skills), personal=True)
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertIn('Already up to date', repeated.stdout)
        conflict = self.run_installer('--skills-dir', str(skills), '--client', 'codex', personal=True)
        self.assertNotEqual(conflict.returncode, 0)

    def test_opencode_personal_config_root(self):
        self.env['XDG_CONFIG_HOME'] = str(self.base / 'user-config')
        result = self.run_installer('--client', 'opencode', personal=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.base / 'user-config/opencode/skills/cetus-pbs/SKILL.md').exists())

    def test_source_destination_and_lock_are_protected(self):
        destination = self.installed('codex')
        destination.parent.mkdir(parents=True)
        destination.symlink_to(SKILL)
        self.assertNotEqual(self.run_installer('--client', 'codex').returncode, 0)
        self.assertTrue(destination.is_symlink())
        destination.unlink()
        (destination.parent / '.cetus-pbs-install.lock').mkdir()
        self.assertNotEqual(self.run_installer('--client', 'codex').returncode, 0)
        self.assertFalse(destination.exists())

    def test_failed_swap_restores_old_skill(self):
        self.assertEqual(self.run_installer('--client', 'codex').returncode, 0)
        previous = self.installed('codex') / 'SKILL.md'
        previous.write_text('keep this copy\n')
        self.command('mv', 'if [[ "$2" == *".cetus-pbs-install."* ]]; then exit 1; fi\nexec /bin/mv "$@"')
        result = self.run_installer('--client', 'codex')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(previous.read_text(), 'keep this copy\n')
        self.assertFalse((previous.parent.parent / '.cetus-pbs-install.lock').exists())

    def test_standalone_pipe_downloads_complete_skill(self):
        payload = self.base / 'payload.tar.gz'
        with tarfile.open(payload, 'w:gz') as archive:
            archive.add(SKILL, arcname='UTS_PBS_Skills-main/skills/cetus-pbs')
        self.env['TEST_PAYLOAD'] = str(payload)
        self.command('curl', 'cp -- "$TEST_PAYLOAD" "${@: -1}"')
        result = self.run_installer('--client', 'codex', piped=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.installed('codex') / 'assets/job.pbs').read_bytes(),
                         (SKILL / 'assets/job.pbs').read_bytes())
        self.assertEqual(list(self.base.glob('cetus-pbs-download.*')), [])

    def test_network_failure_leaves_no_skill(self):
        self.command('curl', 'exit 22')
        result = self.run_installer('--client', 'codex', piped=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.installed('codex').exists())
        self.assertEqual(list(self.base.glob('cetus-pbs-download.*')), [])

    def test_server_allocation_and_bad_arguments_are_rejected(self):
        self.env['PBS_JOBID'] = 'test.server'
        self.assertNotEqual(self.run_installer('--client', 'codex').returncode, 0)
        self.env.pop('PBS_JOBID')
        self.command('hostname', 'echo hpc-login02')
        self.assertNotEqual(self.run_installer('--client', 'codex').returncode, 0)
        self.command('hostname', 'echo workstation')
        for args in (('--client',), ('--client', 'unknown'), ('--project', '--update')):
            self.assertNotEqual(self.run_installer(*args).returncode, 0)
        self.assertEqual(list(self.project.iterdir()), [])


class JobTemplateTests(unittest.TestCase):
    def setUp(self):
        if not shutil.which('rsync'):
            self.skipTest('rsync is required for job transfer tests')
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.run = self.base / 'run'
        self.run.mkdir()
        self.scratch = self.base / 'scratch'
        self.scratch.mkdir()
        self.bin = self.base / 'bin'
        self.bin.mkdir()
        hostname = self.bin / 'hostname'
        hostname.write_text('#!/bin/bash\necho hpc-exec-test\n')
        hostname.chmod(0o755)
        self.env = dict(os.environ, PBS_JOBID='123.test', PBS_O_WORKDIR=str(self.run),
                        CETUS_SCRATCH_ROOT=str(self.scratch),
                        PATH=str(self.bin) + ':' + os.environ['PATH'])
        self.env.pop('PBS_ARRAY_INDEX', None)
        code = self.base / 'code'
        code.mkdir()
        (code / 'input.txt').write_text('frozen input\n')
        with tarfile.open(self.run / 'code.tar', 'w') as archive:
            archive.add(code / 'input.txt', arcname='input.txt')
        shutil.copy(SKILL / 'assets/job.pbs', self.run / 'job.pbs')
        (self.run / 'request.env').write_text(
            'REQUEST_SELECT=select=1:ncpus=8:mem=12gb\nREQUEST_WALLTIME=01:23:45\n')
        self.command('cat input.txt > "$2/result.txt"\nprintf "%s" "$1" > "$2/index.txt"')

    def command(self, body):
        (self.run / 'command.sh').write_text('#!/bin/bash\nset -euo pipefail\n' + body + '\n')
        checksums = subprocess.check_output(['sha256sum', 'code.tar', 'job.pbs', 'command.sh', 'request.env'],
                                            cwd=self.run)
        (self.run / 'SHA256SUMS').write_bytes(checksums)

    def execute(self):
        return subprocess.run(['bash', str(self.run / 'job.pbs')], env=self.env,
                              text=True, capture_output=True)

    def attempt(self, index=1):
        return next((self.run / 'tasks' / str(index)).glob('attempt-*'))

    def test_success_and_repeat_keep_independent_attempts(self):
        self.assertEqual(self.execute().returncode, 0)
        attempt = self.attempt()
        self.assertEqual((attempt / 'results/result.txt').read_text(), 'frozen input\n')
        self.assertEqual((attempt / 'exit_status').read_text().strip(), '0')
        self.assertTrue((attempt / 'ended_at').exists())
        self.assertEqual(list(self.scratch.iterdir()), [])
        self.assertEqual(self.execute().returncode, 0)
        self.assertEqual(len(list((self.run / 'tasks/1').glob('attempt-*'))), 2)

    def test_array_index_is_forwarded(self):
        for index in (0, 4):
            self.env['PBS_ARRAY_INDEX'] = str(index)
            self.assertEqual(self.execute().returncode, 0)
            self.assertEqual((self.attempt(index) / 'results/index.txt').read_text(), str(index))

    def test_work_root_can_fall_back_to_run_directory(self):
        self.env.pop('CETUS_SCRATCH_ROOT', None)
        self.env.pop('TMPDIR', None)
        self.assertEqual(self.execute().returncode, 0)
        work = Path((self.attempt() / 'scratch_path').read_text().strip())
        self.assertEqual(work.parent, self.run)
        self.assertFalse(work.exists())
        self.assertTrue((self.attempt() / 'results/result.txt').exists())

    def test_template_preserves_application_thread_settings(self):
        self.env.update(OMP_NUM_THREADS='3', OPENBLAS_NUM_THREADS='2')
        self.command('printf "%s:%s" "$OMP_NUM_THREADS" "$OPENBLAS_NUM_THREADS" > "$2/threads.txt"')
        self.assertEqual(self.execute().returncode, 0)
        self.assertEqual((self.attempt() / 'results/threads.txt').read_text(), '3:2')

    def test_shell_demonstration_runs_without_git_or_python_workload(self):
        document = (SKILL / 'references/pbs.md').read_text()
        prepare = re.findall(r'```bash\n(.*?)```', document, re.S)[0]
        prepare = prepare.replace('skill_dir=/absolute/path/to/cetus-pbs', 'skill_dir="$TEST_SKILL"')
        prepare = prepare.replace('local_base="$HOME/cetus-runs"', 'local_base="$TEST_LOCAL_BASE"')
        root = self.base / 'demo-runs'
        env = dict(self.env, TEST_SKILL=str(SKILL), TEST_LOCAL_BASE=str(root))
        result = subprocess.run(['bash', '-e', '-s'], input=prepare, env=env,
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        demo = next(root.iterdir())
        (demo / 'source/input.txt').write_text('later source change\n')
        env['PBS_O_WORKDIR'] = str(demo)
        worker = subprocess.run(['bash', str(demo / 'job.pbs')], env=env,
                                text=True, capture_output=True)
        self.assertEqual(worker.returncode, 0, worker.stderr)
        attempt = next((demo / 'tasks/1').glob('attempt-*'))
        self.assertEqual((attempt / 'results/output.txt').read_text(), 'example input\n')
        self.assertEqual((attempt / 'exit_status').read_text().strip(), '0')

    def test_application_failure_preserves_outputs_and_exit(self):
        self.command('echo partial > "$2/partial.txt"\nexit 7')
        self.assertEqual(self.execute().returncode, 7)
        self.assertEqual((self.attempt() / 'results/partial.txt').read_text().strip(), 'partial')
        self.assertEqual((self.attempt() / 'exit_status').read_text().strip(), '7')
        self.assertEqual(list(self.scratch.iterdir()), [])

    def test_transfer_failure_retains_scratch(self):
        rsync = self.bin / 'rsync'
        rsync.write_text('#!/bin/bash\nexit 23\n')
        rsync.chmod(0o755)
        self.assertEqual(self.execute().returncode, 23)
        attempt = self.attempt()
        self.assertEqual((attempt / 'exit_status').read_text().strip(), '23')
        self.assertTrue(Path((attempt / 'scratch_path').read_text().strip()).exists())

    def test_checksum_failure_stops_before_workload(self):
        (self.run / 'command.sh').write_text('exit 0\n')
        self.assertNotEqual(self.execute().returncode, 0)
        self.assertTrue((self.attempt() / 'exit_status').exists())
        self.assertEqual(list(self.scratch.iterdir()), [])

    def test_login_node_guard_and_missing_allocation(self):
        (self.bin / 'hostname').write_text('#!/bin/bash\necho hpc-login02\n')
        self.assertNotEqual(self.execute().returncode, 0)
        self.assertFalse((self.run / 'tasks').exists())
        self.env.pop('PBS_JOBID')
        self.assertNotEqual(self.execute().returncode, 0)

    def test_submission_example_refuses_second_qsub(self):
        document = (SKILL / 'references/pbs.md').read_text()
        blocks = re.findall(r"<<'REMOTE'\n(.*?)\nREMOTE", document, re.S)
        submit = blocks[1].replace('cd "$HOME/cetus-runs/$1"', 'cd "$TEST_RUN"')
        qsub = self.bin / 'qsub'
        qsub.write_text('#!/bin/bash\necho called >> "$TEST_RUN/calls"\n'
                        'printf "%s\\n" "$@" > "$TEST_RUN/qsub-args"\necho 123.test\n')
        qsub.chmod(0o755)
        self.env['TEST_RUN'] = str(self.run)
        for expected in (0, 1):
            result = subprocess.run(['bash', '-s', '--', 'run', 'ct123'], input=submit,
                                    env=self.env, text=True, capture_output=True)
            self.assertEqual(result.returncode, expected, result.stderr)
        self.assertEqual((self.run / 'calls').read_text().splitlines(), ['called'])
        self.assertEqual((self.run / 'submission/job_id').read_text().strip(), '123.test')
        args = (self.run / 'qsub-args').read_text().splitlines()
        self.assertIn('select=1:ncpus=8:mem=12gb', args)
        self.assertIn('walltime=01:23:45', args)


if __name__ == '__main__':
    unittest.main()
