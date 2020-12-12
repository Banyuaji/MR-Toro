import asyncio
import discord
import youtube_dl
from discord.ext import commands, tasks
from random import choice

youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '192.168.43.39' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


TOKEN = "NzYzMjg5NTUxODc0NTU1OTE0.X31iyg.PqkHHMoLuQlv8g-GGu5QwZXgnSw"
client = commands.Bot(command_prefix='_')

status = ["Dengerin lagu","Tidur..."]

@client.event
async def on_ready():
    change_status.start()
    print(f"{client.user} was Awoken!")

@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Game(status[1]))

@client.command(name='ping',help='buat cek latency')
async def ping(ctx):
    await ctx.send(f'Latency {round(client.latency * 1000)}ms')

@client.command(name='play',help='masuk vc + jalanin lagu')
async def play(ctx, url):
    if not ctx.message.author.voice:
        await ctx.send('You are not connected to voice channel')
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()
    server = ctx.message.guild
    voice_channel = server.voice_client
    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=client.loop)
        voice_channel.play(player, after=lambda e: print('Player error : %s' %e) if e else None)
    await ctx.send(f'**Now playing:** {player.title}')
    await client.change_presence(activity=discord.Game(status[0]))

@client.command(name='stop',help='berentiin lagu + keluar vc')
async def play(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()

@client.command(name='mon',help='manggil si paimon')
async def mon(ctx):
    await ctx.send("kenape?")

@client.command(name='ehhe',help='???')
async def ehhe(ctx):
    await ctx.send("Ehhe, te Nandayo!")

@client.command(name='vicon',help='buat vicon')
async def vicon(ctx):
    await ctx.send("wey bangun ada vicon nih")
    await ctx.send("<@&753510631503691827> <@&754745050537132064>")
    await ctx.send("`Pesan dari bot bukan dari orang`")

@client.command(name='csgo',help='manggil org yg punya role csgo')
async def csgo(ctx):
    a = ctx.message.author.id
    await ctx.send("wey ngumpul, dipanggil nih sama <@!%a> CS:GO kg?" % a)
    await ctx.send("<@&769037011318997014>")
    await ctx.send("`makasih!`")

@client.command(name='brawlhalla',help='manggil org yg punya role brawlhalla')
async def b(ctx):
    a = ctx.message.author.id
    await ctx.send("Brawlhallers, dipanggil nih sama <@!%a> Brawlhalla kg?"%a)
    await ctx.send("<@&769104797759569940>")
    await ctx.send("`makasih!`")

@client.command(name='l4d2',help='manggil org yg punya role l4d2')
async def l(ctx):
    a = ctx.message.author.id
    await ctx.send("Gabut... dipanggil nih sama <@!%a> Left 4 Dead 2 kg?"%a)
    await ctx.send("<@&769104801844822046>")
    await ctx.send("`makasih!`")

@client.command(name='valorant',help='manggil org yg punya role valorant')
async def v(ctx):
    a = ctx.message.author.id
    await ctx.send("wey ngumpul, dipanggil nih sama <@!%a> Valorant kg?" % a)
    await ctx.send("<@&769117967354953730>")
    await ctx.send("`makasih!`")

@client.command(name='genshin',help='manggil org yg punya role genshin')
async def g(ctx):
    a = ctx.message.author.id
    await ctx.channel.send("kawan2 temanmu butuh bantuan nih <@!%a>, Genshin-impact yuk?" % a)
    await ctx.channel.send("<@&769410013562798120>")
    await ctx.channel.send("`makasih!`")

@client.command(name='here', help='ngasih tau lg di vc mana')
async  def h(ctx):
    if not ctx.message.author.voice:
        await ctx.send('You are not connected to voice channel')
        return
    else:
        channel = ctx.message.author.voice.channel
        a = ctx.message.author.id
        await ctx.channel.send(f"<@!{a}>, ada di voice channel ini {channel}")

client.run(TOKEN)