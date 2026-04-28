import streamlit as st  # thư viện chính để chạy web app

from ui.benchmark_panel import render_benchmark_panel  # import panel benchmark
from ui.map_view import render_map_view  # import phần hiển thị bản đồ
from ui.result_panel import render_main_panels  # import khu vực hiển thị chính
from ui.sidebar import render_sidebar  # import sidebar
from ui.state_manager import init_state  # import hàm khởi tạo session state


def apply_custom_css() -> None:
    """
    Thêm CSS để giao diện gọn và đẹp hơn trên màn hình ngang.
    """
    st.markdown(
        """
        <style>
        /* Giới hạn chiều rộng vùng nội dung chính để không bị kéo quá dài */
        .block-container {
            max-width: 1200px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* Làm tiêu đề gọn hơn */
        h1 {
            margin-bottom: 0.25rem;
        }

        /* Làm container nhìn mềm hơn */
        div[data-testid="stMetric"] {
            background-color: #f8f9fb;
            padding: 12px;
            border-radius: 12px;
            border: 1px solid #e6e9ef;
        }

        /* Dataframe nhìn gọn */
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
        layout="wide",  # vẫn để wide nhưng sẽ bó chiều rộng bằng CSS
    )

    init_state()
    apply_custom_css()

    st.title("Tối ưu hóa lộ trình giao hàng (TSP)")
    st.caption(
        "Ứng dụng hỗ trợ click điểm trên bản đồ, chạy thuật toán TSP và benchmark so sánh các phương pháp."
    )

    render_sidebar()

    tab1, tab2 = st.tabs(["🚚 Tối ưu lộ trình", "📊 Benchmark"])

    with tab1:
        render_main_panels()
        st.divider()
        render_map_view()

    with tab2:
        render_benchmark_panel()


if __name__ == "__main__":
    main()