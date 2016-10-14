#!/usr/bin/env python

"""
This script should convert the JSON from the debate analysis into a CSV file
suitable for Quartz analysis.

WARN: This is currently incomplete, because the output JSON did not have scores
for each candidate.

Other things we should double check:
* Are we accidentally classifying the hosts reactions as the candidates? (probably, yes)
* How accurate is the gender analysis? Can we rely on it to tell Trump from Clinton?
* In general, how should we quantify the accuracy of this? Can we spot-check their facial expressions to see if checks our intuitions?
"""


import csv
import json


EMOTIONS = [
    'happiness'
    'neutral',
    'anger',
    'contempt',
    'suprise',
    'sadness',
    'fear',
    'disgust'
]

CSV_COLUMNS = [
    'frame',
    'trump_visible',
    'trump_happiness',
    'trump_neutral',
    'trump_anger',
    'trump_contempt',
    'trump_suprise',
    'trump_sadness',
    'trump_fear',
    'trump_disgust',
    'clinton_visible',
    'clinton_happiness',
    'clinton_neutral',
    'clinton_anger',
    'clinton_contempt',
    'clinton_suprise',
    'clinton_sadness',
    'clinton_fear',
    'clinton_disgust'
]


def main():
    with open('debate1_full.json') as f:
        json_data = json.load(f)

    frame_keys = sorted(json_data.keys())
    csv_data = []

    for key in frame_keys:
        url = 'https://s3-us-west-2.amazonaws.com/debateinemotion/debate1/frame%s.jpg' % key
        frame = json_data[key]
        print(frame)
        row = {
            'frame': frame,
            'trump_visible': False,
            'clinton_visible': False
        }

        if len(frame) > 2:
            print('Frame %s has more than 2 faces (%s)' % (key, url))
            continue

        for face in frame:
            if 'faceAttributes' not in face:
                print('Frame %s has no gender data (%s)' % (key, url))
                continue

            gender = face['faceAttributes']['gender']

            if gender == 'male':
                prefix = 'trump_'
            elif gender == 'female':
                prefix = 'clinton_'
            else:
                print('Frame %s has an unexpected gender: %s (%s)' % (key, gender, url))
                continue

            row[prefix + 'visible'] = True

            if 'scores' in face:
                for emotion in EMOTIONS:
                    row[prefix + emotion] = face['scores'][emotion]

    with open('debate1.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(csv_data)


if __name__ == '__main__':
    main()
