import discord
from discord.ext import commands
import os
import json
import asyncio
from dotenv import load_dotenv

# 環境変数（.env）読み込み
load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("❌ TOKENが設定されていません")

# Intents設定（member関連のイベントを有効化）
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 退出ユーザー記録ファイル
RECORD_FILE = "left_members.json"

# 初期化：記録ファイルが存在しない場合は空で作成
if not os.path.exists(RECORD_FILE):
    with open(RECORD_FILE, "w") as f:
        json.dump({}, f)

# Bot起動時
@bot.event
async def on_ready():
    print(f"✅ Bot Logged in as {bot.user} (ID: {bot.user.id})")

# ユーザー退出時にIDを記録
@bot.event
async def on_member_remove(member):
    with open(RECORD_FILE, "r") as f:
        data = json.load(f)
    data[str(member.id)] = True
    with open(RECORD_FILE, "w") as f:
        json.dump(data, f)
    print(f"✏️ Recorded leave: {member.name} ({member.id})")

# ユーザー再参加時にロール再付与
@bot.event
async def on_member_join(member):
    print(f"🔄 {member.name} has joined.")
    with open(RECORD_FILE, "r") as f:
        data = json.load(f)

    if str(member.id) in data:
        print("👤 Rejoining member detected.")
        role = member.guild.get_role(1364560062579736668)  # ←ロールIDを確認・変更可
        if role:
            try:
                await member.add_roles(role)
                print("✅ Role added.")
            except Exception as e:
                print(f"❌ Failed to add role: {e}")
        else:
            print("⚠️ Role not found.")

        log_channel = bot.get_channel(1363185026006515828)  # ←ログチャンネルIDを確認・変更可
        if log_channel:
            try:
                # await log_channel.send(f"⚠️ {member.mention} が再参加しました（ロール付与）")  # 実行する場合はコメント解除
                print(f"📢 Would have sent message: ⚠️ {member.mention} が再参加しました（ロール付与）")
            except Exception as e:
                print(f"❌ Failed to send message: {e}")
        else:
            print("⚠️ Log channel not found.")

# こんにちはに反応する機能
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "こんにちは" in message.content:
        await asyncio.sleep(1)
        await message.channel.send("こんにちは！")
    await bot.process_commands(message)

# Bot起動
bot.run(TOKEN)

