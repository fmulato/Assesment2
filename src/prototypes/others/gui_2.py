import dearpygui.dearpygui as dpg

def say_hello():
    name = dpg.get_value("name_input")
    dpg.set_value("greeting_text", f"Hi, {name}!")

dpg.create_context()

dpg.create_viewport(title='Window in Dear PyGui', width=800, height=600)

with dpg.window(label="Greetings", width=800, height=600):
    dpg.add_input_text(tag="name_input", label="What's your name?")
    dpg.add_button(label="Say Hello", callback=say_hello)
    dpg.add_text("", tag="greeting_text")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
