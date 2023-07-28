#!/usr/bin/env python

# Crete an application that connects to Twich chat and strims the chat to stdout, using python-twitch-stream library and TwitchChatStream object

from chat import TwitchChatStream
import argparse
import time


def main():
    parser = argparse.ArgumentParser(description='Twitch chat')
    required = parser.add_argument_group('required arguments')
    required.add_argument('-u', '--username',
                          help='twitch username',
                          required=True)
    required.add_argument('-o', '--oauth',
                          help='twitch oauth '
                               '(visit https://twitchapps.com/tmi/ '
                               'to create one for your account)',
                          required=True)
    required.add_argument('-c', '--channel',
                          help='twitch channel to join',
                          required=True)

    args = parser.parse_args()
    with TwitchChatStream(
            # Must provide a lowercase username.
            username=args.username.lower(),
            oauth=args.oauth,
            verbose=False) as chatstream:
        
        chatstream.join_channel(args.channel.lower())
        while True:
            # Every loop, call to receive messages.
            # This is important, when it is not called,
            # Twitch will automatically log you out.
            # This call is non-blocking.
            received = chatstream.twitch_receive_messages()

            # process all the messages
            if received:
                for chat_message in received:
                    print(f"{chat_message['username']}: {chat_message['message']}")
            else:
                time.sleep(.1)


if __name__ == '__main__':
    main()
