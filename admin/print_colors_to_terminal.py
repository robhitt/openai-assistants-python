from colorama import Fore, Back, Style

print("\033[1m============ Manual Colors ============\033[0m")
print("\033[91mThis is red text\033[0m")
print("\033[92mThis is green text\033[0m")
print("\033[94mThis is blue text\033[0m")
print("\033[93mThis is yellow text\033[0m")

print("\n")

print(f"{Fore.MAGENTA}============ Using colorama package ============{Style.RESET_ALL}")
print(f"{Back.CYAN}{Fore.BLUE}Robin Hood is a good movie.{Style.RESET_ALL}")
print(f"{Back.CYAN}{Fore.BLUE}{Style.BRIGHT}Robin Hood is a good movie.{Style.RESET_ALL}")
