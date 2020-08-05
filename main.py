import base64
import discord
from scraper import *
from token import *
import random

client = discord.Client()
parser = Bongard()
slnparse = Solution()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(')help'):
        await message.channel.send('List of commands:\n**)bong [number]** or **)b [number]**: displays the '
                                   'corresponding Bongard problem from the OEBP database. \n**)solution [number]** or '
                                   '**)sln [number]**: displays the solution for the corresponding Bongard problem '
                                   'from the OEBP database.\n**)randbong** or **)rand**: displays a random Bongard '
                                   'number.\n**)ping**: displays bot latency in milliseconds\n**)info**: displays '
                                   'more information about Bongard problems.')

    if message.content.startswith(')info'):
        await message.channel.send('__**WHAT IS A BONGARD PROBLEM?**__\nThe term "Bongard problem" is used to refer '
                                   'to a number of problems developed by Soviet computer scientist Mikhail M. Bongard '
                                   '(and others) that are designed to test for intelligence in a computer. As such, '
                                   'logic lies at the core of these problems, and can be quite fun for humans to '
                                   'solve as well.\n__**HOW DO I SOLVE A BONGARD PROBLEM?**__\nA Bongard problem has '
                                   'two sets of six tiles, six on the left of a dividing line and six on the right of '
                                   'it. The set of tiles on the left all follow a particular rule, i.e. the elements '
                                   'within the tiles have one specific characteristic in common. The set of tiles on '
                                   'the right all break this rule. **Once you state the rule, you have "solved" the '
                                   'problem!**\n__**WHERE ARE THESE COMING FROM?**__\nAll the Bongard problems used '
                                   'by the bot are taken from http://www.oebp.org/. I highly recommend you look at '
                                   'their site, as you can search problems by tag or creator, view commentary on '
                                   'specific problems, and even submit your own Bongard problems made from new or '
                                   'existing assets. I have no affiliation with the OEBP, I just think it\'s a really '
                                   'neat place run by some very passionate people. **I do not and don\'t '
                                   'expect to have any sort of financial gain as a result of this bot.**')

    if message.content.startswith(')randbong') or message.content.startswith(')rand') or message.content.startswith(')rb'):
        randbong = random.randint(2, 394)
        url = "http://oebp.org/incarnate.php?bp=" + str(randbong)
        page = requests.get(url, headers=headers)
        parser.feed(page.text)
        bong = str.encode(parser.img)
        base = base64.decodebytes(bong)
        with open("bong.jpg", "wb") as f:
            f.write(base)
        await message.channel.send('BONG! Bongard problem #' + str(randbong) + ': \n(' + url + ')')
        await message.channel.send(file=discord.File('bong.jpg'))

    if message.content.startswith(')bong') or message.content.startswith(')b'):
        number = message.content.split()[1]
        if number == '1':
            await message.channel.send('BONG! Bongard problem #1:\n(http://oebp.org/incarnate.php?bp=1)')
            await message.channel.send(file=discord.File('bong1.png'))
        else:
            url = "http://oebp.org/incarnate.php?bp=" + number
            page = requests.get(url, headers=headers)
            parser.feed(page.text)
            bong = str.encode(parser.img)
            base = base64.decodebytes(bong)
            with open("bong.jpg", "wb") as f:
                f.write(base)
            await message.channel.send('BONG! Bongard problem #' + number + ': \n(' + url + ')')
            await message.channel.send(file=discord.File('bong.jpg'))

    if message.content.startswith(')solution') or message.content.startswith(')sln') or message.content.startswith(')s'):
        number = message.content.split()[1]
        url = "http://oebp.org/BP" + number
        page = requests.get(url, headers=headers)
        slnparse.feed(page.text)
        await message.channel.send('BONG! Sent you the solution for problem #' + number + '.')
        await message.author.send('BONG! Solution for Bongard problem #' + number + ': ||' + slnparse.text + '||')\

    if message.content.startswith(')ping'):
        ping = str(int(client.latency * 1000))
        await message.channel.send('BONG! Ping: ' + ping + ' milliseconds.')

client.run(token)
