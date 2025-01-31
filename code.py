import time
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
import adafruit_display_text.label

dev_mode = True  

displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width=32, height=64, bit_depth=6,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

STOCKS = [
    {"symbol": "RELIANCE", "name": "Reliance"},
    {"symbol": "TCS", "name": "TCS"},
    {"symbol": "HDFCBANK", "name": "HDFC"},
    {"symbol": "ICICIBANK", "name": "ICICI"},
    {"symbol": "HINDUNILVR", "name": "HUL"},
    {"symbol": "INFY", "name": "Infosys"},
    {"symbol": "ITC", "name": "ITC"},
    {"symbol": "BHARTIARTL", "name": "Airtel"},
    {"symbol": "SBIN", "name": "SBI"},
    {"symbol": "BAJFINANCE", "name": "Bajaj"},
    {"symbol": "KOTAKBANK", "name": "Kotak"},
    {"symbol": "WIPRO", "name": "Wipro"},
    {"symbol": "HCLTECH", "name": "HCL"},
    {"symbol": "ASIANPAINT", "name": "Asian"},
    {"symbol": "LT", "name": "L&T"}
]

def get_stock_data():
    if not dev_mode:
        return None  
    return {
        "RELIANCE": {"price": 2457.50, "change": 1.2},
        "TCS": {"price": 3678.25, "change": -0.5},
        "HDFCBANK": {"price": 1678.30, "change": 0.8},
        "ICICIBANK": {"price": 945.75, "change": 1.5},
        "HINDUNILVR": {"price": 2567.80, "change": -0.3},
        "INFY": {"price": 1434.90, "change": 0.7},
        "ITC": {"price": 438.45, "change": 2.1},
        "BHARTIARTL": {"price": 867.30, "change": 0.9},
        "SBIN": {"price": 576.25, "change": 1.8},
        "BAJFINANCE": {"price": 6789.50, "change": -0.6},
        "KOTAKBANK": {"price": 1789.35, "change": 0.4},
        "WIPRO": {"price": 456.70, "change": -0.8},
        "HCLTECH": {"price": 1234.55, "change": 1.1},
        "ASIANPAINT": {"price": 3245.60, "change": -0.2},
        "LT": {"price": 2456.75, "change": 0.5}
    }

def ease_in_out_cubic(t):
    if t < 0.5:
        return 4 * t * t * t
    p = 2 * t - 2
    return 0.5 * p * p * p + 1

main_group = displayio.Group()
stock_group = displayio.Group()
x_position = 32
stock_labels = []

for stock in STOCKS:
    stock_label = adafruit_display_text.label.Label(
        terminalio.FONT, color=0xFFFFFF, text=stock["name"]
    )
    stock_label.x = x_position
    stock_label.y = 4  
    
    price_label = adafruit_display_text.label.Label(
        terminalio.FONT, color=0xFFFFFF, text="Loading..."
    )
    price_label.x = x_position
    price_label.y = 18  
    
    stock_labels.append({"name": stock_label, "price": price_label, "symbol": stock["symbol"]})
    stock_group.append(stock_label)
    stock_group.append(price_label)
    
    x_position += 80  # Enough spacing to make stocks readable

main_group.append(stock_group)
display.root_group = main_group

SCROLL_SPEED = 1.2  # **Moderate speed**
FRAME_TIME = 0.016  # **Smoother motion (~60 FPS)**
SCROLL_PAUSE = 1.2  # **Slightly longer pause between cycles**
UPDATE_INTERVAL = 10  

last_update = 0
scroll_position = 32
target_position = -x_position
animation_start_time = time.monotonic()
animation_duration = abs(target_position - scroll_position) / (SCROLL_SPEED * 20)
is_paused = False
pause_start = 0
prev_time = time.monotonic()

while True:
    current_time = time.monotonic()
    delta_time = current_time - prev_time
    prev_time = current_time

    if current_time - last_update >= UPDATE_INTERVAL:
        stock_data = get_stock_data()
        if stock_data:
            for label_set in stock_labels:
                if label_set["symbol"] in stock_data:
                    data = stock_data[label_set["symbol"]]
                    change_symbol = "▲" if data["change"] > 0 else "▼"
                    label_set["price"].text = f"₹{data['price']:.1f} {change_symbol}"
                    label_set["price"].color = 0x00FF00 if data["change"] > 0 else 0xFF0000
        last_update = current_time

    if not is_paused:
        elapsed_time = current_time - animation_start_time
        progress = min(elapsed_time / animation_duration, 1.0)
        eased_progress = ease_in_out_cubic(progress)
        scroll_position = 32 + (target_position - 32) * eased_progress
        stock_group.x = int(scroll_position)

        if progress >= 1.0:
            is_paused = True
            pause_start = current_time
    else:
        if current_time - pause_start >= SCROLL_PAUSE:
            is_paused = False
            scroll_position = 32
            stock_group.x = int(scroll_position)
            animation_start_time = current_time
            animation_duration = abs(target_position - scroll_position) / (SCROLL_SPEED * 20)

    display.refresh(minimum_frames_per_second=0)
    
    sleep_time = max(0, FRAME_TIME - (time.monotonic() - current_time))
    time.sleep(sleep_time)
