import streamlit as st  # dùng để tạo giao diện benchmark trong Streamlit

from core.benchmark import run_benchmark, summarize_benchmark_results  # hàm chạy benchmark và tổng hợp kết quả
from visualization.charts import plot_distance_chart, plot_runtime_chart  # hàm vẽ biểu đồ


def _init_benchmark_state() -> None:
    """
    Khởi tạo các biến session_state liên quan đến benchmark nếu chưa có.
    Tách riêng để không phụ thuộc bắt buộc vào state_manager.py.
    """
    if "benchmark_summary" not in st.session_state:
        st.session_state.benchmark_summary = None  # nơi lưu bảng kết quả benchmark đã tổng hợp

    if "benchmark_raw_results" not in st.session_state:
        st.session_state.benchmark_raw_results = None  # nơi lưu raw results nếu sau này cần dùng thêm


def _parse_dataset_sizes(raw_text: str) -> list[int]:
    """
    Chuyển chuỗi nhập từ text input thành list[int].

    Ví dụ:
    "5, 7, 9, 12, 15" -> [5, 7, 9, 12, 15]
    """
    parts = raw_text.split(",")  # tách chuỗi theo dấu phẩy
    sizes = []  # danh sách số lượng điểm sau khi parse

    for part in parts:
        cleaned = part.strip()  # bỏ khoảng trắng thừa ở đầu/cuối
        if not cleaned:
            continue  # nếu rỗng thì bỏ qua

        value = int(cleaned)  # chuyển sang số nguyên
        if value < 2:
            raise ValueError("Mỗi dataset size phải >= 2.")  # benchmark TSP không có ý nghĩa nếu < 2 điểm

        sizes.append(value)  # thêm vào danh sách

    if not sizes:
        raise ValueError("Danh sách dataset size không được để trống.")  # không cho phép rỗng

    # loại trùng rồi sắp xếp tăng dần để nhìn bảng/biểu đồ gọn hơn
    sizes = sorted(set(sizes))

    return sizes  # trả về danh sách số lượng điểm hợp lệ


def render_benchmark_panel() -> None:
    """
    Render toàn bộ khu benchmark:
    - nhập cấu hình benchmark
    - chạy benchmark
    - hiển thị bảng kết quả
    - hiển thị chart runtime và distance
    """
    _init_benchmark_state()  # đảm bảo state benchmark đã tồn tại

    st.subheader("Benchmark và biểu đồ đánh giá")  # tiêu đề phần benchmark
    st.caption(
        "Chạy benchmark trên dữ liệu ngẫu nhiên có kiểm soát bằng seed để so sánh runtime và chất lượng lời giải."
    )  # mô tả ngắn

    with st.expander("Cấu hình benchmark", expanded=True):
        dataset_sizes_text = st.text_input(
            "Dataset sizes (cách nhau bởi dấu phẩy)",
            value="5, 7, 9, 12, 15",  # giá trị mặc định để chạy nhanh
            help="Ví dụ: 5, 7, 9, 12, 15",
        )  # ô nhập các mức số lượng điểm

        repeats = st.number_input(
            "Số lần lặp cho mỗi mức n",
            min_value=1,
            max_value=20,
            value=3,
            step=1,
            help="Mỗi mức số điểm sẽ được chạy nhiều lần để lấy số trung bình.",
        )  # số lần lặp benchmark cho mỗi n

        selected_algorithms = st.multiselect(
            "Chọn thuật toán benchmark",
            options=["nearest_neighbor", "two_opt", "bruteforce"],
            default=["nearest_neighbor", "two_opt", "bruteforce"],
            help="Brute Force sẽ tự bị bỏ qua ở các mức n vượt quá ngưỡng cho phép trong solver.",
        )  # danh sách thuật toán muốn benchmark

        use_log_scale = st.checkbox(
            "Dùng trục log cho biểu đồ runtime",
            value=False,
            help="Hữu ích khi runtime các thuật toán chênh lệch rất lớn.",
        )  # tùy chọn log scale cho runtime chart

        if st.button("Run Benchmark", use_container_width=True):
            try:
                dataset_sizes = _parse_dataset_sizes(dataset_sizes_text)  # parse chuỗi thành list[int]

                if not selected_algorithms:
                    raise ValueError("Cần chọn ít nhất một thuật toán để benchmark.")  # không cho chạy nếu không chọn gì

                raw_results = run_benchmark(
                    dataset_sizes=dataset_sizes,  # danh sách số lượng điểm
                    algorithms=selected_algorithms,  # thuật toán được chọn
                    repeats=int(repeats),  # số lần lặp
                )  # chạy benchmark thực tế

                summary = summarize_benchmark_results(raw_results)  # gộp kết quả để tính trung bình

                st.session_state.benchmark_raw_results = raw_results  # lưu raw results vào session
                st.session_state.benchmark_summary = summary  # lưu summary vào session

                st.success("Đã chạy benchmark thành công.")  # báo thành công

            except ValueError as error:
                st.session_state.benchmark_raw_results = None  # reset dữ liệu benchmark nếu lỗi
                st.session_state.benchmark_summary = None
                st.error(str(error))  # hiển thị nội dung lỗi

    summary = st.session_state.benchmark_summary  # lấy summary hiện tại từ session_state

    if summary is None:
        st.info("Chưa có dữ liệu benchmark. Hãy cấu hình và bấm Run Benchmark.")  # nếu chưa chạy benchmark
        return

    st.markdown("### Bảng kết quả benchmark")  # tiêu đề bảng kết quả
    st.dataframe(summary, use_container_width=True)  # hiển thị bảng summary

#for app_v2.py
    st.markdown("### Biểu đồ đánh giá")

    runtime_fig = plot_runtime_chart(summary, use_log_scale=use_log_scale)
    distance_fig = plot_distance_chart(summary)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Biểu đồ runtime**")
        st.pyplot(runtime_fig)

    with col2:
        st.markdown("**Biểu đồ quãng đường**")
        st.pyplot(distance_fig)


''' for app.py
    st.markdown("### Biểu đồ runtime")  # tiêu đề chart runtime
    runtime_fig = plot_runtime_chart(summary, use_log_scale=use_log_scale)  # vẽ biểu đồ runtime
    st.pyplot(runtime_fig)  # hiển thị figure trong Streamlit

    st.markdown("### Biểu đồ quãng đường")  # tiêu đề chart distance
    distance_fig = plot_distance_chart(summary)  # vẽ biểu đồ distance
    st.pyplot(distance_fig)  # hiển thị figure trong Streamlit
'''
