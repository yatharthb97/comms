#Test File for UD Counter

from counter import UD_Counter


counter = UD_Counter()
print(counter.updater(4))

counter.set_up_counter(0)
print(counter.val())
print(counter.update())
print(counter.val())

print(counter.update())
print(counter.val())

print("down")
counter.set_down_counter(10)
print(counter.val())
print(counter.update())
print(counter.val())