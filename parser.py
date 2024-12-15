out = open("facts.clp", "w+")

facts = {}

out.write("\n(deffacts possible-facts")
for line in open("games-knowledge-base\\facts.md", "r").readlines():
    if line.startswith('#') or line.strip() == "":
        continue
    fact_index = line.split(":")[0].strip()
    fact_name = line.split(":")[1].strip()
    facts[fact_index] = fact_name
    out.write(f"\n(possible-fact (name \"{fact_name}\"))")
out.write("\n)")

for i, line in enumerate(open("games-knowledge-base\\rules.md", "r").readlines()):
    if line.startswith('#') or line.strip() == "":
        continue
    from_facts = line.split("->")[0].strip().split(";")
    to_fact = line.split("->")[1].strip()

    rule_token = f"\n(deffacts rule-token-{i} (token (name \"rule_{i}\")))"
    out.write(rule_token)

    # Write first rule (if fact not exists)
    s1 = f"\n(defrule rule{i}_1"
    for fact_index in from_facts:
        s1 += f"\n(fact (name \"{facts[fact_index.strip()]}\") (certainty ?c{fact_index.strip()}))"
    s1 += f"\n(not (exists (fact (name \"{facts[to_fact.strip()]}\"))))"
    s1 += f"\n?tk <- (token (name \"rule_{i}\"))"
    s1 += "\n=>"
    s1 += f"\n(retract ?tk)"
    certainty = "(* (min " + " ".join([f"?c{fact_index.strip()}" for fact_index in from_facts]) + ") 0.9)"
    s1 += f"\n(bind ?cnew {certainty})"
    s1 += f"\n(assert (fact (name \"{facts[to_fact.strip()]}\") (certainty ?cnew)))"
    s1 += f"\n(assert (sendmessage \"{str.join(", ", [facts[ind.strip()] for ind in from_facts])} -> {facts[to_fact]}\"))"
    s1 += f"\n(assert (sendmessage (str-cat \"{facts[to_fact]} \" ?cnew))))"
    out.write(s1)

    # Write second rule (if fact exists and combination is needed)
    s2 = f"\n(defrule rule{i}_2"
    for fact_index in from_facts:
        s2 += f"\n(fact (name \"{facts[fact_index.strip()]}\") (certainty ?c{fact_index.strip()}))"
    s2 += f"\n?f <- (fact (name \"{facts[to_fact.strip()]}\") (certainty ?cf_))"
    s2 += f"\n?tk <- (token (name \"rule_{i}\"))"
    s2 += "\n=>"
    s2 += f"\n(retract ?tk)"
    certainty = "(combine (* (min " + " ".join([f"?c{fact_index.strip()}" for fact_index in from_facts]) + ") 0.9) ?cf_)"
    s2 += f"\n(bind ?cnew {certainty})"
    s2 += f"\n(modify ?f (certainty ?cnew))"
    s2 += f"\n(assert (sendmessage \"{str.join(", ", [facts[ind.strip()] for ind in from_facts])} -> {facts[to_fact]}\"))"
    s2 += f"\n(assert (sendmessage (str-cat \"{facts[to_fact]} \" ?cnew))))"
    out.write(s2)


print("ye")
