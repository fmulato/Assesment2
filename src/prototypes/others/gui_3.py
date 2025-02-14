import flet as ft

def main(page: ft.Page):
    page.title = "Window in Flet"

    def say_hello(e):
        name = name_input.value
        greeting_text.value = f"Hi, {name}!"
        page.update()

    name_input = ft.TextField(label="What's your name?")
    greeting_text = ft.Text()
    hello_button = ft.ElevatedButton("Say Hello", on_click=say_hello)

    page.add(name_input, hello_button, greeting_text)

ft.app(target=main)

