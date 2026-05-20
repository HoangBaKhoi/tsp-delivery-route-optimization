import streamlit as st

from ui.benchmark_panel import render_benchmark_panel
from ui.map_view import render_map_view
from ui.result_panel import render_main_panels
from ui.sidebar import render_sidebar
from ui.state_manager import init_state


def apply_custom_css() -> None:
    """
    Thêm CSS để giao diện gọn và dễ đọc hơn.
    """
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 1200px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        h1 {
            margin-bottom: 0.25rem;
        }

        div[data-testid="stMetric"] {
            background-color: #f8f9fb;
            padding: 12px;
            border-radius: 12px;
            border: 1px solid #e6e9ef;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    """
    Hàm chính của ứng dụng Streamlit.
    """
    st.set_page_config(
        page_title="TSP Delivery Route Optimizer",
        page_icon="🚚",
        layout="wide",
    )

    init_state()
    apply_custom_css()

    st.title("Tối ưu hóa lộ trình giao hàng (TSP)")
    st.caption(
        "Ứng dụng hỗ trợ click điểm trên bản đồ, chạy thuật toán TSP và benchmark so sánh các phương pháp."
    )

    render_sidebar()

    render_main_panels()
    st.divider()
    render_map_view()
    st.divider()
    render_benchmark_panel()


if __name__ == "__main__":
    main()
