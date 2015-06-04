# coding=utf-8

import time

from .session import authenticate

# raw_input was renamed to input in python 3.x
try:
    input = raw_input
except NameError:
    pass


def select_report(nessus=None):
    """
    Present a command line interface to easily select a report from the
    report Nessus server, and return the report's UUID.
    """
    if nessus is None:
        nessus = authenticate()

    report_data = nessus.reports
    reports = [report for report in report_data]
    reports.reverse()

    index = 0
    selected = None
    print("\nPlease select a report (most recent first)")

    while selected is None:
        print("="*75)
        print("Showing reports {0} to {1} (of {2}) Most recent reports first."
              .format(index+1, min(index+10, len(reports)), len(reports)))
        for i in range(10):
            try:
                timestamp = time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    time.localtime(int(reports[index+i].timestamp)))
                name = reports[index+i].name
                status = reports[index+i].status
                # list each report with the format:
                # [#] (date) Report Name {status}
                # {status} is only shown if it is not 'completed'
                print("  [{0}] ({1}) {2} {3}".format(i, timestamp, name,
                                                     "[{0}]".format(status) if status != 'completed' else ''))
                max_choice = i
            except IndexError:
                pass
        choice = input("Selection (n for next page, p for prev): ")
        print("\n")

        if choice == 'n' and len(reports) > index+10:
            index += 10
        elif choice == 'p' and index >= 10:
            index -= 10
        else:
            try:
                selected = int(choice)
                if selected not in range(max_choice+1):
                    raise ValueError
            except ValueError:
                print(" >>> Invalid selection <<<")
                selected = None
                continue

    return reports[index+selected]


def get_reports_between(start, end, nessus=None):
    """
    Go through all of the reports available to us. Carve out
    the ones that are between start and end, which are both
    POSIX timestamps.

    Returns an array of all reports within the given timeframe.
    """
    if nessus is None:
        nessus = authenticate()

    reports = nessus.reports
    reports.reverse()
    selected_reports = []

    for report in reports:
        report_time = time.mktime(time.localtime(int(report.timestamp)))
        timestamp = time.strftime(
            "%Y-%m-%d %H:%M:%S",
            time.localtime(int(report.timestamp)))
        name = report.name
        status = report.status
        if start < report_time < end and status == 'completed':
            print("Found report: ({0}) {1}".format(
                timestamp, name))
            selected_reports.append(report)

    return selected_reports
