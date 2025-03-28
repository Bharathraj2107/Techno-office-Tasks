import zenoh  # Import the Zenoh library
import time   # Import time module for sleep functionality

# Define the message handler function
def listener(sample):
    # Convert Zenoh's ZBytes payload to Python bytes, then decode as UTF-8 string
    print(f"Received: {bytes(sample.payload).decode('utf-8')}")

# Main subscriber function
def subscriber():
    # Create a default Zenoh configuration
    config = zenoh.Config()
    
    # Open a Zenoh session with the config
    session = zenoh.open(config)
    
    # Declare a subscriber for the topic "demo/topic" and attach the listener
    sub = session.declare_subscriber("demo/topic", listener)
    
    # Keep the subscriber running until Ctrl+C is pressed
    print("Waiting for messages... (Ctrl+C to exit)")
    try:
        while True:
            time.sleep(1)  # Prevent CPU overuse
    except KeyboardInterrupt:  # Handle Ctrl+C
        sub.undeclare()  # Clean up the subscriber
        session.close()  # Close the session gracefully

# Execute the subscriber when the script is run directly
if __name__ == "__main__":
    subscriber()


# Key Points:

# 1)listener(sample)

# Called every time a message is received.

# sample.payload is in ZBytes format (Zenoh's binary data type).

# bytes(sample.payload).decode('utf-8') converts it to a readable string.

# 2)zenoh.Config()

# Creates a default configuration (auto-discovers peers on the local network).

# 3) session.declare_subscriber()

# Subscribes to "demo/topic" and calls listener when a message arrives.

# 4) KeyboardInterrupt Handling

# Ensures resources are freed before exiting.