from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import lines as mpl_lines

data = pd.read_csv(".\SNP500Historical.csv")

df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])
df.rename(columns={'Close/Last': "Close"}, inplace=True)

# 0:1000 - standard
# 220:400
# 610:700
df1 = df.iloc[:1000].reset_index(drop=True)
df2 = df.iloc[220:400].reset_index(drop=True)
df3 = df.iloc[610:700].reset_index(drop=True)


def ema1(n, x):
    a = 2 / (n + 1)
    ema_values = []

    ema_prev = x[0]
    ema_values.append(ema_prev)

    for price in x[n:]:
        ema_current = a * price + (1 - a) * ema_prev
        ema_values.append(ema_current)
        ema_prev = ema_current

    return ema_values


def ema_calc(n, x):
    a = 2 / (n + 1)

    ema_values = []
    ema_prev = x[0]
    ema_values.append(ema_prev)

    for i in x[1:]:
        ema_prev = a * i + (1 - a) * ema_prev
        ema_values.append(ema_prev)

    return ema_values


def macd_calc(fast, slow, x):
    macd = []
    ema_slow = ema_calc(slow, x)
    ema_fast = ema_calc(fast, x)
    for i in range(len(ema_slow) - 1):
        macd.append(ema_fast[i] - ema_slow[i])
    return macd


def signal_calc(n, macd):
    return ema_calc(n, macd)


def markers(macd, signal):
    sell_points = []
    buy_points = []

    for i in range(1, len(macd)):
        if (macd[i - 1] < signal[i - 1] and macd[i] > signal[i]):
            last_intersection = macd[i]
            buy_points.append(i)
        elif (macd[i - 1] > signal[i - 1] and macd[i] < signal[i]):
            last_intersection = macd[i]
            sell_points.append(i)
    return sell_points, buy_points


def investing_simulation(data, initial_capital, historical_data):
    capital = initial_capital
    shares = 0

    wallet = [[], []]

    for index, row in data.iterrows():
        stock_close_value = row['price']

        if row['type'] == 'buy':
            shares += capital / stock_close_value
            capital = 0

            wallet[0].append(row['date'])
            wallet[1].append(shares * stock_close_value / 100000)

        else:
            capital += shares * stock_close_value
            shares = 0

            wallet[0].append(row['date'])
            wallet[1].append(capital / 100000)

        # print(f"Shares: {shares}, capital: {capital}") TEST LINE BY LINE

    if shares == 0:
        return capital, wallet
    else:
        return shares * historical_data['Close'].iloc[0], wallet


def biggest_lost_win(data):
    win = [[0, 0], [0, 0]]
    lost = [[0, 0], [0, 0]]
    win_diff, lost_diff = 0, 0
    for index, row in data[1:].iterrows():
        win_diff_temp, lost_diff_temp = 0, 0
        price_next = data.loc[index]['price']
        price_prev = data.loc[index - 1]['price']
        if price_next > price_prev:
            win_diff_temp = price_next - price_prev
        elif price_next < price_prev:
            lost_diff_temp = price_next - price_prev

        if win_diff < win_diff_temp:
            win_diff = win_diff_temp
            win[0] = [price_prev, data.loc[index - 1]['date']]
            win[1] = [price_next, data.loc[index]['date']]
        if lost_diff > lost_diff_temp:
            lost_diff = lost_diff_temp
            lost[0] = [price_prev, data.loc[index - 1]['date']]
            lost[1] = [price_next, data.loc[index]['date']]

    return win, lost


def historical_plot(df):
    # Wykres notowan finansowych
    plt.figure(figsize=(10, 5))
    plt.plot(df1['Date'], df['Close'], linestyle='-')

    plt.xlim(df['Date'][998], df['Date'][0])
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.title("Stock Price Over Time")
    plt.locator_params(axis="x", nbins=2)

    # plt.savefig('StockPriceOverTime.png')
    plt.show()


def macd_signal(macd, signal, marker_buy, marker_sell, buy_y, sell_y):
    # Wykres MACD + Signal
    plt.figure(figsize=(15, 9))
    plt.plot(macd, '-', color='steelblue', label="MACD")
    plt.plot(signal, '-', color='goldenrod', label="Signal")
    plt.scatter(marker_buy, buy_y, color='green', marker='^', label='Buy', zorder=5)
    plt.scatter(marker_sell, sell_y, color='red', marker='v', label='Sell', zorder=5)
    plt.title("MACD and Signal Lines")
    plt.xlim(-5, len(macd) + 5)
    plt.legend()

    # plt.savefig('MACD_SIGNAL.png')
    plt.show()


