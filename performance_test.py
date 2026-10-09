import time
import urllib.request
URL = "http://example.com/"
PROXY = "http://127.0.0.1:8080"
TRIALS = 10

def test_direct(url):
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    start = time.perf_counter()
    response = opener.open(url)
    data = response.read()
    print("DIRECT:",response.status,response.geturl(),len(data))
    end = time.perf_counter()
    return end-start, len(data)

def test_proxy(url):
    proxy_handler = urllib.request.ProxyHandler({'http': PROXY})
    opener = urllib.request.build_opener(proxy_handler)
    start= time.perf_counter()
    response = opener.open(url)
    data = response.read()
    print("PROXY:",response.status,response.geturl(),len(data))
    end = time.perf_counter()
    return end-start, len(data)

if __name__ == "__main__":
        direct_times = []
        proxy_times = []
        direct_bytes = 0
        proxy_bytes = 0
        run_id=time.time_ns()
        for i in range(TRIALS):
            test_url = f"{URL}?benchmark={run_id}-{i}"
            direct_time, direct_size = test_direct(test_url)
            proxy_time, proxy_size = test_proxy(test_url)
            direct_times.append(direct_time)
            proxy_times.append(proxy_time)
            direct_bytes += direct_size
            proxy_bytes += proxy_size
            print(f"Trial {i + 1}: Direct={direct_time:.4f}s, Proxy={proxy_time:.4f}s")
        avg_direct = sum(direct_times)/TRIALS
        avg_proxy = sum(proxy_times)/TRIALS
        overhead = avg_proxy-avg_direct
        direct_throughput = direct_bytes/sum(direct_times)
        proxy_throughput = proxy_bytes/sum(proxy_times)
        print("\n--- Performance Results ---")
        print(f"Average direct latency: {avg_direct * 1000:.2f} ms")
        print(f"Average proxy latency: {avg_proxy * 1000:.2f} ms")
        print(f"Average overhead: {overhead * 1000:.2f} ms")
        print(f"Direct throughput: {direct_throughput:.2f} bytes/s")
        print(f"Proxy throughput: {proxy_throughput:.2f} bytes/s")
