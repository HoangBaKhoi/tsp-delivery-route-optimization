from core.models import Point  # dùng model Point đã khai báo


def get_sample_points() -> list[Point]:
    """
    Bộ dữ liệu mẫu 11 điểm trải dài toàn quốc.
    Phù hợp để so sánh Nearest Neighbor và 2-opt.
    Brute Force sẽ bị chặn nếu bạn giữ BRUTE_FORCE_LIMIT = 9.
    """
    return [
        Point(id=0, name="Kho - Đà Nẵng", lat=16.0544, lng=108.2022),

        Point(id=1, name="Điểm 1 - Hà Nội", lat=21.0285, lng=105.8542),
        Point(id=2, name="Điểm 2 - Hạ Long", lat=20.9517, lng=107.0560),
        Point(id=3, name="Điểm 3 - Hải Phòng", lat=20.8449, lng=106.6881),

        Point(id=4, name="Điểm 4 - Vinh", lat=18.6796, lng=105.6813),
        Point(id=5, name="Điểm 5 - Đồng Hới", lat=17.4689, lng=106.6223),

        Point(id=6, name="Điểm 6 - Pleiku", lat=13.9833, lng=108.0000),
        Point(id=7, name="Điểm 7 - Nha Trang", lat=12.2388, lng=109.1967),

        Point(id=8, name="Điểm 8 - TP.HCM", lat=10.8231, lng=106.6297),
        Point(id=9, name="Điểm 9 - Cần Thơ", lat=10.0452, lng=105.7469),
        Point(id=10, name="Điểm 10 - Vũng Tàu", lat=10.4114, lng=107.1362),
    ]