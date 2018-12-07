from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import heapq
import sys

"""
You find yourself standing on a snow-covered coastline; apparently, you
landed a little off course. The region is too hilly to see the North
Pole from here, but you do spot some Elves that seem to be trying to
unpack something that washed ashore. It's quite cold out, so you decide
to risk creating a paradox by asking them for directions.

"Oh, are you the search party?" Somehow, you can understand whatever Elves
from the year 1018 speak; you assume it's Ancient Nordic Elvish. Could
the device on your wrist also be a translator? "Those clothes don't look
very warm; take this." They hand you a heavy coat.

"We do need to find our way back to the North Pole, but we have
higher priorities at the moment. You see, believe it or not, this
box contains something that will solve all of Santa's transportation
problems - at least, that's what it looks like from the pictures in the
instructions." It doesn't seem like they can read whatever language it's
in, but you can: "Sleigh kit. Some assembly required."

"'Sleigh'? What a wonderful name! You must help us assemble this 'sleigh'
at once!" They start excitedly pulling more parts out of the box.

The instructions specify a series of steps and requirements about which
steps must be finished before others can begin (your puzzle input). Each
step is designated by a single letter. For example, suppose you have
the following instructions:

Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
Visually, these requirements look like this:


  -->A--->B--
 /    \      \
C      -->D----->E
 \           /
  ---->F-----
Your first goal is to determine the order in which the steps should be
completed. If more than one step is ready, choose the step which is first
alphabetically. In this example, the steps would be completed as follows:

Only C is available, and so it is done first.
Next, both A and F are available. A is first alphabetically, so it is done next.
Then, even though F was available earlier, steps B and D are now also available, and B is the first alphabetically of the three.
After that, only D and F are available. E is not available because only some of its prerequisites are complete. Therefore, D is completed next.
F is the only choice, so it is done next.
Finally, E is completed.
So, in this example, the correct order is CABDFE.

In what order should the steps in your instructions be completed?
"""

class Step(object):

  steps = {}

  def __init__(this, name):
    this.name = name
    # Number of things I depend on
    this.time = 61 + ord(name.lower()) - ord('a')
    this.finish = 0
    this.dep_count = 0
    # Who depends on me
    this.dependants = set()
    Step.steps[name] = this

  def __str__(this):
    return 'Step(%s dep=%d, time=%d precedes %s)' % (
        this.name, this.dep_count, this.time, this.dependants)

  def AddDependant(this, name):
    if name not in this.dependants:
      this.dependants.add(name)
      Step.ByName(name).dep_count += 1

  def Finish(this):
    this.dep_count = -1
    for d in this.dependants:
      Step.ByName(d).dep_count -= 1

  @staticmethod
  def ByName(name):
    return Step.steps.get(name) or Step(name)


def LoadSteps(inp):
  for l in inp:
    pre, after = l.strip().split(' ')
    Step.ByName(pre).AddDependant(after)


def part1():
  ret = ''
  while True:
    # Pick next step
    to_do = 'ZZZZZ'
    for step_name in Step.steps:
      s = Step.ByName(step_name)
      if s.dep_count == 0 and step_name < to_do:
        to_do = step_name
    if to_do == 'ZZZZZ':
      break
    step_to_do = Step.ByName(to_do)
    # print('Doing %s' % step_to_do)
    ret += to_do
    step_to_do.Finish()
  return ret

"""
As you're about to begin construction, four of the Elves offer
to help. "The sun will set soon; it'll go faster if we work
together." Now, you need to account for multiple people working on steps
simultaneously. If multiple steps are available, workers should still
begin them in alphabetical order.

Each step takes 60 seconds plus an amount corresponding to its letter:
A=1, B=2, C=3, and so on. So, step A takes 60+1=61 seconds, while step
Z takes 60+26=86 seconds. No time is required between steps.

To simplify things for the example, however, suppose you only have
help from one Elf (a total of two workers) and that each step takes
60 fewer seconds (so that step A takes 1 second and step Z takes 26
seconds). Then, using the same instructions as above, this is how each
second would be spent:

Second   Worker 1   Worker 2   Done
   0        C          .
   1        C          .
   2        C          .
   3        A          F       C
   4        B          F       CA
   5        B          F       CA
   6        D          F       CAB
   7        D          F       CAB
   8        D          F       CAB
   9        D          .       CABF
  10        E          .       CABFD
  11        E          .       CABFD
  12        E          .       CABFD
  13        E          .       CABFD
  14        E          .       CABFD
  15        .          .       CABFDE

Each row represents one second of time. The Second column identifies
how many seconds have passed as of the beginning of that second. Each
worker column shows the step that worker is currently doing (or . if
they are idle). The Done column shows completed steps.

Note that the order of the steps has changed; this is because steps
now take time to finish and multiple workers can begin multiple steps
simultaneously.

In this example, it would take 15 seconds for two workers to complete these steps.

With 5 workers and the 60+ second step durations described above, how long will it take to complete all of the steps?
"""


def part2():
  workers = [0] * 5
  running = [''] * 5
  ret = ''
  sec = -1 
  doing_work = True
  while True:
    sec += 1
    doing_work = False
    for i in range(len(workers)):
      if workers[i] > 0:
        workers[i] -= 1
        if workers[i] == 0:
          done = running[i]
          dt = Step.ByName(done)
          print('worker %d finished %s at %d, expected %d' % (i, do_name, sec, dt.finish))
          dt.Finish()
          running[i] = ''
        else:
          doing_work = True
      elif workers[i] < 0:
        raise ValueError('wtf %s' % workers)

    # Pick next step
    dispatchable = []
    for step_name in Step.steps:
      s = Step.ByName(step_name)
      # if s.dep_count == 0 and step_name not in dispatchable and step_name not in running:
      if s.dep_count == 0 and step_name not in dispatchable:
        heapq.heappush(dispatchable, step_name)
    print('second %d, %d dispatchable' % (sec, len(dispatchable)))

    if len(dispatchable) == 0 and not doing_work:
      break

    for i in range(len(workers)):
      if workers[i] == 0:
        try:
          do_name = heapq.heappop(dispatchable)
          if not do_name:
            raise ValueError('wtf null in %s' % dispatchable)

          do_step = Step.ByName(do_name)
          workers[i] = do_step.time
          do_step.finish = sec + do_step.time
          running[i] = do_name
          do_step.dep_count = -1

          print('give %s to worker %d at %d' % (do_name, i, sec))
          doing_work = True
          ret += do_name
        except IndexError:
          pass
  print('%d seconds' % sec)
  return ret

if __name__ == '__main__':
  with open(sys.argv[1]) as inp:
    LoadSteps(inp)
  if True:
    for s in Step.steps:
      print(Step.ByName(s))
  # print('part1: %s' % part1())
  print('part2: %s' % part2())
