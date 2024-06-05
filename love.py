import pyttsx3

text = """
On a quiet June morning, five heroes—Joeri, Vasilis, Joris, Mehmet, and Jan-Willem—embark on a mission in Bjorn Lecis's classroom: to complete an epic final project using Python. Joeri, "The Joeerri," programmed the vending module, known for his ingenious but buggy solutions. Vasilis, "Mr. Feta," ensured flawless coding with his love for Greek cheese. Joris, "Mr. Duvel," excelled at debugging, often with a beer in hand. Mehmet, "Dostum," brought calm to conflict resolution, likening code to kebab wrapping. Jan-Willem, "The Bald One," led user management with his abundant programming wisdom. Under Bjorn Lecis's guidance, they overcame bugs and late nights to create an ERP software package. Their story, filled with humor and camaraderie, will be remembered beyond their code."""

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