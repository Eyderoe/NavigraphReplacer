## Navigraph 替换

通过 mitmproxy 拦截和替换部分信息，Navi 免费的账号也能使用，不需要额外订阅 Ultra。一个简单的数据示例放 release 供参考

### 已进行测试

假如账号已有付费订阅，一般没问题。这里只针对免费账号的测试

- ToLiss EFB：最新版本需要有效 Navi 订阅，还没解决
- Falcon8X ND：没问题，但需要但命令行的启动 XPlane

### OpenStreetMap

地图的瓦片数据，请求很简单

```
https://tile.openstreetmap.org/8/203/105.png
```

程序会替换处于国境线内的地图瓦片数据，虽然理论上用的是 Web Mercator，但在范围内用其他的比如正轴圆柱投影其实问题也不大

### Navigraph Chart

稍微麻烦一点，有三份数据需要准备。

```
https://api.navigraph.com/v2/airport/ZUCK
https://api.navigraph.com/v2/charts/ZUCK?version=STD
https://api.navigraph.com/v2/charts/ZUCK/zuck51_d.png
```

1. 机场基本信息
2. 航图列表，假如被替换 则一定是 STD
3. 航图本身，程序是按 dpi360 进行的渲染

具体参数设置可以在 Navi 的[开发网站](https://developers.navigraph.com/docs/charts/airport-charts)找到

对于国内机场图不太喜欢真北朝上的习惯，可以通过新增字段的方式（6元素），以正确形式返回请求

```json
"sp_chart_rotate_information_record": {
  "pixel_to_geo_matrix": [
    [a, b, c],
    [d, e, f]
  ]
}

经度 = ax + by + c
纬度 = dx + ey + f
```

