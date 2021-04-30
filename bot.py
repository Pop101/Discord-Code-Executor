import discord
from Levenshtein import distance
from whats_that_code.election import guess_language_all_methods # Guesslang does not run for me
import re, requests
import boilerplates

import yaml
try: from yaml import CLoader as Loader
except ImportError: from yaml import Loader

# load the config
config = dict()
with open('./config.yml') as file:
    yml = yaml.load(file.read(), Loader=Loader)
    try:
        config['token'] = yml['Token']
    except (KeyError, ValueError): 
        print('Error in config')
        quit(1)
    assert '<TOKEN>' not in repr(config), 'Please add your token to the config!'

bot = discord.Client()

@bot.event
async def on_ready():
    print('\n\nBooted!\n\n')

@bot.event
async def on_message(message):
    code_blocks = map(lambda x: x.group(), re.finditer(r'(```.*\n).*?(\n```)', message.content, flags=re.M|re.S))
    
    for code_block in code_blocks:
        # Parse lang and code out of the block
        language = code_block.split('\n')[0][3:].strip()
        code = '\n'.join(code_block.split('\n')[1:-1]).strip()
        
        if not code: continue # If the code block is empty, ignore
        if not language: # If the language is empty, try to guess
            language = guess_language_all_methods(code)
        
        # Get closest lang
        versions = dict()
        for lang in requests.get('https://emkc.org/api/v2/piston/runtimes').json():
            versions[lang['language']] = lang['version']
            for alias in lang['aliases']: versions[alias] = lang['version']
        
        language = min(versions.keys(), key=lambda x: distance(language, x) / len(language))
        
        if language in boilerplates.supported_languages:
            code = boilerplates.add_boilerplate(language, code)
        
        # Execute code using piston api
        req = requests.post('https://emkc.org/api/v2/piston/execute', json={
            'language': language,
            'version': versions[language],
            'files': [
                {'name': f'temp.txt', 'content': code}
            ]
        })
        output = req.json()

        # get output or stdout
        if 'run' not in output: continue
        output = (output['run']['output'] or output['run']['stdout'] or '').strip()
        if output: await message.channel.send(output)

bot.run(config['token'])
print('\n\nShut Down')