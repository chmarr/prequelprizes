PrequelPrizes server-side code Copyright (c) 2013 Chris Cogdon - chris@cogdon.org

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

---------

TopazPlus fonts have licenced under a CreativeCommons licence. A full package can and should
be obtained here:

http://www.asciiarena.com/apps/t!s-af10.zip

---------

Please visit http://www.prequeladventure.com/ for one of the most comic-strippy comic strips
on the interwebs!

---------

For those just discovering this, this code was the server-side component of a prize-for-prowess for the
following game:

http://www.prequeladventure.com/this/KatiaTakeControl.html

---------

At the time of release, there were several known ways of gaming the system.

Due to the expected short time-frame that prizes would be open, we did not consider these to
be major issues, and they weren't. If you're using this code for the basis of something
more serious, please take these issues into account.

1. Keys issued by the server were themselves not signed, so it was possible for someone to use a proxy
to generate their own keys and thus bypass the automatic counter-based cut off. A planned change was to
return both the random-key, AND a HMAC-signing of that key, and have the game include the signature
into the message-to-be-signed when returning it back to the server.

2. The general issues around trying to prevent multiple registrations. There was some code inside the
flash game which was supposed to not re-request for keys if the game was re-started. This didn't appear
to work very well, or at all. Fortunately it wasn't heavily abused.