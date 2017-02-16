"""Function used to restore data."""

import vsb_utils as utils
import os
import pwd
import grp
import subprocess


def restoreFile(settings, file_dir):
    """Restore file as in info file."""
    info = utils.loadJsonFile(os.path.join(file_dir, 'info.json'))
    try:
        o_s = oct(int(info['permissions']))
        if os.path.isfile(info['filename']):
            os.remove(info['filename'])
        if not os.path.isdir(info['filename']):
            utils.copy(os.path.join(file_dir, 'file'), info['filename'])

        os.chmod(info['filename'], int(o_s[-len(o_s)+o_s.index('o')+1:]))
        # TODO le -4 est pas bon
        # restore owner and group
        uid = pwd.getpwnam(info['owner']).pw_uid
        gid = grp.getgrnam(info['group']).gr_gid
        os.chown(info['filename'], uid, gid)

    except (KeyError, PermissionError):
        print('ERROR: Cannot restore ',
              info['filename'], ': insufficient permission')


def restoreSection(settings, name, path):
    """Restore a given section."""
    # restore files
    print('Restoring section', name)
    files_path = os.path.join(path, 'files')
    file_nums = os.listdir(files_path)
    for num in file_nums:
        restoreFile(settings, os.path.join(files_path, num))

    # restore users,groups,packages
    restoreMetaSection(settings, name, path)


def restoreMetaSection(settings, name, path):
    """Restore groups, users, packages."""
    conf = utils.loadJsonFile(os.path.join(path, 'conf.json'))
    # packages
    try:
        cmd = settings['package_installer']
        for pkg in conf['packages']:
            cmd = cmd + ' ' + pkg
        print('Installing packages:', cmd)
        subprocess.call(cmd.split())
    except (KeyError, PermissionError):
        print('Error')

    # groups
    for group in conf['groups']:
        try:
            cmd = 'groupadd ' + group
            print('Adding groups:', cmd)
            subprocess.call(cmd.split())
        except (KeyError, PermissionError):
            print('Error adding group:', group)

    # users
    for user in conf['users']:
        try:
            name = user['name']
            group = user['group']
            groups = user['groups']
            cmd = 'useradd -G ' + group + ' ' + name
            print('Adding user:', cmd)
            subprocess.call(cmd.split())

            for gr in groups:
                cmd = 'usermod -g ' + gr + ' ' + name
                print('Addings groups to user:', cmd)
                subprocess.call(cmd.split())
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
