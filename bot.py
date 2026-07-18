import os
import discord
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configurações
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Cliente DeepSeek (compatível com OpenAI)
client_ai = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

intents = discord.Intents.default()
intents.message_content = True  # Necessário para ler mensagens

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'🤖 Bot conectado como {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Evita loop infinito
    
    # Verifica se o bot foi mencionado
    if bot.user in message.mentions:
        # Remove a menção do conteúdo da mensagem
        user_message = message.content.replace(f'<@{bot.user.id}>', '').replace(f'<@!{bot.user.id}>', '').strip()
        
        if not user_message:
            user_message = "Oi! Como posso te ajudar hoje?"  # Mensagem padrão se só mencionar
        
        try:
            # Chama a DeepSeek
            response = client_ai.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "Você é uma assistente mulher, porém fala muito palavrão. Responda sempre em até 400 caracteres."},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=150,
                temperature=0.7,
            )
            
            ai_reply = response.choices[0].message.content.strip()
            
            # Garante limite de 200 caracteres
            if len(ai_reply) > 200:
                ai_reply = ai_reply[:197] + "..."
            
            await message.reply(ai_reply)
            
        except Exception as e:
            print(f"Erro: {e}")
            await message.reply("Desculpa, tive um probleminha agora... Tenta de novo!")

bot.run(DISCORD_TOKEN)

