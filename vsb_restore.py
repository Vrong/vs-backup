"""Function used to restore data."""

import vsb_utils as utils
import os
import pwd
import grp
import subprocess
import shlex


def restoreFile(settings, file_dir):
    """Restore file as in info file."""
    info = utils.loadJsonFile(os.path.join(file_dir, 'info.json'))
    try:
        print('INFO', 'Restoring file:', info['filename'])
        if os.path.isfile(info['filename']):
            os.remove(info['filename'])
        if not os.path.isdir(info['filename']):
            utils.copy(os.path.join(file_dir, 'file'), info['filename'])

        os.chmod(info['filename'], int(info['permissions'], 8))
        # restore owner and group
        uid = pwd.getpwnam(info['owner']).pw_uid
        gid = grp.getgrnam(info['group']).gr_gid
        os.chown(info['filename'], uid, gid)

    except (KeyError, PermissionError):
        print('ERROR: Cannot restore ',
              info['filename'], ': insufficient permission')


def restoreSection(settings, name, path):
    """Restore a given section."""
    print()
    print()
    print('\t', 'RESTORING SECTION', name)

    # restore users,groups,packages
    restoreMetaSection(settings, name, path)

    # restore files
    files_path = os.path.join(path, 'files')
    file_nums = os.listdir(files_path)
    for num in file_nums:
        restoreFile(settings, os.path.join(files_path, num))

    # run commands at the end of restoration
    runCmdEnd(settings, name, path)


def runCmdEnd(settings, name, path):
    """Run end commands."""
    conf = utils.loadJsonFile(os.path.join(path, 'conf.json'))
    # before package installation cmd_start
    if 'cmd_end' in conf:
        try:
            for cmd in conf['cmd_end']:
                print('INFO:', 'Running command:', cmd)
                os.system(cmd)
        except Exception:
            print('Error while running:', cmd)


def restoreMetaSection(settings, name, path):
    """Restore groups, users, packages."""
    conf = utils.loadJsonFile(os.path.join(path, 'conf.json'))

    # before package installation cmd_start
    if 'cmd_start' in conf:
        try:
            for cmd in conf['cmd_start']:
                print('INFO:', 'Running command:', cmd)
                os.system(cmd)
        except Exception:
            print('Error while running:', cmd)

    # dependencies
    if 'dependencies' in conf:
        try:
            cmd = settings['package_installer']
            for pkg in conf['dependencies']:
                cmd = cmd + ' ' + pkg
            print('INFO:', 'Installing dependencies:', cmd)
            subprocess.call(shlex.split(cmd))
        except (KeyError, PermissionError):
            print('Error while installing dependencies')
            raise

    # after dependencies installation
    if 'cmd_after_dependencies' in conf:
        try:
            for cmd in conf['cmd_after_dependencies']:
                print('INFO:', 'Running command:', cmd)
                os.system(cmd)
        except Exception:
            print('Error while running:', cmd)

    # packages
    if 'packages' in conf:
        try:
            cmd = settings['package_installer']
            for pkg in conf['packages']:
                cmd = cmd + ' ' + pkg
            print('INFO:', 'Installing packages:', cmd)
            subprocess.call(shlex.split(cmd))
        except (KeyError, PermissionError):
            print('Error while installing packages')

    # running after packages commands
    if 'cmd_after_packages' in conf:
        try:
            for cmd in conf['cmd_after_packages']:
                print('INFO:', 'Running command:', cmd)
                os.system(cmd)
        except Exception:
            print('Error while running:', cmd)

    # groups
    if 'groups' in conf:
        for group in conf['groups']:
            try:
                cmd = 'groupadd ' + group
                print('INFO:', 'Adding groups:', cmd)
                subprocess.call(shlex.split(cmd))
            except (KeyError, PermissionError):
                print('Error adding group:', group)

    # users
    if 'users' in conf:
        for user in conf['users']:
            try:
                name = user['name']
                group = user['group'] if 'group' in user else None
                groups = user['groups'] if 'groups' in user else []
                if group is None:
                    cmd = 'useradd ' + name
                else:
                    cmd = 'useradd -G ' + group + ' ' + name
                print('INFO:', 'Adding user:', cmd)
                subprocess.call(shlex.split(cmd))

                for gr in groups:
                    cmd = 'usermod -g ' + gr + ' ' + name
                    print('INFO:', 'Addings groups to user:', cmd)
                    subprocess.call(shlex.split(cmd))
            except (KeyError, PermissionError):
                print('Error while adding user', user)


def restore(settings):
    """Restore files from tmp root."""
    restore_dir = utils.tmpRestoreDir(settings)
    sections_dir = os.path.join(restore_dir, 'sections')
    sections = os.listdir(sections_dir)
    for section_name in sections:
        restoreSection(settings, section_name,
                       os.path.join(sections_dir, section_name))
