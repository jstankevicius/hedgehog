import numpy as np

def roc(prices, period=21):

    num_prices = len(prices)

    if num_prices < period:
        # show error message
        raise SystemExit('Error: num_prices < period')

    roc_range = num_prices - period

    rocs = np.zeros(roc_range)

    for idx in range(roc_range):
        rocs[idx] = ((prices[idx + period] - prices[idx]) / prices[idx]) * 100

    return rocs


def rsi(prices, period=14):

    num_prices = len(prices)

    if num_prices < period:
        # show error message
        raise SystemExit('Error: num_prices < period')

    # this could be named gains/losses to save time/memory in the future
    changes = prices[1:] - prices[:-1]
    #num_changes = len(changes)

    rsi_range = num_prices - period

    rsis = np.zeros(rsi_range)

    gains = np.array(changes)
    # assign 0 to all negative values
    masked_gains = gains < 0
    gains[masked_gains] = 0

    losses = np.array(changes)
    # assign 0 to all positive values
    masked_losses = losses > 0
    losses[masked_losses] = 0
    # convert all negatives into positives
    losses *= -1

    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])

    if avg_loss == 0:
        rsis[0] = 100
    else:
        rs = avg_gain / avg_loss
        rsis[0] = 100 - (100 / (1 + rs))

    for idx in range(1, rsi_range):
        avg_gain = ((avg_gain * (period - 1) + gains[idx + (period - 1)]) /
                    period)
        avg_loss = ((avg_loss * (period - 1) + losses[idx + (period - 1)]) /
                    period)

        if avg_loss == 0:
            rsis[idx] = 100
        else:
            rs = avg_gain / avg_loss
            rsis[idx] = 100 - (100 / (1 + rs))

    # The above method is correct for calculating the RSI of a stock option.
    # However, we need to normalize the value for the neural network.
    rsis = np.divide(rsis, 100)
    return rsis

def sma(prices, period):

    num_prices = len(prices)

    if num_prices < period:
        # show error message
        raise SystemExit('Error: num_prices < period')

    sma_range = num_prices - period + 1

    smas = np.zeros(sma_range)

    # only required for the commented code below
    #k = period

    for idx in range(sma_range):
        # this is the code, but using np.mean below is faster and simpler
        #for period_num in range(period):
        #    smas[idx] += prices[idx + period_num]
        #smas[idx] /= k

        smas[idx] = np.mean(prices[idx:idx + period])

    # Now, normalize:
    formatted_prices = prices[period - 1:]
    smas = np.divide(smas, formatted_prices)

    # We're now looking for how many percentage points the
    # SMA is above the price. Thus, we subtract 1 and multiply
    # by 100.
    smas = np.subtract(smas, 1)
    smas = np.multiply(smas, 100)

    # Because this is a moving average, we need to delete the first
    # element.
    smas = np.delete(smas, 0, 0)
    return smas


def wma(prices, period):

    num_prices = len(prices)

    if num_prices < period:
        # show error message
        raise SystemExit('Error: num_prices < period')

    wma_range = num_prices - period + 1

    wmas = np.zeros(wma_range)

    k = (period * (period + 1)) / 2.0

    # only required for the commented code below
    #w = 2 / float(period + 1)

    for idx in range(wma_range):
        for period_num in range(period):
            weight = period_num + 1
            wmas[idx] += prices[idx + period_num] * weight
        wmas[idx] /= k
        
    # Now, normalize:
    formatted_prices = prices[period - 1:]
    wmas = np.divide(wmas, formatted_prices)

    # We're now looking for how many percentage points the
    # WMA is above the price. Thus, we subtract 1 and multiply
    # by 100.
    wmas = np.subtract(wmas, 1)
    wmas = np.multiply(wmas, 100)

    # Because this is a moving average, we need to delete the first
    # element.
    wmas = np.delete(wmas, 0, 0)
    return wmas


def ema(prices, period, ema_type=0):

    num_prices = len(prices)

    if num_prices < period:
        # show error message
        raise SystemExit('Error: num_prices < period')

    if ema_type == 0:  # 1st value is the average of the period
        ema_range = num_prices - period + 1

        emas = np.zeros(ema_range)

        emas[0] = np.mean(prices[:period])

        w = 2 / float(period + 1)

        # only required for the 4th formula
        #w = 1 - 2 / float(period + 1)

        for idx in range(1, ema_range):
            emas[idx] = w * prices[idx + period - 1] + (1 - w) * emas[idx - 1]

    elif ema_type == 1:  # 1st value is the 1st price
        ema_range = num_prices

        emas = np.zeros(ema_range)

        emas[0] = prices[0]

        w = 2 / float(period + 1)


        for idx in range(1, ema_range):
            emas[idx] = w * prices[idx] + (1 - w) * emas[idx - 1]

    else:
        ema_range = num_prices - period + 1

        emas = np.zeros(ema_range)

        w = 2 / float(period + 1)

        k = 1 / float(1 - w)

        for idx in range(ema_range):
            for period_num in range(period):
                # this runs the prices backwards to comply with the formula
                emas[idx] += w**period_num * \
                    prices[idx + period - period_num - 1]
            emas[idx] /= k
            
    # Now, normalize:
    formatted_prices = prices[period - 1:]
    emas = np.divide(emas, formatted_prices)

    # We're now looking for how many percentage points the
    # EMA is above the price. Thus, we subtract 1 and multiply
    # by 100.
    emas = np.subtract(emas, 1)
    emas = np.multiply(emas, 100)

    # Because this is a moving average, we need to delete the first
    # element.
    emas = np.delete(emas, 0, 0)

    return emas

def macd(prices, periodshort, periodlong):

    finalarray = []
    
    num_prices = len(prices)

    if num_prices < periodlong:
        # show error message
        raise Exception('Error: num_prices < period')

    if periodlong < periodshort:
        periodlong, periodshort = periodshort, periodlong

    startpos = prices[periodlong]

    for idx in range(periodlong, num_prices):
        shortprice = prices[idx - periodshort, idx]
        longprice = prices[idx - periodlong, idx]

        shortema = ema(shortprice, periodshort,1)
        longema = ema(longprice, periodlong,1)

        emadiff = longema - shortema

        finalarray.append(emadiff)

    return finalarray

def dir_macd(macdlist, period):
    
    #Since the directional macdlist is goign to be running ema again, the list will be even shorter.
    shortmacdlist = macdlist[period:]

    dirmacdlist = []

    for idx in range(period, len(macdlist)):
        val = ema(idx-period, period, 1)
        dirmacdlist.append(val)

    if len(dirmacdlist) != len(shortmacdlist):
        raise Exception('Lengths are different', str(len(shortmacdlist)), str(len(dirmacdlist)))

    finalreturn = []
    for x in range(0, len(shortmacdlist)):
        sub = shortmacdlist[x] - dirmacdlist[x]
        finalreturn.append(sub)