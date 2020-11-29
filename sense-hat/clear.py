try:
    from sense_hat import SenseHat
except ImportError:
    from sense_emu import SenseHat

if __name__ == '__main__':

    hat = SenseHat()
    hat.clear()