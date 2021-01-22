import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean

# TODO: transform input data into csv separated by semicolons (;), see example .csv files

names = ['col_' + str(i) for i in range(1, 27)]

df_ntrl = pd.read_csv('participant_3_neutral_csv.csv', sep=';', names=names)    # neutral
df_ngtv = pd.read_csv('participant_3_negative_csv.csv', sep=';', names=names)   # negative

df_ntrl = df_ntrl.drop(columns=['col_25', 'col_26'])
df_ngtv = df_ngtv.drop(columns=['col_26'])

# access sample i: s = df_ntrl['col_i']

# TODO: hand pick 10 samples per condition, insert column numbers in list below ('col_i')
# hand picked samples
samples_ntrl = ['col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_8', 'col_12', 'col_14', 'col_19', 'col_24']
samples_ngtv = ['col_3', 'col_6', 'col_9', 'col_10', 'col_12', 'col_14', 'col_18', 'col_19', 'col_20', 'col_24']

# remove all columns except hand picked samples
df_ntrl = df_ntrl[samples_ntrl]
df_ngtv = df_ngtv[samples_ngtv]


### functions ###

# E.g.: plot_all(samples_ngtv)
def plot_all(samples, condition: str):
    for key in samples:
        plt.plot(samples[key])
        plt.title(f'{condition}: {key}')
        plt.show()


def get_max_amplitude(sample: pd.DataFrame):
    max_amp = max(sample)
    max_amp_index = sample.idxmax()     # +1 to get excel file row number
    return max_amp, max_amp_index


# TODO: extract latency (first rising value) manually by looking at plots and insert into dict in 'get_latency'
#       below, use plot_all function to plot each sample (hover over plot to see x,y values)

plot_all(df_ntrl, condition='neutral')
plot_all(df_ngtv, condition='negative')


# latency (SCR onset) extracted manually from plots
def get_latency(key: str, condition: str):
    if condition == 'neutral':
        latencies = {'col_1': 61, 'col_2': 58, 'col_3': 17, 'col_4': 24, 'col_5': 55, 'col_8': 74, 'col_12': 58,
                     'col_14': 31, 'col_19': 45, 'col_24': 19}
        return latencies[key]
    elif condition == 'negative':
        latencies = {'col_3': 18, 'col_6': 22, 'col_9': 25, 'col_10': 23, 'col_12': 23, 'col_14': 66, 'col_18': 23,
                     'col_19': 22, 'col_20': 36, 'col_24': 21}
        return latencies[key]


def process_samples(samples, condition: str):
    # condition: 'neutral' or 'negative'
    max_amps = []               # max amplitudes per sample
    max_amps_indices = []       # indices of max amplitudes per sample
    latencies = []              # latency per sample
    rise_times = []             # rise time per sample
    keys = []
    for key in samples:
        keys.append(key)
        z = get_max_amplitude(samples[key])
        amp = z[0]
        amp_index = z[1]
        max_amps.append(amp)
        max_amps_indices.append(amp_index)
        lat = get_latency(key, condition)
        latencies.append(lat)
        rise_time = amp_index - lat
        rise_times.append(rise_time)

    print(f'---------------\nCondition: {condition}')
    print(f'key,        Max amp         latency         rise time')
    for i in range(len(max_amps)):
        print(f'{keys[i]},     {max_amps[i]},       {latencies[i]},             {rise_times[i]}')
    print(f'\nMean:       {mean(max_amps)},      {mean(latencies)},           {mean(rise_times)}')
    print('\n\n')


def mean_sample(samp_ntrl, samp_ngtv):
    mean_vals_ntrl = []
    for i in range(1, 298):
        vals = []
        for s in samp_ntrl:
            vals.append(samp_ntrl[s][i])
        avg = mean(vals)
        mean_vals_ntrl.append(avg)

    mean_vals_ngtv = []
    for i in range(1, 298):
        vals = []
        for s in samp_ngtv:
            vals.append(samp_ngtv[s][i])
        avg_ngtv = mean(vals)
        mean_vals_ngtv.append(avg_ngtv)

    plt.plot(mean_vals_ntrl, label='Neutral')
    plt.plot(mean_vals_ngtv, label='Negative')
    plt.xlabel('Time (s)')
    plt.ylabel('Difference to baseline mean (mm)')
    plt.title('Participant 3')
    plt.xlim([0, 297])
    plt.xticks([i for i in range(0, 297, 20)]+ [297])
    plt.grid(axis='y')
    plt.legend()
    plt.show()


process_samples(df_ntrl, 'neutral')
process_samples(df_ngtv, 'negative')
mean_sample(df_ntrl, df_ngtv)