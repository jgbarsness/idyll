import tkinter as tk


class TextBox():
    'a text box for taking in input and displaying it'
    def __init__(self, object_passed, attribute):
        self.text = None
        self.root = tk.Tk()
        text_box = tk.Text(self.root, height=15, width=50,
                           bg='#1c1d1c', fg='#fafbfa',
                           wrap='word',
                           highlightthickness=0,
                           selectbackground='#313231',
                           font=(None, 14))
        text_box.pack(side='bottom', fill='both', expand='yes')
        # auto focus on window to minimize clicking
        text_box.focus_force()

        button = tk.Button(self.root, text='store',
                           command=lambda: get_text(),
                           font=(None, 12))
        button.pack(side='top', fill='both')

        def get_text():
            'retrieve input and destroy window'
            if attribute == 'note':
                object_passed.notes = text_box.get('1.0', 'end-1c')
            elif attribute == 'why':
                object_passed.why = text_box.get('1.0', 'end-1c')

            # delay needed to allow information passing / prevent freezes
            # delay 1ms
            self.root.after(1, self.root.destroy())

        tk.mainloop()
