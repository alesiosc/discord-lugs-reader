import os

import time

import json

import requests

import random

import re

from dotenv import load_dotenv

from datetime import datetime

# Load .env file, overriding system environment variables
load_dotenv(".env", override=True)

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
SNAPSHOT_FILE = "snapshot.txt"

def get_latest_messages():
    """Fetches the latest messages from the snapshot file."""
    print("Getting latest messages from snapshot.txt...")
    try:
        with open(SNAPSHOT_FILE, 'r') as f:
            snapshot_content = f.read()
        
        messages = []
        if snapshot_content:
            lines = snapshot_content.split('\n')
            for line in lines:
                if 'article' in line and 'LugsBot' in line:
                    try:
                        # Extract the message content between quotes
                        message_match = re.search(r'"([^"]*)"', line)
                        if message_match:
                            full_message = message_match.group(1)
                            # Extract the ticker info part from the message
                            ticker_match = re.search(r'\[([A-Z]+)\].*?Timestamp: ([^,]+), Mid: ([\d.]+), Lower: ([\d.]+), Upper: ([\d.]+)', full_message)
                            if ticker_match:
                                msg_type = ticker_match.group(1)
                                timestamp_str = ticker_match.group(2)
                                # Convert timestamp string to datetime object for proper sorting
                                dt_object = datetime.strptime(timestamp_str, "%m/%d/%Y %I:%M:%S %p")
                                mid = float(ticker_match.group(3))
                                lower = float(ticker_match.group(4))
                                upper = float(ticker_match.group(5))
                                # Reconstruct the message in the expected format
                                reconstructed_message = f"[{msg_type}] Timestamp: {timestamp_str}, Mid: {mid}, Lower: {lower}, Upper: {upper}"
                                messages.append({
                                    'message': reconstructed_message,
                                    'type': msg_type,
                                    'timestamp': dt_object
                                })
                    except Exception as e:
                        print(f"Error processing line: {line}, Error: {e}")
                        pass
        
        # Sort messages by timestamp (most recent first) and keep only the latest for each type
        if messages:
            # Sort by timestamp, descending (most recent first)
            messages.sort(key=lambda x: x['timestamp'], reverse=True)
            
            # Keep only the latest message for each ticker type (NQ, ES, YM)
            latest_messages = {}
            for msg in messages:
                msg_type = msg['type']
                if msg_type in ['NQ', 'ES', 'YM', 'CL', 'GC'] and msg_type not in latest_messages:
                    latest_messages[msg_type] = msg['message']
            
            # Return the latest messages as a list
            return list(latest_messages.values())
        else:
            return []
    except FileNotFoundError:
        print("snapshot.txt not found. Please wait for it to be created.")
        return []
    except Exception as e:
        print(f"An error occurred while getting messages: {e}")
        return []

def format_message(message):
    """Formats a message string into the desired format."""
    print(f"Formatting message: {message}")
    try:
        parts = message.split(",")
        msg_type = parts[0].split("]")[0].strip("[")
        timestamp_str = parts[0].split("Timestamp:")[1].strip()
        mid = float(parts[1].split(":")[1].strip())
        lower = float(parts[2].split(":")[1].strip())
        upper = float(parts[3].split(":")[1].strip())

        # Add randomization based on ticker type
        if msg_type in ["NQ", "YM", "RTY"]:  # Added RTY with ±3 range
            mid += random.uniform(-3, 3)
            lower += random.uniform(-3, 3)
            upper += random.uniform(-3, 3)
        elif msg_type == "ES":
            mid += random.uniform(-2, 2)
            lower += random.uniform(-2, 2)
            upper += random.uniform(-2, 2)
        elif msg_type == "CL":  # Added CL with ±0.5 range
            mid += random.uniform(-0.5, 0.5)
            lower += random.uniform(-0.5, 0.5)
            upper += random.uniform(-0.5, 0.5)
        elif msg_type == "GC":
            mid += random.uniform(-0.5, 0.5)
            lower += random.uniform(-0.5, 0.5)
            upper += random.uniform(-0.5, 0.5)

        # Convert timestamp
        dt_object = datetime.strptime(timestamp_str, "%m/%d/%Y %I:%M:%S %p")
        formatted_timestamp = dt_object.strftime("%Y-%m-%d %H:%M:%S EDT")

        return f"[{msg_type}] Time: {formatted_timestamp} | Mid: {mid:.2f}, Lower: {lower:.2f}, Upper: {upper:.2f}"
    except Exception as e:
        print(f"Error formatting message: {e}")
        return None

def send_to_discord(message):
    """Sends a message to the Discord webhook."""
    print(f"Sending message to Discord: {message}")
    if not WEBHOOK_URL:
        print("WEBHOOK_URL not set. Cannot send message.")
        return

    data = {"content": message}
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        response.raise_for_status() # Raise an exception for bad status codes
        print("Message sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Discord: {e}")

def load_processed_messages():
    """Load processed messages from file to persist across restarts."""
    try:
        with open('processed_messages.json', 'r') as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_processed_messages(processed_keys):
    """Save processed messages to file."""
    with open('processed_messages.json', 'w') as f:
        json.dump(list(processed_keys), f)

def main():
    """Main monitoring loop."""
    # Load previously processed messages to avoid duplicates across restarts
    processed_message_keys = load_processed_messages()
    print(f"Loaded {len(processed_message_keys)} previously processed messages")

    # Allow disabling dedup via env for testing
    disable_dedup = os.getenv("DISABLE_DEDUP", "false").lower() == "true"
    print(f"Deduplication disabled: {disable_dedup}")

    while True:
        print("\n--- Checking for new messages ---")
        messages = get_latest_messages()
        new_messages_found = False

        if not messages:
            print("No messages found.")
        else:
            for message in messages:
                try:
                    # Only consider NQ/ES/YM per requirements
                    if not any(s in message for s in ["[NQ]", "[ES]", "[YM]", "[CL]", "[GC]"]):
                        continue

                    # Extract ticker type and timestamp from message
                    msg_type_match = re.search(r'\[([A-Z]+)\]', message)
                    timestamp_match = re.search(r'Timestamp: ([^,]+)', message)

                    if disable_dedup:
                        # Send regardless of prior state
                        formatted_message = format_message(message)
                        if formatted_message:
                            send_to_discord(formatted_message)
                            new_messages_found = True
                        continue

                    if msg_type_match and timestamp_match:
                        msg_type = msg_type_match.group(1)
                        timestamp_str = timestamp_match.group(1)
                        message_key = f"{msg_type}_{timestamp_str}"

                        if message_key not in processed_message_keys:
                            new_messages_found = True
                            print(f"New message found: {message}")
                            formatted_message = format_message(message)
                            if formatted_message:
                                send_to_discord(formatted_message)
                                # Only add to processed if successfully sent
                                processed_message_keys.add(message_key)
                                save_processed_messages(processed_message_keys)
                        else:
                            print(f"Message already processed: {message}")
                    else:
                        # Fallback to using the entire message as key
                        if message not in processed_message_keys:
                            new_messages_found = True
                            print(f"New message found: {message}")
                            formatted_message = format_message(message)
                            if formatted_message:
                                send_to_discord(formatted_message)
                                # Only add to processed if successfully sent
                                processed_message_keys.add(message)
                                save_processed_messages(processed_message_keys)
                        else:
                            print(f"Message already processed: {message}")
                except Exception as e:
                    print(f"Error processing message: {e}")
        
        if not new_messages_found:
            print("No new messages.")

        # Wait for 60 seconds before checking again
        print("Waiting for 60 seconds...")
        time.sleep(60)

if __name__ == "__main__":
    main()