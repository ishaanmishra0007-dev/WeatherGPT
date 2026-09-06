from datetime import datetime


def find_best_hour(results):

    if not results:
        return None

    return max(
        results,
        key=lambda x: x["score"]
    )


def find_best_window(results, minimum_score=80, minimum_duration=2):

    if not results:
        return None

    best_window = []
    current_window = []

    # Find the normal time interval from the data
    times = [
        datetime.strptime(item["time"], "%H:%M")
        for item in results
    ]

    intervals = []

    for i in range(1, len(times)):
        difference = (
            times[i] - times[i - 1]
        ).total_seconds() / 3600

        if difference > 0:
            intervals.append(difference)

    if not intervals:
        return None

    # Use the most common interval in the data
    expected_interval = min(intervals)

    # Find continuous suitable periods
    for i, result in enumerate(results):

        if result["score"] >= minimum_score:

            if not current_window:
                current_window = [result]

            else:
                previous_time = datetime.strptime(
                    current_window[-1]["time"],
                    "%H:%M"
                )

                current_time = datetime.strptime(
                    result["time"],
                    "%H:%M"
                )

                difference = (
                    current_time - previous_time
                ).total_seconds() / 3600

                # Check whether this point is continuous
                if difference == expected_interval:
                    current_window.append(result)

                else:
                    if current_window:
                        best_window = choose_better_window(
                            best_window,
                            current_window,
                            minimum_duration
                        )

                    current_window = [result]

        else:

            if current_window:
                best_window = choose_better_window(
                    best_window,
                    current_window,
                    minimum_duration
                )

            current_window = []

    # Check final window
    if current_window:
        best_window = choose_better_window(
            best_window,
            current_window,
            minimum_duration
        )

    if not best_window:
        return None

    start = datetime.strptime(
        best_window[0]["time"],
        "%H:%M"
    )

    end = datetime.strptime(
        best_window[-1]["time"],
        "%H:%M"
    )

    duration = (
        end - start
    ).total_seconds() / 3600

    average_score = sum(
        item["score"] for item in best_window
    ) / len(best_window)

    return {
        "start": best_window[0]["time"],
        "end": best_window[-1]["time"],
        "duration": duration,
        "average_score": round(average_score),
        "hours": len(best_window)
    }


def choose_better_window(
    current_best,
    candidate,
    minimum_duration
):

    if len(candidate) < 2:
        return current_best

    start = datetime.strptime(
        candidate[0]["time"],
        "%H:%M"
    )

    end = datetime.strptime(
        candidate[-1]["time"],
        "%H:%M"
    )

    duration = (
        end - start
    ).total_seconds() / 3600

    if duration < minimum_duration:
        return current_best

    if not current_best:
        return candidate

    current_average = sum(
        item["score"] for item in current_best
    ) / len(current_best)

    candidate_average = sum(
        item["score"] for item in candidate
    ) / len(candidate)

    if candidate_average > current_average:
        return candidate

    return current_best