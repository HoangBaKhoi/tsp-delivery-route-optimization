import random  # dùng để sinh dữ liệu điểm ngẫu nhiên có kiểm soát bằng seed

from core.models import BenchmarkResult, Point  # import model kết quả benchmark và Point
from core.solver import run_solver  # dùng solver thống nhất để gọi thuật toán


def generate_random_points(
    n_points: int,
    seed: int | None = None,
    center_lat: float = 10.7769,
    center_lng: float = 106.7009,
    spread: float = 0.03,
) -> list[Point]:
    """
    Sinh ngẫu nhiên một danh sách điểm quanh một tâm cố định.

    Parameters
    ----------
    n_points : int
        Số lượng điểm cần sinh.
    seed : int | None
        Seed để sinh ngẫu nhiên có thể lặp lại được.
    center_lat : float
        Tâm vĩ độ để sinh điểm xung quanh.
    center_lng : float
        Tâm kinh độ để sinh điểm xung quanh.
    spread : float
        Biên độ lệch tối đa quanh tâm theo cả lat và lng.

    Returns
    -------
    list[Point]
        Danh sách điểm ngẫu nhiên.
    """
    rng = random.Random(seed)  # tạo bộ sinh số ngẫu nhiên riêng để tái lập được kết quả
    points = []  # danh sách điểm sẽ trả về

    for i in range(n_points):
        lat = center_lat + rng.uniform(-spread, spread)  # sinh vĩ độ ngẫu nhiên quanh tâm
        lng = center_lng + rng.uniform(-spread, spread)  # sinh kinh độ ngẫu nhiên quanh tâm

        point_name = "Kho" if i == 0 else f"Điểm {i}"  # đặt tên điểm đầu là Kho, các điểm sau là Điểm i

        points.append(
            Point(
                id=i,  # gán id theo thứ tự
                name=point_name,  # tên điểm
                lat=lat,  # vĩ độ
                lng=lng,  # kinh độ
            )
        )

    return points  # trả về danh sách điểm ngẫu nhiên


def run_benchmark(
    dataset_sizes: list[int],
    algorithms: list[str],
    repeats: int = 3,
) -> list[BenchmarkResult]:
    """
    Chạy benchmark hàng loạt cho nhiều kích thước dataset và nhiều thuật toán.

    Logic:
    - với mỗi n_points trong dataset_sizes
    - lặp lại nhiều lần theo repeats
    - mỗi lần sinh một bộ điểm ngẫu nhiên bằng seed khác nhau
    - chạy từng thuật toán trên cùng bộ điểm đó
    - ghi lại kết quả BenchmarkResult

    Parameters
    ----------
    dataset_sizes : list[int]
        Danh sách số lượng điểm cần benchmark, ví dụ [5, 7, 9, 15, 20].
    algorithms : list[str]
        Danh sách thuật toán cần chạy, ví dụ ["nearest_neighbor", "two_opt", "bruteforce"].
    repeats : int
        Số lần lặp cho mỗi kích thước dữ liệu để có nhiều mẫu đo hơn.

    Returns
    -------
    list[BenchmarkResult]
        Danh sách toàn bộ kết quả benchmark.
    """
    benchmark_results = []  # nơi lưu tất cả kết quả benchmark

    for n_points in dataset_sizes:  # duyệt từng kích thước dữ liệu
        for repeat_index in range(repeats):  # lặp lại nhiều lần để giảm may rủi
            seed = n_points * 100 + repeat_index  # tạo seed đơn giản, ổn định và dễ tái lập

            points = generate_random_points(
                n_points=n_points,  # số lượng điểm cần sinh
                seed=seed,  # seed cho lần benchmark này
            )

            for algorithm in algorithms:  # chạy từng thuật toán trên cùng bộ điểm
                try:
                    result = run_solver(
                        points=points,  # cùng một input cho các thuật toán để so sánh công bằng
                        algorithm_name=algorithm,  # thuật toán cần chạy
                    )

                    benchmark_results.append(
                        BenchmarkResult(
                            algorithm=algorithm,  # tên thuật toán
                            n_points=n_points,  # số điểm của lần benchmark này
                            distance=result.total_distance_km,  # tổng quãng đường
                            elapsed_ms=result.elapsed_ms,  # thời gian chạy theo ms
                        )
                    )

                except ValueError:
                    # nếu thuật toán không chạy được, ví dụ brute force vượt ngưỡng,
                    # thì bỏ qua trường hợp đó và tiếp tục benchmark các thuật toán khác
                    continue

    return benchmark_results  # trả về toàn bộ kết quả benchmark


