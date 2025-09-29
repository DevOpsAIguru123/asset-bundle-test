import os

def main():
    # Get the environment message from environment variable
    # This will be set by the Databricks job configuration
    environment_message = os.getenv('ENVIRONMENT_MESSAGE', 'Hello World Default')
    print(environment_message)

if __name__ == "__main__":
    main()