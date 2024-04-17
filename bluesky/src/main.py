from service.bluesky.client import BlueSkyClient
import os

def main():
    email = os.environ["LOGIN_EMAIL"]
    password = os.environ["LOGIN_PASSWORD"]

    images = ["https://www.beex-inc.com/media/QISDiddoYpbRyikytAgb57CxEmFFzQa0VWeIrkDX.png", "https://www.beex-inc.com/media/QISDiddoYpbRyikytAgb57CxEmFFzQa0VWeIrkDX.png"]

    client = BlueSkyClient(email, password)
    client.post_image(
        images,
        "AWS is super good"
    )


if __name__ == "__main__":
    main()