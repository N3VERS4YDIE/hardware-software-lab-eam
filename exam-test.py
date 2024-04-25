import random

led_pins = (18, 22, 24, 26, 16)
button_pins = (32, 36, 38, 40, 37)

pattern = []
user_pattern = []

is_user_turn = False

def button_pressed(pin: int):
    if is_user_turn:
        try:
            i = led_pins.index(pin)
            mapped_led = led_pins[i]
            user_pattern.append(mapped_led)
        except ValueError:
            pass


def verify_pattern():
    for user_led, led in zip(user_pattern, pattern):
        if user_led != led:
            return False
    return True

def game_over():
    pattern.clear()
    print("\nGAME OVER\n")

while True:
    if is_user_turn:
        print(f"Select a led pin: {led_pins}")
        button_pressed(int(input("Pin: ")))
        if len(user_pattern) < len(pattern):
            continue

        if not verify_pattern():
            game_over()

        user_pattern.clear()
        is_user_turn = False

    else:
        next_random_led = random.choice(led_pins)
        pattern.append(next_random_led)

        print(f"\nPattern: {pattern}")
        is_user_turn = True