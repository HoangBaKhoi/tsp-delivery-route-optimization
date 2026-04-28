import streamlit as st  # dùng để tạo các thành phần giao diện bên sidebar

from core.solver import run_solver  # hàm điều phối thuật toán
from data.sample_points import get_sample_points  # bộ dữ liệu mẫu hiện tại
from ui.state_manager import (
    remove_last_point,
    reset_points,
    set_points,
    set_route_result,
    set_selected_algorithm,
)  # các hàm thao tác session state


def render_sidebar() -> None:
    """
    Render toàn bộ khu vực sidebar của ứng dụng.

    Sidebar sẽ gồm:
    - chọn thuật toán
    - load dữ liệu mẫu
    - xóa điểm cuối
    - reset toàn bộ điểm
    - chạy solve
    """
    with st.sidebar:  # mọi thành phần bên trong block này sẽ nằm ở thanh bên trái
        st.header("Điều khiển")  # tiêu đề sidebar

        algorithm_options = [
            "nearest_neighbor",
            "two_opt",
            "bruteforce",
        ]  # danh sách thuật toán cho phép chọn

        selected_algorithm = st.selectbox(
            "Chọn thuật toán",  # nhãn của dropdown
            options=algorithm_options,  # danh sách lựa chọn
            index=algorithm_options.index(
                st.session_state.selected_algorithm
            ),  # giữ lại lựa chọn hiện tại trong session
        )

        set_selected_algorithm(selected_algorithm)  # cập nhật thuật toán đã chọn vào session state

        if st.button("Load sample points", use_container_width=True):
            sample_points = get_sample_points()  # lấy bộ điểm mẫu
            set_points(sample_points)  # nạp dữ liệu mẫu vào session state
            st.success("Đã load dữ liệu mẫu.")  # thông báo thành công

        if st.button("Remove last point", use_container_width=True):
            remove_last_point()  # xóa điểm cuối cùng nếu có
            st.warning("Đã xóa điểm cuối cùng.")  # thông báo trạng thái

        if st.button("Reset points", use_container_width=True):
            reset_points()  # xóa toàn bộ điểm hiện tại
            st.warning("Đã reset toàn bộ điểm.")  # thông báo trạng thái

        if st.button("Solve", use_container_width=True):
            try:
                result = run_solver(
                    st.session_state.points,  # danh sách điểm hiện tại
                    st.session_state.selected_algorithm,  # thuật toán đang chọn
                )
                set_route_result(result)  # lưu kết quả vào session state
                st.success("Chạy thuật toán thành công.")  # báo thành công
            except ValueError as error:
                set_route_result(None)  # nếu có lỗi thì xóa kết quả cũ
                st.error(str(error))  # hiển thị nội dung lỗi cho người dùng