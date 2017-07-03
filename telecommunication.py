from datetime import datetime
from operator import itemgetter

TYPE_START = 1
TYPE_END = -1


def format_interval_to_datetime(pair):
    if type(pair[0]) is int and type(pair[1]) is int:
        return tuple(datetime.fromtimestamp(value) for value in pair)
    else:
        return pair


def find_peaks(array, calculation_params):
    interval_start, interval_end = format_interval_to_datetime(
        calculation_params)
    formated_array = (format_interval_to_datetime(
        interval) for interval in array)

    calls = (
        (
            (start_time, TYPE_START),
            (end_time, TYPE_END),
        )
        for (start_time, end_time) in formated_array
        if (not start_time > interval_end) and (not end_time < interval_start)
    )

    if not calls:
        return

    start_points, end_points = zip(*calls)
    timeline = sorted(start_points + end_points, key=itemgetter(0))

    concurrency, counter = [], 0
    for point in timeline:
        counter += point[1]
        concurrency.append(counter)

    counted_timeline = zip(timeline, concurrency)
    max_concurrency = max(concurrency)
    peaks = filter(lambda (point, concurrency): concurrency == max_concurrency, counted_timeline)

    return map(lambda (point, concurrency): (point[0], concurrency), peaks)


if __name__ == '__main__':
    print(find_peaks(((1, 5), (2, 5), (3, 5), (4, 6)), (4, 5)))