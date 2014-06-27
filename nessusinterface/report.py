import time
from nessusapi.report import list_reports

def select_report():
    report_data = list_reports()
    reports = [report for report in report_data]
    reports.reverse()
    selected = None
    print("\nPlease select a report (most recent first)")
    index = 0
    while selected is None:
        print("="*75)
        print("Showing reports {0} to {1} (of {2}) Most recent reports first."
               .format(index+1,min(index+10,len(reports)),len(reports)))
        for i in range(10):
            try:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(reports[index+i]['timestamp'])))
                name = reports[index+i]['readableName']
                status = reports[index+i]['status']
                print("  [{0}] ({1}) {2} {3}".format(i, timestamp, name, "[{0}]".format(status) if status != 'completed' else ''))
                max_choice = i
            except IndexError:
                pass
        choice = raw_input("Selection (n for next page, p for prev): ")
        print("\n")
        if choice == 'n' and len(reports) > index+10:
            index += 10
        elif choice == 'p' and index >= 10:
            index -= 10
        else:
            try:
                selected = int(choice)
                if not selected in range(max_choice+1):
                    selected = None
                    raise ValueError
            except ValueError:
                print(" >>> Invalid selection <<<")
                continue
          
    return reports[index+selected]['name']

