def regular_func():
	return "my_regular"
	
async def coroutine():
	return "my_coroutine"
	

def main():
   m1 = regular_func()
   m2 = coroutine()
   
   print(f"Regular function returned {m1} and it's type type({m1})")
   print(f"Corutine function returned {m2} and it's type type({m2})")

if __name__ == "__main__":
    main()
