aVar = nve(
    value = 5, #Allow for Matrix <- should ignore comments (largely follow python format
    display = \alpha_{\beta},
    units = \hertz,
    description = a different variable, but with a comma and (some brackets, commma){[(bllllu)]},
    glsType = symbol,
    ensureMath = true
)
anotherVar = nve(
    symbol = \delta
    value = 100,
    units = \mega\electronvolt,
    description = test variable
)
c = nve(
    value = 3e8,
    symbol = c,
    units = \meter\per\second,
    glsType = cst,
    ensureMath = false
)
anEq = nve(
    expr = aVar**(2/3),
    symbol = \eta,
    units = \giga\hertz,
    description = a sub calculation,
    lambdifyOpts = numpy,
    #specialExprOpt = 
)
scndEq = nve(
    expr = x*anEq*anotherVar/(aVar*c),
    symbol = \delta,
    units = \kilo\gram,
    description = calculating the thing
)
thrdEq = nve(
    expr = solve(scndEq, aVar),
    symbol = \rho,
    units = \mega\watt
)
