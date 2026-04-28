import math  # dùng để kiểm tra số thực gần bằng nhau

from core.distance import build_distance_matrix, haversine_distance  # import các hàm cần test
from core.models import Point  # import model Point
from data.sample_points import get_sample_points  # lấy dữ liệu mẫu để test


def test_haversine_distance_same_point_is_zero():
    """
    Test 1:
    Khoảng cách từ một điểm tới chính nó phải bằng 0.
    """
    point = Point(id=0, name="A", lat=10.7769, lng=106.7009)  # tạo 1 điểm mẫu

    distance = haversine_distance(point, point)  # tính khoảng cách từ điểm đó tới chính nó

    assert math.isclose(distance, 0.0, abs_tol=1e-9)  # kiểm tra khoảng cách gần bằng 0


def test_haversine_distance_is_symmetric():
    """
    Test 2:
    Khoảng cách từ A tới B phải bằng khoảng cách từ B tới A.
    """
    point_a = Point(id=0, name="A", lat=10.7769, lng=106.7009)  # điểm A
    point_b = Point(id=1, name="B", lat=10.7828, lng=106.6953)  # điểm B

    distance_ab = haversine_distance(point_a, point_b)  # khoảng cách A -> B
    distance_ba = haversine_distance(point_b, point_a)  # khoảng cách B -> A

    assert math.isclose(distance_ab, distance_ba, rel_tol=1e-9)  # kiểm tra tính đối xứng


def test_build_distance_matrix_shape_matches_number_of_points():
    """
    Test 3:
    Ma trận khoảng cách phải có kích thước n x n với n là số lượng điểm.
    """
    points = get_sample_points()  # lấy bộ điểm mẫu
    matrix = build_distance_matrix(points)  # tạo ma trận khoảng cách

    n = len(points)  # số lượng điểm

    assert len(matrix) == n  # số dòng phải bằng n
    assert all(len(row) == n for row in matrix)  # mỗi dòng phải có đúng n cột


def test_build_distance_matrix_diagonal_is_zero():
    """
    Test 4:
    Đường chéo chính của ma trận phải bằng 0,
    vì khoảng cách từ một điểm tới chính nó là 0.
    """
    points = get_sample_points()  # lấy bộ điểm mẫu
    matrix = build_distance_matrix(points)  # tạo ma trận khoảng cách

    for i in range(len(points)):  # duyệt từng phần tử trên đường chéo
        assert math.isclose(matrix[i][i], 0.0, abs_tol=1e-9)  # kiểm tra gần bằng 0


def test_build_distance_matrix_is_symmetric():
    """
    Test 5:
    Ma trận khoảng cách phải gần đối xứng,
    tức matrix[i][j] gần bằng matrix[j][i].
    """
    points = get_sample_points()  # lấy bộ điểm mẫu
    matrix = build_distance_matrix(points)  # tạo ma trận khoảng cách

    n = len(points)  # số lượng điểm

    for i in range(n):  # duyệt từng dòng
        for j in range(n):  # duyệt từng cột
            assert math.isclose(matrix[i][j], matrix[j][i], rel_tol=1e-9)  # kiểm tra đối xứng