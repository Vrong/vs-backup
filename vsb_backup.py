"""Methods required to make backups."""

from pathlib import Path
import json
import os
import vsb_consts as consts
import vsb_utils as utils


def backupSections(settings, sections):
    """Backup data based on sections and settings."""
    keys = list(sections)
    print(len(keys), "section(s) to backup")
    for key in keys:
        backupSection(settings, key, sections[key])
        pass


def backupSection(settings, name, section):
    """Prepare backup for one given section."""
    section_path = os.path.join(utils.tmpBackupDir(settings), 'sections', name)
    section_file_path = os.path.join(section_path, 'files')
    # create the paths for later use and restore
    if not os.path.exists(section_file_path):
        os.makedirs(section_file_path)
    file_num = 0
    print()
    print("Making backup for section", name)

    # backup dirs
    if 'backup_dirs' in section:
        files = section['backup_dirs']
        for file in files:
            print(file)
            file_backup_path = os.path.join(section_file_path, str(file_num))
            print(file_backup_path)
            backupFile(settings, file, file_backup_path)
            file_num = file_num + 1

    # backup dir include
    if 'backup_dirs_inc' in section:
        files = section['backup_dirs_inc']
        for file in files:
            for dir, subdirs, fnames in os.walk(file):
                # iterate content of all subdirs
                # save dirs
                file_backup_path = os.path.join(section_file_path,
                                                str(file_num))
                backupFile(settings, dir, file_backup_path)
                file_num = file_num + 1

                for fname in fnames:
                    # save all subfiles
                    incfile = os.path.join(dir, fname)
                    file_backup_path = os.path.join(section_file_path,
                                                    str(file_num))
                    backupFile(settings, incfile, file_backup_path)
                    file_num = file_num + 1

    # backup files
    if 'backup_files' in section:
        files = section['backup_files']
        for file in files:
            file_backup_path = os.path.join(section_file_path, str(file_num))
            backupFile(settings, file, file_backup_path)
            file_num = file_num + 1

    # save groups, users,
    backupMetaSection(settings, name, section, section_path)
    pass


def backupMetaSection(settings, name, section, section_path):
    """Backup datas as users, groups and packages."""
    of = os.path.join(section_path, 'conf.json')
    info = dict()
    if 'packages' in section:
        info['packages'] = section['packages']
    if 'groups' in section:
        info['groups'] = section['groups']
    if 'users' in section:
        info['users'] = section['users']
    with open(of, 'w') as outfile:
        json.dump(info, outfile)


def backupFile(settings, filename, backup_path):
    """Create backup for one file."""
    print("Backing up", filename, 'to', backup_path)
    if not os.path.exists(filename):
        print('No file', filename)
        return
    os.makedirs(backup_path)
    info = dict()
    info['filename'] = filename
    info['permissions'] = oct(os.stat(filename).st_mode)[-3:]
    info['owner'] = Path(filename).owner()
    info['group'] = Path(filename).group()
    # write info file
    with open(os.path.join(backup_path, 'info.json'), 'w') as outfile:
        json.dump(info, outfile)
    # copy file
    # shutil.copyfile(filename, backup_path + '/' + consts.file_generic_name)
    utils.copy(filename, os.path.join(backup_path, consts.file_generic_name))


def backupList(settings):
    """Put the backuplist config in the backup."""
    utils.copy(settings['backuplist'], utils.tmpBackupDir(settings))


def genBackupName(settings):
    """Generate a backup file name based on settings."""
    basename = settings['backupfile']
    if settings['timestamp'] is True:
        basename = basename + utils.genTimestamp()
    basename = basename + '.tar.gz'
    return basename
