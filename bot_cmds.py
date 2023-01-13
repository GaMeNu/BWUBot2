import discord
from dotenv import load_dotenv
import json
import math
import os

load_dotenv()
JSON_PATH = os.getenv('GD_STORAGE_PATH')
OUTPUT_CHANNEL = int(os.getenv('COMMAND_OUTPUT_CHANNEL'))

# class _GD is concerned with editing, manipulating, and registering blocks to the storage file


class _GD:
    """
    This static class is used for editing, manipulating, and registering blocks to the JSON storage file

    class variables:
        temp_store: A dictionary to store items temporarily before dumping to JSON file

    Methods
    -------

    sort_dict(dct):
        Utility function that returns a sorted dictionary (by keys) from a given dictionary

    register_block(cmd):
        Parses a cmd from this template: ``([x,y,z]:"PlayerName")``
        to ``key = '[x,y,z]'``, ``value = 'PlayerName'``
        and adds it to `temp_store`

    commit_blocks():
        Adds the entries from `temp_store` to the JSON

    """

    # Temporary memory for saving blocks until commiting them with CommitBlocks:
    temp_store = {}

    # sorting method to sort JSON before dumping:
    @staticmethod
    def sorted_dict(dct: dict) -> dict:
        """
        Utility function that returns a sorted dictionary (by keys) from a given dictionary

        Parameters:
            dct: ``dict``
                dict to sort

        Returns:
            ``dict``:
                Sorted dictionary by keys
        """
        temp = dct
        dct = {}
        for i in sorted(temp):
            dct[i] = temp[i]

        return dct

    # Add blocks to temporary memory
    @staticmethod
    def register_block(cmd: str) -> None:
        """
        Parses a command from a template and adds it to temporary memory

        | Parses a cmd from this template: ``([x,y,z]|"PlayerName")``\n
        | to ``key = '[x,y,z]'``, ``value = 'PlayerName'``\n
        | and adds it to `temp_store`

        Parameters:
            cmd: ``str``:
                string to parse
        """
        # Command template:
        # RegisterBlock([num,num,num]|"PlayerName")

        # Parse command from string (floor values if recieved floats)
        cmdblck = cmd[1:-1:].split('|')

        flooring = cmdblck[0][1:-1:].split(',')
        for i in range(len(flooring)):
            flooring[i] = math.floor(float(flooring[i]))
        cmdblck[0] = f'[{flooring[0]},{flooring[1]},{flooring[2]}]'

        cmdblck[1] = cmdblck[1][1:-1:]

        # Resgister new blocks to temp memory
        _GD.temp_store[cmdblck[0]] = cmdblck[1]

    # Commit the blocks to the JSON
    @staticmethod
    def commit_blocks() -> None:
        """
        Adds the entries from `temp_store` to the JSON
        """
        # load JSON file to program memory
        with open(JSON_PATH, 'r') as f:
            storage = dict(json.loads(f.read()))

        # add new entries and sort
        storage.update(_GD.temp_store)
        storage = _GD.sorted_dict(storage)

        # dump new JSON back to file
        with open(JSON_PATH, 'w') as f:
            f.write(json.dumps(storage))

        # reset memory
        _GD.temp_store = {}

    @staticmethod
    def return_json_as_dict() -> dict:
        """
        This method returns the storage JSON file as a dict
        """
        with open(JSON_PATH, 'r') as f:
            ret_dct = json.loads(f.read())

        return ret_dct


class _Output:
    """
    This static class is used for sending messages and output

    Methods
    -------

    out(content, client, channel_id?):
        Sends a message to the default channel, or to a specific channel by ID

    request_block(cmd, client):
        Sends a message with a requested block and the requester using a template
    """

    @staticmethod
    async def out(content: str, client: discord.Client, channel_id: int = None) -> None:
        """
        This function sends a message to the default channel, or to a specific channel if an ID is given.

        Parameters
        ----------

        content: ``str``
            Message to send

        client: ``discord.Client``
            A discord bot client to send the message with

        channel_id: ``int | None``
            A discord channel ID to send the message to.
            Sends to the `DEFAULT_CHANNEL` if None is given.
        """

        if channel_id == None:
            channel = client.get_channel(OUTPUT_CHANNEL)
        else:
            channel = client.get_channel(channel_id)

        await channel.send(content=content)

    async def request_block(cmd: str, client: discord.Client):
        """
        Sends a message to the `DEFAULT_CHANNEL` with the requested block and a requester.\n
        Template: ([x,y,z]|"RequesterName")

        Parameters:
            cmd: ``str``
                Command to parse
            client: ``discord.Client``
                Discord client to send from
        """
        cmdblck = cmd[1:-1].split('|')

        flooring = cmdblck[0][1:-1:].split(',')
        for i in range(len(flooring)):
            flooring[i] = math.floor(float(flooring[i]))
        cmdblck[0] = f'[{flooring[0]},{flooring[1]},{flooring[2]}]'

        cmdblck[1] = cmdblck[1][1:-1:]

        storage = _GD.return_json_as_dict()

        out_str: str
        if not cmdblck[0] in storage.keys():
            out_str = f'There doesn\'t seem to be any player saved to location **{cmdblck[0]}**.'
        else:
            out_str = f'The last player to modify the block at location **{cmdblck[0]}** is **{storage[cmdblck[0]]}**'

        out_str += f'\n(Requested by {cmdblck[1]})'

        await _Output.out(out_str, client)


async def run_command(cmd: str, client: discord.Client = None) -> None:
    """
    This function interprets the command passed to it and runs the fitting function.

    Parameters:
        cmd: ``str``
            A command to parse
        client: ``discord.Client``
            A discord bot client for commands that require it
    """

    if cmd.startswith('RegisterBlock('):
        _GD.register_block(cmd[len('RegisterBlock')::])
    elif cmd.startswith('CommitBlocks()'):
        _GD.commit_blocks()
    elif cmd.startswith('RequestBlock('):
        await _Output.request_block(cmd[len('RequestBlock')::], client)


if __name__ == '__main__':
    print('\nError: Please do not run the bot_cmds file! Quitting program...\n')
    quit()
