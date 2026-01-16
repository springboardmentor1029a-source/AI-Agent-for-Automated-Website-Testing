def generate_report(results):
    report_path = "test_report.txt"

    with open(report_path, "w") as f:
        for r in results:
            f.write(r + "\n")

    return report_path
