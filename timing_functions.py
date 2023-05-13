def linear(x):
    return x

def ease_in_out(alpha=1):
    def fn(x):
        return (x**alpha) / (x**alpha + (1 - x)**alpha)
    return fn