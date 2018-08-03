import os
import re
import subprocess

class SnapraidError(Exception):
    def __init__(self, error_code, message):
        self.error_code = error_code
        self.message = message

class SnapraidDiff:
    def __init__(self, command_output):
        lines = command_output.splitlines()
        groupings = self._group_output(lines)

        self.equal = self._extract_value(groupings['equal'])
        self.added = self._extract_value(groupings['added'])
        self.removed = self._extract_value(groupings['removed'])
        self.updated = self._extract_value(groupings['updated'])
        self.moved = self._extract_value(groupings['moved'])
        self.copied = self._extract_value(groupings['copied'])
        self.restored = self._extract_value(groupings['restored'])
        self.text = command_output

    def has_changes(self):
        return self.added > 0 \
            or self.removed > 0 \
            or self.updated > 0 \
            or self.moved > 0 \
            or self.copied > 0 \
            or self.restored > 0

    def _group_output(self, lines):
        groupings = {
            'equal': [],
            'added': [],
            'removed': [],
            'updated': [],
            'moved': [],
            'copied': [],
            'restored': []
        }

        for line in lines:
            for key in groupings.keys():
                if key in line:
                    groupings[key].append(line.strip())
                    break

        return groupings

    def _extract_value(self, arr):
        return int(arr[-1].split()[0])

class SnapraidStatus:
    def __init__(self, command_output):
        self.text = command_output

        summary_index = command_output.find('The oldest block was scrubbed')
        self.summary = command_output[summary_index:]

        (self.oldest_scrubbed_at,
         self.median_scrubbed_at,
         self.newest_scrubbed_at) = self._extract_scrub_metadata(self.summary)

    # Example summary line: The oldest block was scrubbed 22 days ago, the median 10, the newest 0.
    def _extract_scrub_metadata(self, summary):
        scrub_line = summary.splitlines()[0].split()
        parsed_scrub_line = [re.sub('[^0-9]', '', item) for item in scrub_line]
        return [int(item) for item in parsed_scrub_line if item.isdigit()]

class SnapraidScrub():
    def __init__(self, command_output):
        lines = command_output.splitlines()
        blank_indices = [index for index, item in enumerate(lines) if not item.strip()]
        self.progress = os.linesep.join(lines[:blank_indices[0]])
        self.result = os.linesep.join(lines[blank_indices[1]:])
        self.summary = os.linesep.join([self.progress, self.result])

class Snapraid:
    @staticmethod
    def sync():
        return Snapraid._run('sync')

    @staticmethod
    def diff():
        output = Snapraid._run('diff')
        return SnapraidDiff(output)

    @staticmethod
    def status():
        output = Snapraid._run('status')
        return SnapraidStatus(output)

    @staticmethod
    def scrub(percentage=None):
        if percentage:
            output = Snapraid._run('-p', percentage, 'scrub')
        else:
            output = Snapraid._run('scrub')
        return SnapraidScrub(output)

    @staticmethod
    def _run(*commands):
        commands = [str(command) for command in commands]
        result = subprocess.run(['snapraid'] + commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 1:
            raise SnapraidError(result.returncode, result.stderr.decode('UTF-8'))
        return result.stdout.decode('UTF-8')
