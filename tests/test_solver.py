import pytest  # dùng framework pytest để viết test và kiểm tra exception

from core.models import Point  # import model Point
from core.solver import BRUTE_FORCE_LIMIT, run_solver  # import solver và ngưỡng brute force
from data.sample_points import get_sample_points  # lấy bộ điểm mẫu để test


def test_run_solver_nearest_neighbor_returns_closed_route():
    """
    Test 1:
    Solver với thuật toán nearest_neighbor phải trả về route khép kín.
    """
    points = get_sample_points()  # lấy bộ điểm mẫu
    result = run_solver(points, "nearest_neighbor")  # chạy solver với nearest neighbor

    assert result.route[0] == result.route[-1]  # route phải bắt đầu và kết thúc cùng một điểm
    assert len(result.route) == len(points) + 1  # route khép kín nên dài hơn số điểm đúng 1 phần tử
    assert result.total_distance_km > 0  # tổng quãng đường phải dương


def test_run_solver_two_opt_returns_closed_route():
    """
    Test 2:
    Solver với thuật toán two_opt phải trả về route khép kín.
    """
    points = get_sample_points()  # lấy bộ điểm mẫu
    result = run_solver(points, "two_opt")  # chạy solver với 2-opt

    assert result.route[0] == result.route[-1]  # route phải khép kín
    assert len(result.route) == len(points) + 1  # số phần tử route phải đúng
    assert result.total_distance_km > 0  # tổng quãng đường phải dương


def test_run_solver_bruteforce_returns_closed_route_for_small_input():
    """
    Test 3:
    Solver với brute force phải chạy được khi số điểm nhỏ hơn hoặc bằng ngưỡng cho phép.
    """
    points = get_sample_points()  # bộ điểm hiện tại chỉ có 5 điểm, đủ nhỏ để brute force chạy
    result = run_solver(points, "bruteforce")  # chạy brute force qua solver

    assert result.route[0] == result.route[-1]  # route phải khép kín
    assert len(result.route) == len(points) + 1  # độ dài route phải đúng
    assert result.total_distance_km > 0  # tổng quãng đường phải dương


def test_run_solver_rejects_less_than_two_points():
    """
    Test 4:
    Nếu ít hơn 2 điểm thì solver phải báo lỗi.
    """
    points = [Point(id=0, name="Only One", lat=10.7769, lng=106.7009)]  # chỉ có 1 điểm

    with pytest.raises(ValueError):  # kỳ vọng hàm sẽ ném ra lỗi ValueError
        run_solver(points, "nearest_neighbor")  # thử chạy solver


def test_run_solver_rejects_invalid_algorithm_name():
    """
    Test 5:
    Nếu truyền tên thuật toán không hợp lệ thì solver phải báo lỗi.
    """
    points = get_sample_points()  # lấy bộ điểm mẫu

    with pytest.raises(ValueError):  # kỳ vọng có lỗi vì tên thuật toán sai
        run_solver(points, "abc_xyz")  # tên thuật toán không tồn tại


def test_run_solver_bruteforce_rejects_input_over_limit():
    """
    Test 6:
    Brute force phải bị chặn khi số điểm vượt quá BRUTE_FORCE_LIMIT.
    """
    points = []  # tạo danh sách điểm rỗng trước

    # tạo số điểm lớn hơn ngưỡng brute force 1 đơn vị
    for i in range(BRUTE_FORCE_LIMIT + 1):
        points.append(
            Point(
                id=i,  # id điểm
                name=f"Point {i}",  # tên điểm
                lat=10.70 + i * 0.001,  # tạo lat khác nhau một chút
                lng=106.60 + i * 0.001,  # tạo lng khác nhau một chút
            )
        )

    with pytest.raises(ValueError):  # kỳ vọng brute force bị chặn và báo lỗi
        run_solver(points, "bruteforce")  # thử chạy brute force vượt ngưỡng


def test_run_solver_two_points_returns_valid_route():
    """
    Test 7:
    Với đúng 2 điểm, solver phải trả về route hợp lệ dạng 0 -> 1 -> 0.
    """
    points = [
        Point(id=0, name="A", lat=10.7769, lng=106.7009),  # điểm đầu
        Point(id=1, name="B", lat=10.7828, lng=106.6953),  # điểm thứ hai
    ]

    result = run_solver(points, "nearest_neighbor")  # chạy solver với 2 điểm

    assert result.route == [0, 1, 0]  # route hợp lệ duy nhất trong trường hợp 2 điểm
    assert result.total_distance_km > 0  # tổng quãng đường phải dương