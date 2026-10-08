"""Validate native MSI dialog tab cycles to prevent Windows Installer error 2809."""
import os
import subprocess
import sys


def export_rows(path, table):
    text = subprocess.check_output([
        os.environ.get('MSIINFO_BIN', 'msiinfo'), 'export', str(path), table
    ]).decode()
    lines = text.splitlines()
    columns = lines[0].split('\t')
    return [dict(zip(columns, line.split('\t'))) for line in lines[3:] if line]


def verify(path):
    controls = export_rows(path, 'Control')
    dialogs = export_rows(path, 'Dialog')
    for dialog in dialogs:
        name = dialog['Dialog']
        local = {r['Control']: r for r in controls if r['Dialog_'] == name}
        for field in ('Control_First', 'Control_Default', 'Control_Cancel'):
            if dialog[field] and dialog[field] not in local:
                raise ValueError(f'{name}: missing {field} {dialog[field]}')
        first = dialog['Control_First']
        seen = set()
        current = first
        while current not in seen:
            if not current or current not in local:
                raise ValueError(f'{name}: broken tab cycle after {sorted(seen)} (2809)')
            seen.add(current)
            current = local[current]['Control_Next']
        if current != first:
            raise ValueError(f'{name}: tab cycle does not return to {first} (2809)')
        # This installer uses only pushbuttons as keyboard input controls.
        buttons = {r['Control'] for r in local.values() if r['Type'] == 'PushButton'}
        if not buttons.issubset(seen):
            raise ValueError(f'{name}: buttons outside tab cycle: {buttons - seen}')
        for row in local.values():
            if row['Control_Next'] and row['Control_Next'] not in local:
                raise ValueError(f'{name}: invalid Control_Next on {row["Control"]}')
    print(f'Validated tab cycles for {len(dialogs)} MSI dialogs')


if __name__ == '__main__':
    verify(sys.argv[1])
