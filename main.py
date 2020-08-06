import base64
import discord
from scraper import *
from botToken import *
import random

client = discord.Client()
parser = Bongard()
slnparse = Solution()


@client.event
async def on_ready():
    print('{0.user} IS ONLINE. INITIALIZE BONGARDIZATION.'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(')help'):
        await message.channel.send(helpmsg)

    if message.content.startswith(')info'):
        await message.channel.send(infomsg)

    if message.content.startswith(')randbong') or message.content.startswith(')rand') or message.content.startswith(
            ')rb') or (message.content.startswith(')bong') and len(message.content) == 5):
        randbong = random.randint(1, 800)
        if randbong == 1:
            await message.channel.send('BONG! Bongard problem #1:\n(http://oebp.org/incarnate.php?bp=1)')
            await message.channel.send(file=discord.File('bong1.png'))
        else:
            url = "http://oebp.org/incarnate.php?bp=" + str(randbong)
            page = requests.get(url, headers=headers)
            parser.feed(page.text)
            bong = str.encode(parser.img)
            if bong == blankBong:
                randbong = random.randint(1, 800)
                if randbong == 1:
                    await message.channel.send('BONG! Bongard problem #1:\n(http://oebp.org/incarnate.php?bp=1)')
                    await message.channel.send(file=discord.File('bong1.png'))
                else:
                    url = "http://oebp.org/incarnate.php?bp=" + str(randbong)
                    page = requests.get(url, headers=headers)
                    parser.feed(page.text)
                    bong = str.encode(parser.img)
                    base = base64.decodebytes(bong)
                    with open("bong.jpg", "wb") as f:
                        f.write(base)
                    await message.channel.send('BONG! Bongard problem #' + str(randbong) + ': \n(' + url + ')')
                    await message.channel.send(file=discord.File('bong.jpg'))
            else:
                base = base64.decodebytes(bong)
                with open("bong.jpg", "wb") as f:
                    f.write(base)
                await message.channel.send('BONG! Bongard problem #' + str(randbong) + ': \n(' + url + ')')
                await message.channel.send(file=discord.File('bong.jpg'))

    if message.content.startswith(')bong') or message.content.startswith(')b'):
        if len(message.content) != 5:
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
                if bong == blankBong:
                    await message.channel.send('Sorry, this Bongard problem does not exist yet! Please try another.')
                else:
                    await message.channel.send('BONG! Bongard problem #' + number + ': \n(' + url + ')')
                    await message.channel.send(file=discord.File('bong.jpg'))

    if message.content.startswith(')solution') or message.content.startswith(')sln') or message.content.startswith(
            ')s'):
        number = message.content.split()[1]
        url = "http://oebp.org/BP" + number
        page = requests.get(url, headers=headers)
        slnparse.feed(page.text)
        if slnparse.text is None:
            await message.channel.send('Sorry, this Bongard problem does not exist yet! Please try another.')
        else:
            await message.channel.send('BONG! Sent you the solution for problem #' + number + '.')
            await message.author.send('BONG! Solution for Bongard problem #' + number + ': ||' + slnparse.text + '||')

    if message.content.startswith(')ping'):
        ping = str(int(client.latency * 1000))
        await message.channel.send('BONG! Ping: ' + ping + ' milliseconds.')


client.run(token)
