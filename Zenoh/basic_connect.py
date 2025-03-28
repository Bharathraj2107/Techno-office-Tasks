import zenoh

def main():
    # Create a default configuration
    config = zenoh.Config()#Creates a new Zenoh configuration object using the Config() class from the zenoh module.
    
    # Open a Zenoh session
    session = zenoh.open(config)#Establishes a connection to the Zenoh network using the configuration we created.zenoh.open() is the main entry point to create a session.The session object (session) is your handle to interact with the Zenoh network:
    
    print("Successfully connected to Zenoh!")
    
    # Close the session
    session.close()

if __name__ == "__main__":
    main()