import folium  # thư viện tạo bản đồ Leaflet bằng Python
import streamlit as st  # dùng để hiển thị trong app Streamlit
from streamlit_folium import st_folium  # dùng để nhúng map Folium vào Streamlit

from ui.state_manager import add_point  # hàm thêm điểm mới vào session state


def get_map_center(points: list) -> tuple[float, float]:
    """
    Tính tâm bản đồ.

    Nếu chưa có điểm nào:
    - trả về tâm mặc định ở khu vực Việt Nam

    Nếu đã có điểm:
    - lấy trung bình lat/lng để map focus vào cụm điểm hiện tại
    """
    if not points:
        return 16.0, 106.0  # tâm mặc định gần khu vực Việt Nam

    avg_lat = sum(point.lat for point in points) / len(points)  # trung bình vĩ độ
    avg_lng = sum(point.lng for point in points) / len(points)  # trung bình kinh độ
    return avg_lat, avg_lng  # trả về tâm map


def build_route_coordinates(points: list, route: list[int]) -> list[list[float]]:
    """
    Chuyển route dạng index thành danh sách tọa độ [lat, lng]
    để Folium có thể vẽ PolyLine.
    """
    coordinates = []  # danh sách tọa độ theo thứ tự route

    for index in route:
        point = points[index]  # lấy điểm theo index trong route
        coordinates.append([point.lat, point.lng])  # thêm cặp lat/lng vào danh sách

    return coordinates  # trả về danh sách tọa độ hoàn chỉnh


def build_points_bounds(points: list) -> list[list[float]]:
    lat_values = [point.lat for point in points]
    lng_values = [point.lng for point in points]

    return [
        [min(lat_values), min(lng_values)],
        [max(lat_values), max(lng_values)],
    ]


def build_segment_midpoint(start_coordinate: list[float], end_coordinate: list[float]) -> list[float]:
    return [
        (start_coordinate[0] + end_coordinate[0]) / 2,
        (start_coordinate[1] + end_coordinate[1]) / 2,
    ]


