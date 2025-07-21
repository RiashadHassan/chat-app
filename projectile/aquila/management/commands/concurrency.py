import time
import requests
import concurrent.futures

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Stress test concurrency limits by firing many simultaneous GET requests to a target URL."

    DEFAULT_URL = "http://127.0.0.1:8000/api/aquila/health/concurrency/"
    DEFAULT_NUM_REQUESTS = 500
    DEFAULT_TIMEOUT = 60

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            type=str,
            default=self.DEFAULT_URL,
            help="Target URL for GET requests",
        )
        parser.add_argument(
            "--requests",
            type=int,
            default=self.DEFAULT_NUM_REQUESTS,
            help="Number of concurrent requests to send",
        )
        parser.add_argument(
            "--timeout",
            type=int,
            default=self.DEFAULT_TIMEOUT,
            help="Request timeout in seconds",
        )

    def handle(self, *args, **options):
        url = options["url"]
        num_requests = options["requests"]
        timeout = options["timeout"]

        self.stdout.write(
            f"Starting stress test: {num_requests} requests to {url} (timeout {timeout}s)"
        )

        start_time = time.time()
        success_count = 0
        fail_count = 0
        exception_count = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [
                executor.submit(self.make_request, url, timeout, i)
                for i in range(num_requests)
            ]

            for future in concurrent.futures.as_completed(futures):
                try:
                    s, f, e = future.result()
                    success_count += s
                    fail_count += f
                    exception_count += e
                except Exception as ex:
                    self.stderr.write(f"Exception from future: {ex}")
                    exception_count += 1

        total_time = time.time() - start_time

        self.stdout.write("")
        self.stdout.write(f"Test completed in {total_time:.2f} seconds")
        self.stdout.write(f"Successful responses: {success_count}")
        self.stdout.write(f"Failed responses (status not in 200s): {fail_count}")
        self.stdout.write(f"Exceptions: {exception_count}")

    def make_request(self, url, timeout, index):
        try:
            q_param = f"req-{index}"
            response = requests.get(url, params={"q": q_param}, timeout=timeout)
            print(f"[{index}] {response.status_code}")
            if response.status_code in [200, 201]:
                return 1, 0, 0  # success, fail, exception
            else:
                return 0, 1, 0
        except Exception as e:
            print(f"[{index}] Exception: {e}")
            return 0, 0, 1
