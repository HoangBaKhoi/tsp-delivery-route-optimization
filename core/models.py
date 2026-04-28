from dataclasses import dataclass  # dùng dataclass để khai báo model gọn hơn
from typing import Optional  # dùng cho kiểu dữ liệu có thể có hoặc không có giá trị


@dataclass
class Point:
    id: int  # mã số điểm
    name: str  # tên điểm, ví dụ "Kho", "Điểm 1"
    lat: float  # vĩ độ
    lng: float  # kinh độ


@dataclass
class RouteResult:
    route: list[int]  # danh sách index hoặc id các điểm theo thứ tự đi
    total_distance_km: float  # tổng quãng đường tính theo km
    elapsed_ms: float  # thời gian chạy thuật toán tính theo mili giây


@dataclass
class BenchmarkResult:
    algorithm: str  # tên thuật toán
    n_points: int  # số lượng điểm trong lần benchmark
    distance: float  # tổng quãng đường của lời giải
    elapsed_ms: float  # thời gian chạy tương ứng


@dataclass
class AppState:
    points: list[Point]  # danh sách điểm hiện tại trên giao diện
    selected_algorithm: str  # thuật toán đang được chọn
    route_result: Optional[RouteResult] = None  # kết quả route hiện tại, mặc định chưa có