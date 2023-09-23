def add_to_dict(data):
    news_dict = {}
    i = 0
    while i < len(data) - 7:
        news_dict[data[i]] = {
            'id': data[i][-(len(data[i])-2)//2:],
            'title': data[i + 1],
            'description': data[i + 2],
            'category_id': data[i + 3],
            'author_id': data[i + 4],
            'photo': data[i + 5],
            'coord_lat': data[i + 6],
            'coord_lon': data[i + 7],
        }
        i += 8
        print((len(data[i])-2)//2)
    return news_dict