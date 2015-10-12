# Eye Tracking Data to Visualization using Bokeh

from __future__ import print_function
import sys


#data_folder = 'data/'
#data_output_file = 'data_out.html'
data = {}

def main():
    data_folder = sys.argv[1]
    data_output_file = sys.argv[2]
    parse_data(data_folder)
    visualize_data(data_output_file)


def comparator(x, y):
    if 'Line' in x:
        if 'Line' in y:
            return cmp(x[5:], y[5:])
        if 'Step' in y:
            return -1
        if 'Directions' in y:
            return -1

    if 'Step' in x:
        if 'Line' in y:
            return 1
        if 'Step' in y:
            return cmp(x[5:], y[5:])
        if 'Directions' in y:
            return -1

    if 'Directions' in x:
        if 'Line' in y:
            return 1
        if 'Step' in y:
            return 1
        if 'Directions' in y:
            return 0


def parse_data(data_folder):
    from os import listdir

    data_ls = listdir(data_folder)

    for data_file in data_ls:
        with open(data_folder + data_file, 'r') as f:
            file_data_list = []

            time_sum = 0
            for line in f:
                split_line = line.split(', ')
                # line_type, time, start_time, end_time, desc
                line_triple = (split_line[0], int(split_line[1]), \
                    time_sum, time_sum + int(split_line[1]), split_line[2][:-1])
                file_data_list.append(line_triple)
                time_sum += line_triple[1]

            #file_data_list.sort(cmp=comparator, key=lambda x: x[0])
        
        data[data_file] = file_data_list

    with open('outfile.txt', 'w') as f:
        for data_item in data.iteritems():
            f.write(str(data_item) + '\n')


def visualize_data(data_output_file):
    from bokeh.plotting import figure, output_file, save, vplot
    from bokeh.models import ColumnDataSource, FactorRange

    plots = []

    # output to static HTML file
    output_file(data_output_file, title='Eye Tracking Data', mode='cdn')

    for file_name, file_data in data.iteritems():
        # prepare the data
        line_types = [line_data[0] for line_data in file_data]
        #line_types_top = [line_data[0] + '2.0' for line_data in file_data]
        #line_types_bot = [line_data[0] + '1.0' for line_data in file_data]
        times = [line_data[1] for line_data in file_data]
        start_times = [line_data[2] for line_data in file_data]
        end_times = [line_data[3] for line_data in file_data]
        descs = [line_data[4] for line_data in file_data]

        #x0 = [0 for type_ in line_types]

        '''source = ColumnDataSource({
            'time': times,
            'start': start_times,
            'end': end_times,
            'line_types_top': line_types_top,
            'line_types_bot': line_types_bot,
        })'''

        source = ColumnDataSource({
            'x': [(t1 + t2)/2 for t1, t2 in zip(start_times, end_times)],
            'y': line_types,
            'width': times,
            'height': [0.7 for _ in line_types],
            'fill_color': ['red' if 'Incorrect' in desc \
                    else 'green' for desc in descs]
        })

        # create a new plot
        plot = figure(
           tools='pan,reset,save',
           title=file_name, y_range=FactorRange(factors=line_types[::-1]),
           x_range=[0, sum(times)],
           x_axis_label='Time (ms)', y_axis_label='Line Type'
        )

        plot.rect(x='x', y='y', width='width', height='height', \
            fill_color='fill_color', source=source)

        #plot.quad(left='start', right='end', \
        #    top='line_types_top', bottom='line_types_bot', source=source)
    
        # add some renderers
        #plot.segment(x0, line_types, times, line_types, \
        #    line_width=2, line_color="green")

        plots.append(plot)

    # show the results
    save(vplot(*plots))


if __name__ == '__main__':
    main()
