from zheye import zheye
z = zheye()
positions = z.Recognize('zhihu_image/a.gif')

last_position = []
if len(positions) == 2:
    if positions[0][1] > positions[1][1]:   # 按照顺序排列倒立文字坐标
        last_position.append([positions[1][1], positions[1][0]])
        last_position.append([positions[0][1], positions[0][1]])
    else:
        last_position.append([positions[0][1], positions[0][1]])
        last_position.append([positions[1][1], positions[1][0]])
else:  # 如果只有一个倒立文字
    last_position.append([positions[0][1], positions[0][1]])
print(last_position)