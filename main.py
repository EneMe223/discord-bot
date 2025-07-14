import discord
from discord.ext import commands
import json
import os


# Discord Bot のトークンを環境変数から取得
TOKEN = os.getenv("TOKEN")

# Botの設定
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# 退出ユーザー記録ファイル
RECORD_FILE = "left_members.json"

# 初期化：退出ユーザー記録ファイルを作成（なければ）
if not os.path.exists(RECORD_FILE):
    with open(RECORD_FILE, "w") as f:
        json.dump({}, f)

# Botが起動したときの処理
@bot.event
async def on_ready():
    print(f"✅ Bot Logged in as {bot.user}!")

# ユーザーが退出したときにIDを記録
@bot.event
async def on_member_remove(member):
    with open(RECORD_FILE, "r") as f:
        data = json.load(f)
    data[str(member.id)] = True
    with open(RECORD_FILE, "w") as f:
        json.dump(data, f)

# 再参加時の処理：記録があればロールを再付与＋通知
@bot.event
async def on_member_join(member):
    print(f"🔄 {member.name} has joined.")
    with open(RECORD_FILE, "r") as f:
        data = json.load(f)

    if str(member.id) in data:
        print("👤 Rejoining member detected.")
        role = member.guild.get_role(1364560062579736668)
        if role:
            try:
                await member.add_roles(role)
                print("✅ Role added.")
            except Exception as e:
                print(f"❌ Failed to add role: {e}")
        else:
            print("⚠️ Role not found.")

        log_channel = bot.get_channel(1363185026006515828)
        if log_channel:
            try:
                await log_channel.send(f"⚠️ {member.mention} が再参加しました（ロール付与）")
                print("📢 Message sent.")
            except Exception as e:
                print(f"❌ Failed to send message: {e}")
        else:
            print("⚠️ Log channel not found.")

# 「こんにちは」に反応するシンプルなメッセージ機能（エラーハンドリング付き）
@bot.event
async def on_message(message):
    try:
        print(f"[DEBUG] message from {message.author}: {message.content}")

        if message.author == bot.user:
            return

        if "こんにちは" in message.content:
            await message.channel.send("こんにちは！")

        await bot.process_commands(message)

    except Exception as e:
        print(f"❌ Error in on_message: {e}")


# Bot起動
bot.run(TOKEN)
