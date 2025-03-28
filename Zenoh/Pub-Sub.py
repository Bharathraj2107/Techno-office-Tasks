import zenoh
import time

# Publisher
def publisher():
    session = zenoh.open()
    pub = session.declare_publisher("demo/topic")
    
    for i in range(5):
        msg = f"Hello Zenoh #{i}"
        pub.put(msg)
        print(f"Published: {msg}")
        time.sleep(1)
    
    session.close()

# Subscriber
def subscriber():
    def listener(sample):
        print(f"Received: {sample.payload.decode('utf-8')}")

    session = zenoh.open()
    sub = session.declare_subscriber("demo/topic", listener)
    
    print("Waiting for messages... (Ctrl+C to exit)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sub.undeclare()
        session.close()

# Run either publisher() or subscriber() in separate terminals