import zenoh  # Import Zenoh library
import time   # Import time for delays

# Main publisher function
def publisher():
    # Create a default Zenoh configuration
    config = zenoh.Config()
    
    # Open a Zenoh session
    session = zenoh.open(config)
    
    # Declare a publisher for the topic "demo/topic"
    pub = session.declare_publisher("demo/topic")
    
    # Publish 5 messages with a 1-second delay
    for i in range(5):
        msg = f"Hello Zenoh #{i}"
        # Encode the string as bytes before sending
        pub.put(msg.encode('utf-8'))
        print(f"Published: {msg}")
        time.sleep(1)  # Wait 1 second between messages
    
    # Close the session when done
    session.close()

# Execute publisher when script is run directly
if __name__ == "__main__":
    publisher()

# pub.put(msg.encode('utf-8'))

# Zenoh expects binary data, so we encode the string as UTF-8 bytes.

# The subscriber will decode it back to a string.

# session.declare_publisher()

# Registers this script as a publisher for "demo/topic".

# time.sleep(1)

# Adds a delay to avoid flooding the network.    