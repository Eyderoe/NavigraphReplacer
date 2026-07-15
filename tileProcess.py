import json
import math
import os
from typing import Optional
import cv2
import numpy as np


def tile_xyz_to_latlon_bounds(x: int, y: int, z: int) -> tuple:
    """
    根据 OSM 瓦片的 x, y, z 坐标，计算该瓦片左上角和右下角的经纬度。
    :param x: 瓦片列号
    :param y: 瓦片行号
    :param z: 缩放级别
    :return: ((左上角纬度, 左上角经度), (右下角纬度, 右下角经度))
    """

    def tile_to_latlon(tx: int, ty: int, zoom: int) -> tuple:
        n = 2.0 ** zoom
        lon_deg = tx / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ty / n)))
        lat_deg = math.degrees(lat_rad)
        return lat_deg, lon_deg

    top_left = tile_to_latlon(x, y, z)
    bottom_right = tile_to_latlon(x + 1, y + 1, z)
    return top_left, bottom_right


def have_overlap(tile_bound: tuple) -> bool:
    """
    判断瓦片是否与地图多边形存在交集
    tile_bound:
        ((top_lat, left_lon), (bottom_lat, right_lon))
    mapData:
        [[lon, lat], [lon, lat], ...]
    """
    (tile_top_lat, tile_left_lon), (tile_bottom_lat, tile_right_lon) = tile_bound
    tile_rect = np.array([
        [tile_left_lon, tile_top_lat],
        [tile_right_lon, tile_top_lat],
        [tile_right_lon, tile_bottom_lat],
        [tile_left_lon, tile_bottom_lat]
    ], dtype=np.float32)
    tile_min_x = tile_left_lon
    tile_max_x = tile_right_lon
    tile_min_y = tile_bottom_lat
    tile_max_y = tile_top_lat

    def line_intersect(a, b, c, d):
        def cross(v1, v2):
            return v1[0] * v2[1] - v1[1] * v2[0]

        ab = b - a
        ac = c - a
        ad = d - a
        cd = d - c
        ca = a - c
        cb = b - c
        return (
                cross(ab, ac) * cross(ab, ad) <= 0 and
                cross(cd, ca) * cross(cd, cb) <= 0
        )

    for polygon in mapData:
        if len(polygon) < 3:
            continue
        poly = np.array(
            polygon,
            dtype=np.float32
        )
        poly_min_x = np.min(poly[:, 0])
        poly_max_x = np.max(poly[:, 0])
        poly_min_y = np.min(poly[:, 1])
        poly_max_y = np.max(poly[:, 1])
        if (
                tile_max_x < poly_min_x or
                tile_min_x > poly_max_x or
                tile_max_y < poly_min_y or
                tile_min_y > poly_max_y
        ):
            continue
        for p in tile_rect:
            if cv2.pointPolygonTest(
                    poly,
                    (float(p[0]), float(p[1])),
                    False
            ) >= 0:
                return True
        for p in poly:
            if (
                    tile_min_x <= p[0] <= tile_max_x and
                    tile_min_y <= p[1] <= tile_max_y
            ):
                return True
        for i in range(len(poly)):
            p1 = poly[i]
            p2 = poly[(i + 1) % len(poly)]
            for j in range(4):
                t1 = tile_rect[j]
                t2 = tile_rect[(j + 1) % 4]
                if line_intersect(
                        p1,
                        p2,
                        t1,
                        t2
                ):
                    return True
    return False


def cut_from_map(tile_bound: tuple) -> Optional[np.ndarray]:
    """
    根据经纬度范围从矫正后的地图中裁剪区域
    tile_bound:
        ((top_lat, left_lon), (bottom_lat, right_lon))
    返回:
        numpy图片区域
    """
    if rawMap is None:
        return None
    if controlPoints is None or len(controlPoints) < 2:
        return None
    (top_lat, left_lon), (bottom_lat, right_lon) = tile_bound
    x1, y1, lat1, lon1 = controlPoints[0]
    x2, y2, lat2, lon2 = controlPoints[1]
    px_per_lon = (x2 - x1) / (lon2 - lon1)
    px_per_lat = (y2 - y1) / (lat2 - lat1)

    def lon_to_x(lon):
        return x1 + (lon - lon1) * px_per_lon

    def lat_to_y(lat):
        return y1 + (lat - lat1) * px_per_lat

    x0 = int(round(lon_to_x(left_lon)))
    y0 = int(round(lat_to_y(top_lat)))
    x1p = int(round(lon_to_x(right_lon)))
    y1p = int(round(lat_to_y(bottom_lat)))
    xmin = min(x0, x1p)
    xmax = max(x0, x1p)
    ymin = min(y0, y1p)
    ymax = max(y0, y1p)
    h, w = rawMap.shape[:2]
    xmin = max(0, xmin)
    ymin = max(0, ymin)
    xmax = min(w, xmax)
    ymax = min(h, ymax)
    if xmin >= xmax or ymin >= ymax:
        return None
    return rawMap[ymin:ymax, xmin:xmax]


def get_tile(x: int, y: int, z: int) -> Optional[np.ndarray]:
    """
    获取地图瓦片 OSM 格式
    :param x: 瓦片列号
    :param y: 瓦片行号
    :param z: 缩放级别
    :return: 可能的返回一张图片
    """
    if z < 5 or z > 13:
        return None
    bound = tile_xyz_to_latlon_bounds(x, y, z)
    if not have_overlap(bound):
        return None
    tile = cut_from_map(bound)
    if tile is None:
        return None
    tile = cv2.resize(tile, (256, 256), interpolation=cv2.INTER_AREA)
    return tile


_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
mapData = None
rawMap = None
controlPoints = None
_DEFAULT_CONTROL_POINTS = [
    [3142, 7472, 46, 80],
    [18878, 16910, 22, 120]
]
_last_border_file = None
_last_map_file = None
_last_points = None


def init_tile_process(border_file: str, map_file: str, points: list = None):
    """
    初始化瓦片处理模块，从指定路径加载国境线文件和航图文件
    :param border_file: 国境线 JSON 文件路径
    :param map_file: 航图图片文件路径
    :param points: 控制点列表，格式为 [[x1, y1, lat1, lon1], [x2, y2, lat2, lon2]]
                   如果为 None，则使用默认值
    """
    global mapData, rawMap, controlPoints, _last_border_file, _last_map_file, _last_points
    _last_border_file = border_file
    _last_map_file = map_file
    _last_points = points
    with open(border_file, 'r') as f:
        mapData = json.load(f)
    rawMap = cv2.imdecode(
        np.fromfile(map_file, dtype=np.uint8),
        cv2.IMREAD_COLOR
    )
    controlPoints = points if points is not None else _DEFAULT_CONTROL_POINTS


def get_tile_config():
    """获取当前的瓦片配置，用于传递给子进程"""
    return {
        'border_file': _last_border_file,
        'map_file': _last_map_file,
        'points': _last_points
    }


if os.environ.get('OSM_TILE_BORDER_FILE') and os.environ.get('OSM_TILE_MAP_FILE'):
    border_file = os.environ['OSM_TILE_BORDER_FILE']
    map_file = os.environ['OSM_TILE_MAP_FILE']
    points_env = os.environ.get('OSM_TILE_POINTS')
    points = None
    if points_env:
        points = json.loads(points_env)
    print(f"[tileProcess] 从环境变量初始化: border={border_file}, map={map_file}, points={points}")
    init_tile_process(border_file, map_file, points)
    print(
        f"[tileProcess] 初始化完成: mapData={mapData is not None}, rawMap={rawMap is not None}, controlPoints={controlPoints is not None}")
