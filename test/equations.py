aVar = nve(
    value = 5, #Allow for Matrix <- should ignore comments (largely follow python format
    display = \alpha_{\beta},
    units = \hertz,
    description = a different variable, but with a comma and (some brackets, commma){[(bllllu)]},
    glsType = symbol,
    ensureMath = true
)
anotherVar = nve(
    value = 100,
    units = \mega\electronvolt,
    descrition = test variable,
)
c = nve(
    value = 3e8,
    display = c,
    units = \meter\per\second,
    glsType = cst,
    ensureMath = false
)
anEq = nve(
    expr = aVar**(2/3),
    display = \eta,
    units = \giga\hertz,
    description = a sub calculation,
    lambdifyOpts = numpy,
    #specialExprOpt = 
)
scndEq = nve(
    expr = x*anEq*anotherVar/(aVar*c),
    display = \delta,
    units = \kilo\gram,
    description = calculating the thing
)
thrdEq = nve(
    expr = solve(scndEq, aVar),
    display = \rho,
    units = \mega\watt
)
