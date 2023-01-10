# About
License is BSD, author is github.com/gled-rs

The goal of this script is to allow you to follow another instance domain block and replicate for yours.

Be careful that your instance will block whatever other instance you

# Setup
- pip install -r requirements.txt
- run the first time by hand to answer the config questions
- run with a cron next time
- edit config.json if you need to tweak config

# getting an API key:
- On gotosocial, navigate to your instance admin page and use your browser network inspector to get the key
Ctrl+shift+i on Firefox, then click network and then navigate to generate  traffic. You can click a request, look at 'Request headers' and search for the Authorization: Bearer APIKEY header.
- the above method should also work on mastodon, unsure though as I don't use it.

# Items in config.json
- MY_INSTANCE: your instance domain.
- API_KEY: your instance API key to use to add the blocks ( that API key must be authorized to act to add or read blocked domain).
- TRUSTED_INSTANCES: the list of instances you want to follow ( not all instances publish their blocklist though ).
- EXEMPT_INSTANCES: the list of instances you'll never block automatically even if one of your followed instance does.

# Notes:
PR/Feedback welcome.

This has been tested on my single user gotosocial instance using a couple mastodon instances as the source of the blocklists.

As said on the [Announce post](https://ap.remote-shell.net/@gled/statuses/01GPCMVQBN1Q61PVM2589GXH8Y), there may be dragons to such an approach, think if one of the instance you decide to use
as a source for your blocklist decide to block another where you follow some friends and you did not add that one in the EXEMPT_INSTANCES list, poof, no more...

Also, as is, the script does not delete blocks, so if an instance you follow delete a block, yours won't. ( I may add that as a request if you want to file an issue for it ).
