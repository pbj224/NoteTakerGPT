# NoteTakerGPT

NoteTakerGPT is a script designed to transcribe and summarize audio recordings, specifically tailored for meetings. The core idea behind NoteTakerGPT is to transform the cumbersome task of note-taking into an automated process by utilizing the remarkable capabilities of OpenAI's GPT-4 model. 

This script is a perfect companion for professionals who frequently attend meetings and need a reliable tool to capture the key details. It saves time, increases productivity, and ensures that no important information is lost or overlooked. The output of the script is a well-structured, comprehensive set of bullet-point notes that provide a clear summary of the meeting.

NoteTakerGPT combines the power of several Python libraries and the OpenAI API to handle audio recording, transcription, text chunking, and summarization. It performs all these tasks in real-time, ensuring that the notes are ready shortly after a meeting ends. Furthermore, NoteTakerGPT handles the entire process in a way that maintains the privacy and security of your data. It's a robust and versatile tool that simplifies the note-taking process.

## Table of Contents

- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [How it Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

These instructions will guide you on how to get the project up and running on your local machine for development and testing purposes. 

### Prerequisites 

The project has a few dependencies that need to be installed for it to work correctly. The dependencies include:

- requests
- openai
- traceback
- pandas
- numpy
- tiktoken
- pyaudio
- wave
- keyboard
- time
- threading
- multiprocessing
- os

You can install these dependencies using pip:

```shell
pip install requests openai pandas numpy tiktoken pyaudio wave keyboard
```

## Installation

1. Clone the repository to your local machine:

```shell
git clone https://github.com/yourusername/NoteTakerGPT.git
```

2. Navigate into the cloned repository:

```shell
cd NoteTakerGPT
```

3. Install the prerequisites:

```shell
pip install -r requirements.txt
```

4. Run the script:

```shell
python NoteTakerGPT.py
```

## Usage

To use NoteTakerGPT, follow these steps:

1. Run the script:
```shell
python NoteTakerGPT.py
```

2. The script will automatically start recording and transcribing audio. The transcription and summarization process will continue until a KeyboardInterrupt event occurs (typically by pressing Ctrl+C).

3. At the end of the transcription and summarization process, the script will output a comprehensive set of bullet point notes derived from the recorded audio.

## How it Works

At the core of NoteTakerGPT is an intricate process that involves several stages. Each stage is designed to ensure the transformation of raw audio data into a structured, comprehensive set of notes. Here's a more in-depth look into each stage:

1. **Audio Recording**: The first stage involves recording the audio. This is done using the PyAudio library, which provides Python bindings for PortAudio, the cross-platform audio I/O library. The script records audio in 30-second intervals to ensure manageability and efficiency in the subsequent steps. At the end of each interval, the audio data is saved as a .wav file.

2. **Transcription**: Once the audio data is stored, the script initiates the transcription process. This is done by sending the audio data to OpenAI's Whisper ASR (Automatic Speech Recognition) system via the OpenAI API. It transcribes the audio data into text, which is then returned to the script. The transcription process runs in a separate process to ensure that the recording process is not blocked and continues smoothly.

3. **Chunking and Analysis**: When the transcription data is received, it is broken down into manageable chunks for analysis. This takes into consideration the token limit that the OpenAI API has for each request. The script splits the transcriptions into chunks and sends each one to the OpenAI's GPT-4 model for summarization. Accompanying each chunk is a prompt instructing the model to read the text and generate detailed bullet-point notes summarizing the content.

4. **Note Consolidation**: After all the chunks have been analyzed and summarized, the script enters the final stage: note consolidation. Here, all the summarized points are collected and formatted into a single, comprehensive set of notes. This is done by another# NoteTakerGPT

## Usage

To use NoteTakerGPT, follow these steps:

1. Run the script:
```shell
python NoteTakerGPT.py
```

2. The script will automatically start recording and transcribing audio. The transcription and summarization process will continue until a KeyboardInterrupt event occurs (typically by pressing Ctrl+C).

3. At the end of the transcription and summarization process, the script will output a comprehensive set of bullet point notes derived from the recorded audio.

## Contributing

Contributions are always welcome! To contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE.md) file for the full text. This allows you to use, modify, and distribute the code in your own projects as long as you include the original copyright notice and disclaimers.
