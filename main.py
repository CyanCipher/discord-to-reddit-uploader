import os
import discord
from PIL import Image
import praw
import time
import cv2


reddit = praw.Reddit(
    user_agent="meme:0.1",
    client_id=os.environ['CLIENT'],
    client_secret=os.environ['SECRET'],
    username=os.environ['ID'],
    password=os.environ['PASS'],
)

def delete_file(file: str):
    if os.path.exists(f'memesaves/{file}'):
        os.remove(f'memesaves/{file}')
        print("Delete Success...")


def gen_nail(file: str):
    vidcap = cv2.VideoCapture(f'memesaves/{file}')
    success, image = vidcap.read()

    if success:
        cv2.imwrite('thumbnail.jpg', image)

image_types = ["png", "jpeg", "gif", "jpg"]
video_types = ["mp4", "mov"]

intents = discord.Intents.default()
client = discord.Client(intents = intents)

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message: discord.Message) -> None:

    if message.channel.id == 1037587618390614046:
        if "^ping" in message.content.lower():
            await message.channel.send(f"{message.author.mention} Zinda hu bhay...")
        
        if message.attachments:
            try:
                for attachment in message.attachments:
                    if any(attachment.filename.lower().endswith(image) for image in image_types):
                        try:
                            # 'attachments/{{attachment.filename}' is the PATH to where the attachmets/images will be saved. Example: home/you/Desktop/attachments/{{attachment.filename}
                            await attachment.save(f'memesaves/{attachment.filename}')
                            reddit.subreddit(os.environ['SUB']).submit_image(title=message.content, image_path=f'memesaves/{attachment.filename}')
                            delete_file(attachment.filename)
                        except FileNotFoundError:
                            image = Image.new('RGB', (100, 100))
                            image.save(f'memesaves/{attachment.filename}', "PNG")
                            await attachment.save(f'memesaves/{attachment.filename}')
                            reddit.subreddit(os.environ['SUB']).submit_image(title=message.content, image_path=f'memesaves/{attachment.filename}')
                            delete_file(attachment.filename)
                            await message.add_reaction('✅')
                        else:
                            await message.add_reaction('✅')

                    elif any(attachment.filename.lower().endswith(video) for video in video_types):
                        try:
                            await attachment.save(f'memesaves/{attachment.filename}')
                            gen_nail(attachment.filename)
                            reddit.subreddit(os.environ['SUB']).submit_video(title=message.content, video_path=f'memesaves/{attachment.filename}', thumbnail_path='./thumbnail.jpg')
                            delete_file(attachment.filename)
                        except FileNotFoundError:
                            image = Image.new('RGB', (100, 100))
                            image.save(f'memesaves/{attachment.filename}', "PNG")
                            # 'attachments/{{attachment.filename}' is the PATH to where the attachmets/images will be saved. Example: home/you/Desktop/attachments/{{attachment.filename}
                            await attachment.save(f'memesaves/{attachment.filename}')
                            reddit.subreddit(os.environ['SUB']).submit_video(title=message.conent, video_path=f'memesaves/{attachment.filename}', thumbnail_path='./thumbnail.jpg')
                            delete_file(attachment.filename)
                            await message.add_reaction('✅')
                        else:
                            await message.add_reaction('✅')
                    time.sleep(10)


            except:
                await message.add_reaction('❎')

client.run(os.environ['TOKEN'])
