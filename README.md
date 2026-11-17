## Navigraph 替换

通过拦截和替换部分信息, 来实现加载本地航图或地图瓦片。一个简单的数据示例放 release 供参考

### 适用范围

替换分为两种, mitmproxy 和本地 hosts
- mitmproxy 配置要麻烦一些, 通过修改部分请求数据来实现替换
- hosts 配置比较简单, 但会直接覆盖所有 Navigraph 服务, 比如 Navi 的航路图和桌面端等

对于不同的应用, 要求也不同。但至少应该都能通过 hosts+XPlane 命令行启动解决
- ToLiss EFB：独立的应用, 对于没有订阅的用户 mitproxy 好像不太行, 但 hosts 无所谓
- Falcon8X ND：没问题, 但需要通过命令行启动 XPlane 来生效

### OpenStreetMap

地图的瓦片数据, 请求很简单

```
https://tile.openstreetmap.org/8/203/105.png
```

程序会替换处于国境线内的地图瓦片数据, 虽然理论上用的是 Web Mercator, 但在范围内用其他的比如正轴圆柱投影其实问题也不大

### Navigraph Chart

稍微麻烦一点, 有三份数据需要准备。

```
https://api.navigraph.com/v2/airport/ZUCK
https://api.navigraph.com/v2/charts/ZUCK?version=STD
https://api.navigraph.com/v2/charts/ZUCK/zuck51_d.png
```

1. 机场基本信息
2. 航图列表, 假如被替换 则一定是 STD
3. 航图本身, 程序是按 dpi360 进行的渲染

具体参数设置可以在 Navi 的[开发网站](https://developers.navigraph.com/docs/charts/airport-charts)找到

对于国内机场图不太喜欢真北朝上的习惯, 可以通过新增字段的方式（仿射变换参数）, 以正确形式返回请求

```
"sp_chart_rotate_information_record": {
  "pixel_to_geo_matrix": [
  	[a, b, c],
  	[d, e, f]
  ]
}

经度 = ax + by + c
纬度 = dx + ey + f
```

