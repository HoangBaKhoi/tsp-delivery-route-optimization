import streamlit as st

from core.benchmark import run_benchmark_on_points, summarize_benchmark_results
from visualization.charts import (
    plot_algorithm_distance_bar_chart,
    plot_algorithm_runtime_bar_chart,
)


def _init_benchmark_state() -> None:
    if "benchmark_summary" not in st.session_state:
        st.session_state.benchmark_summary = None

    if "benchmark_raw_results" not in st.session_state:
        st.session_state.benchmark_raw_results = None

    if "benchmark_points_signature" not in st.session_state:
        st.session_state.benchmark_points_signature = None


def _build_points_signature(points: list) -> tuple:
    return tuple(
        (point.id, point.name, round(point.lat, 6), round(point.lng, 6))
        for point in points
    )


def _clear_stale_benchmark(points_signature: tuple) -> None:
    saved_signature = st.session_state.benchmark_points_signature

    if saved_signature is None:
        return

    if saved_signature != points_signature:
        st.session_state.benchmark_summary = None
        st.session_state.benchmark_raw_results = None
        st.session_state.benchmark_points_signature = None


def render_benchmark_panel() -> None:
    """
    Render benchmark trên chính dữ liệu điểm hiện tại của người dùng.
    """
    _init_benchmark_state()

    points = st.session_state.points
    points_signature = _build_points_signature(points)
    _clear_stale_benchmark(points_signature)

    st.subheader("Benchmark trên dữ liệu hiện tại")
    st.caption(
        "So sánh các thuật toán bằng đúng danh sách điểm đang có trong tab tối ưu lộ trình."
    )

    st.metric("Số điểm hiện tại", len(points))

    with st.expander("Cấu hình benchmark", expanded=True):
        selected_algorithms = st.multiselect(
            "Chọn thuật toán benchmark",
            options=["nearest_neighbor", "two_opt", "bruteforce"],
            default=["nearest_neighbor", "two_opt"],
            help="Brute Force chỉ nên bật khi số điểm nhỏ vì thời gian chạy tăng rất nhanh.",
        )

        repeats = st.number_input(
            "Số lần lặp trên cùng dữ liệu",
            min_value=1,
            max_value=20,
            value=3,
            step=1,
            help="Chạy lặp lại trên cùng bộ điểm để lấy thời gian trung bình ổn định hơn.",
        )

        if st.button("Run Benchmark", use_container_width=True):
            try:
                if len(points) < 2:
                    raise ValueError(
                        "Cần ít nhất 2 điểm để benchmark. Hãy load sample hoặc click thêm điểm trên bản đồ."
                    )

                if not selected_algorithms:
                    raise ValueError("Cần chọn ít nhất một thuật toán để benchmark.")

                raw_results = run_benchmark_on_points(
                    points=points,
                    algorithms=selected_algorithms,
                    repeats=int(repeats),
                )

                if not raw_results:
                    raise ValueError(
                        "Không có thuật toán nào chạy được trên dữ liệu hiện tại."
                    )

                summary = summarize_benchmark_results(raw_results)

                st.session_state.benchmark_raw_results = raw_results
                st.session_state.benchmark_summary = summary
                st.session_state.benchmark_points_signature = points_signature

                st.success("Đã benchmark trên dữ liệu hiện tại.")

            except ValueError as error:
                st.session_state.benchmark_raw_results = None
                st.session_state.benchmark_summary = None
                st.error(str(error))

    summary = st.session_state.benchmark_summary

    if summary is None:
        st.info("Chưa có dữ liệu benchmark. Hãy chọn thuật toán và bấm Run Benchmark.")
        return

    st.markdown("### Bảng kết quả benchmark")
    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True,
        column_config={
            "algorithm": "Thuật toán",
            "n_points": "Số điểm",
            "avg_distance": st.column_config.NumberColumn(
                "Quãng đường TB (km)",
                format="%.2f",
            ),
            "avg_elapsed_ms": st.column_config.NumberColumn(
                "Runtime TB (ms)",
                format="%.4f",
            ),
            "runs": "Số lần chạy",
        },
    )

    st.markdown("### Biểu đồ so sánh")

    runtime_fig = plot_algorithm_runtime_bar_chart(summary)
    distance_fig = plot_algorithm_distance_bar_chart(summary)

    col1, col2 = st.columns(2)

    with col1:
        st.pyplot(runtime_fig)

    with col2:
        st.pyplot(distance_fig)
