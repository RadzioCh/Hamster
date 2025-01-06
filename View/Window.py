import tkinter as tk
import json
from tkinter import ttk
from tkhtmlview import HTMLLabel

class Window():
    def __init__(self, on_send_callback=None):
        self.on_send_callback = on_send_callback
       


    def WindowBox(self):
        root = tk.Tk()
        root.title("POLIGON")
        root.state('zoomed')

        top_frame = tk.Frame(root, bg='#333333')      # szerokość w pikselach
        
        top_frame.place(relx=0.01,      # 1% od lewej
                         rely=0.01,         # 1% od góry
                         relwidth=0.98,     # 98% szerokości okna
                         relheight=0.8)  
        top_frame.pack_propagate(False)

        # self.response_label = tk.Label(top_frame, 
        #                 text="Twój tekst tutaj",
        #                 bg='#333333',  # tło takie samo jak frame
        #                 fg='white')    # kolor tekstu
        # self.response_label .place(relx=0.99, rely=0.01, anchor='ne')

        self.response_label = HTMLLabel(top_frame, 
                                      background='#333333',
                                      foreground='white')
        self.response_label.place(relx=0.99, rely=0.01, anchor='ne')



        # Frame na dole okna
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(side='bottom', fill='x', pady=10, padx=10)
        # Textarea
        self.text_area = tk.Text(bottom_frame, height=4)
        self.text_area.pack(fill='x', pady=(0, 5))
        self.text_area.bind('<Return>', self.on_send)
        # Przycisk Wyślij
        send_button = tk.Button(bottom_frame, text="Wyślij", command=self.on_send)
        send_button.pack(side='right', padx=5)

        root.mainloop()

    def on_send(self, event=None):
        text = self.text_area.get("1.0", "end-1c")
        self.text_area.delete("1.0", "end")  # Czyszczenie textarea
        self.text_area.mark_set("insert", "1.0")  # Ustawienie kursora na początek
        self.text_area.focus_set()  # Przywrócenie fokusu na textarea
        
        if self.on_send_callback:
            response = self.on_send_callback(text)  # odbieramy odpowiedź
            if response:
                self.display_response(response)  # wyświetlamy odpowiedź

    def display_response(self, text):
        if hasattr(self, 'response_label'):
            parsedText = json.loads(text)
            print(parsedText)

            clearText = ''
            for valText in parsedText:
                print(valText)
                clearText += '<b>'+valText['role']+'</b><br /><i>'+valText['content']+'</i><br />'

            self.response_label.set_html(clearText)