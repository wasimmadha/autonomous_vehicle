import pandas as pd
import warnings
import os

stop_df = pd.DataFrame()
def warn(*args, **kwargs):
    pass
warnings.warn = warn

df = pd.DataFrame(columns=['image', 'label'])

def create_columns_for_imagedf(text, date = True):
    sep = '.'

    if(date == True):
        stripped = text.split(sep, 1)[0]
        stripped = stripped.replace('-', '/')
        return (stripped)
    else:
        stripped = text.split(sep, 1)[1][:4]
        stripped = float(stripped)/10000
        return stripped

def prepare_clean_datasamples(sample_no, sample_images, sample_ir, start_timeStamp, end_timeStamp):
    
    global df
    last_sample = df.shape[0]

    sample_images['milliseconds'] = sample_images['time'].apply(create_columns_for_imagedf, date=False)
    sample_images['trimmed_date'] = sample_images['time'].apply(create_columns_for_imagedf)

    sample_images['trimmed_date'] = pd.to_datetime(sample_images['trimmed_date'])

    sample_ir['timeStamp'] = pd.to_datetime(sample_ir['timeStamp'])

    sample_ir = sample_ir.loc[((sample_ir['timeStamp'] > start_timeStamp) & (sample_ir['timeStamp'] < end_timeStamp))]
    sample_images = sample_images.loc[((sample_images['trimmed_date'] > start_timeStamp) & (sample_images['trimmed_date'] < end_timeStamp))]

    unique_date_values = sample_images['trimmed_date'].unique()

    sample_ir.loc[sample_ir['timeStamp'] == start_timeStamp]

    for i in unique_date_values:
        unique_ir = sample_ir.loc[sample_ir['timeStamp'] == i]
        number_of_ir = unique_ir.shape[0]

        j = 0
        range_values = []
        while j < number_of_ir:
            range_values.append((1/number_of_ir)*j)
            j += 1

        label_idx = 0

        for k, single_range in enumerate(range_values):
            if k == 0:
                first_range = 0.0
                second_range = range_values[k]
            elif k == (len(range_values)) - 1:
                first_range = range_values[k]
                second_range = 1.0
            else:
                first_range = range_values[k]
                second_range = range_values[k+1]
            label = unique_ir.iloc[label_idx]['ACTION']
            label_idx += 1
            
            data = sample_images.loc[((sample_images['trimmed_date'] == i ) & (((sample_images['milliseconds']) > first_range) & ((sample1_images['milliseconds']) < second_range)))]
            images = data['image'].values
            if(len(images) != 0):
                for image in (images):
                    data_point = {
                        
                        'image' : os.path.join(rf'Data Samples\DataSamples-{sample_no}', image),
                        'label' : label
                    }
                    df = df.append(data_point, ignore_index=True)
    print(f"The records added for Sample-{sample_no} are {df.shape[0] - last_sample}")
    df.to_csv(r'Data Samples\data.csv', index=False)

timeFrame = {
    1 : {
        "start_timeStamp" : '2022-08-17 01:18:51',
        "end_timeStamp" : '2022-08-17 01:19:39'
    },
    2: {
        "start_timeStamp" : '2022-08-17 01:49:10',
        "end_timeStamp" : '2022-08-17 01:50:54'
    },
    3: {
        "start_timeStamp" : '2022-08-17 01:57:32',
        "end_timeStamp" : '2022-08-17 01:58:06'
    }
    ,
    4: {
        "start_timeStamp" : '2022-08-17 01:58:39',
        "end_timeStamp" : '2022-08-17 01:59:13'
    },
    5: {
        "start_timeStamp" : '2022-08-17 02:01:20',
        "end_timeStamp" : '2022-08-17 02:02:10'
    },
    6: {
        "start_timeStamp" : '2022-08-17 02:03:45',
        "end_timeStamp" : '2022-08-17 02:04:12'
    },
    7: {
        "start_timeStamp" : '2022-08-17 02:04:59',
        "end_timeStamp" : '2022-08-17 02:05:46'
    },
    8: {
        "start_timeStamp" : '2022-08-17 02:06:19',
        "end_timeStamp" : '2022-08-17 02:07:08'
    }
}

for i in range(1, 9):
    sample1_ir = pd.read_csv(rf'C:\Users\wasim\line-following\Data Samples\DataSamples-{i}\data_ir.csv')
    sample1_images = pd.read_csv(rf'C:\Users\wasim\line-following\Data Samples\DataSamples-{i}\out_images.csv')

    prepare_clean_datasamples(sample_no = i, sample_images=sample1_images, sample_ir=sample1_ir, start_timeStamp=timeFrame[i]["start_timeStamp"], end_timeStamp=timeFrame[i]["end_timeStamp"])

