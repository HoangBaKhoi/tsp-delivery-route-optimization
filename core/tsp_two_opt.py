import time  # dùng để đo thời gian chạy thuật toán

from core.distance import build_distance_matrix  # dùng để tạo ma trận khoảng cách
from core.models import Point, RouteResult  # import các model cần dùng


def calculate_route_distance(route: list[int], distance_matrix: list[list[float]]) -> float:
    """
    Tính tổng quãng đường của một route đã khép kín.
    Ví dụ route = [0, 1, 2, 0].
    """
    total_distance = 0.0  # biến cộng dồn tổng quãng đường

    # duyệt từng cặp điểm liên tiếp trong route
    for i in range(len(route) - 1):
        from_index = route[i]  # điểm xuất phát của cạnh hiện tại
        to_index = route[i + 1]  # điểm đích của cạnh hiện tại
        total_distance += distance_matrix[from_index][to_index]  # cộng khoảng cách cạnh vào tổng

    return total_distance  # trả về tổng quãng đường


def is_valid_closed_route(route: list[int], n_points: int) -> bool:
    """
    Kiểm tra route có hợp lệ hay không.

    Route hợp lệ khi:
    - có ít nhất 2 phần tử
    - điểm đầu và điểm cuối giống nhau để tạo chu trình khép kín
    - đi qua đủ tất cả các điểm đúng 1 lần ở phần giữa
    """
    if len(route) < 2:
        return False  # route quá ngắn thì không hợp lệ

    if route[0] != route[-1]:
        return False  # không quay về điểm đầu thì không phải route khép kín

    middle_nodes = route[:-1]  # bỏ phần tử cuối vì nó lặp lại điểm đầu
    unique_nodes = set(middle_nodes)  # lấy tập các điểm duy nhất

    if len(middle_nodes) != n_points:
        return False  # số điểm trong route không khớp với tổng số điểm cần đi

    if len(unique_nodes) != n_points:
        return False  # có lặp điểm ở giữa hoặc thiếu điểm

    if unique_nodes != set(range(n_points)):
        return False  # không đi qua đủ đúng các index từ 0 tới n-1

    return True  # nếu qua hết các điều kiện thì route hợp lệ


def improve_two_opt(points: list[Point], initial_route: list[int]) -> RouteResult:
    """
    Cải thiện một route ban đầu bằng thuật toán 2-opt.

    Ý tưởng:
    - Chọn 2 vị trí i, k trong route
    - Đảo ngược đoạn giữa i..k
    - Nếu route mới ngắn hơn route cũ thì chấp nhận
    - Lặp lại cho tới khi không còn cải thiện

    Parameters
    ----------
    points : list[Point]
        Danh sách các điểm giao hàng
    initial_route : list[int]
        Route khép kín ban đầu, ví dụ [0, 1, 2, 3, 4, 0]

    Returns
    -------
    RouteResult
        Route sau khi tối ưu bằng 2-opt
    """
    start_time = time.perf_counter()  # ghi nhận thời điểm bắt đầu để đo runtime

    n = len(points)  # số lượng điểm

    # xử lý trường hợp không có điểm nào
    if n == 0:
        return RouteResult(
            route=[],
            total_distance_km=0.0,
            elapsed_ms=0.0,
        )

    # kiểm tra route đầu vào có hợp lệ không
    if not is_valid_closed_route(initial_route, n):
        raise ValueError("initial_route không hợp lệ hoặc không khép kín.")

    distance_matrix = build_distance_matrix(points)  # tạo ma trận khoảng cách giữa các điểm

    best_route = initial_route[:]  # copy route ban đầu để tối ưu dần
    best_distance = calculate_route_distance(best_route, distance_matrix)  # tính khoảng cách hiện tại

    improved = True  # cờ đánh dấu còn cải thiện được hay không

    # lặp cho tới khi không còn tìm thấy route tốt hơn
    while improved:
        improved = False  # giả sử vòng này không cải thiện được

        # i bắt đầu từ 1 để cố định điểm đầu depot, không đảo vào vị trí đầu tiên
        for i in range(1, len(best_route) - 2):
            # k dừng trước phần tử cuối cùng vì phần tử cuối là depot lặp lại
            for k in range(i + 1, len(best_route) - 1):
                # tạo route mới bằng cách:
                # - giữ nguyên đoạn trước i
                # - đảo ngược đoạn từ i đến k
                # - giữ nguyên đoạn sau k
                new_route = (
                    best_route[:i]
                    + best_route[i:k + 1][::-1]
                    + best_route[k + 1:]
                )

                # tính tổng quãng đường của route mới
                new_distance = calculate_route_distance(new_route, distance_matrix)

                # nếu route mới tốt hơn thì cập nhật nghiệm tốt nhất
                if new_distance < best_distance:
                    best_route = new_route  # lưu route mới tốt hơn
                    best_distance = new_distance  # cập nhật khoảng cách tốt nhất
                    improved = True  # đánh dấu là có cải thiện
                    break  # thoát vòng k để quay lại quét từ đầu với route mới

            if improved:
                break  # nếu đã cải thiện, thoát vòng i để bắt đầu lại từ route mới

    elapsed_ms = (time.perf_counter() - start_time) * 1000  # tính thời gian chạy theo ms

    return RouteResult(
        route=best_route,  # route sau tối ưu
        total_distance_km=best_distance,  # tổng quãng đường tốt nhất tìm được
        elapsed_ms=elapsed_ms,  # thời gian chạy
    )