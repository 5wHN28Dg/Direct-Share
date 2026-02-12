async_loop = asyncio.new_event_loop()


def start_async_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


threading.Thread(target=start_async_loop, args=(async_loop,), daemon=True).start()
