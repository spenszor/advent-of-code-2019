height = 6
width = 25
with open('./inputs/day08') as data:
    raw = list(data.readline().strip())
    offset = 0
    layers = []
    while offset < len(raw):
        layer = []
        for h in range(height):
            idx = offset + width
            layer.append(raw[offset:idx])
            offset = idx
        layers.append(layer)
    # part one
    zero_count = width * height
    best_layer = []
    for layer in layers:
        total = sum(row.count('0') for row in layer)
        if total < zero_count:
            zero_count = total
            best_layer = layer
    ones = sum(row.count('1') for row in best_layer)
    twos = sum(row.count('2') for row in best_layer)
    print(ones * twos)

    #part two
    image = []
    for h in range(height):
        row = []
        for w in range(width):
            for layer in layers:
                if layer[h][w] == '1' or layer[h][w] == '0':
                    row.append(layer[h][w])
                    break
        image.append(row)
    for row in image:
        t = ''
        for c in row:
            if c == '1':
                t += 'I'
            else:
                t += ' '
        print(t)



