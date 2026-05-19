import streamlit as st  # dùng để hiển thị dữ liệu trên giao diện


def render_points_table() -> None:
    """
    Hiển thị danh sách điểm hiện tại dưới dạng bảng.
    """
    points = st.session_state.points  # lấy danh sách điểm từ session state

    if not points:
        st.info("Hiện chưa có điểm nào.")  # nếu không có điểm thì hiện thông báo
        return

    table_data = []  # danh sách dữ liệu để đổ vào bảng

    for point in points:
        table_data.append(
            {
                "ID": point.id,  # mã số điểm
                "Tên": point.name,  # tên điểm
                "Lat": point.lat,  # vĩ độ
                "Lng": point.lng,  # kinh độ
            }
        )

    st.dataframe(table_data, use_container_width=True)  # hiển thị bảng dữ liệu chiếm toàn chiều ngang


def render_route_result() -> None:
    """
    Hiển thị kết quả route hiện tại:
    - tổng quãng đường
    - thời gian chạy
    - route dạng index
    - route dạng tên điểm
    """
    result = st.session_state.route_result  # lấy kết quả route hiện tại
    if result is None:
        st.info("Chưa có kết quả. Hãy load dữ liệu mẫu và bấm Solve.")  # nếu chưa solve thì báo
        return

    st.subheader("Kết quả tối ưu")  # tiêu đề khu vực kết quả

    col1, col2 = st.columns(2)  # chia làm 2 cột để hiển thị metric gọn hơn

    with col1:
        st.metric(
            "Tổng quãng đường (km)",
            round(result.total_distance_km, 2),
        )  # hiển thị tổng quãng đường

    with col2:
        st.metric(
            "Thời gian chạy (ms)",
            round(result.elapsed_ms, 4),
        )  # hiển thị thời gian chạy

    st.caption("Chi tiết thứ tự đường đi được hiển thị bên cạnh bản đồ.")

#for app_v2.py
def render_main_panels() -> None:
    """
    Render 2 panel chính của giao diện:
    - bên trái: danh sách điểm
    - bên phải: kết quả route
    """
    left_col, right_col = st.columns([1.4, 1])  # cột trái rộng hơn một chút

    with left_col:
        st.subheader("Danh sách điểm")
        render_points_table()

    with right_col:
        render_route_result()

''' for app.py
def render_main_panels() -> None:
    """
    Render 2 panel chính của giao diện:
    - bên trái: danh sách điểm
    - bên phải: kết quả route
    """
    left_col, right_col = st.columns([1, 1])  # chia layout chính thành 2 cột bằng nhau

    with left_col:
        st.subheader("Danh sách điểm")  # tiêu đề cột trái
        render_points_table()  # hiển thị bảng điểm

    with right_col:
        render_route_result()  # hiển thị kết quả solve
'''
