import tkinter

button_values = [
    ["AC", "+/-", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "√", "="]
]

right_symbols = ["÷", "×", "-", "+", "="]
top_symbols = ["AC", "+/-", "%", "√"]

row_count = len(button_values)
column_count = len(button_values[0])

# --- Dark Blue Color Scheme ---
color_dark_blue = "#0A192F"
color_blue_gray = "#112240"
color_light_blue = "#233554"
color_accent = "#64FFDA"
color_white = "#FFFFFF"
color_gray = "#8892B0"

window = tkinter.Tk()
window.title("Calculator")
window.resizable(True, True)
window.configure(bg=color_dark_blue)

frame = tkinter.Frame(window, bg=color_dark_blue)
frame.pack(fill="both", expand=True)

# Configure grid weights for scalability
frame.grid_rowconfigure(0, weight=2)
for r in range(1, row_count + 1):
    frame.grid_rowconfigure(r, weight=1)
for c in range(column_count):
    frame.grid_columnconfigure(c, weight=1)

label = tkinter.Label(
    frame, text="0", font=("Arial", 45), background=color_dark_blue,
    foreground=color_accent, anchor="e"
)
label.grid(row=0, column=0, columnspan=column_count, sticky="nsew", padx=2, pady=2)

# --- Circular Buttons using Canvas ---
button_canvases = []
button_radius = 48

def on_canvas_click(event, value):
    button_clicked(value)

for row in range(row_count):
    canvas_row = []
    for column in range(column_count):
        value = button_values[row][column]
        canvas = tkinter.Canvas(
            frame,
            width=button_radius*2, height=button_radius*2,
            bg=color_dark_blue, highlightthickness=0
        )
        # Choose color
        if value in top_symbols:
            fill_color = color_accent
            text_color = color_dark_blue
        elif value in right_symbols:
            fill_color = color_light_blue
            text_color = color_white
        else:
            fill_color = color_blue_gray
            text_color = color_white

        # Draw circle
        circle = canvas.create_oval(
            4, 4, button_radius*2-4, button_radius*2-4,
            fill=fill_color, outline=fill_color
        )
        # Draw text
        canvas.create_text(
            button_radius, button_radius,
            text=value, fill=text_color, font=("Arial", 24, "bold")
        )
        # Bind click event
        canvas.bind("<Button-1>", lambda e, v=value: on_canvas_click(e, v))
        canvas.grid(row=row+1, column=column, padx=8, pady=8, sticky="nsew")
        canvas_row.append(canvas)
    button_canvases.append(canvas_row)

A = "0"
operator = None
B = None

def clear_all():
    global A, B, operator
    A = "0"
    operator = None
    B = None

def remove_zero_decimal(num):
    if num % 1 == 0:
        num = int(num)
    return str(num)

def button_clicked(value):
    global right_symbols, top_symbols, label, A, B, operator

    if value == "√":
        try:
            num = float(label["text"])
            if num < 0:
                label["text"] = "Error"
            else:
                label["text"] = remove_zero_decimal(num ** 0.5)
            clear_all()
        except Exception:
            label["text"] = "Error"
            clear_all()
        return

    if value in right_symbols:
        if value == "=":
            if A is not None and operator is not None:
                B = label["text"]
                numA = float(A)
                numB = float(B)

                if operator == "+":
                    label["text"] = remove_zero_decimal(numA + numB)
                elif operator == "-":
                    label["text"] = remove_zero_decimal(numA - numB)
                elif operator == "×":
                    label["text"] = remove_zero_decimal(numA * numB)
                elif operator == "÷":
                    try:
                        label["text"] = remove_zero_decimal(numA / numB)
                    except ZeroDivisionError:
                        label["text"] = "Error"
                clear_all()

        elif value in "+-×÷":
            if operator is None:
                A = label["text"]
                label["text"] = "0"
                B = "0"
            operator = value

    elif value in top_symbols:
        if value == "AC":
            clear_all()
            label["text"] = "0"

        elif value == "+/-":
            try:
                result = float(label["text"]) * -1
                label["text"] = remove_zero_decimal(result)
            except Exception:
                label["text"] = "Error"

        elif value == "%":
            try:
                result = float(label["text"]) / 100
                label["text"] = remove_zero_decimal(result)
            except Exception:
                label["text"] = "Error"
        
    else: #digits or .
        if value == ".":
            if value not in label["text"]:
                label["text"] += value

        elif value in "0123456789":
            if label["text"] == "0":
                label["text"] = value
            else:
                label["text"] += value


window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

window.mainloop()