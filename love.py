import pyttsx3

text = """
It is a quiet Thursday morning in June. The sun is just peeking over the horizon as five brave heroes, known as Joeri, Vasilis, Joris, Mehmet, and Jan-Willem, enter their battleground: the classroom of Bjorn Lecis. Their mission? To complete an epic final project that will go down in the annals of programming history. Their weapon? Python. Their enemy? Bugs. Lots of bugs.

Joeri, affectionately called "The Joeerri" by his friends, programmed the vending module, a management system for vending machines. With his brilliant but chaotic mind, he always comes up with the most ingenious solutions, which often cause the most bizarre bugs. His favorite saying, "It works on my machine!" has become legendary. His motto: "A bug is just an unexpected feature."

Vasilis, known as "Mr. Feta" for his love of Greek cheese, programmed the restaurant module. With his sharp eye and determination, he ensures everything is flawless. Whenever there was an error in the code, his standard response was, "Have you tried it with more feta?" His secret ingredient in coding: "Feta makes everything betta."

Joris, also known as "Mr. Duvel," is the party animal of the group and responsible for data management. His code reviews are often conducted with a glass of his favorite beer in hand. Despite his relaxed demeanor, he is a master at debugging. "Why doesn't this code work?" Joeri once asked in despair. "Because you're sober," Joris replied dryly. His favorite database query: "SELECT * FROM beers WHERE mood = 'happy';"

Mehmet, better known as "Dostum" (which means "friend" in Turkish), programmed the inventory management module. With his calm and patient nature, he resolves conflicts as if they were nothing. His motto: "Code is like kebab; the better you wrap it, the tastier it is." And believe us, he was right. His favorite command: "pip install friendship."

And then there's Jan-Willem, who has the honor of being called "The Bald One." Despite his lack of hair, he is blessed with an abundance of programming knowledge. He programmed the login and user management system. His bald head radiates a kind of wisdom that can only be gained from countless hours of writing SQL. His favorite Python function? "def bald_eagle(): return wisdom"

Together, these five warriors wrote an ERP software package that can handle everything, from inventory management to customer relations. The project was a true test of their skills and friendship. The bugs were numerous, the nights long, and the coffee supply always low. But with the support of each other and a constant stream of pizzas, they managed to pull it off.

And then there is, of course, Bjorn Lecis, the indispensable mentor and teacher. He was the Gandalf to their Fellowship, always ready with wise advice and sometimes with a warning: "Guys, this isn't wizardry, it's a programming language!" With his patience and humor, he guided them through the toughest moments. Every time the group thought they had reached the end of their rope, Bjorn was there to lift their spirits with his legendary anecdotes about his own coding adventures. His favorite Python joke: "Why is Python like a beer tap? It has many kegs (and few bugs)!"

And so, with their project completed and their friendship strengthened, these five heroes are ready to conquer the world with their ERP software package. Whether they will ever become famous, no one knows. But one thing is certain: they will always cherish the memories of the time when "The Joeerri," "Mr. Feta," "Mr. Duvel," "Dostum," and "The Bald One" worked together under the wise guidance of Bjorn Lecis. Their story will live on, not only in their code but also in the hearts of those who were lucky enough to witness it.
"""

# Initialize the TTS engine
engine = pyttsx3.init()

# Get available voices and try to set a deep, authoritative English voice
voices = engine.getProperty('voices')
voice_set = False

for voice in voices:
    if 'english' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        voice_set = True
        break

if not voice_set:
    print("No English voice found! Ensure that your TTS engine supports English voices.")

# Set speaking rate and pitch to emulate a deeper, slower tone
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 70)  # Slow down the rate for clarity

# Emulate a deeper voice by adjusting volume and pitch if possible
volume = engine.getProperty('volume')
engine.setProperty('volume', volume + 0.1)  # Increase volume slightly

# Read the text
engine.say(text)
engine.runAndWait()