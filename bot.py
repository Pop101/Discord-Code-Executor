import discord
from Levenshtein import distance
from whats_that_code.election import guess_language_all_methods # Guesslang does not run for me
import re, requests, time
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
    # Quick scan for at least 1 match
    if not re.match(r'(```.*?\n).*?(\n```)', message.content, flags=re.M|re.S): return

    # Get all valid languages and their versions
    versions = dict()
    for lang in requests.get('https://emkc.org/api/v2/piston/runtimes').json():
        versions[lang['language']] = lang['version']
        for alias in lang['aliases']: versions[alias] = lang['version']

    # Parse all code blocks into code of a specific language
    code_blocks = map(lambda x: x.group(), re.finditer(r'(```.*?\n).*?(\n```)', message.content, flags=re.M|re.S))
    code_to_run = list()
    for code_block in code_blocks:
        # Parse lang and code out of the block
        language = code_block.split('\n')[0][3:].strip()
        code = '\n'.join(code_block.split('\n')[1:-1]).strip()
        
        if not code: continue # If the code block is empty, ignore
        if not language: # If the language is empty, try to guess
            language = guess_language_all_methods(code)
        
        # Get closest lang
        language = min(versions.keys(), key=lambda x: distance(language, x) / len(language))
        
        if language in boilerplates.supported_languages:
            code = boilerplates.add_boilerplate(language, code)
        code_to_run.append((language, code))

    # Execute code using piston api
    embed = discord.Embed(title='Code Ran', colour=discord.Colour.green())
    for i, language, code in zip(range(1, len(code_to_run)+1), *zip(*code_to_run)):
        title = f'Code Block{f" {i}" if len(code_to_run) > 1 else ""}'
        req = requests.post('https://emkc.org/api/v2/piston/execute', json={
            'language': language,
            'version': versions[language],
            'files': [
                {'name': title, 'content': code}
            ]
        })
        
        output = req.json()
        
        # Get output
        if 'run' not in output: continue

        emoji = '✅' if not output['run']['stderr'] else '❎'
        output = output['run']['output'].strip()

        # Add output to embed
        if len(code_to_run) > 1:
            embed.add_field(name=f'{emoji} {title} {emoji}', value=output, inline=False)
            if i < len(code_to_run): time.sleep(0.5) # sleep through ratelimit
        else:
            embed.title = f'{emoji} {title} {emoji}'
            embed.description = output
    
    await message.reply(embed=embed, mention_author=False)

bot.run(config['token'])
print('\n\nShut Down')