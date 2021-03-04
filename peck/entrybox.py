from peck.ab_entry import AEntry


class TextBox():
    'a text box for taking in input and displaying it'

    def __init__(self, obj_ref: AEntry = None, attribute=None):
        from tkinter import Tk, Text, Button, mainloop
        self.text = None
        self.root = Tk()
        text_box = Text(self.root, height=15, width=50,
                           bg='#1c1d1c', fg='#fafbfa',
                           wrap='word',
                           highlightthickness=0,
                           selectbackground='#313231',
                           font=(None, 14))
        text_box.pack(side='bottom', fill='both', expand='yes')
        # auto focus on window to minimize clicking
        text_box.focus_force()

        button = Button(self.root, text='store',
                           command=lambda: get_text(),
                           font=(None, 12))
        button.pack(side='top', fill='both')

        def get_text():
            'retrieve input and destroy window'

            # refers to which section was passed, and assigns accordingly
            if attribute == 'first':
                obj_ref.first = text_box.get('1.0', 'end-1c')
            elif attribute == 'second':
                obj_ref.second = text_box.get('1.0', 'end-1c')
            elif attribute == 'title':
                obj_ref.title = text_box.get('1.0', 'end-1c')

            # destroy root
            self.root.after(1, self.root.destroy())

        mainloop()