def run_benchmark_on_points(
    points: list[Point],
    algorithms: list[str],
    repeats: int = 3,
) -> list[BenchmarkResult]:
    """
    Chạy benchmark trực tiếp trên bộ điểm hiện tại của người dùng.

    Hàm này không sinh dữ liệu ngẫu nhiên. Nó dùng đúng danh sách points đang có
    trên giao diện để so sánh các thuật toán trên cùng một input.
    """
    benchmark_results = []
    n_points = len(points)

    for _ in range(repeats):
        for algorithm in algorithms:
            try:
                result = run_solver(
                    points=points,
                    algorithm_name=algorithm,
                )

                benchmark_results.append(
                    BenchmarkResult(
                        algorithm=algorithm,
                        n_points=n_points,
                        distance=result.total_distance_km,
                        elapsed_ms=result.elapsed_ms,
                    )
                )

            except ValueError:
                continue

    return benchmark_results


def summarize_benchmark_results(
    results: list[BenchmarkResult],
) -> list[dict]:
    """
    Gộp kết quả benchmark theo (algorithm, n_points) và tính trung bình.

    Output là list[dict] để tiện:
    - in ra console
    - đưa vào bảng Streamlit
    - hoặc vẽ chart sau này

    Mỗi dict gồm:
    - algorithm
    - n_points
    - avg_distance
    - avg_elapsed_ms
    - runs
    """
    grouped_data = {}  # dictionary dùng để gom nhóm kết quả theo khóa (algorithm, n_points)

    for item in results:
        key = (item.algorithm, item.n_points)  # khóa nhóm gồm tên thuật toán và số điểm

        if key not in grouped_data:
            grouped_data[key] = {
                "algorithm": item.algorithm,  # tên thuật toán
                "n_points": item.n_points,  # số lượng điểm
                "distances": [],  # danh sách quãng đường để tính trung bình
                "elapsed_times": [],  # danh sách thời gian để tính trung bình
            }

        grouped_data[key]["distances"].append(item.distance)  # thêm quãng đường vào nhóm
        grouped_data[key]["elapsed_times"].append(item.elapsed_ms)  # thêm runtime vào nhóm

    summary = []  # danh sách kết quả tổng hợp cuối cùng

    for _, value in grouped_data.items():
        runs = len(value["distances"])  # số lần chạy thực tế của nhóm này

        avg_distance = sum(value["distances"]) / runs  # trung bình quãng đường
        avg_elapsed_ms = sum(value["elapsed_times"]) / runs  # trung bình thời gian chạy

        summary.append(
            {
                "algorithm": value["algorithm"],  # tên thuật toán
                "n_points": value["n_points"],  # số điểm
                "avg_distance": avg_distance,  # quãng đường trung bình
                "avg_elapsed_ms": avg_elapsed_ms,  # thời gian chạy trung bình
                "runs": runs,  # số lần chạy được ghi nhận
            }
        )

    # sắp xếp để dễ đọc:
    # trước theo n_points tăng dần, sau đó theo tên thuật toán
    summary.sort(key=lambda row: (row["n_points"], row["algorithm"]))

    return summary  # trả về kết quả tổng hợp
