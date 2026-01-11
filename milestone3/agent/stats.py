stats = {"total": 0, "passed": 0, "failed": 0}

def update_stats(passed):
    stats["total"] += 1
    if passed:
        stats["passed"] += 1
    else:
        stats["failed"] += 1

def get_stats():
    return stats
