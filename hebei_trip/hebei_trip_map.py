import folium
from folium import plugins
from datetime import datetime, timedelta

# 创建地图，以河北省为中心
m = folium.Map(location=[39.3, 116.7], zoom_start=7)

# 定义城市和景点数据
cities = {
    '北京': {
        'location': [39.904179, 116.407387],
        'is_city': True,
        'day': [0, 14]
    },
    '承德': {
        'location': [40.952942, 117.962749],
        'is_city': True,
        'day': [1, 2],
        'attractions': [
            {'name': '避暑山庄', 'location': [40.986006, 117.936326]},
            {'name': '普陀宗乘之庙', 'location': [40.975256, 117.941744]},
            {'name': '普宁寺', 'location': [40.978837, 117.949726]}
        ]
    },
    '秦皇岛': {
        'location': [39.888243, 119.520220],
        'is_city': True,
        'day': [3, 4],
        'attractions': [
            {'name': '山海关', 'location': [40.003639, 119.754911]},
            {'name': '北戴河', 'location': [39.825120, 119.518639]},
            {'name': '老龙头', 'location': [39.969570, 119.797391]}
        ]
    },
    '唐山': {
        'location': [39.630680, 118.180149],
        'is_city': True,
        'day': [5],
        'attractions': [
            {'name': '唐山地震遗址纪念公园', 'location': [39.630505, 118.180147]},
            {'name': '南湖生态城', 'location': [39.615833, 118.174722]}
        ]
    },
    '廊坊': {
        'location': [39.538304, 116.683546],
        'is_city': True,
        'day': [6],
        'attractions': [
            {'name': '大厂影视基地', 'location': [39.886389, 116.986944]},
            {'name': '永清温泉', 'location': [39.321389, 116.499444]}
        ]
    },
    '保定': {
        'location': [38.874476, 115.464523],
        'is_city': True,
        'day': [7, 8],
        'attractions': [
            {'name': '白洋淀', 'location': [38.938914, 115.978436]},
            {'name': '清西陵', 'location': [39.133333, 115.216667]}
        ]
    },
    '石家庄': {
        'location': [38.042007, 114.514976],
        'is_city': True,
        'day': [9, 10],
        'attractions': [
            {'name': '西柏坡纪念馆', 'location': [38.346344, 113.847172]},
            {'name': '正定古城', 'location': [38.144269, 114.574173]},
            {'name': '隆兴寺', 'location': [38.146111, 114.571944]}
        ]
    },
    '邯郸': {
        'location': [36.625849, 114.539150],
        'is_city': True,
        'day': [11, 12],
        'attractions': [
            {'name': '响堂山石窟', 'location': [36.558611, 114.216667]},
            {'name': '娲皇宫', 'location': [36.537778, 114.066667]}
        ]
    },
    '张家口': {
        'location': [40.768931, 114.885895],
        'is_city': True,
        'day': [13],
        'attractions': [
            {'name': '崇礼滑雪场', 'location': [40.975278, 115.282778]},
            {'name': '察哈尔民俗博物馆', 'location': [40.766667, 114.883333]}
        ]
    }
}

# 创建行程路线
route = ['北京', '承德', '秦皇岛', '唐山', '廊坊', '保定', '石家庄', '邯郸', '张家口', '北京']

# 添加城市标记
for city_name, city_data in cities.items():
    # 为城市添加标记
    color = 'red' if city_name == '北京' else 'blue'
    folium.CircleMarker(
        location=city_data['location'],
        radius=8,
        color=color,
        fill=True,
        popup=city_name
    ).add_to(m)
    
    # 添加景点标记
    if 'attractions' in city_data:
        for attraction in city_data['attractions']:
            folium.Marker(
                location=attraction['location'],
                popup=f"{attraction['name']} ({city_name})",
                icon=folium.Icon(color='green', icon='info-sign')
            ).add_to(m)

# 添加路线连接
coordinates = []
for city_name in route:
    coordinates.append(cities[city_name]['location'])

# 使用不同颜色的线条连接城市
folium.PolyLine(
    coordinates,
    weight=2,
    color='red',
    opacity=0.8
).add_to(m)

# 添加图例
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 150px; height: 90px; 
            border:2px solid grey; z-index:9999; 
            background-color:white;
            padding: 10px;
            font-size: 14px;">
    <p><i class="fa fa-circle" style="color:red"></i> 起点/终点（北京）</p>
    <p><i class="fa fa-circle" style="color:blue"></i> 途经城市</p>
    <p><i class="fa fa-info-circle" style="color:green"></i> 景点</p>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# 添加行程说明
start_date = datetime(2024, 5, 6)  # 设置起始日期
schedule_html = '''
<div style="position: fixed; 
            top: 50px; right: 50px; width: 200px;
            border:2px solid grey; z-index:9999; 
            background-color:white;
            padding: 10px;
            font-size: 14px;
            max-height: 400px;
            overflow-y: auto;">
    <h4>行程安排：</h4>
'''

for i, city_name in enumerate(cities):
    city_data = cities[city_name]
    if 'day' in city_data:
        for day in city_data['day']:
            if day > 0:  # 跳过起点的第0天
                date = start_date + timedelta(days=day-1)
                schedule_html += f"<p><b>{date.strftime('%m月%d日')} (第{day}天)</b><br>"
                schedule_html += f"{city_name}"
                if 'attractions' in city_data:
                    schedule_html += ":<br>"
                    for attraction in city_data['attractions']:
                        schedule_html += f"- {attraction['name']}<br>"
                schedule_html += "</p>"

schedule_html += '</div>'
m.get_root().html.add_child(folium.Element(schedule_html))

# 保存地图
m.save('hebei_trip_map.html')