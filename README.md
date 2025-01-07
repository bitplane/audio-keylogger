# ⌨👂 audio keylogger

So I heard this could be done with a phone on a desk using the accelerometer,
but what if we tried using keyboard + mic data first?

## Wat

1. Record audio, create JSON keypress outputs
2. Train a model that can reconstruct keypresses from the audio.

```
$ pip install -r requirements.txt
./record.py
```

Data goes into the ./data dir.

## Future / todo

* Train `whisper` or similar with the outputs + evaluate with different sample rates etc.
* Create a Dockerized web app that uploads to archive.org, for mass data collection.
* Train something to separate keypress audio from background noise.
