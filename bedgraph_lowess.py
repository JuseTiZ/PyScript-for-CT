import pandas as pd
import statsmodels.api as sm
import argparse

def get_args():

    parser = argparse.ArgumentParser(description='Perform lowess smooth on bedgraph.')
    
    parser.add_argument('--input', '-i', help='Input bedgraph file.', required=True)
    parser.add_argument('--output', '-o', help='Output smoothed bedgraph file.', required=True)
    parser.add_argument('--span', help='Span size of loess smoothing.', type=int, required=True)
    parser.add_argument("--chr", required=True,
                        help="The chrom to input. e.g. 1-22,X,Y")
    
    args = parser.parse_args()

    return args


def parse_range(value):
    result = []
    for part in value.split(','):
        if '-' in part:
            start, end = part.split('-')
            result.extend(range(int(start), int(end) + 1))
        else:
            result.append(int(part))
    return result


def main():

    args = get_args()

    data = pd.read_csv(args.input, sep='\t', header=None, names=['chrom', 'start', 'end', 'value'])
    data['midpoint'] = (data['start'] + data['end']) / 2

    span_size = args.span
    smoothed_data = []
    chr_list = [f'chr{i}' for i in parse_range(args.chr)]

    for chrom in data['chrom'].unique():
        chrom_data = data[data['chrom'] == chrom]
        if chrom not in chr_list:
            continue

        chrom_length = chrom_data['end'].iloc[-1] - chrom_data['start'].iloc[0]
        span_frac = span_size / chrom_length

        lowess = sm.nonparametric.lowess(chrom_data['value'], chrom_data['midpoint'], frac=span_frac)
        smoothed_df = pd.DataFrame(lowess, columns=['midpoint', 'smoothed_value'])
        chrom_data = chrom_data.reset_index(drop=True)
        chrom_data['smoothed_value'] = smoothed_df['smoothed_value']
        smoothed_data.append(chrom_data)

    smoothed_data = pd.concat(smoothed_data)
    smoothed_data[['chrom', 'start', 'end', 'smoothed_value']].to_csv(args.output, sep='\t', header=False, index=False)

if __name__ == '__main__':
    main()