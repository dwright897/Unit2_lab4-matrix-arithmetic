#Dalton Wright
#10/9/24
#Bear Fish River


from ecosystem import *
from time import sleep

DAYS_SIMULATED =30
RIVER_SIZE = 15
START_BEARS = 10
START_FISH = 10

def BearFishRiver():


  r = River(RIVER_SIZE, START_BEARS, START_FISH)
  day = 0
  done = False
  for day in range(DAYS_SIMULATED):
    print("".center(50,"-"))
    print(f"\n\nDay: {day+1}")
    print(r)
    print(f"\nStarting Poplation: {r.population} animals")
    done = r.new_day()
    print(f"Ending Poplation: {r.population} animals")
    print(r)
    day += 1
    sleep(5)
    if r.population == (RIVER_SIZE**2):
      print("⚠️ The river is full and the simulation will now end. ⚠️")
      break
    elif r.population <= 0:
      print("⚠️The river is empty! The simulation will now end. ⚠️")
      break
    elif day == DAYS_SIMULATED:
      print(f"The simulation reached {DAYS_SIMULATED} days and has ended.")
      
def main():
  BearFishRiver()
if __name__ == "__main__":
  main()