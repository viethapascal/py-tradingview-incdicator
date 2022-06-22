import pandas as pd

'''
RSV (n days)=(Cn－Ln)/(Hn－Ln)×100

Cn is the closing price on the n-th day; Ln is the lowest price in n days; Hn is the highest price in n days.

Second, calculate the K value and D value:

K value = 2/3 × K value of the previous day + 1/3 × RSV of the day

D value = 2/3 × D value of the previous day + 1/3 × K value of the day

J value = 3 × K value of the day-2 × D value of the day

Pine Script Code
# This is formatted as code
study("KDJ Indicator - @iamaltcoin", shorttitle="GM_V2_KDJ")
ilong = input(9, title="period")
isig = input(3, title="signal")

bcwsma(s,l,m) => 
    _s = s
    _l = l
    _m = m
    _bcwsma = (_m*_s+(_l-_m)*nz(_bcwsma[1]))/_l
    _bcwsma

c = close
h = highest(high, ilong)
l = lowest(low,ilong)
RSV = 100*((c-l)/(h-l))
pK = bcwsma(RSV, isig, 1)
pD = bcwsma(pK, isig, 1)
pJ = 3 * pK-2 * pD
'''


def RSV(df, period=9):
    L_n = df['low'].rolling(window=period, min_periods=0).min()
    H_n = df['high'].rolling(window=period, min_periods=0).max()
    rsv = 100 * ((df['close'] - L_n) / (H_n - L_n))
    rsv_df = pd.DataFrame({'rsv': rsv})
    return rsv_df


def calc_k(df, left, right, sig, m):
    for i in range(len(df)):
        if i > 0:
            df.loc[:, right].iloc[i] = (m * df[left].iloc[i] + (sig - m) * df[right].iloc[i - 1]) / sig
        else:
            df.loc[:, right].iloc[i] = (m * df[left].iloc[i]) / sig
        df.loc[:, right].iloc[i] = df.loc[:, right].iloc[i].round(5)


def KDJ(df, period=9, signal=3):
    '''

    :param df: DataFrame with at least these column: open_time, close, high, low
    :param period: default 9
    :param signal:
    :return:
    DataFrame with 4 cols: open_time, rsv, K, D, J
    '''
    rsv_df = RSV(df, period=period)
    rsv_df['open_time'] = df['open_time']
    rsv_df.loc[:, 'K'] = 0
    rsv_df.loc[:, 'D'] = 0
    calc_k(rsv_df, 'rsv', 'K', signal, 1)
    calc_k(rsv_df, 'K', 'D', signal, 1)
    rsv_df['J'] = rsv_df.apply(lambda row: 3 * row['K'] - 2 * row['D'], axis=1)
    rsv_df = rsv_df[['open_time', 'rsv', 'K', 'D', 'J']]
    return rsv_df

