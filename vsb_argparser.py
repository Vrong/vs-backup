"""Parses args for vs_backup."""

import argparse


def parseArgs(settings):
    """Initialize vsbackup with cli args."""
    parser = argparse.ArgumentParser(description='Create a backup.')

    parser.add_argument('-b', '--backup', dest='backup', action='store_true',
                        help='start backup', default=False)

    parser.add_argument('-r', '--restore', action='store', dest='restorefile',
                        help='restore backup (ex: -r ./backup20170215.tar.gz)')

    parser.add_argument('-l', '--list', dest='backuplist', action='store',
                        default=None,
                        help='output file prefix (ex: ./backuplist.json)')
    parser.add_argument('-o', '--output', dest='backupfile', action='store',
                        default=None,
                        help='output file prefix (ex: ./backup)')
    parser.add_argument('-ts', '--timestamp', dest='timestamp',
                        action='store',
                        help='append timestamp to backup filename.\
                        (ex: -ts on|off)')
    parser.add_argument('-tmp', '--tmp', dest='tmp_dir', action='store',
                        default=None,
                        help='temporary directory (ex: /tmp)')
    # TODO add all settings in args

    args = parser.parse_args()

    if args.backup is True:
        settings['backup'] = args.backup

    if args.restorefile is not None:
        settings['restorefile'] = args.restorefile

    if args.backupfile is not None:
        settings['backupfile'] = args.backupfile

    if args.timestamp == 'on':
        settings['timestamp'] = True
    elif args.timestamp == 'off':
        settings['timestamp'] = False

    if args.backuplist is not None:
        settings['backuplist'] = args.backuplist

    if args.tmp_dir is not None:
        settings['tmp_dir'] = args.tmp_dir

    print('Settings in use :', settings)
    return settings
