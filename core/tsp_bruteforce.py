import itertools  # dùng để sinh tất cả hoán vị có thể
import time  # dùng để đo thời gian chạy thuật toán

from core.distance import build_distance_matrix  # dùng để tạo ma trận khoảng cách
from core.models import Point, RouteResult  # import các model cần dùng


def calculate_route_distance(route: list[int], distance_matrix: list[list[float]]) -> float:
    """
    Tính tổng quãng đường của một route đã khép kín.
    Ví dụ: [0, 1, 2, 0]
    """
    total_distance = 0.0  # biến cộng dồn tổng quãng đường

    # duyệt từng cặp điểm liên tiếp trong route
    for i in range(len(route) - 1):
        from_index = route[i]  # điểm xuất phát của cạnh hiện tại
        to_index = route[i + 1]  # điểm đến của cạnh hiện tại
        total_distance += distance_matrix[from_index][to_index]  # cộng khoảng cách cạnh vào tổng

    return total_distance  # trả về tổng quãng đường


def solve_bruteforce(points: list[Point]) -> RouteResult:
    """
    Giải bài toán TSP bằng Brute Force.

    Ý tưởng:
    - Cố định điểm xuất phát là 0
    - Sinh mọi hoán vị của các điểm còn lại
    - Với mỗi hoán vị, tạo route khép kín
    - Tính tổng quãng đường
    - Chọn route ngắn nhất

    Lưu ý:
    - Thuật toán này chỉ phù hợp với n nhỏ vì số hoán vị tăng rất nhanh.
    """
    start_time = time.perf_counter()  # ghi nhận thời điểm bắt đầu để đo runtime

    n = len(points)  # số lượng điểm

    # trường hợp không có điểm nào
    if n == 0:
        return RouteResult(
            route=[],
            total_distance_km=0.0,
            elapsed_ms=0.0,
        )

    # trường hợp chỉ có 1 điểm
    if n == 1:
        elapsed_ms = (time.perf_counter() - start_time) * 1000  # đổi sang ms
        return RouteResult(
            route=[0, 0],  # đi từ điểm đó rồi quay lại chính nó
            total_distance_km=0.0,
            elapsed_ms=elapsed_ms,
        )

    # trường hợp có đúng 2 điểm
    if n == 2:
        distance_matrix = build_distance_matrix(points)  # tạo ma trận khoảng cách
        route = [0, 1, 0]  # route khép kín đơn giản
        total_distance = calculate_route_distance(route, distance_matrix)  # tính tổng quãng đường
        elapsed_ms = (time.perf_counter() - start_time) * 1000  # tính runtime

        return RouteResult(
            route=route,
            total_distance_km=total_distance,
            elapsed_ms=elapsed_ms,
        )

    distance_matrix = build_distance_matrix(points)  # tạo ma trận khoảng cách giữa các điểm

    start_index = 0  # cố định điểm xuất phát là 0
    other_indices = list(range(1, n))  # các điểm còn lại sẽ được hoán vị

    best_route = []  # lưu route tốt nhất tìm được
    best_distance = float("inf")  # khởi tạo khoảng cách tốt nhất là vô cùng

    # sinh mọi hoán vị của các điểm còn lại
    for perm in itertools.permutations(other_indices):
        # ghép thành route đầy đủ, có quay về điểm đầu
        candidate_route = [start_index] + list(perm) + [start_index]

        # tính tổng quãng đường của route hiện tại
        candidate_distance = calculate_route_distance(candidate_route, distance_matrix)

        # nếu route hiện tại tốt hơn route tốt nhất trước đó thì cập nhật
        if candidate_distance < best_distance:
            best_distance = candidate_distance
            best_route = candidate_route

    elapsed_ms = (time.perf_counter() - start_time) * 1000  # tính tổng thời gian chạy theo ms

    return RouteResult(
        route=best_route,  # route tốt nhất
        total_distance_km=best_distance,  # tổng quãng đường ngắn nhất
        elapsed_ms=elapsed_ms,  # thời gian chạy
    )