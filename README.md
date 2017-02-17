# vs-backup
## Synopsis

**vsbackup** is a tool used to create and restore backups on GNU/Linux systems. Backup directives are written in **backuplist.json** file.

## Prerequisites

Need **python3**

## Usage examples

To make a backup, use :
`./vsbackup -b`

By default, **./backuplist.json** file will be used.

If you want to use another location for your json configuration, use `./vsbackup -b -l BACKUPLIST`

By default, the backup will be created to **./backups/backup-timestamp-.tar.gz**, to save it to another location use `./vsbackup -b -o OUTPUT`

To restore a backup, locate the backup.tar.gz file you want to restore, and use :
`./vsbackup -r BACKUPFILE`

Note that **./settings.json** will be used as vsbackup configuration file.

For more options, use `./vsbackup -h`

## settings.json

This file is used to configure vsbackup.

Example:
~~~json
{
  "package_installer":"apt install -y",
  "tmp_dir":"/tmp",
  "backupfile":"./backups/backup",
  "backuplist":"./backuplist.json",
  "timestamp":true,
  "backup":false
}
~~~
### Help
* **package_installer** The command line to install packages on your system
* **tmp_dir** A temporary location that vsbackup can use
* **backupfile** Output backup file that will be created
* **backuplist** Backup description list that will be used (if none is specified)
* **timestamp** Append a timestamp to output backup file
* **backup** Make a backup when the program is launched, even if it's note specified in command line

## backuplist.json

Example:
~~~json
{
  "section_name":
  {
    "dependencies": ["package0"],
    "packages": ["package1", "package2"],
    "backup_files":
      [
        "/etc/somesoftware/software.conf",
        "/usr/somesoftware/database.db"
      ],
    "backup_inc":
      [
        "/etc/somesoftware/conf.d",
        "/etc/somesoftware/directorycontenttobackup"
      ],
    "backup_dirs":
      [
        "/etc/somesoftware/directorytocreate",
        "/etc/somesoftware/contentwontbebackedup"
      ],
    "backup_dirs_tree":
      [
        "/var/backupfoldertree/butnofiles"
      ],
    "groups":["group1", "group2", "group3"],
    "users":
      [
        {"name":"user1","group":"group1","groups":["group2", "groups3"]},
        {"name":"user2","group":"group2","groups":["wheel", "groups3"]}
      ],
    "cmd_start":
      [
        "command to be excuted before restoration",
        "cmd2"
      ],
    "cmd_after_dependencies":["command to run after dependencies installation"],
    "cmd_after_packages":["this command will be ran after packages installation"],
    "cmd_end":["this command will run at the end of restoration"]
  },


  "nginx-example":
  {
    "dependencies": ["curl"],
    "packages": ["nginx"],
    "cmd_after_packages":["systemctl stop nginx"],
    "backup_files":["/etc/nginx/nginx.conf"],
    "backup_inc":
      [
        "/etc/nginx/sites-available",
        "/etc/nginx/sites-enabled"
      ],
    "groups":["www-data"],
    "users":
      [
        {"name":"www-data","group":"www-data","groups":[]}
      ],
    "cmd_end":["systemctl start nginx"],
  }
}
~~~

For each program you want to backup you can create a section_name as in this example. Though the section_name can whatever you want it to be.

* **dependencies** These packages will be installed before **packages**, using the package installer set in settings.json
* **packages** These packages will be installed using the package installer set in **settings.json**
* **backup_files** These files will be backed up
* **backup_inc** These directories with their content will be backed up
* **backup_dirs** These directories will be backed up, but not their content. They will just be created with same permissions at restore time.
* **backup_dirs_tree** This directory will be backed up recursively, but files will not be included. Only folder tree.
* **groups** These groups will be created in the system if they does not exist
* **users** These users will be created with their primary and secondary groups
* **cmd_start** Theses commands will be called before section restoration
* **cmd_after_dependencies** These commands will be called after dependencies installation
* **cmd_after_packages** These commands will be called after packages installation
* **cmd_end** These commands will be called at the end of restoration
