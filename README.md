# YouTube Video Fetcher

This project fetches all videos from a specified YouTube channel and saves the details to an Excel file. It uses the YouTube Data API v3 and is managed using Poetry.

## Features

- Fetches all videos from a specified YouTube channel.
- Retrieves video details including title, short link, duration, and upload date.
- Saves the video details to an Excel file.

## Requirements

- Python 3.7+
- Poetry for dependency management
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) for authentication and token management

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/youtube-video-fetcher.git
    cd youtube-video-fetcher
    ```

2. Install dependencies using Poetry:
    ```sh
    poetry install
    ```

3. Set up your environment variables:
    - `CREDENTIALS_PATH`: Path to your Google API credentials JSON file.
    - `TOKEN_PATH`: Path to store the token file.
    - `YOUTUBE_CHANNEL_ID`: The ID of the YouTube channel you want to fetch videos from.

    You can set these variables in a `.env` file or export them in your shell:
    ```sh
    export CREDENTIALS_PATH=/path/to/credentials.json
    export TOKEN_PATH=/path/to/token.json
    export YOUTUBE_CHANNEL_ID=YOUR_CHANNEL_ID
    ```

## Usage

1. Run the script:
    ```sh
    poetry run python youtube_api/main.py
    ```

2. The script will authenticate using the provided credentials, fetch all videos from the specified channel, and save the details to `youtube_videos.xlsx`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.