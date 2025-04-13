# 🌞 SunPosition

A Python application that real-time tracks the position of the sun and visually represents relative to a house.

## 📸 Overview

The program displays two views:
- **Front view**: showing the sun's elevation in the sky.
- **Top view**: showing the sun's azimuth relative to the orientation of your house.

Sun data is updated in real-time using your configured geographic location.

---

## 🚀 Features

- Real-time tracking of the sun’s position.
- Visual representation of altitude and azimuth.
- Customizable geographic location, house orientation and timezone via a JSON config file.

---

## 🛠 Requirements

Make sure you have the following Python packages installed:

- `pygame`
- `astropy`
- `pytz`

You can install them using:

```bash
pip install -r requirements.txt
```

---

## 📁 Configuration

Customize the `config.json` file in the same directory as the script with the following structure:

```json
{
  "house": {
    "latitude": 45.55,
    "longitude": 9.18,
    "timezone": "Europe/Rome",
    "direction": 165
  }
}
```

---

## ▶️ How to Run

```bash
python sun_position.py
```

The window will open showing two views of the house and the current position of the sun, updating every second.

Press **ESC** or close the window to exit the program.

---

## 🧠 How It Works

- Uses [Astropy](https://www.astropy.org/) to calculate the sun’s position in AltAz coordinates.
- Renders sun path and position using [Pygame](https://www.pygame.org/news).
- Adjusts the sun's angle and direction based on real-time data and your custom house orientation.

---

## 🧾 License

This project is open-source under the MIT License.

---

## 🙌 Acknowledgments

- [Astropy Project](https://www.astropy.org/)
- [Pygame](https://www.pygame.org/)
```

---

Fammi sapere se vuoi aggiungere anche uno **screenshot** o un **GIF animato** del programma in esecuzione per il README!
