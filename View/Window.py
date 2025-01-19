import tkinter as tk
import json
from tkinter import ttk
from tkhtmlview import HTMLLabel
import markdown

class Window():
    def __init__(self, on_send_callback=None, start=None):
        self.root = tk.Tk()
        self.on_send_callback = on_send_callback
        # Create the main menu
        self.main_menu = tk.Menu(self.root)
        self.start = start
       
    def menuBar(self):
        # print("MENU BAR", self.start)
        # Create the submenus
        CHAT = tk.Menu(self.main_menu, tearoff=0)
        CHAT.add_command(
            label="MISTRAL LARGE LASTED",
            command=lambda: (
                self.chatWithModels(),
                setattr(self.start, 'model', "MISTRAL LARGE MODEL") if self.start else None
            )
        )
        CHAT.add_command(
            label="GEMINI",
            command=lambda: (
                self.chatWithModels(), 
                setattr(self.start, 'model', "GEMINI 1.5-FLASH-LASTEST") if self.start else None
            )
        )
        TESTER = tk.Menu(self.main_menu, tearoff=0)
        TESTER.add_command(label="TESTER FORMULARZY", command=self.FormTester)
        # Add the submenus to the main menu
        self.main_menu.add_cascade(label="CHAT", menu=CHAT)
        self.main_menu.add_cascade(label="TESTER", menu=TESTER)
        # Add the main menu to the root window
        self.root.config(menu=self.main_menu)


    def WindowBox(self):
        self.root.title("HAMSTER")
        self.root.state('zoomed')
        self.menuBar()
        self.root.mainloop()

    def chatWithModels(self):
        top_frame = tk.Frame(self.root, bg='#333333')      # szerokość w pikselach
        top_frame.place(relx=0.01,      # 1% od lewej
                         rely=0.01,         # 1% od góry
                         relwidth=0.98,     # 98% szerokości okna
                         relheight=0.8)  
        top_frame.pack_propagate(False)

        self.response_label = HTMLLabel(top_frame, 
                                      background='#333333',
                                      foreground='white')
        self.response_label.place(relx=0.03, rely=0.01, relwidth=0.9, relheight=0.9, anchor='nw')
        # Frame na dole okna
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side='bottom', fill='x', pady=10, padx=10)
        # Textarea
        self.text_area = tk.Text(bottom_frame, height=6)
        self.text_area.pack(fill='x', pady=(0, 5))
        # self.text_area.bind('<Return>', self.on_send) # Przycisk Enter
        # Przycisk Wyślij
        send_button = tk.Button(bottom_frame, text="Wyślij", command=self.on_send)
        send_button.pack(side='right', padx=5)

    def on_send(self, event=None):
        text = self.text_area.get("1.0", "end-1c")
        if not text.strip():
            return
        
        loading_text = {
            "role": "assistant",
            "content": "Wysyłanie... ⏳"
        }
        self.display_response(json.dumps([loading_text]))

        self.text_area.delete("1.0", "end")  # Czyszczenie textarea
        self.text_area.mark_set("insert", "1.0")  # Ustawienie kursora na początek
        self.text_area.focus_set()  # Przywrócenie fokusu na textarea
        
        if self.on_send_callback:
            response = self.on_send_callback(text)  # odbieramy odpowiedź
            if response:
                self.display_response(response)  # wyświetlamy odpowiedź

    def display_response(self, text):
        """
        Wyświetla odpowiedź od modelu.
        :param text: Odpowiedź od modelu w formacie JSON
        :type text: str
        :return: None
        :rtype: None
        """
        if hasattr(self, 'response_label'):
            parsedText = json.loads(text)
            clearText = ''
            # Znajdujemy indeks ostatniego "user"
            last_user_index = -1
            for i, valText in enumerate(parsedText):
                if valText['role'] == 'user':
                    last_user_index = i

            for j, valText in enumerate(parsedText):
                if(j == 0 and valText['role'] == 'user'):
                    continue

                if valText['role'] == 'user':
                    colorText = "#fff"
                else:
                    colorText = "#ffdd00"

                 # Zamieniamy kropki na escape sequence w numeracji
                responseText = valText.get('content') or ''.join(valText.get('parts', []))
                content = responseText
                content = content.replace('1.', '1\\.')
                content = content.replace('2.', '2\\.')
                content = content.replace('3.', '3\\.')

                md = markdown.Markdown(extensions=['fenced_code', 'tables', 'nl2br'])
                content_html = md.convert(content)
                # Dodajemy id do diva jeśli to ostatni user
                div_id = ' id="last-user"' if i == last_user_index else ''
                clearText += f'''
                <div {div_id} style="color: {colorText}; margin-top: 1px; padding-bottom: 1px;">
                <b>{valText['role'].upper()}</b>
                <br />
                <i style="font-size: 11px;">{content_html}</i></div>
                '''

            self.response_label.set_html(clearText)
            self.response_label.update()  # Aktualizujemy widget
            # Przewijamy do ostatniego "user" jeśli istnieje
            if last_user_index != -1:
                self.response_label.yview_moveto(last_user_index / len(parsedText))

    def FormTester(self):
        self.wyczysc_ekran()
        print('FORM TESTER')

    def wyczysc_ekran(self):
        for widget in self.root.winfo_children():
            if widget != self.main_menu:
                widget.destroy()