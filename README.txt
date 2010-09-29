Sending notifications manually
==============================

This plugin starts a TCP server on the given port and address, and forwards
data sent the the server to an IRC channel.

To send a message, use:
    echo '#channel message' | nc -w 1 host port

To turn off notifications for a channel, use:

    !notifications off

in the channel (replace '!' with whatever your command prefix is).


Publishing notifications by email
=================================

Put the subjectifier python program somewhere. Edit your /etc/aliases
file to pipe mail to it. For example, if I were to use
foobar@peopleareducks.com for publishing I would use this:

    foobar:        "|/usr/bin/subjectifier"

Then update your databases with 'newaliases' or 'postaliases' or
whatever your system uses. Check aliases (5) in your manpages if
you're uncertain.

You will want to customize subjectifier before you install it.


 - Pick a default channel to post to in the notify_channel() function

 - Add or remove log_procedssed calls for more or less debugging.
   Also: pick the right path for their output.



