import discord
from discord import app_commands
from discord.ext import commands
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        logging.info(f"✅ Synced {len(synced)} slash commands")
    except Exception as e:
        logging.error(e)
    logging.info(f"🤖 Logged in as {bot.user} (Admin & Owner Bot Active)")

# ==================== أوامر الإدارة الشاملة (Slash Commands) ====================

@bot.tree.command(name="ban", description="🔨 طرد وحظر عضو من السيرفر نهائياً")
@app_commands.describe(member="العضو المراد حظره", reason="سبب الحظر")
@app_commands.checks.has_permissions(ban_members=True)
async def ban_member(interaction: discord.Interaction, member: discord.Member, reason: str = "لم يتم ذكر السبب"):
    await member.ban(reason=reason)
    await interaction.response.send_message(f"✅ تم حظر العضو {member.mention} بنجاح. السبب: {reason}", ephemeral=True)

@bot.tree.command(name="kick", description="👢 طرد عضو من السيرفر")
@app_commands.describe(member="العضو المراد طرده", reason="سبب الطرد")
@app_commands.checks.has_permissions(kick_members=True)
async def kick_member(interaction: discord.Interaction, member: discord.Member, reason: str = "لم يتم ذكر السبب"):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"✅ تم طرد العضو {member.mention} بنجاح. السبب: {reason}", ephemeral=True)

@bot.tree.command(name="mute", description="🔇 إسكات (كتم) عضو في السيرفر")
@app_commands.describe(member="العضو المراد كتمه", minutes="مدة الكتم بالدقائق")
@app_commands.checks.has_permissions(moderate_members=True)
async def mute_member(interaction: discord.Interaction, member: discord.Member, minutes: int):
    from datetime import timedelta
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason="إسكات إداري")
    await interaction.response.send_message(f"🔇 تم كتم العضو {member.mention} لمدة {minutes} دقيقة.", ephemeral=True)

@bot.tree.command(name="unmute", description="🔊 إزالة الكتم عن عضو")
@app_commands.describe(member="العضو المراد رفع الكتم عنه")
@app_commands.checks.has_permissions(moderate_members=True)
async def unmute_member(interaction: discord.Interaction, member: discord.Member):
    await member.timeout(None, reason="رفع الكتم")
    await interaction.response.send_message(f"🔊 تم رفع الكتم عن العضو {member.mention}.", ephemeral=True)

@bot.tree.command(name="give_role", description="👑 إعطاء رتبة لعضو")
@app_commands.describe(member="العضو المستهدف", role="الرتبة المراد إعطاؤها")
@app_commands.checks.has_permissions(manage_roles=True)
async def give_role(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await interaction.response.send_message(f"✅ تم منح الرتبة {role.mention} للعضو {member.mention}.", ephemeral=True)

@bot.tree.command(name="remove_role", description="⚠️ سحب رتبة من عضو")
@app_commands.describe(member="العضو المستهدف", role="الرتبة المراد سحبها")
@app_commands.checks.has_permissions(manage_roles=True)
async def remove_role(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await interaction.response.send_message(f"⚠️ تم سحب الرتبة {role.mention} من العضو {member.mention}.", ephemeral=True)

@bot.tree.command(name="clear", description="🗑️ مسح عدد محدد من الرسائل في الشات")
@app_commands.describe(amount="عدد الرسائل المراد حذفها")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear_messages(interaction: discord.Interaction, amount: int):
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"🗑️ تم مسح `{len(deleted)}` رسالة بنجاح.", ephemeral=True)

@bot.tree.command(name="say", description="📢 جعل البوت يرسل رسالة رسمية في الشات")
@app_commands.describe(text="النص المراد إرساله")
@app_commands.checks.has_permissions(administrator=True)
async def say_message(interaction: discord.Interaction, text: str):
    await interaction.response.send_message("✅ تم إرسال الرسالة.", ephemeral=True)
    await interaction.channel.send(text)

# معالجة أخطاء الصلاحيات
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("❌ ليس لديك الصلاحيات الكافية لاستخدام هذا الأمر الإداري!", ephemeral=True)
    else:
        logging.error(error)


