import pystache

class WebApp:

    def __init__(self):

    def render_database(self, )

# Load html template for rendering
    template = ""
    with open(os.path.join('app','index.html'),"r") as fconv:
        template = fconv.read()

    # Define the render context from the processed histograms, images, and stats
    context = {}
    context['version'] = '1.0.1.05'
    context['total_images'] = total_images
    context['proc_time'] = proc_time
    context['duration'] = total_seconds
    context['compression_ratio'] = int((1000.0*24*total_images)/np.sum(file_size))
    context['rois_per_second'] = total_images/context['duration']
    context['kb_per_second'] = int(np.sum(file_size)/context['duration'])
    context['recording_started'] = datetime.datetime.fromtimestamp(np.min(unixtime)).strftime('%Y-%m-%d %H:%M:%S')
    context['app_title'] = "SPC Convert: " + base_dir_name
    context['dir_name'] = base_dir_name
    context['raw_color'] = raw_color
    context['image_res'] = image_res
    if use_jpeg:
        context['image_ext'] = '.jpeg'
    else:
        context['image_ext'] = '.png'
    context['stats_names'] = [{"name":"Min"},{"name":"Max"},{"name":"Mean"},{"name":"Standard Deviation"},{"name":"Skewness"},{"name":"Kurtosis"}]

        # definie the charts to display from the histogram data
    charts = []
    for chart_name, data_values in all_hists.items():
        chart = {}
        chart['source'] = 'js/' + chart_name + '.js'
        chart['name'] = chart_name
        units = ""
        if chart_name == 'area':
            units = " (mm*mm)"
        if chart_name == 'major_axis_length' or chart_name == 'minor_axis_length':
            units = " (mm)"
        if chart_name == 'file_size':
            units = " (kB)"
        if chart_name == 'elapsed_seconds':
            units = " (s)"
        if chart_name == 'orientation':
            units = " (deg)"
        chart['title'] = 'Histogram of ' + chart_name + units
        chart['x_title'] = chart_name + units
        chart['y_title'] = 'counts'
        chart['stats_title'] = chart_name
        chart['data'] = data_values
        chart['stats'] = []
        chart['stats'].append({"name":"Min","value":"{:10.3f}".format(all_stats[chart_name][1][0])})
        chart['stats'].append({"name":"Max","value":"{:10.3f}".format(all_stats[chart_name][1][1])})
        chart['stats'].append({"name":"Mean","value":"{:10.3f}".format(all_stats[chart_name][2])})
        chart['stats'].append({"name":"Standard Deviation","value":"{:10.3f}".format(math.sqrt(all_stats[chart_name][3]))})
        chart['stats'].append({"name":"Skewness","value":"{:10.3f}".format(all_stats[chart_name][4])})
        chart['stats'].append({"name":"Kurtosis","value":"{:10.3f}".format(all_stats[chart_name][5])})
        charts.append(chart)

    context['charts'] = charts
    
    # render the html page and save to disk
    page = pystache.render(template,context)