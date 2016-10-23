with open('~/busdata/Route2092.txt', 'r') as route_file:
    day_number = 0
    day_data = ''
    empty_brace_count = 0
    consume_mode = False

    for line in route_file:
        if line == '[]\n' or '"UpdatedAgo":""' in line:
            if not consume_mode:
                empty_brace_count+=1
        else:
            consume_mode = False # We see data now, stop consuming
            day_data += line
        if empty_brace_count > 1290:
            day_number+=1
            file_name = ('~/busdata/Fri1014/boop_' +
                str(day_number) + '.txt')
            print file_name
            with open(file_name, 'w') as data_file:
                data_file.write(day_data)
            day_data = ''
            empty_brace_count = 0
            consume_mode = True # Start consuming the rest of the square brackets

    day_number += 1
    file_name = ('~/busdata/Fri1014/boop_' +
                 str(day_number) + '.txt')
    print file_name
    with open(file_name, 'w') as data_file:
        data_file.write(day_data)
