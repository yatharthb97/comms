

from colorama import Fore, Style

def radio(code=0, status=False, rt=[0,0]):
	
	tcode	 = f"{Fore.CYAN}RTDevice{Fore.RESET}"
	
	code = 'D-' + str(code).ljust(4)
	
	if status:
		s = f"\033[32;5m{'(*)'}\033[0m{Fore.RESET}"
	else:
		s = f"{Style.DIM}{'(•)'}{Style.RESET_ALL}"

	cmap = {True: lambda string: f"{Fore.GREEN}{string.upper()}{Fore.RESET}",
		    False: lambda string :f"{Style.DIM}{string.lower()}{Style.RESET_ALL}" }

	rRiTt = f"< {cmap[rt[0]]('R')}{cmap[False]('|')}{cmap[rt[1]]('T')} >"

	illu = \
f"""    o       o   
     ╲     /    
      ╲   /     
       ╲ /      
  ┌─•───╩────•─┐
  │ │{tcode }│ │
  │ •───••───• │
  │ ╭────────╮ │
  │ │     {s}│ │
  │ │ {code} │ │
  │ │        │ │
  │ │{rRiTt} │ │
  │ ╰────────╯ │
  └────────────┘"""

	return illu