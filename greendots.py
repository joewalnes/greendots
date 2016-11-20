#!/usr/bin/env python

"""

Sorry about this.

See https://github.com/joewalnes/greendots/ (or README.md)

-Joe Walnes @joewalnes

"""

from bitmap import Bitmap
from simplefont import string_bitmap

from datetime import date, datetime, time, timedelta
from sys import argv, exit, stdout, stderr

# The pixel will get darker based on number of commits.
# The 4 shades, from lightest to darkest are on 1, 4, 8, 11
# commits. So 11 commits per day will give the darkest color.
commits_per_pixel = 11

def main():
    text = ' '.join(argv[1:])

    if not text:
        stderr.write('ERROR: missing text\n')
        exit(1)

    one_year_ago = date.today() - timedelta(days=365)
    while one_year_ago.weekday() != 6: # go to start of week (sunday)
        one_year_ago -= timedelta(days=1)

    canvas = Bitmap(width=52, height=7)  # year of weeks
    
    label = string_bitmap(text)
    canvas.apply(label, x=canvas.width - label.width)  # right align
    
    if label.width > canvas.width:
        stderr.write('WARNING: text truncated\n')

    stderr.write('preview:\n\n')
    canvas.dump(stderr)

    print('#!/bin/bash')
    print('set -euo pipefail')
    print('echo "Generating a bunch of git commits..."')
    print('git init')
    n = 0
    for contrib_date in bitmap_to_contribution_dates(canvas, one_year_ago):
        stamp = datetime.combine(contrib_date, time(12, 0)).isoformat()
        for i in range(commits_per_pixel):
            print('echo {} > .greendot'.format(n))
            print('git add .greendot')
            print('GIT_COMMITTER_DATE="{}" GIT_AUTHOR_DATE="{}" git commit -m "greendot {}"'
                .format(stamp, stamp, n))
            n += 1
    print('echo "All done. Commits: {}"'.format(n))


def bitmap_to_contribution_dates(bitmap, start_date):
    current_date = start_date
    for x in range(bitmap.width):
        for y in range(bitmap.height):
            if bitmap.data[y][x]:
                yield current_date
            current_date += timedelta(days=1)

    
if __name__ == '__main__':
    main()
