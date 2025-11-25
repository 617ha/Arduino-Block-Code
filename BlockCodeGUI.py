import tkinter as tk
from main import *

ser = connect_serial()
DROP_HEIGHT = 25  # drop area height

class DraggableBlock:
    def __init__(self, canvas, x, y, text="Block", color="#2b2b2b"):
        self.canvas = canvas
        self.text = text
        self.color = color
        self.tag = f"block_{id(self)}"
        self.child = None  # connected block

        w, h = 120, 50
        self.width = w
        self.height = h

        # Rectangle + text
        self.rect = canvas.create_rectangle(
            x, y, x + w, y + h,
            fill=color, outline="#6ea8fe", width=2, tags=(self.tag,)
        )
        self.label = canvas.create_text(
            x + w // 2, y + h // 2,
            text=text, fill="white", font=("Arial", 12), tags=(self.tag,)
        )

        # Drop area
        self.drop_area = canvas.create_rectangle(
            x, y + h, x + w, y + h + DROP_HEIGHT,
            fill="#1f1f1f", outline="#444444", dash=(2,2),
            tags=(self.tag + "_drop",)
        )

        self._drag_data = {"x":0, "y":0}

        # Bind events
        canvas.tag_bind(self.tag, "<ButtonPress-1>", self.on_press)
        canvas.tag_bind(self.tag, "<B1-Motion>", self.on_motion)
        canvas.tag_bind(self.tag, "<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        self.canvas.tag_raise(self.tag)
        self.canvas.tag_raise(self.tag + "_drop")

    def on_motion(self, event):
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        self.move_by(dx, dy)
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_release(self, event):
        # Snap to drop areas
        for block in self.canvas.blocks:
            if block == self:
                continue
            x1, y1, x2, y2 = self.canvas.coords(block.drop_area)
            bx1, by1, bx2, by2 = self.canvas.coords(self.rect)
            if (bx2 > x1 and bx1 < x2) and (by2 > y1 and by1 < y2):
                dx = x1 - bx1
                dy = y1 - by1
                self.move_by(dx, dy)
                if block.child:
                    block.child.move_by(0, self.height + DROP_HEIGHT)
                block.child = self
                return

    def move_by(self, dx, dy):
        self.canvas.move(self.tag, dx, dy)
        self.canvas.move(self.tag + "_drop", dx, dy)
        if self.child:
            self.child.move_by(dx, dy)

def collect_sequence(block):
    seq = [block.text]
    child = block.child
    while child:
        seq.append(child.text)
        child = child.child
    return seq

def main():
    root = tk.Tk()
    root.title("Block Chain Demo")
    root.geometry("900x600")
    root.configure(bg="#1E1F21")

    # Left frame (sidebar)
    sidebarcolor = "#141414"
    sidebar = tk.Frame(root, width=220, bg=sidebarcolor)
    sidebar.pack(side="left", fill="y", padx=15, pady=15)

    tk.Label(sidebar, text="Arudino block code", font=("Arial", 16, "bold"), bg=sidebarcolor, fg="white").pack(pady=(10,8))

    canvas_frame = tk.Frame(root)
    canvas_frame.pack(side="right", expand=True, fill="both", padx=12, pady=12)

    canvas = tk.Canvas(canvas_frame, bg="#0f1720", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.blocks = []

    # First block: Run
    run_block = DraggableBlock(canvas, 40, 40, text="Run", color="#ff8000")
    canvas.blocks.append(run_block)

    def remove_letter(lst, letter):
        return [s.replace(letter, "") for s in lst]

    def replace_letter(lst, letter, replace):
        return [s.replace(letter, replace) for s in lst]

    def list_convert(lst):
        lst = remove_letter(lst, ")")
        lst = remove_letter(lst, "(")
        lst = replace_letter(lst, "servo", "Servo")
        lst = replace_letter(lst, "digpin", "Digital")
        lst = replace_letter(lst, "anapin", "Analog")
        lst = replace_letter(lst, "sleep", "Sleep")
        del lst[0]
        return lst

    def run_sequence():
        seq = collect_sequence(run_block)
        seq = list_convert(seq)
        for f in seq:
            sc(ser, f)
        print(seq)

    tk.Button(sidebar, text="Run", command=run_sequence, bg="#ff8000", fg="white").pack(pady=6, fill="x", padx=12)


    # Add block button
    def sleep():
        num = len(canvas.blocks)
        val = entry1.get()
        if val.isnumeric():
            val = int(val)
        else:
            val = 0
        block = DraggableBlock(canvas, 200, 50 + num*70, text=f"sleep ({val})", color="#459DD0")
        canvas.blocks.append(block)

    tk.Button(sidebar, text="sleep [param1]", command=sleep, bg="#459DD0", fg="white").pack(pady=6, fill="x", padx=12)

    def digitalpin():
        num = len(canvas.blocks)
        val = entry1.get()
        val2 = entry2.get()
        if val.isnumeric():
            val = int(val)
        else:
            val = 0

        if val2.lower() == "on":
            val2 = "ON"
        else:
            val2 = "OFF"
        block = DraggableBlock(canvas, 200, 50 + num*70, text=f"digpin ({val}) ({val2})", color="#E44384")
        canvas.blocks.append(block)

    tk.Button(sidebar, text="digitalpin [param1][param2]", command=digitalpin, bg="#E44384", fg="white").pack(pady=6, fill="x", padx=12)

    def analogpin():
        num = len(canvas.blocks)
        val = entry1.get()
        val2 = entry2.get()
        if val.isnumeric():
            val = int(val)
        else:
            val = 0

        if val2.isnumeric():
            val2 = int(val2)
        else:
            val2 = 0
        block = DraggableBlock(canvas, 200, 50 + num*70, text=f"anapin ({val}) ({val2})", color="#E44384")
        canvas.blocks.append(block)

    tk.Button(sidebar, text="analogpin [param1][param2]", command=analogpin, bg="#E44384", fg="white").pack(pady=6, fill="x", padx=12)

    def servo():
        num = len(canvas.blocks)
        val = entry1.get()
        val2 = entry2.get()
        if val.isnumeric():
            val = int(val)
        else:
            val = 0

        if val2.isnumeric():
            val2 = int(val2)
            if val2 > 180:
                val2 = 180
        else:
            val2 = 90
        block = DraggableBlock(canvas, 200, 50 + num*70, text=f"servo ({val}) ({val2})", color="#C696BE")
        canvas.blocks.append(block)

    tk.Button(sidebar, text="Servo [param1][param2]", command=servo, bg="#C696BE", fg="white").pack(pady=6, fill="x", padx=12)


    def add_block():
        num = len(canvas.blocks)
        block = DraggableBlock(canvas, 200, 50 + num*70, text=f"Block {num}")
        canvas.blocks.append(block)

    tk.Button(sidebar, text="Add Block", command=add_block, bg="#2b2b2b", fg="white").pack(pady=6, fill="x", padx=12)

    # Clear button
    def clear_canvas():
        nonlocal run_block  # allow reassignment of run_block

        # 1) Break child links BEFORE clearing visuals/list
        for block in canvas.blocks:
            block.child = None

        # 2) Clear canvas and list
        canvas.delete("all")
        canvas.blocks.clear()

        # 3) Recreate Run block and update run_block reference
        run_block = DraggableBlock(canvas, 40, 40, text="Run", color="#ff8000")
        canvas.blocks.append(run_block)

    tk.Button(sidebar, text="Clear Canvas", command=clear_canvas, bg="#2b2b2b", fg="white").pack(pady=6, fill="x", padx=12)

    param1_frame = tk.Frame(sidebar, bg=sidebarcolor)
    param1_frame.pack(fill="x", pady=5)

    tk.Label(param1_frame, text="Parameter 1", font=("Arial", 10, "bold"), bg=sidebarcolor, fg="white").pack(anchor="w")
    entry1 = tk.Entry(param1_frame, bg="white", fg="black")
    entry1.pack(pady=2, padx=3, side="left")

    # Frame for Parameter 2
    param2_frame = tk.Frame(sidebar, bg=sidebarcolor)
    param2_frame.pack(fill="x", pady=5)

    tk.Label(param2_frame, text="Parameter 2", font=("Arial", 10, "bold"), bg=sidebarcolor, fg="white").pack(anchor="w")
    entry2 = tk.Entry(param2_frame, bg="white", fg="black")
    entry2.pack(pady=2, padx=3, side="left")
    root.mainloop()

if __name__ == "__main__":
    main()
