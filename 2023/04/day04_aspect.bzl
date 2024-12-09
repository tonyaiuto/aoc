

CardInfo = provider(
    fields = {
        'card': 'card',
        'tot': 'accumulator',
        'count': 'how many have I acumulated',
        'left': 'how many have I acumulated',
    }
)

Wins = provider(
    fields = {
        'card': 'card',
        'wins': 'how many times this card won',
    }
)

def _card_winner_impl(target, ctx):
    if not ctx.rule.attr.dep:
      wins = target[Wins]
      return [CardInfo(card = ctx.label.name, tot = 1, count = 1, left=[wins.wins])]

    cc = ctx.rule.attr.dep[CardInfo]
    wins = target[Wins]

    # How many times this card appears
    # print("Child", cc.card, cc.count, cc.left)
    new_left = []
    count = cc.count
    for c in cc.left:
      if c > 0:
        count += 1
        new_left.append(c - 1)
    new_left.append(wins.wins)
    print("Child", cc.card, 'count', cc.count, '=>', count, cc.left, '=>', new_left)
    return [CardInfo(card = ctx.label.name, tot = cc.tot + count, count = count, left = new_left)]

card_winner = aspect(
    implementation = _card_winner_impl,
    attr_aspects = ['dep'],
)

def _card_impl(ctx):
    w = {x: 1 for x in ctx.attr.winners}
    wins = 0
    for x in ctx.attr.got:
      if x in w:
        wins += 1
    print('card %s, wins: %d' % (ctx.label.name, wins))
    if ctx.attr.dep:
        cc = ctx.attr.dep[CardInfo]
        print(" RULE: dep", cc.card, 'tot=%d'%cc.tot, 'count', cc.count, cc.left)

        new_left = []
        count = cc.count
        for c in cc.left:
          if c > 0:
            count += 1
            new_left.append(c - 1)
        new_left.append(wins)
        print("Child", cc.card, 'count', cc.count, '=>', count, cc.left, '=>', new_left)
        return [
            Wins(card = int(ctx.label.name), wins = wins),
        CardInfo(card = ctx.label.name, tot = cc.tot + count, count = count, left = new_left)]

    return [Wins(card = int(ctx.label.name), wins = wins),
            CardInfo(card = ctx.label.name, tot = 1, count = 1, left=[wins])]

_card = rule(
    implementation = _card_impl,
    attrs = {
        "winners": attr.int_list(),
        "got": attr.int_list(),
        # "dep": attr.label(aspects = [card_winner]),
        "dep": attr.label(),
    }
)

def card(name, winners, got):
  numb = int(name)
  dep = ':%d' % (numb - 1) if numb > 1 else None
  _card(
    name = name,
    winners = winners,
    got = got,
    dep = dep,
  )
