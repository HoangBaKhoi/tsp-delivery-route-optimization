# Tối ưu hóa lộ trình giao hàng bằng Travelling Salesman Problem (TSP)

## 1. Giới thiệu đề tài

Dự án này xây dựng một ứng dụng hỗ trợ tối ưu hóa lộ trình giao hàng dựa trên bài toán **Travelling Salesman Problem (TSP)**.

Trong bài toán này, một người giao hàng hoặc một xe giao hàng cần đi qua tất cả các điểm giao đúng một lần và quay trở lại điểm xuất phát sao cho **tổng quãng đường là nhỏ nhất**.

Ứng dụng cho phép:

- click trực tiếp các điểm trên bản đồ
- chọn thuật toán giải TSP
- hiển thị lộ trình tối ưu trên bản đồ
- hiển thị tổng quãng đường và thời gian chạy
- benchmark các thuật toán và trực quan hóa bằng biểu đồ

---

## 2. Mục tiêu

Mục tiêu của dự án là:

- mô phỏng bài toán tối ưu lộ trình giao hàng
- cài đặt và so sánh nhiều thuật toán giải TSP
- trực quan hóa kết quả trên bản đồ
- đánh giá trade-off giữa **chất lượng lời giải** và **thời gian chạy**

---

## 3. Các thuật toán được sử dụng

### 3.1. Brute Force
Thuật toán vét cạn, thử tất cả các hoán vị có thể của lộ trình để tìm nghiệm tối ưu tuyệt đối.

**Ưu điểm:**
- luôn tìm được lời giải tối ưu

**Nhược điểm:**
- thời gian chạy tăng rất nhanh theo số lượng điểm
- chỉ phù hợp với số điểm nhỏ

---

### 3.2. Nearest Neighbor
Thuật toán tham lam, tại mỗi bước luôn chọn điểm chưa đi gần nhất với điểm hiện tại.

**Ưu điểm:**
- đơn giản
- tốc độ rất nhanh

**Nhược điểm:**
- không đảm bảo tối ưu toàn cục
- dễ rơi vào nghiệm cục bộ chưa tốt

---

### 3.3. 2-opt
Thuật toán heuristic cải thiện lộ trình ban đầu bằng cách đảo các đoạn đường để giảm tổng quãng đường.

Trong dự án này, 2-opt sử dụng route ban đầu từ **Nearest Neighbor**.

**Ưu điểm:**
- thường cho lời giải tốt hơn Nearest Neighbor
- tốc độ vẫn nhanh hơn rất nhiều so với Brute Force

**Nhược điểm:**
- không đảm bảo tối ưu tuyệt đối

---

## 4. Công nghệ sử dụng

- **Python 3.11+**
- **Streamlit**: xây dựng giao diện web
- **Folium + OpenStreetMap**: hiển thị bản đồ
- **streamlit-folium**: tích hợp bản đồ Folium vào Streamlit
- **matplotlib**: vẽ biểu đồ benchmark
- **pytest**: kiểm thử

---

## 5. Cấu trúc thư mục

```text
project/
├── app.py
├── requirements.txt
├── README.md
├── core/
│   ├── __init__.py
│   ├── distance.py
│   ├── models.py
│   ├── tsp_bruteforce.py
│   ├── tsp_nearest_neighbor.py
│   ├── tsp_two_opt.py
│   ├── solver.py
│   └── benchmark.py
├── ui/
│   ├── __init__.py
│   ├── map_view.py
│   ├── sidebar.py
│   ├── result_panel.py
│   ├── state_manager.py
│   └── benchmark_panel.py
├── data/
│   ├── __init__.py
│   └── sample_points.py
├── visualization/
│   ├── __init__.py
│   └── charts.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_distance.py
    └── test_solver.py

8. Cách sử dụng ứng dụng
8.1. Thêm điểm giao hàng

Có 2 cách:

bấm Load sample points để nạp dữ liệu mẫu
click trực tiếp lên bản đồ để thêm điểm mới
8.2. Chọn thuật toán

Trong sidebar, chọn một trong các thuật toán:

nearest_neighbor
two_opt
bruteforce
8.3. Giải bài toán

Bấm nút Solve để chạy thuật toán.

Kết quả hiển thị gồm:

route
tổng quãng đường
thời gian chạy
lộ trình vẽ trên bản đồ
8.4. Benchmark

Ở phần benchmark:

nhập các mức số lượng điểm, ví dụ: 5, 7, 9, 12, 15
chọn số lần lặp
chọn thuật toán
bấm Run Benchmark

Kết quả gồm:

bảng benchmark
biểu đồ runtime
biểu đồ tổng quãng đường