def wallet_overtime(wallet):
    # Wykres wartosci portfela
    pos_ops, neg_ops = 0, 0

    plt.figure(figsize=(15, 9))
    plt.plot(wallet[0], wallet[1], linestyle='-', marker='o', ms='4', mfc='black', label='Sell/Buy Transaction')

    ax = plt.gca()

    last_value = None
    alternator = 1

    for idx, (i, j) in enumerate(zip(wallet[0], wallet[1])):
        if j != last_value:
            offset_y = 20 * alternator
            offset_x = 5

            if last_value is not None and j > last_value:
                color = 'green'
                pos_ops += 1
            else:
                color = 'red'
                neg_ops += 1

            if idx == 0: color = 'grey'

            ax.plot([i, i], [j, j + offset_y / 10], linestyle="--", color=color, alpha=0.7)

            if alternator == -1: offset_y = -65

            ax.annotate(f"{j:.2f}", xy=(i, j), xytext=(offset_x, (offset_y + 20)),
                        textcoords="offset points", ha='center', color=color)

            alternator *= -1
            last_value = j

    plt.text(wallet[0][int(len(wallet[0]) / 3) + 10], min(wallet[1]),
             "Note: 'o' markers are not labeled if the value repeats from the previous point.",
             fontsize=10, ha="left")
    plt.text(wallet[0][int(len(wallet[0]) / 3) + 10], min(wallet[1]) - 0.5,
             "Green indicates increased value of wallet.",
             fontsize=10, color='g', ha="left")
    plt.text(wallet[0][int(len(wallet[0]) / 3) + 10], min(wallet[1]) - 1,
             "Red indicates decreased value of wallet.",
             fontsize=10, color='r', ha="left")

    plt.xlabel("Date")
    plt.ylabel("Wallet Value [Divided by 10^5]")
    plt.title("Wallet Value Over Time")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    # plt.savefig("WalletOverTime.png")
    plt.show()

    print(f'Liczba pozytywnych transakcji: {pos_ops}\nLiczba negatywnych transakcji: {neg_ops}')


def bar_wallet(wallet):
    transactions = list(range(len(wallet[1])))
    amounts = wallet[1]

    transactions = transactions[::2]
    transactions_g = transactions[::1]
    amounts = amounts[::2]
    amounts_g = amounts[::1]

    colors = ['green' if amounts[i] >= amounts[i - 1] else 'red' for i in range(1, len(amounts))]
    colors.insert(0, 'gray')

    plt.figure(figsize=(12, 6))
    plt.bar(transactions, amounts, color=colors, alpha=0.7, label="Wallet Balance")

    plt.xlabel("Transaction Number")
    plt.ylabel("Wallet Value [Divided by 10^5] ($)")
    plt.title("Wallet Value Over Sell Transactions")

    for i, val in enumerate(amounts):
        plt.text(i * 2, val + (max(amounts) * 0.02), f"{val:.2f}", ha='center', fontsize=10, color='black')

    # plt.savefig("WalletOver.png")
    plt.show()


