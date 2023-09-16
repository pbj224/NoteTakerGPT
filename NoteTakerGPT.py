import requests
import openai
import traceback
import pandas as pd
import numpy as np
import tiktoken
import pyaudio
import wave
import keyboard
import time
import threading
import multiprocessing
from multiprocessing import Manager
from queue import Queue
import os

# Initialize OpenAI API key
openai.api_key = "OPENAI_API_KEY"

# Constants
MODEL = "gpt-4"
RECORDING_INTERVAL_SECONDS = 60

def split_text_into_chunks(text, chunk_size=20):
    sentences = text.split('\n')
    chunks = [sentences[i:i + chunk_size] for i in range(0, len(sentences), chunk_size)]
    return ['. '.join(chunk) for chunk in chunks]

def passage_segmenter(passage, interval=600):
    segment = []
    count = 0
    while count < len(passage):
        segment.append(passage[count:count + interval])
        count += interval
    return segment

def ask_question(messages):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        stream=True  # Set stream=True for streaming completions
    )
    output = ""
    for chunk in response:
        if "delta" in chunk["choices"][0]:
            delta = chunk["choices"][0]["delta"]
            if "content" in delta:
                content = delta["content"]
                output += content
                print(content, end="")  # Add end parameter to prevent newline character

    return output

def count_tokens(string):
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(string))
    return num_tokens

def create_analysis(passage):
    messages = [
      {"role": "system", "content": "Read the following section from a meeting transcript and generate detailed bullet point notes on all the key points and details being discussed.\n\nSection: " + passage}
    ]
    return ask_question(messages)

def intermediate_notes(passage):
    messages = [
      {"role": "system", "content": """Read the following collection of bullet point notes on a meeting and rewrite them to improve flow and make space for additional entities with fusion, compression, and removal of uninformative phrases like \"the meeting participants are discussing\". The new section of bullet pointed notes that you make should become highly dense and concise yet self-contained, i.e., easily understood, even for people who didnt attend the meeting. They must also still be in bullet point format.\n\nSection: """ + passage}
    ]
    return ask_question(messages)

def reformat_analysis(analysis, seg_count):
    tok_len = count_tokens(analysis)
    if tok_len <=6000:
        messages = [
            {"role": "system", "content": "You are a helpful, GPT-4 powered sumnmary generator. You will be given a set of bullet point notes broken out into " + seg_count + " sections, each corresponding to a section of a call transctipt and you will consolidate all the sections into one single very detailed, very comprehensive set of bullet point notes organized by topic rather than section. Your outputted notes should be a minimum of 2300 words in length, so make sure to capture all the details without watering them down, shortening them, nor skipping any"},
            {"role": "user", "content": ".\n\nNotes: " + analysis}
        ]
        return ask_question(messages)
    else:
        meeting_notes = analysis
        num_segments = seg_count
        notes_tok_len = tok_len
        while notes_tok_len > 6000:
            shortened_notes = ""
            segments = split_text_into_chunks(meeting_notes)
            for segment in segments:
                new_segment = intermediate_notes(segment)
                shortened_notes += new_segment + "\n"
            meeting_notes = shortened_notes
            num_segments = len(segments)
            notes_tok_len = count_tokens(meeting_notes)
        messages = [
            {"role": "system", "content": "You are a helpful, GPT-4 powered sumnmary generator. You will be given a set of bullet point notes broken out into " + num_segments + " sections, each corresponding to a section of a call transctipt and you will consolidate all the sections into one single very detailed, very comprehensive set of bullet point notes organized by topic rather than section. Your outputted notes should be a minimum of 2300 words in length, so make sure to capture all the details without watering them down, shortening them, nor skipping any"},
            {"role": "user", "content": ".\n\nNotes: " + meeting_notes}
        ]
        return ask_question(messages)

def transcribe_audio(audio_queue, result_queue, shared_list):  # Add result_queue as an argument
    while True:
        audio_file = audio_queue.get()
        if audio_file is None:
            break
        # Open the audio file
        with open(audio_file, 'rb') as file:
            transcript = openai.Audio.transcribe("whisper-1", file)  # Pass the file object
            transcript = str(transcript).replace("{", "").replace("}", "")
            segments = passage_segmenter(transcript)
            count = 1
            for segment in segments:
                analysis = create_analysis(segment)
                analysis = analysis + "\n"
                shared_list.append(analysis)
                count += 1
        # Delete the audio file after it has been transcribed
        os.remove(audio_file)

def record_audio(filename, rate=44100, channels=1, chunk=2048, format=pyaudio.paInt16, stop_event=None):
    p = pyaudio.PyAudio()
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []
    start_time = time.time()
    recording_started = False

    while not stop_event.is_set():
        if not recording_started:
            recording_started = True
            start_time = time.time()

        data = stream.read(chunk)
        frames.append(data)

        if time.time() - start_time >= RECORDING_INTERVAL_SECONDS:
            break

    stream.stop_stream()
    stream.close()
    p.terminate()
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

def main():
    # Create a multiprocessing Event to signal recording termination
    stop_event = multiprocessing.Event()
    # Create a multiprocessing Queue for transcription results
    result_queue = multiprocessing.Queue()
    # Create a Manager object and a shared list
    manager = Manager()
    shared_list = manager.list()

    # Start the transcription process in parallel
    transcription_process = multiprocessing.Process(
        target=transcribe_audio, args=(result_queue, result_queue, shared_list)  # Pass result_queue twice
    )
    transcription_process.start()
    print("Process has started")
    counter = 1
    try:
        while True:
            filename = f"recorded_audio{counter}.wav"
            # Start recording immediately
            record_audio(filename, stop_event=stop_event)
            # Queue the audio file for transcription
            result_queue.put(filename)
            counter += 1
    except KeyboardInterrupt:
        # Stop recording and transcription when Ctrl+C is pressed
        stop_event.set()

    transcription_process.join()
    # At this point, all transcriptions have gone through the queue
    unformatted = "\n".join(shared_list)  # Join all the elements in the shared list
    # Perform the reformatting after all transcriptions are done
    notes = reformat_analysis(unformatted, str(counter - 1))
    print("\n\n\n\n")
    print(notes)

if __name__ == "__main__":
    main()