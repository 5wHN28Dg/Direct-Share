import dearpygui.dearpygui as dpg

dpg.create_context()

# add a font registry
with dpg.font_registry():
    # first argument ids the path to the .ttf or .otf file
    default_font = dpg.add_font("font/ProggyVector-Regular.otf", 75)

dpg.create_viewport(title="Direct Share", width=1280, height=720)

with dpg.window(label="Example Window", no_title_bar=True, tag="Main Window"):
    dpg.bind_font(default_font)
    dpg.add_button(label="search for peers", callback=search_callback)
    dpg.add_listbox(items=[], callback=callback, tag="Peer List", show=False)

    with dpg.file_dialog(
        show=False,
        callback=callback,
        tag="file_dialog_id",
        cancel_callback=cancel_callback,
        width=1280,
        height=720,
    ):
        dpg.add_file_extension(".*")
        dpg.add_file_extension("", color=(150, 255, 150, 255))
        dpg.add_file_extension(
            "Source files (*.cpp *.h *.hpp){.cpp,.h,.hpp}", color=(0, 255, 255, 255)
        )
        dpg.add_file_extension(".h", color=(255, 0, 255, 255), custom_text="[header]")
        dpg.add_file_extension(".py", color=(0, 255, 0, 255), custom_text="[Python]")
    dpg.add_button(
        label="file Selector", callback=lambda: dpg.show_item("file_dialog_id")
    )
    dpg.add_button(label="connect", callback=connect_callback)
    dpg.add_button(label="send")
dpg.setup_dearpygui()
dpg.set_primary_window("Main Window", True)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