def subplots(macd, signal, df, buy_df, sell_df, marker_buy, marker_sell, buy_y, sell_y, win, lost):
    # Subplot z wykresem MACD i notowan finansowych wraz z sygnalami

    plt.figure(figsize=(20, 5))

    plt.subplot(1, 2, 2)
    plt.plot(macd, '-', color='steelblue', label="MACD")
    plt.plot(signal, '-', color='goldenrod', label="Signal")
    plt.scatter(marker_buy, buy_y, color='green', marker='^', label='Buy', zorder=5)
    plt.scatter(marker_sell, sell_y, color='red', marker='v', label='Sell', zorder=5)
    plt.title("MACD and Signal Lines")
    plt.xlim(-5, len(macd) + 5)
    plt.legend()

    # plt.savefig('MACD_SIGNAL.png')

    plt.subplot(1, 2, 1)
    plt.plot(df['Date'], df['Close'], linestyle='-')
    plt.scatter(buy_df['date'], buy_df['price'], color='green', marker='^', label='Buy', s=100, zorder=2)
    plt.scatter(sell_df['date'], sell_df['price'], color='red', marker='v', label='Sell', s=100, zorder=2)

    # plt.xlim(df['Date'][998], df['Date'][0])
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.title("Stock Price Over Time")
    plt.xticks(rotation=45)
    plt.locator_params(axis="x", nbins=2)
    plt.legend()

    win_dates = [win[0][1], win[1][1]]
    win_prices = [win[0][0], win[1][0]]

    lost_dates = [lost[0][1], lost[1][1]]
    lost_prices = [lost[0][0], lost[1][0]]

    ax = plt.gca()

    line_win = mpl_lines.Line2D(win_dates, win_prices, linestyle='--', color='black', linewidth=2,
                                label='Highest upwards price differance', zorder=1)
    line_lost = mpl_lines.Line2D(lost_dates, lost_prices, linestyle='--', color='sienna', linewidth=2,
                                 label='Highest downwards price differance', zorder=1)

    ax.add_line(line_win)
    ax.add_line(line_lost)

    if len(df) > 100:
        special_buy = buy_df.iloc[2]
        special_sell = sell_df.iloc[0]
    else:
        special_buy = buy_df.iloc[2]
        special_sell = sell_df.iloc[1]

    plt.scatter(special_buy['date'], special_buy['price'], color='lightgreen', edgecolors='black', marker='^', s=400,
                zorder=3)
    plt.scatter(special_sell['date'], special_sell['price'], color='darkred', edgecolors='black', marker='v', s=400,
                zorder=3)

    handles, labels = ax.get_legend_handles_labels()
    handles.extend([line_win, line_lost])
    ax.legend(handles, labels, loc='best')

    # plt.savefig("SubplotForStockOverTime.png")
    plt.show()


def main(df):
    macd = macd_calc(12, 26, df['Close'])

    signal = signal_calc(9, macd)

    marker_sell, marker_buy = markers(macd, signal)
    buy_y = [signal[i] for i in marker_buy]
    sell_y = [signal[i] for i in marker_sell]

    buy_date = [df['Date'][i] for i in marker_buy]
    sell_date = [df['Date'][i] for i in marker_sell]
    buy1_y = [df['Close'][i] for i in marker_buy]
    sell1_y = [df['Close'][i] for i in marker_sell]

    if (len(df) > 800):
        historical_plot(df)

    df = df.iloc[:len(signal)].reset_index(drop=True)  # Dostosowanie do dlugosci algorytmu macd signal
    afd = pd.DataFrame({
        'macd': macd,
        'signal': signal,
        'date': df['Date']
    })

    buy_df = pd.DataFrame({
        'price': buy1_y,
        'date': buy_date,
        'type': 'buy'
    })

    sell_df = pd.DataFrame({
        'price': sell1_y,
        'date': sell_date,
        'type': 'sell'
    })

    concat_df = pd.concat([buy_df, sell_df])
    concat_df = concat_df.sort_values(by='date').reset_index(drop=True)

    initial_capital = 1000

    if (concat_df['type'][0] == 'buy'):
        close_value = concat_df['price'][0]
        concat_df = concat_df[1:].reset_index(drop=True)
    else:
        close_value = df['Close'][0]

    initial_capital *= close_value

    macd_sim_capital, wallet = investing_simulation(concat_df, initial_capital, df)
    macd_sim_capital = macd_sim_capital.round(2)

    hold_sim_capital = 1000 * df['Close'].iloc[0]  ## Symulacja Hold
    win, lost = biggest_lost_win(concat_df)

    if (len(df) > 800):
        macd_signal(macd, signal, marker_buy, marker_sell, buy_y, sell_y)
        wallet_overtime(wallet)
    else:
        subplots(macd, signal, df, buy_df, sell_df, marker_buy, marker_sell, buy_y, sell_y, win, lost)
        bar_wallet(wallet)

    #  Wyniki obu strategii
    print(f'Capital after: \n -MACD strategy: {macd_sim_capital}\n -Hold strategy: {hold_sim_capital} ',
          f'\nDifferance HOLD vs MACD: {round(100 - (macd_sim_capital / hold_sim_capital * 100), 2)}%')

    main(df1)
    main(df2)
    main(df3)