def add_route_step_labels(folium_map: folium.Map, route_coordinates: list[list[float]]) -> None:
    for step_index in range(len(route_coordinates) - 1):
        midpoint = build_segment_midpoint(
            route_coordinates[step_index],
            route_coordinates[step_index + 1],
        )

        folium.Marker(
            location=midpoint,
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    background: #f97316;
                    color: white;
                    border: 2px solid white;
                    border-radius: 6px;
                    box-shadow: 0 1px 5px rgba(0,0,0,0.35);
                    font-size: 12px;
                    font-weight: 800;
                    height: 24px;
                    line-height: 20px;
                    text-align: center;
                    transform: translate(-12px, -12px);
                    width: 24px;
                ">{step_index + 1}</div>
                """
            ),
        ).add_to(folium_map)


def build_route_step_rows(points: list, route: list[int]) -> list[dict]:
    rows = []

    for step_index in range(len(route) - 1):
        from_point = points[route[step_index]]
        to_point = points[route[step_index + 1]]

        rows.append(
            {
                "Bước": step_index + 1,
                "Từ": f"{from_point.id} - {from_point.name}",
                "Đến": f"{to_point.id} - {to_point.name}",
            }
        )

    return rows


def render_route_steps_panel(points: list, route_result) -> None:
    st.subheader("Thứ tự đường đi")

    if route_result is None or len(route_result.route) < 2:
        st.info("Chưa có lộ trình. Bấm Solve để xem thứ tự đường đi.")
        return

    route_rows = build_route_step_rows(points, route_result.route)
    st.dataframe(route_rows, use_container_width=True, hide_index=True, height=700)


def handle_map_click() -> None:
    """
    Xử lý sự kiện click trên bản đồ.

    Logic:
    - đọc last_clicked từ dữ liệu trả về của st_folium
    - làm tròn tọa độ để tránh sai số rất nhỏ
    - so sánh với click gần nhất để tránh thêm trùng khi Streamlit rerun
    - nếu là click mới thì thêm Point mới vào session state
    """
    map_data = st.session_state.get("delivery_route_map")

    if not map_data:
        return  # nếu không có dữ liệu trả về thì bỏ qua

    clicked = map_data.get("last_clicked")  # lấy thông tin click gần nhất
    if not clicked:
        return  # nếu chưa click gì thì bỏ qua

    lat = round(clicked["lat"], 6)  # làm tròn vĩ độ để ổn định so sánh
    lng = round(clicked["lng"], 6)  # làm tròn kinh độ để ổn định so sánh

    current_click_signature = (lat, lng)  # chữ ký của click hiện tại

    # nếu click hiện tại trùng click gần nhất đã xử lý thì không thêm lại
    if st.session_state.last_map_click == current_click_signature:
        return

    # cập nhật click gần nhất đã xử lý
    st.session_state.last_map_click = current_click_signature

    # tạo tên điểm mới theo số thứ tự hiện tại
    point_number = len(st.session_state.points)
    point_name = "Kho" if point_number == 0 else f"Điểm {point_number}"

    add_point(
        name=point_name,  # tên điểm mới
        lat=lat,  # vĩ độ từ map
        lng=lng,  # kinh độ từ map
    )


@st.fragment
def render_map_view() -> None:
    """
    Hiển thị bản đồ, marker các điểm, route nếu đã có kết quả solve,
    và cho phép click để thêm điểm mới.
    """
    st.subheader("Bản đồ lộ trình")  # tiêu đề phần map
    st.caption("Click trực tiếp lên bản đồ để thêm điểm giao hàng.")  # hướng dẫn ngắn cho người dùng

    points = st.session_state.points  # lấy danh sách điểm hiện tại
    route_result = st.session_state.route_result  # lấy kết quả route hiện tại nếu có

    center_lat, center_lng = get_map_center(points)  # tính tâm map
    zoom_start = 6 if not points else 13  # nếu chưa có điểm thì zoom rộng, có điểm thì zoom gần hơn

    folium_map = folium.Map(
        location=[center_lat, center_lng],  # tâm bản đồ
        zoom_start=zoom_start,  # mức zoom ban đầu
        tiles="OpenStreetMap",  # sử dụng nền bản đồ OSM
    )

    # thêm popup hiển thị tọa độ khi click để người dùng dễ quan sát
    folium.LatLngPopup().add_to(folium_map)

    # thêm marker cho từng điểm hiện tại
    for point in points:
        popup_text = (
            f"ID: {point.id}<br>"
            f"Tên: {point.name}<br>"
            f"Lat: {point.lat}<br>"
            f"Lng: {point.lng}"
        )  # nội dung popup khi bấm vào marker

        tooltip_text = f"{point.id} - {point.name}"  # tooltip ngắn gọn

        marker_color = "red" if point.id == 0 else "green"
        marker_icon = "home" if point.id == 0 else "map-marker"

        folium.Marker(
            location=[point.lat, point.lng],  # vị trí marker
            popup=popup_text,  # popup chi tiết
            tooltip=tooltip_text,  # tooltip hiện khi rê chuột
            icon=folium.Icon(color=marker_color, icon=marker_icon, prefix="fa"),
        ).add_to(folium_map)  # thêm marker vào map

        folium.Marker(
            location=[point.lat, point.lng],
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    background: {'#dc2626' if point.id == 0 else '#16a34a'};
                    color: white;
                    border: 2px solid white;
                    border-radius: 999px;
                    box-shadow: 0 1px 4px rgba(0,0,0,0.35);
                    font-size: 12px;
                    font-weight: 700;
                    height: 24px;
                    line-height: 20px;
                    text-align: center;
                    transform: translate(-4px, -34px);
                    width: 24px;
                ">{point.id}</div>
                """
            ),
        ).add_to(folium_map)

    # nếu đã có route thì vẽ polyline
    if route_result is not None and len(route_result.route) >= 2:
        route_coordinates = build_route_coordinates(points, route_result.route)  # route index -> tọa độ

        folium.PolyLine(
            locations=route_coordinates,  # danh sách tọa độ theo thứ tự route
            color="#f97316",
            weight=6,  # độ dày đường
            opacity=0.9,  # độ trong suốt
            tooltip="Lộ trình tối ưu",  # tooltip của đường đi
        ).add_to(folium_map)  # thêm đường đi vào map
        add_route_step_labels(folium_map, route_coordinates)

    if len(points) >= 2:
        folium_map.fit_bounds(build_points_bounds(points), padding=(30, 30))

    map_col, route_col = st.columns([2.2, 1])

    with map_col:
        # render map và lấy dữ liệu tương tác trả về
        st_folium(
            folium_map,
            height=700,  # chiều cao khung bản đồ (cũ là 500)
            width=None,  # để Streamlit tự co giãn theo layout
            key="delivery_route_map",
            returned_objects=["last_clicked"],
            on_change=handle_map_click,
        )

    with route_col:
        render_route_steps_panel(points, route_result)
