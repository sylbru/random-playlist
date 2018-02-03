# random-playlist
Random M3U playlist generation (with silences).

## Usage
> `../gen_playlist.py config.json`

## Configuration
A JSON file with the following keys:

* `output_name`: the relative path of the resulting playlist file, without the extension
* `audio_folder`: the relative path of the folder containing the audio files (including silences)
* `sounds`: the names of the actual sound files
* `silences`: the names of the “silent files” (keys) and their durations (values)
* `prevent_consecutive_or_almost`: weird property name meaning “play at least X other sounds before playing this sound again”
* `minimum_silence_duration`: minimum silence duration
* `maximum_silence_duration`: maximum silence duration
* `length`: desired length of the playlist, excluding silences