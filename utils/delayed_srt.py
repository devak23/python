from datetime import datetime, timedelta, time
import re


PATTERN = r'(\d{2}):(\d{2}):(\d{2}),(\d{3})'

def main(file_name: str, delay: float):

    with open(file_name + '_fixed', 'w') as out_file:
        with open(file_name, "r", encoding="utf-8", newline='') as in_file:
            for line in in_file:
                if '-->' in line:
                    parts = line.split('-->')
                    new_start_time = add_delay(parts[0].strip(), delay)
                    new_end_time = add_delay(parts[1].strip(), delay)
                    out_file.write(f"{new_start_time} --> {new_end_time}\r\n")
                else:
                    out_file.write(line)


def add_delay(line: str, delay: float) -> str:
    match = re.match(PATTERN, line)

    if match:
        hours, minutes, seconds, millis = map(int, match.groups())
        dt_time = time(hours, minutes, seconds, millis * 1000)
        dt = datetime.combine(datetime.min.date(), dt_time)
        nt = dt + timedelta(seconds=delay)

        h = nt.hour
        m = nt.minute
        s = nt.second
        ms = nt.microsecond // 1000

        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    else:
        return line

if __name__ == '__main__':
    main('../data/sample.srt', 9.5)
