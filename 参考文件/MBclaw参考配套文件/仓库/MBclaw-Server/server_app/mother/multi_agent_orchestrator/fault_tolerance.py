class FaultTolerance:

    def retry_failed(self, tasks, results):

        failed = []

        for t in tasks:

            if t["id"] not in results:

                failed.append(t)

        return failed
