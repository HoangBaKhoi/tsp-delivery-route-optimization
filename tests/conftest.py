import sys  # dùng để thao tác với danh sách đường dẫn import của Python
from pathlib import Path  # dùng để xử lý đường dẫn thư mục dễ hơn


# lấy thư mục gốc của project:
# file hiện tại là tests/conftest.py
# .parent là tests/
# .parent.parent là thư mục project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent


# nếu project root chưa có trong sys.path thì thêm vào đầu danh sách
# để pytest có thể import được các package như core, data, ui...
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))