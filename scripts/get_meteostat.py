import base64
from io import BytesIO
from meteostat import Point, Daily
from datetime import datetime
import matplotlib.pyplot as plt


def get_meteostat_data_detailed(title = "Vancouver", lat=49.2497, lon=-123.1193):
    start = datetime(2021, 1, 1)
    end = datetime(2021, 12, 31)
    vancouver = Point(lat, lon, 70)
    data = Daily(vancouver, start, end)

    #plots
    color = ['#1fc46a','#1f7dc4', '#e6de10']
    ylabel = 'temperature, C'
    title_all = title + " daily temperature(t) data of 2021"
    title_avg = title + " average daily temperature of 2021"
    title_min = title + " minimum daily temperature of 2021"
    title_max = title + " maximum daily temperature of 2021"
    data = data.fetch()
    data4 = data

    #csv plot and images
    for_csv = data.to_csv(encoding='utf-8', index=True).replace('tsun\n','tsun\n%0A').replace(',\n', 'y%0A')
    data0 = data.plot(y=['tavg', 'tmin', 'tmax'], color=color, ylabel=ylabel, xlabel='time', title=title_all)
    data1 = data.plot(y=['tavg'], color=color[0], ylabel=ylabel, xlabel='time', title=title_avg)
    data2 = data.plot(y=['tmin'], color=color[1], ylabel=ylabel, xlabel='time', title=title_min)
    data3 = data.plot(y=['tmax'], color=color[2], ylabel=ylabel, xlabel='time', title=title_max)
    
    #for pdf. plotting into one figure
    fig, axes = plt.subplots(nrows=4)
    fig.set_size_inches(6, 19)
    data4.plot(y=['tavg', 'tmin', 'tmax'], ylabel=ylabel, ax=axes[0], color=color, title=title_all)
    data4.plot(y=['tavg'], ax=axes[1], ylabel=ylabel, legend=False, color=color[0], title=title_avg)
    data4.plot(y=['tmin'], ax=axes[2], ylabel=ylabel, legend=False, color=color[1], title=title_min)
    data4.plot(y=['tmax'], ax=axes[3], ylabel=ylabel, legend=False, color=color[2], title=title_max)
    fig.tight_layout()
    #part of saving plots
    data0 = data0.get_figure()
    data1 = data1.get_figure()
    data2 = data2.get_figure()
    data3 = data3.get_figure()
    data4 = fig.get_figure()

    # Save it to a temporary buffer.
    buf0 = BytesIO()
    buf1 = BytesIO()
    buf2 = BytesIO()
    buf3 = BytesIO()
    buf4 = BytesIO()
    
    #save w format
    data0.savefig(buf0, format="png", bbox_inches='tight')
    data1.savefig(buf1, format="png", bbox_inches='tight')
    data2.savefig(buf2, format="png", bbox_inches='tight')
    data3.savefig(buf3, format="png", bbox_inches='tight')
    fig.savefig(buf4, format="pdf", bbox_inches='tight')

    #decode and release memory by closing buffers
    data0 = base64.b64encode(buf0.getbuffer()).decode("utf-8")
    data1 = base64.b64encode(buf1.getbuffer()).decode("utf-8")
    data2 = base64.b64encode(buf2.getbuffer()).decode("utf-8")
    data3 = base64.b64encode(buf3.getbuffer()).decode("utf-8")
    buf0.close()
    buf1.close()
    buf2.close()
    buf3.close()

    data4 = base64.b64encode(buf4.getbuffer()).decode('utf-8')
    buf4.close()
    
    #in data4 we have pdf, before that - imgs
    data = {
      'for_csv' : for_csv,
      'data0' : data0,
      'data1' : data1,
      'data2' : data2,
      'data3' : data3,
      'data4' : data4
    }
    return data