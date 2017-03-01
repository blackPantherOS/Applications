#! /usr/bin/python

# notify-more.py, an enchanced command line libnotify client. With support for
# actions.
#
# Homepage: http://rory.netsoc.ucd.ie/linux/notify-more/
#
# Copyright 2006 Rory McCann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


__version__ = "0.3"

# GTK stuff
import pygtk
pygtk.require('2.0')
import gtk
import pynotify
import dbus, gobject, dbus.glib, getopt

# standard python modules
import os, sys, pickle, time
from optparse import OptionParser

def show_notification_for_these_options(options, custom_close_cb=None, call_gtk_main=True):
    
    if options.icon:
        n = pynotify.Notification(options.summary, options.content, options.icon)
    else:
        n = pynotify.Notification(options.summary, options.content)

    if options.urgency:
        if options.urgency == 'low':
            n.set_urgency(pynotify.URGENCY_LOW)
        elif options.urgency == 'normal':
            n.set_urgency(pynotify.URGENCY_NORMAL)
        elif options.urgency == 'critical':
            n.set_urgency(pynotify.URGENCY_CRITICAL)

    if options.expire_time:
        n.set_timeout(int(options.expire_time))

    # The global dict mapping action names to commands to execute. The action names
    # are used as the label of the button
    global actions
    actions = {}
    def action_cb_common(n, action):
        """
        This is the action call back. All it does is call the command that matches
        the action (ie string) that is passed in. The string is the text on the
        button. It then closes the notification and quits.
        """
        global actions
        os.system( actions[action] )
        n.close()

    def action_cb_quit_after(n, action):
        action_cb_common(n, action)
        gtk.main_quit()

    def quit_cb(n, action):
        """
        A simple call back that closes the notification n and quits the GTK
        application (i.e. this programme)
        """
        #???n.close()
        gtk.main_quit()


    if options.action_text:
        # If the notification is clicked, then we close the notification. If the
        # user specifies their own 'default' action, then it will overwrite this.
        if custom_close_cb:
            n.add_action( "default", "default", custom_close_cb )
        else:
            n.add_action( "default", "default", quit_cb )

        # If the object n sends the signal 'closed', then call the function
        # quit_cb(n, 'closed'). This is GObject stuff.
        #
        # This is important. When the notification closes (either after the time
        # has expired or the close button is clicked), this method is called. This
        # ensures that this programme will closed after the notification itself has
        # closed.
        if custom_close_cb:
            n.connect( "closed", custom_close_cb, "closed" )
        else:
            n.connect( "closed", quit_cb, "closed" )

        # Loop over all the actions and add then
        for index, action_text in enumerate(options.action_text):
            action_cmd = options.action_cmd[index]
            actions[action_text] = action_cmd
            if call_gtk_main:
                n.add_action( action_text, action_text, action_cb_quit_after )
            else:
                n.add_action( action_text, action_text, action_cb_common )


    # and show the notification
    n.show()

    # we only start the main loop if there are actions. No point in starting the
    # loop if there are no actions.
    if options.action_text and call_gtk_main:
        gtk.main()



parser = OptionParser(add_help_option=False)

parser.add_option( "-u", "--urgency", metavar="LEVEL", help="Specifies the urgency level (low, normal, critical)", default=None )
parser.add_option( "-t", "--expire-time", metavar="TIME", help="Specifies the timeout in milliseconds at which to expire the notification.", default=None, dest="expire_time" )
parser.add_option( "-i", "--icon", metavar="ICON[,ICON...]", help="Specifies an icon filename or stock icon to display.", default=None )
#parser.add_option( "-c", "--category", metavar="TYPE[,TYPE...]", help="Specifies the notification category.", default=None )
parser.add_option( "-?", "--help", action="help")
#parser.add_option( "-h", "--hint", metavar="TYPE:NAME:VALUE", help="Specifies basic extra data to pass. Valid types are int, double, string and byte.", default=None )
parser.add_option( "-v", "--version", help="Version of the package.", action="store_true", default=False )
parser.add_option( "-n", "--action-text", help="Text on the button for an action", default=None, action="append" )
parser.add_option( "-x", "--action-cmd", help="Command to execute when this action is clicked", default=None, action="append" )

parser.add_option( "-s", "--summary", help="Summary of the notification (i.e. the top line)", default=None )
parser.add_option( "-C", "--content", help="Content of the notification (i.e. the body)", default=None )


parser.add_option( "-r", "--replay", help="Replay notifications from the last hour", action="store_true", default=False )

(options, args) = parser.parse_args()

if options.replay:
    # get all notifications from the last hour.
    nm_dir = os.path.expanduser("~/.notify-more")
    if os.path.isdir(nm_dir):
        # first dump this options object.
        time_now = int(time.time())

        time_1hrago = time_now - 60 * 60

        # get all the notifications
        ls = os.listdir(nm_dir)
        ls.sort()
        notification_options = []
        for filename in ls:
            if filename.startswith("notification_"):
                # this is a pickled object, ts = timestamp
                ts = int(filename[13:])
                if ts > time_1hrago:
                    pickled_fp = open(nm_dir+"/"+filename)
                    notification_options.append(pickle.load(pickled_fp))
        num_open_notifications =  len([n for n in notification_options if n.action_text])

        def my_close_cb(n, action):
            global num_open_notifications
            n.close()

            # we only reduce this when the notification is closed. This method
            # is also the default action. if a notification is clicked on, this
            # method will be called, it'll call itself again when the
            # notificationm is closed. Thus we only reduce this value when the
            # notification closes
            if action == 'closed':
                num_open_notifications -= 1
            if num_open_notifications == 0:
                gtk.main_quit()

        pynotify.init("notify-more")

        notification_with_action_exists = False
        for option in notification_options:
            show_notification_for_these_options(option, custom_close_cb=my_close_cb, call_gtk_main=False)

        if num_open_notifications > 0:
            gtk.main()
            

else:
    # Display the notification

    if len(args) > 0 and options.summary == None:
        options.summary = args[0]
        # we pop this off the front of the args array.
        args = args[1:]
    elif len(args) == 0 and options.summary == None:
        print "No summary specified"
        sys.exit(0)


    if options.content == None:
        if len(args) > 0:
            options.content = args[0]
        else:
            options.content = ""
    # we don't have an else here (cmp summary) because content is optional.

    # now dump this object, since we're dealing with unix here, we don't bother with os.path.join(...)
    nm_dir = os.path.expanduser("~/.notify-more")
    if os.path.isdir(nm_dir):
        # first dump this options object.
        time_now = int(time.time())
        pickle_fp = open("%s/notification_%d" % (nm_dir, time_now), 'w')
        pickle.dump(options, pickle_fp)
        pickle_fp.close()

        time_24hrsago = time_now - 24 * 60 * 60

        # now delete all notification that are more than 24 hours old.
        ls = os.listdir(nm_dir)
        for filename in ls:
            if filename.startswith("notification_"):
                # this is a pickled object, ts = timestamp
                ts = int(filename[13:])
                if ts < time_24hrsago:
                    os.remove(nm_dir + "/" + filename)


    pynotify.init("notify-more")

    # Now show the notification for these options, note: this won't return
    show_notification_for_these_options(options, call_gtk_main=True)


