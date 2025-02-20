#!/usr/bin/python -tt
# coding: utf-8
#
# Copyright © 2008-2010  Red Hat, Inc. All rights reserved.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.  You should have
# received a copy of the GNU General Public License along with this program; if
# not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth
# Floor, Boston, MA 02110-1301, USA. Any Red Hat trademarks that are
# incorporated in the source code or documentation are not subject to the GNU
# General Public License and may only be used or replicated with the express
# permission of Red Hat, Inc.
#
# Author(s): Luke Macken <lmacken@redhat.com>

__version__ = '3.7.3'

def parse_args():
    from optparse import OptionParser
    parser = OptionParser(version=__version__)
    parser.add_option('-c', '--console', dest='console', action='store_true',
                      help='Use console mode instead of the GUI')
    parser.add_option('-f', '--force', dest='force', action='store',
                      type='string', help='Force the use of a given drive',
                      metavar='DRIVE')
    parser.add_option('-s', '--safe', dest='safe', action='store_true',
                      help='Use the "safe, slow and stupid" bootloader')
    parser.add_option('-n', '--noverify', dest='noverify', action='store_true',
                      help='Skip checksum verification')
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                      help='Output extra debugging messages')
    parser.add_option('-k', '--extra-kernel-args', dest='kernel_args',
                      action='store', metavar='ARGS', 
                      help='Supply extra kernel arguments'
                           ' (eg: -k noswap,selinux=0,elevator=noop)')
    parser.add_option('-x', '--no-xo', dest='xo', action='store_false',
                      default=True, help='Disable OLPC support')
    parser.add_option('-m', '--reset-mbr', dest='reset_mbr',
                      action='store_true', default=False,
                      help='Reset the Master Boot Record')
    parser.add_option('-C', '--device-checksum', dest='device_checksum',
                      action='store_true', default=False,
                      help='Calculate the SHA1 of the device')
    parser.add_option('-L', '--liveos-checksum', dest='liveos_checksum',
                      action='store_true', default=False,
                      help='Calculate the SHA1 of the device')
    parser.add_option('-H', '--hash', dest='hash',
                      action='store', metavar='HASH', default='sha1',
                      help='Use a specific checksum algorithm (default: sha1)')
    #parser.add_option('-F', '--format', dest='format', action='store_true', default=False,
    #                  help='Format the device as FAT32 (WARNING: destructive)')
    #parser.add_option('-z', '--usb-zip', dest='zip', action='store_true',
    #                  help='Initialize device with zipdrive-compatible geometry'
    #                        ' for booting in USB-ZIP mode with legacy BIOSes. '
    #                        'WARNING:  This will erase everything on your '
    #                        'device!')
    return parser.parse_args() # (opts, args)


def main():
    opts, args = parse_args()
    if opts.console:
        from liveusb import LiveUSBCreator
        try:
            live = LiveUSBCreator(opts)
            live.detect_removable_drives()
            live.verify_filesystem()
            live.extract_iso()
            live.update_configs()
            live.install_bootloader()
        except Exception, e:
            print str(e)
        x = raw_input("\nDone!  Press any key to exit")
    else:
        ## Start our graphical interface
        import sys
        from liveusb.gui import LiveUSBApp
        try:
            LiveUSBApp(opts, sys.argv)
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    main()
