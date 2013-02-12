This is a python (2.7) script that serves downloaded packages from /var/cache/pacman/pkg and sets up a machine as a
temporary mirror. This was written for and tested only on Arch Linux, but can theoretically work for other Unixes
by changing directory of where the packages are cached.

Usage scenario:

1. Archlinux installed on machine A and netinstall being done on machine B. A acts as mirror.
2. Archlinux installed on Host A and netinstall being done on VM B. A acts as mirror.

Quickstart:

1. On machine A, launch the script.
      python2 mirror.py [-c dirs_file] [-p port_no]
2. On machine B, add the address of machine A as the topmost mirror. In /etc/pacman.d/mirrorlist:
      Server = http://machineA:port_no/

That's it. Might be a good idea to do a pacman -Sy on machine A before runing the script so that the databases are
in sync. Don't forget to pacman -Syu before installing anything on machine A, however!

How it works:
The script scans the contents of /var/cache/pacman/pkg and /var/lib/pacman/sync and builds up a dictionary with
the filenames as keys. This works because package names are unique even across repos (core/community for example).

The script then starts up a http server using Python2 BaseHTTPServer classes. Whenever a request is made, the 
last part of the URL (everything after the most final '/') is taken to be the filename and searched in the dictionary.
If the file is found, it is served with mime-type as application/x-compressed.

If the requested file is not found, a 408 response is sent back (timeout). This will cause the client (i.e. pacman on 
machine B) to switch over to the next mirror in /etc/pacman.d/mirrorlist (which is hopefully an actual mirror).

So effectively whatever file is present on A's cache is served instantly while anything absent comes from the mirrors.

Notes:
Better remove the entry for machine A after Archlinux is installed on B. This arrangement provides a speedup for the 
relaitively small footprint of base group, but over time the packages on machine A and machine B will diverge too
much for this to be of any use - you might get missing and stale packages.

If you need to do this sort of thing on an ongoing basis, better look into something like this:
https://aur.archlinux.org/packages/pacserve/

Why did I write this when pacserve was already available? Pacserve seems to need a client from AUR on the
machine receiving packages - difficult to do on a fresh installation. My script works with existing Arch Linux
infrastructure.

Or it could just be that I didn't get pacserve and wanted to write my own stuff.
