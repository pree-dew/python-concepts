import asyncio

def regular_func():
    return "my_func"
    
async def coroutine():
    return "my_coroutine"

m1 = regular_func()
m2 = asyncio.run(coroutine())
    
print(f"Regular function returned {m1} and it's type {type(m1)}")
print(f"Coroutine function returned {m2} and it's type {type(m2)}")
