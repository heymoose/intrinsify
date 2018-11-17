from money import Money

def num_to_currency(num):
    return Money(num, 'USD').format('en_US')

def float_to_percentage_string(num):
    return '{:.2f}%'.format(float(num))

def pretty_float(num):
    return "%.2f" % num
