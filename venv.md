python -m venv .venv

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

pip install streamlit folium streamlit-folium matplotlib plotly pytest
1. streamlit: dùng để làm web app bằng Python rất nhanh. Nó lo phần giao diện như nút bấm, sidebar, chọn thuật toán, hiển thị kết quả, bảng, biểu đồ. 
Với đề tài của bạn, đây sẽ là khung chính của app.
2. folium: dùng để tạo bản đồ tương tác dựa trên Leaflet. Bạn sẽ dùng nó để hiển thị bản đồ, đặt marker các điểm giao hàng, và vẽ tuyến đường trên bản đồ.
3. streamlit-folium: là cầu nối giữa Streamlit và Folium. Nói đơn giản, Folium tự nó tạo map, còn package này giúp nhúng map đó vào app Streamlit và hỗ trợ trao đổi dữ liệu hai chiều. 
Với đề tài này, nó gần như là package bắt buộc nếu bạn muốn có map trong giao diện Streamlit.
4. matplotlib: thư viện vẽ biểu đồ rất phổ biến trong Python. Hợp để vẽ các biểu đồ tương đối đơn giản như runtime theo số lượng điểm, so sánh tổng quãng đường, hoặc xuất hình tĩnh cho báo cáo.
5. plotly: cũng là thư viện vẽ biểu đồ, nhưng mạnh ở chỗ tương tác hơn, ví dụ rê chuột xem giá trị, phóng to, thu nhỏ. 
Nếu bạn muốn phần benchmark nhìn hiện đại hơn trong web app thì Plotly thường hợp hơn Matplotlib.
6. pytest: dùng để viết và chạy test cho code Python. Với project này, bạn sẽ dùng nó để test các hàm như tính khoảng cách, solver, brute force, nearest neighbor, 2-opt. 
Nó phù hợp với đúng phần tests/ trong tài liệu của bạn.

python.exe -m pip install --upgrade pip

pip freeze > requirements.txt

streamlit run app.py