import math  # dùng các hàm toán học như sin, cos, sqrt, atan2

from core.models import Point  # import model Point để dùng kiểu dữ liệu rõ ràng


def haversine_distance(point_a: Point, point_b: Point) -> float:
    """
    Tính khoảng cách Haversine giữa 2 điểm địa lý theo km.
    Công thức này phù hợp khi dữ liệu là lat/lng trên bản đồ.
    """
    earth_radius_km = 6371.0  # bán kính Trái Đất xấp xỉ theo km

    # đổi độ sang radian vì các hàm lượng giác của Python dùng radian
    lat1 = math.radians(point_a.lat)
    lng1 = math.radians(point_a.lng)
    lat2 = math.radians(point_b.lat)
    lng2 = math.radians(point_b.lng)

    # độ chênh lệch vĩ độ và kinh độ
    delta_lat = lat2 - lat1
    delta_lng = lng2 - lng1

    # công thức Haversine
    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lng / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance_km = earth_radius_km * c  # khoảng cách cuối cùng
    return distance_km


def build_distance_matrix(points: list[Point]) -> list[list[float]]:
    """
    Sinh ma trận khoảng cách giữa mọi cặp điểm.
    matrix[i][j] là khoảng cách từ điểm i đến điểm j.
    """
    n = len(points)  # số lượng điểm
    matrix = [[0.0 for _ in range(n)] for _ in range(n)]  # khởi tạo ma trận n x n toàn số 0

    for i in range(n):  # duyệt từng điểm đầu
        for j in range(n):  # duyệt từng điểm đích
            if i == j:
                matrix[i][j] = 0.0  # từ một điểm tới chính nó thì khoảng cách bằng 0
            else:
                matrix[i][j] = haversine_distance(points[i], points[j])  # tính khoảng cách thực

    return matrix