import json
import os
from functools import lru_cache
from typing import List, Dict, Optional

from PIL import ImageOps
import numpy as np
from pdf2image import convert_from_path


def walking(fold: str, file_list: List[str]):
    a = os.listdir(fold)
    for j in a:
        j = os.path.join(fold, j)
        if os.path.isfile(j):
            file_list.append(j)
        else:
            walking(j, file_list)


def extract_name(path: str) -> str:
    path = os.path.basename(path)
    loc = path.rfind('.')
    if loc != -1:
        return path[:loc]
    else:
        return path


class NaviChart:
    def __init__(self):
        self.info = dict()
        self.file_path = ''

    def get_pic(self, night_mode: bool) -> Optional[np.ndarray]:
        if not os.path.exists(self.file_path):
            return None
        image = convert_from_path(self.file_path, dpi=360, fmt='png')[0]
        image = np.asarray(image)[:, :, ::-1]
        if night_mode:
            image = (255 - image)[..., ::-1]
        return image


class NaviAirportInfo:
    def __init__(self, data, files_path):
        self.info: dict = data[0]
        self.charts: Dict[str, NaviChart] = dict()  # 键为图表 id

        icao = self.info["icao_airport_identifier"]
        for iChart in data[1:]:
            # 补充信息
            iChart["image_day"] = "{}_d.png".format(iChart["id"])
            iChart["image_night"] = "{}_n.png".format(iChart["id"])
            iChart["thumb_day"] = "{}_d.png".format(iChart["id"])
            iChart["thumb_night"] = "{}_n.png".format(iChart["id"])
            iChart["icao_airport_identifier"] = icao
            http_prefix = "https://api.navigraph.com/v2/charts/{}/".format(icao)
            iChart["image_day_url"] = "{}{}".format(http_prefix, iChart["image_day"])
            iChart["image_night_url"] = "{}{}".format(http_prefix, iChart["image_night"])
            iChart["thumb_day_url"] = "{}{}".format(http_prefix, iChart["thumb_day"])
            iChart["thumb_night_url"] = "{}{}".format(http_prefix, iChart["thumb_night"])
            # 检查本地文件
            file_path = [i for i in files_path if (icao in i) and (iChart["index_number"] in i)]
            if len(file_path) != 1:
                continue
            temp = NaviChart()
            temp.info = iChart
            temp.file_path = file_path[0]
            self.charts[iChart["id"]] = temp

    def get_ap_info(self) -> dict:
        """
        1. 获取机场基本信息
        :return: 机场信息
        """
        return self.info

    def get_ap_charts(self) -> Optional[List[dict]]:
        """
        2. 获取所有图表信息
        :return: 图表信息
        """
        temp = [i.info for i in self.charts.values()]
        return None if len(temp) == 0 else temp

    def get_pic(self, uni_id: str, night_mode: bool) -> Optional[np.ndarray]:
        """
        3. 获取某个图表
        :param uni_id: 图表 ID
        :param night_mode: 采取夜间模式
        :return: 图片本身
        """
        if uni_id not in self.charts:
            return None
        return self.charts[uni_id].get_pic(night_mode)


class NaviInfoManage:
    def __init__(self, chart_folder: str):
        self.aps: Dict[str, NaviAirportInfo] = {}  # 键为 ICAO

        self.all_files: List[str] = []
        walking(chart_folder, self.all_files)

    def load_folder(self, folder: str):
        """
        从一个文件夹路径加载信息
        :param folder: 文件夹
        """
        for file in os.listdir(folder):
            if file.endswith(".Tnavi"):
                self.__load_file(os.path.join(folder, file))

    # 难绷 买的codex真就用一天被封, 还是手写的代码写着舒服 纱暖
    def __load_file(self, file_path: str):
        """
        加载一个文件
        :param file_path: 文件
        """
        with open(file_path, "r", encoding="utf-8") as f:
            ap_data = json.load(f)
        icao = extract_name(file_path)
        self.aps[icao] = NaviAirportInfo(ap_data, [i for i in self.all_files if icao in i])

    def get_available_ap(self) -> List[str]:
        """获取所有可拦截的机场"""
        return list(self.aps.keys())

    def get_ap_info(self, icao: str) -> Optional[dict]:
        """
        1. 获取机场基本信息 (.../v2/airport/YBOK)
        :param icao: ICAO
        :return: 机场信息
        """
        if icao not in self.aps:
            return None
        return self.aps[icao].get_ap_info()

    def get_ap_charts(self, icao: str) -> Optional[Dict[str, List[dict]]]:
        """
        2. 获取所有图表信息 (.../v2/charts/YBOK?version=STD)
        :param icao: ICAO
        :return: 图表信息
        """
        if icao not in self.aps:
            return None
        temp = self.aps[icao].get_ap_charts()
        if temp is None:
            return None
        return {"charts": temp}

    @lru_cache(maxsize=36)
    def get_pic(self, uni_id: str, night_mode: bool) -> Optional[np.ndarray]:
        """
        3. 获取某个图表 (.../v2/charts/YBOK/ybok103_d.png)
        :param uni_id: 图表 ID eg. ybok103
        :param night_mode: 采取夜间模式
        :return: 图片本身
        """
        icao = uni_id[:4].upper()
        if icao not in self.aps:
            return None
        return self.aps[icao].get_pic(uni_id, night_mode)
# https://api.navigraph.com/v2/airport/ZUCK
# https://api.navigraph.com/v2/charts/ZUCK?version=STD
# https://api.navigraph.com/v2/charts/ZUCK/zuck51_d.png
