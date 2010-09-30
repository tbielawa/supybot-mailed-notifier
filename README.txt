Introduction
============

This supybot-mailed-notifier is the set up I use at work so that we
can have Nagios alerts and configuration package updates broadcast to
our IRC channel.

What's it look like?

If an ldap server goes down, we see this:

    <shagbot> Host DOWN alert for ldapslave001!

When I update our webserver package we get a notice like this:

    <shagbot> Source: lcsee-webserver updated to Version: 8.1.1 by
    Changed-By: Timothy Bielawa (Shaggy) <tbielawa@csee.wvu.edu>

How it works:

There's an email address on my bots server that is configured to pipe
all his incoming mail to the subjectifier for parsing and
consideration. If a subject matches something we want to see then
subjectifier formats a string for the supybot plugin and writes it to
the port on localhost that the supybot-notify plugin is listening on.


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
foobar@peopleareducks.com for publishing I would add this:

    foobar:        "|/usr/bin/subjectifier"

Then update your databases with 'newaliases' or 'postaliases' or
whatever your system uses. Check aliases (5) in your manpages if
you're uncertain.


You will need to customize subjectifier before you install it.

 - Pick a default channel to post to in the notify_channel() function

 - Add or remove log_procedssed() calls for more or less debugging.
   Also: pick the right path for their output.

 - In filter_subject() you will want to define your own subject
   matching regular expressions. Without these nothing will be matched
   to make notifications about.


Going beyond
============

The subjectifier program can be adapted to do more than just spamming
IRC channels. At it's core, subjectifier is just a stand-alone program
that acts based on the content of the messages received. The way it's
configured by default it writes the last accepted message to a file
accessable on the web. It could just as easily format an RSS feed,
or enter into a database for other use later.
