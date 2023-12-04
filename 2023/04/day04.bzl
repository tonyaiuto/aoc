# AoC - day4
#
# This is actually not that interesting. Just a recursive solution
# using deps to point to the recursion.  I was hoping it would have
# to be interesting with an aspect traversal.
#
#  ./to_build.sh <input.txt >BUILD
#  bazel build part2.txt
#  cat bazel-bin/part2.txt

CardInfo = provider(
    fields = {
        'card': 'card',
        'tot': 'accumulator',
        'count': 'how many have I acumulated',
        'left': 'how many have I acumulated',
        'counts': 'how many of each of those left',
    }
)

def _card_impl(ctx):
    # How many winners to I have?
    w = {x: 1 for x in ctx.attr.winners}
    wins = 0
    for x in ctx.attr.got:
      if x in w:
        wins += 1

    # print('card %s, wins: %d' % (ctx.label.name, wins))
    if ctx.attr.dep:
        cc = ctx.attr.dep[CardInfo]
        # print(" dep card", cc.card, 'tot=%d'%cc.tot, 'count', cc.count, cc.left, cc.counts)

        count = 1  # start with one of this card
        # for each active previous card, add in the number of instance of it
        new_left = []
        new_counts = []
        for ic in range(len(cc.left)):
          c = cc.left[ic]
          if c > 0:
            count += cc.counts[ic]
            new_left.append(c - 1)
            new_counts.append(cc.counts[ic])
        new_left.append(wins)
        new_counts.append(count)

        tot = cc.tot + count

        # print(" ret", ctx.label.name, 'tot:%d' % tot, 'mycount:%d'%count, cc.left, '=>', new_left)
        if ctx.outputs.out:
            ctx.actions.write(
                ctx.outputs.out,
                content="""card: %s, total cards:%d, my count = %d\n""" % (ctx.label.name, tot, count))
        return [
            CardInfo(
                card = ctx.label.name,
                tot = tot,
                count = count,
                left = new_left,
                counts = new_counts)
        ]
    return [CardInfo(card = ctx.label.name, tot = 1, count = 1, left=[wins], counts=[1])]

_card = rule(
    implementation = _card_impl,
    attrs = {
        "winners": attr.int_list(),
        "got": attr.int_list(),
        "dep": attr.label(),
        "out": attr.output(mandatory=False),
    }
)

def card(name, winners, got, out=None):
  numb = int(name)
  dep = ':%d' % (numb - 1) if numb > 1 else None
  _card(
    name = name,
    winners = winners,
    got = got,
    dep = dep,
    out = out,
  )
