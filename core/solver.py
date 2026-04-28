from core.models import Point, RouteResult  # import kiểu dữ liệu đầu vào và đầu ra
from core.tsp_bruteforce import solve_bruteforce  # import thuật toán brute force
from core.tsp_nearest_neighbor import solve_nearest_neighbor  # import thuật toán nearest neighbor
from core.tsp_two_opt import improve_two_opt  # import thuật toán 2-opt


# đặt một ngưỡng để chặn brute force khi số điểm quá lớn
# vì brute force tăng rất nhanh theo giai thừa
BRUTE_FORCE_LIMIT = 11


def run_solver(points: list[Point], algorithm_name: str) -> RouteResult:
    """
    Hàm điều phối thống nhất để UI hoặc app gọi thuật toán.

    Parameters
    ----------
    points : list[Point]
        Danh sách các điểm giao hàng
    algorithm_name : str
        Tên thuật toán cần chạy

    Returns
    -------
    RouteResult
        Kết quả route tương ứng với thuật toán được chọn

    Supported algorithm names
    -------------------------
    - "bruteforce"
    - "nearest_neighbor"
    - "two_opt"
    """

    n = len(points)  # lấy số lượng điểm hiện tại

    # không cho chạy nếu ít hơn 2 điểm
    # vì bài toán TSP không có ý nghĩa nếu chỉ có 0 hoặc 1 điểm
    if n < 2:
        raise ValueError("Cần ít nhất 2 điểm để chạy thuật toán TSP.")

    # chuẩn hóa tên thuật toán:
    # - bỏ khoảng trắng đầu/cuối
    # - chuyển về chữ thường để tránh lỗi nhập liệu
    normalized_name = algorithm_name.strip().lower()

    # nếu đúng 2 điểm thì mọi thuật toán thực chất đều cho cùng một route
    # route duy nhất hợp lệ là 0 -> 1 -> 0
    # ở đây ta gọi brute force để lấy kết quả chuẩn và đơn giản nhất
    if n == 2:
        return solve_bruteforce(points)

    # chạy brute force nếu người dùng chọn đúng thuật toán đó
    if normalized_name == "bruteforce":
        # chặn brute force nếu vượt ngưỡng cấu hình
        if n > BRUTE_FORCE_LIMIT:
            raise ValueError(
                f"Brute Force chỉ được phép chạy khi số điểm <= {BRUTE_FORCE_LIMIT}."
            )

        return solve_bruteforce(points)

    # chạy nearest neighbor nếu người dùng chọn thuật toán tham lam
    if normalized_name == "nearest_neighbor":
        return solve_nearest_neighbor(points, start_index=0)

    # chạy 2-opt:
    # trước tiên cần một route ban đầu hợp lệ
    # theo đặc tả, mặc định route ban đầu lấy từ nearest neighbor
    if normalized_name == "two_opt":
        initial_result = solve_nearest_neighbor(points, start_index=0)  # sinh route ban đầu
        return improve_two_opt(points, initial_result.route)  # tối ưu route đó bằng 2-opt

    # nếu tên thuật toán không nằm trong danh sách hỗ trợ thì báo lỗi rõ ràng
    raise ValueError(
        "Thuật toán không hợp lệ. Hãy dùng một trong các giá trị: "
        "'bruteforce', 'nearest_neighbor', 'two_opt'."
    )