# # Data Sample 1 
# sample1_ir = pd.read_csv(r'C:\Users\wasim\line-following\Data Samples\DataSamples-1\data_ir.csv')
# sample1_images = pd.read_csv(r'C:\Users\wasim\line-following\Data Samples\DataSamples-1\out_images.csv')

# start_timeStamp = '2022-08-17 01:18:51'
# end_timeStamp = '2022-08-17 01:19:39' 
# prepare_clean_datasamples(sample_images=sample1_images, sample_ir=sample1_ir, start_timeStamp=start_timeStamp, end_timeStamp=end_timeStamp)

# # Data Sample 2
# sample2_ir = pd.read_csv(r'C:\Users\wasim\line-following\Data Samples\DataSamples-2\data_ir.csv')
# sample2_images = pd.read_csv(r'C:\Users\wasim\line-following\Data Samples\DataSamples-2\out_images.csv')

# start_timeStamp = '2022-08-17 01:49:10'
# end_timeStamp = '2022-08-17 01:50:54' 
# prepare_clean_datasamples(sample_images=sample2_images, sample_ir=sample2_ir, start_timeStamp=start_timeStamp, end_timeStamp=end_timeStamp)

# # Data Sample 3
# sample3_ir = pd.read_csv(r'C:\Users\wasim\line-following\Data Samples\DataSamples-3\data_ir.csv')
# sample3_images = pd.read_csv(r'C:\Users\wasim\line-following\Data Samples\DataSamples-3\out_images.csv')

# start_timeStamp = '2022-08-17 01:57:32'
# end_timeStamp = '2022-08-17 01:58:06' 
# prepare_clean_datasamples(sample_images=sample3_images, sample_ir=sample3_ir, start_timeStamp=start_timeStamp, end_timeStamp=end_timeStamp)

# # Data Sample 4
# sample4_ir = pd.read_csv(r'C:\Users\wasim\line-following\Data Samples\DataSamples-4\data_ir.csv')
# sample4_images = pd.read_csv(r'C:\Users\wasim\line-following\Data Samples\DataSamples-4\out_images.csv')

# start_timeStamp = '2022-08-17 01:58:39'
# end_timeStamp = '2022-08-17 01:59:13' 
# prepare_clean_datasamples(sample_images=sample4_images, sample_ir=sample4_ir, start_timeStamp=start_timeStamp, end_timeStamp=end_timeStamp)

# # Data Sample 5
# sample5_ir = pd.read_csv(r'C:\Users\wasim\line-following\Data Samples\DataSamples-5\data_ir.csv')
# sample5_images = pd.read_csv(r'C:\Users\wasim\line-following\Data Samples\DataSamples-5\out_images.csv')

# start_timeStamp = '2022-08-17 02:01:20'
# end_timeStamp = '2022-08-17 02:02:10' 
# prepare_clean_datasamples(sample_images=sample5_images, sample_ir=sample5_ir, start_timeStamp=start_timeStamp, end_timeStamp=end_timeStamp)

# # Data Sample 6
# sample6_ir = pd.read_csv(r'C:\Users\wasim\line-following\Data Samples\DataSamples-6\data_ir.csv')
# sample6_images = pd.read_csv(r'C:\Users\wasim\line-following\Data Samples\DataSamples-6\out_images.csv')

# start_timeStamp = '2022-08-17 02:03:45'
# end_timeStamp = '2022-08-17 02:04:12' 
# prepare_clean_datasamples(sample_images=sample6_images, sample_ir=sample6_ir, start_timeStamp=start_timeStamp, end_timeStamp=end_timeStamp)

# # Data Sample 7
# sample7_ir = pd.read_csv(r'C:\Users\wasim\line-following\Data Samples\DataSamples-7\data_ir.csv')
# sample7_images = pd.read_csv(r'C:\Users\wasim\line-following\Data Samples\DataSamples-7\out_images.csv')

# start_timeStamp = '2022-08-17 02:04:59'
# end_timeStamp = '2022-08-17 02:05:46' 
# prepare_clean_datasamples(sample_images=sample7_images, sample_ir=sample7_ir, start_timeStamp=start_timeStamp, end_timeStamp=end_timeStamp)

# # Data Samples 8
# sample8_ir = pd.read_csv(r'C:\Users\wasim\line-following\Data Samples\DataSamples-8\data_ir.csv')
# sample8_images = pd.read_csv(r'C:\Users\wasim\line-following\Data Samples\DataSamples-8\out_images.csv')

# start_timeStamp = '2022-08-17 02:06:19'
# end_timeStamp = '2022-08-17 02:07:08'
# prepare_clean_datasamples(sample_images=sample8_images, sample_ir=sample8_ir, start_timeStamp=start_timeStamp, end_timeStamp=end_timeStamp)