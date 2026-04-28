import time  # dùng để đo thời gian chạy thuật toán

from core.distance import build_distance_matrix  # dùng để tạo ma trận khoảng cách
from core.models import Point, RouteResult  # import kiểu dữ liệu đã khai báo


def solve_nearest_neighbor(points: list[Point], start_index: int = 0) -> RouteResult:
    """
    Giải TSP bằng thuật toán tham lam Nearest Neighbor.

    Ý tưởng:
    - Bắt đầu từ một điểm xuất phát
    - Mỗi bước chọn điểm chưa đi qua gần nhất
    - Khi đi hết tất cả điểm thì quay về điểm đầu

    Parameters
    ----------
    points : list[Point]
        Danh sách các điểm giao hàng
    start_index : int
        Index của điểm bắt đầu, mặc định là 0

    Returns
    -------
    RouteResult
        route: danh sách index theo thứ tự đi, có lặp lại điểm đầu ở cuối để khép kín
        total_distance_km: tổng quãng đường
        elapsed_ms: thời gian chạy thuật toán tính bằng mili giây
    """

    start_time = time.perf_counter()  # ghi nhận thời điểm bắt đầu để đo runtime

    n = len(points)  # số lượng điểm

    # kiểm tra trường hợp dữ liệu rỗng
    if n == 0:
        return RouteResult(
            route=[],  # không có route nào
            total_distance_km=0.0,  # không có quãng đường
            elapsed_ms=0.0,  # không có thời gian xử lý đáng kể
        )

    # kiểm tra trường hợp chỉ có 1 điểm
    if n == 1:
        elapsed_ms = (time.perf_counter() - start_time) * 1000  # đổi sang mili giây
        return RouteResult(
            route=[0, 0],  # đi từ điểm đó rồi quay lại chính nó để khép kín
            total_distance_km=0.0,  # không phát sinh quãng đường
            elapsed_ms=elapsed_ms,
        )

    # kiểm tra start_index có hợp lệ không
    if start_index < 0 or start_index >= n:
        raise ValueError("start_index không hợp lệ.")

    distance_matrix = build_distance_matrix(points)  # tạo ma trận khoảng cách giữa các điểm

    visited = [False] * n  # mảng đánh dấu điểm nào đã đi qua
    route = [start_index]  # route bắt đầu từ điểm xuất phát
    visited[start_index] = True  # đánh dấu điểm bắt đầu là đã thăm
    total_distance = 0.0  # biến cộng dồn tổng quãng đường
    current_index = start_index  # vị trí hiện tại ban đầu là điểm xuất phát

    # lặp cho tới khi đi qua hết tất cả điểm
    for _ in range(n - 1):
        nearest_index = None  # lưu index của điểm gần nhất chưa đi
        nearest_distance = float("inf")  # khởi tạo khoảng cách nhỏ nhất là vô cùng

        # duyệt toàn bộ điểm để tìm điểm gần nhất chưa thăm
        for next_index in range(n):
            if not visited[next_index]:  # chỉ xét các điểm chưa đi qua
                current_distance = distance_matrix[current_index][next_index]  # khoảng cách từ điểm hiện tại

                # nếu tìm thấy điểm gần hơn thì cập nhật
                if current_distance < nearest_distance:
                    nearest_distance = current_distance
                    nearest_index = next_index

        # sau khi duyệt xong, nearest_index là điểm gần nhất tiếp theo
        if nearest_index is None:
            break  # an toàn, dù thực tế không nên xảy ra

        route.append(nearest_index)  # thêm điểm đó vào route
        visited[nearest_index] = True  # đánh dấu đã thăm
        total_distance += nearest_distance  # cộng khoảng cách vừa đi
        current_index = nearest_index  # cập nhật vị trí hiện tại

    # sau khi đi qua hết các điểm, quay về điểm đầu để tạo chu trình khép kín
    total_distance += distance_matrix[current_index][start_index]
    route.append(start_index)  # thêm lại điểm đầu vào cuối route

    elapsed_ms = (time.perf_counter() - start_time) * 1000  # tính thời gian chạy theo ms

    return RouteResult(
        route=route,  # route cuối cùng
        total_distance_km=total_distance,  # tổng quãng đường
        elapsed_ms=elapsed_ms,  # thời gian chạy
    )