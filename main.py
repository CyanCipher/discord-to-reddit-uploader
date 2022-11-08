import discord
from discord.ext import commands
from PIL import Image
import ids
import praw
from praw.models import InlineImage
import os
import time


reddit = praw.Reddit(
    user_agent="meme:0.1",
    client_id=ids.CLIENT,
    client_secret=ids.SECRET,
    username=ids.ID,
    password=ids.PASS,
)


def imgsubmit(image: str, title: str):
    media = f"memesaves/{image}"

    subreddit = reddit.subreddit(ids.SUB)

    print("submitting post on reddit...")

    try:
        post = subreddit.submit_image(title, image_path=media)
        print("post submitted...")

    except error as e:
        print(e)


    if os.path.exists(f"memesaves/{image}"):
        os.remove(f"memesaves/{image}")  # one file at a time
        print("deleted file sucessfully...")

    return str(post.shortlink)


def vidsubmit(video: str, title: str):
    media = f"memesaves/{video}"

    subreddit = reddit.subreddit(ids.SUB)

    print("submitting post on reddit...")

    subreddit.submit_video(title, video_path=media)
    print("post submitted...")


    if os.path.exists(f"memesaves/{video}"):
        os.remove(f"memesaves/{video}")  # one file at a time
        print("deleted file sucessfully...")


# You can add more attachments/formats here to be saved.
image_types = ["png", "jpeg", "gif", "jpg"]
video_types = ["mp4", "mov"]
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message: discord.Message) -> None:

    if message.channel.id == 1037587618390614046:
        if message.content.startswith('^'):
            if "ping" in message.content.lower():
                await message.channel.send(f"{message.author.mention} Zinda hu bhay...")
                print("working...")
        
        if message.attachments:
            try:
                for attachment in message.attachments:
                    if any(attachment.filename.lower().endswith(image) for image in image_types):
                        try:
                            # 'attachments/{{attachment.filename}' is the PATH to where the attachmets/images will be saved. Example: home/you/Desktop/attachments/{{attachment.filename}
                            await attachment.save(f'memesaves/{attachment.filename}')
                            postlink = imgsubmit(image=str(attachment.filename),
                                    title=str(message.content))
                        except FileNotFoundError:
                            image = Image.new('RGB', (100, 100))
                            image.save(f'memesaves/{attachment.filename}', "PNG")
                            # 'attachments/{{attachment.filename}' is the PATH to where the attachmets/images will be saved. Example: home/you/Desktop/attachments/{{attachment.filename}
                            await attachment.save(f'memesaves/{attachment.filename}')
                            postlink = imgsubmit(image=str(attachment.filename),
                                    title=str(message.content))
                            print("Saved new file")
                            await message.add_reaction('✅')
                        else:
                            print("sucessful")
                            await message.add_reaction('✅')

                    elif any(attachment.filename.lower().endswith(video) for video in video_types):
                        try:
                            await attachment.save(f'memesaves/{attachment.filename}')
                            vidsubmit(video=str(attachment.filename),
                                    title=str(message.content))
                        except FileNotFoundError:
                            image = Image.new('RGB', (100, 100))
                            image.save(f'memesaves/{attachment.filename}', "PNG")
                            # 'attachments/{{attachment.filename}' is the PATH to where the attachmets/images will be saved. Example: home/you/Desktop/attachments/{{attachment.filename}
                            await attachment.save(f'memesaves/{attachment.filename}')
                            vidsubmit(video=str(attachment.filename),
                                    title=str(message.content))
                            print("Saved new file")
                            await message.add_reaction('✅')
                        else:
                            print("sucessful")
                            await message.add_reaction('✅')
                    time.sleep(10)
            
            except:
                await message.add_reaction('❎')

client.run(ids.TOKEN)

