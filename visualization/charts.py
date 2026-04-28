import matplotlib.pyplot as plt  # dùng để vẽ biểu đồ


def _group_summary_by_algorithm(summary: list[dict]) -> dict[str, list[dict]]:
    """
    Gom dữ liệu summary theo từng thuật toán.
    """
    grouped = {}

    for row in summary:
        algorithm = row["algorithm"]

        if algorithm not in grouped:
            grouped[algorithm] = []

        grouped[algorithm].append(row)

    for algorithm in grouped:
        grouped[algorithm].sort(key=lambda item: item["n_points"])

    return grouped


def plot_runtime_chart(summary: list[dict], use_log_scale: bool = False):
    """
    Vẽ biểu đồ runtime theo số lượng điểm.
    """
    grouped = _group_summary_by_algorithm(summary)

    fig, ax = plt.subplots(figsize=(10, 6))

    # cấu hình style riêng cho từng thuật toán để dễ phân biệt hơn
    styles = {
        "bruteforce": {
            "marker": "s",       # marker hình vuông
            "linestyle": "--",   # nét đứt
            "linewidth": 2.5,    # nét dày hơn
            "zorder": 3,         # ưu tiên nổi lên trên
        },
        "nearest_neighbor": {
            "marker": "o",       # marker hình tròn
            "linestyle": "-",    # nét liền
            "linewidth": 2.0,
            "zorder": 2,
        },
        "two_opt": {
            "marker": "^",       # marker hình tam giác
            "linestyle": "-.",   # nét gạch chấm
            "linewidth": 2.0,
            "zorder": 2,
        },
    }

    # chủ động vẽ bruteforce sau cùng để nếu trùng điểm vẫn dễ thấy hơn
    plot_order = ["nearest_neighbor", "two_opt", "bruteforce"]

    for algorithm in plot_order:
        if algorithm not in grouped:
            continue

        rows = grouped[algorithm]
        x_values = [row["n_points"] for row in rows]
        y_values = [row["avg_elapsed_ms"] for row in rows]

        style = styles.get(algorithm, {})

        ax.plot(
            x_values,
            y_values,
            label=algorithm,
            marker=style.get("marker", "o"),
            linestyle=style.get("linestyle", "-"),
            linewidth=style.get("linewidth", 2.0),
            zorder=style.get("zorder", 2),
        )

    ax.set_title("Biểu đồ runtime theo số lượng điểm")
    ax.set_xlabel("Số lượng điểm")
    ax.set_ylabel("Thời gian chạy trung bình (ms)")
    ax.grid(True)
    ax.legend()

    if use_log_scale:
        ax.set_yscale("log")

    fig.tight_layout()
    return fig


def plot_distance_chart(summary: list[dict]):
    """
    Vẽ biểu đồ tổng quãng đường trung bình theo số lượng điểm.
    """
    grouped = _group_summary_by_algorithm(summary)

    fig, ax = plt.subplots(figsize=(10, 6))

    # cấu hình style riêng cho từng thuật toán để tránh bị đè lên nhau
    styles = {
        "bruteforce": {
            "marker": "s",       # marker hình vuông
            "linestyle": "--",   # nét đứt
            "linewidth": 2.5,    # nét dày hơn
            "zorder": 3,         # vẽ nổi hơn
        },
        "nearest_neighbor": {
            "marker": "o",       # marker hình tròn
            "linestyle": "-",    # nét liền
            "linewidth": 2.0,
            "zorder": 2,
        },
        "two_opt": {
            "marker": "^",       # marker hình tam giác
            "linestyle": "-.",   # nét gạch chấm
            "linewidth": 2.0,
            "zorder": 2,
        },
    }

    # vẽ bruteforce sau cùng để nếu trùng với two_opt vẫn dễ quan sát hơn
    plot_order = ["nearest_neighbor", "two_opt", "bruteforce"]

    for algorithm in plot_order:
        if algorithm not in grouped:
            continue

        rows = grouped[algorithm]
        x_values = [row["n_points"] for row in rows]
        y_values = [row["avg_distance"] for row in rows]

        style = styles.get(algorithm, {})

        ax.plot(
            x_values,
            y_values,
            label=algorithm,
            marker=style.get("marker", "o"),
            linestyle=style.get("linestyle", "-"),
            linewidth=style.get("linewidth", 2.0),
            zorder=style.get("zorder", 2),
        )

    ax.set_title("Biểu đồ quãng đường theo số lượng điểm")
    ax.set_xlabel("Số lượng điểm")
    ax.set_ylabel("Tổng quãng đường trung bình (km)")
    ax.grid(True)
    ax.legend()

    fig.tight_layout()
    return fig