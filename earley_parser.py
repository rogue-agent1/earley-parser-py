#!/usr/bin/env python3
"""Earley parser — handles any context-free grammar."""
import sys

class Rule:
    def __init__(self,name,symbols): self.name=name; self.symbols=symbols
    def __repr__(self): return f"{self.name} -> {' '.join(self.symbols)}"

class Item:
    def __init__(self,rule,dot,origin):
        self.rule=rule; self.dot=dot; self.origin=origin
    def completed(self): return self.dot>=len(self.rule.symbols)
    def next_symbol(self): return self.rule.symbols[self.dot] if not self.completed() else None
    def __eq__(self,o): return self.rule==o.rule and self.dot==o.dot and self.origin==o.origin
    def __hash__(self): return hash((id(self.rule),self.dot,self.origin))

def earley_parse(grammar,start,tokens):
    chart=[set() for _ in range(len(tokens)+1)]
    for r in grammar:
        if r.name==start: chart[0].add(Item(r,0,0))
    for i in range(len(tokens)+1):
        queue=list(chart[i])
        while queue:
            item=queue.pop(0)
            if item.completed():
                for prev in chart[item.origin]:
                    if not prev.completed() and prev.next_symbol()==item.rule.name:
                        new=Item(prev.rule,prev.dot+1,prev.origin)
                        if new not in chart[i]: chart[i].add(new); queue.append(new)
            elif item.next_symbol() in {r.name for r in grammar}:
                for r in grammar:
                    if r.name==item.next_symbol():
                        new=Item(r,0,i)
                        if new not in chart[i]: chart[i].add(new); queue.append(new)
            elif i<len(tokens) and item.next_symbol()==tokens[i]:
                new=Item(item.rule,item.dot+1,item.origin)
                chart[i+1].add(new)
    return any(it.completed() and it.rule.name==start and it.origin==0 for it in chart[len(tokens)])

if __name__ == "__main__":
    grammar=[Rule("S",["NP","VP"]),Rule("NP",["det","noun"]),Rule("NP",["noun"]),
             Rule("VP",["verb","NP"]),Rule("VP",["verb"])]
    tests=[
        (["det","noun","verb","det","noun"],True),
        (["noun","verb"],True),
        (["verb","det"],False),
    ]
    for tokens,expected in tests:
        result=earley_parse(grammar,"S",tokens)
        print(f"  {'✅' if result==expected else '❌'} {tokens} -> {result}")
