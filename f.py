import random
import nexmo
import os
import time
import requests

# Hardcoded API keys
NEXMO_API_KEY = "2c385cd0"
NEXMO_API_SECRET = "xbWRmgqYjR61N0AO"

# Check if the specified text is present on the pastebin page
pastebin_url = "https://pastebin.com/YQFXtrQA"
response = requests.get(pastebin_url)

if response.status_code != 200 or "B4ssl1n3rXSSB4ssl1n3rXSS" not in response.text:
    print("Pastebin content not accessible or specified text not found. Stopping the script.")
    exit()

# Read sender IDs from sender_ids.txt
sender_ids = ["sender_id_1", "sender_id_2"]  # Replace with actual sender IDs

# Read recipient numbers from numbers.txt
with open("numbers.txt", "r") as file:
    recipient_numbers = [line.strip() for line in file.readlines()]

# Initialize Nexmo client
client = nexmo.Client(key=NEXMO_API_KEY, secret=NEXMO_API_SECRET)

# Welcome message
print("Welcome to the ULTIMATE SMART Bulk SMS Sender")
print("With Random Words Replacement to stop cell providers fingerprinting your messages and blocking the route.")
print("If EVERY message is UNIQUE, it can't be Blocked!")
print("\n\n\n\n\n\nCustom coded by Crypt0")
add_stop = input("Would you like to add a stop message? (Y/N): ")

# Sample message using all randomizations
sample_message = """
Hello [RANDOM 1]!

You've been selected to receive our special offer. Click [URL] to claim now.
Use reference code: [Ref]

This is a sample message to showcase different randomizations:
- [RANDOM 1]: A random word will be selected from the list of words in random1.txt and replace [ RANDOM 1] in the message body
- [RANDOM 2]: A random word will be selected from the list of words in random1.txt and replace [ RANDOM 1] in the message body
- [RANDOM 3]: A random word will be selected from the list of words in random1.txt and replace [ RANDOM 1] in the message body
- [RANDOM 4]: A random word will be selected from the list of words in random1.txt and replace [ RANDOM 1] in the message body
- [RANDOM 5]: A random word will be selected from the list of words in random1.txt and replace [ RANDOM 1] in the message body
- [URL]: A random URL.
- [COMPANY]: A random word from the companies list will be replaced in the message body (For example BANCO SANTANDER)
- [Ref]: A random reference code will be added to the message (ALL WAYS USE this as it helps with the ranomization of the messages not getting finger printed)
"""

# Explanation of available random words
random_words_explanation = """
Available Random Words:
[RANDOM 1]: The [RANDOM 1] tag will be replaced with a random word from random1.txt.
for example:
- Paypal
- paypal
- [paypal]
- {paypal}
"""

# Display explanations
print("\nExplanation of Randomizations:")
print("[RANDOM 1]: This tag will be replaced with a random word from a list of words in random1.txt.")
print("[URL]: This tag will be replaced with a random URL.")
print("[Ref]: This tag will be replaced with a random reference code.")
print("\nSample Message with Randomizations:")
print(sample_message)
print("\n" + random_words_explanation)

# User input for number of message bodies
num_message_bodies = int(input("How many message bodies would you like to use? (1/2/3): "))

# User input for message bodies
message_bodies = []
for i in range(num_message_bodies):
    message = input(f"Enter message body {i + 1}: ")
    message_bodies.append(message)

def replace_random_tags(message):
    for i in range(1, num_message_bodies + 1):
        random_tag = f"[RANDOM {i}]"
        if random_tag in message:
            with open(f"random{i}.txt", "r") as file:
                random_words = [line.strip() for line in file.readlines()]
            random_word = random.choice(random_words)
            message = message.replace(random_tag, random_word)
    if "[URL]" in message:
        with open("URL.txt", "r") as file:
            urls = [line.strip() for line in file.readlines()]
        random_url = random.choice(urls)
        message = message.replace("[URL]", random_url)
    if "[Ref]" in message:
        with open("ref.txt", "r") as file:
            refs = [line.strip() for line in file.readlines()]
        random_ref = random.choice(refs)
        message = message.replace("[Ref]", random_ref)
    return message

# Sending bulk SMS with rotating user message and random pause
message_count = 0
for recipient_number in recipient_numbers:
    sender_id = random.choice(sender_ids)
    user_message = random.choice(message_bodies)
    user_message = replace_random_tags(user_message)  # Replace random tags
    
    sms = nexmo.Sms(client)

    response = sms.send_message({
        'from': sender_id,
        'to': recipient_number,
        'text': user_message
    })

    message_count += 1
    
    if message_count % 500 == 0:
        print("500 messages sent. Consider changing sender IDs if not using random ones.")
        print("You have 20 seconds to add new sender IDs to the sender_ids list.")
        time.sleep(20)  # Pause for 20 seconds
        
        continue_prompt = input("Continue from where you left off? (Y/N): ")
        if continue_prompt.lower() != 'y':
            print("Exiting.")
            break
    
    if response['messages'][0]['status'] == '0':
        print(f"Message sent successfully to {recipient_number} from {sender_id}")
    else:
        print(f"Message failed to send to {recipient_number} from {sender_id}. Error: {response['messages'][0]['error-text']}")
    
    # Add a random pause between 1 and 5 seconds
    pause_duration = random.uniform(1, 5)
    time.sleep(pause_duration)
