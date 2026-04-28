import streamlit as st  # dùng session_state của Streamlit để lưu trạng thái giao diện

from core.models import Point, RouteResult  # import model Point và RouteResult


def init_state() -> None:
    """
    Khởi tạo các biến trạng thái cần thiết cho ứng dụng.
    Hàm này nên được gọi ngay khi app Streamlit bắt đầu chạy.
    """
    if "points" not in st.session_state:
        st.session_state.points = []  # danh sách điểm hiện tại trên giao diện

    if "selected_algorithm" not in st.session_state:
        st.session_state.selected_algorithm = "nearest_neighbor"  # thuật toán mặc định

    if "route_result" not in st.session_state:
        st.session_state.route_result = None  # kết quả route hiện tại, ban đầu chưa có

    if "next_point_id" not in st.session_state:
        st.session_state.next_point_id = 0  # id tiếp theo để tạo điểm mới

    if "last_map_click" not in st.session_state:
        st.session_state.last_map_click = None  # lưu click gần nhất để tránh thêm trùng điểm


def set_points(points: list[Point]) -> None:
    """
    Gán lại toàn bộ danh sách điểm.
    Dùng khi load sample data hoặc import dữ liệu.
    """
    st.session_state.points = points[:]  # copy danh sách điểm để tránh sửa nhầm tham chiếu

    if points:
        max_id = max(point.id for point in points)  # tìm id lớn nhất hiện tại
        st.session_state.next_point_id = max_id + 1  # id tiếp theo sẽ là lớn nhất + 1
    else:
        st.session_state.next_point_id = 0  # nếu không có điểm nào thì reset về 0

    st.session_state.route_result = None  # dữ liệu đầu vào thay đổi thì kết quả cũ không còn hợp lệ
    st.session_state.last_map_click = None  # reset click gần nhất khi thay toàn bộ danh sách điểm


def add_point(name: str, lat: float, lng: float) -> None:
    """
    Thêm một điểm mới vào danh sách điểm hiện tại.
    """
    point_id = st.session_state.next_point_id  # lấy id mới

    new_point = Point(
        id=point_id,  # id của điểm mới
        name=name,  # tên điểm
        lat=lat,  # vĩ độ
        lng=lng,  # kinh độ
    )

    st.session_state.points.append(new_point)  # thêm điểm vào danh sách
    st.session_state.next_point_id += 1  # tăng bộ đếm id cho lần thêm tiếp theo
    st.session_state.route_result = None  # dữ liệu đầu vào thay đổi thì xóa kết quả cũ


def remove_last_point() -> None:
    """
    Xóa điểm cuối cùng trong danh sách điểm.
    """
    if st.session_state.points:
        st.session_state.points.pop()  # xóa phần tử cuối cùng
        st.session_state.route_result = None  # dữ liệu thay đổi nên xóa kết quả cũ


def reset_points() -> None:
    """
    Xóa toàn bộ điểm và reset trạng thái liên quan.
    """
    st.session_state.points = []  # xóa hết điểm
    st.session_state.route_result = None  # xóa kết quả route
    st.session_state.next_point_id = 0  # reset bộ đếm id
    st.session_state.last_map_click = None  # reset click gần nhất


def set_selected_algorithm(algorithm_name: str) -> None:
    """
    Cập nhật thuật toán được chọn trên giao diện.
    """
    st.session_state.selected_algorithm = algorithm_name  # lưu tên thuật toán đang chọn


def set_route_result(route_result: RouteResult | None) -> None:
    """
    Lưu kết quả route hiện tại.
    """
    st.session_state.route_result = route_result  # cập nhật kết quả thuật toán