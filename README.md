# LED Matrix Stock Ticker

This project is a **real-time stock ticker** that displays stock prices and changes on a **64x32 RGB LED matrix** using a **Xiao ESP32-C3 (or similar microcontroller)**. It smoothly scrolls through stock data with a well-balanced speed and animations.

---

## Features 🚀

✅ **Smooth scrolling animation** with easing for better readability.\
✅ **Real-time stock data fetching** (simulated in development mode).\
✅ **Stock names, prices, and changes displayed clearly.**\
✅ **Optimized speed (\~60 FPS) and balanced scrolling.**\
✅ **Automatic stock data updates every 10 seconds.**\
✅ **Color-coded price changes:** Green (▲) for increase, Red (▼) for decrease.

---

## Hardware Requirements 🛠️

- **64x32 RGB LED Matrix** (HUB75 interface)
- **Microcontroller** (ESP32, Xiao ESP32-C3, or similar)
- **5V 2A Power Supply**
- **Jumper Wires**

### **Pin Configuration (ESP32/Xiao ESP32-C3)**

| LED Matrix Pin | ESP32/Xiao ESP32-C3 |
| -------------- | ------------------- |
| R1, G1, B1     | D6, D5, D9          |
| R2, G2, B2     | D11, D10, D12       |
| A, B, C, D     | A5, A4, A3, A2      |
| CLK            | D13                 |
| Latch          | D0                  |
| OE             | D1                  |

---

## Software Requirements 🖥️

- **CircuitPython** installed on your microcontroller.
- Required libraries from [Adafruit CircuitPython Bundle](https://circuitpython.org/libraries):
  - `displayio`
  - `framebufferio`
  - `rgbmatrix`
  - `adafruit_display_text`
  - `terminalio`
  - `requests`

---

## Installation & Setup 🔧

1. **Install CircuitPython** on your microcontroller (check [Adafruit Guide](https://learn.adafruit.com/welcome-to-circuitpython)).
2. **Copy required libraries** to the `lib/` folder on your microcontroller.
3. **Upload the Python script** (`main.py`) to the root directory.
4. **Power up your microcontroller** and see the stock ticker in action! 🚀

---

## Configuration ⚙️

- To **enable real-time stock data**, modify `dev_mode = False` and implement an API request inside `get_stock_data()`.
- Adjust `SCROLL_SPEED` and `SCROLL_PAUSE` in the script for preferred scrolling behavior.

---

## Future Enhancements 🌟

✅ **Live API integration** for fetching real-time stock prices.
✅ **WiFi connectivity** for remote updates.
✅ **Button controls** to change the scrolling speed.
✅ **Additional display effects** like flashing price alerts.

