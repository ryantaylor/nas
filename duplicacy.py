from datetime import datetime
import subprocess

class DuplicacyError(Exception):
    def __init__(self, error_code, output, error):
        self.error_code = error_code
        self.output = output
        self.error = error

class DuplicacyList:
    def __init__(self, command_output):
        self.last_updated_at = self._extract_final_revision_timestamp(command_output)
        self.text = command_output

    def _extract_final_revision_timestamp(self, command_output):
        final_revision = command_output.splitlines()[-1]
        timestamp = ' '.join(final_revision.split()[-3:-1])
        return datetime.strptime(timestamp, '%Y-%m-%d %H:%M')

class Duplicacy:
    @staticmethod
    def list():
        output = Duplicacy._run('list')
        return DuplicacyList(output)

    @staticmethod
    def backup():
        return Duplicacy._run('backup', '-threads', '4', '-stats')

    @staticmethod
    def prune(*policies):
        policies = [['-keep', policy] for policy in policies]
        flat_policies = [item for sublist in policies for item in sublist]
        return Duplicacy._run('prune', *flat_policies)

    @staticmethod
    def _run(*commands):
        commands = [str(command) for command in commands]
        result = subprocess.run(['duplicacy'] + commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            raise DuplicacyError(result.returncode, result.stdout.decode('UTF-8'), result.stderr.decode('UTF-8'))
        return result.stdout.decode('UTF-8')
