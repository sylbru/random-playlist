#!/usr/bin/env python3

import sys
import os
import json
import random
import math

def generate_playlist(config):
    playlist = []
    length = 0
    sounds = config.get('sounds')
    forbidden_amount = config.get('prevent_consecutive_or_almost')
    forbidden_sounds = []

    while length < config.get('length'):
        found = False
        while not found:
            random_sound = random.choice(sounds)
            found = random_sound not in forbidden_sounds

        playlist.append(random_sound)
        length += 1

        forbidden_sounds.insert(0, random_sound)
        if len(forbidden_sounds) > forbidden_amount:
            forbidden_sounds = forbidden_sounds[:forbidden_amount]
        
        silence = make_silence(config)
        playlist += silence

    return playlist

def make_silence(config):
    mini = config.get('minimum_silence_duration')
    maxi = config.get('maximum_silence_duration')
    step = mini

    silences = config.get('silences')
    silences = {value: key for key,value in silences.items()}
    durations = list(silences.keys())
    shortest = min(durations)

    if mini not in durations:
        raise ValueError('`mini` should be one of the silences')

    wanted_duration = random.randrange(mini, maxi + 1, step)

    values = []
    actual_duration = 0

    while len(durations) > 0 and actual_duration < wanted_duration:
        actual_duration = sum(values)

        while (len(durations) > 0
                and actual_duration + max(durations) > wanted_duration):
            durations.remove(max(durations))

        if len(durations) > 0:
            values.append(max(durations))

    files = []
    for value in values:
        files.append(silences.get(value))

    return files

def write_playlist(playlist, config):
    filename = config.get('output_name') + '.m3u'
    file = open(filename, 'w')

    for item in playlist:
        file.write(config.get('audio_folder')
            + '/' + item + '\n')

def parse_config(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError("File " + filename + " does not exist.")

    file = open(filename, 'r')
    config = json.load(file)

    if (config.get('prevent_consecutive_or_almost')
        >= len(config.get('sounds'))):
        raise ValueError('prevent_consecutive_or_almost is too high,\
            should be less than the amount of sounds')

    return config

if __name__ == "__main__":
    if len(sys.argv) > 1:
        config = parse_config(sys.argv[1])
        playlist = generate_playlist(config)
        write_playlist(playlist, config)
    else:
        print("Argument missing.")