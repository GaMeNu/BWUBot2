from dotenv import load_dotenv
import json
import math
import os

load_dotenv()
BOTDATA = os.getenv('GD_STORAGE_PATH')
class _GD:
    
    temp_store = {}

    #Add blocks to temporary memory
    @staticmethod
    def register_block(cmd: str):
        #RegisterBlock([num,num,num]:"PlayerName")
        cmdblck = cmd[1:-1:].split(':')
        flooring = cmdblck[0][1:-1:].split(',')
        for i in range(len(flooring)):
            flooring[i] = math.floor(float(flooring[i]))
        
        cmdblck[0] = f'[{flooring[0]},{flooring[1]},{flooring[2]}]'
        
        cmdblck[1] = cmdblck[1][1:-1:]
        _GD.temp_store[cmdblck[0]] = cmdblck[1]

    #Commit the blocks to the JSON
    @staticmethod
    def commit_blocks():
        with open(BOTDATA, 'r') as f:
            storage = dict(json.loads(f.read()))

        storage.update(_GD.temp_store)

        with open(BOTDATA, 'w') as f:
            f.write(json.dumps(storage))
        _GD.temp_store = {}

#Master class Run provides a way for running all commands from the main file
class Run:
#Master function for determining the command
    async def run_command(cmd: str):

        if cmd.startswith('RegisterBlock('):
            _GD.register_block(cmd[len('RegisterBlock')::])
        elif cmd.startswith('CommitBlocks()'):
            _GD.commit_blocks()

if __name__ == '__main__':
    print('Error: Please do not run the bot_cmds file! Quitting program...')
    quit()