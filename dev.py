

from colorama import Fore, Style

def print_(code=0, status=False, rt=[0,0]):
	
	transpond = f"{Fore.CYAN}TRANSPONDER{Fore.RESET}"
	
	code = 'D-' + str(code).ljust(6)
	
	if status:
		s = f"\033[32;5m{'(*)'}\033[0m{Fore.RESET}"
	else:
		s = f"{Style.DIM}{'(•)'}{Style.RESET_ALL}"

	cmap = {True: lambda string: f"{Fore.GREEN}{string.upper()}{Fore.RESET}",
		    False: lambda string :f"{Style.DIM}{string.lower()}{Style.RESET_ALL}" }

	rRiTt = f"< {cmap[rt[0]]('R')}{cmap[False]('|')}{cmap[rt[1]]('T')} >"

	illu = \
f"""     o       o   
      ╲     /    
       ╲   /     
        ╲ /      
  ┌──────╩──────┐
  │•{transpond}•│
  │ ___________ │
  │ ╭─────────╮ │
  │ │      {s}│ │
  │ │{ code } │ │
  │ │         │ │
  │ │{rRiTt}  │ │
  │ ╰─────────╯ │
  └─────────────┘"""

	return illu


if __name__ == "__main__":


	print(repr(Fore.GREEN))
	print_(rt=[1, 0])
	i = print_(status=True, rt=[1, 1])
	i = i.split('\n')


	x = ['But I must explain to you', ' how all this mistaken id', 'ea of denouncing pleasure', ' and praising pain was bo', 'rn and I will give you a ', 'complete account of the s', 'ystem, and expound the ac', 'tual teachings of the gre', 'at explorer of the truth,', ' the master-builder of hu', 'man happiness. No one rej', 'ects, dislikes, or avoids', ' pleasure itself, because', ' it is pleasure, but beca', 'use those who do not know', ' how to pursue pleasure r', 'ationally encounter conse', 'quences that are extremel', 'y painful. Nor again is t', 'here anyone who loves or ', 'pursues or desires to obt', 'ain pain of itself, becau', 'se it is pain, but becaus', 'e occasionally circumstan', 'ces occur in which toil a', 'nd pain can procure him s', 'ome great pleasure. To ta', 'ke a trivial example, whi', 'ch of us ever undertakes ', 'laborious physical exerci', 'se, except to obtain some', ' advantage from it? But w', 'ho has any right to find ', 'fault with a man who choo', 'ses to enjoy a pleasure t', 'hat has no annoying conse', 'quences, or one who avoid', 's a pain that produces no', ' resultant pleasure?']

	max_len = max([chars.find('│') or chars.find('/') or chars.find('o')for chars in i])
	for idx in range(len(i)):
		print(f"{i[idx].ljust(max_len, '0')}  {x[idx].lstrip()}")